"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.execFileText = execFileText;
exports.spawnCombined = spawnCombined;
const node_child_process_1 = require("node:child_process");
const node_util_1 = require("node:util");
const execFileAsync = (0, node_util_1.promisify)(node_child_process_1.execFile);
async function execFileText(command, args, options = {}) {
    const { stdout } = await execFileAsync(command, args, {
        cwd: options.cwd,
        env: options.env,
        encoding: 'utf8',
        maxBuffer: 1024 * 1024 * 8
    });
    return stdout;
}
async function spawnCombined(command, args, options = {}) {
    return await new Promise((resolve, reject) => {
        const child = (0, node_child_process_1.spawn)(command, args, {
            cwd: options.cwd,
            env: options.env,
            stdio: ['ignore', 'pipe', 'pipe']
        });
        let output = '';
        let settled = false;
        let timedOut = false;
        let timeout;
        const onChunk = (chunk) => {
            const text = chunk.toString();
            output += text;
            options.onData?.(text);
        };
        child.stdout?.on('data', onChunk);
        child.stderr?.on('data', onChunk);
        if (options.timeoutMs) {
            timeout = setTimeout(() => {
                timedOut = true;
                child.kill('SIGTERM');
            }, options.timeoutMs);
        }
        child.on('error', (error) => {
            if (timeout)
                clearTimeout(timeout);
            if (settled)
                return;
            settled = true;
            reject(Object.assign(error, { output, timedOut }));
        });
        child.on('close', (code) => {
            if (timeout)
                clearTimeout(timeout);
            if (settled)
                return;
            settled = true;
            if (timedOut) {
                const error = new Error('Process timed out');
                reject(Object.assign(error, { output, timedOut: true, code: code ?? -1 }));
                return;
            }
            if ((code ?? 1) !== 0) {
                const error = new Error(`Process exited with code ${code ?? 1}`);
                reject(Object.assign(error, { output, timedOut: false, code: code ?? 1 }));
                return;
            }
            resolve({ output, code: code ?? 0, timedOut: false });
        });
    });
}
//# sourceMappingURL=process.js.map