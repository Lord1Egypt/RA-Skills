export const PY_KIND_BY_NODE = {
    function_definition: 'function',
    class_definition: 'struct',
};
// Descend into containers; never into a `function_definition`'s body.
// `block` is class-scope here (class_definition.body) — recursing into it
// surfaces methods. Function-body block is guarded by not recursing into
// function_definition.
export const PY_RECURSE_NODES = new Set([
    'module',
    'class_definition',
    'decorated_definition',
    'block',
    'expression_statement',
]);
export const PY_UPPER_SNAKE = /^[A-Z][A-Z0-9_]*$/;
