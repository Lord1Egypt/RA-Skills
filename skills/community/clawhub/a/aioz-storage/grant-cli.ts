#!/usr/bin/env npx ts-node
// @ts-nocheck
/**
 * Grant CLI - standalone grant generator with CLI interface
 *
 * Usage:
 *   # From config file
 *   npx ts-node grant-cli.ts --config config.json
 *
 *   # Per-bucket mode via flags
 *   npx ts-node grant-cli.ts \
 *     --mode per-bucket \
 *     --zkey <rootZKey> \
 *     --account <accountId> \
 *     --url w3s \
 *     --duration 0 \
 *     --bucket vinh \
 *     --passphrase "conduct muffin auto ..." \
 *     --permissions 1,2,3 \
 *     --prefix ""
 *
 *   # All-buckets mode via flags
 *   npx ts-node grant-cli.ts \
 *     --mode all-buckets \
 *     --zkey <rootZKey> \
 *     --account <accountId> \
 *     --url w3s \
 *     --duration 86400000 \
 *     --passphrase "your passphrase"
 *
 *   # Output format
 *   --output json     # JSON output (default: text)
 *   --quiet           # Only output grant and zkey, no logs
 */

import * as fs from "fs";
import * as path from "path";
import * as crypto from "crypto";
import { fileURLToPath } from "url";

// ts-node may run this file in ESM mode; __dirname is not defined there.
// Define __filename/__dirname compat to keep path logic working.
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ─── Arg parser ─────────────────────────────────────────────────────────────

function parseArgs(argv: string[]): Map<string, string[]> {
    const args = new Map<string, string[]>();
    let current: string | null = null;

    for (const arg of argv.slice(2)) {
        if (arg.startsWith("--")) {
            current = arg.slice(2);
            if (!args.has(current)) args.set(current, []);
        } else if (current) {
            args.get(current)!.push(arg);
        }
    }
    return args;
}

function getArg(args: Map<string, string[]>, key: string): string | undefined {
    const vals = args.get(key);
    return vals && vals.length > 0 ? vals.join(" ") : undefined;
}

function hasFlag(args: Map<string, string[]>, key: string): boolean {
    return args.has(key);
}

function printUsage() {
    console.log(`
Grant CLI - Standalone grant generator

USAGE:
  npx ts-node grant-cli.ts --config <file>
  npx ts-node grant-cli.ts --mode <mode> --zkey <key> --account <id> [options]

FROM CONFIG FILE:
  --config <path>         Path to config JSON file

PER-BUCKET MODE:
  --mode per-bucket
  --zkey <rootZKey>       Root ZKey (base64url)
  --account <accountId>   Account UUID
  --url <url>             Service URL (e.g. w3s)
  --duration <ms>         Duration in ms (0 = no expiry)
  --bucket <name>         Bucket name (repeatable for multiple buckets)
  --passphrase <phrase>   Passphrase for encryption key derivation
  --permissions <ops>     Comma-separated: 1=Read,2=Write,3=List,4=Delete
  --prefix <prefix>       Optional path prefix

  For multiple buckets, use --bucket multiple times with corresponding
  --passphrase and --permissions (in order):
    --bucket a --passphrase "pass a" --permissions 1
    --bucket b --passphrase "pass b" --permissions 1,2,3

ALL-BUCKETS MODE:
  --mode all-buckets
  --zkey <rootZKey>
  --account <accountId>
  --url <url>
  --duration <ms>
  --passphrase <phrase>

OUTPUT OPTIONS:
  --output json           Output as JSON (default: text)
  --quiet                 Suppress info logs, only output result
  --help                  Show this help
`);
}

// ─── Config types ───────────────────────────────────────────────────────────

interface EncryptBucket {
    name: string;
    permissions: string[];
    passphrase: string;
    prefix?: string;
}

interface PerBucketConfig {
    mode: "per-bucket";
    rootZKey: string;
    accountId: string;
    url: string;
    duration: number;
    buckets: EncryptBucket[];
}

interface AllBucketsConfig {
    mode: "all-buckets";
    rootZKey: string;
    accountId: string;
    url: string;
    duration: number;
    passphrase: string;
}

type Config = PerBucketConfig | AllBucketsConfig;

// ─── Build config from CLI args ─────────────────────────────────────────────

function buildConfigFromArgs(args: Map<string, string[]>): Config {
    const mode = getArg(args, "mode");
    const zkey = getArg(args, "zkey");
    const account = getArg(args, "account");
    const url = getArg(args, "url") || "w3s";
    const duration = parseInt(getArg(args, "duration") || "0", 10);

    if (!mode) throw new Error("--mode is required (per-bucket or all-buckets)");
    if (!zkey) throw new Error("--zkey is required");
    if (!account) throw new Error("--account is required");

    if (mode === "per-bucket") {
        const bucketNames = args.get("bucket") || [];
        const passphrases = args.get("passphrase") || [];
        const permsList = args.get("permissions") || [];
        const prefixes = args.get("prefix") || [];

        if (bucketNames.length === 0) {
            throw new Error("--bucket is required for per-bucket mode");
        }
        if (passphrases.length === 0) {
            throw new Error("--passphrase is required");
        }

        // If single passphrase/permissions, apply to all buckets
        const buckets: EncryptBucket[] = bucketNames.map((name, i) => ({
            name,
            passphrase: passphrases[i] || passphrases[0],
            permissions: (permsList[i] || permsList[0] || "1").split(","),
            prefix: prefixes[i] || prefixes[0] || undefined,
        }));

        return {
            mode: "per-bucket",
            rootZKey: zkey,
            accountId: account,
            url,
            duration,
            buckets,
        };
    } else if (mode === "all-buckets") {
        const passphrase = getArg(args, "passphrase");
        if (!passphrase) throw new Error("--passphrase is required for all-buckets mode");

        return {
            mode: "all-buckets",
            rootZKey: zkey,
            accountId: account,
            url,
            duration,
            passphrase,
        };
    } else {
        throw new Error(`Invalid mode: ${mode}. Use "per-bucket" or "all-buckets"`);
    }
}

// ─── Base64 URL helpers ─────────────────────────────────────────────────────

function b64urlEncode(buf: Uint8Array): string {
    return Buffer.from(buf)
        .toString("base64")
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=+$/, "");
}

function b64urlDecode(str: string): Uint8Array {
    const s = str
        .replace(/-/g, "+")
        .replace(/_/g, "/")
        .padEnd(str.length + ((4 - (str.length % 4)) % 4), "=");
    return new Uint8Array(Buffer.from(s, "base64"));
}

function b64Encode(buf: Uint8Array): string {
    return Buffer.from(buf).toString("base64");
}

function b64Decode(str: string): Uint8Array {
    return new Uint8Array(Buffer.from(str, "base64"));
}

// ─── Crypto helpers ─────────────────────────────────────────────────────────

function hmacSha256(key: Uint8Array, data: Uint8Array): Uint8Array {
    return new Uint8Array(crypto.createHmac("sha256", key).update(data).digest());
}

function hmacSha512(key: Uint8Array, data: Uint8Array): Uint8Array {
    return new Uint8Array(crypto.createHmac("sha512", key).update(data).digest());
}

function aesGcmEncrypt(plaintext: Uint8Array, key: Uint8Array, nonce: Uint8Array): Uint8Array {
    const iv = nonce.slice(0, 12);
    const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
    const encrypted = cipher.update(plaintext);
    const final = cipher.final();
    const tag = cipher.getAuthTag();
    const result = new Uint8Array(encrypted.length + final.length + tag.length);
    result.set(encrypted, 0);
    result.set(final, encrypted.length);
    result.set(tag, encrypted.length + final.length);
    return result;
}

// ─── Protobuf writer ────────────────────────────────────────────────────────

class PbWriter {
    buf: number[] = [];
    varint(v: number) {
        while (v > 0x7f) { this.buf.push((v & 0x7f) | 0x80); v >>>= 7; }
        this.buf.push(v);
    }
    fieldVarint(f: number, val: number) {
        if (val === 0) return;
        this.varint((f << 3) | 0); this.varint(val);
    }
    fieldBytes(f: number, data: Uint8Array) {
        if (data.length === 0) return;
        this.varint((f << 3) | 2); this.varint(data.length);
        for (let i = 0; i < data.length; i++) this.buf.push(data[i]);
    }
    fieldString(f: number, s: string) {
        if (!s) return;
        this.fieldBytes(f, new TextEncoder().encode(s));
    }
    fieldBool(f: number, val: boolean) {
        if (!val) return;
        this.varint((f << 3) | 0); this.varint(1);
    }
    fieldMessage(f: number, sub: Uint8Array) {
        this.varint((f << 3) | 2); this.varint(sub.length);
        for (let i = 0; i < sub.length; i++) this.buf.push(sub[i]);
    }
    finish(): Uint8Array { return new Uint8Array(this.buf); }
}

// ─── Protobuf encoders ─────────────────────────────────────────────────────

function encodeTimestamp(d: Date): Uint8Array {
    const w = new PbWriter();
    w.fieldVarint(1, Math.floor(d.getTime() / 1000));
    w.fieldVarint(2, (d.getTime() % 1000) * 1_000_000);
    return w.finish();
}

function encodeTimeCaveat(from: Date | null, to: Date | null): Uint8Array {
    const w = new PbWriter();
    if (to) w.fieldMessage(1, encodeTimestamp(to));
    if (from) w.fieldMessage(2, encodeTimestamp(from));
    return w.finish();
}

function encodeOpCaveat(scopes: { paths: { bucket: string; prefix: Uint8Array }[]; ops: number[] }[]): Uint8Array {
    const w = new PbWriter();
    for (const scope of scopes) {
        const sw = new PbWriter();
        for (const p of scope.paths) {
            const pw = new PbWriter();
            pw.fieldString(1, p.bucket);
            pw.fieldBytes(2, p.prefix);
            sw.fieldMessage(1, pw.finish());
        }
        if (scope.ops.length > 0) {
            const ow = new PbWriter();
            for (const op of scope.ops) ow.varint(op);
            sw.fieldMessage(2, ow.finish());
        }
        w.fieldMessage(1, sw.finish());
    }
    return w.finish();
}

interface EKeyData {
    encrAlg: number; encrBlockSize: number;
    raw: Uint8Array; path: Uint8Array; content: boolean;
}

function encodeEKeyProto(ek: EKeyData): Uint8Array {
    const w = new PbWriter();
    w.fieldVarint(1, ek.encrAlg); w.fieldVarint(2, ek.encrBlockSize);
    w.fieldBytes(3, ek.raw); w.fieldBytes(4, ek.path); w.fieldBool(5, ek.content);
    return w.finish();
}

function encodeZKeyProto(mcr: Uint8Array): Uint8Array {
    const w = new PbWriter(); w.fieldBytes(1, mcr); return w.finish();
}

function encodeGrantProto(url: string, mcr: Uint8Array, eKeysMap: Map<string, EKeyData[]>): Uint8Array {
    const w = new PbWriter();
    w.fieldMessage(1, encodeZKeyProto(mcr));
    for (const [bucket, ekeys] of eKeysMap) {
        const ew = new PbWriter();
        ew.fieldString(1, bucket);
        const lw = new PbWriter();
        for (const ek of ekeys) lw.fieldMessage(1, encodeEKeyProto(ek));
        ew.fieldMessage(2, lw.finish());
        w.fieldMessage(2, ew.finish());
    }
    w.fieldString(3, url);
    return w.finish();
}

// ─── Macaroon V2 binary ────────────────────────────────────────────────────

const F_EOS = 0, F_LOC = 1, F_ID = 2, F_VID = 4, F_SIG = 6;

function readUvarint(buf: Uint8Array, off: number): [number, number] {
    let x = 0, shift = 0, i = off;
    while (i < buf.length) {
        const b = buf[i];
        if (b < 0x80) return [(x | (b << shift)) >>> 0, i + 1];
        x |= (b & 0x7f) << shift; shift += 7; i++;
    }
    throw new Error("varint overflow");
}

function writeUvarint(v: number): number[] {
    const b: number[] = [];
    while (v >= 0x80) { b.push((v & 0xff) | 0x80); v >>>= 7; }
    b.push(v | 0); return b;
}

interface Caveat { identifier: Uint8Array; vid?: Uint8Array; location?: string; }
interface Macaroon { version: number; location?: string; identifier: Uint8Array; caveats: Caveat[]; signature: Uint8Array; }

function importMacaroonV2(data: Uint8Array): Macaroon {
    let o = 0;
    if (data[o++] !== 2) throw new Error("Not V2 macaroon");

    const readField = (expect?: number) => {
        const ft = data[o++];
        if (ft === F_EOS) return { type: F_EOS, data: new Uint8Array() };
        if (expect !== undefined && ft !== expect) { o--; return null; }
        const [len, no] = readUvarint(data, o); o = no;
        const d = data.slice(o, o + len); o += len;
        return { type: ft, data: d };
    };

    let loc: string | undefined;
    const lf = readField(F_LOC);
    if (lf) loc = new TextDecoder().decode(lf.data);

    const idf = readField(F_ID);
    if (!idf) throw new Error("Missing identifier");
    readField(F_EOS);

    const caveats: Caveat[] = [];
    while (true) {
        if (data[o] === F_EOS) { o++; break; }
        let cl: string | undefined;
        const clf = readField(F_LOC);
        if (clf) cl = new TextDecoder().decode(clf.data);
        const cid = readField(F_ID);
        if (!cid) throw new Error("Missing caveat id");
        let cv: Uint8Array | undefined;
        const vf = readField(F_VID);
        if (vf) cv = vf.data;
        readField(F_EOS);
        caveats.push({ identifier: cid.data, vid: cv, location: cl });
    }

    const sf = readField(F_SIG);
    if (!sf) throw new Error("Missing signature");
    return { version: 2, location: loc, identifier: idf.data, caveats, signature: sf.data };
}

function exportMacaroonV2(m: Macaroon): Uint8Array {
    const p: number[] = [2];
    const af = (ft: number, d?: Uint8Array) => {
        p.push(ft);
        if (ft !== F_EOS && d) { p.push(...writeUvarint(d.length)); for (let i = 0; i < d.length; i++) p.push(d[i]); }
    };
    if (m.location) af(F_LOC, new TextEncoder().encode(m.location));
    af(F_ID, m.identifier); af(F_EOS);
    for (const c of m.caveats) {
        if (c.location) af(F_LOC, new TextEncoder().encode(c.location));
        af(F_ID, c.identifier);
        if (c.vid) af(F_VID, c.vid);
        af(F_EOS);
    }
    af(F_EOS); af(F_SIG, m.signature);
    return new Uint8Array(p);
}

function addCaveat(m: Macaroon, condB64: string) {
    // Original macaroon.js stores caveat identifier as UTF-8 bytes of the base64 string
    // (not the decoded raw bytes). This matches how addFirstPartyCaveat works:
    // it calls stringToBytes(base64String) = utf8Encoder.encode(base64String)
    const cond = new TextEncoder().encode(condB64);
    m.caveats.push({ identifier: cond });
    m.signature = hmacSha256(m.signature, cond);
}

// ─── EKey derivation ────────────────────────────────────────────────────────

const SLASH = 0x2f;

function* pathIter(p: Uint8Array): Generator<Uint8Array> {
    let c = 0;
    while (p.length > c) {
        const r = p.slice(c);
        const i = r.indexOf(SLASH);
        if (i === -1) { c += r.length; yield r; continue; }
        c += i + 1; yield r.slice(0, i);
    }
    if (p.length === 0 || p[p.length - 1] === SLASH) yield new Uint8Array();
}

function encodeEncComp(enc: Uint8Array): Uint8Array {
    if (enc.length === 0) return new Uint8Array([0x01]);
    let r = new Uint8Array([0x02]);
    for (let i = 0; i < enc.length; i++) {
        let t: Uint8Array;
        const b = enc[i];
        if (b === 0x2e || b === 0x2f || b === 0xfe || b === 0xff || b === 0x00 || b === 0x01) {
            t = new Uint8Array(r.length + 2); t.set(r);
            if (b === 0x2e) t.set([0x2e, 1], r.length);
            else if (b === 0x2f) t.set([0x2e, 2], r.length);
            else if (b === 0xfe) t.set([0xfe, 1], r.length);
            else if (b === 0xff) t.set([0xfe, 2], r.length);
            else if (b === 0x00) t.set([0x01, 1], r.length);
            else t.set([0x01, 2], r.length);
        } else {
            t = new Uint8Array(r.length + 1); t.set(r);
            t.set([b], r.length);
        }
        r = t;
    }
    return r;
}

interface EK { encrAlg: number; encrBlockSize: number; raw: Uint8Array; path: Uint8Array; content: boolean; }

function ekDeriveKey(ek: EK, content: Uint8Array): EK {
    const h = hmacSha512(ek.raw, content);
    return { ...ek, raw: h.slice(0, 32), path: new Uint8Array(ek.path), content: false };
}

function ekDerivePathComp(ek: EK, comp: Uint8Array): EK {
    const nonce = new Uint8Array(24);
    const enc = aesGcmEncrypt(comp, ek.raw, nonce);
    const ecomp = encodeEncComp(enc);
    const newPath = ek.path.length === 0 ? ecomp : new Uint8Array([...ek.path, SLASH, ...ecomp]);
    const prefix = new TextEncoder().encode("p:");
    const nk = ekDeriveKey(ek, new Uint8Array([...prefix, ...comp]));
    nk.path = newPath;
    return nk;
}

function ekDerivePath(ek: EK, p: Uint8Array): EK {
    let k: EK = { ...ek, path: new Uint8Array(ek.path) };
    for (const comp of pathIter(p)) k = ekDerivePathComp(k, comp);
    return k;
}

async function deriveEKey(password: string, salt: string, bucketPath: string): Promise<EK> {
    const { default: argon2 } = await import("argon2-browser");
    const pw = new TextEncoder().encode(password);
    const sl = new TextEncoder().encode(salt);
    const mixed = hmacSha256(pw, sl);
    const pSalt = hmacSha256(mixed, new TextEncoder().encode(""));

    const result = await argon2.hash({
        pass: password, salt: pSalt, type: 1,
        time: 1, mem: 64 * 1024, parallelism: 1, hashLen: 32,
    });

    const base: EK = { encrAlg: 1, encrBlockSize: 128016, raw: result.hash, path: new Uint8Array(), content: false };
    return bucketPath ? ekDerivePath(base, new TextEncoder().encode(bucketPath)) : base;
}

// ─── Core: generate grant from config ───────────────────────────────────────

async function generateGrant(config: Config): Promise<{ grant: string; zkey: string; info: string[] }> {
    const info: string[] = [];

    // Decode ZKey
    const zkProto = b64urlDecode(config.rootZKey);
    let off = 0;
    const tag = zkProto[off++];
    if ((tag >>> 3) !== 1 || (tag & 0x7) !== 2) throw new Error("Invalid ZKeyProto");
    const [len, no] = readUvarint(zkProto, off); off = no;
    const mcrBin = zkProto.slice(off, off + len);
    const mcr = importMacaroonV2(mcrBin);

    // Time caveat
    const from = new Date();
    const to = config.duration ? new Date(Date.now() + config.duration) : null;
    const tc = encodeTimeCaveat(from, to);
    const tm = new Uint8Array(tc.length + 1); tm[0] = 2; tm.set(tc, 1);
    addCaveat(mcr, b64Encode(tm));
    info.push(`Duration: ${from.toISOString()} -> ${to?.toISOString() || "no expiry"}`);

    // EKeys
    const eKeysMap = new Map<string, EKeyData[]>();

    if (config.mode === "per-bucket") {
        // Op caveat
        const scopes = config.buckets.map(b => ({
            paths: [{ bucket: b.name, prefix: new TextEncoder().encode(b.prefix ?? "") }],
            ops: b.permissions.map(Number),
        }));
        const oc = encodeOpCaveat(scopes);
        const om = new Uint8Array(oc.length + 1); om[0] = 1; om.set(oc, 1);
        addCaveat(mcr, b64Encode(om));

        for (const b of config.buckets) {
            const ek = await deriveEKey(b.passphrase, config.accountId, b.name);
            eKeysMap.set(b.name, [ek]);
            info.push(`Bucket: ${b.name} [permissions: ${b.permissions.join(",")}]`);
        }
    } else {
        const ek = await deriveEKey(config.passphrase, config.accountId, "");
        eKeysMap.set("*", [ek]);
        info.push("Bucket: * (all buckets)");
    }

    const mcrOut = exportMacaroonV2(mcr);
    return {
        grant: b64urlEncode(encodeGrantProto(config.url, mcrOut, eKeysMap)),
        zkey: b64urlEncode(encodeZKeyProto(mcrOut)),
        info,
    };
}

// ─── Main ───────────────────────────────────────────────────────────────────

async function main() {
    const args = parseArgs(process.argv);

    if (hasFlag(args, "help") || process.argv.length <= 2) {
        printUsage();
        process.exit(0);
    }

    // Fix argon2-browser WASM
    const wasmPath = path.join(__dirname, "node_modules", "argon2-browser", "dist", "argon2.wasm");
    if (fs.existsSync(wasmPath)) {
        const wasmBuf = fs.readFileSync(wasmPath);
        const origFetch = globalThis.fetch;
        (globalThis as any).fetch = (input: any, init: any) => {
            if (typeof input === "string" && input.includes("argon2.wasm"))
                return Promise.resolve(new Response(new Uint8Array(wasmBuf), { status: 200, headers: { "Content-Type": "application/wasm" } }));
            return origFetch(input, init);
        };
    }

    // Build config
    let config: Config;
    const configPath = getArg(args, "config");
    if (configPath) {
        if (!fs.existsSync(configPath)) { console.error(`Config not found: ${configPath}`); process.exit(1); }
        config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
    } else {
        config = buildConfigFromArgs(args);
    }

    if (!config.rootZKey || !config.accountId || !config.url) {
        console.error("Missing required: rootZKey/--zkey, accountId/--account, url/--url");
        process.exit(1);
    }

    const quiet = hasFlag(args, "quiet");
    const jsonOutput = getArg(args, "output") === "json";

    if (!quiet) {
        console.error(`Mode: ${config.mode} | Account: ${config.accountId} | URL: ${config.url}`);
    }

    const result = await generateGrant(config);

    if (!quiet) {
        result.info.forEach(l => console.error(`  ${l}`));
    }

    if (jsonOutput) {
        console.log(JSON.stringify({ grant: result.grant, zkey: result.zkey }));
    } else {
        if (!quiet) {
            console.log("\n" + "=".repeat(60));
            console.log("GRANT:");
            console.log("=".repeat(60));
        }
        console.log(result.grant);
        if (!quiet) {
            console.log("=".repeat(60));
            console.log("\nZKEY:");
            console.log("=".repeat(60));
        } else {
            console.log(result.zkey);
        }
        if (!quiet) {
            console.log(result.zkey);
            console.log("=".repeat(60));
            console.log(`\nGrant: ${result.grant.length} chars | ZKey: ${result.zkey.length} chars`);
        }
    }
}

main().catch(err => { console.error("Error:", err.message || err); process.exit(1); });