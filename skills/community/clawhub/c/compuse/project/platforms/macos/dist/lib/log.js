import { format } from 'node:util';
const enabled = process.env.CLAUDE_COMPUTER_USE_DEBUG === '1';
export function logDebug(message, ...args) {
    if (!enabled)
        return;
    process.stderr.write(`[claude-computer-use] ${format(message, ...args)}\n`);
}
export function logWarn(message, ...args) {
    process.stderr.write(`[claude-computer-use][warn] ${format(message, ...args)}\n`);
}
//# sourceMappingURL=log.js.map