import { PortingBacklog, PortingModule } from './models.js';
export interface CommandExecution {
    readonly name: string;
    readonly source_hint: string;
    readonly prompt: string;
    readonly handled: boolean;
    readonly message: string;
}
export declare const PORTED_COMMANDS: readonly PortingModule[];
export declare function builtInCommandNames(): ReadonlySet<string>;
export declare function buildCommandBacklog(): PortingBacklog;
export declare function commandNames(): string[];
export declare function getCommand(name: string): PortingModule | undefined;
export declare function getCommands(_cwd?: string, includePluginCommands?: boolean, includeSkillCommands?: boolean): readonly PortingModule[];
export declare function findCommands(query: string, limit?: number): readonly PortingModule[];
export declare function executeCommand(name: string, prompt?: string): CommandExecution;
export declare function renderCommandIndex(limit?: number, query?: string): string;
