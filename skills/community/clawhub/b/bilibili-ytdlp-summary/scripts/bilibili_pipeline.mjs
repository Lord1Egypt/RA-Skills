import { execSync, spawn } from "node:child_process";
import { createWriteStream } from "node:fs";
import { mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { pipeline } from "node:stream/promises";

const READY_FILE_NAME = ".skill-ready.json";

function fail(message, code = 1) {
  console.error(message);
  process.exit(code);
}

function requireBin(name) {
  try {
    execSync(`which "${name}"`, { stdio: "ignore" });
  } catch {
    fail(`Required binary not found: ${name}. Install it first.`);
  }
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (token.startsWith("--")) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
        args[key] = true;
      } else {
        args[key] = next;
        i++;
      }
    } else {
      args._.push(token);
    }
  }
  return args;
}

function normalizeUrl(value) {
  if (!value) fail("Missing Bilibili URL or BV id.");
  if (/^BV[0-9A-Za-z]+$/i.test(value)) {
    return `https://www.bilibili.com/video/${value}`;
  }
  try {
    return new URL(value).toString();
  } catch {
    fail(`Unsupported input: ${value}`);
  }
}

function ytdlJson(url) {
  const out = execSync(
    `yt-dlp --dump-json --no-playlist --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" --add-headers "Referer:https://www.bilibili.com/" ${JSON.stringify(url)}`,
    { encoding: "utf-8", maxBuffer: 10 * 1024 * 1024 }
  );
  return JSON.parse(out.trim());
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
      Referer: "https://www.bilibili.com/",
      Accept: "application/json,text/plain,*/*",
    },
  });
  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {}
  return { ok: response.ok, status: response.status, json, text };
}

function normalizeSubtitleUrl(value) {
  if (!value) return null;
  if (value.startsWith("//")) return `https:${value}`;
  if (value.startsWith("http://") || value.startsWith("https://")) return value;
  return `https://${value.replace(/^\/+/, "")}`;
}

function readyFilePath(outputDir) {
  return resolve(outputDir, READY_FILE_NAME);
}

async function markReady(outputDir, apiKeyFound) {
  await writeFile(
    readyFilePath(outputDir),
    JSON.stringify(
      { version: 2, created_at: new Date().toISOString(), node_version: process.versions.node, api_key_found: Boolean(apiKeyFound) },
      null,
      2
    ),
    "utf8"
  );
}

async function probeVideo(inputUrl) {
  const videoUrl = normalizeUrl(inputUrl);
  const info = ytdlJson(videoUrl);

  const result = {
    input: inputUrl,
    requested_url: videoUrl,
    title: info.title ?? null,
    bvid: info.id ?? null,
    duration: info.duration ?? null,
    webpage_url: info.webpage_url ?? videoUrl,
    subtitles: [],
    subtitle_text: null,
    audio_formats: [],
  };

  // Fetch official subtitles from B站 API
  if (result.bvid && info.cid_comments) {
    const apiUrl = `https://api.bilibili.com/x/player/v2?bvid=${encodeURIComponent(result.bvid)}&cid=${encodeURIComponent(info.cid_comments || info.cid)}`;
    const subResp = await fetchJson(apiUrl);
    const subtitleItems = subResp.json?.data?.subtitle?.subtitles ?? [];
    result.subtitles = subtitleItems.map((item) => ({
      id: item.id,
      lan: item.lan,
      lan_doc: item.lan_doc,
      subtitle_url: normalizeSubtitleUrl(item.subtitle_url),
    }));

    if (result.subtitles.length > 0) {
      const subUrl = result.subtitles[0].subtitle_url;
      const subFile = await fetchJson(subUrl);
      const body = subFile.json?.body ?? [];
      if (Array.isArray(body) && body.length > 0) {
        result.subtitle_text = body.map((i) => String(i.content ?? "").trim()).filter(Boolean).join("\n");
      }
    }
  }

  // Audio formats from yt-dlp
  const audioOnly = (info.formats ?? []).filter((f) => f.vcodec === "none" && f.acodec !== "none");
  result.audio_formats = audioOnly.map((f) => ({
    id: f.format_id,
    ext: f.ext,
    acodec: f.acodec,
    tbr: f.tbr,
    filesize: f.filesize,
    filesize_approx: f.filesize_approx,
  }));

  return result;
}

function pickBestAudio(formats) {
  if (formats.length === 0) return null;
  // Sort by bitrate descending
  return [...formats].sort((a, b) => (b.tbr ?? 0) - (a.tbr ?? 0))[0];
}

async function downloadAudio(url, outputDir) {
  await mkdir(outputDir, { recursive: true });

  // Use fixed output path to avoid % template issues
  const outPath = resolve(outputDir, "audio.m4a");

  return new Promise((resolvePromise, reject) => {
    const proc = spawn(
      "yt-dlp",
      [
        "-f", "bestaudio[ext=m4a]/bestaudio",
        "--output", outPath,
        "--no-playlist",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "--add-headers", "Referer:https://www.bilibili.com/",
        url,
      ],
      { stdio: ["ignore", "pipe", "pipe"] }
    );

    let stderr = "";
    proc.stderr.on("data", (d) => { stderr += d.toString(); });

    proc.on("close", (code) => {
      if (code === 0) {
        resolvePromise(outPath);
      } else {
        reject(new Error(`yt-dlp failed (exit ${code}): ${stderr.slice(0, 500)}`));
      }
    });
    proc.on("error", reject);
  });
}

async function transcribeWithSiliconFlow(filePath, apiKey, model) {
  if (!apiKey) {
    throw new Error("Missing SiliconFlow API key. Set SILICONFLOW_API_KEY or pass --api-key");
  }

  const buffer = await readFile(filePath);
  const ext = filePath.endsWith(".m4a") ? "audio/mp4" : "audio/mpeg";
  const form = new FormData();
  form.append("file", new Blob([buffer], { type: ext }), `audio.${filePath.endsWith(".m4a") ? "m4a" : "mp3"}`);
  form.append("model", model);

  const response = await fetch("https://api.siliconflow.cn/v1/audio/transcriptions", {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}` },
    body: form,
  });

  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {}

  if (!response.ok) {
    throw new Error(`SiliconFlow transcription failed: HTTP ${response.status} ${text.slice(0, 300)}`);
  }

  return { status: response.status, json, rawText: text };
}

function emitResult(summary, transcriptText) {
  console.log(JSON.stringify(summary, null, 2));
  if (typeof transcriptText === "string" && transcriptText.trim()) {
    console.log("\n===TRANSCRIPT===\n");
    console.log(transcriptText);
  }
}

function durationStr(sec) {
  if (!sec) return "未知时长";
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = Math.floor(sec % 60);
  if (h > 0) return `${h}小时${m}分${s}秒`;
  if (m > 0) return `${m}分${s}秒`;
  return `${s}秒`;
}

async function writeSummaryFile(outputDir, title, bvid, duration, source, transcriptText) {
  const md = [
    `# 📹 ${title}`,
    ``,``,
    `**视频信息**`,
    ``,``,
    `- BV号：${bvid}`,
    `- 时长：${durationStr(duration)}`,
    `- 文字来源：${source}`,
    ``,``,
    `---`,
    ``,``,
    `## 📝 完整文字稿`,
    ``,``,
    transcriptText || "（无文字内容）",
    ``,``,
  ].join("\n");
  await writeFile(resolve(outputDir, "summary.md"), md, "utf8");
}

async function runProbe(url, outputDir, apiKey) {
  const result = await probeVideo(url);
  await mkdir(outputDir, { recursive: true });
  await writeFile(resolve(outputDir, "probe_result.json"), JSON.stringify(result, null, 2), "utf8");
  await writeSummaryFile(outputDir, result.title, result.bvid, result.duration, "未运行", null);
  await markReady(outputDir, apiKey);
  emitResult(
    {
      saved: resolve(outputDir, "probe_result.json"),
      summary_md: resolve(outputDir, "summary.md"),
      ready_file: readyFilePath(outputDir),
      title: result.title,
      bvid: result.bvid,
      duration: result.duration,
      subtitleCount: result.subtitles.length,
      audioFormats: result.audio_formats.length,
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
    bvid: result.bvid,
    subtitle_used: false,
    transcript_path: null,
    audio_path: null,
    transcription_json_path: null,
    notes: [],
  };

  // Priority 1: official subtitles
  if (result.subtitle_text) {
    const transcriptPath = resolve(outputDir, "transcript.txt");
    await writeFile(transcriptPath, `${result.subtitle_text}\n`, "utf8");
    await writeSummaryFile(outputDir, result.title, result.bvid, result.duration, "官方字幕", result.subtitle_text);
    summary.subtitle_used = true;
    summary.transcript_path = transcriptPath;
    summary.summary_md = resolve(outputDir, "summary.md");
    summary.notes.push("Used official subtitle text.");
    await markReady(outputDir, apiKey);
    emitResult(summary, result.subtitle_text);
    return;
  }

  // Priority 2: download audio via yt-dlp, then ASR
  const best = pickBestAudio(result.audio_formats);
  if (!best) {
    summary.notes.push("No audio formats found from yt-dlp.");
    emitResult(summary, null);
    return;
  }

  try {
    const audioPath = await downloadAudio(url, outputDir);
    summary.audio_path = audioPath;
    summary.notes.push(`Downloaded audio via yt-dlp (format ${best.id}, ~${best.tbr}kbps).`);

    if (!apiKey) {
      summary.notes.push("Skipping ASR because SILICONFLOW_API_KEY is missing.");
      await markReady(outputDir, false);
      emitResult(summary, null);
      return;
    }

    const transcription = await transcribeWithSiliconFlow(audioPath, apiKey, model);
    const transJsonPath = resolve(outputDir, "transcription_result.json");
    await writeFile(transJsonPath, JSON.stringify(transcription.json ?? { raw: transcription.rawText }, null, 2), "utf8");
    summary.transcription_json_path = transJsonPath;

    const transcriptText = transcription.json?.text;
    if (typeof transcriptText === "string" && transcriptText.trim()) {
      const transcriptPath = resolve(outputDir, "transcript.txt");
      await writeFile(transcriptPath, `${transcriptText}\n`, "utf8");
      summary.transcript_path = transcriptPath;
    } else {
      summary.notes.push("SiliconFlow returned no usable text field.");
    }

    // Write summary.md with transcript embedded
    await writeSummaryFile(outputDir, result.title, result.bvid, result.duration, "语音转写(ASR)", summary.transcript_path ? transcriptText : null);
    summary.summary_md = resolve(outputDir, "summary.md");

    // Clean up: delete audio file to save disk space
    try {
      await rm(audioPath, { force: true });
      summary.notes.push("Audio file deleted after transcription.");
      summary.audio_path = null; // cleared
    } catch {
      // non-critical
    }

    await markReady(outputDir, true);
    emitResult(summary, transcriptText);
  } catch (err) {
    summary.notes.push(`Audio download or ASR failed: ${err.message}`);
    emitResult(summary, null);
  }
}

async function main() {
  requireBin("node");
  requireBin("yt-dlp");

  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];
  const url = args._[1];
  const outputDir = resolve(args["output-dir"] ?? "./output");
  const apiKey = args["api-key"] ?? process.env.SILICONFLOW_API_KEY ?? "";
  const model = args.model ?? "TeleAI/TeleSpeechASR";

  if (!command || !["probe", "run"].includes(command)) {
    fail("Usage:\n  node scripts/bilibili_pipeline.mjs probe <url> [--output-dir ./output]\n  node scripts/bilibili_pipeline.mjs run <url> [--output-dir ./output] [--api-key ***]");
  }

  if (command === "probe") {
    await runProbe(url, outputDir, apiKey);
    return;
  }
  await runPipeline(url, outputDir, apiKey, model);
}

main().catch((error) => fail(error.stack || error.message));
