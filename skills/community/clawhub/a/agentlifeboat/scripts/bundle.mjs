// The env bundle (KIN-113): chosen environment variables travel inside the snapshot plaintext, encrypted with it,
// so a restored room gets its wallet key and API keys back. Frame: "ESTB" + 4-byte big-endian header length +
// header JSON + the OpenClaw backup archive. A plaintext without the magic is an archive alone (older snapshots).
// The sidecar has the same logic in TypeScript (apps/sidecar/src/bundle.ts).

export const MAGIC = Buffer.from("ESTB", "ascii");
export const FORMAT_V2 = "estate-snapshot-v2+age";
export const FORMAT_V1 = "openclaw-backup+age";
export const BUNDLE_LIMITS = { vars: 100, bytes: 64 * 1024 };
const ENV_NAME = /^[A-Z_][A-Z0-9_]*$/;

/**
 * Which variables to carry: `spec` is ESTATE_ENV_BUNDLE (undefined or "" = default, "off" = none, "A,B" = exactly those).
 * The default is the wallet key plus every name the environment record says is set (config references, skills' requires.env).
 */
export function selectBundleNames(spec, record) {
  if (spec !== undefined && spec.trim().toLowerCase() === "off") return [];
  const names = new Set();
  if (spec !== undefined && spec.trim() !== "") {
    for (const n of spec.split(",").map((s) => s.trim())) if (ENV_NAME.test(n)) names.add(n);
  } else {
    names.add("X402_PRIVATE_KEY");
    for (const e of record?.envVars ?? []) if (e.set && ENV_NAME.test(e.name)) names.add(e.name);
  }
  // The wallet key goes first whatever the spec says: the caps must never drop it behind a long tail of other names.
  const rest = [...names].filter((n) => n !== "X402_PRIVATE_KEY").sort();
  return names.has("X402_PRIVATE_KEY") ? ["X402_PRIVATE_KEY", ...rest] : rest;
}

/** The bundle: values of the selected names that are set, within the caps (later names dropped once a cap is hit). */
export function collectBundle(names, env) {
  const out = {};
  let bytes = 0;
  for (const n of names) {
    const v = env[n];
    if (v === undefined || v === "") continue;
    if (Object.keys(out).length >= BUNDLE_LIMITS.vars) break;
    const size = Buffer.byteLength(n + "=" + v, "utf8");
    if (bytes + size > BUNDLE_LIMITS.bytes) break;
    out[n] = v;
    bytes += size;
  }
  return out;
}

/** Plaintext = frame(header, archive). `env` empty still frames (a v2 snapshot that carries nothing). */
export function frame(header, archive) {
  const json = Buffer.from(JSON.stringify({ v: 1, ...header }), "utf8");
  const len = Buffer.alloc(4);
  len.writeUInt32BE(json.length, 0);
  return Buffer.concat([MAGIC, len, json, Buffer.from(archive)]);
}

/** { header, archive } for a framed plaintext; { header: undefined, archive: bytes } for an archive alone. */
export function unframe(bytes) {
  const b = Buffer.from(bytes);
  if (b.length < 8 || !b.subarray(0, 4).equals(MAGIC)) return { header: undefined, archive: b };
  const len = b.readUInt32BE(4);
  if (len > 1024 * 1024 || 8 + len > b.length) throw new Error("snapshot frame: bad header length");
  let header;
  try {
    header = JSON.parse(b.subarray(8, 8 + len).toString("utf8"));
  } catch {
    throw new Error("snapshot frame: header is not JSON");
  }
  if (!header || typeof header !== "object" || header.v !== 1) throw new Error("snapshot frame: unknown header version");
  const env = {};
  for (const [k, v] of Object.entries(header.env ?? {})) if (ENV_NAME.test(k) && typeof v === "string") env[k] = v;
  return { header: { v: 1, env }, archive: b.subarray(8 + len) };
}

/**
 * A file the gateway entrypoint can source: one line per variable that exports it only when the process does not
 * already have it (the room's own environment wins), the value single-quoted with quotes escaped.
 */
export function renderEnvFile(env) {
  const lines = Object.entries(env)
    .filter(([k]) => ENV_NAME.test(k))
    .sort(([a], [b]) => (a < b ? -1 : 1))
    .map(([k, v]) => `[ -n "\${${k}+x}" ] || export ${k}='${String(v).replace(/'/g, "'\\''")}'`);
  return lines.join("\n") + (lines.length ? "\n" : "");
}

/** The inverse of renderEnvFile for a file this code wrote (the sidecar reads it back to carry a bundle forward). */
export function parseEnvFile(text) {
  const out = {};
  for (const m of text.matchAll(/^\[ -n "\$\{([A-Z_][A-Z0-9_]*)\+x\}" \] \|\| export \1='((?:[^']|'\\'')*)'$/gm)) out[m[1]] = m[2].replace(/'\\''/g, "'");
  return out;
}
