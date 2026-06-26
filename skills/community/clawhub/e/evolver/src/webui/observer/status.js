'use strict';

const fs = require('fs');
const { getObserverPaths } = require('./paths');
const { readJsonSafe } = require('./jsonl');
const { getSafetyState } = require('./safety');
const { redactValue } = require('./redact');

function getStatus() {
  const paths = getObserverPaths();
  const cycle = readJsonSafe(paths.cycleProgressPath, null);
  const solidify = readJsonSafe(paths.solidifyStatePath, null);
  const evolution = readJsonSafe(paths.evolutionStatePath, null);
  const proxy = getProxySettings();
  // Everything observer-derived may carry prompt / task context with
  // embedded credentials. Every other observer endpoint (runs.js,
  // assets.js, interactions.js, ...) already pipes its payload through
  // redactValue; /webui/status is the one that skipped it, so it became
  // the easy exfiltration path. Funnel the three readJsonSafe outputs
  // through the same redaction filter before they leave the process.
  return {
    mode: inferMode(cycle, solidify, proxy),
    heartbeat: redactValue(cycle),
    lastRun: redactValue(solidify && solidify.last_run ? solidify.last_run : null),
    evolutionState: redactValue(evolution),
    proxy,
    filesPresent: filesPresent(paths),
    safety: getSafetyState(),
  };
}

function inferMode(cycle, solidify, proxy) {
  if (cycle && isFresh(cycle.updated_at, 120_000)) return 'running';
  if (solidify && solidify.pending) return 'review_pending';
  if (proxy && proxy.running) return 'proxy_only';
  return 'idle';
}

function isFresh(timestamp, maxAgeMs) {
  const t = Number(timestamp);
  return Number.isFinite(t) && Date.now() - t < maxAgeMs;
}

function getProxySettings() {
  try {
    const { readSettings, isStaleProxy } = require('../../proxy/server/settings');
    const settings = readSettings();
    const proxy = settings.proxy || null;
    if (!proxy) return { running: false, url: null };
    return {
      running: !isStaleProxy(),
      url: proxy.url || null,
      pid: proxy.pid || null,
      started_at: proxy.started_at || null,
    };
  } catch {
    return { running: false, url: null };
  }
}

function filesPresent(paths) {
  return {
    cycleProgress: fs.existsSync(paths.cycleProgressPath),
    solidifyState: fs.existsSync(paths.solidifyStatePath),
    events: fs.existsSync(paths.eventsPath),
    assetCallLog: fs.existsSync(paths.assetCallLogPath),
    pipelineEvents: fs.existsSync(paths.pipelineEventsPath),
  };
}

module.exports = { getStatus, getProxySettings };
