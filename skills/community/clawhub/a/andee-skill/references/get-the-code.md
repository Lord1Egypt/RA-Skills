# Step 1 — get the code

## 1.1 Check what the machine already has

Run these and read the actual output. Do not assume.

```bash
git --version
java -version        # you want 17–20 for this build; see build-and-install.md
adb version          # comes with Android SDK Platform-Tools
```

| Missing | Fix |
|---|---|
| `git` | macOS: `xcode-select --install` · Debian/Ubuntu: `sudo apt install git` · Windows: install Git for Windows |
| a JDK 17–20 | macOS: `brew install --cask temurin@17` · Windows/Linux: [Adoptium Temurin 17](https://adoptium.net/) |
| `adb` | Comes with **Android SDK Platform-Tools** — install Android Studio, or use the command-line path in `build-and-install.md` §2.2 |

> A JDK newer than 20 is worse than useless here: the Gradle wrapper in this project is 8.4 and it
> **cannot run on 21+**. Getting `Unsupported class file major version 69` later means the trap in
> `build-and-install.md` §2.1, not a broken repository.

## 1.2 Clone

Default (works everywhere):

```bash
git clone https://github.com/kuafuai/andee.git
cd andee
```

If the clone is slow, in this order:

```bash
# 1. Shallow clone — history is ~80 commits, so this mostly skips nothing, but it helps on bad links
git clone --depth 1 https://github.com/kuafuai/andee.git

# 2. Or download the ZIP from the repository page (green "Code" button → Download ZIP) and unzip it
```

If your team gave you an **internal mirror** of the repository, use that URL instead — some setups
mirror it precisely because the public one is slow from where they are. Use whatever URL came with
your instructions; do not invent one.

Windows: run the same commands in Git Bash; `./gradlew` becomes `gradlew.bat`.

## 1.3 Confirm what you actually got

```bash
git log --oneline -1          # which commit are you on?
git describe --tags           # which release is nearest? (v0.2.0 is current as of writing)
ls                            # sanity: app/ docs/ gradle/ reports/ tools/ gradlew README.md
```

Then **read the repository's own README** before you build anything. This skill is the onboarding
path; the README is the manual, and it is the thing that stays correct when this skill drifts. The
sections worth five minutes:

- **Quick start** — the shortest honest path, including the two keys.
- **Provisioning** — the from-scratch setup, and a table of the errors you are likely to hit.
- **Permissions: why each one, and what happens if you refuse** — read this *before* you install,
  because the permission set this app asks for is the same set Android banking trojans are detected
  by, and the user deserves to hear that from you rather than discover it.
- **SECURITY.md** — known limitations, including one that matters on any network the person does not
  control: the debug WebSocket server binds `0.0.0.0:9008` and does not authenticate its clients.

## 1.4 Know the shape of what you downloaded

```
app/                  the Android app (pure Kotlin — no Compose, no DI framework, no coroutines)
  src/main/java/net/kuafuai/andee/
    ScreenBodyService.kt   the accessibility service — the entry point, read this first
    brain/                 the agent loop — LocalBrain, LocalPrompt (the character's rulebook),
                           NotificationTriage
    net/                   BodyWsServer / BodyWsClient / CommandDispatcher / ToolSchemas
                           ← CommandDispatcher.kt is the authoritative list of tool method names
    device/                screen control, permissions, vault, robot dog
    config/                VoiceConfig (settings), Notebook (memories, todos, scenes — encrypted)
    ui/                    the overlay: ball, subtitles, settings, self-check, scenes, pages
docs/                 architecture.svg, permissions.md, releases/
reports/              design labs and research notes — part of the repo, not scratch space
tools/                device-side helper scripts and the ball-face lab runners
CLAUDE.md             architecture notes written for AI coding assistants
```

Deliberately absent, and you should not add them: Jetpack Compose (it cannot live inside an
overlay), Hilt/Dagger (there is one service, so dependencies are constructor-injected by hand), and
coroutines (WS callbacks run on a `Handler` plus dedicated executors). Match the existing style.

## → Next

`build-and-install.md`. Do not jump to `debug-loop.md` — the debug loop assumes the provisioning order
in the next file has already been done.
