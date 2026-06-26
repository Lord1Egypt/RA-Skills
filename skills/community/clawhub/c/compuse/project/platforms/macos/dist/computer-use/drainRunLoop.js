import { logDebug } from '../lib/log.js';
import { withResolvers } from '../lib/withResolvers.js';
import { requireComputerUseSwift } from './swiftLoader.js';
let pump;
let pending = 0;
const TIMEOUT_MS = 30_000;
function retain() {
    pending += 1;
    if (!pump) {
        pump = setInterval(() => requireComputerUseSwift()._drainMainRunLoop(), 1);
        logDebug('drain run loop started');
    }
}
function release() {
    pending -= 1;
    if (pending <= 0 && pump) {
        clearInterval(pump);
        pump = undefined;
        pending = 0;
        logDebug('drain run loop stopped');
    }
}
export const retainPump = retain;
export const releasePump = release;
export async function drainRunLoop(fn) {
    retain();
    let timer;
    try {
        const work = fn();
        work.catch(() => { });
        const timeout = withResolvers();
        timer = setTimeout(() => timeout.reject(new Error(`computer-use native call exceeded ${TIMEOUT_MS}ms`)), TIMEOUT_MS);
        return await Promise.race([work, timeout.promise]);
    }
    finally {
        if (timer)
            clearTimeout(timer);
        release();
    }
}
//# sourceMappingURL=drainRunLoop.js.map