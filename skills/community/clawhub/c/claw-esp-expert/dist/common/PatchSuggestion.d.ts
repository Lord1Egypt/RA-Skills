export interface PatchSuggestion {
    path?: string;
    kind: 'append_block' | 'insert_block' | 'replace_block';
    summary: string;
    before?: string;
    after: string;
}
export declare function buildPatchSuggestion(args: {
    path?: string;
    kind: PatchSuggestion['kind'];
    summary: string;
    before?: string;
    after: string;
}): PatchSuggestion;
