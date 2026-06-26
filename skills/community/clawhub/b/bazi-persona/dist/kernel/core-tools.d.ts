import { queryChineseCalendar } from "../tools/calendar/query.js";
import type { BaziChartToolInput, BaziFlowToolInput, CalendarToolInput, ChatImportToolInput, MemoryToolInput, PersonaConversationEntry, PersonaDataToolInput, PersonaMemoryEntry, PersonaRecord, PromptPack, PersonaKnowledge } from "./types.js";
export interface ToolRuntimeContext {
    promptPack: PromptPack;
    knowledge: PersonaKnowledge;
}
export declare function bazi_chart_tool(input: BaziChartToolInput): Promise<{
    chart: PersonaRecord["chart"];
}>;
export declare function calendar_tool(input: CalendarToolInput): Promise<{
    at: string;
    calendar: Awaited<ReturnType<typeof queryChineseCalendar>>;
}>;
export declare function bazi_flow_tool(input: BaziFlowToolInput, context: ToolRuntimeContext): Promise<{
    persona_slug?: string;
    at: string;
    flow: PersonaRecord["snapshot"]["evidence"];
    calendar: Awaited<ReturnType<typeof queryChineseCalendar>> | undefined;
}>;
export declare function chat_import_tool(input: ChatImportToolInput): Promise<{
    source_type: ChatImportToolInput["source_type"];
    timezone: string;
    candidates: PersonaConversationEntry[];
    memories: PersonaMemoryEntry[];
}>;
export declare function persona_data_tool(input: PersonaDataToolInput, context: ToolRuntimeContext): Promise<unknown>;
export declare function memory_tool(input: MemoryToolInput, context: ToolRuntimeContext): Promise<{
    action: MemoryToolInput["action"];
    persona_slug: string;
    count: number;
    created?: number;
    updated?: number;
    deleted?: number;
    items?: PersonaMemoryEntry[];
}>;
