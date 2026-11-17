---
name: cli-butler
description: Manage local CLI tools through any agent — inventory every installed CLI across package managers (brew, npm, pipx, uv, cargo, gem, apt), install/upgrade/uninstall with provenance routing, trace a CLI's full reference chain (symlinks, PATH lines, launchd, config files, last-used), and enumerate what a CLI can do. Use when the user asks to install, uninstall, upgrade or list CLI tools, asks "what CLI tools are installed", wants to know where a CLI comes from or what references it, or wants to know a command's capabilities. Zero third-party dependencies, macOS/Linux.
---

# cli-butler

Agent skill for managing local CLI tools. Status: **v0.1.1 stable** (see `docs/REQUIREMENTS.md`).

## Capabilities

| Command | What it does |
|---------|--------------|
| `bin/list.sh` | Inventory every CLI grouped by channel, each with a one-line description; system-bundled CLIs get their own group marked non-uninstallable. `--by-function` re-groups by purpose (AI agents, mobile dev, containers, runtimes, web, media, VCS, libraries, system) with channel as a per-row attribute |
| `bin/manage.sh` | `info <cli>` / `outdated` / `upgrade <cli>` |
| `bin/install.sh` | Install via the right channel, record provenance |
| `bin/uninstall.sh` | Channel-routed uninstall; manual items go through refchain + dry-run + confirm |
| `bin/refchain.sh` | Five-layer reference chain: symlink → channel → PATH lines → launchd → configs; last-used |
| `bin/cap.sh` | Enumerate a CLI's subcommands from its help output |

## Presenting results to humans

Raw output is grouped by **channel** (that is the management view — it decides
upgrade/uninstall routing and safety). When answering a user's "what do I have"
question, re-present grouped by **function/purpose** (AI agents, containers,
mobile dev, languages, web/network, media, version control, self-written
scripts, library dependencies, system-bundled), with the channel shown as a
per-item attribute — e.g. `docker (brew)`. Users think in purposes, not in
package managers.

## Safety rules (non-negotiable)

1. **Never `rm` a binary owned by a package manager.** Always route through the owning channel (`brew uninstall`, `npm uninstall -g`, …). Direct deletion corrupts the channel's database.
2. **Uninstall is dry-run first.** Show planned actions, require explicit confirmation (`--yes` or interactive).
3. **launchd services are disabled by moving the plist away** (e.g. to `.plist.off`), never by `launchctl bootout` alone — bootout only unregisters the current session; the service returns on next login.
4. **App-embedded symlinks** (e.g. `/usr/local/bin/docker` → inside an .app): move the symlink aside (`.bak`), never delete the app's internals.
5. Single channel probe failures never block the whole inventory; report them, don't guess.
6. **System-bundled CLIs are never uninstalled.** Anything under macOS SIP-protected prefixes (`/usr/bin`, `/bin`, `/sbin`, `/usr/sbin`) is listed but refused on uninstall, with the reason stated.

## Design docs

- `docs/REQUIREMENTS.md` — requirements (source of truth)
- `docs/provenance.md` — channel model, ownership resolution, journal format
- `docs/design.md` — architecture and conventions
