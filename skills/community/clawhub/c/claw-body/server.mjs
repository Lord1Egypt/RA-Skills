import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import os from "os";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.NUWA_PORT || 3099;
const OPENCLAW_GATEWAY = process.env.OPENCLAW_GATEWAY || "http://localhost:18789";

// Read gateway config
const OPENCLAW_CFG_PATH = path.join(process.env.HOME, ".openclaw", "openclaw.json");
let OPENCLAW_TOKEN = process.env.OPENCLAW_GATEWAY_TOKEN || process.env.OPENCLAW_TOKEN || "";

try {
  const cfg = JSON.parse(fs.readFileSync(OPENCLAW_CFG_PATH, "utf-8"));
  if (!OPENCLAW_TOKEN) OPENCLAW_TOKEN = cfg?.gateway?.auth?.token || "";
  
  // Check (but do NOT auto-modify) chatCompletions endpoint
  const enabled = cfg?.gateway?.http?.endpoints?.chatCompletions?.enabled;
  if (!enabled) {
    console.log("   ⚠️  chatCompletions 端点未启用，语音对话将无法工作");
    console.log("   请手动添加到 ~/.openclaw/openclaw.json 并重启 Gateway:");
    console.log('   { "gateway": { "http": { "endpoints": { "chatCompletions": { "enabled": true } } } } }');
    console.log("   然后运行: openclaw gateway restart\n");
  }
} catch {}

// Demo config for 5-min free trial mode.
// These are NuwaAI-issued public demo keys with limited quota, NOT user credentials.
// They only grant access to the demo avatars below and expire per-session.
const DEMO_CONFIG = {
  zh: {
    apiKey: "sk-ody1Xk9lw_vXkRWEPnaO8OwTFB9gbCnng2EWUl5jNbzolDSlFItc9DvWqrr6RLcL",
    avatarId: "2037840977565188097",
    userId: "81936",
  },
  en: {
    apiKey: "sk-ody1Xk9lw_vXkRWEPnaO8OwTFB9gbCnng2EWUl5jNbzolDSlFItc9DvWqrr6RLcL",
    avatarId: "2037841603867942913",
    userId: "81936",
  },
};

// In-memory config store (persisted to local file)
const CONFIG_FILE = path.join(__dirname, ".nuwa-config.json");
let nuwaConfig = { apiKey: "", avatarId: "", userId: "" };
try {
  nuwaConfig = JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
} catch {}

function saveConfig() {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(nuwaConfig, null, 2));
}

const mimeTypes = {
  ".html": "text/html",
  ".js": "application/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
};

// Generate narration scripts for all slides via OpenClaw agent
async function generateNarrationScripts(outputDir) {
  const jsonPath = path.join(outputDir, "presentation.json");
  const data = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));

  const needScript = data.slides.filter(s => !s.script);
  if (needScript.length === 0) return;

  console.log(`[Presentation] Generating narration for ${needScript.length} slides...`);

  // Build a single prompt with all slides that need scripts
  const slideDescriptions = needScript.map(s => {
    const content = (s.content || []).join('\n');
    return `--- 第 ${s.page} 页 ---\n标题: ${s.title || '(无标题)'}\n内容:\n${content || '(无文字内容)'}`;
  }).join('\n\n');

  const prompt = `你是一个专业的演讲稿撰写者。请为以下演示文件的每一页生成自然、流畅的中文演讲词。

要求：
- 每页演讲词 2-4 句话，适合口语播报
- 不要照读幻灯片文字，要用自己的话讲解
- 语气轻松专业，像在给同事做分享
- 页与页之间要有自然过渡
- 严格按格式输出，每页用 [PAGE:数字] 开头

${slideDescriptions}

请按以下格式输出（每页一段）：
[PAGE:1]这里是第1页的演讲词...
[PAGE:2]这里是第2页的演讲词...`;

  const headers = { "Content-Type": "application/json" };
  if (OPENCLAW_TOKEN) headers["Authorization"] = `Bearer ${OPENCLAW_TOKEN}`;

  const resp = await fetch(`${OPENCLAW_GATEWAY}/v1/chat/completions`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      model: "openclaw:main",
      messages: [{ role: "user", content: prompt }],
    }),
  });

  const result = await resp.json();
  const reply = result.choices?.[0]?.message?.content || "";

  // Parse [PAGE:N] blocks
  const pageRegex = /\[PAGE:(\d+)\]([\s\S]*?)(?=\[PAGE:\d+\]|$)/g;
  let match;
  while ((match = pageRegex.exec(reply)) !== null) {
    const pageNum = parseInt(match[1], 10);
    const script = match[2].trim();
    const slide = data.slides.find(s => s.page === pageNum);
    if (slide && script) {
      slide.script = script;
    }
  }

  // Save back
  fs.writeFileSync(jsonPath, JSON.stringify(data, null, 2));
  const filled = data.slides.filter(s => s.script).length;
  console.log(`[Presentation] Done. ${filled}/${data.slides.length} slides have scripts.`);
}

function bufIndexOf(buf, needle, offset) {
  for (let i = offset; i <= buf.length - needle.length; i++) {
    let found = true;
    for (let j = 0; j < needle.length; j++) {
      if (buf[i + j] !== needle[j]) { found = false; break; }
    }
    if (found) return i;
  }
  return -1;
}

const server = http.createServer(async (req, res) => {
  // CORS for local dev
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.writeHead(204); res.end(); return; }

  // API: Health check proxy
  if (req.url === "/api/health" && req.method === "GET") {
    try {
      const headers = {};
      if (OPENCLAW_TOKEN) headers["Authorization"] = `Bearer ${OPENCLAW_TOKEN}`;
      const resp = await fetch(`${OPENCLAW_GATEWAY}/health`, { headers });
      const data = await resp.json();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(data));
    } catch (e) {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: false, error: e.message }));
    }
    return;
  }

  // API: Get/Set NuwaAI config
  if (req.url === "/api/config" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      avatarId: nuwaConfig.avatarId,
      userId: nuwaConfig.userId,
      hasApiKey: !!nuwaConfig.apiKey,
      gateway: OPENCLAW_GATEWAY,
      configured: !!(nuwaConfig.apiKey && nuwaConfig.avatarId && nuwaConfig.userId),
    }));
    return;
  }

  if (req.url === "/api/config" && req.method === "POST") {
    let body = "";
    for await (const chunk of req) body += chunk;
    try {
      const { apiKey, avatarId, userId } = JSON.parse(body);
      if (apiKey !== undefined) nuwaConfig.apiKey = apiKey;
      if (avatarId !== undefined) nuwaConfig.avatarId = avatarId;
      if (userId !== undefined) nuwaConfig.userId = userId;
      saveConfig();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true, configured: !!(nuwaConfig.apiKey && nuwaConfig.avatarId && nuwaConfig.userId) }));
    } catch (e) {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // API: Get demo/trial config
  if (req.url?.startsWith("/api/demo") && req.method === "GET") {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const lang = url.searchParams.get("lang") === "en" ? "en" : "zh";
    const demo = DEMO_CONFIG[lang];

    // /api/demo — just config info
    if (url.pathname === "/api/demo") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ avatarId: demo.avatarId, userId: demo.userId }));
      return;
    }

    // /api/demo/token — get access token
    if (url.pathname === "/api/demo/token") {
      try {
        const resp = await fetch("https://api.nuwaai.com/web/apiKey/auth", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ secretKey: demo.apiKey }),
        });
        const data = await resp.json();
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ...data, avatarId: demo.avatarId }));
      } catch (e) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ code: -1, msg: e.message }));
      }
      return;
    }
  }

  // API: Get NuwaAI access token
  if (req.url === "/api/token" && req.method === "GET") {
    if (!nuwaConfig.apiKey) {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ code: -1, msg: "API Key 未配置" }));
      return;
    }
    try {
      const resp = await fetch("https://api.nuwaai.com/web/apiKey/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secretKey: nuwaConfig.apiKey }),
      });
      const data = await resp.json();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(data));
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ code: -1, msg: e.message }));
    }
    return;
  }

  // API: Chat with OpenClaw (non-streaming fallback)
  if (req.url === "/api/chat" && req.method === "POST") {
    let body = "";
    for await (const chunk of req) body += chunk;
    try {
      const { message, sessionKey = "agent:main:claw-body" } = JSON.parse(body);
      const headers = { "Content-Type": "application/json" };
      if (OPENCLAW_TOKEN) headers["Authorization"] = `Bearer ${OPENCLAW_TOKEN}`;
      headers["x-openclaw-session-key"] = sessionKey;

      const resp = await fetch(`${OPENCLAW_GATEWAY}/v1/chat/completions`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          model: "openclaw:main",
          messages: [{ role: "user", content: message }],
        }),
      });
      const data = await resp.json();
      const reply = data.choices?.[0]?.message?.content || data.error?.message || "...";
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ reply }));
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // API: Chat with OpenClaw (streaming SSE)
  if (req.url === "/api/chat/stream" && req.method === "POST") {
    let body = "";
    for await (const chunk of req) body += chunk;
    try {
      const { message, sessionKey = "agent:main:claw-body" } = JSON.parse(body);
      const headers = { "Content-Type": "application/json" };
      if (OPENCLAW_TOKEN) headers["Authorization"] = `Bearer ${OPENCLAW_TOKEN}`;
      headers["x-openclaw-session-key"] = sessionKey;

      const resp = await fetch(`${OPENCLAW_GATEWAY}/v1/chat/completions`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          model: "openclaw:main",
          messages: [{ role: "user", content: message }],
          stream: true,
        }),
      });

      if (!resp.ok) {
        const errText = await resp.text();
        res.writeHead(resp.status, { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", "Connection": "keep-alive" });
        res.write(`data: ${JSON.stringify({ error: errText })}\n\n`);
        res.end();
        return;
      }

      res.writeHead(200, {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
      });

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith("data: ")) continue;
          const data = trimmed.slice(6);
          if (data === "[DONE]") {
            res.write("data: [DONE]\n\n");
            continue;
          }
          try {
            const parsed = JSON.parse(data);
            const content = parsed.choices?.[0]?.delta?.content;
            if (content) {
              res.write(`data: ${JSON.stringify({ content })}\n\n`);
            }
          } catch {}
        }
      }
      res.end();
    } catch (e) {
      if (!res.headersSent) {
        res.writeHead(500, { "Content-Type": "text/event-stream" });
      }
      res.write(`data: ${JSON.stringify({ error: e.message })}\n\n`);
      res.end();
    }
    return;
  }

  // API: List all presentations
  if (req.url === "/api/presentations" && req.method === "GET") {
    const presRoot = path.join(process.env.HOME, "Desktop", "openclaw", "work", "presentations");
    try {
      if (!fs.existsSync(presRoot)) {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify([]));
        return;
      }
      const dirs = fs.readdirSync(presRoot, { withFileTypes: true })
        .filter(d => d.isDirectory())
        .map(d => {
          const jsonPath = path.join(presRoot, d.name, "presentation.json");
          try {
            const data = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));
            const hasScripts = data.slides?.some(s => s.script);
            const hasImages = fs.existsSync(path.join(presRoot, d.name, "slides"));
            return {
              name: d.name,
              source: data.source || d.name,
              totalPages: data.total_pages || 0,
              hasScripts,
              hasImages,
              ready: hasScripts && hasImages,
              dir: path.join(presRoot, d.name),
            };
          } catch { return null; }
        })
        .filter(Boolean);
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(dirs));
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // API: Upload and parse a presentation file
  if (req.url === "/api/presentations/upload" && req.method === "POST") {
    try {
      const chunks = [];
      for await (const chunk of req) chunks.push(chunk);
      const buf = Buffer.concat(chunks);
      const contentType = req.headers["content-type"] || "";
      const boundaryMatch = contentType.match(/boundary=(.+)/);
      if (!boundaryMatch) { res.writeHead(400, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "no boundary" })); return; }

      const boundary = Buffer.from("--" + boundaryMatch[1]);
      // Find file content between boundaries
      let start = bufIndexOf(buf, boundary, 0);
      if (start === -1) { res.writeHead(400, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "bad multipart" })); return; }
      start += boundary.length + 2; // skip boundary + \r\n
      const end = bufIndexOf(buf, boundary, start);
      if (end === -1) { res.writeHead(400, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "bad multipart" })); return; }
      const partBuf = buf.slice(start, end - 2); // -2 for trailing \r\n

      // Find header/body separator
      const sep = Buffer.from("\r\n\r\n");
      const sepIdx = bufIndexOf(partBuf, sep, 0);
      if (sepIdx === -1) { res.writeHead(400, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "bad part" })); return; }
      const headerStr = partBuf.slice(0, sepIdx).toString("utf-8");
      const fileBody = partBuf.slice(sepIdx + 4);

      // Extract filename
      const fnMatch = headerStr.match(/filename="([^"]+)"/);
      const filename = fnMatch ? fnMatch[1] : "upload.pptx";
      const tmpPath = path.join(os.tmpdir(), "claw-upload-" + Date.now() + "-" + filename);
      fs.writeFileSync(tmpPath, fileBody);

      const { execSync } = await import("child_process");
      const scriptPath = path.join(process.env.HOME, "Desktop", "openclaw", "work", "skills", "claw-presenter", "scripts", "parse-presentation.py");
      if (!fs.existsSync(scriptPath)) { res.writeHead(500, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "parse script not found" })); return; }
      const result = execSync(`python3 "${scriptPath}" "${tmpPath}"`, {
        encoding: "utf-8", timeout: 120000,
        env: { ...process.env, OPENCLAW_WORKSPACE: path.join(process.env.HOME, "Desktop", "openclaw", "work") },
      });
      try { fs.unlinkSync(tmpPath); } catch {}
      const parsed = JSON.parse(result);

      // Auto-generate narration scripts via OpenClaw agent
      if (parsed.status === "ok" && parsed.output_dir) {
        try {
          await generateNarrationScripts(parsed.output_dir);
        } catch (e) {
          console.error("[Presentation] Narration generation failed:", e.message);
        }
      }

      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(parsed));
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.stderr?.toString() || e.message }));
    }
    return;
  }

  // API: Parse a new presentation file
  if (req.url === "/api/presentations/parse" && req.method === "POST") {
    let body = "";
    for await (const chunk of req) body += chunk;
    try {
      const { filePath: fpArg } = JSON.parse(body);
      if (!fpArg) { res.writeHead(400, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "missing filePath" })); return; }
      const fp = fpArg.replace(/^~/, process.env.HOME);
      const { execSync } = await import("child_process");
      // Try claw-presenter script first, fallback to claw-body's copy
      const scriptCandidates = [
        path.join(process.env.HOME, "Desktop", "openclaw", "work", "skills", "claw-presenter", "scripts", "parse-presentation.py"),
        path.join(__dirname, "scripts", "parse-presentation.py"),
      ];
      let scriptPath = scriptCandidates.find(s => fs.existsSync(s));
      if (!scriptPath) { res.writeHead(500, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "parse script not found" })); return; }
      const result = execSync(`python3 "${scriptPath}" "${fp}"`, {
        encoding: "utf-8", timeout: 120000,
        env: { ...process.env, OPENCLAW_WORKSPACE: path.join(process.env.HOME, "Desktop", "openclaw", "work") },
      });
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(result);
    } catch (e) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: e.stderr || e.message }));
    }
    return;
  }

  // API: Serve presentation data
  if (req.url?.startsWith("/api/presentation/") && req.method === "GET") {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const presDir = url.searchParams.get("dir");
    if (!presDir) {
      res.writeHead(400, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "missing dir param" }));
      return;
    }

    const subPath = url.pathname.replace("/api/presentation/", "");

    if (subPath === "data") {
      // Return presentation.json
      const jsonPath = path.join(presDir, "presentation.json");
      try {
        const data = fs.readFileSync(jsonPath, "utf-8");
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(data);
      } catch {
        res.writeHead(404, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "presentation not found" }));
      }
      return;
    }

    if (subPath.startsWith("slide/")) {
      // Return slide image: /api/presentation/slide/001.png?dir=...
      const imgName = subPath.replace("slide/", "");
      const imgPath = path.resolve(presDir, "slides", imgName);
      // Security: must be inside presDir
      if (!imgPath.startsWith(path.resolve(presDir))) {
        res.writeHead(403); res.end("Forbidden"); return;
      }
      try {
        const content = fs.readFileSync(imgPath);
        const ext = path.extname(imgPath);
        res.writeHead(200, { "Content-Type": mimeTypes[ext] || "image/png" });
        res.end(content);
      } catch {
        res.writeHead(404); res.end("Not found");
      }
      return;
    }

    res.writeHead(404); res.end("Not found");
    return;
  }

  // Static files
  let filePath = req.url === "/" ? "/index.html" : req.url.split("?")[0];
  const publicDir = path.join(__dirname, "public");
  filePath = path.resolve(publicDir, "." + filePath);

  // Path traversal protection
  if (!filePath.startsWith(publicDir)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  const ext = path.extname(filePath);
  const contentType = mimeTypes[ext] || "application/octet-stream";

  try {
    const content = fs.readFileSync(filePath);
    res.writeHead(200, { "Content-Type": contentType, "Cache-Control": "no-cache, no-store, must-revalidate" });
    res.end(content);
  } catch {
    res.writeHead(404);
    res.end("Not found");
  }
});

const BIND = process.env.NUWA_BIND || "127.0.0.1";
server.listen(PORT, BIND, () => {
  console.log(`\n🦞 Claw Body — 龙虾真身已启动`);
  console.log(`   打开浏览器: http://localhost:${PORT}`);
  console.log(`   OpenClaw Gateway: ${OPENCLAW_GATEWAY}`);
  if (nuwaConfig.avatarId) {
    console.log(`   形象 ID: ${nuwaConfig.avatarId}`);
  } else {
    console.log(`   ⚠️  首次使用，请在网页中配置你的龙虾形象`);
  }
  console.log();
});

// Graceful shutdown
function shutdown() {
  console.log("\n🦞 Claw Body — 正在关闭...");
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 3000);
}
process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);
