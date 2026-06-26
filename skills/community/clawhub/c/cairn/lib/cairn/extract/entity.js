import { extname } from 'node:path';
import { extractPythonEntities } from './python.js';
import { extractRustEntities } from './rust.js';
import { extractTypeScriptEntities } from './typescript.js';
// Per-language parsers. Add a new grammar by registering it here — the
// dispatcher keeps the public API stable.
const PARSERS = {
    '.rs': extractRustEntities,
    '.ts': extractTypeScriptEntities,
    '.tsx': extractTypeScriptEntities,
    '.py': extractPythonEntities,
};
const EMPTY_FILE = {
    entities: [],
    fnCalls: new Map(),
    fnRefs: new Map(),
};
// Single-file parse: entities plus per-fn AST-derived call/ref data.
export const extractFromFile = (content, filePath) => {
    const ext = extname(filePath).toLowerCase();
    const parser = PARSERS[ext];
    return parser ? parser(content, filePath) : EMPTY_FILE;
};
// Cross-source edges: this source's function bodies reference entities in a
// linked source. Local resolution wins — a name that resolves in this source
// never produces a cross-source edge.
export const buildCrossSourceEdges = (perFile, external) => {
    if (external.size === 0)
        return [];
    const localNames = new Set();
    for (const f of perFile)
        for (const e of f.entities)
            localNames.add(e.name);
    const edges = [];
    for (const file of perFile) {
        const functions = file.entities.filter((e) => e.kind === 'function');
        if (functions.length === 0)
            continue;
        for (const fn of functions) {
            const calls = file.fnCalls.get(fn.id);
            if (calls) {
                for (const call of calls) {
                    if (localNames.has(call))
                        continue;
                    const target = external.get(call);
                    if (!target || target.kind !== 'function')
                        continue;
                    edges.push({
                        from_id: fn.id,
                        to_id: target.id,
                        relation: 'calls',
                        confidence: 1.0,
                        derive: 'parse',
                    });
                }
            }
            const refs = file.fnRefs.get(fn.id);
            if (refs) {
                for (const ref of refs) {
                    if (localNames.has(ref))
                        continue;
                    const target = external.get(ref);
                    if (!target || target.kind === 'function')
                        continue;
                    edges.push({
                        from_id: fn.id,
                        to_id: target.id,
                        relation: 'depends_on',
                        confidence: 1.0,
                        derive: 'parse',
                    });
                }
            }
        }
    }
    return edges;
};
// Cross-file edges: same `calls` and `depends_on` relations as `buildEdges`,
// but the target lives in a different file of the same source. Names that
// collide across files are skipped — without scope info the regex can't pick
// the right one, and a noisy edge is worse than a missing one.
export const buildCrossFileEdges = (perFile) => {
    if (perFile.length < 2)
        return [];
    const byName = new Map();
    const ambiguous = new Set();
    for (const file of perFile) {
        for (const e of file.entities) {
            if (ambiguous.has(e.name))
                continue;
            const prev = byName.get(e.name);
            if (prev && prev.id !== e.id) {
                ambiguous.add(e.name);
                byName.delete(e.name);
                continue;
            }
            byName.set(e.name, e);
        }
    }
    if (byName.size === 0)
        return [];
    const edges = [];
    for (const file of perFile) {
        const localIds = new Set(file.entities.map((e) => e.id));
        const functions = file.entities.filter((e) => e.kind === 'function');
        if (functions.length === 0)
            continue;
        for (const fn of functions) {
            const calls = file.fnCalls.get(fn.id);
            if (calls) {
                for (const call of calls) {
                    const target = byName.get(call);
                    if (!target || target.kind !== 'function')
                        continue;
                    if (localIds.has(target.id))
                        continue;
                    edges.push({
                        from_id: fn.id,
                        to_id: target.id,
                        relation: 'calls',
                        confidence: 1.0,
                        derive: 'parse',
                    });
                }
            }
            const refs = file.fnRefs.get(fn.id);
            if (refs) {
                for (const ref of refs) {
                    const target = byName.get(ref);
                    if (!target || target.kind === 'function')
                        continue;
                    if (localIds.has(target.id))
                        continue;
                    edges.push({
                        from_id: fn.id,
                        to_id: target.id,
                        relation: 'depends_on',
                        confidence: 1.0,
                        derive: 'parse',
                    });
                }
            }
        }
    }
    return edges;
};
export const buildEdges = (file) => {
    const edges = [];
    const entityMap = new Map(file.entities.map((e) => [e.name, e]));
    // No `defines` edge for code: "what does this file define" is already
    // answered by entities.source (file path). The relation type is reserved
    // for the doc-extraction phase.
    const functions = file.entities.filter((e) => e.kind === 'function');
    // calls: function → function (within same file).
    for (const fn of functions) {
        const calls = file.fnCalls.get(fn.id);
        if (!calls)
            continue;
        for (const call of calls) {
            if (call === fn.name)
                continue;
            const target = entityMap.get(call);
            if (!target)
                continue;
            edges.push({
                from_id: fn.id,
                to_id: target.id,
                relation: 'calls',
                confidence: 1.0,
                derive: 'parse',
            });
        }
    }
    // depends_on: function references a struct/enum/constant in the same file.
    for (const fn of functions) {
        const refs = file.fnRefs.get(fn.id);
        if (!refs)
            continue;
        for (const ref of refs) {
            const target = entityMap.get(ref);
            if (!target || target.kind === 'function')
                continue;
            if (target.id === fn.id)
                continue;
            edges.push({
                from_id: fn.id,
                to_id: target.id,
                relation: 'depends_on',
                confidence: 1.0,
                derive: 'parse',
            });
        }
    }
    return edges;
};
