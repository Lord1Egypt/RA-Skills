// x-client-transaction-id for CreateNoteTweet.
// The 2026-11-04 capture: page.fetch without this header returned GraphQL 226;
// the same call with a header the web client had just produced returned 200.
// The mix below is the web client's: verification key, ondemand.s byte indices,
// loading-x-anim frames, then SHA-256 of method!path!time. Inputs come from
// the live x.com document. A missing input returns "" rather than a guessed id.

const KEYWORD = "obfiowerehiring";
const EXTRA = 3;
const EPOCH_MS = Date.UTC(2023, 4, 1, 7, 0, 0);
const TOTAL_TIME = 4096;

export function verificationKeyFromHtml(html) {
  const source = String(html || "");
  const named = source.match(/name=["']twitter-site-verification["'][^>]*content=["']([^"']+)["']/i);
  if (named) return named[1];
  const swapped = source.match(/content=["']([^"']+)["'][^>]*name=["']twitter-site-verification["']/i);
  return swapped ? swapped[1] : "";
}

export function onDemandFileUrl(html) {
  const source = String(html || "");
  const direct = source.match(/https:\/\/abs\.twimg\.com\/responsive-web\/client-web\/ondemand\.s\.[A-Za-z0-9_-]+\.js/);
  if (direct) return direct[0];
  const indexed = source.match(/(\d+):\s*["']ondemand\.s["']/);
  if (indexed) {
    const hash = source.match(new RegExp(`,${indexed[1]}:"([0-9a-fA-F]+)"`));
    if (hash) return `https://abs.twimg.com/responsive-web/client-web/ondemand.s.${hash[1]}a.js`;
  }
  const re = /(\d+):\s*["']ondemand\.s["'][\s\S]*?\}\)\[e\]\s*\|\|\s*e\)\s*\+\s*["']\.["']\s*\+\s*\(\{[\s\S]*?\b\1:\s*["']([a-zA-Z0-9_-]+)["']/;
  const legacy = re.exec(source)?.[2];
  if (!legacy) return "";
  return `https://abs.twimg.com/responsive-web/client-web/ondemand.s.${legacy}a.js`;
}

function tightIndexCluster(hits) {
  if (!hits.length) return null;
  let best = [];
  let run = [hits[0]];
  for (let i = 1; i < hits.length; i += 1) {
    if (hits[i].at - hits[i - 1].at < 80) run.push(hits[i]);
    else {
      if (run.length > best.length) best = run;
      run = [hits[i]];
    }
  }
  if (run.length > best.length) best = run;
  if (best.length < 2) return null;
  return best.slice(0, 6).map((hit) => hit.index);
}

export function keyByteIndices(source) {
  const text = String(source || "");
  const patterns = [
    /\(\w{1,2}\[(\d{1,2})\],\s*16\)/g,
    /\(\s*\w+\s*\[\s*(\d{1,2})\s*\]\s*,\s*16\s*\)/g,
    // X's ondemand.s after 2026-03 uses `[12], 16` without a `(name[12], 16)` wrapper.
    /\[(\d{1,3})\],\s*16/g,
  ];
  for (const pattern of patterns) {
    const hits = [];
    for (const match of text.matchAll(pattern)) {
      hits.push({ index: Number(match[1]), at: match.index });
    }
    const cluster = tightIndexCluster(hits);
    if (cluster) {
      const [rowIndex, ...keyBytesIndices] = cluster;
      return { rowIndex, keyBytesIndices };
    }
  }
  return null;
}

export function animationPathsFromHtml(html) {
  const source = String(html || "");
  const blocks = [];
  const re = /id=["']loading-x-anim-(\d+)["'][^>]*>([\s\S]*?)<\/svg>/gi;
  for (const match of source.matchAll(re)) {
    const paths = Array.from(match[2].matchAll(/\bd=["']([^"']+)["']/gi)).map((item) => item[1]);
    blocks.push({ index: Number(match[1]), path: paths[1] || paths[0] || "" });
  }
  blocks.sort((a, b) => a.index - b.index);
  return blocks.map((block) => block.path);
}

export function shellHasMaterials(html) {
  return Boolean(
    verificationKeyFromHtml(html)
    && onDemandFileUrl(html)
    && animationPathsFromHtml(html).some(Boolean),
  );
}

export function describeMissingMaterials({ html, ondemandSource, paths } = {}) {
  const missing = [];
  if (!verificationKeyFromHtml(html)) missing.push("twitter-site-verification");
  if (!onDemandFileUrl(html)) missing.push("ondemand.s url");
  else if (!keyByteIndices(ondemandSource || "")) missing.push("ondemand.s key-byte indices");
  const frames = (paths && paths.some(Boolean)) ? paths : animationPathsFromHtml(html);
  if (!frames.some(Boolean)) missing.push("loading-x-anim");
  return missing;
}

export function frameRowsFromPath(path) {
  const value = String(path || "");
  if (value.length < 9) return [];
  return value.substring(9).split("C").map((segment) => (segment.match(/\d+/g) || []).map(Number)).filter((row) => row.length);
}

export function decodeKeyBytes(key) {
  try {
    const bytes = Buffer.from(String(key || ""), "base64");
    return bytes.length ? Array.from(bytes) : [];
  } catch {
    return [];
  }
}

function interpolateNum(from, to, factor) {
  return from * (1 - factor) + to * factor;
}

function convertRotationToMatrix(rotation) {
  const rad = (rotation * Math.PI) / 180;
  return [Math.cos(rad), -Math.sin(rad), Math.sin(rad), Math.cos(rad)];
}

function floatToHex(value) {
  const integer = Math.floor(value);
  let fraction = value - integer;
  let result = integer > 0 ? integer.toString(16).toUpperCase() : "";
  if (fraction === 0) return result;
  result += ".";
  while (fraction > 0 && result.length < 24) {
    fraction *= 16;
    const digit = Math.floor(fraction);
    fraction -= digit;
    result += digit.toString(16).toUpperCase();
  }
  return result;
}

function isOdd(num) {
  return num % 2 ? -1 : 0;
}

function formatMatrixValue(value) {
  if (value === 0) return "0";
  const sign = value < 0 ? "-" : "";
  const [mantissa, exponentText] = Math.abs(value).toExponential(5).split("e");
  const exponent = parseInt(exponentText, 10);
  const digits = mantissa.replace(".", "").replace(/0+$/, "") || "0";
  if (exponent < -4 || exponent >= 6) {
    const head = digits.length > 1 ? `${digits[0]}.${digits.slice(1)}` : digits;
    const expSign = exponent < 0 ? "-" : "+";
    return `${sign}${head}e${expSign}${String(Math.abs(exponent)).padStart(2, "0")}`;
  }
  if (exponent >= 0) {
    const intPart = digits.slice(0, exponent + 1).padEnd(exponent + 1, "0");
    const fracPart = digits.slice(exponent + 1);
    return fracPart ? `${sign}${intPart}.${fracPart}` : `${sign}${intPart}`;
  }
  return `${sign}0.${"0".repeat(-exponent - 1)}${digits}`;
}

function matrixNumbers(value) {
  return (formatMatrixValue(value).match(/[\d.-]+/g) || []).map(Number);
}

class Cubic {
  constructor(curves) {
    const [x1 = 0, y1 = 0, x2 = 0, y2 = 0] = curves || [];
    this.cx = 3 * x1;
    this.bx = 3 * (x2 - x1) - this.cx;
    this.ax = 1 - this.cx - this.bx;
    this.cy = 3 * y1;
    this.by = 3 * (y2 - y1) - this.cy;
    this.ay = 1 - this.cy - this.by;
    if (x1 > 0) this.startGradient = y1 / x1;
    else if (y1 === 0 && x2 > 0) this.startGradient = y2 / x2;
    else if (y1 === 0 && y2 === 0) this.startGradient = 1;
    else this.startGradient = 0;
    if (x2 < 1) this.endGradient = (y2 - 1) / (x2 - 1);
    else if (y2 === 1 && x1 < 1) this.endGradient = (y1 - 1) / (x1 - 1);
    else if (y2 === 1 && y1 === 1) this.endGradient = 1;
    else this.endGradient = 0;
    this.samples = Array.from({ length: 11 }, (_, index) => this.sampleX(index / 10));
  }

  sampleX(t) {
    return ((this.ax * t + this.bx) * t + this.cx) * t;
  }

  sampleY(t) {
    return ((this.ay * t + this.by) * t + this.cy) * t;
  }

  getValue(time) {
    if (time < 0) return this.startGradient * time;
    if (time > 1) return 1 + this.endGradient * (time - 1);
    return this.sampleY(this.solveX(time));
  }

  solveX(x) {
    let t0 = 0;
    let t1 = 1;
    let guess = x;
    for (let i = 1; i < this.samples.length; i += 1) {
      if (x <= this.samples[i]) {
        t1 = i / 10;
        t0 = t1 - 0.1;
        const span = this.samples[i] - this.samples[i - 1] || 1;
        guess = t0 + ((t1 - t0) * (x - this.samples[i - 1])) / span;
        break;
      }
    }
    let residual = 0;
    for (let i = 0; i < 4; i += 1) {
      residual = this.sampleX(guess) - x;
      if (Math.abs(residual) < 1e-7) return guess;
      const slope = (3 * this.ax * guess + 2 * this.bx) * guess + this.cx;
      if (Math.abs(slope) < 1e-7) break;
      guess -= residual / slope;
    }
    if (Math.abs(residual) < 1e-7) return guess;
    while (t0 < t1) {
      residual = this.sampleX(guess);
      if (Math.abs(residual - x) < 1e-7) return guess;
      if (x > residual) t0 = guess;
      else t1 = guess;
      guess = (t1 + t0) * 0.5;
    }
    return guess;
  }
}

function solve(value, min, max, floor) {
  const result = (value * (max - min)) / 255 + min;
  return floor ? Math.floor(result) : Math.round(result * 100) / 100;
}

export function animationKey(keyBytes, indices, frameRows) {
  if (!indices || !Array.isArray(frameRows) || !frameRows.length) return "";
  const row = frameRows[keyBytes[indices.rowIndex] % 16];
  if (!row || row.length < 7) return "";
  const frameTime = (indices.keyBytesIndices || []).reduce((time, index) => time * ((keyBytes[index] || 0) % 16), 1);
  const target = (Math.round(frameTime / 10) * 10) / TOTAL_TIME;
  const fromColor = row.slice(0, 3);
  const toColor = row.slice(3, 6);
  const toRotation = solve(row[6], 60, 360, true);
  const curves = row.slice(7).map((value, index) => solve(value, isOdd(index), 1, false));
  const progress = new Cubic(curves).getValue(target);
  const color = fromColor.map((channel, index) => {
    const mixed = interpolateNum(channel, toColor[index], progress);
    return Math.round(Math.max(0, Math.min(255, mixed))).toString(16);
  });
  const matrix = convertRotationToMatrix(interpolateNum(0, toRotation, progress))
    .flatMap((value) => matrixNumbers(value))
    .map((number) => {
      const hex = floatToHex(Math.abs(Number(number.toFixed(2)))).toLowerCase();
      return hex.startsWith(".") ? `0${hex}` : hex || "0";
    });
  return [...color, ...matrix, "0", "0"].join("").replace(/[.-]/g, "");
}

export async function encodeTransactionId({ method, path, keyBytes, animationKey: key, timeNow, randomByte } = {}) {
  if (!keyBytes?.length || !key || !method || !path) return "";
  const time = timeNow ?? Math.floor((Date.now() - EPOCH_MS) / 1000);
  const data = `${method}!${path}!${time}${KEYWORD}${key}`;
  const hash = new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(data)));
  const salt = randomByte ?? Math.floor(Math.random() * 256);
  const bytes = [
    ...keyBytes,
    ...[0, 8, 16, 24].map((shift) => (time >> shift) & 0xff),
    ...hash.slice(0, 16),
    EXTRA,
  ];
  const out = Uint8Array.from([salt, ...bytes.map((byte) => byte ^ salt)]);
  return Buffer.from(out).toString("base64").replace(/=+$/g, "");
}

export async function buildTransactionId({ method, path, html, ondemandSource, paths, timeNow, randomByte } = {}) {
  const key = verificationKeyFromHtml(html);
  const indices = keyByteIndices(ondemandSource);
  const keyBytes = decodeKeyBytes(key);
  if (!keyBytes.length || !indices) return "";
  const selected = (paths || [])[keyBytes[5] % 4] || "";
  const rows = frameRowsFromPath(selected);
  const derived = animationKey(keyBytes, indices, rows);
  if (!derived) return "";
  return encodeTransactionId({
    method,
    path,
    keyBytes,
    animationKey: derived,
    timeNow,
    randomByte,
  });
}
