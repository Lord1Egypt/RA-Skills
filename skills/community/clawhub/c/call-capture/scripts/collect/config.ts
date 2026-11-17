/**
 * The two choices this collector needs. The credential is not one of them:
 * it is a workspace environment variable, per `references/providers.md`.
 */
import type { RecorderSlug } from "./recorders";

/**
 * PLACEHOLDER — which recorder records your calls. Typed against the registry,
 * so an unknown slug fails `npm run typecheck`; `--list` prints the nine that
 * ship. A valid-but-wrong one reports a clean empty run forever, and only a
 * reader catches that.
 */
export const RECORDER: RecorderSlug = "avoma";

/** PLACEHOLDER — your own email domain, or every standup is an account. */
export const INTERNAL_DOMAIN = "example.com";
