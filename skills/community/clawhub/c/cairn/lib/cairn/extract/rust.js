// Tree-sitter-based entity extractor for Rust. Replaces the regex pass that
// triggered design.md §9's "switch when regex misses >20%" criterion.
//
// What we get over regex: no false positives from `fn`/`struct`/`const`
// tokens inside comments or strings, exact AST line ranges, future-proof
// node-name additions instead of new regexes.
//
// Deliberately don't (yet):
//   - Methods inside `impl` blocks share the function namespace with free
//     fns. Two impls with the same method name dedupe to the first
//     encountered; disambiguating to `Type::name` would break the
//     `<file>:<name>` ID format and ripple through edges.
//   - Trait method declarations are skipped — they're signatures, not
//     callable code. Implementations are what graph traversal cares about.
//   - Nested functions inside another fn body are skipped.
import Parser from 'tree-sitter';
import Rust from 'tree-sitter-rust';
import { RUST_KIND_BY_NODE, RUST_RECURSE_NODES } from '../constants/extract/rust.constants.js';
let parser = null;
const getParser = () => {
    if (!parser) {
        parser = new Parser();
        parser.setLanguage(Rust);
    }
    return parser;
};
export const extractRustEntities = (content, filePath) => {
    const tree = getParser().parse(content);
    const entities = [];
    const fnCalls = new Map();
    const fnRefs = new Map();
    const seen = new Set();
    const visit = (node) => {
        const kind = RUST_KIND_BY_NODE[node.type];
        if (kind) {
            const nameNode = node.childForFieldName('name');
            const name = nameNode?.text;
            if (name && !seen.has(name)) {
                const id = `${filePath}:${name}`;
                entities.push({
                    id,
                    kind,
                    name,
                    // tree-sitter rows are 0-indexed; cairn entity rows are 1-indexed.
                    line_start: node.startPosition.row + 1,
                    line_end: node.endPosition.row + 1,
                });
                seen.add(name);
                if (kind === 'function') {
                    const { calls, refs } = collectCallsAndRefs(node);
                    if (calls.size > 0)
                        fnCalls.set(id, calls);
                    if (refs.size > 0)
                        fnRefs.set(id, refs);
                }
            }
        }
        if (RUST_RECURSE_NODES.has(node.type)) {
            for (const child of node.namedChildren)
                visit(child);
        }
    };
    visit(tree.rootNode);
    return { entities, fnCalls, fnRefs };
};
// AST traversal of a function declaration subtree to find call-position
// names (callees) and non-call-position names (potential type/const refs).
// Comments and string contents have their own AST node types — they never
// become identifier or type_identifier — so they don't pollute either set.
const collectCallsAndRefs = (body) => {
    const calls = new Set();
    const refs = new Set();
    const callPositions = new Set(); // startIndex of nodes that ARE call positions
    // Pass 1: every call_expression contributes a callee name + the byte offset
    // of the identifier we treat as the "called name". Macro invocations are
    // intentionally skipped — rarely entities; the regex fallback emitted noise.
    const findCalls = (n) => {
        if (n.type === 'call_expression') {
            const fn = n.childForFieldName('function');
            if (fn) {
                const { name, idNode } = pickRustCallee(fn);
                if (name && idNode) {
                    calls.add(name);
                    callPositions.add(idNode.startIndex);
                }
            }
        }
        for (const child of n.namedChildren)
            findCalls(child);
    };
    findCalls(body);
    // Pass 2: any identifier or type_identifier not recorded as a call position
    // becomes a candidate ref. Edge layer filters by knownNames.
    const findRefs = (n) => {
        if (n.type === 'identifier' || n.type === 'type_identifier') {
            if (!callPositions.has(n.startIndex))
                refs.add(n.text);
        }
        for (const child of n.namedChildren)
            findRefs(child);
    };
    findRefs(body);
    return { calls, refs };
};
const pickRustCallee = (fn) => {
    switch (fn.type) {
        case 'identifier': {
            return { name: fn.text, idNode: fn };
        }
        case 'field_expression': {
            const f = fn.childForFieldName('field');
            return { name: f?.text ?? null, idNode: f ?? null };
        }
        case 'scoped_identifier': {
            const n = fn.childForFieldName('name');
            return { name: n?.text ?? null, idNode: n ?? null };
        }
        default:
            return { name: null, idNode: null };
    }
};
