// Tree-sitter-based entity extractor for TypeScript / TSX.
//   function_declaration / method_definition  → function
//   class_declaration / interface_declaration → struct
//   enum_declaration                          → enum
//   variable_declarator (in lexical_declaration at module / export scope)
//                                             → constant
//
// Skipped for v1:
//   - type_alias_declaration: no good kind without adding a 'type' kind.
//   - Function bodies: nested `function` / nested `let` are locally scoped.
//   - JS / JSX: separate grammar (`tree-sitter-javascript`); add when needed.
import Parser from 'tree-sitter';
import TypeScript from 'tree-sitter-typescript';
import { TS_KIND_BY_NODE, TS_RECURSE_NODES, } from '../constants/extract/typescript.constants.js';
let tsParser = null;
let tsxParser = null;
const getParser = (ext) => {
    if (ext === '.tsx') {
        if (!tsxParser) {
            tsxParser = new Parser();
            tsxParser.setLanguage(TypeScript.tsx);
        }
        return tsxParser;
    }
    if (!tsParser) {
        tsParser = new Parser();
        tsParser.setLanguage(TypeScript.typescript);
    }
    return tsParser;
};
export const extractTypeScriptEntities = (content, filePath) => {
    const ext = filePath.endsWith('.tsx') ? '.tsx' : '.ts';
    const tree = getParser(ext).parse(content);
    const entities = [];
    const fnCalls = new Map();
    const fnRefs = new Map();
    const seen = new Set();
    const visit = (node) => {
        const kind = TS_KIND_BY_NODE[node.type];
        if (kind) {
            const nameNode = node.childForFieldName('name');
            const name = nameNode?.text;
            if (name && !seen.has(name)) {
                const id = `${filePath}:${name}`;
                entities.push({
                    id,
                    kind,
                    name,
                    line_start: node.startPosition.row + 1,
                    line_end: node.endPosition.row + 1,
                });
                seen.add(name);
                // Walk the entire function/method subtree so signature refs (param
                // types, return types) and body calls/refs land in one pass.
                if (kind === 'function') {
                    const { calls, refs } = collectCallsAndRefs(node);
                    if (calls.size > 0)
                        fnCalls.set(id, calls);
                    if (refs.size > 0)
                        fnRefs.set(id, refs);
                }
            }
        }
        if (TS_RECURSE_NODES.has(node.type)) {
            for (const child of node.namedChildren)
                visit(child);
        }
    };
    visit(tree.rootNode);
    return { entities, fnCalls, fnRefs };
};
const collectCallsAndRefs = (body) => {
    const calls = new Set();
    const refs = new Set();
    const callPositions = new Set();
    // Calls come from `call_expression` (`foo()`, `obj.foo()`, `Foo?.foo()`)
    // and `new_expression` (`new Pool()`). For member_expression callees we
    // take the `property` — the method/constructor name itself.
    const findCalls = (n) => {
        if (n.type === 'call_expression') {
            const fn = n.childForFieldName('function');
            if (fn) {
                const picked = pickTsCallee(fn);
                if (picked.name && picked.idNode) {
                    calls.add(picked.name);
                    callPositions.add(picked.idNode.startIndex);
                }
            }
        }
        else if (n.type === 'new_expression') {
            const c = n.childForFieldName('constructor');
            if (c) {
                const picked = pickTsCallee(c);
                if (picked.name && picked.idNode) {
                    calls.add(picked.name);
                    callPositions.add(picked.idNode.startIndex);
                }
            }
        }
        for (const child of n.namedChildren)
            findCalls(child);
    };
    findCalls(body);
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
const pickTsCallee = (fn) => {
    switch (fn.type) {
        case 'identifier':
        case 'type_identifier': {
            return { name: fn.text, idNode: fn };
        }
        case 'member_expression': {
            const p = fn.childForFieldName('property');
            return { name: p?.text ?? null, idNode: p ?? null };
        }
        default:
            return { name: null, idNode: null };
    }
};
