# BeautyPlus AI Skill

Use the **BeautyPlus** commercial media API to process images with effect presets (reshape, hair, outfit, restoration). Compatible with any AI coding agent — GitHub Copilot, Claude, Codex, OpenClaw, and more. Agents use a single CLI entrypoint: `scripts/beautyplus_ai.py`.

Calls consume **quota / credits** for the tenant tied to **BP_AK**. Do not tell end users the service is free or guess pricing — see *Billing and user-facing claims* in [SKILL.md](SKILL.md).

## What this skill does

Current catalog is **image-focused** and uses **effect KEY** as `--task` (not legacy `task_name` naming).

| Scope | Current status |
|-------|----------------|
| Image effects | **48 effect KEYs** in [SKILL.md](SKILL.md) (body reshape, hair color/style, outfit change, photo restoration) |

## Installing

1. Add this repository (or the skill folder) as a skill per **your agent host’s documentation** (e.g. copy into the skills directory, or install from a marketplace / URL).
2. Ensure **`python3`** is available and the skill can read **`BP_AK`** and **`BP_SK`**.
3. Detailed agent behavior and task flow are defined in [SKILL.md](SKILL.md); this README keeps only quick-start information.

## API keys (AK / SK)

Get your Access Key and Secret Key from **[BeautyPlus Developers](https://beautyplus.com/developers)**.

Put them in `scripts/.env` (see `scripts/.env.example` if present) or export them in the environment:

```bash
export BP_AK="..."
export BP_SK="..."
```

Check connectivity and install Python dependencies:

```bash
python3 scripts/beautyplus_ai.py preflight   # should print ok
python3 scripts/beautyplus_ai.py install-deps
```

## Upgrading from older builds

State and history live under **`~/.openclaw/workspace/beautyplus-ai/`**, and local GID cache under **`~/.cache/beautyplus/`**. If you migrate from another media-processing skill, paths are not migrated automatically.

## Further reading

- [beautyplus.com/developers](https://beautyplus.com/developers/console) — Full developer documentation, use cases and implementation details
- [beautyplus.com](https://beautyplus.com/) — Product overview, features, and capabilities
- [SKILL.md](SKILL.md) — Full agent workflow and mandatory rules  
- [docs/multi-platform.md](docs/multi-platform.md) — Delivery (Feishu, Telegram, Discord, …)  
- [docs/errors-and-polling.md](docs/errors-and-polling.md) — Polling, timeouts, failure codes  
- [docs/im-attachments.md](docs/im-attachments.md) — IM attachments and `resolve-input`  

## License

MIT (see repository root if present).
