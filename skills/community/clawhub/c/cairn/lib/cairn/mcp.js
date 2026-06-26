#!/usr/bin/env node
import { existsSync, statSync } from 'node:fs';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { Cairn } from './index.js';
const envRuntime = process.env.CAIRN_RUNTIME;
const runtime = envRuntime === 'ollama' || envRuntime === 'embedded' ? envRuntime : undefined;
const cairn = new Cairn({ runtime });
// v1.2.1+: surface the path-allowlist call to operators who didn't read the
// docs. Connected agents can ingest any local path by default; CAIRN_ALLOWED_ROOTS
// confines them. Real protection is host-side per-call approval; this is the nudge.
if (!process.env.CAIRN_ALLOWED_ROOTS) {
    console.warn('cairn-mcp: CAIRN_ALLOWED_ROOTS unset — connected agents can ingest any local path. ' +
        'Set CAIRN_ALLOWED_ROOTS=/comma/separated/abs/paths to confine ingestion. ' +
        'See SKILL.md "Configuration & safety" or docs/setup.md.');
}
const server = new McpServer({ name: 'cairn', version: '1.2.1' });
server.registerTool('search', {
    description: 'Hybrid search (FTS5 + semantic) across indexed sources. ' +
        'Returns ranked chunks with source, file path, line range, and content.',
    inputSchema: {
        query: z.string().describe('Search query'),
        k: z.number().int().min(1).max(50).optional().describe('Top-N results (default 8)'),
        kind: z
            .enum(['web', 'code', 'file', 'text', 'pdf'])
            .optional()
            .describe('Filter by source kind'),
        source: z
            .union([z.number(), z.string()])
            .optional()
            .describe('Filter by source id (number) or uri (string)'),
        tag: z
            .string()
            .optional()
            .describe('Narrow to chunks whose source file produces at least one entity carrying this tag.'),
    },
}, async ({ query, k, kind, source, tag }) => {
    const hits = await cairn.retrieve.search(query, { k, kind, source, tag });
    return { content: [{ type: 'text', text: formatHits(hits, { kind, source, tag }) }] };
});
server.registerTool('list', {
    description: 'List indexed sources.',
    inputSchema: {
        kind: z.enum(['web', 'code', 'file', 'text', 'pdf']).optional().describe('Filter by kind'),
    },
}, async ({ kind }) => {
    const sources = await cairn.retrieve.list({ kind });
    return { content: [{ type: 'text', text: formatSources(sources) }] };
});
server.registerTool('add', {
    description: 'Add a new source to the index. Auto-detects kind when unspecified: URLs → web, directories → code, *.pdf → pdf, other files → file.',
    inputSchema: {
        kind: z
            .enum(['web', 'code', 'file', 'text', 'pdf'])
            .optional()
            .describe('Source kind. Default: auto-detect from url/path.'),
        target: z.string().describe('URL (for web) or absolute path (for code/file/pdf).'),
        label: z.string().optional().describe('Optional human-readable label.'),
        include: z
            .array(z.string())
            .optional()
            .describe('Suffix matches for code kind (e.g. [".ts", ".tsx"]). Any-of.'),
        exclude: z
            .array(z.string())
            .optional()
            .describe('Path substrings to skip for code kind (e.g. ["test", "fixtures"]).'),
    },
}, async ({ kind, target, label, include, exclude }) => {
    const inputKind = kind ?? autoDetectKind(target);
    const input = buildAddInput(inputKind, target, label, include, exclude);
    const result = await cairn.ingest.add(input);
    return {
        content: [
            {
                type: 'text',
                text: `added id=${result.source_id} kind=${inputKind} files=${result.files_indexed} chunks=${result.chunks_created}`,
            },
        ],
    };
});
server.registerTool('graph', {
    description: 'Query the knowledge graph. Provide `query` for semantic entity lookup (top-k entities + edges) ' +
        'or `entity_id` for direct traversal of a single entity. Returns entities with outbound and inbound edges. ' +
        'Use this for relationship-aware questions ("what calls X?", "what does Y depend on?"); ' +
        'use `search` for passage-level retrieval.',
    inputSchema: {
        query: z.string().optional().describe('Natural-language query — semantic entity search.'),
        entity_id: z
            .string()
            .optional()
            .describe('Exact entity id (e.g. "src/foo.ts:fooFn") for direct lookup.'),
        k: z
            .number()
            .int()
            .min(1)
            .max(50)
            .optional()
            .describe('Top-N for query mode (default 8). Ignored for entity_id.'),
        tag: z.string().optional().describe('Filter results to entities carrying this tag.'),
    },
}, async ({ query, entity_id, k, tag }) => {
    if (!query === !entity_id) {
        return {
            content: [{ type: 'text', text: 'error: provide exactly one of `query` or `entity_id`' }],
            isError: true,
        };
    }
    const hits = await cairn.retrieve.graph({ query, entity_id, k, tag });
    return { content: [{ type: 'text', text: formatGraphHits(hits) }] };
});
server.registerTool('ask', {
    description: 'Composed retrieval: hybrid search like `search`, but each hit also returns the entities ' +
        'in that file plus their 1-hop graph neighbors. Use this when you want code/text passages ' +
        'AND their relationship context in one call (replaces a search-then-graph round trip).',
    inputSchema: {
        query: z.string().describe('Search query'),
        k: z.number().int().min(1).max(50).optional().describe('Top-N hits (default 8)'),
        kind: z
            .enum(['web', 'code', 'file', 'text', 'pdf'])
            .optional()
            .describe('Filter by source kind'),
        source: z
            .union([z.number(), z.string()])
            .optional()
            .describe('Filter by source id or uri'),
        maxEntitiesPerHit: z
            .number()
            .int()
            .min(1)
            .max(20)
            .optional()
            .describe('Max entities returned per hit (default 6)'),
        maxEdgesPerEntity: z
            .number()
            .int()
            .min(1)
            .max(20)
            .optional()
            .describe('Max edges per direction per entity (default 4)'),
        tag: z
            .string()
            .optional()
            .describe('Narrow chunks AND per-hit entities to those carrying this tag.'),
    },
}, async ({ query, k, kind, source, maxEntitiesPerHit, maxEdgesPerEntity, tag }) => {
    const hits = await cairn.retrieve.ask(query, {
        k,
        kind,
        source,
        tag,
        maxEntitiesPerHit,
        maxEdgesPerEntity,
    });
    return { content: [{ type: 'text', text: formatAskHits(hits, { kind, source, tag }) }] };
});
server.registerTool('path', {
    description: 'Find the shortest path between two entities through the graph. Useful for "how is X ' +
        'connected to Y" questions. Walks edges as undirected by default; pass directed=true to ' +
        'follow only outbound edges.',
    inputSchema: {
        from: z.string().describe('Source entity id'),
        to: z.string().describe('Target entity id'),
        maxDepth: z
            .number()
            .int()
            .min(1)
            .max(8)
            .optional()
            .describe('Max BFS depth (default 4)'),
        directed: z.boolean().optional().describe('Follow only outbound edges (default false)'),
    },
}, async ({ from, to, maxDepth, directed }) => {
    const result = await cairn.retrieve.path(from, to, { maxDepth, directed });
    return { content: [{ type: 'text', text: formatPath(result) }] };
});
server.registerTool('tags', {
    description: 'List every tag in use across active entities, with counts. Useful for discovering ' +
        'what tag vocabulary the index actually contains before filtering by tag.',
    inputSchema: {},
}, async () => {
    const tags = await cairn.retrieve.listTags();
    if (tags.length === 0) {
        return { content: [{ type: 'text', text: 'no tags in use' }] };
    }
    const text = tags.map((t) => `${t.count}\t${t.tag}`).join('\n');
    return { content: [{ type: 'text', text }] };
});
server.registerTool('refresh', {
    description: 'Re-index an existing source. Fetches latest content, re-chunks and re-embeds if changed. Use "all" to refresh every source.',
    inputSchema: {
        ref: z
            .union([z.number(), z.string()])
            .describe('Source id (number or numeric string), uri, or "all".'),
    },
}, async ({ ref }) => {
    // Coerce string-of-digits to numeric SourceId. Without this, "41" arriving
    // from an MCP client falls through to URI lookup, fails resolution, and
    // (depending on transport) can leave the MCP server in a bad state.
    let arg;
    if (ref === 'all')
        arg = 'all';
    else if (typeof ref === 'number')
        arg = ref;
    else if (/^\d+$/.test(ref))
        arg = Number(ref);
    else
        arg = ref;
    const results = await cairn.ingest.refresh(arg);
    const lines = results.map((r) => `src=${r.source_id} changed=${r.files_changed} unchanged=${r.files_unchanged} created=${r.chunks_created} deleted=${r.chunks_deleted}`);
    return { content: [{ type: 'text', text: lines.join('\n') }] };
});
const transport = new StdioServerTransport();
await server.connect(transport);
process.on('SIGINT', () => {
    cairn.close();
    process.exit(0);
});
process.on('SIGTERM', () => {
    cairn.close();
    process.exit(0);
});
const describeFilter = (filter) => {
    if (!filter)
        return '';
    const parts = [];
    if (filter.kind)
        parts.push(`kind=${filter.kind}`);
    if (filter.source !== undefined)
        parts.push(`source=${filter.source}`);
    if (filter.tag)
        parts.push(`tag=${filter.tag}`);
    return parts.length > 0 ? ` (filter: ${parts.join(', ')})` : '';
};
const formatHits = (hits, filter) => {
    if (hits.length === 0)
        return `no results${describeFilter(filter)}`;
    const blocks = hits.map((h, i) => {
        const fts = h.fts_rank !== null ? `fts=${h.fts_rank}` : 'fts=-';
        const vec = h.vec_rank !== null ? `vec=${h.vec_rank}` : 'vec=-';
        const head = `[${i + 1}] ${h.source.kind} · ${h.file_path}:${h.start_line}-${h.end_line} ` +
            `· score ${h.score.toFixed(4)} · ${fts} ${vec} · src=${h.source.id}`;
        return `${head}\n${h.content}`;
    });
    return blocks.join('\n\n---\n\n');
};
const formatAskHits = (hits, filter) => {
    if (hits.length === 0)
        return `no results${describeFilter(filter)}`;
    return hits
        .map((h, i) => {
        const fts = h.fts_rank !== null ? `fts=${h.fts_rank}` : 'fts=-';
        const vec = h.vec_rank !== null ? `vec=${h.vec_rank}` : 'vec=-';
        const head = `[${i + 1}] ${h.source.kind} · ${h.file_path}:${h.start_line}-${h.end_line} ` +
            `· score ${h.score.toFixed(4)} · ${fts} ${vec} · src=${h.source.id}`;
        const ents = h.entities.length > 0
            ? '\n--- entities ---\n' +
                h.entities
                    .map((ent) => {
                    const e = ent.entity;
                    const loc = e.line_start !== null && e.line_end !== null
                        ? `:${e.line_start}-${e.line_end}`
                        : '';
                    const out = ent.edges_out
                        .map((edge) => `  → ${edge.relation} → ${edge.to_id} (${edge.derive})`)
                        .join('\n');
                    const inb = ent.edges_in
                        .map((edge) => `  ← ${edge.relation} ← ${edge.from_id} (${edge.derive})`)
                        .join('\n');
                    const head = ent.tags.length > 0
                        ? `${e.kind} ${e.name} · ${e.id}${loc} · tags: ${ent.tags.join(', ')}`
                        : `${e.kind} ${e.name} · ${e.id}${loc}`;
                    const lines = [head, out, inb].filter((s) => s.length > 0);
                    return lines.join('\n');
                })
                    .join('\n')
            : '';
        return `${head}\n${h.content}${ents}`;
    })
        .join('\n\n---\n\n');
};
const formatPath = (result) => {
    if (!result)
        return 'no path found';
    const lines = [];
    for (let i = 0; i < result.entities.length; i++) {
        const e = result.entities[i];
        lines.push(`${i === 0 ? '◯' : '└'} ${e.kind} ${e.name} · ${e.id}`);
        if (i < result.steps.length) {
            const step = result.steps[i];
            const arrow = step.reversed ? '<-' : '->';
            lines.push(`  ${arrow}[${step.edge.relation}@${step.edge.confidence}, ${step.edge.derive}]${arrow}`);
        }
    }
    return lines.join('\n');
};
const formatGraphHits = (hits) => {
    if (hits.length === 0)
        return 'no entities';
    return hits
        .map((h, i) => {
        const e = h.entity;
        const loc = e.line_start !== null && e.line_end !== null ? `:${e.line_start}-${e.line_end}` : '';
        const src = e.source ? `${e.source}${loc}` : '(no source)';
        const rank = h.score !== null ? ` · rank ${h.score}` : '';
        const tags = h.tags.length > 0 ? ` · tags: ${h.tags.join(', ')}` : '';
        const head = `[${i + 1}] ${e.kind} ${e.name} · ${e.id} · ${src}${rank}${tags}`;
        const out = h.edges_out.length
            ? h.edges_out
                .map((e) => `  → ${e.relation} → ${e.to_id} (conf ${e.confidence}, ${e.derive})`)
                .join('\n')
            : '  (no outbound edges)';
        const inb = h.edges_in.length
            ? h.edges_in
                .map((e) => `  ← ${e.relation} ← ${e.from_id} (conf ${e.confidence}, ${e.derive})`)
                .join('\n')
            : '  (no inbound edges)';
        return `${head}\n${out}\n${inb}`;
    })
        .join('\n\n---\n\n');
};
const formatSources = (sources) => {
    if (sources.length === 0)
        return 'no indexed sources';
    return sources
        .map((s) => {
        const label = s.label ? ` — ${s.label}` : '';
        return `${s.id}\t[${s.kind}]${label}\t${s.uri}`;
    })
        .join('\n');
};
// ─── helpers ──────────────────────────────────────────────────────
const autoDetectKind = (target) => {
    if (target.startsWith('http://') || target.startsWith('https://'))
        return 'web';
    // Code-kind walks a directory tree; file-kind ingests a single file.
    // Decide by path type for the structural distinction; the only extension we
    // special-case is .pdf, since file-kind would otherwise try to read it as
    // utf-8 and produce garbage.
    if (existsSync(target) && statSync(target).isDirectory())
        return 'code';
    if (target.toLowerCase().endsWith('.pdf'))
        return 'pdf';
    return 'file';
};
const buildAddInput = (kind, target, label, include, exclude) => {
    switch (kind) {
        case 'web':
            return { kind: 'web', url: target, label };
        case 'code':
            return { kind: 'code', path: target, label, include, exclude };
        case 'file':
            return { kind: 'file', path: target, label };
        case 'text':
            return { kind: 'text', content: target, label };
        case 'pdf':
            return { kind: 'pdf', path: target, label };
    }
};
