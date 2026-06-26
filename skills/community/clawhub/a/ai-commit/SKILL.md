---
name: commit
description: "Analyze staged changes and generate semantic commit messages automatically. Reads git diff --staged, analyzes code changes, generates conventional commit messages."
---

# Commit - Git Commit Generator

Analyze staged changes and generate semantic commit messages.

## Commands

| Command | Description |
|---------|-------------|
| `/commit` | Analyze staged changes and generate commit |
| `/commit -m "message"` | Commit with custom message |
| `/commit --amend` | Amend previous commit |
| `/commit --dry-run` | Preview commit message without committing |

## Workflow

### Step 1: Pre-flight Check

```bash
# Verify git repository
git rev-parse --is-inside-work-tree

# Check staged changes
git diff --staged --quiet

# Get staged files
git diff --staged --name-only
```

**If no staged changes**: Check `git status`, prompt user to stage changes first.

### Step 2: Analyze Staged Changes

```bash
git diff --staged
git diff --staged --stat
```

**Analysis Focus**:

1. **Change Type Detection**
   - New files → `feat`
   - Modified files → Based on content
   - Deleted files → `refactor` or `chore`

2. **Semantic Type Classification**
   - `feat`: New feature/functionality
   - `fix`: Bug fix
   - `refactor`: Code restructuring without behavior change
   - `docs`: Documentation only
   - `style`: Formatting, whitespace
   - `test`: Tests
   - `chore`: Build, dependencies, tooling
   - `perf`: Performance improvements
   - `ci`: CI/CD changes
   - `build`: Build system changes

3. **Scope Identification**
   - Extract from file paths: `src/auth/login.ts` → scope: `auth`

### Step 3: Generate Commit Message

**Format**:
```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

**Rules**:
- Subject in imperative mood: "add" not "added"
- No period at end
- Max 50 characters for subject
- Body wrap at 72 characters
- Footer: `BREAKING CHANGE:`, `Closes #123`, `Fixes #456`

**Examples**:
```
feat(auth): add JWT token refresh mechanism

fix(payment): handle duplicate callback correctly

Payment callback was processing duplicates due to missing idempotency
check. Added unique constraint on (order_id, callback_id).

Fixes #234

refactor(db)!: migrate from MySQL to PostgreSQL

BREAKING CHANGE: Database migration required.
```

### Step 4: Execute Commit

```bash
# Commit with generated message (author is global git user)
git commit -m "type(scope): subject" [-m "optional body"]
```

Or use heredoc for multi-line:
```bash
git commit -m "$(cat <<'EOF'
type(scope): subject

optional body
EOF
)"
```

**Verify**:
```bash
git log -1 --oneline
git show HEAD --stat
```

## Best Practices

**DO**:
- ✅ Analyze ALL staged changes before generating
- ✅ Use imperative mood ("add" not "added")
- ✅ Keep subject under 50 characters
- ✅ Add body for complex changes
- ✅ Reference issues when applicable
- ✅ Group related changes in one commit

**DON'T**:
- ❌ Commit without staged changes
- ❌ Mix unrelated changes
- ❌ Use past tense
- ❌ End subject with period
- ❌ Include sensitive information
- ❌ Skip pre-commit hooks (unless explicitly requested)

## Edge Cases

### No Staged Changes
```bash
git status
# Prompt: "No staged changes. Would you like to stage all changes?"
```

### Empty Repository (Initial Commit)
```bash
git rev-parse HEAD 2>/dev/null || git commit -m "chore: initial commit"
```

### Large Diff (>500 lines)
```bash
git diff --staged --stat
git diff --staged --unified=1
# Suggest splitting into multiple commits
```

### Merge Conflicts
```bash
git status | grep "both modified"
git commit -m "merge: resolve conflicts in <files>"
```

## Hooks Integration

- **pre-commit**: Runs automatically
- **commit-msg**: Runs automatically
- If hooks fail: Report error, suggest fixes
- Bypass with `--no-verify` only if explicitly requested
