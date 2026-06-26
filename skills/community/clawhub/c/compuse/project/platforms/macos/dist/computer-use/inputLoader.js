import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let cached;
export function requireComputerUseInput() {
    if (cached)
        return cached;
    throw new Error('Legacy native input loader was retained only for source-history reference. ' +
        'The standalone runtime now uses the Python bridge in src/computer-use/pythonBridge.ts instead.');
}
//# sourceMappingURL=inputLoader.js.map