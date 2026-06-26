import { type ToolRuntimeContext } from "./core-tools.js";
export declare function workflow_create_persona(params: {
    args: Record<string, string>;
    context: ToolRuntimeContext;
}): Promise<string>;
export declare function workflow_update_persona(params: {
    args: Record<string, string>;
    context: ToolRuntimeContext;
}): Promise<string>;
export declare function workflow_chat(params: {
    args: Record<string, string>;
    context: ToolRuntimeContext;
}): Promise<string>;
export declare function workflow_query_flow(params: {
    args: Record<string, string>;
    context: ToolRuntimeContext;
}): Promise<string>;
export declare function workflow_query_calendar(params: {
    args: Record<string, string>;
}): Promise<string>;
export declare function workflow_import_chat(params: {
    args: Record<string, string>;
    context: ToolRuntimeContext;
}): Promise<string>;
export declare function workflow_persona_startup_injection(params: {
    args: Record<string, string>;
    context: ToolRuntimeContext;
}): Promise<string>;
