'use strict';

// Apple's epoch, 2001-01-01T00:00:00Z, in Unix milliseconds.
const APPLE_EPOCH_MS = 978307200000;

/**
 * chat.db date (nanoseconds since 2001, or seconds before macOS 10.13) into a
 * Date. Accepts a number or a BigInt; 0 and null mean no date.
 */
function appleDate(raw) {
  if (raw === null || raw === undefined) return null;
  const n = BigInt(raw);
  if (n === 0n) return null;
  const ms = n > 100000000000n ? Number(n / 1000000n) : Number(n) * 1000;
  return new Date(APPLE_EPOCH_MS + ms);
}

/** A Date into chat.db nanoseconds, as a BigInt for comparing in SQL. */
function toAppleNanos(date) {
  return BigInt(date.getTime() - APPLE_EPOCH_MS) * 1000000n;
}

/**
 * The plain text inside an attributedBody blob, an NSArchiver typedstream of
 * an NSAttributedString. The string follows the NSString class name as
 * `+`, a typedstream length (one byte, or 0x81 then uint16, or 0x82 then
 * uint32, little endian), then UTF-8 bytes.
 */
function decodeAttributedBody(blob) {
  if (!blob) return null;
  const buf = Buffer.isBuffer(blob) ? blob : Buffer.from(blob);
  const marker = buf.indexOf('NSString');
  if (marker < 0) return null;
  let i = buf.indexOf(0x2b, marker + 8);
  if (i < 0 || i > marker + 16) return null;
  i++;
  let len = buf[i];
  if (len === 0x81) {
    len = buf.readUInt16LE(i + 1);
    i += 3;
  } else if (len === 0x82) {
    len = buf.readUInt32LE(i + 1);
    i += 5;
  } else {
    i += 1;
  }
  if (len === undefined || i + len > buf.length) return null;
  return buf.subarray(i, i + len).toString('utf8');
}

/** Message text from either column, without the U+FFFC placeholders attachments leave. */
function messageText(text, attributedBody) {
  const raw = text != null && text !== '' ? text : decodeAttributedBody(attributedBody);
  if (raw == null) return null;
  const clean = raw.replace(/￼/g, '').trim();
  return clean || null;
}

module.exports = { APPLE_EPOCH_MS, appleDate, toAppleNanos, decodeAttributedBody, messageText };
