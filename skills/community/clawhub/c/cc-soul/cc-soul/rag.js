import { existsSync, readFileSync } from "fs";
import { extname } from "path";
import { spawnCLI } from "./cli.ts";
import { addMemory } from "./memory.ts";
const URL_PATTERN = /https?:\/\/[^\s<>"']+/g;
const MAX_CHUNK_SIZE = 500;
function shouldIngest(msg) {
  URL_PATTERN.lastIndex = 0;
  if (URL_PATTERN.test(msg) && (msg.includes("\u8BB0\u4F4F") || msg.includes("remember") || msg.includes("\u8BFB\u4E00\u4E0B") || msg.includes("read this"))) {
    return true;
  }
  if (msg.length > 1e3 && (msg.includes("\u8BB0\u4F4F\u8FD9\u4E2A") || msg.includes("remember this") || msg.includes("\u5B58\u4E00\u4E0B") || msg.includes("save this"))) {
    return true;
  }
  return false;
}
function extractUrl(msg) {
  URL_PATTERN.lastIndex = 0;
  const match = msg.match(URL_PATTERN);
  return match ? match[0] : null;
}
function chunkMarkdown(text, maxSize = MAX_CHUNK_SIZE) {
  const sections = text.split(/^(?=##\s)/m);
  if (sections.length <= 1) return chunkByParagraph(text, maxSize);
  const result = [];
  for (const section of sections) {
    if (section.length <= maxSize) {
      if (section.trim().length > 10) result.push(section.trim());
    } else {
      result.push(...chunkByParagraph(section, maxSize));
    }
  }
  return result;
}
function chunkCode(text, maxSize = MAX_CHUNK_SIZE) {
  const defPattern = /^(?:export\s+)?(?:async\s+)?(?:function|class|def|fn|func|impl|interface|type|struct|enum)\s/m;
  const lines = text.split("\n");
  const chunks = [];
  let current = [];
  for (const line of lines) {
    if (defPattern.test(line) && current.length > 0) {
      const block = current.join("\n").trim();
      if (block.length > 10) {
        if (block.length <= maxSize) chunks.push(block);
        else chunks.push(...chunkByParagraph(block, maxSize));
      }
      current = [];
    }
    current.push(line);
  }
  if (current.length > 0) {
    const block = current.join("\n").trim();
    if (block.length > 10) {
      if (block.length <= maxSize) chunks.push(block);
      else chunks.push(...chunkByParagraph(block, maxSize));
    }
  }
  return chunks;
}
function chunkByParagraph(text, maxSize = MAX_CHUNK_SIZE) {
  const chunks = [];
  const paragraphs = text.split(/\n\n+/);
  let current = "";
  for (const para of paragraphs) {
    if (current.length + para.length > maxSize && current.length > 0) {
      chunks.push(current.trim());
      current = para;
    } else {
      current += (current ? "\n\n" : "") + para;
    }
  }
  if (current.trim()) chunks.push(current.trim());
  const result = [];
  for (const chunk of chunks) {
    if (chunk.length <= maxSize) {
      result.push(chunk);
    } else {
      const sentences = chunk.split(/[。！？.!?\n]+/);
      let buf = "";
      for (const sent of sentences) {
        if (buf.length + sent.length > maxSize && buf.length > 0) {
          result.push(buf.trim());
          buf = sent;
        } else {
          buf += (buf ? "\u3002" : "") + sent;
        }
      }
      if (buf.trim()) result.push(buf.trim());
    }
  }
  return result.filter((c) => c.length > 10);
}
function detectPaper(text) {
  const markers = ["abstract", "introduction", "conclusion", "references", "methodology", "related work"];
  const found = markers.filter((m) => new RegExp(`^\\s*(?:\\d+\\.?\\s*)?${m}`, "im").test(text));
  if (found.length < 3) return null;
  const title = text.split("\n").find((l) => l.trim().length > 5)?.trim() || "Untitled Paper";
  const absMatch = text.match(/abstract[:\s]*\n?([\s\S]*?)(?=\n\s*(?:\d+\.?\s*)?(?:introduction|keywords|1\s))/im);
  const abstract = absMatch?.[1]?.trim().slice(0, 800) || "";
  const concMatch = text.match(/conclusions?[:\s]*\n?([\s\S]*?)(?=\n\s*(?:\d+\.?\s*)?(?:references|acknowledgment|appendix))/im);
  const conclusions = concMatch?.[1]?.trim().slice(0, 800) || "";
  return { title, abstract, conclusions };
}
function chunkPaper(text, maxSize = MAX_CHUNK_SIZE) {
  const sections = text.split(/\n(?=\s*(?:\d+\.?\s*)?(?:abstract|introduction|related work|methodology|method|experiment|result|discussion|conclusion|references)\b)/im);
  const chunks = [];
  for (const section of sections) {
    const trimmed = section.trim();
    if (trimmed.length < 15) continue;
    if (trimmed.length <= maxSize) {
      chunks.push(trimmed);
    } else {
      chunks.push(...chunkByParagraph(trimmed, maxSize));
    }
  }
  return chunks;
}
function chunkText(text, maxSize = MAX_CHUNK_SIZE, ext) {
  if (ext === ".md" || ext === ".markdown") return chunkMarkdown(text, maxSize);
  const codeExts = [".ts", ".js", ".py", ".rs", ".go", ".java", ".swift", ".c", ".cpp", ".h", ".m"];
  if (ext && codeExts.includes(ext)) return chunkCode(text, maxSize);
  if (detectPaper(text)) return chunkPaper(text, maxSize);
  return chunkByParagraph(text, maxSize);
}
function ingestUrl(url, userId, channelId) {
  console.log(`[cc-soul][rag] ingesting URL: ${url}`);
  spawnCLI(
    `Read the content from this URL and extract the key information. Return ONLY the main text content (no HTML, no navigation, no ads). If it's too long, summarize the key points.

URL: ${url}`,
    (output) => {
      if (!output || output.length < 50) {
        console.log(`[cc-soul][rag] URL fetch returned empty/short content`);
        return;
      }
      if (output.length > 5 * 1024 * 1024) {
        console.log(`[cc-soul][rag] URL content too large (>${(output.length / 1024 / 1024).toFixed(1)}MB), skipping`);
        return;
      }
      const chunks = chunkText(output, MAX_CHUNK_SIZE);
      let stored = 0;
      for (const chunk of chunks.slice(0, 20)) {
        addMemory(`[doc:${url.slice(0, 50)}] ${chunk}`, "fact", userId, "global", channelId);
        stored++;
      }
      console.log(`[cc-soul][rag] stored ${stored} chunks from ${url}`);
    },
    1e4
    // 10s timeout for URL fetching
  );
}
function ingestText(text, source, userId, channelId) {
  const chunks = chunkText(text, MAX_CHUNK_SIZE);
  let stored = 0;
  for (const chunk of chunks.slice(0, 30)) {
    addMemory(`[doc:${source.slice(0, 30)}] ${chunk}`, "fact", userId, "global", channelId);
    stored++;
  }
  console.log(`[cc-soul][rag] stored ${stored} text chunks (source: ${source})`);
  return stored;
}
function ingestFile(filePath, userId, channelId) {
  if (!existsSync(filePath)) {
    console.log(`[cc-soul][rag] file not found: ${filePath}`);
    return -1;
  }
  try {
    const text = readFileSync(filePath, "utf-8");
    if (!text || text.length < 10) {
      console.log(`[cc-soul][rag] file too short: ${filePath}`);
      return 0;
    }
    const ext = extname(filePath).toLowerCase();
    const source = filePath.split("/").pop() || filePath.slice(0, 30);
    const paper = detectPaper(text);
    if (paper) {
      const summary = `[paper:${source}] Title: ${paper.title}
Abstract: ${paper.abstract}
Conclusions: ${paper.conclusions}`;
      addMemory(summary, "paper", userId, "global", channelId);
      console.log(`[cc-soul][rag] detected paper "${paper.title}" \u2014 stored summary`);
    }
    const chunks = paper ? chunkPaper(text, MAX_CHUNK_SIZE) : chunkText(text, MAX_CHUNK_SIZE, ext);
    let stored = paper ? 1 : 0;
    for (const chunk of chunks.slice(0, 50)) {
      addMemory(`[doc:${source}] ${chunk}`, "fact", userId, "global", channelId);
      stored++;
    }
    console.log(`[cc-soul][rag] ingested file "${filePath}": ${stored} chunks (ext: ${ext})`);
    return stored;
  } catch (err) {
    console.log(`[cc-soul][rag] failed to read file "${filePath}": ${err.message}`);
    return -1;
  }
}
function processIngestion(msg, userId, channelId) {
  if (!shouldIngest(msg)) return "";
  const url = extractUrl(msg);
  if (url) {
    ingestUrl(url, userId, channelId);
    return `[document ingestion] Reading and storing content from ${url}. It will be available in memory for future conversations.`;
  }
  if (msg.length > 1e3) {
    const preview = msg.slice(0, 50);
    const count = ingestText(msg, preview, userId, channelId);
    return `[document ingestion] Stored ${count} knowledge chunks from pasted text.`;
  }
  return "";
}
const ragModule = {
  id: "rag",
  name: "RAG \u68C0\u7D22\u589E\u5F3A",
  dependencies: ["memory"],
  priority: 50
};
export {
  ingestFile,
  ingestText,
  ingestUrl,
  processIngestion,
  ragModule,
  shouldIngest
};
