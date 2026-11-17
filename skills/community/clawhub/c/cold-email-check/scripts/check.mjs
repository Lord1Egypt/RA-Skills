#!/usr/bin/env node
// cold-email-check: ask Precleared whether a cold email to an address is allowed.
// Node 18 or later, no dependencies. Run with --help for every option.
//
// One address:
//   node check.mjs --email jane@acme.co.uk --sender GB --source SOURCE [--pitch "..."]
// A list (CSV with a header row, JSON Lines or a JSON array):
//   node check.mjs --file leads.csv --sender GB --source SOURCE --out leads-checked.csv
// SOURCE is where the addresses came from: published, bought, scraped, given or unknown.
//
// Sends each address and the facts given for it to precleared.dev, with PRECLEARED_API_KEY
// if that is set. Nothing else leaves the machine, and nothing is sent to the recipient.

import { createHash } from "node:crypto";
import { accessSync, constants, existsSync, readFileSync, realpathSync, writeFileSync } from "node:fs";
import { dirname, extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const VERSION = "1.0.2";
// Where this copy of the skill was published. It goes in the user agent so Precleared can
// count the checks that come from each listing. Nothing about the user is added.
const CHANNEL = "clawhub";
const DEFAULT_API_URL = "https://precleared.dev/api/v1/check";
const SOURCES = ["published", "bought", "scraped", "given", "unknown"];
const SENDERS = ["GB", "US", "AE"];
const VERDICTS = ["ok_to_email", "consent_needed", "blocked", "unknown"];
const STOP_ERRORS = new Set(["daily_limit", "payment_required", "invalid_key", "revoked_key"]);
const ROW_ERRORS = new Set(["invalid_row", "invalid_request"]);
const KEY_RE = /^pc_live_[A-Za-z0-9]{32}$/;
const EMAIL_RE = /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[^\s@<>()",;:]+$/;
const DOMAIN_RE = /^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{0,61}[a-z0-9]$/;
const MAX_REQUEST_MS = 25000;
const MIN_REQUEST_MS = 3000;
const RETRY_WAIT_MS = 2000;
const SAVE_EVERY_MS = 5000;
const MAX_PITCH = 2000;
const BOM = String.fromCharCode(0xfeff);
const OUT_EXTENSIONS = [".csv", ".jsonl", ".ndjson"];

export const EXIT = { OK: 0, USAGE: 1, DO_NOT_SEND: 2, NOT_CHECKED: 3, TIME_LIMIT: 4 };

const USAGE = `cold-email-check ${VERSION}: is a cold email to this address allowed? (Precleared)

One address:
  node check.mjs --email jane@acme.co.uk --sender GB --source SOURCE --pitch "what you offer"
  node check.mjs --domain acme.co.uk --sender GB --source SOURCE

A list (CSV with a header row, .jsonl or a .json array):
  node check.mjs --file leads.csv --sender GB --source SOURCE --out leads-checked.csv

SOURCE is where the addresses came from: published, bought, scraped, given or unknown.
Take it from the user. Never guess it.

Facts (the verdict depends on them, so never guess to get a better answer):
  --email ADDRESS          recipient's email address (one address per check)
  --domain DOMAIN          recipient's domain, when there is no address yet
  --sender GB|US|AE        where the sending business is based (or set PRECLEARED_SENDER_COUNTRY)
  --source SOURCE          published, bought, scraped, given or unknown
  --pitch TEXT             what the email offers, in a few words
  --country COUNTRY        recipient's country (two-letter code or English name), if known
  --company-number N       UK company number, if known
  --pitch-relevant         the offer relates to the recipient's job or business
  --pitch-not-relevant     the offer does not relate to it
  --existing-customer      the recipient has bought from the sender before
  --suppressed             the address is on the sender's do-not-contact list

Lists:
  --file PATH              rows need an email (or domain) column. Optional columns override the
                           flags for their row: source, country, pitch, company_number,
                           pitch_relevant, existing_customer, and an opt-out column such as
                           suppressed, do_not_email, unsubscribed or email_opt_out
  --out PATH               write the results to PATH (.csv keeps the original columns and adds
                           precleared_* columns; .jsonl writes one JSON object per row).
                           Running the same command again keeps the answers already in PATH and
                           checks only the rest. Use a new PATH to check everything again
  --time-limit SECONDS     stop starting new checks after this long (default 90, 0 for none)
  --delay-ms MS            pause between checks (default 200)

Other:
  --dry-run                show what would be sent, without sending it
  --help                   show this help

Exit codes:
  0  one address: ok_to_email. A list: every row has a verdict. That does not mean every row
     can be emailed: send only where precleared_send is yes (send is true in JSON)
  2  one address: do not send (consent_needed, blocked or unknown)
  3  an address could not be checked (missing or unreadable facts in a list row, daily limit,
     no credits, bad key, network): do not send to it yet
  4  a list stopped at the time limit or was interrupted: run the same command again
  1  usage error, or no row of the list could be checked. Read the message

Environment:
  PRECLEARED_API_KEY         optional. Free key at https://precleared.dev/get-key
  PRECLEARED_SENDER_COUNTRY  optional default for --sender
`;

const FLAGS = {
  "--email": "email",
  "--domain": "domain",
  "--sender": "sender",
  "--source": "source",
  "--pitch": "pitch",
  "--country": "country",
  "--company-number": "companyNumber",
  "--file": "file",
  "--out": "out",
  "--time-limit": "timeLimit",
  "--delay-ms": "delayMs",
};

const SWITCHES = {
  "--pitch-relevant": ["pitchRelevant", true],
  "--pitch-not-relevant": ["pitchRelevant", false],
  "--existing-customer": ["existingCustomer", true],
  "--suppressed": ["suppressed", true],
  "--dry-run": ["dryRun", true],
  "--help": ["help", true],
  "-h": ["help", true],
};

const isOption = (s) => {
  const name = s.includes("=") ? s.slice(0, s.indexOf("=")) : s;
  return Object.hasOwn(FLAGS, name) || Object.hasOwn(SWITCHES, name);
};

export function parseArgs(argv) {
  const opts = {};
  for (let i = 0; i < argv.length; i++) {
    let arg = argv[i];
    let inline;
    const eq = arg.indexOf("=");
    if (arg.startsWith("--") && eq > 2) {
      inline = arg.slice(eq + 1);
      arg = arg.slice(0, eq);
    }
    if (Object.hasOwn(SWITCHES, arg)) {
      if (inline !== undefined) throw new Error(`${arg} does not take a value`);
      const [key, value] = SWITCHES[arg];
      if (key === "pitchRelevant" && opts.pitchRelevant !== undefined && opts.pitchRelevant !== value) {
        throw new Error("Use --pitch-relevant or --pitch-not-relevant, not both");
      }
      opts[key] = value;
      continue;
    }
    if (Object.hasOwn(FLAGS, arg)) {
      let value = inline;
      if (value === undefined) {
        value = argv[++i];
        if (value === undefined || isOption(value)) throw new Error(`Missing value for ${arg}`);
      }
      opts[FLAGS[arg]] = value;
      continue;
    }
    throw new Error(`Unknown option: ${arg}. Run with --help to see the options.`);
  }
  return opts;
}

const isObject = (value) => Boolean(value) && typeof value === "object" && !Array.isArray(value);
const text = (value) => (typeof value === "string" && value.trim() ? value.trim() : null);
const num = (value) => (typeof value === "number" && Number.isFinite(value) ? value : null);
const clean = (value) => (value === undefined || value === null ? "" : String(value).trim());
const sleep = (ms) => new Promise((done) => setTimeout(done, ms));

export function normaliseEmail(value) {
  let s = clean(value);
  const angle = /<([^<>\s]+@[^<>\s]+)>/.exec(s);
  if (angle) s = angle[1];
  s = s.replace(/^mailto:/i, "");
  const query = s.indexOf("?");
  if (query >= 0) s = s.slice(0, query);
  return s.toLowerCase();
}

export function normaliseDomain(value) {
  let s = clean(value).toLowerCase();
  if (!s) return "";
  if (s.includes("@") && !s.includes("/")) s = s.slice(s.lastIndexOf("@") + 1);
  s = s.replace(/^[a-z][a-z0-9+.-]*:\/\//, "");
  s = s.split(/[/?#]/)[0];
  s = s.replace(/:\d+$/, "").replace(/\.$/, "").replace(/^www\./, "");
  return s;
}

// ---------- countries ----------

const ISO_CODES = (
  "AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW " +
  "BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ " +
  "FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ " +
  "IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH " +
  "MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL " +
  "PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD " +
  "TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW"
).split(" ");
const ISO = new Set(ISO_CODES);

const COUNTRY_ALIASES = {
  UK: "GB",
  "GREAT BRITAIN": "GB",
  BRITAIN: "GB",
  ENGLAND: "GB",
  SCOTLAND: "GB",
  WALES: "GB",
  "NORTHERN IRELAND": "GB",
  USA: "US",
  AMERICA: "US",
  "UNITED STATES OF AMERICA": "US",
  DEUTSCHLAND: "DE",
  "CZECH REPUBLIC": "CZ",
  HOLLAND: "NL",
  TURKEY: "TR",
  "SOUTH KOREA": "KR",
  UAE: "AE",
  "IVORY COAST": "CI",
};

export const countryKey = (value) =>
  clean(value)
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toUpperCase()
    .replace(/\./g, "")
    .replace(/&/g, " AND ")
    .replace(/[^A-Z0-9]+/g, " ")
    .trim()
    .replace(/^THE /, "");

let countryNames = null;
function namesToCodes() {
  if (countryNames) return countryNames;
  countryNames = new Map(Object.entries(COUNTRY_ALIASES));
  try {
    const names = new Intl.DisplayNames(["en"], { type: "region", fallback: "none" });
    for (const code of ISO_CODES) {
      const name = names.of(code);
      const key = name ? countryKey(name) : "";
      if (key && !countryNames.has(key)) countryNames.set(key, code);
    }
  } catch {
    // Without full ICU only the aliases and two-letter codes are read.
  }
  return countryNames;
}

// Returns a two-letter code, "" when there is no value, or null when the value can't be read.
export function countryCode(value) {
  const key = countryKey(value);
  if (!key) return "";
  if (/^[A-Z]{2}$/.test(key)) {
    if (key === "UK") return "GB";
    return ISO.has(key) ? key : null;
  }
  return namesToCodes().get(key) ?? null;
}

export function parseBool(value) {
  if (typeof value === "boolean") return value;
  const s = clean(value).toLowerCase();
  if (!s) return undefined;
  if (["true", "yes", "y", "1"].includes(s)) return true;
  if (["false", "no", "n", "0"].includes(s)) return false;
  throw new Error(`"${value}" is not a yes or no value`);
}

// Turns one set of facts into the request body. Throws with a plain message when a fact is
// missing or unreadable, so an address is never checked with facts it was not given.
export function buildPayload(facts) {
  const payload = {};
  const rawEmail = clean(facts.email);
  if ((rawEmail.match(/@/g) || []).length > 1) {
    throw new Error("More than one address in one value. Check one address at a time (one per row in a list).");
  }
  const email = normaliseEmail(rawEmail);
  const domain = normaliseDomain(facts.domain);
  if (email) {
    if (!EMAIL_RE.test(email)) throw new Error(`"${email}" is not an email address`);
    payload.recipient_email = email;
  } else if (domain) {
    if (!DOMAIN_RE.test(domain)) throw new Error(`"${domain}" is not a domain`);
    payload.recipient_domain = domain;
  } else {
    throw new Error("No email address or domain");
  }
  const sender = clean(facts.sender).toUpperCase();
  if (!sender) {
    throw new Error("No sender country. Ask the user where the sending business is based, then pass --sender GB, US or AE.");
  }
  if (!SENDERS.includes(sender)) {
    throw new Error(`Sender country "${facts.sender}" is not covered: Precleared checks email from businesses based in GB, US or AE.`);
  }
  payload.sender_country = sender;
  const source = clean(facts.source).toLowerCase();
  if (!source) {
    throw new Error(
      "Where the address came from is missing. Ask the user, then pass --source published, bought, scraped, given or unknown (unknown if they can't say).",
    );
  }
  if (!SOURCES.includes(source)) {
    throw new Error(`Address source "${facts.source}" is not one of ${SOURCES.join(", ")}. Ask the user where the address came from.`);
  }
  payload.address_source = source;
  const pitch = clean(facts.pitch);
  if (pitch.length > MAX_PITCH) throw new Error("The pitch is longer than 2,000 characters. Describe the offer in a few words.");
  if (pitch) payload.pitch = pitch;
  const country = countryCode(facts.country);
  if (country === null) {
    throw new Error(`Recipient country "${facts.country}" is not a country this script recognises. Use its two-letter code, such as ES.`);
  }
  if (country) payload.recipient_country = country;
  const companyNumber = clean(facts.companyNumber).toUpperCase().replace(/\s+/g, "");
  if (companyNumber) {
    if (companyNumber.length > 12) throw new Error(`Company number "${facts.companyNumber}" is too long`);
    payload.company_number = companyNumber;
  }
  for (const [key, field] of [
    ["pitchRelevant", "pitch_relevant"],
    ["existingCustomer", "existing_customer"],
    ["suppressed", "suppressed"],
  ]) {
    const value = parseBool(facts[key]);
    if (value !== undefined) payload[field] = value;
  }
  return payload;
}

// A short fingerprint of the facts sent, so a later run only reuses an answer to the same question.
export const factsHash = (payload) => createHash("sha256").update(JSON.stringify(payload)).digest("hex").slice(0, 16);

export function resolveApiUrl(env = process.env) {
  const raw = clean(env.PRECLEARED_API_URL);
  if (!raw) return DEFAULT_API_URL;
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new Error("PRECLEARED_API_URL is not a valid URL");
  }
  const local = url.protocol === "http:" && ["127.0.0.1", "localhost", "[::1]"].includes(url.hostname);
  const ours = url.protocol === "https:" && (url.hostname === "precleared.dev" || url.hostname.endsWith(".precleared.dev"));
  if (!local && !ours) throw new Error("PRECLEARED_API_URL may only point at precleared.dev or a local test server");
  return url.href;
}

export function resolveKey(env = process.env) {
  const key = clean(env.PRECLEARED_API_KEY);
  if (!key) return null;
  if (!KEY_RE.test(key)) {
    throw new Error(
      "PRECLEARED_API_KEY is set but is not a Precleared key (pc_live_ followed by 32 letters and digits). Fix it, or unset it to use the keyless allowance.",
    );
  }
  return key;
}

// Reads one API response. Only a JSON object with a known verdict counts as an answer:
// anything else means the check could not be made, so it is never read as a verdict.
export function summarise(status, body, origin) {
  if (status === 200 && isObject(body) && VERDICTS.includes(body.verdict)) {
    const reasons = Array.isArray(body.reasons) ? body.reasons.filter(isObject) : [];
    const ruled = reasons.find((r) => text(r.text)) || {};
    const notes = reasons.map((r) => text(r.note)).filter(Boolean);
    const receiptId = isObject(body.receipt) ? text(body.receipt.id) : null;
    const usage = isObject(body.usage) ? body.usage : null;
    return {
      verdict: body.verdict,
      send: body.verdict === "ok_to_email",
      confidence: text(body.confidence),
      rule: text(ruled.text) || notes[0] || null,
      rule_source: text(ruled.source_title),
      rule_source_url: text(ruled.source_url),
      notes: notes.length ? notes : undefined,
      footer_text: text(body.footer_text),
      next_step: text(body.next_step),
      receipt_id: receiptId,
      receipt_url: receiptId ? `${origin}/r/${receiptId}` : null,
      checked_at: (isObject(body.receipt) && text(body.receipt.created_at)) || new Date().toISOString(),
      usage: usage
        ? { free_remaining_today: num(usage.free_remaining_today), credits_remaining: num(usage.credits_remaining) }
        : undefined,
    };
  }
  const error = isObject(body) ? body : {};
  return {
    verdict: null,
    send: false,
    error: text(error.error) || (status === 0 ? "unreachable" : status === 200 ? "unexpected_response" : `http_${status}`),
    message: text(error.message) || "Precleared could not answer. Do not send to this address yet.",
    get_key_url: text(error.get_key_url) || undefined,
    buy_url: text(error.buy_url) || undefined,
  };
}

export async function callApi(url, payload, { key = null, timeoutMs = MAX_REQUEST_MS } = {}) {
  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
    "User-Agent": `precleared-skill/${VERSION} (cold-email-check; ${CHANNEL})`,
  };
  if (key) headers.Authorization = `Bearer ${key}`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
      redirect: "error",
      signal: AbortSignal.timeout(timeoutMs),
    });
    const raw = await res.text();
    let body = null;
    try {
      body = raw ? JSON.parse(raw) : null;
    } catch {
      body = null;
    }
    return { status: res.status, body };
  } catch (err) {
    const timedOut = err && (err.name === "TimeoutError" || err.name === "AbortError");
    return {
      status: 0,
      body: {
        error: timedOut ? "timeout" : "unreachable",
        message: timedOut ? "Precleared did not answer in time." : `Precleared could not be reached (${err.message}).`,
      },
    };
  }
}

const transient = (status, body) =>
  status === 0 || status >= 500 || (status === 429 && !(isObject(body) && body.error === "daily_limit"));

// ---------- reading and writing lists ----------

export function decodeText(buffer) {
  const bom = buffer.length >= 3 && buffer[0] === 0xef && buffer[1] === 0xbb && buffer[2] === 0xbf;
  try {
    return { text: new TextDecoder("utf-8", { fatal: true }).decode(buffer), bom, encoding: "utf-8" };
  } catch {
    // Not UTF-8: most likely a spreadsheet saved as Windows-1252. The results are written as
    // UTF-8 with a byte order mark, which spreadsheet apps read correctly.
    let decoded;
    try {
      decoded = new TextDecoder("windows-1252").decode(buffer);
    } catch {
      decoded = buffer.toString("latin1");
    }
    return { text: decoded, bom: true, encoding: "windows-1252" };
  }
}

function detectDelimiter(source) {
  const counts = { ",": 0, ";": 0, "\t": 0 };
  let inQuotes = false;
  for (const c of source) {
    if (c === '"') inQuotes = !inQuotes;
    else if (!inQuotes && (c === "\n" || c === "\r")) break;
    else if (!inQuotes && c in counts) counts[c]++;
  }
  let best = ",";
  for (const d of [";", "\t"]) if (counts[d] > counts[best]) best = d;
  return best;
}

export function parseCsv(input) {
  let source = input.startsWith(BOM) ? input.slice(1) : input;
  let delimiter;
  let sepLine = null;
  const sep = /^sep=(.)[ \t]*(\r\n|\n|\r)/i.exec(source);
  if (sep) {
    delimiter = sep[1];
    sepLine = sep[0].replace(/[\r\n]+$/, "");
    source = source.slice(sep[0].length);
  } else {
    delimiter = detectDelimiter(source);
  }
  const rows = [];
  let row = [];
  let field = "";
  let inQuotes = false;
  let quoted = false;
  for (let i = 0; i < source.length; i++) {
    const c = source[i];
    if (inQuotes) {
      if (c === '"') {
        if (source[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
      continue;
    }
    if (c === '"' && !quoted && field.trim() === "") {
      inQuotes = true;
      quoted = true;
      field = "";
    } else if (c === delimiter) {
      row.push(field);
      field = "";
      quoted = false;
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && source[i + 1] === "\n") i++;
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
      quoted = false;
    } else {
      field += c;
    }
  }
  if (inQuotes) throw new Error("The CSV has a quote that is never closed");
  if (field !== "" || row.length) {
    row.push(field);
    rows.push(row);
  }
  return {
    rows: rows.filter((r) => r.some((cell) => cell.trim() !== "")),
    delimiter,
    sepLine,
    eol: /\r\n/.test(source) ? "\r\n" : "\n",
  };
}

const COLUMN_ALIASES = {
  email: ["email", "recipient_email", "email_address", "e_mail", "e_mail_address", "work_email", "business_email", "mail"],
  domain: ["domain", "recipient_domain", "company_domain", "website", "company_website", "web_site", "url"],
  source: ["source", "address_source"],
  country: ["country", "recipient_country", "country_code"],
  pitch: ["pitch", "offer"],
  companyNumber: ["company_number", "companies_house_number", "company_no", "crn", "registration_number"],
  pitchRelevant: ["pitch_relevant", "relevant"],
  existingCustomer: ["existing_customer", "is_customer", "customer"],
  suppressed: [
    "suppressed",
    "do_not_contact",
    "do_not_email",
    "dnc",
    "unsubscribed",
    "unsubscribe",
    "email_unsubscribed",
    "unsubscribed_from_all_email",
    "opted_out",
    "opt_out",
    "optout",
    "email_opt_out",
    "hasoptedoutofemail",
  ],
};

export const headerKey = (name) =>
  clean(name)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");

// Maps each fact to the columns that can hold it, in alias order.
export function mapColumns(columns) {
  const keys = columns.map(headerKey);
  const map = {};
  for (const [fact, aliases] of Object.entries(COLUMN_ALIASES)) {
    const found = [];
    for (const alias of aliases) {
      keys.forEach((k, index) => {
        if (k === alias && !found.includes(index)) found.push(index);
      });
    }
    if (found.length) map[fact] = found;
  }
  return map;
}

export function rowFacts(values, map) {
  const facts = {};
  for (const [fact, indexes] of Object.entries(map)) {
    for (const index of indexes) {
      const value = clean(values[index]);
      if (value) {
        facts[fact] = value;
        break;
      }
    }
  }
  return facts;
}

function objectRows(list, label) {
  if (!list.every(isObject)) throw new Error(`${label} must hold one object per lead`);
  const columns = [];
  for (const item of list) for (const k of Object.keys(item)) if (!columns.includes(k)) columns.push(k);
  const values = list.map((item) => columns.map((c) => (item[c] === undefined || item[c] === null ? "" : String(item[c]))));
  return { columns, values };
}

export function readList(path) {
  if (!existsSync(path)) throw new Error(`No file at ${path}`);
  const { text: raw, bom, encoding } = decodeText(readFileSync(path));
  const ext = extname(path).toLowerCase();
  const head = raw.trimStart();
  let table;
  let csv = null;
  if (ext === ".json" || (ext !== ".csv" && ext !== ".jsonl" && ext !== ".ndjson" && head.startsWith("["))) {
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch (err) {
      throw new Error(`${path} is not valid JSON: ${err.message}`);
    }
    if (!Array.isArray(parsed)) throw new Error(`${path} must hold a JSON array of leads`);
    table = objectRows(parsed, path);
  } else if (ext === ".jsonl" || ext === ".ndjson" || (ext !== ".csv" && head.startsWith("{"))) {
    const items = [];
    raw.split(/\r?\n/).forEach((line, i) => {
      if (!line.trim()) return;
      try {
        items.push(JSON.parse(line));
      } catch (err) {
        throw new Error(`Line ${i + 1} of ${path} is not valid JSON: ${err.message}`);
      }
    });
    table = objectRows(items, path);
  } else {
    csv = parseCsv(raw);
    csv.bom = bom || encoding !== "utf-8";
    if (!csv.rows.length) throw new Error(`${path} is empty`);
    const [columns, ...values] = csv.rows;
    const width = Math.max(columns.length, ...values.map((v) => v.length));
    table = { columns: [...columns.map((c) => c.trim()), ...new Array(width - columns.length).fill("")], values };
  }
  if (!table.values.length) throw new Error(`${path} has no leads in it`);
  const map = mapColumns(table.columns);
  if (!map.email && !map.domain) {
    throw new Error(`${path} needs an email or domain column. Columns found: ${table.columns.filter(Boolean).join(", ") || "none"}`);
  }
  return { ...table, map, csv, encoding };
}

const OUT_COLUMNS = [
  ["precleared_verdict", (r) => r.verdict],
  ["precleared_send", (r) => (r.verdict ? (r.send ? "yes" : "no") : "")],
  ["precleared_rule", (r) => r.rule],
  ["precleared_footer_text", (r) => r.footer_text],
  ["precleared_next_step", (r) => r.next_step],
  ["precleared_receipt_id", (r) => r.receipt_id],
  ["precleared_receipt_url", (r) => r.receipt_url],
  ["precleared_checked_at", (r) => (r.verdict ? r.checked_at : "")],
  ["precleared_error", (r) => (r.verdict ? "" : r.error ? `${r.error}: ${r.message ?? ""}`.trim() : "")],
  ["precleared_facts_hash", (r) => (r.verdict ? r.facts_hash : "")],
];

function csvCell(value, delimiter) {
  const s = value === null || value === undefined ? "" : String(value);
  return s.includes('"') || s.includes("\n") || s.includes("\r") || s.includes(delimiter) ? `"${s.replace(/"/g, '""')}"` : s;
}

export function writeResults(path, list, results) {
  if (extname(path).toLowerCase() === ".csv") {
    const delimiter = list.csv?.delimiter ?? ",";
    const eol = list.csv?.eol ?? "\n";
    const keep = list.columns.map((name, index) => [name, index]).filter(([name]) => !name.startsWith("precleared_"));
    const header = [...keep.map(([name]) => name), ...OUT_COLUMNS.map(([name]) => name)];
    const lines = [];
    if (list.csv?.sepLine) lines.push(list.csv.sepLine);
    lines.push(header.map((c) => csvCell(c, delimiter)).join(delimiter));
    list.values.forEach((values, i) => {
      const r = results[i] ?? {};
      const cells = [...keep.map(([, index]) => values[index] ?? ""), ...OUT_COLUMNS.map(([, get]) => get(r))];
      lines.push(cells.map((c) => csvCell(c, delimiter)).join(delimiter));
    });
    writeFileSync(path, (list.csv?.bom ? BOM : "") + lines.join(eol) + eol, "utf8");
  } else {
    const rows = list.values.map(
      (_, i) => results[i] ?? { row: i + 1, verdict: null, send: false, error: "not_checked", message: "Not checked yet." },
    );
    writeFileSync(path, rows.map((r) => JSON.stringify(r)).join("\n") + "\n", "utf8");
  }
}

const NOT_OURS = (path) => `${path} already exists and is not a results file from this script. Choose another --out name.`;

// Answers saved by an earlier run, keyed by the fingerprint of the facts they answered, so rows can
// move around and a list longer than one day's allowance can be finished over several days.
export function readEarlier(path) {
  const earlier = new Map();
  if (!path || !existsSync(path)) return earlier;
  const { text: raw } = decodeText(readFileSync(path));
  if (!raw.trim()) return earlier;
  const keepAnswer = (hash, answer) => {
    if (VERDICTS.includes(answer.verdict) && hash && !earlier.has(hash)) {
      earlier.set(hash, { ...answer, send: answer.verdict === "ok_to_email", facts_hash: hash });
    }
  };
  if (extname(path).toLowerCase() === ".csv") {
    let rows;
    try {
      ({ rows } = parseCsv(raw));
    } catch {
      throw new Error(NOT_OURS(path));
    }
    const [header = [], ...body] = rows;
    const index = Object.fromEntries(header.map((h, i) => [h.trim(), i]));
    if (index.precleared_verdict === undefined || index.precleared_facts_hash === undefined) throw new Error(NOT_OURS(path));
    const cell = (cells, name) => (index[name] === undefined ? null : clean(cells[index[name]]) || null);
    for (const cells of body) {
      keepAnswer(cell(cells, "precleared_facts_hash"), {
        verdict: cell(cells, "precleared_verdict"),
        rule: cell(cells, "precleared_rule"),
        footer_text: cell(cells, "precleared_footer_text"),
        next_step: cell(cells, "precleared_next_step"),
        receipt_id: cell(cells, "precleared_receipt_id"),
        receipt_url: cell(cells, "precleared_receipt_url"),
        checked_at: cell(cells, "precleared_checked_at"),
      });
    }
    return earlier;
  }
  const parsed = raw
    .split(/\r?\n/)
    .filter((line) => line.trim())
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    });
  if (!parsed.every((r) => isObject(r) && Number.isInteger(r.row) && r.row > 0)) throw new Error(NOT_OURS(path));
  for (const r of parsed) {
    const { row, email, domain, duplicate_of_row, from_earlier_run, warnings, facts_hash, ...answer } = r;
    if (typeof facts_hash === "string") keepAnswer(facts_hash, answer);
  }
  return earlier;
}

function checkWritable(path) {
  try {
    accessSync(dirname(resolve(path)), constants.W_OK);
    if (existsSync(path)) accessSync(path, constants.W_OK);
  } catch (err) {
    throw new Error(`Can't write to ${path}: ${err.code === "ENOENT" ? "that folder doesn't exist" : err.message}`);
  }
}

// ---------- running ----------

function parseNumber(value, name, fallback) {
  if (value === undefined) return fallback;
  const n = Number(value);
  if (clean(value) === "" || !Number.isFinite(n) || n < 0) throw new Error(`${name} must be a number of 0 or more`);
  return n;
}

async function runOne(opts, env, out) {
  if (opts.email && opts.domain) throw new Error("Give --email or --domain, not both");
  if (opts.timeLimit !== undefined || opts.delayMs !== undefined) throw new Error("--time-limit and --delay-ms only work with --file");
  const sender = opts.sender ?? env.PRECLEARED_SENDER_COUNTRY;
  const payload = buildPayload({ ...opts, sender });
  const url = resolveApiUrl(env);
  const key = resolveKey(env);
  if (opts.dryRun) {
    out.stdout(JSON.stringify({ dry_run: true, url, key: key ? "set" : "not set", payload }));
    return EXIT.OK;
  }
  let { status, body } = await callApi(url, payload, { key });
  if (transient(status, body)) {
    await sleep(RETRY_WAIT_MS);
    ({ status, body } = await callApi(url, payload, { key }));
  }
  const result = summarise(status, body, new URL(url).origin);
  out.stdout(JSON.stringify(result));
  if (!result.verdict) return EXIT.NOT_CHECKED;
  return result.send ? EXIT.OK : EXIT.DO_NOT_SEND;
}

async function runList(opts, env, out) {
  const timeLimitMs = parseNumber(opts.timeLimit, "--time-limit", 90) * 1000;
  const delayMs = parseNumber(opts.delayMs, "--delay-ms", 200);
  const url = resolveApiUrl(env);
  const key = resolveKey(env);
  const origin = new URL(url).origin;

  // Facts that apply to every row are checked before anything is read or sent.
  const sender = clean(opts.sender ?? env.PRECLEARED_SENDER_COUNTRY);
  if (!sender) throw new Error("No sender country. Ask the user where the sending business is based, then pass --sender GB, US or AE.");
  if (!SENDERS.includes(sender.toUpperCase())) {
    throw new Error(`Sender country "${sender}" is not covered: Precleared checks email from businesses based in GB, US or AE.`);
  }
  if (opts.source !== undefined && !SOURCES.includes(clean(opts.source).toLowerCase())) {
    throw new Error(`--source "${opts.source}" is not one of ${SOURCES.join(", ")}. Ask the user where the addresses came from.`);
  }
  if (opts.country !== undefined && !countryCode(opts.country)) {
    throw new Error(`--country "${opts.country}" is not a country this script recognises. Use its two-letter code, such as ES.`);
  }
  if (opts.pitch !== undefined && clean(opts.pitch).length > MAX_PITCH) {
    throw new Error("The pitch is longer than 2,000 characters. Describe the offer in a few words.");
  }
  if (opts.out) {
    if (!OUT_EXTENSIONS.includes(extname(opts.out).toLowerCase())) throw new Error("--out must end in .csv or .jsonl");
    if (resolve(opts.out) === resolve(opts.file)) throw new Error("--out must be a different file from --file");
  }

  const list = readList(opts.file);
  if (opts.source === undefined && !list.map.source) {
    throw new Error(
      "Where the addresses came from is missing. Ask the user, then pass --source published, bought, scraped, given or unknown, or add a source column.",
    );
  }
  const earlier = readEarlier(opts.out);
  const saving = Boolean(opts.out) && !opts.dryRun;
  if (saving) checkWritable(opts.out);

  const defaults = {
    sender,
    source: opts.source,
    pitch: opts.pitch,
    country: opts.country,
    companyNumber: opts.companyNumber,
    pitchRelevant: opts.pitchRelevant,
    existingCustomer: opts.existingCustomer,
    suppressed: opts.suppressed,
  };
  const columnsUsed = Object.fromEntries(Object.entries(list.map).map(([fact, idx]) => [fact, idx.map((i) => list.columns[i])]));

  const results = new Array(list.values.length);
  const answered = new Map(); // facts fingerprint -> row index of the first answer in this run
  const started = Date.now();
  let stopped = null;
  let timeUp = false;
  let interrupted = false;
  let saveError = null;
  let failuresInARow = 0;
  let lastCallMs = 0;
  let calls = 0;
  let planned = 0;
  let usage = null;
  let lastSave = 0;

  const save = (force = false) => {
    if (!saving || saveError) return;
    if (!force && Date.now() - lastSave < SAVE_EVERY_MS) return;
    try {
      writeResults(opts.out, list, results);
      lastSave = Date.now();
    } catch (err) {
      saveError = err.message;
    }
  };
  const emit = (i) => {
    if (!saving) out.stdout(JSON.stringify(results[i]));
  };

  const finish = () => {
    save(true);
    const count = (pred) => results.filter((r) => r && pred(r)).length;
    const reused = results.filter((r) => r && r.from_earlier_run);
    const oldest = reused.map((r) => r.checked_at).filter(Boolean).sort()[0];
    const summary = {
      rows: results.length,
      checked: count((r) => r.verdict),
      ok_to_email: count((r) => r.verdict === "ok_to_email"),
      consent_needed: count((r) => r.verdict === "consent_needed"),
      blocked: count((r) => r.verdict === "blocked"),
      unknown: count((r) => r.verdict === "unknown"),
      not_checked: results.length - count((r) => r.verdict || r.dry_run || ROW_ERRORS.has(r.error)),
      invalid_rows: count((r) => ROW_ERRORS.has(r.error)),
      repeated_rows: count((r) => r.duplicate_of_row),
      from_earlier_run: reused.length,
      checks_made: calls,
      columns: columnsUsed,
    };
    if (oldest) summary.oldest_reused_check = oldest;
    if (usage) Object.assign(summary, usage);
    if (saving) summary.out = opts.out;

    const parts = [];
    let exitCode = EXIT.OK;
    if (opts.dryRun) {
      summary.dry_run = true;
      parts.push(`Dry run: ${planned} checks would be made.`);
      if (reused.length) parts.push(`${reused.length} rows would keep answers already in ${opts.out}.`);
      parts.push("Nothing was sent.");
    } else {
      parts.push(
        `${summary.checked} of ${summary.rows} rows have a verdict: ${summary.ok_to_email} ok_to_email, ${summary.consent_needed} consent_needed, ${summary.blocked} blocked, ${summary.unknown} unknown.`,
      );
      if (summary.ok_to_email) parts.push("Send only to rows where precleared_send is yes (send is true in JSON).");
      if (reused.length) {
        parts.push(
          `${reused.length} answers were kept from an earlier run (oldest checked ${oldest ?? "at an unknown time"}). Write to a new --out file to check everything again.`,
        );
      }
    }
    if (saveError) {
      exitCode = EXIT.NOT_CHECKED;
      summary.stopped = "save_failed";
      summary.save_error = saveError;
      parts.push(`Could not save to ${opts.out} (${saveError}), so checking stopped and the results are printed above.`);
    } else if (stopped) {
      exitCode = EXIT.NOT_CHECKED;
      summary.stopped = stopped.error;
      parts.push(`Stopped: ${stopped.message} ${summary.not_checked} rows were not checked; do not email them yet.`);
      if (stopped.get_key_url) summary.get_key_url = stopped.get_key_url;
      if (stopped.buy_url) summary.buy_url = stopped.buy_url;
    } else if (summary.not_checked && (timeUp || interrupted)) {
      exitCode = EXIT.TIME_LIMIT;
      summary.stopped = interrupted ? "interrupted" : "time_limit";
      const why = interrupted ? "Interrupted" : "Time limit reached";
      parts.push(
        saving
          ? `${why} with ${summary.not_checked} rows left. Run the same command again to carry on.`
          : `${why} with ${summary.not_checked} rows left. Add --out FILE so the next run carries on from here.`,
      );
    } else if (summary.not_checked && !opts.dryRun) {
      exitCode = EXIT.NOT_CHECKED;
      summary.stopped = "errors";
      parts.push(`${summary.not_checked} rows could not be checked because of errors; do not email them yet. Try again later.`);
    }
    if (summary.invalid_rows) {
      const first = results.find((r) => r && ROW_ERRORS.has(r.error));
      parts.push(
        `${summary.invalid_rows} rows have missing or unreadable facts (row ${first.row}: ${first.message}). Fix them, or ask the user, and run again.`,
      );
      if (exitCode === EXIT.OK) exitCode = summary.invalid_rows === summary.rows ? EXIT.USAGE : EXIT.NOT_CHECKED;
      else if (summary.invalid_rows === summary.rows) exitCode = EXIT.USAGE;
    }
    summary.message = parts.join(" ");
    if (saveError) results.forEach((r) => out.stdout(JSON.stringify(r)));
    if (saving || saveError) out.stdout(JSON.stringify({ summary }));
    else out.stderr(JSON.stringify({ summary }));
    return exitCode;
  };

  const onSignal = () => {
    interrupted = true;
    for (let i = 0; i < results.length; i++) {
      if (!results[i]) {
        results[i] = { row: i + 1, verdict: null, send: false, error: "not_checked", message: "Not checked: the run was interrupted." };
        emit(i);
      }
    }
    process.exit(finish());
  };
  process.once("SIGINT", onSignal);
  process.once("SIGTERM", onSignal);

  // Settle every row that needs no check, and save once before spending any checks, so an
  // unwritable --out fails here rather than after the checks are made.
  const pending = [];
  const payloads = new Array(list.values.length);
  for (let i = 0; i < list.values.length; i++) {
    const facts = rowFacts(list.values[i], list.map);
    const base = { row: i + 1 };
    const email = normaliseEmail(facts.email);
    if (email) base.email = email;
    else if (facts.domain) base.domain = normaliseDomain(facts.domain);
    const merged = { ...defaults };
    for (const [k, v] of Object.entries(facts)) merged[k] = v;
    try {
      const payload = buildPayload(merged);
      const hash = factsHash(payload);
      payloads[i] = { base, payload, hash };
      if (earlier.has(hash)) results[i] = { ...base, ...earlier.get(hash), from_earlier_run: true };
      else pending.push(i);
    } catch (err) {
      results[i] = { ...base, verdict: null, send: false, error: "invalid_row", message: err.message };
    }
  }
  if (saving) {
    try {
      writeResults(opts.out, list, results);
      lastSave = Date.now();
    } catch (err) {
      throw new Error(`Can't write to ${opts.out}: ${err.message}`);
    }
  }
  const pendingSet = new Set(pending);

  for (let i = 0; i < list.values.length; i++) {
    if (!pendingSet.has(i)) {
      emit(i);
      continue;
    }
    const { base, payload, hash } = payloads[i];
    if (answered.has(hash)) {
      const { from_earlier_run, duplicate_of_row, ...answer } = results[answered.get(hash)];
      results[i] = { ...answer, ...base, duplicate_of_row: answered.get(hash) + 1 };
      emit(i);
      continue;
    }
    if (opts.dryRun) {
      results[i] = { ...base, dry_run: true, payload };
      answered.set(hash, i);
      planned++;
      emit(i);
      continue;
    }
    const elapsed = Date.now() - started;
    if (!stopped && !saveError && !timeUp && timeLimitMs > 0 && calls > 0 && elapsed + Math.max(lastCallMs, 2000) > timeLimitMs) {
      timeUp = true;
    }
    if (stopped || saveError || timeUp) {
      const why = stopped ? stopped.message : saveError ? "the results could not be saved." : "the time limit was reached.";
      results[i] = { ...base, verdict: null, send: false, error: "not_checked", message: `Not checked: ${why}` };
      emit(i);
      continue;
    }

    if (calls > 0 && delayMs) await sleep(delayMs);
    const callStart = Date.now();
    // Each request gets at most the time left before the limit (but never less than a few
    // seconds), so a slow answer can't carry a run far past the agent's own timeout.
    const budget = () =>
      timeLimitMs > 0 ? Math.min(MAX_REQUEST_MS, Math.max(MIN_REQUEST_MS, timeLimitMs - (Date.now() - started))) : MAX_REQUEST_MS;
    let { status, body } = await callApi(url, payload, { key, timeoutMs: budget() });
    const remaining = timeLimitMs > 0 ? timeLimitMs - (Date.now() - started) : Infinity;
    if (transient(status, body) && remaining >= RETRY_WAIT_MS + MIN_REQUEST_MS) {
      await sleep(RETRY_WAIT_MS);
      ({ status, body } = await callApi(url, payload, { key, timeoutMs: budget() }));
    }
    lastCallMs = Date.now() - callStart;
    calls++;
    const { usage: used, ...answer } = summarise(status, body, origin);
    if (used) usage = used;
    results[i] = { ...base, ...answer, ...(answer.verdict ? { facts_hash: hash } : {}) };
    if (answer.verdict) {
      failuresInARow = 0;
      answered.set(hash, i);
    } else if (STOP_ERRORS.has(answer.error)) {
      stopped = answer;
    } else if (!ROW_ERRORS.has(answer.error)) {
      failuresInARow++;
      if (failuresInARow >= 3) stopped = { ...answer, message: `three checks in a row failed (${answer.message})` };
    }
    emit(i);
    save();
  }
  return finish();
}

const defaultOut = {
  stdout: (line) => process.stdout.write(line.endsWith("\n") ? line : line + "\n"),
  stderr: (line) => process.stderr.write(line.endsWith("\n") ? line : line + "\n"),
};

export async function main(argv = process.argv.slice(2), env = process.env, out = defaultOut) {
  let opts;
  try {
    opts = parseArgs(argv);
  } catch (err) {
    out.stdout(JSON.stringify({ error: "usage", message: err.message }));
    return EXIT.USAGE;
  }
  if (opts.help || argv.length === 0) {
    out.stdout(USAGE);
    return opts.help ? EXIT.OK : EXIT.USAGE;
  }
  try {
    if (opts.file) {
      if (opts.email || opts.domain) throw new Error("Use --file on its own, or --email/--domain for one address");
      return await runList(opts, env, out);
    }
    if (opts.out) throw new Error("--out only works with --file");
    return await runOne(opts, env, out);
  } catch (err) {
    out.stdout(JSON.stringify({ error: "usage", message: err.message }));
    return EXIT.USAGE;
  }
}

function invokedDirectly() {
  if (!process.argv[1]) return false;
  try {
    const self = realpathSync(fileURLToPath(import.meta.url));
    const invoked = realpathSync(resolve(process.argv[1]));
    return process.platform === "win32" ? self.toLowerCase() === invoked.toLowerCase() : self === invoked;
  } catch {
    return false;
  }
}

if (invokedDirectly()) {
  main().then((code) => {
    process.exitCode = code;
  });
}
