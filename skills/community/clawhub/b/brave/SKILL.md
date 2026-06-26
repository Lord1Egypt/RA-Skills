---
name: Brave Browser
slug: brave
version: 1.0.0
homepage: https://clawic.com/skills/brave
description: Operate, automate, and troubleshoot Brave Browser with profiles, Shields, extensions, and Chromium debugging workflows.
changelog: Initial release with profile workflows, site-compatibility diagnostics, extension handling, and browser recovery playbooks.
metadata: {"clawdbot":{"emoji":"🦁","requires":{"bins":[],"config":["~/brave/"]},"os":["linux","darwin","win32"],"configPaths":["~/brave/"]}}
---

## When to Use

User needs help with Brave Browser itself, not generic browsing advice. Use this when the task depends on Brave-specific behavior such as Shields, profile isolation, private windows, extension compatibility, Chromium debugging, or a website that behaves differently in Brave than in Chrome.

Choose this skill when the blocker is operational: install path, launch flags, profile selection, site breakage, extension conflicts, remote debugging, or a repeatable browser workflow that must stay inside Brave.

## Architecture

Memory lives in `~/brave/`. If `~/brave/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/brave/
|-- memory.md          # Durable activation rules, OS facts, and safety boundaries
|-- profiles.md        # Known profiles, purpose, and launch notes
|-- sites.md           # Site-specific Shields overrides and known-good fixes
|-- automation.md      # Remote-debugging ports, test flows, and tool preferences
`-- incidents.md       # Startup failures, extension conflicts, and recovery notes
```

## Quick Reference

Load only the smallest file needed for the current blocker.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Launch commands and profile strategy | `launch-and-profiles.md` |
| Shields and site-breakage recovery | `shields-and-compatibility.md` |
| Brave automation and DevTools workflows | `automation-and-debugging.md` |
| Extensions, sync, wallet, and private windows | `extensions-and-wallet.md` |
| Failure recovery and cleanup order | `troubleshooting.md` |

## Requirements

- Brave Browser should already be installed, or there must be permission to guide installation.
- Verify the operating system, install path, and target profile before changing anything.
- Ask for explicit approval before enabling remote debugging, clearing profile data, importing wallet or sync state, changing global Shields defaults, or opening multiple sensitive sites.
- Treat login sessions, cookies, private windows, sync, and wallet data as user-sensitive state.

## Operating Coverage

This skill is for operating Brave as a browser platform, not for generic web search or Brave Search API setup. It covers:
- app launch and path detection across macOS, Windows, and Linux
- normal profiles, disposable profiles, and private-window workflows
- site failures caused by Shields, aggressive blocking, or extension conflicts
- Chromium-compatible automation using Brave with Playwright, Puppeteer, or remote debugging
- extension compatibility, sync boundaries, and wallet-adjacent caution
- browser recovery when startup, updates, or profile state go wrong

## Data Storage

Keep only durable Brave operating context in `~/brave/`:
- approved profiles and what each one is for
- known site fixes and whether they are per-site or global
- allowed automation posture, remote-debugging defaults, and no-go actions
- repeated incidents such as crash-on-launch, bad flags, corrupted profile state, or extension collisions

## Core Rules

### 1. Identify the Exact Brave Surface Before Acting
- Lock four facts first: OS, install path, target profile, and whether the issue is launch, browsing, extension, or automation related.
- Brave problems often look like "the browser is broken" when the real cause is the wrong profile or a stale flag.
- Do not change settings until the target surface is explicit.

### 2. Treat Shields as the First Compatibility Check
- When a site loops on login, breaks scripts, hides media, or blocks checkout, inspect Brave Shields before assuming the site itself is bad.
- Prefer per-site fixes before global relaxations so privacy defaults stay intact elsewhere.
- Use `shields-and-compatibility.md` to move from symptom to the smallest reversible change.

### 3. Keep Profiles Separate by Risk and Purpose
- Use one stable daily profile and separate profiles for testing, automation, or risky extensions.
- Do not debug a broken production login inside the same profile used for experiments.
- If a fresh profile fixes the issue, record that before touching the main profile.

### 4. Reuse Chromium Tooling, But Verify Brave-Specific Behavior
- Brave supports Chromium-style automation, but Shields, built-in blockers, and profile choices can change outcomes.
- Use `automation-and-debugging.md` when attaching Playwright, Puppeteer, or a DevTools client.
- A workflow that passes in Chrome is not proof that it will pass in Brave without adjustment.

### 5. Treat Extensions, Sync, Wallet, and Private Windows as Trust Boundaries
- Extension installs, sync enablement, wallet access, and private-window workflows affect sensitive user state.
- Ask before changing permissions, importing state, or enabling anything that broadens data exposure.
- Never present private windows or Tor-based browsing as a way to bypass site restrictions or anti-fraud controls.

### 6. Change One Variable at a Time
- When diagnosing, isolate profile, Shields, extension set, launch flag, or remote-debugging state instead of changing several together.
- One controlled change plus one verification step beats "try everything" browser debugging.
- Record the exact change that fixed the issue so the user does not repeat the incident.

### 7. Verify in the Browser, Not Only in the Command Output
- A launch command succeeding does not prove the right window, profile, or site state is live.
- Confirm the actual browser state: expected profile opened, extension loaded, site behavior changed, or DevTools endpoint became reachable.
- If the expected state is not visible, stop and switch to a safer fallback.

## Brave Traps

- Treating Brave as "just Chrome with a different icon" -> Shields and privacy defaults keep surprising the workflow.
- Disabling blockers globally for one broken site -> privacy posture degrades everywhere.
- Testing automation in the user's daily profile -> cookies, extensions, and session state skew the result.
- Clearing profile data too early -> the hardest-to-recover state gets destroyed first.
- Mixing sync, wallet, and private-window issues in one troubleshooting pass -> the blast radius becomes unclear.
- Assuming a site failure is anti-bot hostility -> many breaks are local compatibility problems and can be fixed reversibly.

## Security & Privacy

Data that may leave your machine:
- normal website traffic to the domains the user opens in Brave
- optional sync, extension-store, or wallet-related traffic only if the user already uses those Brave features
- optional automation traffic to a local DevTools endpoint when the user enables remote debugging

Data that stays local:
- browser state already stored by Brave in its own profile directories
- durable operating notes under `~/brave/` if the user approves persistence

This skill does NOT:
- use undeclared remote APIs by default
- recommend bypassing bot checks, paywalls, or fraud controls
- assume remote debugging is safe to leave on permanently
- clear profiles or security-sensitive browser state without explicit approval

## Scope

This skill ONLY:
- helps operate Brave Browser safely and predictably
- structures profile, Shields, extension, and automation work into reversible steps
- keeps durable notes for approved profiles, site fixes, and recurring incidents

This skill NEVER:
- act as a generic search-engine skill
- require the user to adopt sync, wallet, or private-window workflows they did not ask for
- store secrets, passwords, or full browsing history in its own memory files
- modify its own skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `chrome` - Reuse Chromium debugging patterns when the issue is not Brave-specific.
- `playwright` - Automate and verify web flows after the Brave launch surface is stable.
- `puppeteer` - Drive DevTools and Chromium automation with lower-level script control.
- `macos` - Handle macOS app paths, permissions, and automation details around Brave on Apple systems.
- `web` - Fetch or inspect web content after the browser environment is behaving correctly.

## Feedback

- If useful: `clawhub star brave`
- Stay updated: `clawhub sync`
