import { mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import Database from 'better-sqlite3';
import * as sqliteVec from 'sqlite-vec';
import { SCHEMA, VEC_OVERFETCH } from '../schema.js';
export class DbProvider {
    db;
    // sources
    sInsertSource;
    sGetSourceById;
    sGetSourceByUri;
    sListSources;
    sListSourcesByKind;
    sDeleteSource;
    sTouchSource;
    // files
    sInsertFile;
    sGetFile;
    sUpdateFileChanged;
    sUpdateFileMtime;
    sListFiles;
    sDeleteFilesNotIn;
    sClearFileHashes;
    // chunks
    sInsertChunk;
    sDeleteChunksByFile;
    // vec
    sInsertVec;
    // search
    sSearchFts;
    sSearchFtsBySource;
    sSearchFtsByKind;
    sSearchVec;
    sSearchVecBySource;
    sSearchVecByKind;
    // hydrate (narrow seeks via json_each)
    sChunksByIds;
    sFilesByIds;
    sSourcesByIds;
    // graph — entities
    sUpsertEntity;
    sGetEntity;
    sGetEntitiesBySource;
    sSoftDeleteEntity;
    sDeleteEntity;
    sUpdateEntityLineRange;
    // graph — edges
    sInsertEdge;
    sGetEdges;
    sGetEdgesInbound;
    sGetEdgesForMany;
    sGetEdgesInboundForMany;
    sDeleteParseEdgesForPaths;
    sDeleteDocEdgesForPath;
    sListEntitiesBySourceWithRowid;
    sGetDocExtractedHash;
    sSetDocExtractedHash;
    // graph — cross-source links
    sAddSourceLink;
    sRemoveSourceLink;
    sListSourceLinks;
    sGetSourcesLinkedFrom;
    sGetSourcesLinkingTo;
    sGetActiveEntitiesForSource;
    // graph — vec
    sInsertEntityVec;
    sUpdateEntityVec;
    sDeleteEntityVec;
    sSearchEntityVec;
    // tags (v1.1)
    sDeleteTagsForEntity;
    sInsertTag;
    sGetTagsForEntity;
    sGetTagsForMany;
    sGetEntitiesByTag;
    sListTags;
    constructor(dbPath) {
        mkdirSync(dirname(dbPath), { recursive: true });
        this.db = new Database(dbPath);
        this.db.pragma('journal_mode = WAL');
        this.db.pragma('foreign_keys = ON');
        sqliteVec.load(this.db);
        this.db.exec(SCHEMA);
        this.sInsertSource = this.db.prepare(`INSERT INTO sources (kind, uri, label, embed_model, added_at, last_indexed_at)
       VALUES (@kind, @uri, @label, @embed_model, @ts, @ts)
       RETURNING *`);
        this.sGetSourceById = this.db.prepare(`SELECT * FROM sources WHERE id = ?`);
        this.sGetSourceByUri = this.db.prepare(`SELECT * FROM sources WHERE uri = ?`);
        this.sListSources = this.db.prepare(`SELECT * FROM sources ORDER BY added_at DESC`);
        this.sListSourcesByKind = this.db.prepare(`SELECT * FROM sources WHERE kind = ? ORDER BY added_at DESC`);
        this.sDeleteSource = this.db.prepare(`DELETE FROM sources WHERE id = ?`);
        this.sTouchSource = this.db.prepare(`UPDATE sources SET last_indexed_at = ? WHERE id = ?`);
        this.sInsertFile = this.db.prepare(`INSERT INTO files (source_id, path, hash, mtime, lang)
       VALUES (@source_id, @path, @hash, @mtime, @lang)`);
        this.sGetFile = this.db.prepare(`SELECT * FROM files WHERE source_id = ? AND path = ?`);
        this.sUpdateFileChanged = this.db.prepare(`UPDATE files SET hash = @hash, mtime = @mtime, lang = @lang WHERE id = @id`);
        this.sUpdateFileMtime = this.db.prepare(`UPDATE files SET mtime = ? WHERE id = ?`);
        this.sListFiles = this.db.prepare(`SELECT * FROM files WHERE source_id = ?`);
        this.sDeleteFilesNotIn = this.db.prepare(`DELETE FROM files
       WHERE source_id = ?
         AND path NOT IN (SELECT value FROM json_each(?))
       RETURNING id`);
        // Force-rebuild path: zero hashes so the next refresh sees every file as
        // changed. doc_extracted_hash → NULL so the LLM doc pass re-runs too.
        this.sClearFileHashes = this.db.prepare(`UPDATE files SET hash = '', doc_extracted_hash = NULL WHERE source_id = ?`);
        this.sInsertChunk = this.db.prepare(`INSERT INTO chunks (file_id, content, start_line, end_line)
       VALUES (@file_id, @content, @start_line, @end_line)`);
        this.sDeleteChunksByFile = this.db.prepare(`DELETE FROM chunks WHERE file_id = ?`);
        this.sInsertVec = this.db.prepare(`INSERT INTO chunks_vec (rowid, embedding) VALUES (?, ?)`);
        // FTS5: MATCH binds to the table or a column — aliases aren't accepted on the LHS.
        this.sSearchFts = this.db.prepare(`SELECT c.id AS chunk_id
       FROM chunks_fts fts JOIN chunks c ON c.id = fts.rowid
       WHERE fts.content MATCH ?
       ORDER BY fts.rank LIMIT ?`);
        this.sSearchFtsBySource = this.db.prepare(`SELECT c.id AS chunk_id
       FROM chunks_fts fts
       JOIN chunks c ON c.id = fts.rowid
       JOIN files f ON f.id = c.file_id
       WHERE fts.content MATCH ? AND f.source_id = ?
       ORDER BY fts.rank LIMIT ?`);
        this.sSearchFtsByKind = this.db.prepare(`SELECT c.id AS chunk_id
       FROM chunks_fts fts
       JOIN chunks c ON c.id = fts.rowid
       JOIN files f ON f.id = c.file_id
       JOIN sources s ON s.id = f.source_id
       WHERE fts.content MATCH ? AND s.kind = ?
       ORDER BY fts.rank LIMIT ?`);
        // vec0 requires `k = ?` directly on the KNN — not LIMIT after a JOIN.
        this.sSearchVec = this.db.prepare(`SELECT rowid AS chunk_id
       FROM chunks_vec
       WHERE embedding MATCH ? AND k = ?
       ORDER BY distance`);
        this.sSearchVecBySource = this.db.prepare(`WITH knn AS (
          SELECT rowid AS chunk_id, distance
          FROM chunks_vec
          WHERE embedding MATCH ? AND k = ?
        )
        SELECT knn.chunk_id AS chunk_id
        FROM knn
        JOIN chunks c ON c.id = knn.chunk_id
        JOIN files f ON f.id = c.file_id
        WHERE f.source_id = ?
        ORDER BY knn.distance LIMIT ?`);
        this.sSearchVecByKind = this.db.prepare(`WITH knn AS (
          SELECT rowid AS chunk_id, distance
          FROM chunks_vec
          WHERE embedding MATCH ? AND k = ?
        )
        SELECT knn.chunk_id AS chunk_id
        FROM knn
        JOIN chunks c ON c.id = knn.chunk_id
        JOIN files f ON f.id = c.file_id
        JOIN sources s ON s.id = f.source_id
        WHERE s.kind = ?
        ORDER BY knn.distance LIMIT ?`);
        // hydrate: three narrow seeks via json_each, no big JOIN.
        this.sChunksByIds = this.db.prepare(`SELECT * FROM chunks WHERE id IN (SELECT value FROM json_each(?))`);
        this.sFilesByIds = this.db.prepare(`SELECT * FROM files WHERE id IN (SELECT value FROM json_each(?))`);
        this.sSourcesByIds = this.db.prepare(`SELECT * FROM sources WHERE id IN (SELECT value FROM json_each(?))`);
        // ─── graph prepared statements ─────────────────────────────────
        this.sUpsertEntity = this.db.prepare(`INSERT INTO entities (id, source_id, kind, name, source, line_start, line_end, created_at, removed_at)
       VALUES (@id, @source_id, @kind, @name, @source, @line_start, @line_end, @created_at, @removed_at)
       ON CONFLICT(id) DO UPDATE SET
         source_id = excluded.source_id,
         kind = excluded.kind,
         name = excluded.name,
         source = excluded.source,
         line_start = excluded.line_start,
         line_end = excluded.line_end,
         removed_at = NULL
       RETURNING rowid, (SELECT id FROM entities WHERE rowid = last_insert_rowid()) AS id`);
        this.sGetEntity = this.db.prepare(`SELECT * FROM entities WHERE id = ? AND removed_at IS NULL`);
        this.sGetEntitiesBySource = this.db.prepare(`SELECT * FROM entities WHERE source = ? AND removed_at IS NULL`);
        this.sSoftDeleteEntity = this.db.prepare(`UPDATE entities SET removed_at = ? WHERE id = ?`);
        this.sDeleteEntity = this.db.prepare(`DELETE FROM entities WHERE id = ?`);
        this.sUpdateEntityLineRange = this.db.prepare(`UPDATE entities SET line_start = ?, line_end = ?, removed_at = NULL WHERE id = ?`);
        this.sInsertEdge = this.db.prepare(`INSERT OR IGNORE INTO edges (from_id, to_id, relation, confidence, derive)
       VALUES (@from_id, @to_id, @relation, @confidence, @derive)`);
        // Edge queries JOIN entities on both endpoints and filter active.
        // Soft-deleted entities hide their edges without touching the edges table.
        this.sGetEdges = this.db.prepare(`SELECT e.* FROM edges e
       INNER JOIN entities ef ON ef.id = e.from_id AND ef.removed_at IS NULL
       INNER JOIN entities et ON et.id = e.to_id   AND et.removed_at IS NULL
       WHERE e.from_id = ?`);
        this.sGetEdgesInbound = this.db.prepare(`SELECT e.* FROM edges e
       INNER JOIN entities ef ON ef.id = e.from_id AND ef.removed_at IS NULL
       INNER JOIN entities et ON et.id = e.to_id   AND et.removed_at IS NULL
       WHERE e.to_id = ?`);
        // Batched layer fetches for BFS and ask() — one round trip per call.
        this.sGetEdgesForMany = this.db.prepare(`SELECT e.* FROM edges e
       INNER JOIN entities ef ON ef.id = e.from_id AND ef.removed_at IS NULL
       INNER JOIN entities et ON et.id = e.to_id   AND et.removed_at IS NULL
       WHERE e.from_id IN (SELECT value FROM json_each(?))`);
        this.sGetEdgesInboundForMany = this.db.prepare(`SELECT e.* FROM edges e
       INNER JOIN entities ef ON ef.id = e.from_id AND ef.removed_at IS NULL
       INNER JOIN entities et ON et.id = e.to_id   AND et.removed_at IS NULL
       WHERE e.to_id IN (SELECT value FROM json_each(?))`);
        // Rebuild path: wipe parse edges whose from_id lives in any of the given
        // file paths. Doc-derived edges (`derive = 'doc'`) are deliberately preserved.
        this.sDeleteParseEdgesForPaths = this.db.prepare(`DELETE FROM edges
       WHERE derive = 'parse'
         AND from_id IN (
           SELECT id FROM entities WHERE source IN (SELECT value FROM json_each(?))
         )`);
        this.sListEntitiesBySourceWithRowid = this.db.prepare(`SELECT id, rowid FROM entities WHERE source = ? AND removed_at IS NULL`);
        // Doc-extraction rebuild: wipe doc edges whose from_id lives in this doc.
        this.sDeleteDocEdgesForPath = this.db.prepare(`DELETE FROM edges
       WHERE derive = 'doc'
         AND from_id IN (SELECT id FROM entities WHERE source = ?)`);
        this.sGetDocExtractedHash = this.db.prepare(`SELECT doc_extracted_hash FROM files WHERE id = ?`);
        this.sSetDocExtractedHash = this.db.prepare(`UPDATE files SET doc_extracted_hash = ? WHERE id = ?`);
        // ─── source-link statements ──────────────────────────────────────
        this.sAddSourceLink = this.db.prepare(`INSERT OR IGNORE INTO source_links (source_a, source_b) VALUES (?, ?)`);
        this.sRemoveSourceLink = this.db.prepare(`DELETE FROM source_links WHERE source_a = ? AND source_b = ?`);
        this.sListSourceLinks = this.db.prepare(`SELECT source_a, source_b FROM source_links ORDER BY source_a, source_b`);
        this.sGetSourcesLinkedFrom = this.db.prepare(`SELECT source_b FROM source_links WHERE source_a = ?`);
        this.sGetSourcesLinkingTo = this.db.prepare(`SELECT source_a FROM source_links WHERE source_b = ?`);
        this.sGetActiveEntitiesForSource = this.db.prepare(`SELECT * FROM entities WHERE source_id = ? AND removed_at IS NULL`);
        this.sInsertEntityVec = this.db.prepare(`INSERT INTO entities_vec (entity_rowid, embedding) VALUES (?, ?)`);
        this.sUpdateEntityVec = this.db.prepare(`UPDATE entities_vec SET embedding = ? WHERE entity_rowid = ?`);
        this.sDeleteEntityVec = this.db.prepare(`DELETE FROM entities_vec WHERE entity_rowid = ?`);
        this.sSearchEntityVec = this.db.prepare(`SELECT e.* FROM entities e
       JOIN entities_vec ev ON ev.entity_rowid = e.rowid
       WHERE ev.embedding MATCH ? AND k = ?
         AND e.removed_at IS NULL
       ORDER BY ev.distance`);
        // ─── tag prepared stmts (v1.1) ───────────────────────────────
        this.sDeleteTagsForEntity = this.db.prepare(`DELETE FROM entity_tags WHERE entity_id = ?`);
        this.sInsertTag = this.db.prepare(`INSERT OR IGNORE INTO entity_tags (entity_id, tag) VALUES (?, ?)`);
        this.sGetTagsForEntity = this.db.prepare(`SELECT tag FROM entity_tags WHERE entity_id = ? ORDER BY tag`);
        this.sGetTagsForMany = this.db.prepare(`SELECT entity_id, tag FROM entity_tags
       WHERE entity_id IN (SELECT value FROM json_each(?))`);
        // Active entities only — soft-deleted entities keep their tag rows but
        // shouldn't surface in tag-driven discovery.
        this.sGetEntitiesByTag = this.db.prepare(`SELECT e.* FROM entities e
       JOIN entity_tags t ON t.entity_id = e.id
       WHERE t.tag = ? AND e.removed_at IS NULL
       LIMIT ?`);
        // Counts active entities per tag — same active-only filter as above.
        this.sListTags = this.db.prepare(`SELECT t.tag AS tag, COUNT(*) AS count
       FROM entity_tags t
       JOIN entities e ON e.id = t.entity_id
       WHERE e.removed_at IS NULL
       GROUP BY t.tag
       ORDER BY count DESC, t.tag ASC`);
    }
    // ─── sources ──────────────────────────────────────────────────────
    insertSource(input) {
        return this.sInsertSource.get(input);
    }
    getSource(ref) {
        const row = typeof ref === 'number' ? this.sGetSourceById.get(ref) : this.sGetSourceByUri.get(ref);
        return row ?? null;
    }
    listSources(filter) {
        if (filter?.kind)
            return this.sListSourcesByKind.all(filter.kind);
        return this.sListSources.all();
    }
    deleteSource(id) {
        this.sDeleteSource.run(id);
    }
    touchSource(id, ts) {
        this.sTouchSource.run(ts, id);
    }
    // ─── files ────────────────────────────────────────────────────────
    upsertFile(input) {
        const existing = this.sGetFile.get(input.source_id, input.path);
        if (!existing) {
            const r = this.sInsertFile.run(input);
            return { file_id: r.lastInsertRowid, changed: true };
        }
        if (existing.hash === input.hash) {
            this.sUpdateFileMtime.run(input.mtime, existing.id);
            return { file_id: existing.id, changed: false };
        }
        this.sUpdateFileChanged.run({
            id: existing.id,
            hash: input.hash,
            mtime: input.mtime,
            lang: input.lang,
        });
        return { file_id: existing.id, changed: true };
    }
    getFile(source_id, path) {
        return this.sGetFile.get(source_id, path) ?? null;
    }
    listFiles(source_id) {
        return this.sListFiles.all(source_id);
    }
    deleteFilesNotIn(source_id, paths) {
        // FK cascade nukes chunks; chunks_av trigger nukes chunks_vec; chunks_ad trigger nukes fts.
        const keep = JSON.stringify(paths);
        const rows = this.sDeleteFilesNotIn.all(source_id, keep);
        return rows.map((r) => r.id);
    }
    clearFileHashes(source_id) {
        this.sClearFileHashes.run(source_id);
    }
    // ─── chunks + vec ────────────────────────────────────────────────
    replaceChunks(file_id, chunks, embeddings) {
        if (chunks.length !== embeddings.length) {
            throw new Error(`replaceChunks: chunks=${chunks.length} embeddings=${embeddings.length}`);
        }
        const tx = this.db.transaction(() => {
            this.sDeleteChunksByFile.run(file_id); // chunks_ad + chunks_av triggers handle fts + vec
            const newIds = [];
            for (let i = 0; i < chunks.length; i++) {
                const c = chunks[i];
                const r = this.sInsertChunk.run({
                    file_id,
                    content: c.content,
                    start_line: c.start_line,
                    end_line: c.end_line,
                });
                const id = Number(r.lastInsertRowid);
                newIds.push(id);
                const e = embeddings[i];
                const buf = Buffer.from(e.buffer, e.byteOffset, e.byteLength);
                // sqlite-vec rejects JS number for rowid — must be bigint.
                this.sInsertVec.run(BigInt(id), buf);
            }
            return newIds;
        });
        return tx();
    }
    deleteChunksForFile(file_id) {
        const r = this.sDeleteChunksByFile.run(file_id);
        return r.changes;
    }
    // ─── graph ───────────────────────────────────────────────────────
    upsertEntity(input) {
        const existing = this.db
            .prepare(`SELECT rowid FROM entities WHERE id = ? AND removed_at IS NULL`)
            .get(input.id);
        const buf = Buffer.from(input.embedding.buffer, input.embedding.byteOffset, input.embedding.byteLength);
        if (existing) {
            this.sUpdateEntityLineRange.run(input.line_start, input.line_end, input.id);
            this.sUpdateEntityVec.run(buf, BigInt(existing.rowid));
            return { rowid: existing.rowid, inserted: false };
        }
        const params = {
            id: input.id,
            source_id: input.source_id,
            kind: input.kind,
            name: input.name,
            source: input.source,
            line_start: input.line_start,
            line_end: input.line_end,
            created_at: Date.now(),
            removed_at: null,
        };
        const row = this.sUpsertEntity.get(params);
        if (!row)
            throw new Error(`upsertEntity returned no row for ${input.id}`);
        this.sInsertEntityVec.run(BigInt(row.rowid), buf);
        return { rowid: row.rowid, inserted: true };
    }
    upsertEdges(edges) {
        if (edges.length === 0)
            return;
        const tx = this.db.transaction(() => {
            for (const edge of edges) {
                this.sInsertEdge.run(edge);
            }
        });
        tx();
    }
    getEntity(id) {
        return this.sGetEntity.get(id) ?? null;
    }
    getEntitiesBySource(source) {
        return this.sGetEntitiesBySource.all(source);
    }
    getEdges(entityId) {
        return this.sGetEdges.all(entityId);
    }
    getEdgesInbound(entityId) {
        return this.sGetEdgesInbound.all(entityId);
    }
    getEdgesForMany(ids) {
        return this.fetchEdgesByGroup(this.sGetEdgesForMany, ids, 'from_id');
    }
    getEdgesInboundForMany(ids) {
        return this.fetchEdgesByGroup(this.sGetEdgesInboundForMany, ids, 'to_id');
    }
    // Run a `WHERE col IN json_each(?)` query and group rows by the join column
    // in JS. Cheaper than a SQL GROUP BY + JSON aggregation; keys not present
    // in the result are pre-seeded with empty arrays so callers don't have to
    // null-check.
    fetchEdgesByGroup(stmt, ids, groupBy) {
        const out = new Map();
        for (const id of ids)
            out.set(id, []);
        if (ids.length === 0)
            return out;
        const rows = stmt.all(JSON.stringify(ids));
        for (const row of rows) {
            const key = row[groupBy];
            const bucket = out.get(key);
            if (bucket)
                bucket.push(row);
        }
        return out;
    }
    softDeleteMissingEntities(source, keepIds) {
        const rows = this.sListEntitiesBySourceWithRowid.all(source);
        if (rows.length === 0)
            return 0;
        let deleted = 0;
        const tx = this.db.transaction(() => {
            const ts = Date.now();
            for (const r of rows) {
                if (keepIds.has(r.id))
                    continue;
                this.sSoftDeleteEntity.run(ts, r.id);
                this.sDeleteEntityVec.run(BigInt(r.rowid));
                deleted++;
            }
        });
        tx();
        return deleted;
    }
    deleteParseEdgesForSources(paths) {
        if (paths.length === 0)
            return 0;
        const r = this.sDeleteParseEdgesForPaths.run(JSON.stringify(paths));
        return r.changes;
    }
    deleteDocEdgesForSource(path) {
        return this.sDeleteDocEdgesForPath.run(path).changes;
    }
    getDocExtractedHash(file_id) {
        const row = this.sGetDocExtractedHash.get(file_id);
        return row?.doc_extracted_hash ?? null;
    }
    setDocExtractedHash(file_id, hash) {
        this.sSetDocExtractedHash.run(hash, file_id);
    }
    // ─── source-link methods ─────────────────────────────────────────
    addSourceLink(from, to) {
        if (from === to)
            throw new Error(`source cannot link to itself: ${from}`);
        this.sAddSourceLink.run(from, to);
    }
    removeSourceLink(from, to) {
        this.sRemoveSourceLink.run(from, to);
    }
    listSourceLinks() {
        const rows = this.sListSourceLinks.all();
        return rows.map((r) => ({ from: r.source_a, to: r.source_b }));
    }
    getSourcesLinkedFrom(from) {
        const rows = this.sGetSourcesLinkedFrom.all(from);
        return rows.map((r) => r.source_b);
    }
    getSourcesLinkingTo(to) {
        const rows = this.sGetSourcesLinkingTo.all(to);
        return rows.map((r) => r.source_a);
    }
    getActiveEntitiesForSource(source_id) {
        return this.sGetActiveEntitiesForSource.all(source_id);
    }
    searchEntitiesByEmbedding(queryVec, k) {
        const buf = Buffer.from(queryVec.buffer, queryVec.byteOffset, queryVec.byteLength);
        return this.sSearchEntityVec.all(buf, k);
    }
    softDeleteEntity(id) {
        this.sSoftDeleteEntity.run(Date.now(), id);
    }
    deleteEntity(id) {
        const rowid = this.db.prepare(`SELECT rowid FROM entities WHERE id = ?`).get(id);
        if (rowid) {
            this.sDeleteEntityVec.run(BigInt(rowid.rowid));
        }
        this.sDeleteEntity.run(id);
    }
    // ─── search ──────────────────────────────────────────────────────
    searchFts(query, k, filter) {
        const rows = this.runSearchFts(query, k, filter);
        return rows.map((r, i) => ({ chunk_id: r.chunk_id, rank: i + 1 }));
    }
    searchVec(queryVec, k, filter) {
        const buf = Buffer.from(queryVec.buffer, queryVec.byteOffset, queryVec.byteLength);
        const rows = this.runSearchVec(buf, k, filter);
        return rows.map((r, i) => ({ chunk_id: r.chunk_id, rank: i + 1 }));
    }
    hydrate(chunkIds) {
        const out = new Map();
        if (chunkIds.length === 0)
            return out;
        const chunks = this.sChunksByIds.all(JSON.stringify(chunkIds));
        const fileIds = Array.from(new Set(chunks.map((c) => c.file_id)));
        const files = this.sFilesByIds.all(JSON.stringify(fileIds));
        const fileMap = new Map(files.map((f) => [f.id, f]));
        const sourceIds = Array.from(new Set(files.map((f) => f.source_id)));
        const sources = this.sSourcesByIds.all(JSON.stringify(sourceIds));
        const sourceMap = new Map(sources.map((s) => [s.id, s]));
        for (const chunk of chunks) {
            const file = fileMap.get(chunk.file_id);
            if (!file)
                continue;
            const source = sourceMap.get(file.source_id);
            if (!source)
                continue;
            out.set(chunk.id, { chunk, file, source });
        }
        return out;
    }
    // ─── tags (v1.1) ─────────────────────────────────────────────────
    replaceEntityTags(entity_id, tags) {
        const tx = this.db.transaction(() => {
            this.sDeleteTagsForEntity.run(entity_id);
            for (const tag of tags) {
                this.sInsertTag.run(entity_id, tag);
            }
        });
        tx();
    }
    getTagsForEntity(entity_id) {
        const rows = this.sGetTagsForEntity.all(entity_id);
        return rows.map((r) => r.tag);
    }
    getEntitiesByTag(tag, k) {
        // SQLite LIMIT requires a value; pass a large cap when caller didn't.
        const limit = k ?? 1_000_000;
        return this.sGetEntitiesByTag.all(tag, limit);
    }
    getTagsForMany(ids) {
        const out = new Map();
        for (const id of ids)
            out.set(id, []);
        if (ids.length === 0)
            return out;
        const rows = this.sGetTagsForMany.all(JSON.stringify(ids));
        for (const r of rows) {
            const bucket = out.get(r.entity_id);
            if (bucket)
                bucket.push(r.tag);
        }
        // Sort each bucket so output is deterministic across calls.
        for (const tags of out.values())
            tags.sort();
        return out;
    }
    listTags() {
        return this.sListTags.all();
    }
    close() {
        this.db.close();
    }
    get rawDb() {
        return this.db;
    }
    // ─── search dispatch helpers ─────────────────────────────────────
    runSearchFts(query, k, filter) {
        if (filter?.source_id !== undefined) {
            return this.sSearchFtsBySource.all(query, filter.source_id, k);
        }
        if (filter?.kind !== undefined) {
            return this.sSearchFtsByKind.all(query, filter.kind, k);
        }
        return this.sSearchFts.all(query, k);
    }
    runSearchVec(buf, k, filter) {
        if (filter?.source_id !== undefined) {
            return this.sSearchVecBySource.all(buf, k * VEC_OVERFETCH, filter.source_id, k);
        }
        if (filter?.kind !== undefined) {
            return this.sSearchVecByKind.all(buf, k * VEC_OVERFETCH, filter.kind, k);
        }
        return this.sSearchVec.all(buf, k);
    }
}
