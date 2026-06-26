// Tools – mirrored tool entries loaded from snapshot JSON
// Mirrored from Python src/tools.py
import { PortingBacklog, PortingModule } from './models.js';
// Module-level cached snapshot (replaces Python's @lru_cache)
const _PORTED_TOOLS = (() => {
    const entries = [
        { name: 'AgentTool', source_hint: 'tools/AgentTool/AgentTool.tsx', responsibility: 'Tool module mirrored from archived TypeScript path tools/AgentTool/AgentTool.tsx' },
        { name: 'BashTool', source_hint: 'tools/BashTool/BashTool.tsx', responsibility: 'Tool module mirrored from archived TypeScript path tools/BashTool/BashTool.tsx' },
        { name: 'FileReadTool', source_hint: 'tools/FileReadTool/FileReadTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/FileReadTool/FileReadTool.ts' },
        { name: 'FileEditTool', source_hint: 'tools/FileEditTool/FileEditTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/FileEditTool/FileEditTool.ts' },
        { name: 'FileWriteTool', source_hint: 'tools/FileWriteTool/FileWriteTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/FileWriteTool/FileWriteTool.ts' },
        { name: 'GlobTool', source_hint: 'tools/GlobTool/GlobTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/GlobTool/GlobTool.ts' },
        { name: 'GrepTool', source_hint: 'tools/GrepTool/GrepTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/GrepTool/GrepTool.ts' },
        { name: 'PowerShellTool', source_hint: 'tools/PowerShellTool/PowerShellTool.tsx', responsibility: 'Tool module mirrored from archived TypeScript path tools/PowerShellTool/PowerShellTool.tsx' },
        { name: 'SkillTool', source_hint: 'tools/SkillTool/SkillTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/SkillTool/SkillTool.ts' },
        { name: 'TaskCreateTool', source_hint: 'tools/TaskCreateTool/TaskCreateTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/TaskCreateTool/TaskCreateTool.ts' },
        { name: 'TaskListTool', source_hint: 'tools/TaskListTool/TaskListTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/TaskListTool/TaskListTool.ts' },
        { name: 'WebFetchTool', source_hint: 'tools/WebFetchTool/WebFetchTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/WebFetchTool/WebFetchTool.ts' },
        { name: 'WebSearchTool', source_hint: 'tools/WebSearchTool/WebSearchTool.ts', responsibility: 'Tool module mirrored from archived TypeScript path tools/WebSearchTool/WebSearchTool.ts' },
    ];
    return entries.map((e) => new PortingModule({
        name: e.name,
        responsibility: e.responsibility,
        source_hint: e.source_hint,
        status: 'mirrored',
    }));
})();
export const PORTED_TOOLS = _PORTED_TOOLS;
export function buildToolBacklog() {
    return new PortingBacklog({ title: 'Tool surface', modules: PORTED_TOOLS });
}
export function toolNames() {
    return PORTED_TOOLS.map((m) => m.name);
}
export function getTool(name) {
    const needle = name.toLowerCase();
    return PORTED_TOOLS.find((m) => m.name.toLowerCase() === needle);
}
export function filterToolsByPermissionContext(tools, permissionContext) {
    if (permissionContext === undefined)
        return tools;
    return tools.filter((m) => !permissionContext.blocks(m.name));
}
export function getTools(simpleMode = false, includeMcp = true, permissionContext) {
    let tools = PORTED_TOOLS;
    if (simpleMode) {
        tools = tools.filter((m) => ['BashTool', 'FileReadTool', 'FileEditTool'].includes(m.name));
    }
    if (!includeMcp) {
        tools = tools.filter((m) => !m.name.toLowerCase().includes('mcp') &&
            !m.source_hint.toLowerCase().includes('mcp'));
    }
    return filterToolsByPermissionContext(tools, permissionContext);
}
export function findTools(query, limit = 20) {
    const needle = query.toLowerCase();
    const matches = PORTED_TOOLS.filter((m) => m.name.toLowerCase().includes(needle) ||
        m.source_hint.toLowerCase().includes(needle));
    return matches.slice(0, limit);
}
export function executeTool(name, payload = '') {
    const module = getTool(name);
    if (module === undefined) {
        return {
            name,
            source_hint: '',
            payload,
            handled: false,
            message: `Unknown mirrored tool: ${name}`,
        };
    }
    const message = `Mirrored tool '${module.name}' from ${module.source_hint} would handle payload ${JSON.stringify(payload)}.`;
    return {
        name: module.name,
        source_hint: module.source_hint,
        payload,
        handled: true,
        message,
    };
}
export function renderToolIndex(limit = 20, query) {
    const modules = query ? findTools(query, limit) : PORTED_TOOLS.slice(0, limit);
    const lines = [`Tool entries: ${PORTED_TOOLS.length}`, ''];
    if (query) {
        lines.push(`Filtered by: ${query}`);
        lines.push('');
    }
    lines.push(...modules.map((m) => `- ${m.name} — ${m.source_hint}`));
    return lines.join('\n');
}
