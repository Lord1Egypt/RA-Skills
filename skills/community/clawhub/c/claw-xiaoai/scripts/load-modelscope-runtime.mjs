#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { resolve } from 'node:path';

const DEFAULT_BASE_URL = 'https://api-inference.modelscope.cn/';
const DEFAULT_MODEL = 'Tongyi-MAI/Z-Image-Turbo';
const DEFAULT_POLL_INTERVAL_SECONDS = 5;
const DEFAULT_MAX_POLLS = 60;
const DEFAULT_TIMEOUT_SECONDS = 60;

function ensureTrailingSlash(value) {
  return value.endsWith('/') ? value : `${value}/`;
}

function readApiKeyFromOpenClawConfig() {
  const openClawConfigPath = resolve(process.env.HOME || homedir(), '.openclaw', 'openclaw.json');

  try {
    if (!existsSync(openClawConfigPath)) return undefined;
    const data = JSON.parse(readFileSync(openClawConfigPath, 'utf8'));
    const entry = data?.skills?.entries?.['claw-xiaoai'];
    if (entry && typeof entry.apiKey === 'string' && entry.apiKey.trim()) return entry.apiKey.trim();
    if (entry?.env?.MODELSCOPE_API_KEY) return String(entry.env.MODELSCOPE_API_KEY).trim();
    if (entry?.env?.MODELSCOPE_TOKEN) return String(entry.env.MODELSCOPE_TOKEN).trim();
  } catch {}

  return undefined;
}

export function loadModelScopeRuntime() {
  const apiKey = process.env.MODELSCOPE_API_KEY || process.env.MODELSCOPE_TOKEN || readApiKeyFromOpenClawConfig();

  return {
    apiKey,
    baseUrl: ensureTrailingSlash(DEFAULT_BASE_URL),
    model: DEFAULT_MODEL,
    pollIntervalMs: DEFAULT_POLL_INTERVAL_SECONDS * 1000,
    maxPolls: DEFAULT_MAX_POLLS,
    timeoutMs: DEFAULT_TIMEOUT_SECONDS * 1000
  };
}
