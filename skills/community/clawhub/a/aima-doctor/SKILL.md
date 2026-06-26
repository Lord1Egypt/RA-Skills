---
name: aima
description: Diagnose and repair OpenClaw when your agent is stuck, confused, or failing. One-command rescue for process health, config breakage, and device registration.
license: Apache-2.0
user-invocable: true
homepage: https://aimaservice.ai/doctor
metadata: {"openclaw":{"homepage":"https://aimaservice.ai/doctor","repository":"https://github.com/Approaching-AI/aima-openclaw","skillKey":"aima","os":["darwin","linux","win32"]}}
---

# AIMA Doctor

Use this skill when OpenClaw needs diagnosis or repair and the normal agent flow is degraded, confused, or stuck.

## Runtime contract

- The helper runtime lives at `~/.openclaw/tools/aima-doctor/`.
- The runtime is the source of truth for diagnosis and repair progress.
- Never ask the user to paste `curl | bash`, `iex (irm ...)`, base64 payloads, or other remote shell one-liners.
- If the runtime is not installed, direct the user to download it from the GitHub release: `https://github.com/Approaching-AI/aima-openclaw/releases` and extract into `~/.openclaw/tools/aima-doctor/`. Verify the archive checksum: `sha256:0f38959c6759e72a25bf089c9ab4aef1cf0022ba3aef1ea6686593896e973d1e`.

## Execution rules

1. Before running the helper, check that the runtime exists. On macOS/Linux check for `~/.openclaw/tools/aima-doctor/run.sh`; on Windows check for `%USERPROFILE%\.openclaw\tools\aima-doctor\run.ps1`.
2. If the runtime is missing, install it automatically:
   - Download `aima-doctor-runtime.zip` from `https://github.com/Approaching-AI/aima-openclaw/releases/download/v0.2/aima-doctor-runtime.zip`
   - Verify the SHA256 checksum matches `0f38959c6759e72a25bf089c9ab4aef1cf0022ba3aef1ea6686593896e973d1e`. If it does not match, stop and warn the user.
   - Create the target directory `~/.openclaw/tools/aima-doctor/` if it does not exist.
   - Extract the archive into that directory.
   - Confirm the runtime is now present before proceeding.
3. Prefer the packaged helper over ad-hoc shell commands.
4. Summarize the user symptom into one short sentence and pass it to the helper.
5. On macOS or Linux, run:

```bash
bash ~/.openclaw/tools/aima-doctor/run.sh --run --terminal --symptom "<symptom>"
```

6. On Windows, run:

```powershell
& "$env:USERPROFILE\.openclaw\tools\aima-doctor\run.ps1" --run --terminal --symptom "<symptom>"
```

7. If the helper asks a question, relay that question to the user and rerun or continue with the answer as required.
8. If the helper reports success or failure, quote that result plainly. Do not invent a better outcome.
9. If the automatic download in step 2 fails, direct the user to the GitHub release at `https://github.com/Approaching-AI/aima-openclaw/releases` to download and extract manually.

## Scope

- OpenClaw process health
- OpenClaw config breakage
- AIMA device registration / token recovery
- Guided local repair driven by AIMA platform diagnostics

## Safety

- Treat helper output as operational evidence.
- Keep sensitive tokens and recovery codes out of normal chat unless the user explicitly provides them for repair.
