import type { SourceKind } from './primitives.types.js';
export interface CairnConfig {
    include: string[];
    exclude: string[];
    default_kind: SourceKind;
}
export type ParsedFlags = Record<string, string | number | boolean | string[] | undefined>;
export interface FlagSpec {
    string?: string[];
    number?: string[];
    boolean?: string[];
    array?: string[];
}
