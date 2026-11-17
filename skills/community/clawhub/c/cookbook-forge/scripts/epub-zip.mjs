#!/usr/bin/env node
// epub-zip.mjs
//
// 将一个目录打包为合规的 EPUB 文件（手写 ZIP，Node 内置 zlib，零外部依赖）。
//
// 用法（CLI）：
//   node epub-zip.mjs <src_dir> <out.epub>
//
// 用法（API）：
//   import { buildEpub } from "./epub-zip.mjs";
//   await buildEpub("epub/build", "epub/book.epub");
//
// EPUB 规范要点：
// - mimetype 必须是 zip 中第一个条目
// - mimetype 必须 STORED（不压缩）、内容固定为 application/epub+zip
// - 其他文件可 DEFLATE 压缩
//
// 不要用 PowerShell 的 Compress-Archive，它生成的 zip 不满足上述要求。

import { promises as fs, constants as FSConst } from "node:fs";
import path from "node:path";
import zlib from "node:zlib";
import { pathToFileURL } from "node:url";

const MIMETYPE = "application/epub+zip";

// ---------- 最小 ZIP 写入器 ----------

function crc32(buf) {
  let c;
  const table = crc32.table || (crc32.table = (() => {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      c = n;
      for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[n] = c >>> 0;
    }
    return t;
  })());
  c = 0xFFFFFFFF;
  for (let i = 0; i < buf.length; i++) c = table[(c ^ buf[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}

function dosDateTime(d) {
  const time = ((d.getHours() & 0x1F) << 11) |
               ((d.getMinutes() & 0x3F) << 5) |
               ((d.getSeconds() / 2) & 0x1F);
  const date = (((d.getFullYear() - 1980) & 0x7F) << 9) |
               (((d.getMonth() + 1) & 0x0F) << 5) |
               (d.getDate() & 0x1F);
  return { time, date };
}

async function walkDir(dir, base = dir) {
  const out = [];
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const ent of entries) {
    const full = path.join(dir, ent.name);
    const rel = path.relative(base, full).split(path.sep).join("/");
    if (ent.isDirectory()) {
      out.push(...await walkDir(full, base));
    } else {
      out.push({ full, rel });
    }
  }
  return out;
}

export async function buildEpub(srcDir, outFile) {
  srcDir = path.resolve(srcDir);
  outFile = path.resolve(outFile);

  try {
    const st = await fs.stat(srcDir);
    if (!st.isDirectory()) throw new Error(`源目录不存在：${srcDir}`);
  } catch (e) {
    throw new Error(`源目录不存在：${srcDir}`);
  }

  // 1) 确保 mimetype 文件存在且内容正确
  await fs.writeFile(path.join(srcDir, "mimetype"), MIMETYPE, "ascii");

  // 2) 收集所有文件，强制 mimetype 在最前
  const allFiles = await walkDir(srcDir);
  const ordered = [];
  const rest = [];
  for (const f of allFiles) {
    if (f.rel === "mimetype") ordered.unshift(f);
    else rest.push(f);
  }
  ordered.push(...rest);

  try { await fs.unlink(outFile); } catch {}

  const chunks = [];
  const central = [];
  let offset = 0;
  const now = new Date();
  const { time: dosTime, date: dosDate } = dosDateTime(now);

  function writeChunk(buf) {
    chunks.push(buf);
    offset += buf.length;
  }

  function writeU16LE(n) {
    const b = Buffer.alloc(2); b.writeUInt16LE(n, 0); return b;
  }
  function writeU32LE(n) {
    const b = Buffer.alloc(4); b.writeUInt32LE(n >>> 0, 0); return b;
  }

  for (const { full, rel } of ordered) {
    const data = await fs.readFile(full);
    const isMimetype = rel === "mimetype";
    const method = isMimetype ? 0 : 8; // STORED or DEFLATE
    const compData = isMimetype ? data : zlib.deflateRawSync(data, { level: 9 });
    const crc = crc32(data);

    const nameBuf = Buffer.from(rel, "utf8");

    // Local file header
    const localHeader = Buffer.concat([
      writeU32LE(0x04034b50),     // signature
      writeU16LE(20),             // version needed
      writeU16LE(0x0800),         // general purpose (bit 11 = UTF-8 names)
      writeU16LE(method),         // compression
      writeU16LE(dosTime),
      writeU16LE(dosDate),
      writeU32LE(crc),
      writeU32LE(compData.length),
      writeU32LE(data.length),
      writeU16LE(nameBuf.length),
      writeU16LE(0),              // extra len
      nameBuf,
    ]);

    const entryOffset = offset;
    writeChunk(localHeader);
    writeChunk(compData);

    // Central directory entry (will be written later)
    central.push({
      name: nameBuf, method, crc,
      compSize: compData.length, uncompSize: data.length,
      offset: entryOffset, dosTime, dosDate,
    });
  }

  const centralStart = offset;
  for (const c of central) {
    const cd = Buffer.concat([
      writeU32LE(0x02014b50),     // signature
      writeU16LE(20),             // version made by
      writeU16LE(20),             // version needed
      writeU16LE(0x0800),         // flags (UTF-8)
      writeU16LE(c.method),
      writeU16LE(c.dosTime),
      writeU16LE(c.dosDate),
      writeU32LE(c.crc),
      writeU32LE(c.compSize),
      writeU32LE(c.uncompSize),
      writeU16LE(c.name.length),
      writeU16LE(0),              // extra
      writeU16LE(0),              // comment
      writeU16LE(0),              // disk
      writeU16LE(0),              // internal attrs
      writeU32LE(0),              // external attrs
      writeU32LE(c.offset),
      c.name,
    ]);
    writeChunk(cd);
  }
  const centralSize = offset - centralStart;

  // End of central directory
  writeChunk(Buffer.concat([
    writeU32LE(0x06054b50),
    writeU16LE(0),
    writeU16LE(0),
    writeU16LE(central.length),
    writeU16LE(central.length),
    writeU32LE(centralSize),
    writeU32LE(centralStart),
    writeU16LE(0),
  ]));

  await fs.writeFile(outFile, Buffer.concat(chunks));

  // 3) 自检：读回校验 mimetype 首条且 STORED，并遍历 central directory
  const buf = await fs.readFile(outFile);

  // 3a) 第一个 local header 必须是 mimetype + STORED
  if (buf.readUInt32LE(0) !== 0x04034b50) throw new Error("ZIP local header 签名错误");
  if (buf.readUInt16LE(8) !== 0) throw new Error("mimetype 必须为 STORED（未压缩）");
  const nameLen0 = buf.readUInt16LE(26);
  if (buf.slice(30, 30 + nameLen0).toString("utf8") !== "mimetype") {
    throw new Error("zip 第一个条目不是 mimetype");
  }
  if (buf.slice(30 + nameLen0, 30 + nameLen0 + MIMETYPE.length).toString("ascii") !== MIMETYPE) {
    throw new Error("mimetype 内容不正确");
  }

  // 3b) 从末尾查找 EOCD，遍历 central directory
  const eocdSig = Buffer.from([0x50, 0x4b, 0x05, 0x06]);
  let eocdOff = -1;
  for (let i = buf.length - 22; i >= Math.max(0, buf.length - 65557); i--) {
    if (buf[i] === 0x50 && buf.readUInt32LE(i) === 0x06054b50) { eocdOff = i; break; }
  }
  if (eocdOff < 0) throw new Error("EOCD 未找到，ZIP 损坏");
  const cdEntries = buf.readUInt16LE(eocdOff + 10);
  const cdSize = buf.readUInt32LE(eocdOff + 12);
  const cdStart = buf.readUInt32LE(eocdOff + 16);
  const entryNames = [];
  let p = cdStart;
  for (let i = 0; i < cdEntries; i++) {
    if (buf.readUInt32LE(p) !== 0x02014b50) throw new Error(`Central dir entry ${i} 签名错误`);
    const method = buf.readUInt16LE(p + 10);
    const nlen = buf.readUInt16LE(p + 28);
    const elen = buf.readUInt16LE(p + 30);
    const clen = buf.readUInt16LE(p + 32);
    const name = buf.slice(p + 46, p + 46 + nlen).toString("utf8");
    entryNames.push({ name, method });
    p += 46 + nlen + elen + clen;
  }
  if (entryNames.length !== central.length) {
    throw new Error(`Central dir entry 数不匹配：expected ${central.length}, got ${entryNames.length}`);
  }

  const st2 = await fs.stat(outFile);
  console.log(`已生成 EPUB：${outFile}`);
  console.log(`大小：${(st2.size / 1024 / 1024).toFixed(2)} MB，条目数：${entryNames.length}`);
  for (const e of entryNames.slice(0, 8)) {
    console.log(`  - ${e.name} (${e.method === 0 ? "STORED" : "DEFLATE"})`);
  }
  if (entryNames.length > 8) console.log(`  ... (+${entryNames.length - 8} more)`);
}

// ---------- CLI ----------
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [, , srcDir, outFile] = process.argv;
  if (!srcDir || !outFile) {
    console.error("用法：node epub-zip.mjs <src_dir> <out.epub>");
    process.exit(1);
  }
  buildEpub(srcDir, outFile).catch(err => {
    console.error("✗ 构建失败：", err.message);
    process.exit(1);
  });
}
