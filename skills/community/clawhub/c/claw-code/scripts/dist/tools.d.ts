import { PortingBacklog, PortingModule } from './models.js';
import { ToolPermissionContext } from './permissions.js';
export interface ToolExecution {
    readonly name: string;
    readonly source_hint: string;
    readonly payload: string;
    readonly handled: boolean;
    readonly message: string;
}
export declare const PORTED_TOOLS: readonly PortingModule[];
export declare function buildToolBacklog(): PortingBacklog;
export declare function toolNames(): string[];
export declare function getTool(name: string): PortingModule | undefined;
export declare function filterToolsByPermissionContext(tools: readonly PortingModule[], permissionContext: ToolPermissionContext | undefined): readonly PortingModule[];
export declare function getTools(simpleMode?: boolean, includeMcp?: boolean, permissionContext?: ToolPermissionContext): readonly PortingModule[];
export declare function findTools(query: string, limit?: number): readonly PortingModule[];
export declare function executeTool(name: string, payload?: string): ToolExecution;
export declare function renderToolIndex(limit?: number, query?: string): string;
