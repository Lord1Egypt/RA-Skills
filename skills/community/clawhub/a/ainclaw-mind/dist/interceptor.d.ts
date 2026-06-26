/**
 * Interceptor — the main hook that fires on every intent.
 *
 * Flow:
 * 1. User issues an intent (e.g., "login to GitHub")
 * 2. Interceptor queries ClawMind Cloud for a matching Lobster macro
 * 3. If hit → execute the Lobster workflow directly (skip LLM exploration)
 * 4. If miss → passthrough to normal OpenClaw flow
 * 5. On success → contribute the trace back to the cloud
 * 6. On failure → report failure for circuit breaker tracking
 */
import type { OpenClawContext } from "./types.js";
export declare function interceptIntent(ctx: OpenClawContext): Promise<void>;
/**
 * Hook: called when a session completes successfully.
 * Compiles the session trace into a Lobster workflow and contributes it.
 */
export declare function onSessionComplete(ctx: OpenClawContext): Promise<void>;
