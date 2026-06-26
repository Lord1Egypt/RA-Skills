# Ghostclaw Troubleshooting Guide

If you encounter issues while installing, configuring, or running Ghostclaw, consult the common issues and resolutions below.

---

## 1. Installation & Import Errors

### `ModuleNotFoundError: No module named 'core.analyzer'`

**Symptom:** You try to run `ghostclaw` or a script and receive an error indicating `core` cannot be found.
**Cause:** This usually happens if you are running an outdated version of the codebase before the `src/ghostclaw/` restructuring, or if you haven't installed the package correctly.
**Solution:**

1. Ensure your repository is up to date.
2. If running from source, ensure you run `pip install -e .` from the repository root, OR use the wrapper scripts in `./scripts/` (e.g., `./scripts/ghostclaw.sh`).

### `ModuleNotFoundError: No module named 'ghostclaw'` (OpenClaw Skill Install)

**Symptom:** After manually installing Ghostclaw into `~/.openclaw/skills/ghostclaw/`, OpenClaw or Python cannot import `ghostclaw`.
**Cause:** The skill directory structure is incorrect. The Python package **must** be inside a top-level `ghostclaw/` directory (i.e., `~/.openclaw/skills/ghostclaw/ghostclaw/`). A common mistake is to copy only the contents of `src/ghostclaw/` directly, flattening the package.
**Solution:**

1. Verify your skill layout:

   ```text
   ~/.openclaw/skills/ghostclaw/
   ├── SKILL.md
   └── ghostclaw/          ← this package directory is required
       ├── __init__.py
       ├── cli/
       ├── core/
       ├── lib/
       ├── stacks/
       └── references/
   ```

2. If the `ghostclaw/` package is missing, reinstall using the `skills` branch:

   ```bash
   git clone https://github.com/Ev3lynx727/ghostclaw.git
   cd ghostclaw
   git checkout skills
   cp -r ghostclaw ~/.openclaw/skills/ghostclaw/ghostclaw
   cp SKILL.md ~/.openclaw/skills/ghostclaw/
   ```

3. Test the installation:

   ```bash
   python3 -c "import sys; sys.path.insert(0, str(Path.home() / '.openclaw/skills/ghostclaw')); from ghostclaw.core.analyzer import CodebaseAnalyzer; print('OK')"
   ```

For a complete walkthrough, see [docs/HOWTOUSE.md](./HOWTOUSE.md#5-manual-installation-as-an-openclaw-skill).

### `Command 'ghostclaw' not found`

**Symptom:** You installed Ghostclaw via pip, but the CLI command is unavailable.
**Cause:** Your Python generic binaries directory (`~/.local/bin`) is not in your system `$PATH`.
**Solution:**
Add the Python user bin directory to your shell profile (e.g., `~/.bashrc` or `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Or, as an alternative, run the module directly via python:

```bash
python3 -m ghostclaw.cli.ghostclaw
```

---

## 2. Ghost Adapter Integration Issues

Since v0.1.6, Ghostclaw uses a plugin-based adapter system.

### `ValueError: Plugin name already registered`

**Symptom:** Ghostclaw exits with an error about a duplicate plugin name.
**Cause:** This occurs if you try to register a plugin with a name that already exists (e.g., trying to add a second "pyscn" adapter).
**Solution:** Check your `.ghostclaw/plugins/` directory for duplicate implementations or ensure your custom adapter names are unique.

### External Adapter Failed to Load

**Symptom:** You added a custom adapter to `.ghostclaw/plugins/`, but it doesn't appear in `ghostclaw plugins list`.
**Cause:** The adapter might have syntax errors, or it doesn't correctly implement the `BaseAdapter` interface (Protocol).
**Solution:**

1. Check the console output for "Plugin Error" messages.
2. Ensure your adapter class has the required `analyze()` (for `MetricAdapter`) or `emit_event()` methods.
3. Run `ghostclaw plugins scaffold <name>` to compare your implementation with a valid template.

### Missing PySCN or AI-CodeIndex Insights

**Symptom:** You ran `ghostclaw analyze --pyscn` but see no clone/dead code data.
**Cause:** The corresponding adapter is registered, but the underlying CLI tool (`pyscn` or `ai-codeindex`) is not installed or not in your PATH.
**Solution:**

1. Run `pyscn --version` in your terminal to verify installation.
2. Check `ghostclaw plugins list` to ensure the adapter is "Active".

---

## 3. Automation and Webhook Issues

### PR Creation Fails / `HTTP 401 Unauthorized`

**Symptom:** The watcher script fails to open GitHub Pull Requests.
**Cause:** Missing or invalid GitHub API token.
**Solution:** Set the `GH_TOKEN` environment variable before running the script:

```bash
export GH_TOKEN="ghp_your_personal_access_token"
./scripts/watcher --repos-file repos.txt --create-pr
```

### No Data in Watcher Cache

**Symptom:** Running `./scripts/compare.sh` returns `Repositories: 0` or "No data."
**Cause:** The watcher script needs to successfully run on repositories *before* the compare script can detect historical data in the filesystem.
**Solution:** Ensure you've run `./scripts/watcher --repos-file repos.txt` successfully at least once. Data is cached at `~/.cache/ghostclaw/vibe_history.json`.
