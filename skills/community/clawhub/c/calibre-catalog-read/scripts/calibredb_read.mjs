#!/usr/bin/env node
import {
  parseArgs,
  loadConfig,
  resolveEndpoint,
  validateFields,
  runCalibre,
  machineJson,
  shortError,
} from "./lib/calibre_common.mjs";
const FIELDS =
  "title,authors,author_sort,uuid,series,series_index,tags,formats,publisher,pubdate,languages,last_modified";
const ALLOWED = [
  "with-library",
  "library-id",
  "config",
  "username",
  "password-env",
  "timeout",
  "fields",
  "limit",
  "query",
  "book-id",
];
function integer(value, name, max = Number.MAX_SAFE_INTEGER) {
  if (
    !/^[1-9][0-9]*$/.test(String(value)) ||
    !Number.isSafeInteger(Number(value)) ||
    Number(value) > max
  )
    throw new Error(name + " must be a positive bounded integer");
  return Number(value);
}
function main() {
  const raw = process.argv.slice(2);
  if (raw.includes("--help") || raw.length === 0)
    return {
      usage:
        "node /absolute/skill/scripts/calibredb_read.mjs <list|search|id|libraries> [--with-library URL#ID] [--book-id N] [--query TEXT] [--limit N]",
    };
  const command = raw.shift();
  if (!["list", "search", "id", "libraries"].includes(command))
    throw new Error("read-only commands: list/search/id/libraries");
  const args = parseArgs(raw, ALLOWED);
  if (args._.length) throw new Error("unexpected positional arguments");
  if (args["book-id"] && command !== "id") throw new Error("--book-id is only valid for id");
  if (args.query && command !== "search") throw new Error("--query is only valid for search");
  const loaded = loadConfig(args);
  if (command === "libraries") args["library-id"] = "-";
  let endpoint = resolveEndpoint(args, loaded);
  if (command === "libraries") {
    if (!/^https?:/.test(endpoint)) throw new Error("libraries requires a Content server endpoint");
    const u = new URL(endpoint);
    u.hash = "-";
    endpoint = u.toString();
    const result = runCalibre(["list"], args, {
      endpoint,
      config: loaded.config,
      timeoutSeconds: integer(args.timeout || 120, "--timeout", 3600),
    });
    return {
      ok: true,
      mode: command,
      endpoint,
      items: result
        .split(/\r?\n/)
        .map((x) => x.trim())
        .filter(Boolean),
    };
  }
  if (/^https?:/.test(endpoint) && new URL(endpoint).hash === "#-")
    throw new Error("select a library id; use libraries for discovery");
  const fields = validateFields(args.fields, FIELDS + (command === "id" ? ",comments" : ""));
  const limit = command === "id" ? 2 : integer(args.limit || 100, "--limit", 10000);
  const cmd = ["list", "--for-machine", "--fields", fields, "--limit", String(limit)];
  let id;
  if (command === "id") {
    id = integer(args["book-id"], "--book-id");
    cmd.push("--search", "id:" + id);
  }
  if (command === "search") {
    if (!args.query?.trim()) throw new Error("missing --query");
    cmd.push("--search", args.query);
  }
  const items = machineJson(
    runCalibre(cmd, args, {
      endpoint,
      config: loaded.config,
      timeoutSeconds: integer(args.timeout || 120, "--timeout", 3600),
    }),
  );
  if (
    !Array.isArray(items) ||
    items.some((x) => !x || typeof x !== "object" || !Number.isSafeInteger(x.id))
  )
    throw new Error("invalid catalogue rows");
  const out = {
    ok: true,
    mode: command,
    endpoint,
    library_id: endpoint,
    fields,
    items,
    possibly_truncated: command !== "id" && items.length >= limit,
  };
  if (command === "id") {
    const matches = items.filter((x) => x.id === id);
    if (matches.length > 1) throw new Error("ambiguous exact id");
    out.book_id = id;
    out.item = matches[0] || null;
    out.found = matches.length === 1;
    out.items = matches;
  }
  return out;
}
try {
  process.stdout.write(JSON.stringify(main(), null, 2) + "\n");
} catch (error) {
  process.stdout.write(JSON.stringify({ ok: false, error: shortError(error) }) + "\n");
  process.exitCode = 1;
}
