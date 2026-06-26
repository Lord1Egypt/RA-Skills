import fs from "fs";
import path from "path";
import crypto from "crypto";
import os from "os";
import { ProxyAgent } from "undici";

// Bun 原生支持 fetch
// 图像处理建议用 sharp（需要安装）
import sharp from "sharp";

// 获取图片缓存目录
// 优先级: 1. T2P_IMAGE_DIR 环境变量
//         2. Windows: %LOCALAPPDATA%/trend2product/images
//            Linux/macOS: ~/.cache/trend2product/images
function getCacheDir(): string {
  // 1. 优先使用环境变量
  if (process.env.T2P_IMAGE_DIR) {
    return path.resolve(process.env.T2P_IMAGE_DIR);
  }

  const homeDir = os.homedir();

  // 2. 根据操作系统选择缓存目录
  if (process.platform === "win32") {
    // Windows: 使用 %LOCALAPPDATA% (C:\Users\<用户名>\AppData\Local)
    const localAppData = process.env.LOCALAPPDATA || path.join(homeDir, "AppData", "Local");
    return path.join(localAppData, "trend2product", "images");
  } else {
    // Linux/macOS: 使用 XDG 标准缓存目录 ~/.cache
    const xdgCacheDir = process.env.XDG_CACHE_HOME || path.join(homeDir, ".cache");
    return path.join(xdgCacheDir, "trend2product", "images");
  }
}

const CACHE_DIR = getCacheDir();

// ====== Types ======

export type CacheImageResult = {
  localPath: string;
  width: number;
  height: number;
  fromCache: boolean;
  hash: string;
};

// ====== Init ======

function ensureDirs() {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
  }
}

// ====== Hash ======

function hashUrl(url: string): string {
  return crypto.createHash("md5").update(url).digest("hex");
}

// ====== Path ======

function getImagePath(hash: string): string {
  const subdir = hash.slice(0, 2);
  const dir = path.join(CACHE_DIR, subdir);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  return path.join(dir, `${hash}.jpg`);
}

// ====== Download ======

async function downloadImage(url: string, retries = 2, useProxy = true): Promise<Buffer> {
  const proxy = process.env.T2P_PROXY;
  try {
    let fetchOptions: any = {};

    if (proxy && useProxy) {
      // @ts-ignore
      if (process.versions.bun) {
        // 在 Bun 环境中，使用其原生的 proxy 选项
        fetchOptions.proxy = proxy;
      } else {
        fetchOptions.dispatcher = new ProxyAgent(proxy);
      }
    }

    // Add headers to avoid blocking
    // Dynamic referer based on target domain
    let referer = 'https://www.google.com/';
    if (url.includes('pinimg.com') || url.includes('pinterest.com')) {
      referer = 'https://www.pinterest.com/';
    } else if (url.includes('facebook.com') || url.includes('fbcdn.net')) {
      referer = 'https://www.facebook.com/';
    } else if (url.includes('instagram.com') || url.includes('cdninstagram.com')) {
      referer = 'https://www.instagram.com/';
    } else if (url.includes('amazon.com') || url.includes('amazonaws.com')) {
      referer = 'https://www.amazon.com/';
    } else if (url.includes('temu.com')) {
      referer = 'https://www.temu.com/';
    }

    fetchOptions.headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9',
      'Referer': referer,
    };

    const res = await fetch(url, fetchOptions);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const buffer = Buffer.from(await res.arrayBuffer());
    return buffer;
  } catch (err) {
    if (retries > 0) {
      return downloadImage(url, retries - 1, useProxy);
    }
    throw err;
  }
}

// ====== Main ======

export async function cacheImage(
  url: string,
  options?: {
    resize?: { width: number; height: number };
  }
): Promise<CacheImageResult> {
  ensureDirs();

  const hash = hashUrl(url);
  const localPath = getImagePath(hash);

  // ====== Cache Hit ======
  if (fs.existsSync(localPath)) {
    const meta = await sharp(localPath).metadata();
    return {
      localPath,
      width: meta.width || 0,
      height: meta.height || 0,
      fromCache: true,
      hash,
    };
  }

  // ====== Download ======
  const buffer = await downloadImage(url);

  // ====== Resize ======
  let image = sharp(buffer);

  if (options?.resize) {
    image = image.resize(options.resize.width, options.resize.height, {
      fit: "inside",
    });
  }

  await image.jpeg({ quality: 90 }).toFile(localPath);

  const meta = await sharp(localPath).metadata();

  return {
    localPath,
    width: meta.width || 0,
    height: meta.height || 0,
    fromCache: false,
    hash,
  };
}

// ====== Utils ======

export function hasCache(url: string): boolean {
  const hash = hashUrl(url);
  const localPath = getImagePath(hash);
  return fs.existsSync(localPath);
}

export function getCachedPath(url: string): string | null {
  const hash = hashUrl(url);
  const localPath = getImagePath(hash);
  return fs.existsSync(localPath) ? localPath : null;
}

export function clearCache() {
  if (fs.existsSync(CACHE_DIR)) {
    fs.rmSync(CACHE_DIR, { recursive: true, force: true });
  }
}