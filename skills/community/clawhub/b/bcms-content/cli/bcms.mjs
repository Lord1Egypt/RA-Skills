#!/usr/bin/env node
/**
 * bcms-content — thin, agent-facing CLI for BCMS content operations.
 *
 * Wraps the official `@thebcms/client` SDK so entry meta is converted to the
 * raw props the backend expects (the SDK handles that; raw REST does not).
 *
 * Auth: set BCMS_API_KEY="keyId.secret.instanceId" — the SAME three-part key
 * used for the BCMS MCP. Optionally set BCMS_API_ORIGIN for self-hosted setups.
 *
 * Usage:
 *   node cli/bcms.mjs <command> [args] [flags]
 *   npx bcms-content <command> [args] [flags]   (after `npm install` in this folder)
 *
 * Commands:
 *   create-entry <template>  --data '<json>' | --data-file <path>  [--lng en] [--status <id>]
 *   update-entry <entryId>   --template <t>  --data '<json>'       [--lng en] [--status <id>]
 *   delete-entry <entryId>   --template <t>
 *   list-entries <template>
 *   upload-media <filePath>  [--parent <dirId>]
 *   help
 *
 * --data JSON shape (single language; --lng controls the locale):
 *   create: { "meta": { "<propName>": <value>, ... }, "content"?: <string | node[]> }
 *   update: { "meta": { ... }, "content"?: <string | node[]> }   // content preserved if omitted
 *
 * `content` may be a plain string (blank lines split paragraphs) or a raw
 * EntryContentNode[] array for rich text (headings, lists, media, widgets).
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import process from 'node:process';

const MIME_BY_EXT = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.avif': 'image/avif',
    '.pdf': 'application/pdf',
    '.json': 'application/json',
    '.txt': 'text/plain',
    '.md': 'text/markdown',
    '.csv': 'text/csv',
    '.mp4': 'video/mp4',
    '.webm': 'video/webm',
    '.mp3': 'audio/mpeg',
    '.zip': 'application/zip',
};

function fail(message) {
    console.error(`bcms-content: ${message}`);
    process.exit(1);
}

function mimeFromName(name) {
    return MIME_BY_EXT[path.extname(name).toLowerCase()] || 'application/octet-stream';
}

function parseArgs(argv) {
    const args = { _: [] };
    for (let i = 0; i < argv.length; i++) {
        const token = argv[i];
        if (token.startsWith('--')) {
            const key = token.slice(2);
            const next = argv[i + 1];
            if (next === undefined || next.startsWith('--')) {
                args[key] = true;
            } else {
                args[key] = next;
                i++;
            }
        } else {
            args._.push(token);
        }
    }
    return args;
}

async function getClient() {
    const apiKey = process.env.BCMS_API_KEY;
    if (!apiKey) {
        fail(
            'BCMS_API_KEY is required (format: keyId.secret.instanceId — the same key used for the BCMS MCP).',
        );
    }
    let Client;
    try {
        ({ Client } = await import('@thebcms/client'));
    } catch {
        fail(
            'Cannot find "@thebcms/client". Run `npm install` inside the bcms-content skill folder first.',
        );
    }
    const options = { apiKey, useMemCache: true, injectSvg: false };
    if (process.env.BCMS_API_ORIGIN) {
        options.cmsOrigin = process.env.BCMS_API_ORIGIN;
    }
    return new Client(options);
}

function readData(args) {
    let raw;
    if (args['data-file']) {
        raw = fs.readFileSync(path.resolve(String(args['data-file'])), 'utf8');
    } else if (typeof args.data === 'string') {
        raw = args.data;
    }
    if (!raw) {
        fail("missing entry data — pass --data '<json>' or --data-file <path>.");
    }
    try {
        return JSON.parse(raw);
    } catch (err) {
        fail(`--data is not valid JSON: ${err.message}`);
    }
}

function toContentNodes(content) {
    if (!content) {
        return [];
    }
    if (Array.isArray(content)) {
        return content;
    }
    if (typeof content === 'string') {
        return content.split(/\n{2,}/).map((block) => {
            const text = block.trim();
            return {
                type: 'paragraph',
                content: text ? [{ type: 'text', text: text.replace(/\n/g, ' ') }] : [],
            };
        });
    }
    fail('`content` must be a string or an array of content nodes.');
}

function printResult(message, payload) {
    console.log(message);
    console.log(JSON.stringify(payload, null, 2));
}

async function createEntry(args) {
    const template = args._[0] || (typeof args.template === 'string' ? args.template : undefined);
    if (!template) {
        fail('create-entry requires a template: `create-entry <templateIdOrName>`.');
    }
    const lng = typeof args.lng === 'string' ? args.lng : 'en';
    const status = typeof args.status === 'string' ? args.status : undefined;
    const input = readData(args);
    const client = await getClient();
    const entry = await client.entry.create(template, {
        statuses: status ? [{ lng, id: status }] : [],
        meta: [{ lng, data: input.meta || {} }],
        content: [{ lng, nodes: toContentNodes(input.content) }],
    });
    const fullEntry = await client.entry.getById(entry._id, template);
    printResult(`Created entry ${entry._id} (template "${template}")`, fullEntry);
}

async function updateEntry(args) {
    const entryId = args._[0];
    const template = typeof args.template === 'string' ? args.template : undefined;
    if (!entryId) {
        fail('update-entry requires an entry id: `update-entry <entryId> --template <t>`.');
    }
    if (!template) {
        fail('update-entry requires --template <idOrName>.');
    }
    const lng = typeof args.lng === 'string' ? args.lng : 'en';
    const status = typeof args.status === 'string' ? args.status : undefined;
    const input = readData(args);
    const client = await getClient();
    let nodes;
    if (input.content !== undefined) {
        nodes = toContentNodes(input.content);
    } else {
        const existing = await client.entry.getByIdRaw(entryId, template);
        const current = existing.content.find((e) => e.lng === lng);
        nodes = current ? current.nodes : [];
    }
    const existingParsed = await client.entry.getById(entryId, template);
    const existingMeta = existingParsed.meta[lng] || {};
    const mergedMeta = { ...existingMeta, ...(input.meta || {}) };
    const entry = await client.entry.update(template, entryId, {
        lng,
        status,
        meta: mergedMeta,
        content: nodes,
    });
    const fullEntry = await client.entry.getById(entryId, template);
    printResult(`Updated entry ${entry._id} (template "${template}")`, fullEntry);
}

async function deleteEntry(args) {
    const entryId = args._[0];
    const template = typeof args.template === 'string' ? args.template : undefined;
    if (!entryId) {
        fail('delete-entry requires an entry id: `delete-entry <entryId> --template <t>`.');
    }
    if (!template) {
        fail('delete-entry requires --template <idOrName>.');
    }
    const client = await getClient();
    await client.entry.deleteById(entryId, template);
    console.log(`Deleted entry ${entryId} (template "${template}")`);
}

async function listEntries(args) {
    const template = args._[0] || (typeof args.template === 'string' ? args.template : undefined);
    if (!template) {
        fail('list-entries requires a template: `list-entries <templateIdOrName>`.');
    }
    const client = await getClient();
    const entries = await client.entry.getAllLite(template);
    console.log(
        JSON.stringify(
            entries.map((e) => ({ _id: e._id, templateId: e.templateId })),
            null,
            2,
        ),
    );
}

async function uploadMedia(args) {
    const filePath = args._[0];
    if (!filePath) {
        fail('upload-media requires a file path: `upload-media <filePath>`.');
    }
    const abs = path.resolve(filePath);
    if (!fs.existsSync(abs)) {
        fail(`file not found: ${abs}`);
    }
    const name = path.basename(abs);
    const buffer = await fs.promises.readFile(abs);
    const parentId = typeof args.parent === 'string' ? args.parent : undefined;
    const client = await getClient();
    const uploadToken = await client.media.requestUploadToken();
    const file = new File([buffer], name, { type: mimeFromName(name) });
    const media = await client.media.createFile({ uploadToken, file, name, parentId });
    printResult(`Uploaded media ${media._id} (${media.name})`, {
        _id: media._id,
        name: media.name,
        type: media.type,
    });
}

function printHelp() {
    console.log(`bcms-content — BCMS content operations CLI

Auth:
  export BCMS_API_KEY="keyId.secret.instanceId"   (same key as the BCMS MCP)
  export BCMS_API_ORIGIN="https://app.thebcms.com" (optional; for self-hosted)

Commands:
  create-entry <template>  --data '<json>' | --data-file <path>  [--lng en] [--status <id>]
  update-entry <entryId>   --template <t>  --data '<json>'       [--lng en] [--status <id>]
  delete-entry <entryId>   --template <t>
  list-entries <template>
  upload-media <filePath>  [--parent <dirId>]
  help

--data JSON (single language, controlled by --lng):
  { "meta": { "<propName>": <value> }, "content"?: "<string or node[]>" }

Examples:
  node cli/bcms.mjs create-entry blog --data '{"meta":{"title":"Hello","slug":"hello"},"content":"First paragraph."}'
  node cli/bcms.mjs update-entry 663f... --template blog --data '{"meta":{"title":"Updated title"}}'
  node cli/bcms.mjs list-entries blog
  node cli/bcms.mjs delete-entry 663f... --template blog
  node cli/bcms.mjs upload-media ./hero.png`);
}

async function main() {
    const argv = process.argv.slice(2);
    const command = argv[0];
    const args = parseArgs(argv.slice(1));

    switch (command) {
        case 'create-entry':
            return createEntry(args);
        case 'update-entry':
            return updateEntry(args);
        case 'delete-entry':
            return deleteEntry(args);
        case 'list-entries':
            return listEntries(args);
        case 'upload-media':
            return uploadMedia(args);
        case 'help':
        case '--help':
        case '-h':
        case undefined:
            return printHelp();
        default:
            console.error(`Unknown command: ${command}\n`);
            printHelp();
            process.exit(1);
    }
}

main().catch((err) => {
    const detail = err && err.response && err.response.data ? JSON.stringify(err.response.data) : err.message;
    fail(detail || String(err));
});
