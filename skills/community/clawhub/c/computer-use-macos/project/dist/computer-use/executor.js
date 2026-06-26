import { API_RESIZE_PARAMS, targetImageSize } from '../vendor/computer-use-mcp/imageResize.js';
import { execFileNoThrow } from '../lib/execFileNoThrow.js';
import { sleep } from '../lib/sleep.js';
import { CLI_CU_CAPABILITIES, CLI_HOST_BUNDLE_ID } from './common.js';
import { callPythonHelper } from './pythonBridge.js';
const SCREENSHOT_JPEG_QUALITY = 0.75;
const MOVE_SETTLE_MS = 50;
function computeTargetDims(logicalW, logicalH, scaleFactor) {
    const physW = Math.round(logicalW * scaleFactor);
    const physH = Math.round(logicalH * scaleFactor);
    return targetImageSize(physW, physH, API_RESIZE_PARAMS);
}
function normalizeDisplayGeometry(display) {
    return {
        ...display,
        displayId: display.displayId ?? display.id,
        label: display.label ?? display.name,
    };
}
async function readClipboardViaPbpaste() {
    const { stdout, code } = await execFileNoThrow('pbpaste', [], { useCwd: false });
    if (code !== 0)
        throw new Error(`pbpaste exited with code ${code}`);
    return stdout;
}
async function writeClipboardViaPbcopy(text) {
    const { code } = await execFileNoThrow('pbcopy', [], { input: text, useCwd: false });
    if (code !== 0)
        throw new Error(`pbcopy exited with code ${code}`);
}
async function typeViaClipboard(text) {
    let saved;
    try {
        saved = await readClipboardViaPbpaste();
    }
    catch { }
    try {
        await writeClipboardViaPbcopy(text);
        await callPythonHelper('key', { keySequence: 'command+v', repeat: 1 });
        await sleep(100);
    }
    finally {
        if (typeof saved === 'string') {
            try {
                await writeClipboardViaPbcopy(saved);
            }
            catch { }
        }
    }
}
export function createCliExecutor(_opts) {
    if (process.platform !== 'darwin') {
        throw new Error(`createCliExecutor called on ${process.platform}. Computer control is macOS-only.`);
    }
    return {
        capabilities: {
            ...CLI_CU_CAPABILITIES,
            hostBundleId: CLI_HOST_BUNDLE_ID,
        },
        async prepareForAction() {
            return callPythonHelper('prepare_for_action', {});
        },
        async previewHideSet() {
            return callPythonHelper('preview_hide_set', {});
        },
        async getDisplaySize(displayId) {
            return normalizeDisplayGeometry(await callPythonHelper('get_display_size', { displayId }));
        },
        async listDisplays() {
            const displays = await callPythonHelper('list_displays', {});
            return displays.map(display => normalizeDisplayGeometry(display));
        },
        async findWindowDisplays(bundleIds) {
            return callPythonHelper('find_window_displays', { bundleIds });
        },
        async resolvePrepareCapture(opts) {
            const display = await this.getDisplaySize(opts.preferredDisplayId);
            const [targetW, targetH] = computeTargetDims(display.width, display.height, display.scaleFactor);
            const result = await callPythonHelper('resolve_prepare_capture', {
                preferredDisplayId: opts.preferredDisplayId,
                targetWidth: targetW,
                targetHeight: targetH,
                jpegQuality: SCREENSHOT_JPEG_QUALITY,
            });
            return {
                ...result,
                display: normalizeDisplayGeometry(result.display),
                resolvedDisplayId: result.resolvedDisplayId ?? result.displayId,
            };
        },
        async screenshot(opts) {
            const display = await this.getDisplaySize(opts.displayId);
            const [targetW, targetH] = computeTargetDims(display.width, display.height, display.scaleFactor);
            const result = await callPythonHelper('screenshot', {
                displayId: opts.displayId,
                targetWidth: targetW,
                targetHeight: targetH,
                jpegQuality: SCREENSHOT_JPEG_QUALITY,
            });
            return result;
        },
        async zoom(regionLogical, _allowedBundleIds, displayId) {
            const display = await this.getDisplaySize(displayId);
            const [outW, outH] = computeTargetDims(regionLogical.w, regionLogical.h, display.scaleFactor);
            return callPythonHelper('zoom', {
                x: regionLogical.x,
                y: regionLogical.y,
                width: regionLogical.w,
                height: regionLogical.h,
                targetWidth: outW,
                targetHeight: outH,
            });
        },
        async key(keySequence, repeat) {
            await callPythonHelper('key', { keySequence, repeat: repeat ?? 1 });
        },
        async holdKey(keyNames, durationMs) {
            await callPythonHelper('hold_key', { keyNames, durationMs });
        },
        async type(text, opts2) {
            if (opts2.viaClipboard) {
                await typeViaClipboard(text);
                return;
            }
            await callPythonHelper('type', { text });
        },
        readClipboard: readClipboardViaPbpaste,
        writeClipboard: writeClipboardViaPbcopy,
        async click(x, y, button, count, modifiers) {
            await callPythonHelper('click', { x, y, button, count, modifiers });
            await sleep(MOVE_SETTLE_MS);
        },
        async mouseDown() {
            await callPythonHelper('mouse_down', {});
        },
        async mouseUp() {
            await callPythonHelper('mouse_up', {});
        },
        async getCursorPosition() {
            return callPythonHelper('cursor_position', {});
        },
        async drag(from, to) {
            await callPythonHelper('drag', { from, to });
            await sleep(MOVE_SETTLE_MS);
        },
        async moveMouse(x, y) {
            await callPythonHelper('move_mouse', { x, y });
            await sleep(MOVE_SETTLE_MS);
        },
        async scroll(x, y, dx, dy) {
            await callPythonHelper('scroll', { x, y, deltaX: dx, deltaY: dy });
        },
        async getFrontmostApp() {
            return callPythonHelper('frontmost_app', {});
        },
        async appUnderPoint(x, y) {
            return callPythonHelper('app_under_point', { x, y });
        },
        async listInstalledApps() {
            return callPythonHelper('list_installed_apps', {});
        },
        async listRunningApps() {
            return callPythonHelper('list_running_apps', {});
        },
        async openApp(bundleId) {
            await callPythonHelper('open_app', { bundleId });
        },
    };
}
export async function unhideComputerUseApps(_bundleIds) {
    return;
}
//# sourceMappingURL=executor.js.map