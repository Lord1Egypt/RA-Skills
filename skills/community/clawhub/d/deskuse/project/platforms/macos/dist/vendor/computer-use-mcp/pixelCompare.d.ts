/**
 * Staleness guard ported from the Vercept acquisition.
 *
 * Compares the model's last-seen screenshot against a fresh-right-now
 * screenshot at the click target, so the model never clicks pixels it hasn't
 * seen. If the 9×9 patch around the target differs, the click is aborted and
 * the model is told to re-screenshot. This is NOT a popup detector.
 *
 * Semantics preserved exactly:
 *   - Skip on no `lastScreenshot` (cold start) — click proceeds.
 *   - Skip on any internal error (crop throws, screenshot fails, etc.) —
 *     click proceeds. Validation failure must never block the action.
 *   - 9×9 exact byte equality on raw pixel bytes. No fuzzing, no tolerance.
 *   - Compare in percentage coords so Retina scale doesn't matter.
 *
 * JPEG decode + crop is INJECTED via `ComputerUseHostAdapter.cropRawPatch`.
 * The original used `sharp` (LGPL, native `.node` addon); we inject Electron's
 * `nativeImage` (Chromium decoders, BSD, nothing to bundle) from the host, so
 * this package never imports it — the crop is a function parameter.
 */
import type { ScreenshotResult } from "./executor.js";
import type { Logger } from "./types.js";
/** Injected by the host. See `ComputerUseHostAdapter.cropRawPatch`. */
export type CropRawPatchFn = (jpegBase64: string, rect: {
    x: number;
    y: number;
    width: number;
    height: number;
}) => Buffer | null;
export interface PixelCompareResult {
    /** true → click may proceed. false → patch changed, abort the click. */
    valid: boolean;
    /** true → validation did not run (cold start, sub-gate off, or internal
     * error). The caller MUST treat this identically to `valid: true`. */
    skipped: boolean;
    /** Populated when valid === false. Returned to the model verbatim. */
    warning?: string;
}
/**
 * Compare the same patch location between two screenshots.
 *
 * @returns true when the raw pixel bytes are identical. false on any
 * difference, or on any internal error (the caller treats an error here as
 * `skipped`, so the false is harmless).
 */
export declare function comparePixelAtLocation(crop: CropRawPatchFn, lastScreenshot: ScreenshotResult, freshScreenshot: ScreenshotResult, xPercent: number, yPercent: number, gridSize?: number): boolean;
/**
 * Battle-tested click-target validation ported from the Vercept acquisition,
 * with the fresh-screenshot capture delegated to the caller (we don't have
 * a global `SystemActions.takeScreenshot()` — the executor is injected).
 *
 * Skip conditions (any of these → `{ valid: true, skipped: true }`):
 *   - `lastScreenshot` is undefined (cold start).
 *   - `takeFreshScreenshot()` throws or returns null.
 *   - Injected crop function returns null (decode failure).
 *   - Any other exception.
 *
 * The caller decides whether to invoke this at all (sub-gate check lives
 * in toolCalls.ts, not here).
 */
export declare function validateClickTarget(crop: CropRawPatchFn, lastScreenshot: ScreenshotResult | undefined, xPercent: number, yPercent: number, takeFreshScreenshot: () => Promise<ScreenshotResult | null>, logger: Logger, gridSize?: number): Promise<PixelCompareResult>;
