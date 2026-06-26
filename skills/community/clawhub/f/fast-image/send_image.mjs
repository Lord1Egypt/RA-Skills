#!/usr/bin/env node
/**
 * fast-image: 快速发送本地图片到channel
 * - 文件小于10MB: 直接复制到 ~/.openclaw/media/browser/
 * - 文件大于等于10MB: 使用sharp压缩后复制
 * - 发送后自动删除临时文件
 *
 * 依赖: npm install sharp
 */

import { promises as fs } from 'fs';
import { spawn } from 'child_process';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 配置
const TMP_DIR = "~/.openclaw/media/browser/";
const SIZE_THRESHOLD = 10 * 1024 * 1024; // 10MB

async function ensureTmpDir() {
  await fs.mkdir(TMP_DIR, { recursive: true });
}

async function getFileSize(filePath) {
  const stats = await fs.stat(filePath);
  return stats.size;
}

async function copyOrCompress(sourcePath) {
  const fileSize = await getFileSize(sourcePath);
  const fileName = path.basename(sourcePath);
  let targetName;

  if (fileSize >= SIZE_THRESHOLD) {
    const stem = path.parse(fileName).name;
    targetName = `${stem}_compressed.jpg`;
  } else {
    targetName = fileName;
  }

  const targetPath = path.join(TMP_DIR, targetName);

  if (fileSize < SIZE_THRESHOLD) {
    await fs.copyFile(sourcePath, targetPath);
  } else {
    try {
      const sharp = (await import('sharp')).default;
      await sharp(sourcePath)
        .jpeg({ quality: 80, progressive: true })
        .toFile(targetPath);
    } catch (err) {
      console.error('FAIL: 压缩图片失败');
      process.exit(1);
    }
  }

  return targetPath;
}

function sendImage(imagePath, channel, target, message) {
  // 对于 qqbot 频道，直接输出 qqimg 标签（框架会自动解析发送）
  if (channel === 'qqbot') {
    console.log(`<qqimg>${imagePath}</qqimg>`);
    return Promise.resolve(true);
  }

  return new Promise((resolve) => {
    const args = ['message', 'send', '--media', imagePath, '--channel', channel, '--target', target];
    if (message) args.push('--message', message);

    const proc = spawn('openclaw', args, {
      stdio: 'inherit',
      shell: true
    });

    proc.on('close', (code) => {
      if (code === 0) {
        console.log('SUCCESS');
        resolve(true);
      } else {
        console.error('FAIL');
        resolve(false);
      }
    });

    proc.on('error', () => {
      console.error('FAIL');
      resolve(false);
    });
  });
}

async function cleanup(imagePath) {
  try {
    await fs.unlink(imagePath);
  } catch {}
}

async function main() {
  if (process.argv.length < 5) {
    console.error('FAIL: 参数不足');
    process.exit(1);
  }

  const sourcePath = process.argv[2];
  const channel = process.argv[3];
  const target = process.argv[4];
  const message = process.argv[5] || null;

  try {
    await fs.access(sourcePath);
  } catch {
    console.error('FAIL: 文件不存在');
    process.exit(1);
  }

  await ensureTmpDir();

  const tempPath = await copyOrCompress(sourcePath);
  const success = await sendImage(tempPath, channel, target, message);

  // qqbot 频道不删除（框架解析 <qqimg> 后自己处理），其他频道发送后删除
  if (channel !== 'qqbot') {
    await cleanup(tempPath);
  }

  process.exit(success ? 0 : 1);
}

main();
