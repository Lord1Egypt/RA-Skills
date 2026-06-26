// Setup – workspace setup and report
// Mirrored from Python src/setup.py
import { runDeferredInit } from './deferred_init.js';
import { startKeychainPrefetch, startMdmRawRead, startProjectScan } from './prefetch.js';
export class WorkspaceSetup {
    constructor(args) {
        this.python_version = args?.python_version ?? '3.12.0';
        this.implementation = args?.implementation ?? 'Node.js';
        this.platform_name = args?.platform_name ?? 'TypeScript Port';
        this.test_command = args?.test_command ?? 'python3 -m unittest discover -s tests -v';
    }
    startup_steps() {
        return [
            'start top-level prefetch side effects',
            'build workspace context',
            'load mirrored command snapshot',
            'load mirrored tool snapshot',
            'prepare parity audit hooks',
            'apply trust-gated deferred init',
        ];
    }
}
export function runSetup(_cwd, trusted = true) {
    const prefetches = [
        startMdmRawRead(),
        startKeychainPrefetch(),
        startProjectScan(_cwd ?? '<root>'),
    ];
    return {
        setup: new WorkspaceSetup(),
        prefetches,
        deferred_init: runDeferredInit(trusted),
        trusted,
        cwd: _cwd ?? '<cwd>',
    };
}
