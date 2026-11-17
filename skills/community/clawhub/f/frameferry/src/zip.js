const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');

const ZIP32_MAX = 0xffffffff;
const ZIP32_ENTRY_LIMIT = 0xffff;
const DATA_DESCRIPTOR_SIGNATURE = 0x08074b50;
const LOCAL_FILE_HEADER_SIGNATURE = 0x04034b50;
const CENTRAL_DIRECTORY_SIGNATURE = 0x02014b50;
const EOCD_SIGNATURE = 0x06054b50;
const GP_FLAG_DATA_DESCRIPTOR = 0x0008;
const METHOD_STORE = 0;
const VERSION_NEEDED = 20;
const VERSION_MADE_BY = 20;

const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let j = 0; j < 8; j++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    table[i] = c >>> 0;
  }
  return table;
})();

function crc32Init() { return 0xffffffff; }
function crc32Update(crc, buf) {
  let value = crc >>> 0;
  for (let i = 0; i < buf.length; i++) value = CRC_TABLE[(value ^ buf[i]) & 0xff] ^ (value >>> 8);
  return value >>> 0;
}
function crc32Final(crc) { return (crc ^ 0xffffffff) >>> 0; }
function crc32(buf) { return crc32Final(crc32Update(crc32Init(), buf)); }

function toDosDateTime(date = new Date()) {
  const year = Math.max(1980, date.getUTCFullYear());
  const dosTime = ((date.getUTCHours() & 0x1f) << 11) | ((date.getUTCMinutes() & 0x3f) << 5) | ((Math.floor(date.getUTCSeconds() / 2)) & 0x1f);
  const dosDate = (((year - 1980) & 0x7f) << 9) | (((date.getUTCMonth() + 1) & 0xf) << 5) | (date.getUTCDate() & 0x1f);
  return { dosTime, dosDate };
}

function validateEntryName(name) {
  if (!name || typeof name !== 'string') throw new Error('zip entry name required');
  if (name.startsWith('/') || /^[A-Za-z]:/.test(name) || name.includes('\\')) throw new Error('zip entry name must be relative with forward slashes');
  const parts = name.split('/');
  if (parts.some(part => !part || part === '.' || part === '..')) throw new Error('zip entry name must not contain traversal');
  return name;
}

class ZipWriter {
  constructor(file, { maxEntries = ZIP32_ENTRY_LIMIT, maxBytes = ZIP32_MAX - 1024 } = {}) {
    this.file = file;
    this.maxEntries = maxEntries;
    this.maxBytes = maxBytes;
    this.entries = [];
    this.offset = 0;
    this.fh = null;
    this.closed = false;
  }

  static async create(file, opts = {}) {
    await fsp.mkdir(path.dirname(file), { recursive: true, mode: 0o700 });
    const writer = new ZipWriter(file, opts);
    writer.fh = await fsp.open(file, 'wx', 0o600);
    return writer;
  }

  async #write(buf) {
    if (!Buffer.isBuffer(buf)) buf = Buffer.from(buf);
    if (this.offset + buf.length > this.maxBytes) throw new Error('zip exceeds configured size limit');
    await this.fh.write(buf, 0, buf.length, this.offset);
    this.offset += buf.length;
  }

  #startEntry(name, mtime) {
    const filename = Buffer.from(validateEntryName(name), 'utf8');
    const { dosTime, dosDate } = toDosDateTime(mtime);
    const header = Buffer.alloc(30 + filename.length);
    header.writeUInt32LE(LOCAL_FILE_HEADER_SIGNATURE, 0);
    header.writeUInt16LE(VERSION_NEEDED, 4);
    header.writeUInt16LE(GP_FLAG_DATA_DESCRIPTOR, 6);
    header.writeUInt16LE(METHOD_STORE, 8);
    header.writeUInt16LE(dosTime, 10);
    header.writeUInt16LE(dosDate, 12);
    header.writeUInt32LE(0, 14);
    header.writeUInt32LE(0, 18);
    header.writeUInt32LE(0, 22);
    header.writeUInt16LE(filename.length, 26);
    header.writeUInt16LE(0, 28);
    filename.copy(header, 30);
    return { name, filename, dosTime, dosDate, headerOffset: this.offset, crc32: 0, compressedSize: 0, uncompressedSize: 0, mtime };
  }

  async #finishEntry(entry) {
    const descriptor = Buffer.alloc(16);
    descriptor.writeUInt32LE(DATA_DESCRIPTOR_SIGNATURE, 0);
    descriptor.writeUInt32LE(entry.crc32 >>> 0, 4);
    descriptor.writeUInt32LE(entry.compressedSize >>> 0, 8);
    descriptor.writeUInt32LE(entry.uncompressedSize >>> 0, 12);
    await this.#write(descriptor);
    this.entries.push(entry);
  }

  async addBuffer(name, buffer, { mtime = new Date() } = {}) {
    if (this.closed) throw new Error('zip already closed');
    if (this.entries.length >= this.maxEntries) throw new Error('zip exceeds entry limit');
    const data = Buffer.isBuffer(buffer) ? buffer : Buffer.from(buffer);
    if (data.length > ZIP32_MAX) throw new Error('zip entry exceeds ZIP32 size limit');
    const entry = this.#startEntry(name, mtime);
    await this.#write(Buffer.alloc(30 + entry.filename.length));
    const header = Buffer.alloc(30 + entry.filename.length);
    header.writeUInt32LE(LOCAL_FILE_HEADER_SIGNATURE, 0);
    header.writeUInt16LE(VERSION_NEEDED, 4);
    header.writeUInt16LE(GP_FLAG_DATA_DESCRIPTOR, 6);
    header.writeUInt16LE(METHOD_STORE, 8);
    header.writeUInt16LE(entry.dosTime, 10);
    header.writeUInt16LE(entry.dosDate, 12);
    header.writeUInt16LE(entry.filename.length, 26);
    entry.filename.copy(header, 30);
    await this.fh.write(header, 0, header.length, entry.headerOffset);
    await this.#write(data);
    entry.crc32 = crc32(data);
    entry.compressedSize = data.length;
    entry.uncompressedSize = data.length;
    await this.#finishEntry(entry);
  }

  async addFile(name, sourcePath, { mtime = new Date() } = {}) {
    if (this.closed) throw new Error('zip already closed');
    if (this.entries.length >= this.maxEntries) throw new Error('zip exceeds entry limit');
    const st = await fsp.stat(sourcePath);
    if (!st.isFile()) throw new Error('zip source must be a regular file');
    if (st.size > ZIP32_MAX) throw new Error('zip entry exceeds ZIP32 size limit');
    const entry = this.#startEntry(name, mtime);
    const header = Buffer.alloc(30 + entry.filename.length);
    header.writeUInt32LE(LOCAL_FILE_HEADER_SIGNATURE, 0);
    header.writeUInt16LE(VERSION_NEEDED, 4);
    header.writeUInt16LE(GP_FLAG_DATA_DESCRIPTOR, 6);
    header.writeUInt16LE(METHOD_STORE, 8);
    header.writeUInt16LE(entry.dosTime, 10);
    header.writeUInt16LE(entry.dosDate, 12);
    header.writeUInt16LE(entry.filename.length, 26);
    entry.filename.copy(header, 30);
    await this.#write(header);
    let crc = crc32Init();
    let bytes = 0;
    const stream = fs.createReadStream(sourcePath);
    try {
      for await (const chunkRaw of stream) {
        const chunk = Buffer.from(chunkRaw);
        bytes += chunk.length;
        if (bytes > ZIP32_MAX) throw new Error('zip entry exceeds ZIP32 size limit');
        crc = crc32Update(crc, chunk);
        await this.#write(chunk);
      }
    } finally {
      stream.destroy();
    }
    entry.crc32 = crc32Final(crc);
    entry.compressedSize = bytes;
    entry.uncompressedSize = bytes;
    await this.#finishEntry(entry);
  }

  async close() {
    if (this.closed) return;
    if (this.entries.length > ZIP32_ENTRY_LIMIT) throw new Error('zip exceeds ZIP32 entry limit');
    const centralStart = this.offset;
    for (const entry of this.entries) {
      if (entry.headerOffset > ZIP32_MAX) throw new Error('zip requires ZIP64 offset support');
      const header = Buffer.alloc(46 + entry.filename.length);
      header.writeUInt32LE(CENTRAL_DIRECTORY_SIGNATURE, 0);
      header.writeUInt16LE(VERSION_MADE_BY, 4);
      header.writeUInt16LE(VERSION_NEEDED, 6);
      header.writeUInt16LE(GP_FLAG_DATA_DESCRIPTOR, 8);
      header.writeUInt16LE(METHOD_STORE, 10);
      header.writeUInt16LE(entry.dosTime, 12);
      header.writeUInt16LE(entry.dosDate, 14);
      header.writeUInt32LE(entry.crc32 >>> 0, 16);
      header.writeUInt32LE(entry.compressedSize >>> 0, 20);
      header.writeUInt32LE(entry.uncompressedSize >>> 0, 24);
      header.writeUInt16LE(entry.filename.length, 28);
      header.writeUInt16LE(0, 30);
      header.writeUInt16LE(0, 32);
      header.writeUInt16LE(0, 34);
      header.writeUInt16LE(0, 36);
      header.writeUInt32LE(0, 38);
      header.writeUInt32LE(entry.headerOffset >>> 0, 42);
      entry.filename.copy(header, 46);
      await this.#write(header);
    }
    const centralSize = this.offset - centralStart;
    if (centralStart > ZIP32_MAX || centralSize > ZIP32_MAX) throw new Error('zip requires ZIP64 central directory support');
    const eocd = Buffer.alloc(22);
    eocd.writeUInt32LE(EOCD_SIGNATURE, 0);
    eocd.writeUInt16LE(0, 4);
    eocd.writeUInt16LE(0, 6);
    eocd.writeUInt16LE(this.entries.length, 8);
    eocd.writeUInt16LE(this.entries.length, 10);
    eocd.writeUInt32LE(centralSize >>> 0, 12);
    eocd.writeUInt32LE(centralStart >>> 0, 16);
    eocd.writeUInt16LE(0, 20);
    await this.#write(eocd);
    await this.fh.close();
    this.closed = true;
  }

  async abort() {
    try { if (this.fh) await this.fh.close(); } catch {}
    this.closed = true;
  }
}

module.exports = { ZipWriter, ZIP32_MAX, ZIP32_ENTRY_LIMIT, crc32, validateEntryName };