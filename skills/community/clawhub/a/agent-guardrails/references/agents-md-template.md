# AGENTS.md — Template with Mechanical Enforcement

Copy and adapt this template for your project's AGENTS.md file.

---

# AGENTS.md — [Project Name]

## 🚨 Iron Laws

### 1. Never Hardcode Secrets
- All secrets from environment variables — no exceptions
- No fallback values in `os.getenv()` — fail loudly
- Pre-commit scan: `bash scripts/check-secrets.sh`

### 2. Never Bypass Established Standards
- Existing validation logic → **import it, don't rewrite**
- "Too slow" → **optimize it, don't bypass it**
- Before new code → check if project already has it
- User-facing output → must go through project's validation pipeline

### 3. Verify Before Acting
- Modify config → backup first, verify after
- Write code → research first, test after
- Uncertain → look it up, don't guess

## 🔧 Mechanical Enforcement

**Rules in markdown are suggestions. Code hooks are laws.**

### Before creating any new .py file:
```bash
bash scripts/pre-create-check.sh .
```

### After creating/editing any .py file:
```bash
bash scripts/post-create-validate.sh <file_path>
```

### Git pre-commit hook (automatic):
- Blocks bypass patterns ("simplified version", "quick version", "temporary")
- Blocks hardcoded secrets
- Override with `--no-verify` (explain why)

### Project registry:
- `__init__.py` lists official validated functions
- New scripts MUST import from registry, not reimplement

### Self-check before writing code:
- [ ] Does existing code already do what I need?
- [ ] Am I "simplifying" away important validation?
- [ ] Does output go through the validated pipeline?
- [ ] Am I importing from the registry?
