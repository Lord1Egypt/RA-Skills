import { createHash } from 'node:crypto';
import { readFileSync, statSync } from 'node:fs';
import { basename, extname, isAbsolute, resolve } from 'node:path';
import { chunkCode, chunkText } from '../chunk.js';
import { CODE_EXTS } from '../constants/files.constants.js';
import { DOC_CONTENT_LIMIT, DOC_ENTITY_CONTEXT_LIMIT, } from '../constants/ingest.constants.js';
import { DEFAULT_MAX_INGEST_BYTES, DEFAULT_MAX_INGEST_FILES, } from '../constants/safety.constants.js';
import { buildCrossFileEdges, buildCrossSourceEdges, buildEdges, extractFromFile, } from '../extract/entity.js';
import { extractDoc } from '../extract/doc.js';
import { fetchWeb } from '../fetch.js';
import { extractPdfText } from '../pdf.js';
import { walk } from '../walk.js';
export class IngestProvider {
    db;
    embed;
    chat;
    constructor(db, embed, chat) {
        this.db = db;
        this.embed = embed;
        this.chat = chat;
    }
    assertHealthy() {
        if (!this.embed.healthy) {
            throw new Error('llm is not reachable — embeddings are unavailable.');
        }
    }
    async add(input) {
        const uri = uriFor(input);
        if (this.db.getSource(uri)) {
            throw new Error(`source already exists: ${uri} (use refresh)`);
        }
        switch (input.kind) {
            case 'web':
                return this.addWeb(input.url, input.label ?? null);
            case 'code':
                return this.addCode(input.path, input.label ?? null, input.include, input.exclude, input.force ?? false);
            case 'file':
                return this.addFile(input.path, input.label ?? null);
            case 'text':
                return this.addText(input.content, input.label ?? null);
            case 'pdf':
                return this.addPdf(input.path, input.label ?? null);
        }
    }
    async remove(ref) {
        const src = this.resolve(ref);
        this.db.deleteSource(src.id);
    }
    async refresh(ref) {
        if (ref === 'all') {
            const out = [];
            for (const s of this.db.listSources()) {
                out.push(await this.refreshOne(s));
            }
            return out;
        }
        return [await this.refreshOne(this.resolve(ref))];
    }
    async reindex(ref) {
        // Bypass the hash gate by clearing every file's hash (and doc-extracted
        // hash) before delegating to refresh. Existing rebuild semantics pick up
        // the rest, so reindex inherits clean-slate behavior for free.
        if (ref === 'all') {
            for (const s of this.db.listSources()) {
                this.db.clearFileHashes(s.id);
            }
        }
        else {
            const src = this.resolve(ref);
            this.db.clearFileHashes(src.id);
        }
        return this.refresh(ref);
    }
    async link(from, to) {
        const a = this.resolve(from);
        const b = this.resolve(to);
        this.db.addSourceLink(a.id, b.id);
        // Re-derive a's edges immediately so the new link's cross-source edges
        // appear without requiring a separate refresh.
        this.rebuildSourceEdgesById(a.id);
    }
    async unlink(from, to) {
        const a = this.resolve(from);
        const b = this.resolve(to);
        this.db.removeSourceLink(a.id, b.id);
        this.rebuildSourceEdgesById(a.id);
    }
    async links() {
        return this.db.listSourceLinks();
    }
    // ─── add per-kind ────────────────────────────────────────────────
    async addWeb(url, label) {
        const fetched = await fetchWeb(url);
        const src = this.insertSource('web', url, label ?? fetched.title);
        return await this.indexSingle(src.id, urlPath(url), fetched.text, 'text');
    }
    async addCode(path, label, include, exclude, force) {
        const abs = absDir(path);
        assertAllowedRoot(abs);
        const rels = walk(abs, { include, exclude });
        if (!force)
            assertSizeWithinLimits(abs, rels);
        const src = this.insertSource('code', abs, label ?? basename(abs));
        let filesIndexed = 0;
        let chunksCreated = 0;
        for (const rel of rels) {
            const r = await this.indexCodeFile(src.id, abs, rel);
            if (r.changed) {
                filesIndexed++;
                chunksCreated += r.chunks;
            }
        }
        const knownPaths = this.db.listFiles(src.id).map((f) => f.path);
        this.rebuildSourceEdges(abs, rels, knownPaths, src.id);
        this.cascadeRebuildLinkedFrom(src.id);
        await this.runDocExtractionPass(src.id, abs, rels);
        this.db.touchSource(src.id, Date.now());
        return { source_id: src.id, files_indexed: filesIndexed, chunks_created: chunksCreated };
    }
    async addFile(path, label) {
        const abs = absFile(path);
        assertAllowedRoot(abs);
        const src = this.insertSource('file', abs, label ?? basename(abs));
        const content = readFileSync(abs, 'utf8');
        const mode = isCodeExt(abs) ? 'code' : 'text';
        return await this.indexSingle(src.id, basename(abs), content, mode);
    }
    async addText(content, label) {
        const uri = `text:${sha256(content)}`;
        const src = this.insertSource('text', uri, label);
        return await this.indexSingle(src.id, 'content', content, 'text');
    }
    async addPdf(path, label) {
        const abs = absFile(path);
        assertAllowedRoot(abs);
        const buffer = readFileSync(abs);
        const { text } = await extractPdfText(buffer);
        const src = this.insertSource('pdf', abs, label ?? basename(abs));
        return await this.indexSingle(src.id, basename(abs), text, 'text');
    }
    // ─── refresh ─────────────────────────────────────────────────────
    async refreshOne(src) {
        let changed = 0;
        let unchanged = 0;
        let chunksCreated = 0;
        let chunksDeleted = 0;
        if (src.kind === 'web') {
            const fetched = await fetchWeb(src.uri);
            const r = await this.refreshSingle(src.id, urlPath(src.uri), fetched.text, 'text');
            changed = r.changed ? 1 : 0;
            unchanged = r.changed ? 0 : 1;
            chunksCreated = r.chunks;
            chunksDeleted = r.deleted;
        }
        else if (src.kind === 'code') {
            const rels = walk(src.uri);
            const seen = new Set(rels);
            for (const rel of rels) {
                const r = await this.indexCodeFile(src.id, src.uri, rel);
                if (r.changed) {
                    changed++;
                    chunksCreated += r.chunks;
                }
                else
                    unchanged++;
            }
            // Snapshot paths BEFORE deleteFilesNotIn so the rebuild can soft-delete
            // entities that lived in files removed this run.
            const knownPaths = this.db.listFiles(src.id).map((f) => f.path);
            const dropped = this.db.deleteFilesNotIn(src.id, [...seen]);
            chunksDeleted += dropped.length;
            this.rebuildSourceEdges(src.uri, rels, knownPaths, src.id);
            this.cascadeRebuildLinkedFrom(src.id);
            await this.runDocExtractionPass(src.id, src.uri, rels);
        }
        else if (src.kind === 'file') {
            const content = readFileSync(src.uri, 'utf8');
            const mode = isCodeExt(src.uri) ? 'code' : 'text';
            const r = await this.refreshSingle(src.id, basename(src.uri), content, mode);
            changed = r.changed ? 1 : 0;
            unchanged = r.changed ? 0 : 1;
            chunksCreated = r.chunks;
            chunksDeleted = r.deleted;
        }
        else if (src.kind === 'pdf') {
            const buffer = readFileSync(src.uri);
            const { text } = await extractPdfText(buffer);
            const r = await this.refreshSingle(src.id, basename(src.uri), text, 'text');
            changed = r.changed ? 1 : 0;
            unchanged = r.changed ? 0 : 1;
            chunksCreated = r.chunks;
            chunksDeleted = r.deleted;
        }
        // 'text' is content-addressed; refresh is a no-op beyond touching the source.
        this.db.touchSource(src.id, Date.now());
        return {
            source_id: src.id,
            files_changed: changed,
            files_unchanged: unchanged,
            chunks_created: chunksCreated,
            chunks_deleted: chunksDeleted,
        };
    }
    // ─── helpers ─────────────────────────────────────────────────────
    insertSource(kind, uri, label) {
        return this.db.insertSource({
            kind,
            uri,
            label,
            embed_model: this.embed.model,
            ts: Date.now(),
        });
    }
    resolve(ref) {
        const src = this.db.getSource(ref);
        if (!src)
            throw new Error(`source not found: ${ref}`);
        return src;
    }
    async indexSingle(source_id, path, content, mode) {
        const r = await this.indexFileContent(source_id, path, content, mode);
        if (r.changed && mode === 'code') {
            const entities = await this.indexEntities(source_id, path, content);
            this.rebuildSingleFileEdges(source_id, path, entities, content);
        }
        return {
            source_id,
            files_indexed: r.changed ? 1 : 0,
            chunks_created: r.chunks,
        };
    }
    async refreshSingle(source_id, path, content, mode) {
        const r = await this.indexFileContent(source_id, path, content, mode);
        if (r.changed && mode === 'code') {
            const entities = await this.indexEntities(source_id, path, content);
            this.rebuildSingleFileEdges(source_id, path, entities, content);
        }
        return r;
    }
    async indexCodeFile(source_id, rootAbs, rel) {
        const abs = `${rootAbs}/${rel}`;
        let content;
        try {
            content = readFileSync(abs, 'utf8');
        }
        catch {
            return { changed: false, chunks: 0, deleted: 0 };
        }
        const mode = isCodeExt(rel) ? 'code' : 'text';
        const r = await this.indexFileContent(source_id, rel, content, mode);
        // Multi-file source: only entity upsert here. Edge rebuild happens once
        // per source in `rebuildSourceEdges` so the global name map is complete.
        if (r.changed && mode === 'code') {
            await this.indexEntities(source_id, rel, content);
        }
        return r;
    }
    async indexFileContent(source_id, path, content, mode) {
        this.assertHealthy();
        const hash = sha256(content);
        const mtime = Date.now();
        const lang = mode === 'code' ? extname(path).slice(1) || null : null;
        const upserted = this.db.upsertFile({ source_id, path, hash, mtime, lang });
        if (!upserted.changed)
            return { changed: false, chunks: 0, deleted: 0 };
        const before = this.db.listFiles(source_id).find((f) => f.id === upserted.file_id);
        const previouslyHadChunks = before !== undefined; // best-effort: we re-chunk on any change
        const chunks = mode === 'code' ? chunkCode(content) : chunkText(content);
        if (chunks.length === 0) {
            this.db.deleteChunksForFile(upserted.file_id);
            return { changed: true, chunks: 0, deleted: previouslyHadChunks ? 1 : 0 };
        }
        const embeddings = await this.embed.embedBatch(chunks.map((c) => c.content));
        this.db.replaceChunks(upserted.file_id, chunks, embeddings);
        return { changed: true, chunks: chunks.length, deleted: 0 };
    }
    // Embeds + upserts entities for a single file. No edge work — callers run
    // the appropriate edge rebuild. Returns entities with source-namespaced ids
    // so caller-side edge builders see the canonical ids the DB now stores.
    async indexEntities(source_id, filePath, content) {
        const bare = extractFromFile(content, filePath).entities;
        if (bare.length === 0)
            return bare;
        const extracted = bare.map((e) => ({
            ...e,
            id: namespaceId(source_id, e.id),
        }));
        // 200-char prefix is a placeholder description — fine for now since the
        // entity-search KNN ranks by name proximity in practice.
        const descriptions = extracted.map(() => content.slice(0, 200));
        const embeddings = await this.embed.embedBatch(descriptions);
        const newEmbeddings = new Map();
        for (let i = 0; i < extracted.length; i++) {
            newEmbeddings.set(extracted[i].id, embeddings[i]);
        }
        // better-sqlite3 transaction() requires a sync body — async would commit
        // before any upserts ran.
        const tx = this.db.rawDb.transaction(() => {
            for (const entity of extracted) {
                this.db.upsertEntity({
                    id: entity.id,
                    source_id,
                    kind: entity.kind,
                    name: entity.name,
                    source: filePath,
                    line_start: entity.line_start,
                    line_end: entity.line_end,
                    embedding: newEmbeddings.get(entity.id),
                });
            }
        });
        tx();
        return extracted;
    }
    // Per-file rebuild for single-file code sources (addFile / refresh-file).
    rebuildSingleFileEdges(source_id, filePath, entities, content) {
        const keepIds = new Set(entities.map((e) => e.id));
        this.db.softDeleteMissingEntities(filePath, keepIds);
        this.db.deleteParseEdgesForSources([filePath]);
        if (entities.length === 0)
            return;
        const fresh = extractFromFile(content, filePath);
        const file = {
            filePath,
            content,
            entities: ensureNamespaced(source_id, entities),
            fnCalls: namespaceMapKeys(source_id, fresh.fnCalls),
            fnRefs: namespaceMapKeys(source_id, fresh.fnRefs),
        };
        const edges = buildEdges(file);
        if (edges.length > 0)
            this.db.upsertEdges(edges);
    }
    // Source-wide rebuild for code sources. Runs after pass 1 has chunked +
    // upserted entities for every (changed) file. Re-extracts each file with
    // tree-sitter to get a global name map, soft-deletes entities that vanished
    // anywhere in the source, wipes parse edges from any known path, then
    // re-emits intra + cross-file + cross-source parse edges in one shot.
    // Doc-derived edges are untouched — that layer rebuilds itself.
    rebuildSourceEdges(rootAbs, rels, knownPaths, source_id) {
        const perFile = [];
        for (const rel of rels) {
            if (!isCodeExt(rel))
                continue;
            let content;
            try {
                content = readFileSync(`${rootAbs}/${rel}`, 'utf8');
            }
            catch {
                continue;
            }
            const fresh = extractFromFile(content, rel);
            const entities = source_id !== undefined
                ? fresh.entities.map((e) => ({ ...e, id: namespaceId(source_id, e.id) }))
                : fresh.entities;
            const fnCalls = source_id !== undefined ? namespaceMapKeys(source_id, fresh.fnCalls) : fresh.fnCalls;
            const fnRefs = source_id !== undefined ? namespaceMapKeys(source_id, fresh.fnRefs) : fresh.fnRefs;
            perFile.push({ filePath: rel, content, entities, fnCalls, fnRefs });
        }
        const newIdsByPath = new Map();
        for (const f of perFile)
            newIdsByPath.set(f.filePath, new Set(f.entities.map((e) => e.id)));
        for (const path of knownPaths) {
            this.db.softDeleteMissingEntities(path, newIdsByPath.get(path) ?? new Set());
        }
        if (knownPaths.length > 0)
            this.db.deleteParseEdgesForSources(knownPaths);
        const edges = [];
        for (const f of perFile) {
            if (f.entities.length === 0)
                continue;
            edges.push(...buildEdges(f));
        }
        edges.push(...buildCrossFileEdges(perFile));
        if (source_id !== undefined) {
            const external = this.collectExternalEntities(source_id);
            if (external.size > 0)
                edges.push(...buildCrossSourceEdges(perFile, external));
        }
        if (edges.length > 0)
            this.db.upsertEdges(edges);
    }
    // Build a name → entity map from all sources this source links TO. Skips
    // ambiguous names (same bare name in multiple linked sources).
    collectExternalEntities(source_id) {
        const linkedTo = this.db.getSourcesLinkedFrom(source_id);
        if (linkedTo.length === 0)
            return new Map();
        const byName = new Map();
        const ambiguous = new Set();
        for (const targetId of linkedTo) {
            for (const e of this.db.getActiveEntitiesForSource(targetId)) {
                if (e.kind !== 'function' && e.kind !== 'struct' && e.kind !== 'enum' && e.kind !== 'constant')
                    continue;
                if (ambiguous.has(e.name))
                    continue;
                const prev = byName.get(e.name);
                if (prev && prev.id !== e.id) {
                    ambiguous.add(e.name);
                    byName.delete(e.name);
                    continue;
                }
                byName.set(e.name, {
                    id: e.id,
                    kind: e.kind,
                    name: e.name,
                    line_start: e.line_start ?? 0,
                    line_end: e.line_end ?? 0,
                });
            }
        }
        return byName;
    }
    // Cascade-rebuild edges for every source that links TO `to_id`.
    cascadeRebuildLinkedFrom(to_id) {
        for (const fromId of this.db.getSourcesLinkingTo(to_id)) {
            this.rebuildSourceEdgesById(fromId);
        }
    }
    rebuildSourceEdgesById(source_id) {
        const src = this.db.getSource(source_id);
        if (!src || src.kind !== 'code')
            return;
        const knownPaths = this.db.listFiles(source_id).map((f) => f.path);
        const rels = walk(src.uri);
        this.rebuildSourceEdges(src.uri, rels, knownPaths, source_id);
    }
    // Doc-extraction LLM pass. For each markdown file in this code source:
    // skip if hash matches the last successful extraction, call the chat model
    // with the doc + code-entity context, resolve concept names to ids, rebuild
    // this doc's `derive='doc'` edges. Failures are logged and tolerated:
    // chunk indexing already succeeded; the doc layer is best-effort enrichment.
    async runDocExtractionPass(source_id, rootAbs, rels) {
        if (!this.chat)
            return;
        const docs = rels.filter((r) => extname(r).toLowerCase() === '.md');
        if (docs.length === 0)
            return;
        if (!(await this.chat.healthCheck())) {
            console.warn(`cairn: chat model "${this.chat.model}" not reachable — skipping doc-extraction (${docs.length} file(s)). \`ollama pull ${this.chat.model}\` to enable.`);
            return;
        }
        const codeEntities = this.collectCodeEntities(source_id);
        for (const rel of docs) {
            const fileRow = this.db.getFile(source_id, rel);
            if (!fileRow)
                continue;
            const lastHash = this.db.getDocExtractedHash(fileRow.id);
            if (lastHash === fileRow.hash)
                continue;
            let content;
            try {
                content = readFileSync(`${rootAbs}/${rel}`, 'utf8');
            }
            catch {
                continue;
            }
            const truncated = content.slice(0, DOC_CONTENT_LIMIT);
            let resolved;
            try {
                const out = await extractDoc(this.chat, {
                    docPath: rel,
                    docContent: truncated,
                    codeEntities,
                    source_id,
                });
                resolved = out.resolved;
            }
            catch (e) {
                console.warn(`cairn: doc-extract failed on ${rel}: ${e.message}. leaving prior edges intact.`);
                continue;
            }
            if (process.env.CAIRN_DEBUG_DOC) {
                console.log(`cairn: doc-extract ${rel} → concepts=${resolved.concepts.length} edges=${resolved.edges.length} dropped=${resolved.dropped}`);
            }
            await this.applyDocExtraction(source_id, rel, resolved);
            this.db.setDocExtractedHash(fileRow.id, fileRow.hash);
        }
    }
    // Apply a resolved extraction to the DB: rebuild this doc's concept entities
    // and `derive='doc'` edges from scratch.
    async applyDocExtraction(source_id, docPath, resolved) {
        const keepIds = new Set(resolved.concepts.map((c) => c.id));
        this.db.softDeleteMissingEntities(docPath, keepIds);
        this.db.deleteDocEdgesForSource(docPath);
        if (resolved.concepts.length > 0) {
            // Embed the concept's description (or its name as a fallback) plus its
            // tags as a small framing cue — `[tags: attack, mev]`. Lets KNN find
            // tagged concepts on tag-keyword queries even when the surrounding
            // doc text doesn't literally contain the tag word.
            const inputs = resolved.concepts.map((c) => {
                const base = c.description ?? `${c.name} (concept from ${docPath})`;
                return c.tags.length > 0 ? `${base} [tags: ${c.tags.join(', ')}]` : base;
            });
            const embeddings = await this.embed.embedBatch(inputs);
            const tx = this.db.rawDb.transaction(() => {
                for (let i = 0; i < resolved.concepts.length; i++) {
                    const c = resolved.concepts[i];
                    this.db.upsertEntity({
                        id: c.id,
                        source_id,
                        kind: 'concept',
                        name: c.name,
                        source: docPath,
                        line_start: null,
                        line_end: null,
                        embedding: embeddings[i],
                    });
                    // Replace tag set per concept — doc-extract is the source of truth
                    // for this doc's tags. Same model as edge rebuild.
                    this.db.replaceEntityTags(c.id, c.tags);
                }
            });
            tx();
        }
        if (resolved.edges.length > 0) {
            this.db.upsertEdges(resolved.edges.map((e) => ({
                from_id: e.from_id,
                to_id: e.to_id,
                relation: e.relation,
                confidence: e.confidence,
                derive: 'doc',
            })));
        }
    }
    // Collect code entities (function/struct/enum/constant) for use as edge
    // endpoints in the LLM prompt. Capped to keep prompt size bounded.
    collectCodeEntities(source_id) {
        const out = [];
        const codeKinds = new Set(['function', 'struct', 'enum', 'constant']);
        for (const f of this.db.listFiles(source_id)) {
            const ents = this.db.getEntitiesBySource(f.path);
            for (const e of ents) {
                if (!codeKinds.has(e.kind))
                    continue;
                out.push({ id: e.id, kind: e.kind, name: e.name });
                if (out.length >= DOC_ENTITY_CONTEXT_LIMIT)
                    return out;
            }
        }
        return out;
    }
}
// ─── module helpers ────────────────────────────────────────────────
const uriFor = (input) => {
    switch (input.kind) {
        case 'web':
            return input.url;
        case 'code':
            return absDir(input.path);
        case 'file':
            return absFile(input.path);
        case 'text':
            return `text:${sha256(input.content)}`;
        case 'pdf':
            return absFile(input.path);
    }
};
const absDir = (path) => {
    const abs = isAbsolute(path) ? path : resolve(process.cwd(), path);
    const st = statSync(abs);
    if (!st.isDirectory()) {
        throw new Error(`not a directory: ${abs}`);
    }
    return abs;
};
const absFile = (path) => {
    const abs = isAbsolute(path) ? path : resolve(process.cwd(), path);
    const st = statSync(abs);
    if (!st.isFile()) {
        throw new Error(`not a file: ${abs}`);
    }
    return abs;
};
const urlPath = (url) => {
    try {
        const u = new URL(url);
        return u.pathname || '/';
    }
    catch {
        return url;
    }
};
const isCodeExt = (path) => CODE_EXTS.has(extname(path).toLowerCase());
const sha256 = (s) => createHash('sha256').update(s).digest('hex');
// Prepend `source_id:` to a bare entity id (`<filepath>:<name>`). Idempotent
// when applied to an already-namespaced id from the same source.
const namespaceId = (source_id, bareId) => {
    const prefix = `${source_id}:`;
    return bareId.startsWith(prefix) ? bareId : `${prefix}${bareId}`;
};
const ensureNamespaced = (source_id, entities) => entities.map((e) => ({ ...e, id: namespaceId(source_id, e.id) }));
// Rewrite the keys of a per-fn data map (calls / refs) with namespaced ids.
// Values are sets of bare callee/ref names — looked up against entity-name maps
// in the edge layer, so they stay unchanged.
const namespaceMapKeys = (source_id, m) => {
    const out = new Map();
    for (const [k, v] of m) {
        out.set(namespaceId(source_id, k), v);
    }
    return out;
};
// ─── safety gates (CAIRN_ALLOWED_ROOTS, size caps) ─────────────────
// Defense-in-depth path allowlist. When CAIRN_ALLOWED_ROOTS is set
// (comma-separated absolute paths), `cairn add` rejects any local-path
// ingestion outside those roots. Unset = no restriction (default).
// Real protection is host-side MCP per-call approval; this is the belt.
const assertAllowedRoot = (abs) => {
    const raw = process.env.CAIRN_ALLOWED_ROOTS;
    if (!raw || raw.trim().length === 0)
        return;
    const roots = raw
        .split(',')
        .map((s) => s.trim().replace(/\/+$/, ''))
        .filter((s) => s.length > 0);
    if (roots.length === 0)
        return;
    const ok = roots.some((root) => abs === root || abs.startsWith(root + '/'));
    if (!ok) {
        throw new Error(`cairn: path "${abs}" is not under any CAIRN_ALLOWED_ROOTS entry. ` +
            `Allowed roots: ${roots.join(', ')}`);
    }
};
// Size-cap pre-check on directory ingestion. Aborts before any chunking /
// embedding work happens. Bypassable via CLI `--force` (passed through to
// AddInput.force) or by raising the env-var thresholds. MCP intentionally
// does not expose `force` — host-side approval is the override path there.
const assertSizeWithinLimits = (abs, rels) => {
    const maxFiles = Number(process.env.CAIRN_MAX_INGEST_FILES ?? DEFAULT_MAX_INGEST_FILES);
    if (rels.length > maxFiles) {
        throw new Error(`cairn: directory "${abs}" contains ${rels.length} files, ` +
            `exceeds CAIRN_MAX_INGEST_FILES=${maxFiles}. ` +
            `Pass --force on CLI, raise the limit, or narrow with --include / --exclude.`);
    }
    const maxBytes = Number(process.env.CAIRN_MAX_INGEST_BYTES ?? DEFAULT_MAX_INGEST_BYTES);
    let total = 0;
    for (const rel of rels) {
        try {
            total += statSync(`${abs}/${rel}`).size;
        }
        catch {
            // unreadable file — count as 0; the indexer will skip it later anyway.
        }
    }
    if (total > maxBytes) {
        const mb = (total / 1024 / 1024).toFixed(0);
        const capMb = (maxBytes / 1024 / 1024).toFixed(0);
        throw new Error(`cairn: directory "${abs}" totals ${mb}MB, exceeds CAIRN_MAX_INGEST_BYTES=${capMb}MB. ` +
            `Pass --force on CLI, raise the limit, or narrow with --include / --exclude.`);
    }
};
