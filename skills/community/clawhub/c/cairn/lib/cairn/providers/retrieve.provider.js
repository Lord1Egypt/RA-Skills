import { CANDIDATE_K, DEFAULT_ASK_EDGES_PER_ENTITY, DEFAULT_ASK_ENTITIES_PER_HIT, DEFAULT_GRAPH_K, DEFAULT_K, DEFAULT_PATH_MAX_DEPTH, RRF_K, } from '../constants/retrieve.constants.js';
// FTS5's query parser treats `-`, `:`, `*`, `^`, parens, quotes, AND/OR/NOT as
// syntax — bare `Token-2022` parses as a column filter and errors with "no
// such column: 2022". Wrap each whitespace-separated token in double quotes
// so FTS5 treats it as a literal phrase.
const toFtsQuery = (text) => text
    .split(/\s+/)
    .filter((t) => t.length > 0)
    .map((t) => `"${t.replace(/"/g, '""')}"`)
    .join(' ');
// Distance from an entity's center line to a target line. Concepts and other
// entities without line spans sort to the back via Number.POSITIVE_INFINITY.
const proximity = (entity, target) => {
    if (entity.line_start === null || entity.line_end === null)
        return Number.POSITIVE_INFINITY;
    const mid = (entity.line_start + entity.line_end) / 2;
    return Math.abs(mid - target);
};
export class RetrieveProvider {
    db;
    embed;
    constructor(db, embed) {
        this.db = db;
        this.embed = embed;
    }
    async search(query, opts) {
        if (query.trim().length === 0)
            return [];
        const k = opts?.k ?? DEFAULT_K;
        const filter = this.buildFilter(opts);
        const qvec = await this.embed.embed(query);
        const ftsQuery = toFtsQuery(query);
        // Over-fetch when a tag filter is in play — the post-hydrate filter may
        // drop chunks that don't sit in a tagged file, and we still want the
        // caller's k. Use the same multiplier as VEC_OVERFETCH lives by.
        const candidateK = opts?.tag ? CANDIDATE_K * 2 : CANDIDATE_K;
        const ftsHits = ftsQuery ? this.db.searchFts(ftsQuery, candidateK, filter) : [];
        const vecHits = this.db.searchVec(qvec, candidateK, filter);
        const fused = new Map();
        for (const h of ftsHits) {
            fused.set(h.chunk_id, {
                score: 1 / (RRF_K + h.rank),
                fts_rank: h.rank,
                vec_rank: null,
            });
        }
        for (const h of vecHits) {
            const cur = fused.get(h.chunk_id) ?? { score: 0, fts_rank: null, vec_rank: null };
            cur.score += 1 / (RRF_K + h.rank);
            cur.vec_rank = h.rank;
            fused.set(h.chunk_id, cur);
        }
        const rankedAll = [...fused.entries()].sort((a, b) => b[1].score - a[1].score);
        if (rankedAll.length === 0)
            return [];
        // Hydrate every candidate so we can apply the tag filter on file_path
        // before slicing to k. The hydrate is one batched seek either way.
        const allIds = rankedAll.map(([id]) => id);
        const hydrated = this.db.hydrate(allIds);
        const taggedFiles = opts?.tag ? this.taggedFileSet(opts.tag) : null;
        const out = [];
        for (const [id, fuse] of rankedAll) {
            const h = hydrated.get(id);
            if (!h)
                continue;
            if (taggedFiles && !taggedFiles.has(`${h.source.id}:${h.file.path}`))
                continue;
            out.push({
                chunk_id: id,
                source: h.source,
                file_path: h.file.path,
                start_line: h.chunk.start_line,
                end_line: h.chunk.end_line,
                content: h.chunk.content,
                score: fuse.score,
                fts_rank: fuse.fts_rank,
                vec_rank: fuse.vec_rank,
            });
            if (out.length >= k)
                break;
        }
        return out;
    }
    // (source_id, file_path) pairs whose files contain at least one active
    // entity carrying the tag. Used as a soft filter on search()/ask() hits.
    taggedFileSet(tag) {
        const out = new Set();
        for (const e of this.db.getEntitiesByTag(tag)) {
            // entity ids are `<source_id>:<filepath>:<name>` — pull source_id off
            // the prefix so we can pair it with entities.source (the file path).
            const m = e.id.match(/^(\d+):/);
            if (!m || !e.source)
                continue;
            out.add(`${m[1]}:${e.source}`);
        }
        return out;
    }
    async list(filter) {
        return this.db.listSources(filter);
    }
    async graph(input) {
        if ((input.query == null) === (input.entity_id == null)) {
            throw new Error('graph: provide exactly one of `query` or `entity_id`');
        }
        if (input.entity_id) {
            const entity = this.db.getEntity(input.entity_id);
            if (!entity)
                return [];
            const tags = this.db.getTagsForEntity(entity.id);
            if (input.tag && !tags.includes(input.tag))
                return [];
            return [this.buildGraphHit(entity, tags, null)];
        }
        if (input.query.trim().length === 0)
            return [];
        const k = input.k ?? DEFAULT_GRAPH_K;
        // Over-fetch when a tag filter trims results post-hydrate.
        const fetchK = input.tag ? k * 4 : k;
        const qvec = await this.embed.embed(input.query);
        const entities = this.db.searchEntitiesByEmbedding(qvec, fetchK);
        const tagsByEntity = this.db.getTagsForMany(entities.map((e) => e.id));
        const hits = [];
        for (const e of entities) {
            const tags = tagsByEntity.get(e.id) ?? [];
            if (input.tag && !tags.includes(input.tag))
                continue;
            hits.push(this.buildGraphHit(e, tags, hits.length + 1));
            if (hits.length >= k)
                break;
        }
        return hits;
    }
    async ask(query, opts) {
        const hits = await this.search(query, opts);
        if (hits.length === 0)
            return [];
        const maxEnt = opts?.maxEntitiesPerHit ?? DEFAULT_ASK_ENTITIES_PER_HIT;
        const maxEdges = opts?.maxEdgesPerEntity ?? DEFAULT_ASK_EDGES_PER_ENTITY;
        // entities.source stores the relative file path. The same path string can
        // appear under multiple sources, so filter by entity-id prefix to scope
        // to this hit's source. v5 ids are `<source_id>:<filepath>:<name>`.
        const out = [];
        const pickedByHit = [];
        const allPickedIds = [];
        for (const hit of hits) {
            const prefix = `${hit.source.id}:`;
            const all = this.db.getEntitiesBySource(hit.file_path);
            const scoped = all.filter((e) => e.id.startsWith(prefix));
            const mid = (hit.start_line + hit.end_line) / 2;
            scoped.sort((a, b) => proximity(a, mid) - proximity(b, mid));
            const picked = scoped.slice(0, maxEnt);
            pickedByHit.push({ hit, picked });
            for (const p of picked)
                allPickedIds.push(p.id);
        }
        // Three batched fetches cover edges + tags for every picked entity across
        // every hit — replaces 3*N per-entity round-trips.
        const outboundByFrom = this.db.getEdgesForMany(allPickedIds);
        const inboundByTo = this.db.getEdgesInboundForMany(allPickedIds);
        const tagsByEntity = this.db.getTagsForMany(allPickedIds);
        for (const { hit, picked } of pickedByHit) {
            const entities = picked
                .map((entity) => ({
                entity,
                edges_out: (outboundByFrom.get(entity.id) ?? []).slice(0, maxEdges),
                edges_in: (inboundByTo.get(entity.id) ?? []).slice(0, maxEdges),
                tags: tagsByEntity.get(entity.id) ?? [],
            }))
                // When the caller filters by tag, narrow per-hit entities to the
                // matching set. Keeps response coherent with the filter intent
                // (otherwise users see "tagged chunk + unrelated entities").
                .filter((ent) => !opts?.tag || ent.tags.includes(opts.tag));
            out.push({ ...hit, entities });
        }
        return out;
    }
    async listTags() {
        return this.db.listTags();
    }
    async path(from, to, opts) {
        const fromEntity = this.db.getEntity(from);
        const toEntity = this.db.getEntity(to);
        if (!fromEntity || !toEntity)
            return null;
        if (from === to)
            return { entities: [fromEntity], steps: [] };
        const maxDepth = opts?.maxDepth ?? DEFAULT_PATH_MAX_DEPTH;
        const directed = opts?.directed ?? false;
        // BFS from `from`. parents[id] = { prev, edge, reversed } records how we
        // reached `id`. When we discover `to`, walk parents back to reconstruct.
        // Edge fetches are batched per layer — one SQL per direction per layer
        // instead of per node.
        const parents = new Map();
        let frontier = [from];
        const visited = new Set([from]);
        for (let depth = 0; depth < maxDepth; depth++) {
            const outboundByFrom = this.db.getEdgesForMany(frontier);
            const inboundByTo = directed
                ? new Map()
                : this.db.getEdgesInboundForMany(frontier);
            const next = [];
            for (const id of frontier) {
                for (const e of outboundByFrom.get(id) ?? []) {
                    if (visited.has(e.to_id))
                        continue;
                    visited.add(e.to_id);
                    parents.set(e.to_id, { prev: id, edge: e, reversed: false });
                    if (e.to_id === to)
                        return this.reconstructPath(from, to, parents);
                    next.push(e.to_id);
                }
                if (!directed) {
                    for (const e of inboundByTo.get(id) ?? []) {
                        if (visited.has(e.from_id))
                            continue;
                        visited.add(e.from_id);
                        parents.set(e.from_id, { prev: id, edge: e, reversed: true });
                        if (e.from_id === to)
                            return this.reconstructPath(from, to, parents);
                        next.push(e.from_id);
                    }
                }
            }
            if (next.length === 0)
                return null;
            frontier = next;
        }
        return null;
    }
    reconstructPath(from, to, parents) {
        const reverseSteps = [];
        const reverseIds = [to];
        let cursor = to;
        while (cursor !== from) {
            const p = parents.get(cursor);
            if (!p)
                throw new Error(`path reconstruction: missing parent for ${cursor}`);
            reverseSteps.push({ edge: p.edge, reversed: p.reversed });
            reverseIds.push(p.prev);
            cursor = p.prev;
        }
        reverseIds.reverse();
        reverseSteps.reverse();
        const entities = [];
        for (const id of reverseIds) {
            const e = this.db.getEntity(id);
            if (!e)
                throw new Error(`path reconstruction: missing entity ${id}`);
            entities.push(e);
        }
        return { entities, steps: reverseSteps };
    }
    buildGraphHit(entity, tags, score) {
        return {
            entity,
            edges_out: this.db.getEdges(entity.id),
            edges_in: this.db.getEdgesInbound(entity.id),
            tags,
            score,
        };
    }
    buildFilter(opts) {
        if (!opts)
            return undefined;
        const filter = {};
        if (opts.source !== undefined)
            filter.source_id = this.resolveSourceId(opts.source);
        if (opts.kind !== undefined)
            filter.kind = opts.kind;
        return filter.source_id !== undefined || filter.kind !== undefined ? filter : undefined;
    }
    resolveSourceId(ref) {
        // Validate both numeric and string refs against the source table. A clear
        // throw is friendlier and faster to diagnose than silently returning
        // zero hits when an agent passes a stale or invented id.
        const src = this.db.getSource(ref);
        if (!src)
            throw new Error(`source not found: ${ref}`);
        return src.id;
    }
}
