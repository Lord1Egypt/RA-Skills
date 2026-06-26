// AST node type → entity kind. Anything not in this table is ignored for
// entity extraction (containers like mod/impl are still walked through).
export const RUST_KIND_BY_NODE = {
    function_item: 'function',
    struct_item: 'struct',
    union_item: 'struct',
    enum_item: 'enum',
    const_item: 'constant',
    static_item: 'constant',
};
// Container nodes whose children should be visited. Excludes function_item
// (no nested-fn extraction) and trait_item (trait method signatures aren't
// real entities; their impls are).
export const RUST_RECURSE_NODES = new Set([
    'source_file',
    'mod_item',
    'declaration_list',
    'impl_item',
]);
