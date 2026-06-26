#!/usr/bin/env node
/**
 * 移动云 EOS 图片处理脚本
 *
 * 依赖：npm install @aws-sdk/s3-request-presigner @smithy/hash-node @smithy/protocol-http
 * 凭证通过环境变量读取：EOS_ACCESS_KEY, EOS_SECRET_KEY, EOS_REGION, EOS_BUCKET, EOS_ENDPOINT
 *
 * 用法：node scripts/eos_image.mjs <action> [options]
 */

import fs from 'fs';
import http from 'http';
import https from 'https';
import path from 'path';
import { S3RequestPresigner } from '@aws-sdk/s3-request-presigner';
import { Hash } from '@smithy/hash-node';
import { HttpRequest } from '@smithy/protocol-http';

const SecretId = process.env.EOS_ACCESS_KEY;
const SecretKey = process.env.EOS_SECRET_KEY;
const Region = process.env.EOS_REGION;
const Endpoint = process.env.EOS_ENDPOINT;
const EOS_Bucket = process.env.EOS_BUCKET;

const s3Credentials = {
  accessKeyId: SecretId,
  secretAccessKey: SecretKey,
};

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        result[key] = next;
        i++;
      } else {
        result[key] = true;
      }
    }
  }
  return result;
}

function output(data) {
  console.log(JSON.stringify(data, null, 2));
}

function normalizeObjectKey(key) {
  return key.replace(/\\/g, '/');
}

function parseExpires(rawExpires) {
  if (rawExpires === undefined) {
    return 3600;
  }

  const expires = parseInt(rawExpires, 10);
  if (Number.isNaN(expires) || expires <= 0) {
    throw new Error('--expires 参数必须是大于 0 的整数');
  }

  return expires;
}

function requireBucket(bucket) {
  if (!bucket) {
    throw new Error('缺少桶名，请设置 EOS_BUCKET 环境变量或使用 --bucket <bucket>');
  }
}

function requireProcessString(opts) {
  if (opts.process === true) {
    throw new Error('缺少 --process 参数值，请使用 --process "<process-string>"');
  }

  const processString = typeof opts.process === 'string' ? opts.process.trim() : '';
  if (!processString) {
    throw new Error('缺少 --process 参数值，请使用 --process "<process-string>"');
  }
  if (processString.startsWith('x-eos-process=')) {
    throw new Error('--process 只需要传递处理串本身，不要包含 x-eos-process=');
  }

  return processString;
}

function formatPresignedUrl(request) {
  const host = request.port ? `${request.hostname}:${request.port}` : request.hostname;
  const searchParams = new URLSearchParams();

  for (const [key, value] of Object.entries(request.query || {})) {
    if (Array.isArray(value)) {
      value.forEach((item) => {
        if (item !== undefined && item !== null) {
          searchParams.append(key, String(item));
        }
      });
      continue;
    }

    if (value !== undefined && value !== null) {
      searchParams.append(key, String(value));
    }
  }

  const queryString = searchParams.toString();
  return `${request.protocol}//${host}${request.path}${queryString ? `?${queryString}` : ''}`;
}

function buildObjectPath(bucket, key) {
  const encodedSegments = key
    .split('/')
    .filter(Boolean)
    .map((segment) => encodeURIComponent(segment));
  return `/${encodeURIComponent(bucket)}${encodedSegments.length > 0 ? `/${encodedSegments.join('/')}` : ''}`;
}

function toBase64Url(raw) {
  return Buffer.from(raw, 'utf8')
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '');
}

function appendSaveAs(processString, targetBucket, targetKey) {
  return `${processString}|sys/saveas,o_${toBase64Url(targetKey)},b_${toBase64Url(targetBucket)}`;
}

async function presignImageUrl(bucket, key, processString, expires) {
  const endpointUrl = new URL(Endpoint);
  const presigner = new S3RequestPresigner({
    credentials: s3Credentials,
    region: Region,
    sha256: Hash.bind(null, 'sha256'),
  });

  const request = new HttpRequest({
    protocol: endpointUrl.protocol,
    hostname: endpointUrl.hostname,
    port: endpointUrl.port ? Number(endpointUrl.port) : undefined,
    method: 'GET',
    path: buildObjectPath(bucket, key),
    query: {
      'x-eos-process': processString,
    },
    headers: {
      host: endpointUrl.port ? `${endpointUrl.hostname}:${endpointUrl.port}` : endpointUrl.hostname,
    },
  });

  const signedRequest = await presigner.presign(request, { expiresIn: expires });
  return formatPresignedUrl(signedRequest);
}

function buildSaveAsInfo(opts, sourceBucket) {
  const targetKey = opts['target-key'] || opts['saveas-key'];
  if (!targetKey) {
    return null;
  }

  const targetBucket = opts['target-bucket'] || opts['saveas-bucket'] || sourceBucket;
  requireBucket(targetBucket);

  return {
    targetBucket,
    targetKey: normalizeObjectKey(targetKey),
  };
}

function ensureParentDir(filePath) {
  const dir = path.dirname(filePath);
  if (dir && dir !== '.') {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function httpGet(url) {
  const transport = url.startsWith('https:') ? https : http;

  return new Promise((resolve, reject) => {
    const request = transport.get(url, (response) => {
      if (response.statusCode && response.statusCode >= 400) {
        const chunks = [];
        response.on('data', (chunk) => chunks.push(chunk));
        response.on('end', () => {
          reject(new Error(`图片处理请求失败（HTTP ${response.statusCode}）：${Buffer.concat(chunks).toString('utf8')}`));
        });
        return;
      }

      resolve(response);
    });

    request.on('error', reject);
  });
}

async function drainResponse(response) {
  return new Promise((resolve, reject) => {
    response.on('data', () => {});
    response.on('end', resolve);
    response.on('error', reject);
  });
}

async function writeResponseToFile(response, outputPath) {
  ensureParentDir(outputPath);

  return new Promise((resolve, reject) => {
    const stream = fs.createWriteStream(outputPath);
    response.pipe(stream);
    stream.on('finish', resolve);
    stream.on('error', reject);
    response.on('error', reject);
  });
}

function detectSaveAsMode(saveAsInfo, opts) {
  if (!saveAsInfo) {
    return null;
  }

  return opts.execute === 'false' || opts['dry-run'] ? 'url-only' : 'saveas';
}

async function generateUrl(opts) {
  const key = opts.key;
  const bucket = opts.bucket || EOS_Bucket;
  const processString = requireProcessString(opts);
  const expires = parseExpires(opts.expires);

  if (!key) {
    throw new Error('缺少 --key 参数');
  }

  requireBucket(bucket);

  const normalizedKey = normalizeObjectKey(key);
  const saveAsInfo = buildSaveAsInfo(opts, bucket);
  const finalProcess = saveAsInfo
    ? appendSaveAs(processString, saveAsInfo.targetBucket, saveAsInfo.targetKey)
    : processString;
  const url = await presignImageUrl(bucket, normalizedKey, finalProcess, expires);

  output({
    success: true,
    action: 'generate-url',
    bucket,
    key: normalizedKey,
    process: processString,
    finalProcess,
    saveAs: saveAsInfo,
    url,
    expiresIn: expires,
    expiresAt: new Date(Date.now() + expires * 1000).toISOString(),
    mode: detectSaveAsMode(saveAsInfo, opts) || 'download-or-view',
    message: saveAsInfo ? '图片处理持久化外链生成成功' : '图片处理外链生成成功',
  });
}

async function downloadObject(opts) {
  const key = opts.key;
  const bucket = opts.bucket || EOS_Bucket;
  const processString = requireProcessString(opts);
  const expires = parseExpires(opts.expires);
  const outputPath = opts.output;

  if (!key) {
    throw new Error('缺少 --key 参数');
  }
  if (!outputPath) {
    throw new Error('缺少 --output 参数');
  }

  requireBucket(bucket);

  const normalizedKey = normalizeObjectKey(key);
  const url = await presignImageUrl(bucket, normalizedKey, processString, expires);
  const response = await httpGet(url);
  await writeResponseToFile(response, outputPath);

  output({
    success: true,
    action: 'download-object',
    bucket,
    key: normalizedKey,
    process: processString,
    url,
    outputPath,
    expiresIn: expires,
    message: '图片处理结果下载成功',
  });
}

async function saveAsObject(opts) {
  const key = opts.key;
  const bucket = opts.bucket || EOS_Bucket;
  const processString = requireProcessString(opts);
  const expires = parseExpires(opts.expires);
  const saveAsInfo = buildSaveAsInfo(opts, bucket);

  if (!key) {
    throw new Error('缺少 --key 参数');
  }
  if (!saveAsInfo) {
    throw new Error('缺少 --target-key 参数');
  }

  requireBucket(bucket);

  const normalizedKey = normalizeObjectKey(key);
  const finalProcess = appendSaveAs(processString, saveAsInfo.targetBucket, saveAsInfo.targetKey);
  const url = await presignImageUrl(bucket, normalizedKey, finalProcess, expires);

  const shouldExecute = opts.execute !== 'false' && !opts['dry-run'];
  if (shouldExecute) {
    const response = await httpGet(url);
    await drainResponse(response);
  }

  output({
    success: true,
    action: 'saveas-object',
    bucket,
    key: normalizedKey,
    process: processString,
    finalProcess,
    targetBucket: saveAsInfo.targetBucket,
    targetKey: saveAsInfo.targetKey,
    executed: shouldExecute,
    url,
    expiresIn: expires,
    message: shouldExecute ? '图片处理持久化请求已触发' : '图片处理持久化外链生成成功（未执行）',
  });
}

const args = process.argv.slice(2);
const action = args[0];
const opts = parseArgs(args.slice(1));

if (!SecretId || !SecretKey || !Region || !Endpoint) {
  console.error(JSON.stringify({
    success: false,
    error: '环境变量中缺少必要的凭证信息，请运行 setup 脚本配置',
    missing: !SecretId ? 'EOS_ACCESS_KEY' : !SecretKey ? 'EOS_SECRET_KEY' : !Region ? 'EOS_REGION' : 'EOS_ENDPOINT',
  }));
  process.exit(1);
}

const bucketRequiredActions = ['generate-url', 'download-object', 'saveas-object'];
if (!EOS_Bucket && bucketRequiredActions.includes(action) && !opts.bucket) {
  console.error(JSON.stringify({
    success: false,
    error: '环境变量中缺少桶名信息，请运行 setup 脚本配置或通过 --bucket 指定',
    missing: 'EOS_BUCKET',
  }));
  process.exit(1);
}

const actions = {
  'generate-url': generateUrl,
  'download-object': downloadObject,
  'saveas-object': saveAsObject,
};

if (!action || !actions[action]) {
  output({
    success: false,
    error: `未知操作：${action || '(空)'}`,
    availableActions: Object.keys(actions),
    usage: 'node scripts/eos_image.mjs <action> [--option value ...]',
  });
  process.exit(1);
}

try {
  await actions[action](opts);
} catch (err) {
  output({
    success: false,
    action,
    error: err.message || String(err),
    code: err.code,
  });
  process.exit(1);
}
