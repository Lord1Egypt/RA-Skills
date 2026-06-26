import type { PersonaKnowledge, PromptPack } from "./types.js";
export declare const DEFAULT_PERSONA_DIR: string;
export declare function loadPromptPack(promptsDir?: string): PromptPack;
export declare function loadPersonaKnowledge(knowledgeSource?: string): PersonaKnowledge;
export declare function resetKnowledgeCache(): void;
