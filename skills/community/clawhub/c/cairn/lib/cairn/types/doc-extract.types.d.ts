import { z } from 'zod';
import type { EdgeRelation, EntityRow } from './primitives.types.js';
export declare const DOC_RELATIONS: readonly ["mitigates", "references", "verifies"];
export type DocRelation = (typeof DOC_RELATIONS)[number];
export declare const DocExtractZ: z.ZodObject<{
    concepts: z.ZodDefault<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
        tags: z.ZodOptional<z.ZodArray<z.ZodString>>;
    }, z.core.$strip>>>;
    edges: z.ZodDefault<z.ZodArray<z.ZodObject<{
        from: z.ZodString;
        to: z.ZodString;
        relation: z.ZodEnum<{
            verifies: "verifies";
            references: "references";
            mitigates: "mitigates";
        }>;
        confidence: z.ZodNumber;
    }, z.core.$strip>>>;
}, z.core.$strip>;
export type DocExtractRaw = z.infer<typeof DocExtractZ>;
export interface PromptCtx {
    docPath: string;
    docContent: string;
    codeEntities: Pick<EntityRow, 'id' | 'kind' | 'name'>[];
}
export interface ResolvedConcept {
    id: string;
    name: string;
    description: string | null;
    tags: string[];
}
export interface ResolvedEdge {
    from_id: string;
    to_id: string;
    relation: EdgeRelation;
    confidence: number;
}
export interface ResolveResult {
    concepts: ResolvedConcept[];
    edges: ResolvedEdge[];
    dropped: number;
}
