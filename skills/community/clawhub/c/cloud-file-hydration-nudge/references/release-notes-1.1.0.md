# Release Notes - 1.1.0

## Scope

This is a 1.1.0-class hardening update for `cloud-file-hydration-nudge`. The core pattern is unchanged: visible metadata is not proof of readable bytes, and every nudge must be verified with the same bounded read probe before downstream processing continues.

## Provenance

Developed from agent-assisted testing and review in a constrained macOS/OpenClaw environment; published by `@Talonpoint`.

## Tested Boundary

This update was retested on macOS after tightening OpenClaw node/helper control boundaries. Broad Node permissions were not restored, no new Node or helper-app permissions were added for the retest, the connected macOS node had no Accessibility or Screen Recording grant, and `system.run` plus `screen.snapshot` were not advertised. Quick Look automation remained deprecated and was not used.

Signed helper support for a narrow read-only File Provider inspection command remains pending upstream. When constrained helper/provider hydration is unavailable, leave unreadable placeholders pending and tell the user provider/manual hydration is needed.

## Platform Notes

The general pattern is portable: classify the provider, prove readability, use the least-invasive materialization path, and verify with the same read probe before continuing. macOS-specific mechanisms need platform-specific replacements on Linux and Windows.

Linux users should adapt the pattern to their sync client, mount, FUSE layer, provider CLI, or local-availability mechanism. Windows users should adapt it to OneDrive/Cloud Files placeholders, Explorer/provider status, PowerShell or provider tools, and Windows service/user-context permissions.

## Requested Feedback

Useful edits include provider-specific commands, placeholder/read-failure signatures, permission-boundary notes, and causal tests showing pre-nudge read failure followed by post-nudge read success.
