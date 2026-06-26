/**
 * Key combos that cross app boundaries or terminate processes. Gated behind
 * the `systemKeyCombos` grant flag. When that flag is off, the `key` tool
 * rejects these and returns a tool error telling the model to request the
 * flag; all other combos work normally.
 *
 * Matching is canonicalized: every modifier alias the Rust executor accepts
 * collapses to one canonical name. Without this, `command+q` / `meta+q` /
 * `cmd+alt+escape` bypass the gate — see keyBlocklist.test.ts for the three
 * bypass forms and the Rust parity check that catches future alias drift.
 */
/**
 * Normalize "Cmd + Shift + Q" → "shift+meta+q": lowercase, trim, alias →
 * canonical, dedupe, sort modifiers, non-modifiers last.
 */
export declare function normalizeKeySequence(seq: string): string;
/**
 * True if the sequence would fire a blocked OS shortcut.
 *
 * Checks mods + EACH non-modifier key individually, not just the full
 * joined string. `cmd+q+a` → Rust presses Cmd, then Q (Cmd+Q fires here),
 * then A. Exact-match against "meta+q+a" misses; checking "meta+q" and
 * "meta+a" separately catches the Q.
 *
 * Modifiers-only sequences ("cmd+shift") are checked as-is — no key to
 * pair with, and no blocklist entry is modifier-only, so this is a no-op
 * that falls through to false. Covers the click-modifier case where
 * `left_click(text="cmd")` is legitimate.
 */
export declare function isSystemKeyCombo(seq: string, platform: "darwin" | "win32"): boolean;
export declare const _test: {
    CANONICAL_MODIFIER: Readonly<Record<string, string>>;
    BLOCKED_DARWIN: Set<string>;
    BLOCKED_WIN32: Set<string>;
    MODIFIER_ORDER: string[];
};
