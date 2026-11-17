#!/usr/bin/env node
/**
 * Extract the Candidate XML embedded in a PDF produced by the Europass editor (or by any tool that
 * follows the same convention: an embedded file "attachment.xml").
 *
 *   node tools/extract-xml.mjs europass-cv.pdf > cv.xml
 *
 * No dependencies: it scans the PDF for /EmbeddedFile streams and inflates them (the editor uses a
 * single FlateDecode filter). If the PDF uses object streams or another filter this prints an error;
 * fall back to `pdfdetach -saveall` (poppler) or pypdf's `reader.attachments`.
 */
import { readFileSync } from "node:fs";
import { inflateSync } from "node:zlib";

const file = process.argv[2];
if (!file) {
  console.error("usage: node tools/extract-xml.mjs file.pdf > cv.xml");
  process.exit(2);
}
const buf = readFileSync(file);
const latin = buf.toString("latin1");

const found = [];
const re = /\/Type\s*\/EmbeddedFile[^]*?stream\r?\n/g;
let m;
while ((m = re.exec(latin))) {
  const dict = latin.slice(Math.max(0, m.index - 400), m.index + m[0].length);
  const start = m.index + m[0].length;
  const end = latin.indexOf("endstream", start);
  if (end < 0) continue;
  let raw = buf.subarray(start, end);
  // Trim the EOL before endstream.
  while (raw.length && (raw[raw.length - 1] === 0x0a || raw[raw.length - 1] === 0x0d)) raw = raw.subarray(0, raw.length - 1);
  const flate = /\/Filter\s*\/FlateDecode/.test(dict) || /\/Filter\s*\[\s*\/FlateDecode\s*\]/.test(dict);
  try {
    const bytes = flate ? inflateSync(raw) : raw;
    const text = bytes.toString("utf8");
    if (text.includes("<Candidate") || text.includes("Candidate>")) found.push(text);
  } catch (e) {
    console.error(`warning: an embedded stream could not be inflated (${e.message})`);
  }
}

if (!found.length) {
  console.error("No Candidate XML found among the embedded files. Is this a PDF exported by the Europass editor? Try `pdfdetach -saveall file.pdf`.");
  process.exit(1);
}
if (found.length > 1) console.error(`warning: ${found.length} Candidate documents found, printing the first`);
process.stdout.write(found[0].trimEnd() + "\n");
