// Tree-sitter-based entity extractor for Python.
//
//   function_definition → function   (top-level + class methods)
//   class_definition    → struct     (closest existing kind)
//   ALL_CAPS = ...      → constant   (Python module-level convention)
//
// `decorated_definition` wraps a function/class with decorators; the visitor
// recurses into it and emits the inner def. Function bodies aren't recursed
// — nested `def` is local scope.
import Parser from 'tree-sitter';
import Python from 'tree-sitter-python';
import { PY_KIND_BY_NODE, PY_RECURSE_NODES, PY_UPPER_SNAKE, } from '../constants/extract/python.constants.js';
let parser = null;
const getParser = () => {
    if (!parser) {
        parser = new Parser();
        parser.setLanguage(Python);
    }
    return parser;
};
export const extractPythonEntities = (content, filePath) => {
    const tree = getParser().parse(content);
    const entities = [];
    const fnCalls = new Map();
    const fnRefs = new Map();
    const seen = new Set();
    const emit = (name, kind, node) => {
        if (seen.has(name))
            return null;
        const id = `${filePath}:${name}`;
        entities.push({
            id,
            kind,
            name,
            line_start: node.startPosition.row + 1,
            line_end: node.endPosition.row + 1,
        });
        seen.add(name);
        return id;
    };
    const visit = (node) => {
        const kind = PY_KIND_BY_NODE[node.type];
        if (kind) {
            const name = node.childForFieldName('name')?.text;
            if (name) {
                const id = emit(name, kind, node);
                if (id && kind === 'function') {
                    // Walk the entire function_definition so type annotations and
                    // default-value expressions in the parameters contribute refs
                    // alongside body calls/refs.
                    const { calls, refs } = collectCallsAndRefs(node);
                    if (calls.size > 0)
                        fnCalls.set(id, calls);
                    if (refs.size > 0)
                        fnRefs.set(id, refs);
                }
            }
        }
        // Module-level UPPER_SNAKE = ... → constant. The visitor only reaches
        // `assignment` via expression_statement → assignment when inside `module`
        // (function bodies aren't recursed), so we don't accidentally pick up
        // local-scope all-caps variables.
        if (node.type === 'assignment') {
            const lhs = node.namedChildren[0];
            if (lhs && lhs.type === 'identifier' && PY_UPPER_SNAKE.test(lhs.text)) {
                emit(lhs.text, 'constant', node);
            }
        }
        if (PY_RECURSE_NODES.has(node.type)) {
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
    const findCalls = (n) => {
        if (n.type === 'call') {
            const fn = n.childForFieldName('function');
            if (fn) {
                const picked = pickPyCallee(fn);
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
        if (n.type === 'identifier') {
            if (!callPositions.has(n.startIndex))
                refs.add(n.text);
        }
        for (const child of n.namedChildren)
            findRefs(child);
    };
    findRefs(body);
    return { calls, refs };
};
const pickPyCallee = (fn) => {
    switch (fn.type) {
        case 'identifier': {
            return { name: fn.text, idNode: fn };
        }
        case 'attribute': {
            const a = fn.childForFieldName('attribute');
            return { name: a?.text ?? null, idNode: a ?? null };
        }
        default:
            return { name: null, idNode: null };
    }
};
