// Commands – mirrored command entries loaded from snapshot
// Mirrored from Python src/commands.py
import { PortingBacklog, PortingModule } from './models.js';
// Module-level cached snapshot (replaces Python's @lru_cache)
const _PORTED_COMMANDS = (() => {
    const entries = [
        { name: 'help', source_hint: 'commands/help/help.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/help/help.tsx' },
        { name: 'init', source_hint: 'commands/init.ts', responsibility: 'Command module mirrored from archived TypeScript path commands/init.ts' },
        { name: 'commit', source_hint: 'commands/commit.ts', responsibility: 'Command module mirrored from archived TypeScript path commands/commit.ts' },
        { name: 'branch', source_hint: 'commands/branch/branch.ts', responsibility: 'Command module mirrored from archived TypeScript path commands/branch/branch.ts' },
        { name: 'diff', source_hint: 'commands/diff/diff.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/diff/diff.tsx' },
        { name: 'status', source_hint: 'commands/status/status.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/status/status.tsx' },
        { name: 'session', source_hint: 'commands/session/session.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/session/session.tsx' },
        { name: 'resume', source_hint: 'commands/resume/resume.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/resume/resume.tsx' },
        { name: 'model', source_hint: 'commands/model/model.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/model/model.tsx' },
        { name: 'config', source_hint: 'commands/config/config.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/config/config.tsx' },
        { name: 'plan', source_hint: 'commands/plan/plan.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/plan/plan.tsx' },
        { name: 'compact', source_hint: 'commands/compact/compact.ts', responsibility: 'Command module mirrored from archived TypeScript path commands/compact/compact.ts' },
        { name: 'cost', source_hint: 'commands/cost/cost.ts', responsibility: 'Command module mirrored from archived TypeScript path commands/cost/cost.ts' },
        { name: 'usage', source_hint: 'commands/usage/usage.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/usage/usage.tsx' },
        { name: 'skills', source_hint: 'commands/skills/skills.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/skills/skills.tsx' },
        { name: 'memory', source_hint: 'commands/memory/memory.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/memory/memory.tsx' },
        { name: 'doctor', source_hint: 'commands/doctor/doctor.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/doctor/doctor.tsx' },
        { name: 'exit', source_hint: 'commands/exit/exit.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/exit/exit.tsx' },
        { name: 'clear', source_hint: 'commands/clear/clear.ts', responsibility: 'Command module mirrored from archived TypeScript path commands/clear/clear.ts' },
        { name: 'theme', source_hint: 'commands/theme/theme.tsx', responsibility: 'Command module mirrored from archived TypeScript path commands/theme/theme.tsx' },
    ];
    return entries.map((e) => new PortingModule({
        name: e.name,
        responsibility: e.responsibility,
        source_hint: e.source_hint,
        status: 'mirrored',
    }));
})();
export const PORTED_COMMANDS = _PORTED_COMMANDS;
const _BUILTIN_NAMES = new Set(_PORTED_COMMANDS.map((m) => m.name));
export function builtInCommandNames() {
    return _BUILTIN_NAMES;
}
export function buildCommandBacklog() {
    return new PortingBacklog({ title: 'Command surface', modules: PORTED_COMMANDS });
}
export function commandNames() {
    return PORTED_COMMANDS.map((m) => m.name);
}
export function getCommand(name) {
    const needle = name.toLowerCase();
    return PORTED_COMMANDS.find((m) => m.name.toLowerCase() === needle);
}
export function getCommands(_cwd, includePluginCommands = true, includeSkillCommands = true) {
    let commands = PORTED_COMMANDS;
    if (!includePluginCommands) {
        commands = commands.filter((m) => !m.source_hint.toLowerCase().includes('plugin'));
    }
    if (!includeSkillCommands) {
        commands = commands.filter((m) => !m.source_hint.toLowerCase().includes('skills'));
    }
    return commands;
}
export function findCommands(query, limit = 20) {
    const needle = query.toLowerCase();
    const matches = PORTED_COMMANDS.filter((m) => m.name.toLowerCase().includes(needle) ||
        m.source_hint.toLowerCase().includes(needle));
    return matches.slice(0, limit);
}
export function executeCommand(name, prompt = '') {
    const module = getCommand(name);
    if (module === undefined) {
        return {
            name,
            source_hint: '',
            prompt,
            handled: false,
            message: `Unknown mirrored command: ${name}`,
        };
    }
    const message = `Mirrored command '${module.name}' from ${module.source_hint} would handle prompt ${JSON.stringify(prompt)}.`;
    return {
        name: module.name,
        source_hint: module.source_hint,
        prompt,
        handled: true,
        message,
    };
}
export function renderCommandIndex(limit = 20, query) {
    const modules = query ? findCommands(query, limit) : PORTED_COMMANDS.slice(0, limit);
    const lines = [`Command entries: ${PORTED_COMMANDS.length}`, ''];
    if (query) {
        lines.push(`Filtered by: ${query}`);
        lines.push('');
    }
    lines.push(...modules.map((m) => `- ${m.name} — ${m.source_hint}`));
    return lines.join('\n');
}
