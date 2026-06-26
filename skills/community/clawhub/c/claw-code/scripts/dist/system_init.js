// System Init – system initialization message builder
// Mirrored from Python src/system_init.py
import { builtInCommandNames, getCommands } from './commands.js';
import { getTools } from './tools.js';
import { runSetup } from './setup.js';
export function buildSystemInitMessage(trusted = true) {
    const commands = getCommands();
    const tools = getTools();
    const setupReport = runSetup(undefined, trusted);
    const lines = [
        '# System Init',
        '',
        `Trusted: ${trusted}`,
        `Built-in command names: ${builtInCommandNames().size}`,
        `Loaded command entries: ${commands.length}`,
        `Loaded tool entries: ${tools.length}`,
        '',
        'Startup steps:',
        ...setupReport.setup.startup_steps().map((step) => `- ${step}`),
    ];
    return lines.join('\n');
}
