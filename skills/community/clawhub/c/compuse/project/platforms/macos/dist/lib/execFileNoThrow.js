import { execFile } from 'node:child_process';
export function execFileNoThrow(file, args, options = {}) {
    return new Promise(resolve => {
        const child = execFile(file, args, {
            cwd: options.useCwd === false ? undefined : process.cwd(),
            encoding: 'utf8',
            maxBuffer: 32 * 1024 * 1024,
        }, (error, stdout, stderr) => {
            const code = typeof error?.code === 'number'
                ? error.code
                : error
                    ? 1
                    : 0;
            resolve({ code, stdout: stdout ?? '', stderr: stderr ?? '' });
        });
        if (options.input !== undefined) {
            child.stdin?.end(options.input);
        }
    });
}
//# sourceMappingURL=execFileNoThrow.js.map