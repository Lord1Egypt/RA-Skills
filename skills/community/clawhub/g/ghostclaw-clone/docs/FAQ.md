# Ghostclaw FAQ

Frequently Asked Questions and common troubleshooting tips for Ghostclaw.

## Installation & Setup

### 1. I get `ModuleNotFoundError: No module named 'ghostclaw.cli'` when running the command

This usually happens if the package structure wasn't recognized correctly during installation or if new subpackages were added.  
**Solution:** Reinstall the package in editable mode:

```bash
pip install -e .
```

### 2. Should I use a virtual environment?

Yes, it is highly recommended to use a virtual environment (`.venv`) to prevent dependency conflicts. However, if you've already installed it globally/locally (e.g., in `~/.local/bin`), you can continue using that environment.

### 3. Where should I put my `.env` file?

Place your `.env` file in the **root directory** of the project you are analyzing. Ghostclaw looks for it in the current working directory.  
You can also use:

- `~/.ghostclaw/ghostclaw.json` for global configuration.
- System environment variables (e.g., `export GHOSTCLAW_API_KEY=...`).

---

## Configuration

### 1. How do I configure my AI provider?

You can set this in your `.env` file:

```env
GHOSTCLAW_AI_PROVIDER=openai
GHOSTCLAW_AI_MODEL=gpt-4
GHOSTCLAW_API_KEY=your_key_here
```

Or in `~/.ghostclaw/ghostclaw.json`:

```json
{
  "ai_provider": "openai",
  "ai_model": "gpt-4"
}
```

### 2. How can I see more details about what Ghostclaw is doing?

Use the `--verbose` flag:

```bash
ghostclaw analyze . --verbose
```

This will save raw logs to `ghostclaw.log`.

---

## Commands

### 1. What does `ghostclaw doctor` do?

The `doctor` command runs diagnostic checks on your environment, directory structure, and AI provider connectivity. Use it if you suspect something is misconfigured.

### 2. How do I clear the analysis cache?

Ghostclaw stores cache in `.ghostclaw/cache`. You can manually delete this directory to force a fresh analysis.
