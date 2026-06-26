const os = require("os");
const path = require("path");

const APP_NAME = "douyin-upload-skill";

const CONFIG_DIR = path.join(os.homedir(), ".config", APP_NAME);
const CACHE_DIR = path.join(os.homedir(), ".cache", APP_NAME);
const DATA_DIR = path.join(os.homedir(), ".local", "share", APP_NAME);

const CONFIG_PATH = path.join(CONFIG_DIR, "config.json");
const TOKENS_PATH = path.join(CONFIG_DIR, "tokens.enc.json");
const TOKEN_KEY_PATH = path.join(CONFIG_DIR, "token.key");

const DEFAULT_TRANSCRIPT_CACHE_DIR = path.join(CACHE_DIR, "transcripts");
const DEFAULT_OUTBOX_DIR = path.join(DATA_DIR, "outbox");
const DEFAULT_WHISPER_MODEL_PATH = path.join(os.homedir(), ".cache", "whisper.cpp", "ggml-small.bin");
const DEFAULT_ASR_API_URL = "https://api.openai.com/v1/audio/transcriptions";
const DEFAULT_ASR_API_MODEL = "whisper-1";

const DEFAULT_CONFIG = {
  defaultPrivateStatus: 0,
  autoConfirm: false,
  scope: "user_info,video.create.bind",
  asrMode: "api",
  asrApiUrl: DEFAULT_ASR_API_URL,
  asrApiModel: DEFAULT_ASR_API_MODEL,
  asrApiTimeoutMs: 120000,
  ffmpegBin: "ffmpeg",
  ffprobeBin: "ffprobe",
  whisperBin: "whisper-cli",
  whisperModelPath: DEFAULT_WHISPER_MODEL_PATH,
  whisperLang: "zh",
  transcriptCacheDir: DEFAULT_TRANSCRIPT_CACHE_DIR,
  outboxDir: DEFAULT_OUTBOX_DIR,
};

const LIMITS = {
  maxDurationSec: 15 * 60,
  maxCaptionLength: 1000,
};

const DOUYIN_BASE_URL = "https://open.douyin.com";

module.exports = {
  APP_NAME,
  CACHE_DIR,
  CONFIG_DIR,
  CONFIG_PATH,
  DATA_DIR,
  DEFAULT_ASR_API_MODEL,
  DEFAULT_ASR_API_URL,
  DEFAULT_CONFIG,
  DEFAULT_OUTBOX_DIR,
  DEFAULT_TRANSCRIPT_CACHE_DIR,
  DEFAULT_WHISPER_MODEL_PATH,
  DOUYIN_BASE_URL,
  LIMITS,
  TOKEN_KEY_PATH,
  TOKENS_PATH,
};
