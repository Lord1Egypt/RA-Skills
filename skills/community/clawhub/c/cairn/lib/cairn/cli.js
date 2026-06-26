#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { DEFAULT_CONFIG_PATH, USAGE } from './constants/cli.constants.js';
import { Cairn } from './index.js';
// ─── small helpers (no Cairn dep) ───────────────────────────────
const die = (msg) => {
    console.error(msg);
    process.exit(1);
};
const refOrDie = (ref) => {
    const n = Number(ref);
    return Number.isInteger(n) && String(n) === ref ? n : ref;
};
const indent = (s) => s
    .split('\n')
    .map((l) => `  ${l}`)
    .join('\n');
const loadConfig = () => {
    const configPath = join(process.cwd(), DEFAULT_CONFIG_PATH);
    if (!existsSync(configPath))
        return null;
    try {
        return JSON.parse(readFileSync(configPath, 'utf8'));
    }
    catch {
        return null;
    }
};
// minimal flag parser. supports: --string-flag VALUE, --bool-flag, --array-flag V1 --array-flag V2.
const parseFlags = (args, spec) => {
    const out = {};
    for (const name of spec.array ?? [])
        out[name] = [];
    for (let i = 0; i < args.length; i++) {
        const a = args[i];
        let key = null;
        if (a.startsWith('--'))
            key = a.slice(2);
        else if (a === '-k')
            key = 'k';
        if (!key)
            continue;
        if (spec.boolean?.includes(key)) {
            out[key] = true;
            continue;
        }
        const v = args[++i];
        if (v === undefined)
            die(`missing value for --${key}`);
        if (spec.number?.includes(key))
            out[key] = Number(v);
        else if (spec.array?.includes(key))
            out[key].push(v);
        else
            out[key] = v;
    }
    return out;
};
const mergeIncludeOpts = (flags, config) => {
    if (flags && flags.length > 0)
        return flags;
    return config?.include && config.include.length > 0 ? [...config.include] : undefined;
};
const mergeExcludeOpts = (flags, config) => {
    if (flags && flags.length > 0)
        return flags;
    return config?.exclude && config.exclude.length > 0 ? [...config.exclude] : undefined;
};
const buildAddInput = (target, opts, config = null) => {
    const label = opts.label;
    if (target.startsWith('http://') || target.startsWith('https://')) {
        return { kind: 'web', url: target, label };
    }
    if (!existsSync(target))
        die(`not a URL or path: ${target}`);
    const st = statSync(target);
    if (st.isDirectory()) {
        const isRoot = target === '.' || target === './' || target === '/';
        const kind = opts.kind
            ? opts.kind
            : isRoot && config?.default_kind
                ? config.default_kind
                : 'code';
        return {
            kind: kind,
            path: target,
            label,
            include: mergeIncludeOpts(opts.include, config),
            exclude: mergeExcludeOpts(opts.exclude, config),
            force: opts.force,
        };
    }
    if (target.toLowerCase().endsWith('.pdf')) {
        return { kind: 'pdf', path: target, label };
    }
    return { kind: 'file', path: target, label };
};
// ─── dispatch ───────────────────────────────────────────────────
const argv = process.argv.slice(2);
const [cmd, ...rest] = argv;
if (!cmd || cmd === 'help' || cmd === '--help' || cmd === '-h') {
    console.log(USAGE);
    process.exit(0);
}
const envRuntime = process.env.CAIRN_RUNTIME;
const runtime = envRuntime === 'ollama' || envRuntime === 'embedded' ? envRuntime : undefined;
const cairn = new Cairn({ runtime });
// ─── commands (capture `cairn` from module scope) ───────────────
const runAdd = async (args) => {
    const target = args[0];
    if (!target || target.startsWith('--'))
        die('add: missing url/path argument');
    const opts = parseFlags(args.slice(1), {
        string: ['label'],
        array: ['include', 'exclude'],
        boolean: ['force'],
    });
    const config = loadConfig();
    const input = buildAddInput(target, opts, config);
    const result = await cairn.ingest.add(input);
    console.log(`added id=${result.source_id} files=${result.files_indexed} chunks=${result.chunks_created}`);
};
const runList = async (args) => {
    const { kind } = parseFlags(args, { string: ['kind'] });
    const sources = await cairn.retrieve.list(kind ? { kind: kind } : undefined);
    if (sources.length === 0) {
        console.log('no indexed sources');
        return;
    }
    for (const s of sources) {
        const label = s.label ? ` ${s.label}` : '';
        console.log(`${s.id}\t[${s.kind}]${label}\t${s.uri}`);
    }
};
const runSearch = async (args) => {
    const query = args[0];
    if (!query || query.startsWith('--'))
        die('search: missing query');
    const opts = parseFlags(args.slice(1), {
        number: ['k'],
        string: ['kind', 'source', 'tag'],
    });
    const hits = await cairn.retrieve.search(query, {
        k: opts.k,
        kind: opts.kind,
        source: opts.source,
        tag: opts.tag,
    });
    if (hits.length === 0) {
        console.log('no results');
        return;
    }
    for (const [i, h] of hits.entries()) {
        const fts = h.fts_rank !== null ? `fts=${h.fts_rank}` : 'fts=-';
        const vec = h.vec_rank !== null ? `vec=${h.vec_rank}` : 'vec=-';
        console.log(`[${i + 1}] ${h.source.kind} · ${h.file_path}:${h.start_line}-${h.end_line} ` +
            `· ${h.score.toFixed(4)} · ${fts} ${vec}`);
        console.log(indent(h.content));
        console.log();
    }
};
const runAsk = async (args) => {
    const query = args[0];
    if (!query || query.startsWith('--'))
        die('ask: missing query');
    const opts = parseFlags(args.slice(1), {
        number: ['k', 'entities', 'edges'],
        string: ['kind', 'source', 'tag'],
    });
    const hits = await cairn.retrieve.ask(query, {
        k: opts.k,
        tag: opts.tag,
        kind: opts.kind,
        source: opts.source,
        maxEntitiesPerHit: opts.entities,
        maxEdgesPerEntity: opts.edges,
    });
    if (hits.length === 0) {
        console.log('no results');
        return;
    }
    for (const [i, h] of hits.entries()) {
        const fts = h.fts_rank !== null ? `fts=${h.fts_rank}` : 'fts=-';
        const vec = h.vec_rank !== null ? `vec=${h.vec_rank}` : 'vec=-';
        console.log(`[${i + 1}] ${h.source.kind} · ${h.file_path}:${h.start_line}-${h.end_line} ` +
            `· ${h.score.toFixed(4)} · ${fts} ${vec}`);
        console.log(indent(h.content));
        if (h.entities.length > 0) {
            console.log('  ── entities ─────');
            for (const ent of h.entities) {
                const e = ent.entity;
                const loc = e.line_start !== null && e.line_end !== null ? `:${e.line_start}-${e.line_end}` : '';
                const tags = ent.tags.length > 0 ? ` · tags: ${ent.tags.join(', ')}` : '';
                console.log(`  ${e.kind}/${e.name} (${e.id}${loc})${tags}`);
                for (const edge of ent.edges_out) {
                    console.log(`    -[${edge.relation}@${edge.confidence}]-> ${edge.to_id}`);
                }
                for (const edge of ent.edges_in) {
                    console.log(`    <-[${edge.relation}@${edge.confidence}]- ${edge.from_id}`);
                }
            }
        }
        console.log();
    }
};
const runPath = async (args) => {
    const [from, to] = args;
    if (!from || !to)
        die('path: missing <from-id> <to-id>');
    const opts = parseFlags(args.slice(2), {
        number: ['depth'],
        boolean: ['directed'],
    });
    const result = await cairn.retrieve.path(from, to, {
        maxDepth: opts.depth,
        directed: opts.directed,
    });
    if (!result) {
        console.log('no path found');
        return;
    }
    for (let i = 0; i < result.entities.length; i++) {
        const e = result.entities[i];
        console.log(`${i === 0 ? '◯' : '└'} ${e.kind}/${e.name} (${e.id})`);
        if (i < result.steps.length) {
            const step = result.steps[i];
            const arrow = step.reversed ? '<-' : '->';
            console.log(`  ${arrow}[${step.edge.relation}@${step.edge.confidence}, ${step.edge.derive}]${arrow}`);
        }
    }
};
const runRefresh = async (args) => {
    const ref = args[0];
    if (!ref)
        die('refresh: missing id|uri|all');
    const target = ref === 'all' ? 'all' : refOrDie(ref);
    const results = await cairn.ingest.refresh(target);
    for (const r of results) {
        console.log(`src=${r.source_id} changed=${r.files_changed} unchanged=${r.files_unchanged} ` +
            `chunks_created=${r.chunks_created} chunks_deleted=${r.chunks_deleted}`);
    }
};
const runReindex = async (args) => {
    const ref = args[0];
    if (!ref)
        die('reindex: missing id|uri|all');
    const target = ref === 'all' ? 'all' : refOrDie(ref);
    const results = await cairn.ingest.reindex(target);
    for (const r of results) {
        console.log(`src=${r.source_id} changed=${r.files_changed} unchanged=${r.files_unchanged} ` +
            `chunks_created=${r.chunks_created} chunks_deleted=${r.chunks_deleted}`);
    }
};
const runGraph = async (args) => {
    const opts = parseFlags(args, { string: ['entity', 'tag'], number: ['k'] });
    const entityId = opts.entity;
    let query;
    if (!entityId) {
        const first = args[0];
        if (!first || first.startsWith('--'))
            die('graph: missing query or --entity <id>');
        query = first;
    }
    const hits = await cairn.retrieve.graph({
        query,
        entity_id: entityId,
        k: opts.k,
        tag: opts.tag,
    });
    if (hits.length === 0) {
        console.log(entityId ? `entity not found: ${entityId}` : 'no results');
        return;
    }
    for (const [i, h] of hits.entries()) {
        const e = h.entity;
        const loc = e.source ? ` · ${e.source}${e.line_start ? `:${e.line_start}` : ''}` : '';
        const score = h.score !== null ? ` · rank=${h.score}` : '';
        const tags = h.tags.length > 0 ? ` · tags: ${h.tags.join(', ')}` : '';
        console.log(`[${i + 1}] ${e.kind}/${e.name} (${e.id})${loc}${score}${tags}`);
        for (const edge of h.edges_out) {
            console.log(`    -[${edge.relation}@${edge.confidence}]-> ${edge.to_id}`);
        }
        for (const edge of h.edges_in) {
            console.log(`    <-[${edge.relation}@${edge.confidence}]- ${edge.from_id}`);
        }
        console.log();
    }
};
const runRemove = async (args) => {
    const ref = args[0];
    if (!ref)
        die('remove: missing id|uri');
    await cairn.ingest.remove(refOrDie(ref));
    console.log('removed');
};
const runLink = async (args) => {
    const [a, b] = args;
    if (!a || !b)
        die('link: missing <from-id|uri> <to-id|uri>');
    await cairn.ingest.link(refOrDie(a), refOrDie(b));
    console.log(`linked ${a} → ${b}`);
};
const runUnlink = async (args) => {
    const [a, b] = args;
    if (!a || !b)
        die('unlink: missing <from-id|uri> <to-id|uri>');
    await cairn.ingest.unlink(refOrDie(a), refOrDie(b));
    console.log(`unlinked ${a} → ${b}`);
};
const runLinks = async () => {
    const links = await cairn.ingest.links();
    if (links.length === 0) {
        console.log('no source links');
        return;
    }
    for (const l of links)
        console.log(`${l.from} → ${l.to}`);
};
const runTags = async () => {
    const tags = await cairn.retrieve.listTags();
    if (tags.length === 0) {
        console.log('no tags in use');
        return;
    }
    for (const t of tags)
        console.log(`${t.count}\t${t.tag}`);
};
const runInit = () => {
    const configDir = join(process.cwd(), '.cairn');
    const configPath = join(configDir, 'config.json');
    if (existsSync(configPath)) {
        die('.cairn/config.json already exists (use --force to overwrite)');
    }
    mkdirSync(configDir, { recursive: true });
    const config = {
        include: [],
        exclude: ['test', 'fixtures', 'example', 'node_modules', '.git', 'dist', 'build', 'target'],
        default_kind: 'code',
    };
    writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`created .cairn/config.json`);
};
// ─── execute ────────────────────────────────────────────────────
try {
    switch (cmd) {
        case 'add':
            await runAdd(rest);
            break;
        case 'list':
            await runList(rest);
            break;
        case 'search':
            await runSearch(rest);
            break;
        case 'ask':
            await runAsk(rest);
            break;
        case 'graph':
            await runGraph(rest);
            break;
        case 'path':
            await runPath(rest);
            break;
        case 'refresh':
            await runRefresh(rest);
            break;
        case 'reindex':
            await runReindex(rest);
            break;
        case 'link':
            await runLink(rest);
            break;
        case 'unlink':
            await runUnlink(rest);
            break;
        case 'links':
            await runLinks();
            break;
        case 'tags':
            await runTags();
            break;
        case 'remove':
            await runRemove(rest);
            break;
        case 'init':
            runInit();
            break;
        default:
            console.error(`unknown command: ${cmd}`);
            console.error(USAGE);
            process.exit(1);
    }
}
finally {
    cairn.close();
}
