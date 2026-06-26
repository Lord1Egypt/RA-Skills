import type { BaziChart } from "../tools/bazi/calc.js";
import type { BaziEvidenceSummary, PersonaMemoryEntry, PersonaRecord, PersonaSnapshot, PromptPack, PersonaKnowledge, SupportedLanguage } from "./types.js";
interface ReferenceBlocks {
    cognition: string;
    values: string;
    communication: string;
    relationship: string;
    state: string;
}
export declare function buildBaziEvidence(params: {
    chart: BaziChart;
    knowledge: PersonaKnowledge;
    relationships: string[];
    activeRelationships: string[];
    memory: PersonaMemoryEntry[];
}): {
    evidence: BaziEvidenceSummary;
    references: ReferenceBlocks;
};
export declare function regenerateSnapshot(params: {
    record: Omit<PersonaRecord, "snapshot" | "updated_at" | "created_at">;
    promptPack: PromptPack;
    knowledge: PersonaKnowledge;
}): PersonaSnapshot;
export declare function renderPersonaMarkdown(record: PersonaRecord): string;
export declare function respondInPersona(record: PersonaRecord, message: string, language?: SupportedLanguage): string;
export {};
