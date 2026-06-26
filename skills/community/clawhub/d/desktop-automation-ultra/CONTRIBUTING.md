# Contributing to Desktop Automation Skill

Thank you for your interest! This skill is open-source under the MIT license. All contributions are welcome — bug reports, features, documentation, tests.

---

## 🛠️ Development Environment

### Prerequisites
- Python 3.10+
- Git
- Pip + virtualenv (recommended)

### Setup
```bash
git clone https://github.com/JordaneParis/desktop-automation-ultra-local.git
cd desktop-automation-ultra-local
python -m venv venv
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Test
```bash
# Check module imports
python -c "import pyautogui, pygetwindow, PIL; print('OK')"

# Dry-run a macro (if test file exists)
python scripts/play_macro.py recorded_macro/example.json --dry-run
```

---

## 📝 Code Style

- **PEP 8** — follow Python conventions (4 spaces, camelCase for functions)
- **Type hints** — add for new functions (not required for minor changes)
- **Docstrings** — every function/class must have a docstring in English
- **Logging** — use `logging` instead of `print`. Levels:
  - `DEBUG`: technical details
  - `INFO`: important user actions
  - `WARNING`: recoverable problems
  - `ERROR`: blocking errors
- **Exceptions** — raise clear exceptions with informative messages
- **JSON** — always `ensure_ascii=False`, `indent=2` for readability

---

## 🔄 Contribution Workflow

1. **Fork** the repository
2. **Create a branch**:
   ```bash
   git checkout -b feature/my-new-feature
   ```
   or
   ```bash
   git checkout -b fix/bug-fix
   ```
3. **Develop** with clear commits:
   ```bash
   git commit -am "Add resize_window action"
   ```
4. **Test** locally (if applicable)
5. **Push** to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```
6. **Open a Pull Request**:
   - Clear title (e.g., "Add drag-and-drop action", "Fix window monitor race condition")
   - Full description: what, why, how
   - Link related issues
   - Attach screenshots/outputs if relevant

---

## 📋 PR Checklist

- [ ] Code conforms to style (PEP 8 + rules above)
- [ ] Docstrings added/updated
- [ ] README.md updated if needed (new action, parameter)
- [ ] SKILL.md updated (action list)
- [ ] Tests performed (manual or automated)
- [ ] No stray `print()` statements (use `logging`)
- [ ] UTF-8 everywhere (accents preserved)
- [ ] JSON files well-formed
- [ ] No external dependencies added without discussion (prefer optional)

---

## 🧪 Testing

Currently the skill has no automated tests. If you add them:
- Place tests in `tests/`
- Use `pytest` if possible
- Test pure functions (e.g., timestamp parsing, JSON validation)
- For GUI actions: document manual tests in the PR

---

## 📚 Documentation

- **SKILL.md** — short description, action list, usage example. Update for every new action.
- **README.md** — complete user guide (install, troubleshooting, examples). Update for major changes.
- **Docstrings** — serve as developer reference.

---

## 🔐 Security

- **No network access** — the skill must remain local only
- **No external code execution** (no `eval`, `exec`, `os.system` without sandbox)
- **No credentials** — never request or store passwords
- **Respect permissions** — warn if admin rights are needed

---

## ❓ Questions

- Open an *Issue* to discuss before large modifications
- For bugs: provide steps to reproduce, OS, Python/package versions
- For features: explain the use case

---

## 📄 License

All contributions are under the MIT license (see `LICENSE`). By submitting a PR, you agree that your changes will be distributed under this license.

---

**Thanks for making this skill better!** 🚀
