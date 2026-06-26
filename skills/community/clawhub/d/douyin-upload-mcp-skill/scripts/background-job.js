import { spawn, spawnSync } from 'node:child_process';

const ENV_KEYS_TO_KEEP = [
  'HOME',
  'PATH',
  'USER',
  'LOGNAME',
  'SHELL',
  'DISPLAY',
  'WAYLAND_DISPLAY',
  'XDG_RUNTIME_DIR',
  'DBUS_SESSION_BUS_ADDRESS',
  'OPENCLAW_CONFIG_PATH',
  'OPENCLAW_MODELS_PATH',
  'FEISHU_ACCOUNT_ID',
  'FEISHU_DRY_RUN',
  'FEISHU_DRY_RUN_LOG',
  'DOUYIN_MONITOR_STATE_DIR',
  'DOUYIN_FEISHU_RECEIVE_ID',
  'DOUYIN_FEISHU_RECEIVE_ID_TYPE',
  'DOUYIN_FEISHU_WATCH_STATE',
  'DOUYIN_FEISHU_UPLOAD_DIR',
  'DOUYIN_FEISHU_UPSTREAM_DIR',
  'DOUYIN_FEISHU_UPSTREAM_CACHE_DIR',
  'DOUYIN_NEXT_VIDEO_PLAN_JOB_DIR',
  'DOUYIN_PUBLISH_JOB_DIR',
  'DOUYIN_MARKETING_VIDEO_JOB_DIR',
  'DOUYIN_PERSONA_JOB_DIR',
  'DOUYIN_ONBOARDING_JOB_DIR',
  'DOUYIN_DIGITAL_HUMAN_STATE_PATH',
  'DOUYIN_ALLOW_UNCONFIRMED_DEFAULT_DIGITAL_HUMAN',
  'DOUYIN_DEFAULT_DIGITAL_HUMAN_ID',
  'DOUYIN_NEXT_VIDEO_PLAN_SKIP_SYNC',
  'DOUYIN_NEXT_VIDEO_PLAN_LLM_TIMEOUT_MS',
  'DOUYIN_NEXT_VIDEO_PLAN_MODEL',
  'DOUYIN_NEXT_VIDEO_PLAN_PROVIDER',
  'DOUYIN_NEXT_VIDEO_PLAN_BASE_URL',
  'DOUYIN_NEXT_VIDEO_PLAN_API',
  'DOUYIN_ROUTE_LIGHT_TEST',
  'DOUYIN_MARKETING_STATE_PATH',
  'DOUYIN_PERSONA_STATE_PATH',
  'DOUYIN_PERSONA_API',
  'DOUYIN_PERSONA_API_KEY',
  'DOUYIN_PERSONA_BASE_URL',
  'DOUYIN_PERSONA_MODEL',
  'DOUYIN_PERSONA_PROVIDER',
  'DOUYIN_PERSONA_LLM',
  'DOUYIN_PERSONA_SPLIT_LLM',
  'DOUYIN_PERSONA_LLM_TIMEOUT_MS',
  'DOUYIN_PERSONA_MAX_TOKENS',
  'DOUYIN_PERSONA_ALLOW_RULES_FALLBACK',
  'DOUYIN_PERSONA_REVIEW_MAX_CHARS',
  'DOUYIN_DATA_REPORT_LLM_TIMEOUT_MS',
  'DOUYIN_DATA_REPORT_MODEL',
  'DOUYIN_DATA_REPORT_PROVIDER',
  'DIGITAL_HUMAN_MODEL_ID',
  'DIGITAL_HUMAN_SKIP_COZE',
  'DIGITAL_HUMAN_USE_COZE',
  'DIGITAL_HUMAN_TRAINING_API_KEY',
  'DIGITAL_HUMAN_TRAINING_API_BASE_URL',
  'DIGITAL_HUMAN_TRAINING_AUTH_HEADER',
  'VIRTUALMAN_MODEL_ID',
  'VIDEO_PROVIDER_VH_BIZ_ID',
  'VIDEO_PROVIDER_MODEL_ID',
  'XIAOICE_VIDEO_ENV_PATH',
  'BROWSER_DEBUG_PORT',
  'BROWSER_PATH',
  'BROWSER_HEADLESS',
  'BROWSER_USER_DATA_DIR',
  'BROWSER_PROTOCOL_TIMEOUT',
  'DAEMON_PORT',
  'OUTPUT_DIR',
];

function sanitizeUnitName(name) {
  const clean = String(name || 'job')
    .replace(/[^A-Za-z0-9_.:-]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 180);
  return clean || `job-${Date.now()}`;
}

function buildEnvArgs(extraEnv = {}) {
  const merged = { ...process.env, ...extraEnv };
  const args = [];
  for (const key of ENV_KEYS_TO_KEEP) {
    const value = merged[key];
    if (value !== undefined && value !== null && String(value) !== '') {
      args.push(`--setenv=${key}=${String(value)}`);
    }
  }
  return args;
}

export function startBackgroundNodeJob({
  scriptPath,
  args = [],
  cwd,
  unitName,
  description,
  env = {},
  runtimeMaxSec = 1800,
}) {
  const unit = sanitizeUnitName(unitName);
  const command = [process.execPath, scriptPath, ...args];
  const systemdArgs = [
    '--user',
    '--collect',
    '--no-block',
    `--unit=${unit}`,
    `--description=${description || unit}`,
    `--working-directory=${cwd}`,
    `--property=RuntimeMaxSec=${runtimeMaxSec}`,
    ...buildEnvArgs(env),
    ...command,
  ];
  const systemd = spawnSync('systemd-run', systemdArgs, {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  if (systemd.status === 0) {
    return {
      ok: true,
      runner: 'systemd-run',
      unit,
      output: `${systemd.stderr || ''}${systemd.stdout || ''}`.trim(),
    };
  }

  const child = spawn(process.execPath, [scriptPath, ...args], {
    cwd,
    detached: true,
    stdio: 'ignore',
    env: { ...process.env, ...env },
  });
  child.unref();
  return {
    ok: true,
    runner: 'node-detached-fallback',
    pid: child.pid,
    systemdError: `${systemd.stderr || ''}${systemd.stdout || ''}`.trim(),
  };
}
