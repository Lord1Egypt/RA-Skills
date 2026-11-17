// Minimal ZIP reader — Node std only (zlib). Enough for OOXML (.docx/.xlsx/.pptx).
// 极简 ZIP 读取器，只用 Node 标准库，够读 OOXML。
import { inflateRawSync } from 'node:zlib';

const SIG_EOCD = 0x06054b50;
const SIG_CD = 0x02014b50;
const SIG_LOCAL = 0x04034b50;

export function readZip(buf) {
  let eocd = -1;
  const floor = Math.max(0, buf.length - 22 - 65536);
  for (let i = buf.length - 22; i >= floor; i--) {
    if (buf.readUInt32LE(i) === SIG_EOCD) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error('not a zip archive');

  const count = buf.readUInt16LE(eocd + 10);
  let off = buf.readUInt32LE(eocd + 16);
  const files = new Map();

  for (let n = 0; n < count && off + 46 <= buf.length; n++) {
    if (buf.readUInt32LE(off) !== SIG_CD) break;
    const method = buf.readUInt16LE(off + 10);
    const compSize = buf.readUInt32LE(off + 20);
    const nameLen = buf.readUInt16LE(off + 28);
    const extraLen = buf.readUInt16LE(off + 30);
    const commentLen = buf.readUInt16LE(off + 32);
    const localOff = buf.readUInt32LE(off + 42);
    const name = buf.toString('utf8', off + 46, off + 46 + nameLen);
    files.set(name, { method, compSize, localOff });
    off += 46 + nameLen + extraLen + commentLen;
  }

  return {
    names: () => [...files.keys()],
    read(name) {
      const f = files.get(name);
      if (!f) return null;
      const lo = f.localOff;
      if (buf.readUInt32LE(lo) !== SIG_LOCAL) return null;
      const nameLen = buf.readUInt16LE(lo + 26);
      const extraLen = buf.readUInt16LE(lo + 28);
      const start = lo + 30 + nameLen + extraLen;
      const raw = buf.subarray(start, start + f.compSize);
      return f.method === 0 ? Buffer.from(raw) : inflateRawSync(raw);
    },
  };
}
