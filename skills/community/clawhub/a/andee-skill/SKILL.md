---
name: andee-skill
description: Step-by-step, in English, for getting the Andee Android agent (github.com/kuafuai/andee — a floating ball that reads the screen and taps through any app) running for a real person. Use it when someone wants to (1) download/clone the Andee source, (2) build it locally with Gradle, install it on a phone and debug it over adb plus the device's own WebSocket tool port, or (3) skip all of that and have a pre-configured package built for them by CodeFlying. Covers the JDK 17-20 trap, the Android SDK setup, the on-device provisioning order, the build/install/debug loop, logcat tags, the WS request format, and how to hand an APK to someone else. Triggers: "install Andee", "build Andee", "debug Andee", "run Andee on my phone", "clone the andee repo", "codeflying Andee", "how do I try Andee", "turn my phone into an AI phone".
agent_created: true
---

# Andee — get it, build it, debug it

Andee is one Android app that turns a phone into an agent's body: an accessibility service that
reads and touches the screen, a `WindowManager` overlay that draws a floating ball with a face, and
an LLM behind it. No root, no custom ROM. It ships as a single APK.

- Upstream repository: **https://github.com/kuafuai/andee**
- Minimum device: **Android 11 (API 30)**, and it wants a **real phone** — an emulator runs it but
  almost nothing it does is meaningful there.
- Current release: **v0.2.0** (pre-1.0 on purpose).

Your job in this skill is **not** to recite all of this. It is to walk a human through **one route,
one step at a time**, confirming each step before you move on.

---

## Rule zero — ask which route before you touch anything

Do not start cloning. Ask the person what they actually want, in plain words:

| They say something like | Route | Why |
|---|---|---|
| "I just want to try it / use it on my phone" | **Route A — CodeFlying** | No toolchain, no keys to wire up, no Android knowledge |
| "I want to change the code / fix a bug / look at it" | **Route B — self-host** | You need the source, and you need a debug loop |
| "I don't know" | **Route A** | Cheapest way to find out whether they care before spending an afternoon on a toolchain |

Then follow the matching file. **Every step in those files has a "you should see" line — do not
advance past a step that did not produce it.** Half of the support load on this project is people
who skipped a step and reported the next one as broken.

---

## Route A — the no-build route (CodeFlying)

**Read `references/codeflying-route.md`.**

One-paragraph version: [codeflying.app](https://www.codeflying.app) (English) /
[codeflying.net](https://www.codeflying.net) (Chinese) is a general platform where you **describe the app
you want and it develops and publishes it**. Ask it for Andee and it hands back an installable package
with the keys already configured. There is a one-click page for Andee at
**https://www.codeflying.app/andee**.

**Three things you must tell the user, every time, without being asked:**

1. It is **a separate service with no direct relationship to this project** — not Andee's build
   channel, and not covered by anything in this repository. Its own terms, pricing and data
   handling apply.
2. What it saves is **(a) building and packaging it yourself, and (b) configuring the API keys**.
   It is **not** "nothing to install" — the output is still an APK that has to be put on the device.
3. The free token allowance is **finite**. It covers getting started; once it runs out, tokens are
   purchased. Never present this as a free service.

---

## Route B — self-host (clone → build → install → debug)

Follow these three files in order. Do not skip to the debug loop to "save time"; the debug loop
depends on the provisioning order in file 2.

1. **`references/get-the-code.md`** — check prerequisites, clone, and know what you just downloaded.
2. **`references/build-and-install.md`** — the JDK 17–20 trap, the Android SDK, the build, and the
   on-device order that makes the ball appear.
3. **`references/debug-loop.md`** — adb, logcat, the device's own WebSocket tool port, and the
   traps that look like broken hardware but are not.

---

## Facts you must not get wrong

These are the ones people get wrong most often, and each one costs an hour if you get it backwards:

- **The build JDK must be 17–20.** AGP 8.3.1 needs 17+, and **the Gradle 8.4 wrapper cannot run on
  21 or newer** — Android Studio's bundled JBR 25 fails with
  `Unsupported class file major version 69`. If a build fails and the error mentions a class file
  version, it is the JDK, not the code.
- **APKs are per-ABI.** `splits` is on, `universalApk false`. The file is
  `app/build/outputs/apk/<abi>/…` — pick **`arm64-v8a`** for anything bought in the last several
  years. A debug APK installs as-is; a release APK is **unsigned** and will not install until you
  sign it.
- **`local.properties` is not in the repository** (it is gitignored). A fresh clone has no
  `sdk.dir`, so the first build fails until it is written. Also: whatever is in *your*
  `local.properties` is baked into *your* build — do not ship that file, and do not paste its
  contents into anything public.
- **The keys live on the device, not in the repository.** No credentials ship with the source. With
  the default `brain = local`, **an empty `llm_api_key` means the local brain does not run at all** —
  nothing silently falls back. The Volcengine key is optional and its absence looks like a network
  timeout, not a missing field.
- **The debug WebSocket server binds `0.0.0.0:9008` and does not authenticate clients.** That is a
  known limitation written down in `SECURITY.md`. Say so before telling anyone to run this on a
  network they do not control.
- **The skill is not the source of truth — the repo is.** Once the code is cloned, prefer the files
  in it: `README.md`, `docs/permissions.md`, `SECURITY.md`, `CLAUDE.md`, `CHANGELOG.md`. If this
  skill and the repo disagree, the repo wins, and you should fix this skill.

---

## How to behave while doing this

- **One step, then check.** Run the command, show the person the real output, name what should have
  appeared, and only then continue. Never batch five commands and hope.
- **Evidence over reassurance.** "The build passed" means you saw `BUILD SUCCESSFUL`, not that the
  command exited quietly.
- **Do not invent keys, serial numbers or device paths.** Ask, or read them off the machine.
- **Do not commit `local.properties`**, device serials, or anyone's real chat content. The README's
  showcase section says it plainly: this app reads the screen, so a screenshot is a picture of
  somebody's messages.
- **If you are on a machine where the workspace already contains a deeper, more specific Andee
  skill** (for device-level verification of this codebase in particular), prefer that one for deep
  device work and use this skill as the onboarding path.

---

## Where to send people next

| They want | Send them to |
|---|---|
| To talk about it / ask questions | The repository's Issues |
| To show something they built | Discussions → Show and tell |
| To report a vulnerability | `SECURITY.md` — privately, never a public issue |
| To use it without building it | [codeflying.app](https://www.codeflying.app) · [codeflying.net](https://www.codeflying.net) |
