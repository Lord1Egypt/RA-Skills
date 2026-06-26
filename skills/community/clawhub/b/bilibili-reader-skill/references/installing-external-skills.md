# Installing External GitHub Repos as Hermes Skills

Generalized procedure for cloning a GitHub repo and installing it as a Hermes skill.

## Steps

1. **Clone repo to /tmp**
   ```bash
   git clone https://github.com/<owner>/<repo>.git /tmp/<repo>
   ```

2. **Read SKILL.md** — validate frontmatter (name, description, prerequisites).

3. **Create skill via skill_manage**
   ```python
   skill_manage(action='create', name='<skill-name>', category='<category>', content=<SKILL.md>)
   ```

4. **Create subdirectories first** — source repos often have `src/`, `templates/`, `data/` etc.
   ```bash
   mkdir -p <skill_dir>/src <skill_dir>/templates <skill_dir>/data
   ```

5. **Copy non-dotfile files** — `cp` works for regular files but **dotfiles (.env.example, .gitignore) are blocked** by the sandbox.
   - Regular files: `cp /tmp/<repo>/<file> <skill_dir>/<file>`
   - Dotfiles: use `skill_manage(action='write_file', file_path='scripts/<dotfile>')` instead

6. **Set up Python environment** — sandbox has no pip in system Python.
   ```bash
   uv venv <skill_dir>/.venv
   uv pip install --python <skill_dir>/.venv/bin/python <packages>
   ```

7. **Verify** — test imports, env vars, and API connectivity.

## Pitfalls

- **Dotfiles blocked**: `.env.example`, `.gitignore` etc. can't be copied via `cp`. Use `skill_manage write_file` with `scripts/` prefix.
- **Subdir missing**: `cp` to non-existent dir fails silently or with error. Always `mkdir -p` first.
- **protobuf import**: pip package `protobuf` imports as `from google.protobuf import ...`
- **Sandbox pip**: System Python has no pip. Use `uv venv` + `uv pip install --python <venv>/bin/python`.
