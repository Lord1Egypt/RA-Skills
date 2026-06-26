import { lstat, readFile, realpath, stat } from "node:fs/promises";
import { basename, isAbsolute } from "node:path";

const MAX_UPLOAD_BYTES = 20 * 1024 * 1024;
const ALLOWED_IMAGE_EXTENSIONS = new Set([".png", ".jpg", ".jpeg", ".gif", ".webp"]);

export function inferUploadExtension(filePath: string): string {
  const name = basename(filePath);
  const index = name.lastIndexOf(".");
  return index >= 0 ? name.slice(index) : "";
}

export function inferUploadImageMimeType(filePath: string): string {
  const extension = inferUploadExtension(filePath).toLowerCase();
  switch (extension) {
    case ".png":
      return "image/png";
    case ".jpg":
    case ".jpeg":
      return "image/jpeg";
    case ".gif":
      return "image/gif";
    case ".webp":
      return "image/webp";
    default:
      throw new Error(`Unsupported upload image extension: ${extension || "(none)"}`);
  }
}

function isSupportedImageHeader(extension: string, header: Buffer): boolean {
  if (extension === ".png") {
    return header.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
  }
  if (extension === ".jpg" || extension === ".jpeg") {
    return header[0] === 0xff && header[1] === 0xd8 && header[2] === 0xff;
  }
  if (extension === ".gif") {
    const signature = header.subarray(0, 6).toString("ascii");
    return signature === "GIF87a" || signature === "GIF89a";
  }
  if (extension === ".webp") {
    return header.subarray(0, 4).toString("ascii") === "RIFF" && header.subarray(8, 12).toString("ascii") === "WEBP";
  }
  return false;
}

export function assertSafeUploadFileName(fileName: string) {
  if (fileName !== basename(fileName) || fileName.startsWith(".") || fileName.includes("\0")) {
    throw new Error(`Unsafe upload file name: ${fileName}`);
  }
}

export async function validateLocalImageUpload(filePath: string): Promise<{ realPath: string; mimeType: string }> {
  if (!isAbsolute(filePath)) {
    throw new Error(`Upload path must be absolute: ${filePath}`);
  }

  const linkStats = await lstat(filePath);
  if (linkStats.isSymbolicLink()) {
    throw new Error(`Upload path must not be a symbolic link: ${filePath}`);
  }
  if (!linkStats.isFile()) {
    throw new Error(`Upload path must be a regular image file: ${filePath}`);
  }
  if (linkStats.size <= 0 || linkStats.size > MAX_UPLOAD_BYTES) {
    throw new Error(`Upload image size must be between 1 byte and ${MAX_UPLOAD_BYTES} bytes: ${filePath}`);
  }

  const realPath = await realpath(filePath);
  const realStats = await stat(realPath);
  if (!realStats.isFile()) {
    throw new Error(`Upload path must resolve to a regular image file: ${filePath}`);
  }

  const extension = inferUploadExtension(realPath).toLowerCase();
  if (!ALLOWED_IMAGE_EXTENSIONS.has(extension)) {
    throw new Error(`Unsupported upload image extension: ${extension || "(none)"}`);
  }

  const header = await readFile(realPath, { flag: "r" }).then((buffer) => buffer.subarray(0, 12));
  if (!isSupportedImageHeader(extension, header)) {
    throw new Error(`Upload file does not match supported image signature: ${filePath}`);
  }

  return {
    realPath,
    mimeType: inferUploadImageMimeType(realPath)
  };
}

export async function readValidatedLocalImageUpload(filePath: string): Promise<{
  bytes: ArrayBuffer;
  fileName: string;
  mimeType: string;
  realPath: string;
}> {
  const validated = await validateLocalImageUpload(filePath);
  const bytes = await readFile(validated.realPath);
  return {
    ...validated,
    bytes: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength) as ArrayBuffer,
    fileName: basename(validated.realPath)
  };
}
