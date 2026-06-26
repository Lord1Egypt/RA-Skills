# Troubleshooting Guide — Claude Code Memory Kit

## Common Issues & Solutions

### Issue: "Claude doesn't read my CLAUDE.md"
**Symptoms:** You create CLAUDE.md but Claude Code ignores it.
**Causes:**
- File in wrong location (must be in project root)
- Syntax errors in YAML frontmatter
- File named incorrectly (not exactly `CLAUDE.md`)

**Solutions:**
1. Verify location: must be `/CLAUDE.md` at project root
2. Check for syntax errors — validate YAML
3. Ensure filename is exactly `CLAUDE.md` (case-sensitive)
4. Add to settings.json: `{"permissions": {"allow": ["Read"]}}`

---

### Issue: "Memory doesn't persist between sessions"
**Symptoms:** Each new session feels like starting fresh.
**Causes:**
- No bootstrap.md in project
- Context too long (truncated by API)
- Project not configured for memory persistence

**Solutions:**
1. Create `bootstrap.md` with session context summary
2. Keep bootstrap under 2000 characters
3. Use `/remember` command to flag important info
4. Set up `memory.md` for cross-session patterns

---

### Issue: "Mistakes still repeat"
**Symptoms:** You corrected something, but Claude does it again.
**Causes:**
- Corrections not in mistakes.md
- Rule too vague (not specific enough)
- No enforcement mechanism

**Solutions:**
1. Add specific mistake patterns to `mistakes.md`
2. Use exact code patterns: "Don't use `force push` on branch main"
3. Set up pre-tool confirmations for risky commands
4. 3+ corrections → auto-promote to hard rule

---

### Issue: "Context gets lost with long projects"
**Symptoms:** Claude forgets important context in large codebases.
**Causes:**
- No structured memory system
- Too much info in one file
- Missing bootstrap context

**Solutions:**
1. Split memory into: CLAUDE.md (rules), memory.md (patterns), mistakes.md (anti-patterns)
2. Keep each file under 3000 characters
3. Use bootstrap.md to inject key context at session start
4. Consider project-specific subdirectories for memory

---

### Issue: "Team members override each other's rules"
**Symptoms:** Different team members get different behaviors from Claude.
**Causes:**
- No shared CLAUDE.md
- Personal preferences in project root
- Inconsistent onboarding

**Solutions:**
1. Commit CLAUDE.md to shared repo
2. Use team-specific profile in `.claude/`
3. Document team conventions in CLAUDE.md
4. Add onboarding section for new developers

---

### Issue: "Pre-tool gates don't trigger"
**Symptoms:** You want confirmation before destructive commands but nothing happens.
**Causes:**
- Gates not configured in settings.json
- Wrong permission scope
- Not using correct tool names

**Solutions:**
1. Add to settings.json:
```json
{
  "preToolGates": {
    "Bash(git push --force)": "confirm",
    "Bash(rm -rf)": "confirm",
    "Edit": "warn"
  }
}
```
2. Use exact tool names from Claude Code logs
3. Test with non-destructive commands first

---

### Issue: "Memory files get too large"
**Symptoms:** Memory.md grows infinitely and becomes unusable.
**Causes:**
- No pruning strategy
- Everything saved, nothing deleted
- No prioritization

**Solutions:**
1. Weekly review: move resolved items to archive
2. Keep only current patterns in memory.md
3. Use date stamps for time-sensitive info
4. Delete entries older than 30 days if resolved

---

## Installation Issues

### "npm install fails"
```bash
# Use npx instead for one-off tools
npx @somepackage/command

# Or install globally with correct permissions
npm install -g @somepackage --unsafe-perm=true
```

### "Settings not loading"
- Check JSON syntax (no trailing commas)
- Verify file path: `~/.claude/settings.json`
- Restart Claude Code after changes

---

## Performance Tips

1. **Keep files small** — Under 3000 chars each
2. **Use headers** — Quick scanning for Claude
3. **Be specific** — "Never do X in file Y" vs "be careful"
4. **Test incrementally** — Add one rule, test, then add more

---

## Need More Help?

- Check GitHub issues for Claude Code
- Review Anthropic documentation
- Join Discord community for troubleshooting