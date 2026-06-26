export const TS_KIND_BY_NODE = {
    function_declaration: 'function',
    method_definition: 'function',
    class_declaration: 'struct',
    interface_declaration: 'struct',
    enum_declaration: 'enum',
    variable_declarator: 'constant',
};
// Containers we descend into looking for declarations. Excludes
// `function_declaration` / `method_definition` (their body is private scope)
// and `statement_block` (any block-scoped binding is local).
export const TS_RECURSE_NODES = new Set([
    'program',
    'export_statement',
    'class_declaration',
    'class_body',
    'lexical_declaration',
]);
