import type { BaziChart } from "../tools/bazi/calc.js";
export type SupportedLanguage = "zh" | "en" | "ja" | "ko";
export type PersonaMemoryType = "fact" | "correction" | "style" | "context";
export type RoutedAction = "help" | "create" | "update" | "inspect" | "flow" | "calendar" | "respond";
export interface PersonaMemoryEntry {
    memory_id?: string;
    type: PersonaMemoryType;
    key?: string;
    content: string;
    source: string;
    time_anchor?: string;
    importance?: number;
    confidence?: number;
    created_at: string;
    updated_at?: string;
}
export interface PersonaConversationEntry {
    id?: string;
    session_id: string;
    role: "user" | "assistant";
    content: string;
    mode: "chat" | "analysis" | "update" | "create";
    source_type?: "text" | "json" | "ocr_text" | "chat";
    created_at: string;
}
export interface BaziEvidenceSummary {
    day_master: string;
    primary_ten_god: string;
    five_element_summary: string;
    current_luck: string;
    state_shift: {
        summary: string;
        communication: string;
        decision: string;
    };
    evidence_lines: string[];
}
export interface PersonaSnapshot {
    generated_at: string;
    prompt_stack: string[];
    evidence: BaziEvidenceSummary;
    reference_profile: string;
    reference_state: string;
}
export interface PersonaProfile {
    name: string;
    gender: "男" | "女";
    birth_date: string;
    birth_time?: string;
    birth_location?: string;
    calendar_type: "solar" | "lunar";
}
export interface PersonaRecord {
    schema_version: "4.0.0";
    slug: string;
    profile: PersonaProfile;
    relationships: string[];
    active_relationships: string[];
    preferences: {
        preferred_language: "auto" | SupportedLanguage;
        analysis_mode: "normal" | "cheatsheet";
    };
    chart: BaziChart;
    memory: PersonaMemoryEntry[];
    snapshot: PersonaSnapshot;
    persona_markdown?: string;
    created_at: string;
    updated_at: string;
}
export interface PersonaRef {
    slug: string;
    name: string;
    updated_at: string;
}
export interface PromptManifestEntry {
    id: string;
    file: string;
    stage: string;
}
export interface PromptManifest {
    version: number;
    entries: PromptManifestEntry[];
}
export interface PromptPackEntry extends PromptManifestEntry {
    body: string;
}
export interface PromptPack {
    version: number;
    entries: PromptPackEntry[];
}
export interface PersonaKnowledge {
    stem_to_element: Record<string, string>;
    element_profiles: Record<string, {
        summary: string;
        speech: string;
        decision: string;
        stress: string;
        relationship: string;
        risk: string;
    }>;
    ten_god_behaviors: Record<string, {
        trait: string;
        decision: string;
        communication: string;
        stress: string;
    }>;
    reference_guidance: {
        communication_title: string;
        persona_writing_tip: string;
        relationship_tip_template: string;
        state_writing_tip: string;
        profile_section_title: string;
        state_section_title: string;
    };
    state_shift_by_ten_god: Record<string, {
        summary: string;
        communication: string;
        decision: string;
    }>;
}
export interface RoutedIntent {
    action: RoutedAction;
    payload: string;
    analysis_mode: "normal" | "cheatsheet";
}
export interface BaziChartToolInput {
    name: string;
    gender: "male" | "female" | "男" | "女";
    birth_date: string;
    birth_time?: string;
    birth_location?: string;
    calendar_type?: "solar" | "lunar";
    sect?: 1 | 2;
    true_solar_mode?: "auto" | "on" | "off";
    longitude?: number;
    day_rollover_hour?: number;
}
export interface BaziFlowToolInput {
    chart?: BaziChart;
    persona_slug?: string;
    base_dir?: string;
    at?: string;
    include_calendar?: boolean;
    lang?: SupportedLanguage;
}
export interface CalendarToolInput {
    at?: string;
    lang?: SupportedLanguage;
}
export interface ChatImportToolInput {
    source_type: "text" | "json" | "ocr_text";
    payload: string | Record<string, unknown> | Array<unknown>;
    persona_slug?: string;
    timezone?: string;
    max_candidates?: number;
}
export interface PersonaDataToolInput {
    action: "list" | "search" | "create" | "query" | "patch" | "delete";
    base_dir?: string;
    persona_slug?: string;
    search_query?: string;
    create_payload?: {
        slug?: string;
        profile?: Partial<PersonaProfile>;
        relationship?: string;
        initial_facts?: string[];
        chart?: BaziChart;
        snapshot?: PersonaSnapshot;
        memory?: PersonaMemoryEntry[];
    };
    patch_payload?: {
        memory_append?: PersonaMemoryEntry[];
        snapshot_replace?: Partial<PersonaSnapshot>;
        profile_patch?: Partial<PersonaProfile>;
        relationship?: string;
        analysis_mode?: "normal" | "cheatsheet";
    };
}
export interface MemoryToolInput {
    action: "upsert" | "merge" | "delete" | "query";
    persona_slug: string;
    base_dir?: string;
    memories?: PersonaMemoryEntry[];
    merge_policy?: "append" | "replace_same_key" | "higher_confidence_wins";
    query?: string;
}
