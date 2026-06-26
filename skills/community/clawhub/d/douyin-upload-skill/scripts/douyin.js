#!/usr/bin/env node

const crypto = require("crypto");
const fs = require("fs");
const fsp = fs.promises;
const path = require("path");
const { spawn, spawnSync } = require("child_process");

const { confirm, parseArgs, parseBoolean, parseInteger, printJson, prompt, toErrorPayload } = require("./lib/cli-utils");
const { LIMITS } = require("./lib/constants");
const { assertAuthEnv, loadConfig, readConfigSync, setConfigKey } = require("./lib/config");
const { ensureDir, fileExists, readJson, writeJsonAtomic } = require("./lib/fs-utils");
const { normalizeLocalPath } = require("./lib/path-utils");
const { isAccessTokenExpired, loadTokenData, normalizeTokenPayload, saveTokenData } = require("./lib/token-store");
const {
  DouyinApiError,
  buildAuthUrl,
  createVideo,
  exchangeCodeForToken,
  isPermissionLikeError,
  refreshAccessToken,
  uploadVideoSmall,
} = require("./lib/douyin-api");
const { computeSha256, getTranscriptCachePath, getVideoMetadata, transcribeVideo, validateDurationOrThrow } = require("./lib/media");

function printHelp() {
  const helpText = [
    "douyin-upload-skill CLI",
    "",
    "Usage:",
    "  node scripts/douyin.js doctor",
    "  node scripts/douyin.js auth [--code <code>] [--callback-url <url>] [--scope <scope>] [--open true|false]",
    "  node scripts/douyin.js prepare --video <path>",
    "  node scripts/douyin.js publish --video <path> --text <caption> [--private-status 0|1|2] [--auto-confirm true|false]",
    "  node scripts/douyin.js config list",
    "  node scripts/douyin.js config get <key>",
    "  node scripts/douyin.js config set <key> <value>",
    "",
    "Environment:",
    "  DOUYIN_CLIENT_KEY, DOUYIN_CLIENT_SECRET, DOUYIN_REDIRECT_URI",
    "  DOUYIN_TOKEN_ENC_KEY (optional)",
    "  DOUYIN_ASR_MODE, DOUYIN_ASR_API_URL, DOUYIN_ASR_API_MODEL, DOUYIN_ASR_API_KEY (optional)",
  ];
  process.stdout.write(`${helpText.join("\n")}\n`);
}

function ensureFileReadable(filePath, label = "file") {
  if (!fs.existsSync(filePath)) {
    const error = new Error(`${label} not found: ${filePath}`);
    error.code = "FILE_NOT_FOUND";
    throw error;
  }

  try {
    fs.accessSync(filePath, fs.constants.R_OK);
  } catch {
    const error = new Error(`${label} is not readable: ${filePath}`);
    error.code = "FILE_NOT_READABLE";
    throw error;
  }
}

function extractCode(rawInput) {
  const input = String(rawInput || "").trim();
  if (!input) {
    return "";
  }

  if (/^https?:\/\//i.test(input)) {
    const url = new URL(input);
    return url.searchParams.get("code") || "";
  }

  if (input.includes("code=")) {
    const url = new URL(input.startsWith("http") ? input : `https://dummy.local/?${input.replace(/^\?/, "")}`);
    return url.searchParams.get("code") || "";
  }

  return input;
}

function openUrl(url) {
  const proc = spawn("xdg-open", [url], {
    detached: true,
    stdio: "ignore",
  });
  proc.unref();
}

function commandExists(commandName) {
  if (commandName.includes("/")) {
    return fs.existsSync(commandName);
  }

  const result = spawnSync("which", [commandName], { stdio: "ignore" });
  return result.status === 0;
}

function normalizeCaption(inputText) {
  const text = String(inputText || "").trim();
  if (!text) {
    const error = new Error("Caption text is required. Use --text.");
    error.code = "CAPTION_REQUIRED";
    throw error;
  }

  if (text.length <= LIMITS.maxCaptionLength) {
    return { text, truncated: false };
  }

  return {
    text: text.slice(0, LIMITS.maxCaptionLength),
    truncated: true,
  };
}

async function maybeRefreshToken(tokenData) {
  if (!isAccessTokenExpired(tokenData)) {
    return tokenData;
  }

  if (!tokenData.refreshToken) {
    const error = new Error("Access token expired and refresh_token is missing. Re-run auth.");
    error.code = "TOKEN_EXPIRED";
    throw error;
  }

  const { clientKey, clientSecret } = assertAuthEnv();
  const refreshed = await refreshAccessToken({
    clientKey,
    clientSecret,
    refreshToken: tokenData.refreshToken,
  });

  const normalized = normalizeTokenPayload(refreshed, tokenData);
  await saveTokenData(normalized);
  return normalized;
}

async function loadCachedTranscript(config, videoSha256) {
  const cachePath = getTranscriptCachePath(videoSha256, config);
  const legacyPath = path.join(config.transcriptCacheDir, `${videoSha256}.json`);
  const cached = (await readJson(cachePath, null)) || (await readJson(legacyPath, null));
  if (!cached) {
    return {
      text: "",
      segments: [],
      source: "none",
    };
  }

  return {
    text: String(cached.text || ""),
    segments: Array.isArray(cached.segments) ? cached.segments : [],
    source: "cache",
  };
}

async function createFallbackOutbox({
  config,
  videoPath,
  caption,
  privateStatus,
  transcript,
  reason,
}) {
  await ensureDir(config.outboxDir);

  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const id = crypto.randomBytes(3).toString("hex");
  const outboxPath = path.join(config.outboxDir, `${stamp}-${id}`);
  await ensureDir(outboxPath);

  await fsp.writeFile(path.join(outboxPath, "caption.txt"), `${caption}\n`, { mode: 0o600 });
  await fsp.writeFile(path.join(outboxPath, "transcript.txt"), `${transcript.text || ""}\n`, { mode: 0o600 });
  await fsp.writeFile(path.join(outboxPath, "source-path.txt"), `${videoPath}\n`, { mode: 0o600 });

  await writeJsonAtomic(path.join(outboxPath, "publish-meta.json"), {
    privateStatus,
    createdAt: new Date().toISOString(),
    reason,
  }, 0o600);

  return outboxPath;
}

async function cmdDoctor() {
  const config = await loadConfig();
  const asrMode = String(config.asrMode || "api").trim().toLowerCase();
  const asrModeOk = ["api", "whisper-gpu", "whisper-cpu"].includes(asrMode);

  const checks = {
    ffmpeg: {
      command: config.ffmpegBin,
      ok: commandExists(config.ffmpegBin),
    },
    ffprobe: {
      command: config.ffprobeBin,
      ok: commandExists(config.ffprobeBin),
    },
    xdgOpen: {
      command: "xdg-open",
      ok: commandExists("xdg-open"),
    },
    asrMode: {
      value: asrMode,
      ok: asrModeOk,
    },
  };

  if (asrMode === "whisper-gpu" || asrMode === "whisper-cpu") {
    checks.whisperCli = {
      command: config.whisperBin,
      ok: commandExists(config.whisperBin),
    };
    checks.whisperModel = {
      path: config.whisperModelPath,
      ok: await fileExists(config.whisperModelPath),
    };
  } else if (asrMode === "api") {
    checks.asrApiUrl = {
      value: config.asrApiUrl,
      ok: Boolean(String(config.asrApiUrl || "").trim()),
    };
    checks.asrApiKey = {
      env: "DOUYIN_ASR_API_KEY",
      ok: Boolean(String(process.env.DOUYIN_ASR_API_KEY || "").trim()),
    };
  }

  const env = {
    DOUYIN_CLIENT_KEY: Boolean(process.env.DOUYIN_CLIENT_KEY),
    DOUYIN_CLIENT_SECRET: Boolean(process.env.DOUYIN_CLIENT_SECRET),
    DOUYIN_REDIRECT_URI: Boolean(process.env.DOUYIN_REDIRECT_URI),
    DOUYIN_ASR_API_KEY: Boolean(process.env.DOUYIN_ASR_API_KEY),
  };

  const installHints = [
    "sudo apt-get update && sudo apt-get install -y ffmpeg cmake build-essential curl jq",
    "git clone https://github.com/ggerganov/whisper.cpp.git && cd whisper.cpp && cmake -B build && cmake --build build -j",
    "ln -sf $(pwd)/build/bin/whisper-cli ~/.local/bin/whisper-cli",
    "mkdir -p ~/.cache/whisper.cpp && curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin -o ~/.cache/whisper.cpp/ggml-small.bin",
    "export DOUYIN_ASR_MODE=api && export DOUYIN_ASR_API_KEY=*** && export DOUYIN_ASR_API_URL=https://api.openai.com/v1/audio/transcriptions",
    "or set local whisper mode: node scripts/douyin.js config set asrMode whisper-gpu",
  ];

  const missing = Object.entries(checks)
    .filter(([, value]) => !value.ok)
    .map(([key]) => key);

  printJson({
    ok: missing.length === 0,
    command: "doctor",
    checks,
    env,
    config,
    installHints,
  });
}

async function cmdAuth(options) {
  const config = await loadConfig();
  const { clientKey, clientSecret, redirectUri } = assertAuthEnv();

  const scope = String(options.scope || config.scope).trim();
  const state = crypto.randomBytes(8).toString("hex");
  const authUrl = buildAuthUrl({
    clientKey,
    redirectUri,
    scope,
    state,
  });

  const shouldOpen = parseBoolean(options.open, true);
  if (shouldOpen) {
    try {
      openUrl(authUrl);
    } catch (_) {
      // Ignore browser open failures.
    }
  }

  let rawCode = options.code || "";
  if (!rawCode && options["callback-url"]) {
    rawCode = extractCode(options["callback-url"]);
  }

  if (!rawCode) {
    if (!process.stdin.isTTY) {
      const error = new Error("No --code provided and terminal is non-interactive.");
      error.code = "AUTH_CODE_REQUIRED";
      throw error;
    }

    process.stderr.write(`Open this URL and authorize:\n${authUrl}\n`);
    const input = await prompt("Paste `code` or callback URL: ");
    rawCode = extractCode(input);
  }

  const code = extractCode(rawCode);
  if (!code) {
    const error = new Error("Cannot extract OAuth code.");
    error.code = "AUTH_CODE_INVALID";
    throw error;
  }

  const tokenPayload = await exchangeCodeForToken({
    clientKey,
    clientSecret,
    redirectUri,
    code,
  });

  const normalized = normalizeTokenPayload(tokenPayload);
  await saveTokenData(normalized);

  printJson({
    ok: true,
    command: "auth",
    authUrl,
    scope,
    token: {
      openId: normalized.openId,
      scope: normalized.scope,
      expiresAt: new Date(normalized.expiresAt).toISOString(),
      refreshExpiresAt: new Date(normalized.refreshExpiresAt).toISOString(),
    },
  });
}

async function cmdPrepare(options) {
  const videoInput = options.video;
  if (!videoInput) {
    const error = new Error("Missing required argument: --video <path>");
    error.code = "VIDEO_REQUIRED";
    throw error;
  }

  const config = await loadConfig();
  const normalizedPath = normalizeLocalPath(videoInput);
  ensureFileReadable(normalizedPath, "Video file");

  const sha256 = await computeSha256(normalizedPath);
  const metadata = await getVideoMetadata(normalizedPath, config);
  validateDurationOrThrow(metadata.durationSec);

  let transcript = {
    source: "none",
    text: "",
    segments: [],
  };
  let asrError = null;

  try {
    transcript = await transcribeVideo(normalizedPath, sha256, config);
  } catch (error) {
    asrError = {
      message: error.message,
      code: error.code || null,
    };
  }

  printJson({
    ok: true,
    command: "prepare",
    video: {
      inputPath: videoInput,
      normalizedPath,
      sha256,
      sizeBytes: metadata.sizeBytes,
      durationSec: metadata.durationSec,
      width: metadata.width,
      height: metadata.height,
    },
    transcript,
    asrError,
    limits: {
      maxDurationSec: LIMITS.maxDurationSec,
      maxTextLen: LIMITS.maxCaptionLength,
    },
  });
}

async function cmdPublish(options) {
  const videoInput = options.video;
  if (!videoInput) {
    const error = new Error("Missing required argument: --video <path>");
    error.code = "VIDEO_REQUIRED";
    throw error;
  }

  const config = await loadConfig();
  const normalizedPath = normalizeLocalPath(videoInput);
  ensureFileReadable(normalizedPath, "Video file");

  const requestedPrivateStatus = parseInteger(options["private-status"], config.defaultPrivateStatus);
  if (![0, 1, 2].includes(requestedPrivateStatus)) {
    const error = new Error("private-status must be one of: 0, 1, 2");
    error.code = "PRIVATE_STATUS_INVALID";
    throw error;
  }

  let captionInput = options.text || "";
  if (!captionInput && process.stdin.isTTY) {
    captionInput = await prompt("Paste final caption text: ");
  }

  const caption = normalizeCaption(captionInput);
  const autoConfirm = parseBoolean(options["auto-confirm"], config.autoConfirm);

  if (!autoConfirm) {
    if (!process.stdin.isTTY) {
      const error = new Error("Interactive confirmation is required. Pass --auto-confirm true in non-interactive mode.");
      error.code = "CONFIRMATION_REQUIRED";
      throw error;
    }
    const accepted = await confirm("Publish to Douyin now?", false);
    if (!accepted) {
      printJson({
        ok: false,
        command: "publish",
        cancelled: true,
      });
      return;
    }
  }

  const metadata = await getVideoMetadata(normalizedPath, config);
  validateDurationOrThrow(metadata.durationSec);

  const videoSha256 = await computeSha256(normalizedPath);
  const transcript = await loadCachedTranscript(config, videoSha256);

  let tokenData = await loadTokenData();
  if (!tokenData) {
    const error = new Error("Token not found. Run auth first.");
    error.code = "TOKEN_NOT_FOUND";
    throw error;
  }

  tokenData = await maybeRefreshToken(tokenData);

  try {
    const uploaded = await uploadVideoSmall({
      accessToken: tokenData.accessToken,
      videoPath: normalizedPath,
    });

    const published = await createVideo({
      accessToken: tokenData.accessToken,
      videoId: uploaded.videoId,
      text: caption.text,
      privateStatus: requestedPrivateStatus,
    });

    printJson({
      ok: true,
      command: "publish",
      mode: "official",
      itemId: published.itemId,
      videoId: published.videoId || uploaded.videoId,
      openId: tokenData.openId,
      textTruncated: caption.truncated,
      privateStatus: requestedPrivateStatus,
    });
    return;
  } catch (error) {
    if (!(error instanceof DouyinApiError) || !isPermissionLikeError(error)) {
      throw error;
    }

    const outboxPath = await createFallbackOutbox({
      config,
      videoPath: normalizedPath,
      caption: caption.text,
      privateStatus: requestedPrivateStatus,
      transcript,
      reason: {
        message: error.message,
        code: error.code,
      },
    });

    printJson({
      ok: true,
      command: "publish",
      mode: "fallback",
      outboxPath,
      reason: {
        message: error.message,
        code: error.code,
      },
      textTruncated: caption.truncated,
      privateStatus: requestedPrivateStatus,
    });
  }
}

async function cmdConfig(positionals) {
  const action = positionals[0];
  if (!action || action === "list") {
    const config = await loadConfig();
    printJson({ ok: true, command: "config", config });
    return;
  }

  if (action === "get") {
    const key = positionals[1];
    if (!key) {
      throw new Error("Usage: config get <key>");
    }

    const config = readConfigSync();
    printJson({
      ok: true,
      command: "config",
      key,
      value: config[key],
    });
    return;
  }

  if (action === "set") {
    const key = positionals[1];
    const value = positionals[2];
    if (!key || value === undefined) {
      throw new Error("Usage: config set <key> <value>");
    }

    const updated = await setConfigKey(key, value);
    printJson({
      ok: true,
      command: "config",
      key,
      value: updated[key],
      config: updated,
    });
    return;
  }

  throw new Error(`Unknown config action: ${action}`);
}

async function main() {
  const { positionals, options } = parseArgs(process.argv.slice(2));
  const [command, ...rest] = positionals;

  if (!command || ["-h", "--help", "help"].includes(command)) {
    printHelp();
    return;
  }

  switch (command) {
    case "doctor":
      await cmdDoctor();
      break;
    case "auth":
      await cmdAuth(options);
      break;
    case "prepare":
      await cmdPrepare(options);
      break;
    case "publish":
      await cmdPublish(options);
      break;
    case "config":
      await cmdConfig(rest);
      break;
    default:
      throw new Error(`Unknown command: ${command}`);
  }
}

main().catch((error) => {
  printJson(toErrorPayload(error));
  process.exitCode = 1;
});
