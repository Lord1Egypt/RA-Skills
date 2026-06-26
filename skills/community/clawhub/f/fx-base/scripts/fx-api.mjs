#!/usr/bin/env node
// fx-api.mjs — feima-lab 公共请求库
// 用法：在领域 skill 脚本中 import { fxCheckAuth, fxPost, fxCheckResponse, FX_BASE_URL } from './fx-api.mjs'

// ── 常量 ──
export const FX_BASE_URL = 'https://api-ai-brain.fenxianglife.com/fenxiang-ai-brain';

// ── fxCheckAuth ──
// 校验 FX_AI_API_KEY，未设置则输出标准错误 JSON 并 exit 1
export function fxCheckAuth() {
  const key = process.env.FX_AI_API_KEY;
  if (!key) {
    process.stderr.write(
      '{"status":"error","error_type":"missing_api_key","suggestion":"请设置环境变量 FX_AI_API_KEY，从 https://platform.feima.ai/ 登录获取"}\n'
    );
    process.exit(1);
  }
  return key;
}

// ── fxPost(endpoint, body, errMsg) ──
// 发送 POST 请求到 feima-lab 后端，返回响应 JSON 字符串
// 参数：
//   endpoint — API 路径（如 skill/api/convert），不含 BASE_URL 前缀
//   body     — 请求体对象（会被 JSON.stringify）
//   errMsg   — 可选，失败时的用户提示（默认"服务暂时不可用，请稍后重试"）
// 失败时输出错误 JSON 到 stderr 并 exit 1
export async function fxPost(endpoint, body, errMsg = '服务暂时不可用，请稍后重试') {
  const key = process.env.FX_AI_API_KEY;
  const url = `${FX_BASE_URL}/${endpoint}`;

  let resp;
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 30000);
    try {
      resp = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Fx-Ai-Api-Key': `Bearer ${key}`,
        },
        body: typeof body === 'string' ? body : JSON.stringify(body),
        signal: controller.signal,
      });
    } finally {
      clearTimeout(timer);
    }
  } catch (e) {
    process.stderr.write(
      JSON.stringify({ status: 'error', error_type: 'api_unavailable', suggestion: errMsg }) + '\n'
    );
    process.exit(1);
  }

  if (!resp.ok) {
    process.stderr.write(
      JSON.stringify({ status: 'error', error_type: 'api_unavailable', suggestion: errMsg }) + '\n'
    );
    process.exit(1);
  }

  return resp.text();
}

// ── fxCheckResponse(respJson) ──
// 校验响应：code==200 返回 data 对象，否则输出错误到 stderr 并 exit 1
// 参数：
//   respJson — 完整的响应 JSON 字符串
export function fxCheckResponse(respJson) {
  let resp;
  try {
    resp = JSON.parse(respJson);
  } catch (e) {
    process.stderr.write(
      JSON.stringify({ status: 'error', error_type: 'api_unavailable', suggestion: '响应解析失败' }) + '\n'
    );
    process.exit(1);
  }

  const data = resp.data !== undefined ? resp.data : resp;

  if (resp.code === 200 && data) {
    return data;
  } else {
    const msg = resp.message || '请求失败';
    const err = (data && typeof data === 'object' && data.errorMessage) ? data.errorMessage : msg;
    process.stderr.write(
      JSON.stringify({ status: 'error', message: err }, null, 2) + '\n'
    );
    process.exit(1);
  }
}
