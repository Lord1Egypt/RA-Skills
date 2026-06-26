import path from "node:path";
import { fileURLToPath } from "node:url";
import { fileExists, readJson, readUtf8 } from "../shared/fs.js";
const MODULE_DIR = path.dirname(fileURLToPath(import.meta.url));
const SRC_DIR = path.resolve(MODULE_DIR, "..");
const PROJECT_ROOT = path.resolve(SRC_DIR, "..");
export const DEFAULT_PERSONA_DIR = path.join(PROJECT_ROOT, "personas");
const PROMPTS_DIR = path.join(PROJECT_ROOT, "prompts");
const PROMPT_KNOWLEDGE_FILE = path.join(PROMPTS_DIR, "knowledge.md");
let personaKnowledgeCache;
export function loadPromptPack(promptsDir = PROMPTS_DIR) {
    const manifestPath = path.join(promptsDir, "manifest.json");
    if (!fileExists(manifestPath)) {
        throw new Error(`Prompt manifest missing: ${manifestPath}`);
    }
    const manifest = readJson(manifestPath);
    if (!Array.isArray(manifest.entries) || manifest.entries.length === 0) {
        throw new Error("Prompt manifest is empty.");
    }
    const entries = manifest.entries.map((entry) => {
        const filePath = path.join(promptsDir, entry.file);
        if (!fileExists(filePath)) {
            throw new Error(`Prompt file missing: ${entry.file}`);
        }
        const body = readUtf8(filePath).trim();
        if (!body) {
            throw new Error(`Prompt file is empty: ${entry.file}`);
        }
        return { ...entry, body };
    });
    return {
        version: manifest.version,
        entries,
    };
}
function resolveKnowledgeFile(target) {
    if (target.endsWith(".md")) {
        return target;
    }
    return path.join(target, "knowledge.md");
}
function extractNamedJsonBlock(markdown, blockName) {
    const pattern = new RegExp(`\`\`\`json\\s+${blockName}\\n([\\s\\S]*?)\\n\`\`\``, "u");
    const matched = pattern.exec(markdown);
    if (!matched?.[1]) {
        throw new Error(`Prompt knowledge block missing: ${blockName}`);
    }
    return matched[1].trim();
}
export function loadPersonaKnowledge(knowledgeSource = PROMPT_KNOWLEDGE_FILE) {
    if (personaKnowledgeCache && knowledgeSource === PROMPT_KNOWLEDGE_FILE) {
        return personaKnowledgeCache;
    }
    const filePath = resolveKnowledgeFile(knowledgeSource);
    if (!fileExists(filePath)) {
        throw new Error(`Persona knowledge missing: ${filePath}`);
    }
    const raw = readUtf8(filePath);
    const knowledge = JSON.parse(extractNamedJsonBlock(raw, "persona-knowledge"));
    if (!knowledge.stem_to_element ||
        !knowledge.element_profiles ||
        !knowledge.ten_god_behaviors ||
        !knowledge.reference_guidance) {
        throw new Error("Persona knowledge is incomplete.");
    }
    if (knowledgeSource === PROMPT_KNOWLEDGE_FILE) {
        personaKnowledgeCache = knowledge;
    }
    return knowledge;
}
export function resetKnowledgeCache() {
    personaKnowledgeCache = undefined;
}
