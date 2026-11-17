# Release — Signing, R8, Bundles, and Versioning

The release build is a different app from the debug build: different code (R8), different resources (shrinking), different signature, different behavior. Everything that only breaks in production breaks here first, if you test here.

**Contents:** [Signing Identities](#signing-identities) · [Keystore Handling](#keystore-handling) · [Versioning](#versioning) · [R8](#r8) · [Keep Rules](#keep-rules) · [Resource Shrinking](#resource-shrinking) · [App Bundles and Splits](#app-bundles-and-splits) · [Native Libraries](#native-libraries) · [The Release Checklist](#the-release-checklist) · [Release Traps](#release-traps)

**Before building a release**, read `## Release Setup` in `~/Clawic/data/android/memory.md` (signing pointers, alias, fingerprints, versionCode scheme) and the last rows of `releases/<year>.md`. The previous release's versionCode is not a guess.

## Signing Identities

Three certificates get confused constantly, and mixing them up produces failures that look like something else:

| Identity | Who holds it | What it does |
|---|---|---|
| Debug key | Generated locally, shared conventions, no secrecy | Signs debug builds; its fingerprint is what you register for development services |
| Upload key | You | Signs what you upload to the store; the store verifies and strips it |
| App signing key | The store, under app signing, or you if you opted out | Signs what users actually install; determines whether an update is accepted |

- With store-managed app signing, **losing the upload key is recoverable** (request a key reset) and losing the app signing key is not your problem, because you never had it. Opting out means you hold the only copy of a key whose loss ends the app's ability to ship updates to existing users, ever.
- Anything verifying your app by certificate — App Links assetlinks files, map and sign-in service registrations, payment integrations — needs the **app signing** certificate's fingerprint for production and the **debug** certificate's for development. Using the upload key's fingerprint is the standard reason App Links silently fail to verify (`lifecycle.md`).
- Certificate fingerprints are public. They ship inside every APK and appear in the store console; keeping them in `## Release Setup` is correct and useful (`memory-template.md`).

## Keystore Handling

- The keystore file and its passwords never live in the repository, never in a build file, never in a checked-in properties file. The build reads them from the environment or from a properties file outside version control, and the values are stored in the user's own secret manager.
- In notes and memory, always the pointer, never the value: `keychain:android-upload-key`, `1password:Work/Android/keystore`, `file:~/keystores/upload.jks`. That rule covers the whole of `~/Clawic/data/`, including files created later (SKILL.md data paragraph).
- Back the keystore up somewhere that survives losing the machine, and **verify the backup restores** on a cadence — a keystore backup nobody has ever restored is a belief. That verification is a `## Due` row.
- `Keystore was tampered with, or password was incorrect` means wrong password or wrong file, not corruption. Verify against the pointer; never paste a password anywhere to test it.
- Rotating the upload key is a supported request to the store. Rotating a self-managed app signing key on already-published apps is effectively impossible — one more reason to use store-managed signing.

## Versioning

- `versionCode` is an integer that must strictly increase per upload, with a ceiling of 2,100,000,000. `versionName` is a display string with no rules and no meaning to the system.
- A scheme that works: a date-derived prefix plus a build counter, which stays comfortably under the ceiling and sorts chronologically. A millisecond timestamp does not fit. Pure incrementing counters work but tell you nothing when reading a crash report.
- Multiple APKs from one bundle get distinct version codes internally; with a bundle, you supply one and the store handles the splits.
- **There is no downgrade on the store.** A rollback is a new build with a higher versionCode, produced from the previous tag. That only works if the release row recorded the tag and the toolchain (SKILL.md Rule 9).
- Tag every release in version control at the commit that produced the artifact, and record the tag in the release row — "which commit is in production" must be answerable in one lookup, during an incident.

## R8

- R8 does four things at once: shrinks (removes unreachable code), optimizes, obfuscates (renames), and desugars. `minifyEnabled true` on release turns all of it on; resource shrinking is a separate flag that depends on it.
- On from the first release (SKILL.md Rule 8). Enabling it later means discovering every reflection assumption at once, in the build you can least afford to iterate on.
- Full-mode optimizations are more aggressive and occasionally require additional keep rules for libraries that were tolerant of the older behavior. Adopt it deliberately, with a full pass over the release variant.
- What R8 cannot see: anything reached by name at runtime — reflection, JNI, class names in configuration or annotations, `Class.forName`, serialization by reflective field access, and anything the framework instantiates from the manifest (which the plugin's generated rules already cover).
- Always test the **release variant** before shipping: install it on a device and walk the critical journeys, including the paths that only run for existing users (migrations, restored state). A smoke test against the minified variant in CI catches the rest (`testing.md`).

## Keep Rules

- Write the narrowest rule that works. `-keep class com.example.** { *; }` keeps a package's entire surface and quietly cancels most of R8's benefit for that code.
- Prefer, in order: a code-generating serializer that needs no rules at all; a keep-members rule scoped to the specific classes; an annotation-based keep on the handful of classes that need it; a package-wide rule only as a temporary measure with a dated comment.
- The library's own consumer rules ship with the library and are applied automatically. If a library's usage breaks under R8, check whether it ships consumer rules before writing your own — most do.
- The missing-classes diagnostic generates a suggested rules file. It is a starting point: adding it wholesale silences the diagnostic and keeps references that were genuinely unused.
- **Every keep rule needs a comment saying why.** An unexplained rule survives one cleanup pass and gets deleted in the next, and the crash returns. The set of rules that fixed a real crash goes in `artifacts/keep-rules-<name>.md` with its reasons (`memory-template.md`).
- Keep the source-file and line-number attributes so stack traces stay useful after deobfuscation, and rename the source file to a constant so the attribute leaks nothing (`crashes.md`).

## Resource Shrinking

- Removes resources not referenced from the kept code. Resources reached by name — a drawable looked up by string, a layout inflated from a name in configuration — are invisible to it, and the failure is a resource-not-found exception in release only.
- A keep specification file declares those, in the same narrow spirit as code keep rules.
- Strict mode for resource shrinking also removes resources referenced only through dynamic lookups, which is more aggressive and needs the keep list to be right.
- Language and density stripping belongs to bundle splits, not to shrinking; do not maintain a hand-written list of locales when the store can deliver only what the device needs.

## App Bundles and Splits

- The bundle is the upload format; the store generates and signs per-device APKs from it. The user downloads one architecture, one density and their own languages, which is the largest easy size win available (`performance.md`).
- Test what users will actually install by generating device-specific APKs from the bundle locally with the bundle tool, and installing those — a universal APK built for convenience is not what ships and can hide an ABI or density problem.
- Dynamic feature modules deliver code on demand; asset packs deliver large media. Both add complexity and failure paths (the feature not installed, the download failing offline), so they earn their place on genuinely large payloads only.
- The store enforces a size cap on the compressed download; anything beyond it moves to asset packs or on-demand delivery. Verify the current figure on the store's own documentation before designing around a remembered number (`play-console.md`).

## Native Libraries

- Only ship the ABIs you need. Both 64-bit and 32-bit variants exist for the common architectures, and the store has required 64-bit support for years; shipping an unnecessary 32-bit variant is dead weight that splits do not remove if you packaged it deliberately.
- Native crashes need the unstripped symbols for the exact build to be readable; upload them with the bundle or keep them alongside the mapping file (`crashes.md`).
- Native memory page-size compatibility has become a platform requirement direction; a library built for the older assumption fails to load on newer devices. When a native library fails to load only on recent devices, that is the first hypothesis.
- A library that fails to load on one architecture only is nearly always a packaging problem, not a code problem.

## The Release Checklist

Before uploading:

- `versionCode` strictly higher than the last shipped one, and `versionName` matching the tag
- The release variant installed on a physical device and walked through the critical journeys, including an **update over the previous version**, not only a fresh install
- Process-death check on the main screens (`lifecycle.md`)
- No debug-only dependency, logging interceptor, test endpoint or leak detector in the release variant
- `mapping.txt` and native symbols kept and their location recorded in the release row
- Permissions in the **merged** manifest reviewed — including any a new dependency introduced (`permissions.md`)
- Every declaration form still consistent with what the app now does (`play-console.md`)
- Data safety answers still accurate after any new SDK
- The release row written to `releases/<year>.md` before the rollout starts (SKILL.md Rule 9)

## Release Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Enabling R8 late in the project's life | Every reflection assumption fails at once | On from v1 |
| `-keep class com.example.** { *; }` | Cancels shrinking and obfuscation for the whole package | Narrow rules, with comments |
| Testing only a fresh install | Update-only bugs (migrations, restored state, stale caches) ship | Install the previous version, then update over it |
| Using the upload certificate's fingerprint for App Links | Verification silently fails in production | The app signing certificate's fingerprint |
| Keystore or passwords in the repository | Irreversible once pushed; the key must then be rotated | Environment or an out-of-tree properties file, values in a secret manager |
| A keystore backup nobody has restored | Discovered to be unusable at the worst moment | Verify the restore on a `## Due` cadence |
| Shipping a universal APK to test | Not what users install; hides ABI and density issues | Generate device APKs from the bundle |
| Discarding `mapping.txt` | That build's crashes are unreadable forever | Keep it, and put its location in the release row in `releases/<year>.md` |
| Millisecond timestamps as versionCode | Exceeds the integer ceiling | Date prefix plus counter |
| An unexplained keep rule | Deleted in the next cleanup; the crash returns | Comment the reason; keep the set in `artifacts/` |

## Write Down What It Was

- **The release row** — date, versionName, versionCode, track, rollout, tag, where the mapping went — goes to `releases/<year>.md` before the rollout starts, and gets its vitals columns about 48 hours later (`memory-template.md`).
- **Signing facts** — app signing on or off, alias, fingerprints, the pointer to the keystore — live in `## Release Setup` of `~/Clawic/data/android/memory.md`. Pointers only; a password appearing there is a bug to fix immediately.
- **A keep-rule set that fixed something**, with the reason for each rule, is `artifacts/keep-rules-<name>.md` with its `## Boxes` line.
- **The keystore backup verification** is a `## Due` row, not a good intention.
