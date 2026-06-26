# Git Best Practices

## Commit Message Guidelines

### Structure
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies

### Rules
1. **Subject line**: 50 chars or less, imperative mood ("Add feature" not "Added feature")
2. **Body**: Wrap at 72 chars, explain what and why (not how)
3. **Atomic commits**: One logical change per commit
4. **Present tense**: "Fix bug" not "Fixed bug"

### Examples
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with Google and GitHub providers.
Users can now sign in using their existing accounts.

Closes #123
```

```
fix(api): handle null response in user endpoint

Previously crashed when user data was missing. Now returns 404 with
appropriate error message.
```

## Workflow Best Practices

### Before Committing
1. Review changes: `git diff`
2. Stage selectively: `git add -p` for partial staging
3. Check status: `git status`
4. Verify staged changes: `git diff --staged`

### Amending Commits
- Use `git commit --amend` when fixing the last commit
- Only amend commits that haven't been pushed
- Never amend public history

### Branch Management
- Keep branches focused and short-lived
- Use descriptive branch names: `feature/user-auth`, `fix/login-bug`
- Delete merged branches: `git branch -d branch-name`

### Pushing Changes
- Always push to current branch: `git push origin HEAD`
- Never force push to shared branches without team agreement
- Use `git push --force-with-lease` instead of `--force` when needed

### Dangerous Operations
These require extra caution and user confirmation:
- `git push --force` / `git push -f`
- `git reset --hard`
- `git clean -fd`
- `git rebase` on public branches
- `git branch -D` (force delete)
- Any operation that rewrites history

### Rebase vs Merge
- **Rebase**: Clean linear history, use for feature branches before merging
- **Merge**: Preserves history, use for integrating branches
- Never rebase public/shared branches

### Common Patterns
```bash
# Update feature branch with main
git checkout feature-branch
git fetch origin
git rebase origin/main

# Interactive rebase to clean up commits
git rebase -i HEAD~3

# Stash changes temporarily
git stash
git stash pop

# Cherry-pick specific commit
git cherry-pick <commit-hash>
```
