#!/usr/bin/env node
/**
 * Agnes Image 2.1 Flash 生图脚本
 * 用法：
 *   node generate.mjs --prompt "a cat" --size 1024x1024 --format url
 *   node generate.mjs --prompt "a cat" --size 1024x1024 --format b64_json --output cat.png
 *   node generate.mjs --prompt "cyberpunk style" --image ./input.png --size 1024x1024 --format url
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { extname, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const API_URL = 'https://apihub.agnes-ai.cn/v1/images/generations';
const MODEL = 'agnes-image-2.1-flash';
const DEFAULT_TIMEOUT_MS = 300_000;

function loadEnv() {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const envPaths = [
    join(__dirname, '.env'),
    join(process.cwd(), '.env'),
  ];
  for (const path of envPaths) {
    if (existsSync(path)) {
      const content = readFileSync(path, 'utf-8');
      for (const line of content.split(/\r?\n/)) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) continue;
        const idx = trimmed.indexOf('=');
        if (idx === -1) continue;
        const key = trimmed.slice(0, idx).trim();
        let value = trimmed.slice(idx + 1).trim();
        if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
          value = value.slice(1, -1);
        }
        if (!process.env[key]) {
          process.env[key] = value;
        }
      }
      break;
    }
  }
}

loadEnv();

function printHelp() {
  console.log(`
Agnes Image 2.1 Flash 生图脚本

用法:
  node generate.mjs [选项]

选项:
  --prompt <text>     图像生成/编辑的文本指令（必填）
  --size <WxH>        输出尺寸，默认 1024x1024
  --image <path/url>  图生图输入：本地文件路径或公开 HTTPS URL
  --format <url|b64_json>  输出格式，默认 url
  --output <path>     Base64 输出时保存的文件路径，默认 output.png
  --timeout <ms>      请求超时，默认 300000ms (5分钟)
  --help              显示帮助

示例:
  node generate.mjs --prompt "一只在草原上奔跑的狐狸，写实风格" --size 1024x1024 --format url
  node generate.mjs --prompt "赛博朋克夜景" --image ./day.png --size 1024x1024 --format b64_json --output night.png
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--help') {
      printHelp();
      process.exit(0);
    }
    if (key.startsWith('--')) {
      const name = key.slice(2);
      const value = argv[i + 1];
      if (value === undefined || value.startsWith('--')) {
        throw new Error(`选项 ${key} 需要一个值`);
      }
      args[name] = value;
      i++;
    }
  }
  return args;
}

function isUrl(str) {
  try {
    const url = new URL(str);
    return url.protocol === 'https:' || url.protocol === 'http:';
  } catch {
    return false;
  }
}

function fileToDataUri(path) {
  if (!existsSync(path)) {
    throw new Error(`文件不存在: ${path}`);
  }
  const ext = extname(path).toLowerCase();
  const mimeMap = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
  };
  const mime = mimeMap[ext] || 'image/png';
  const base64 = readFileSync(path).toString('base64');
  return `data:${mime};base64,${base64}`;
}

async function generate({ prompt, size, image, format, timeoutMs }) {
  const apiKey = process.env.AGNES_API_KEY;
  if (!apiKey) {
    throw new Error('未找到 AGNES_API_KEY。请在 skill 目录下的 .env 文件中设置：AGNES_API_KEY=sk-...');
  }

  const body = {
    model: MODEL,
    prompt,
    size: size || '1024x1024',
  };

  const extraBody = {};

  if (format === 'b64_json') {
    extraBody.response_format = 'b64_json';
  } else if (format === 'url') {
    extraBody.response_format = 'url';
  }

  if (image) {
    const imageValue = isUrl(image) ? image : fileToDataUri(image);
    extraBody.image = [imageValue];
  }

  if (format === 'b64_json' && !image) {
    // 文生图 Base64 使用顶层 return_base64
    body.return_base64 = true;
  }

  if (Object.keys(extraBody).length > 0) {
    body.extra_body = extraBody;
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    const data = await res.json().catch(() => null);

    if (!res.ok) {
      const msg = data?.error?.message || JSON.stringify(data) || res.statusText;
      throw new Error(`API 请求失败 (${res.status}): ${msg}`);
    }

    if (!data?.data?.[0]) {
      throw new Error('API 返回异常：未包含 data[0]');
    }

    return data.data[0];
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error(`请求超时（${timeoutMs}ms），建议稍后重试或减小图片尺寸`);
    }
    throw err;
  }
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (err) {
    console.error(`参数错误: ${err.message}`);
    printHelp();
    process.exit(1);
  }

  if (!args.prompt) {
    console.error('错误: --prompt 必填');
    printHelp();
    process.exit(1);
  }

  const format = args.format || 'url';
  if (!['url', 'b64_json'].includes(format)) {
    console.error('错误: --format 必须是 url 或 b64_json');
    process.exit(1);
  }

  const timeoutMs = Number(args.timeout) || DEFAULT_TIMEOUT_MS;

  try {
    const result = await generate({
      prompt: args.prompt,
      size: args.size,
      image: args.image,
      format,
      timeoutMs,
    });

    if (format === 'url' || result.url) {
      console.log(result.url);
      return;
    }

    if (result.b64_json) {
      const outputPath = args.output || 'output.png';
      const buffer = Buffer.from(result.b64_json, 'base64');
      writeFileSync(outputPath, buffer);
      console.log(`已保存: ${outputPath}`);
      return;
    }

    console.error('API 返回中未找到 url 或 b64_json');
    process.exit(1);
  } catch (err) {
    console.error(`生成失败: ${err.message}`);
    process.exit(1);
  }
}

main();
