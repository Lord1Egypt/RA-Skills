# Security — App Surface, Components, and What Attackers Read

Threat model first: the attacker has your APK, an emulator, root, and unlimited time. Everything you shipped, they read. What they cannot get is what your server refuses to give them.

**Contents:** [What Comes Out of an APK](#what-comes-out-of-an-apk) · [Secrets, and Where They Actually Live](#secrets-and-where-they-actually-live) · [Exported Components](#exported-components) · [PendingIntents and Intent Redirection](#pendingintents-and-intent-redirection) · [Deep Link Hijacking](#deep-link-hijacking) · [WebView](#webview) · [Data at Rest and Backup](#data-at-rest-and-backup) · [Integrity and Anti-Tamper](#integrity-and-anti-tamper) · [Logging and Debug Surfaces](#logging-and-debug-surfaces) · [A Pre-Release Security Pass](#a-pre-release-security-pass) · [Security Traps](#security-traps)

**Before a hardening pass**, read `## App Context` and any `artifacts/` entry the `## Boxes` index in `~/Clawic/data/android/memory.md` names for a security decision — a pinning choice, a keystore design, an accepted risk. Re-deciding an accepted risk without knowing it was accepted wastes the session.

## What Comes Out of an APK

An APK is a zip. Within a minute, with public tooling, an attacker has:

- The **manifest**: every component, every permission, every exported flag, every intent filter and every declared authority.
- **All resources and assets**: strings, configuration files, certificates, bundled data.
- **Decompiled code**: R8 renames symbols, it does not encrypt them. String literals survive intact, and control flow is readable.
- **`BuildConfig` constants**: compiled-in fields are literals in the bytecode.
- **Native libraries**: strings and symbols, with a little more effort.
- **Network behavior**: an interception proxy against a rooted device or emulator reveals every endpoint, header and payload the app sends.

Design consequence: the client is untrusted input to your backend. Every authorization decision happens server-side, on the server's own view of who the caller is.

## Secrets, and Where They Actually Live

| Kind of value | Where it belongs |
|---|---|
| API key for a third party that must be called directly | Nowhere in the app — proxy the call through your backend, which holds the key |
| Key that is public by design (a maps or analytics client id) | In the app, restricted server-side by package name and signing certificate so a copied key is useless elsewhere |
| User credentials | Never stored — exchange for a token at sign-in |
| Session or refresh token | The OS keystore-backed storage, short-lived, revocable server-side |
| Encryption key for local data | Generated on-device in the hardware-backed keystore, never leaving it (`data.md`) |
| Signing keystore and passwords | The developer's secret manager and CI secrets, never the repository (`release.md`) |

- Obfuscation, native storage, string splitting and encryption-with-a-hardcoded-key are all speed bumps that cost an attacker minutes. They are legitimate only as friction on top of a design that is safe when they fail.
- Restrict what you cannot hide: an API key that is necessarily in the client should be constrained server-side to your package name and signing certificate, and rate-limited.
- **In this skill's own notes, secrets are always pointers** — `keychain:…`, `env:…`, `1password:…` — and never values, anywhere under `~/Clawic/data/` (`memory-template.md`).

## Exported Components

- From targetSdk 31 every activity, service and receiver with an intent filter must declare `android:exported` explicitly, and the build fails otherwise. That requirement exists because the historical default was surprising.
- **Exported means any app on the device can invoke it.** For each exported component, ask: what does it do with the intent's extras, and what happens if a malicious app supplies them? An exported activity that reads a file path from an extra and displays its contents is a file-disclosure vulnerability.
- Protect what must be exported with a signature-level custom permission, so only apps signed by your key can call it. A `normal`-level custom permission protects nothing — any app can request it.
- Content providers are exported by default on very old targets and are the classic disclosure surface: enforce read and write permissions, use path-based restrictions, and never build SQL from a caller-supplied selection string.
- Broadcast receivers registered at runtime must declare exported or not-exported from targetSdk 34. A not-exported receiver is the correct default for internal events.

## PendingIntents and Intent Redirection

- A `PendingIntent` carries your app's identity to whoever holds it. `FLAG_IMMUTABLE` is the default choice; `FLAG_MUTABLE` is only for cases where a system component must fill in the intent (a direct-reply notification action), and a mutable one whose base intent is not fully specified lets the holder redirect it anywhere with your privileges.
- Always specify the target component explicitly in the wrapped intent. An implicit intent inside a mutable pending intent is the textbook escalation.
- **Intent redirection**: an exported component that takes an intent (or a URI) from an extra and starts or loads it is executing an attacker's choice with your permissions. Never forward an intent received from outside; extract the data you need and construct a new, explicit intent yourself.
- StrictMode's unsafe-intent-launch detection catches most of these during development (`debug.md`).

## Deep Link Hijacking

- A custom scheme (`myapp://`) can be registered by any app on the device. Whichever the user picks wins, and the user has no way to tell. Never deliver an authorization code, a token, or anything sensitive over a custom scheme.
- Verified App Links (`https` with autoverification and a well-known assets file on the domain, containing the **app signing** certificate fingerprint) cannot be claimed by another app, because the domain vouches for you. That is the only link type safe for auth callbacks (`lifecycle.md`).
- Auth flows should use the platform's browser-based flow with a verified redirect, plus a proof-key exchange so an intercepted code is useless.
- Treat every deep-link parameter as untrusted input: validate the destination against an allowlist, never navigate to an arbitrary URL from a parameter, and never construct a query from one.

## WebView

- A WebView with JavaScript enabled plus a JavaScript interface exposes the interface's methods to whatever page is loaded. If the page can ever be attacker-influenced — a redirect, an injected ad, a compromised CDN — that is remote code execution with your app's permissions.
- If an interface is unavoidable: annotate only the methods that are meant to be exposed, validate every argument, and check the origin of the page before responding.
- Disable file access and content access unless required; a WebView that can load `file://` URLs plus a JavaScript injection reads the app's private storage.
- Never disable TLS validation for a WebView, and never accept an SSL error callback. That callback exists to be rejected.
- Load only origins you control, from an allowlist, and prefer the system's custom-tab browser component over an in-app WebView for external content — it uses the user's browser, its updates and its security state instead of yours.

## Data at Rest and Backup

- Modern devices encrypt storage when the user has a screen lock; that covers the lost-device threat for most apps. Additional application-level encryption is for data that must resist a compromised device or that carries a regulatory requirement, and the key lives in the hardware-backed keystore (`data.md`).
- `android:allowBackup` defaults to true: app data leaves the device through cloud backup and device-to-device transfer. Sensitive files — token stores, caches of other people's data, offline databases — are excluded through the data-extraction rules, with separate rule sets for cloud backup and device transfer.
- A restore delivers old data into a new install and possibly a dead session. Handle that explicitly rather than crashing on the first launch after a transfer.
- Anything genuinely sensitive should also be re-derivable: an app that can recover from having its local data wiped has no backup problem at all.
- Do not write personal data to external or shared storage, where any app with the corresponding access can read it.

## Integrity and Anti-Tamper

- Client-side root, emulator and tamper detection can be bypassed by anyone with the app and an afternoon. It is friction against low-effort fraud, never a control, and it produces support tickets from legitimate users with unlocked bootloaders.
- The supported approach is a server-verified attestation: the app requests a verdict from the platform's integrity service, the **server** verifies it, and the server decides. A verdict evaluated on the client is worth exactly nothing.
- Use it where fraud has a monetary cost (payments, promotions, competitive games) and skip it elsewhere. Every check is friction for honest users.
- Repackaging protection follows from signature verification server-side, via the certificate the platform attests to — not from a self-check inside the app, which the repackager simply removes.

## Logging and Debug Surfaces

- Release builds log nothing sensitive. Any device with debugging enabled exposes logcat to a connected machine, and some logs are readable more broadly through bug reports the user shares.
- Debug-only tooling — logging interceptors, leak detectors, database inspectors, developer menus — enters through debug-only dependencies and debug source sets so it cannot ship. A runtime `if (BuildConfig.DEBUG)` still ships the code and the strings.
- The debuggable flag must be false in release; a debuggable release build lets any user attach a debugger and read process memory.
- Custom trust managers, cleartext exemptions and test endpoints belong in the debug network configuration, where the platform enforces that they cannot apply to a release build (`networking.md`).
- Screenshots and the recents thumbnail can leak content; the secure-window flag prevents both for screens showing sensitive data, at the cost of blocking legitimate screenshots too.

## A Pre-Release Security Pass

Run against the **merged** manifest and the release artifact:

- Every exported component is intentional, and each one validates its inputs
- Every `PendingIntent` is immutable, or mutable with a fully explicit base intent
- No component forwards an intent or a URI received from outside
- Custom permissions protecting components are signature-level
- No secret in `BuildConfig`, resources, assets or native strings — search the built artifact, not the source
- Backup rules exclude token stores and sensitive caches; `allowBackup` is a deliberate choice
- WebView: JavaScript and interfaces only where required, file access off, no SSL error suppression
- Auth callbacks arrive over verified App Links, never a custom scheme
- No debug tooling, verbose logging, test endpoint or debuggable flag in the release variant
- Dependencies scanned for known vulnerabilities, and the scan repeated on a cadence — a build that was clean six months ago is not clean now

## Security Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| API key in `BuildConfig`, resources, or native code | All three are extractable in minutes | Proxy server-side; restrict what must be client-side |
| Treating obfuscation as protection | R8 renames; it does not encrypt, and strings survive | Assume the code is readable |
| An exported component that trusts its extras | Any installed app can invoke it with anything | Validate, or set exported false |
| Mutable `PendingIntent` with an implicit intent | The holder redirects it with your privileges | Immutable, explicit target |
| Forwarding a received intent | Executes an attacker's choice as you | Extract data, build a new explicit intent |
| Auth callback over a custom scheme | Any app can register the same scheme | Verified App Links |
| `addJavascriptInterface` with a remote page | Remote code execution surface | Local content only, or no interface |
| Suppressing an SSL error in a WebView | Disables TLS for that content entirely | Never; fix the certificate |
| Client-side root detection as a control | Bypassed trivially; annoys legitimate users | Server-verified attestation, where fraud has a cost |
| Leaving `allowBackup` at its default with tokens on disk | The data leaves the device by design | Exclusion rules |
| A dependency scan run once at adoption | Vulnerabilities are published after you adopt | Scan on a `## Due` cadence |
| Storing a user's pasted log or bug report to investigate | It contains their tokens and personal data | Extract the trace, discard the rest |

## Write Down What It Was

- **A security decision and the risk accepted** — pinning or not, attestation or not, an exported component that must stay exported and why — is `artifacts/adr-<name>.md` with its `## Boxes` line. An accepted risk that is not written down gets re-litigated or, worse, silently reversed (`memory-template.md`).
- **The backup exclusion list and the encryption design** belong in the same artifact family, because they are also the source for Play's data-safety answers (`play-console.md`).
- **A vulnerability found and fixed** is a line in `## Pain Points` of `~/Clawic/data/android/memory.md`, with the class of bug, so the pre-release pass gains a check.
- **The dependency-scan cadence** is a row in `## Due`.
