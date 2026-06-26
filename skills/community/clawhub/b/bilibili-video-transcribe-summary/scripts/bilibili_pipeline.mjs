import { createWriteStream } from "node:fs";
import { mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { pipeline } from "node:stream/promises";

const READY_FILE_NAME = ".skill-ready.json";

function fail(message, code = 1) {
  console.error(message);
  process.exit(code);
}

function ensureNodeVersion() {
  const major = Number.parseInt(process.versions.node.split(".")[0], 10);
  if (Number.isNaN(major) || major < 18) {
    fail(`Node.js 18+ is required. Current version: ${process.versions.node}`);
  }
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith("--")) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    } else {
      args._.push(token);
    }
  }
  return args;
}

function normalizeVideoUrl(value) {
  if (!value) {
    fail("Missing Bilibili URL or BV id.");
  }

  if (/^BV[0-9A-Za-z]+$/i.test(value)) {
    return `https://www.bilibili.com/video/${value}`;
  }

  try {
    const url = new URL(value);
    return url.toString();
  } catch {
    fail(`Unsupported input: ${value}`);
  }
}

const USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36";

function buildHeaders(extra = {}) {
  return {
    "user-agent": USER_AGENT,
    accept:
      "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    referer: "https://www.bilibili.com/",
    ...extra,
  };
}

async function fetchText(url, headers = {}) {
  const response = await fetch(url, {
    headers: buildHeaders(headers),
    redirect: "follow",
  });
  return {
    ok: response.ok,
    status: response.status,
    url: response.url,
    text: await response.text(),
  };
}

async function fetchJson(url, headers = {}) {
  const response = await fetch(url, {
    headers: buildHeaders({
      accept: "application/json,text/plain,*/*",
      ...headers,
    }),
    redirect: "follow",
  });
  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    json = null;
  }
  return {
    ok: response.ok,
    status: response.status,
    url: response.url,
    text,
    json,
  };
}

function extractJsonBlock(html, token) {
  const start = html.indexOf(token);
  if (start === -1) {
    return null;
  }

  let i = start + token.length;
  while (i < html.length && /\s/.test(html[i])) {
    i += 1;
  }

  if (html[i] !== "{") {
    return null;
  }

  let depth = 0;
  let inString = false;
  let escaped = false;
  const begin = i;

  for (; i < html.length; i += 1) {
    const ch = html[i];
    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === '"') {
        inString = false;
      }
      continue;
    }

    if (ch === '"') {
      inString = true;
      continue;
    }

    if (ch === "{") {
      depth += 1;
      continue;
    }

    if (ch === "}") {
      depth -= 1;
      if (depth === 0) {
        return html.slice(begin, i + 1);
      }
    }
  }

  return null;
}

function simplifyPlayInfo(playInfo) {
  if (!playInfo?.data) {
    return {};
  }

  return {
    quality: playInfo.data.quality,
    format: playInfo.data.format,
    timelength: playInfo.data.timelength,
    accept_quality: playInfo.data.accept_quality ?? [],
    accept_description: playInfo.data.accept_description ?? [],
    durl: Array.isArray(playInfo.data.durl)
      ? playInfo.data.durl.map((item) => ({
          size: item.size,
          length: item.length,
          url: item.url,
          backup_url: item.backup_url ?? [],
        }))
      : [],
    dash: {
      video: Array.isArray(playInfo.data.dash?.video)
        ? playInfo.data.dash.video.map((item) => ({
            id: item.id,
            codecid: item.codecid,
            bandwidth: item.bandwidth,
            baseUrl: item.baseUrl ?? item.base_url,
            backupUrl: item.backupUrl ?? item.backup_url ?? [],
          }))
        : [],
      audio: Array.isArray(playInfo.data.dash?.audio)
        ? playInfo.data.dash.audio.map((item) => ({
            id: item.id,
            bandwidth: item.bandwidth,
            baseUrl: item.baseUrl ?? item.base_url,
            backupUrl: item.backupUrl ?? item.backup_url ?? [],
          }))
        : [],
    },
  };
}

function normalizeSubtitleUrl(value) {
  if (!value) {
    return null;
  }
  if (value.startsWith("//")) {
    return `https:${value}`;
  }
  if (value.startsWith("http://") || value.startsWith("https://")) {
    return value;
  }
  return `https://${value.replace(/^\/+/, "")}`;
}

function readyFilePath(outputDir) {
  return resolve(outputDir, READY_FILE_NAME);
}

async function markReady(outputDir, apiKeyFound) {
  const payload = {
    version: 1,
    created_at: new Date().toISOString(),
    node_version: process.versions.node,
    api_key_found: Boolean(apiKeyFound),
  };
  await writeFile(readyFilePath(outputDir), JSON.stringify(payload, null, 2), "utf8");
}

async function probeVideo(inputUrl) {
  const videoUrl = normalizeVideoUrl(inputUrl);
  const page = await fetchText(videoUrl);

  const result = {
    input: inputUrl,
    requested_url: videoUrl,
    final_page_url: page.url,
    page_status: page.status,
    title: null,
    bvid: null,
    aid: null,
    cid: null,
    subtitles: [],
    subtitle_text: null,
    playinfo: {},
    errors: [],
  };

  const initialStateRaw =
    extractJsonBlock(page.text, "window.__INITIAL_STATE__=") ??
    extractJsonBlock(page.text, "__INITIAL_STATE__=");
  const playInfoRaw =
    extractJsonBlock(page.text, "window.__playinfo__=") ??
    extractJsonBlock(page.text, "__playinfo__=");

  if (initialStateRaw) {
    try {
      const initialState = JSON.parse(initialStateRaw);
      result.title = initialState?.videoData?.title ?? null;
      result.bvid = initialState?.bvid ?? initialState?.videoData?.bvid ?? null;
      result.aid = initialState?.aid ?? initialState?.videoData?.aid ?? null;
      const pages = initialState?.videoData?.pages ?? [];
      result.cid = pages[0]?.cid ?? initialState?.videoData?.cid ?? null;
    } catch (error) {
      result.errors.push(`Failed to parse __INITIAL_STATE__: ${error.message}`);
    }
  } else {
    result.errors.push("Page does not contain __INITIAL_STATE__.");
  }

  if (!result.bvid) {
    const match = page.url.match(/\/video\/(BV[0-9A-Za-z]+)/i);
    if (match) {
      result.bvid = match[1];
    }
  }

  if (playInfoRaw) {
    try {
      result.playinfo = simplifyPlayInfo(JSON.parse(playInfoRaw));
    } catch (error) {
      result.errors.push(`Failed to parse __playinfo__: ${error.message}`);
    }
  }

  if (result.bvid && result.cid) {
    const subtitleApi = `https://api.bilibili.com/x/player/v2?bvid=${encodeURIComponent(
      result.bvid
    )}&cid=${encodeURIComponent(result.cid)}`;
    const subtitleResponse = await fetchJson(subtitleApi);
    const subtitleItems = subtitleResponse.json?.data?.subtitle?.subtitles ?? [];
    result.subtitles = subtitleItems.map((item) => ({
      id: item.id,
      lan: item.lan,
      lan_doc: item.lan_doc,
      subtitle_url: normalizeSubtitleUrl(item.subtitle_url),
    }));

    if (result.subtitles.length > 0) {
      const subtitleUrl = result.subtitles[0].subtitle_url;
      const subtitleFile = await fetchJson(subtitleUrl, { referer: page.url });
      const body = subtitleFile.json?.body ?? [];
      if (Array.isArray(body) && body.length > 0) {
        result.subtitle_text = body
          .map((item) => String(item.content ?? "").trim())
          .filter(Boolean)
          .join("\n");
      }
    }
  }

  return result;
}

function pickBestAudio(playinfo) {
  const audios = Array.isArray(playinfo?.dash?.audio) ? [...playinfo.dash.audio] : [];
  if (audios.length === 0) {
    return null;
  }
  audios.sort((a, b) => (b.bandwidth ?? 0) - (a.bandwidth ?? 0));
  return audios[0];
}

async function downloadToFile(url, outputPath, referer) {
  const response = await fetch(url, {
    headers: buildHeaders({
      accept: "*/*",
      referer,
    }),
    redirect: "follow",
  });

  if (!response.ok || !response.body) {
    throw new Error(`Download failed: HTTP ${response.status}`);
  }

  await mkdir(dirname(outputPath), { recursive: true });
  await pipeline(response.body, createWriteStream(outputPath));
}

function emitResult(summary, transcriptText) {
  console.log(JSON.stringify(summary, null, 2));
  if (typeof transcriptText === "string" && transcriptText.trim()) {
    console.log("\n===TRANSCRIPT===\n");
    console.log(transcriptText);
  }
}

async function transcribeWithSiliconFlow(filePath, apiKey, model) {
  if (!apiKey) {
    throw new Error(
      "Missing SiliconFlow API key. Set SILICONFLOW_API_KEY or pass --api-key <key>."
    );
  }

  const buffer = await readFile(filePath);
  const form = new FormData();
  form.append("file", new Blob([buffer], { type: "audio/mpeg" }), "audio.mp3");
  form.append("model", model);

  const response = await fetch("https://api.siliconflow.cn/v1/audio/transcriptions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
    },
    body: form,
  });

  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    json = null;
  }

  if (!response.ok) {
    throw new Error(`SiliconFlow transcription failed: HTTP ${response.status} ${text}`);
  }

  return {
    status: response.status,
    json,
    rawText: text,
  };
}

async function runProbe(url, outputDir, apiKey) {
  const result = await probeVideo(url);
  await mkdir(outputDir, { recursive: true });
  const out = resolve(outputDir, "probe_result.json");
  await writeFile(out, JSON.stringify(result, null, 2), "utf8");
  await markReady(outputDir, apiKey);
  emitResult(
    {
      saved: out,
      ready_file: readyFilePath(outputDir),
      title: result.title,
      bvid: result.bvid,
      cid: result.cid,
      subtitleCount: result.subtitles.length,
      hasAudio: Boolean(pickBestAudio(result.playinfo)),
    },
    result.subtitle_text
  );
}

async function runPipeline(url, outputDir, apiKey, model) {
  const result = await probeVideo(url);
  await mkdir(outputDir, { recursive: true });
  const probePath = resolve(outputDir, "probe_result.json");
  await writeFile(probePath, JSON.stringify(result, null, 2), "utf8");

  const summary = {
    probe_path: probePath,
    ready_file: readyFilePath(outputDir),
    title: result.title,
    subtitle_used: false,
    transcript_path: null,
    audio_mp3_path: null,
    transcription_json_path: null,
    notes: [],
  };

  if (result.subtitle_text) {
    const transcriptPath = resolve(outputDir, "transcript.txt");
    await writeFile(transcriptPath, `${result.subtitle_text}\n`, "utf8");
    summary.subtitle_used = true;
    summary.transcript_path = transcriptPath;
    summary.notes.push("Used official subtitle text, so no transcription API call was needed.");
    await markReady(outputDir, apiKey);
    emitResult(summary, result.subtitle_text);
    return;
  }

  const audio = pickBestAudio(result.playinfo);
  if (!audio?.baseUrl) {
    summary.notes.push("No anonymous audio URL was found in the page playinfo.");
    emitResult(summary, null);
    return;
  }

  const m4sPath = resolve(outputDir, "audio.m4s");
  const mp3Path = resolve(outputDir, "audio.mp3");
  await downloadToFile(audio.baseUrl, m4sPath, result.final_page_url);
  try {
    await rm(mp3Path, { force: true });
  } catch {
  }
  await rename(m4sPath, mp3Path);
  summary.audio_mp3_path = mp3Path;
  summary.notes.push("Downloaded the anonymous Bilibili audio stream and renamed .m4s to .mp3 without transcoding.");

  if (!apiKey) {
    summary.notes.push("Skipping transcription because SILICONFLOW_API_KEY is missing.");
    await markReady(outputDir, false);
    emitResult(summary, null);
    return;
  }

  const transcription = await transcribeWithSiliconFlow(mp3Path, apiKey, model);
  const transcriptionJsonPath = resolve(outputDir, "transcription_result.json");
  await writeFile(transcriptionJsonPath, JSON.stringify(transcription.json ?? { raw: transcription.rawText }, null, 2), "utf8");
  summary.transcription_json_path = transcriptionJsonPath;

  const transcriptText = transcription.json?.text;
  if (typeof transcriptText === "string" && transcriptText.trim()) {
    const transcriptPath = resolve(outputDir, "transcript.txt");
    await writeFile(transcriptPath, `${transcriptText}\n`, "utf8");
    summary.transcript_path = transcriptPath;
  } else {
    summary.notes.push("SiliconFlow returned no usable text field.");
  }

  await markReady(outputDir, true);
  emitResult(summary, transcriptText);
}

async function main() {
  ensureNodeVersion();
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];
  const url = args._[1];
  const outputDir = resolve(args["output-dir"] ?? "./output");
  const apiKey = args["api-key"] ?? process.env.SILICONFLOW_API_KEY ?? "";
  const model = args.model ?? "TeleAI/TeleSpeechASR";

  if (!command || !["probe", "run"].includes(command)) {
    fail(
      "Usage:\n  node scripts/bilibili_pipeline.mjs probe <url> [--output-dir ./output]\n  node scripts/bilibili_pipeline.mjs run <url> [--output-dir ./output] [--api-key <key>] [--model TeleAI/TeleSpeechASR]"
    );
  }

  if (command === "probe") {
    await runProbe(url, outputDir, apiKey);
    return;
  }

  await runPipeline(url, outputDir, apiKey, model);
}

main().catch((error) => fail(error.stack || error.message));