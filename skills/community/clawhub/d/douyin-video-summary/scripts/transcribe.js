#!/usr/bin/env node
'use strict';

const crypto = require('node:crypto');

const API_BASE = 'https://calapi.ailuk.cn';
const RECHARGE_URL = 'https://payhtml.ailuk.cn';
const SERVICE_FAILURE_MESSAGE = '支撑服务出问题了，不能继续了。';
const POLL_INTERVAL_MS = Number(process.env.DOUYIN_POLL_INTERVAL_MS || 3000);
const TIMEOUT_MS = Number(process.env.DOUYIN_TIMEOUT_MS || 3 * 60 * 60 * 1000);

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

function requiredEnv(name) {
  const value = (process.env[name] || '').trim();
  if (!value) {
    const error = new Error(`缺少环境变量 ${name}`);
    error.code = 'CONFIG_ERROR';
    throw error;
  }
  return value;
}

function errorDetails(body, status) {
  const detail = body && body.detail ? body.detail : body;
  if (detail && typeof detail === 'object') {
    return {
      code: detail.code || `HTTP_${status}`,
      message: detail.message || JSON.stringify(detail),
      rechargeUrl: detail.recharge_url || RECHARGE_URL
    };
  }
  return { code: `HTTP_${status}`, message: String(detail || `请求失败（${status}）`), rechargeUrl: RECHARGE_URL };
}

async function requestJson(url, options) {
  const response = await fetch(url, options);
  const text = await response.text();
  let body = {};
  try { body = text ? JSON.parse(text) : {}; } catch (_) { body = { message: text }; }
  if (!response.ok) {
    const details = errorDetails(body, response.status);
    const error = new Error(details.message);
    Object.assign(error, details, { status: response.status });
    throw error;
  }
  return body;
}

function formatSeconds(durationMs) {
  return `${Math.round((durationMs || 0) / 100) / 10} 秒`;
}

function createIdempotencyKey(sourceUrl, audioUrl) {
  return crypto.createHash('sha256').update(`${sourceUrl || ''}\0${audioUrl}`).digest('hex');
}

function failureOutput(error) {
  if (error.code === 'INSUFFICIENT_BALANCE' || error.status === 402) {
    return {
      exitCode: 2,
      lines: [`余额不足：${error.message}`, `充值地址：${RECHARGE_URL}`]
    };
  }
  if (error.code === 'CONFIG_ERROR') {
    return { exitCode: 1, lines: [`转写失败：${error.message}`] };
  }
  return { exitCode: 1, lines: [SERVICE_FAILURE_MESSAGE] };
}

async function main() {
  const audioUrl = requiredEnv('DOUYIN_AUDIO_URL');
  const apiKey = requiredEnv('DOUYIN_API_KEY');
  const sourceUrl = process.argv[2] || null;
  const title = (process.env.DOUYIN_TITLE || '未知标题').trim();
  const author = (process.env.DOUYIN_AUTHOR || '未知作者').trim();
  const idempotencyKey = createIdempotencyKey(sourceUrl, audioUrl);
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
    'Idempotency-Key': idempotencyKey
  };

  let job = await requestJson(`${API_BASE}/v1/transcriptions`, {
    method: 'POST', headers,
    body: JSON.stringify({ audio_url: audioUrl, source_url: sourceUrl, title, author })
  });
  const deadline = Date.now() + TIMEOUT_MS;
  while (job.status === 'queued' || job.status === 'processing') {
    if (Date.now() >= deadline) throw new Error(`转写等待超时，任务 ID：${job.id}`);
    await sleep(POLL_INTERVAL_MS);
    job = await requestJson(`${API_BASE}/v1/transcriptions/${encodeURIComponent(job.id)}`, { headers });
  }
  if (job.status !== 'succeeded') throw new Error(job.error_message || '转写失败');

  const result = {jobId:job.id,title:job.title||title,author:job.author||author,durationMs:job.duration_ms,chargedFen:job.charged_fen,transcript:job.transcript,subtitlesSrt:job.subtitles_srt};
  console.log(JSON.stringify(result));
  console.error(`转写完成：${result.title}｜${formatSeconds(result.durationMs)}｜扣费 ¥${((result.chargedFen || 0) / 100).toFixed(2)}`);
}

if (require.main === module) {
  main().catch(error => {
    const output = failureOutput(error);
    for (const line of output.lines) console.error(line);
    process.exitCode = output.exitCode;
  });
}

module.exports = { API_BASE, RECHARGE_URL, SERVICE_FAILURE_MESSAGE, createIdempotencyKey, errorDetails, failureOutput, formatSeconds, main };
