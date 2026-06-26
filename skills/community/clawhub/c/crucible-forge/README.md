# Forge — AI Workspace Architect

**Systematic workspace reorganization for AI agent users.**

Forge scans your AI agent's workspace, builds a safety-first reorganization plan, executes it with zero data loss, and verifies everything works afterward. Built from a battle-tested methodology used on production AI workspaces.

---

## The Problem

AI agent workspaces accumulate chaos fast. Files pile up at root. Memory files reference moved documents. Cron jobs point to old paths. Config files drift. One bad reorganization can brick your agent's memory, break running processes, or corrupt critical state files.

Manual cleanup is dangerous. Automated cleanup without safeguards is worse.

## What Forge Does

### 1. **Scan** (`forge_scan.py`)
- Maps your entire workspace: files, directories, sizes, types
- Discovers all cross-references (file A mentions file B)
- Finds broken references (file A mentions file B, but B doesn't exist)
- Identifies running processes and their file dependencies
- Detects hardcoded paths in scripts and configs
- Catalogs cron jobs, scheduled tasks, and their path dependencies
- Outputs a complete workspace report

### 2. **Plan** (`forge_plan.py`)
- Generates a reorganization plan based on your configured directory template
- Creates hardline safety rules before touching anything
- Produces an ordered execution sequence with dependency tracking
- Identifies protected files that must never be modified
- Plans reference patches (what needs updating after moves)
- Generates rollback procedures for every step
- Outputs a human-reviewable plan — nothing executes automatically

### 3. **Audit** (`forge_audit.py`)
- **Pre-move audit:** Verifies backup exists, creates file manifest, checks all protected files
- **Post-move audit:** Compares file counts, verifies no files lost, checks all references resolve, validates protected files unchanged
- **Content audit:** Scans for misplaced content, secrets in wrong locations, orphaned files
- **Reference audit:** Verifies every cross-reference in every file still resolves

---

## Quick Start

```bash
# 1. Configure your workspace
cp config_example.py forge_config.py
# Edit forge_config.py with your workspace path, protected files, directory template

# 2. Scan your workspace
python3 forge_scan.py --config forge_config.py

# 3. Generate a reorganization plan
python3 forge_plan.py --config forge_config.py --scan-report scan_report.json

# 4. Review the plan (ALWAYS review before executing)
cat reorg_plan.json

# 5. Run pre-move audit
python3 forge_audit.py --config forge_config.py --phase pre

# 6. Execute the plan (you do this manually or with your own script)
# Forge generates the plan. YOU execute it. This is deliberate.

# 7. Run post-move audit
python3 forge_audit.py --config forge_config.py --phase post --manifest pre_manifest.txt
```

## Design Philosophy

### Safety First, Always
- **Never deletes files.** Moves only. If something looks like garbage, it goes to archive.
- **Never modifies protected files.** You define what's protected; Forge won't touch them.
- **Backup before changes.** Forge refuses to generate a plan without a verified backup.
- **Human reviews the plan.** Forge doesn't auto-execute. You read the plan, you decide.
- **Rollback for every step.** Every move in the plan includes how to undo it.

### Zero-Deletion Policy
No file is ever deleted during reorganization. Files are moved, never removed. Even files that appear to be duplicates are preserved until you explicitly confirm deletion.

### Atomic Reference Updates
When a file moves, every reference to that file must update in the same logical step. Forge tracks these as paired operations: move file + update references = one unit. If the reference update fails, the move should be rolled back.

### Framework, Not Opinions
Forge doesn't dictate your directory structure. You configure the template. Forge handles the mechanics of getting there safely.

---

## Use Cases

- **New AI agent setup:** Start with a clean, structured workspace from day one
- **Workspace recovery:** Untangle months of accumulated file chaos
- **Platform migration:** Moving from one AI agent platform to another
- **Team onboarding:** Standardize workspace structure across multiple agents
- **Pre-deployment cleanup:** Verify workspace integrity before going live
- **Post-incident audit:** Check what broke and what's still intact after a failure

## What's Included

| File | Purpose |
|------|---------|
| `forge_scan.py` | Workspace scanner and reference mapper |
| `forge_plan.py` | Reorganization planner with safety rules |
| `forge_audit.py` | Pre/post audit verification |
| `config_example.py` | Configuration template |
| `LIMITATIONS.md` | What Forge doesn't do |
| `LICENSE` | MIT License |

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- Works on any OS (Linux, macOS, Windows)
- Platform-agnostic (OpenClaw, AutoGPT, CrewAI, or any file-based workspace)

## Configuration

See `config_example.py` for the full configuration reference. Key settings:

- **`WORKSPACE_ROOT`** — Path to your workspace
- **`PROTECTED_FILES`** — Files that must never be modified or moved
- **`PROTECTED_DIRS`** — Directories that must never be touched
- **`DIRECTORY_TEMPLATE`** — Your desired directory structure
- **`BACKUP_DIR`** — Where backups are stored
- **`ARCHIVE_DIR`** — Where "deleted" files actually go
- **`README_TEMPLATE`** — Content template for per-directory `_README.md` files

---

## quality-verified


## License

MIT — See `LICENSE` file.


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
