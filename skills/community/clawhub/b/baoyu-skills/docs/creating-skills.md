# Creating New Skills

**REQUIRED READING**: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## Key Requirements

| Requirement | Details |
|-------------|---------|
| **Prefix** | All skills MUST use `baoyu-` prefix |
| **name field** | Max 64 chars, lowercase letters/numbers/hyphens only, no "anthropic"/"claude" |
| **description** | Max 1024 chars, third person, include what + when to use |
| **SKILL.md body** | Keep under 500 lines; use `references/` for additional content |
| **References** | One level deep from SKILL.md; avoid nested references |

## SKILL.md Frontmatter Template

```yaml
---
name: baoyu-<name>
description: <Third-person description. What it does + when to use it.>
version: <semver matching marketplace.json>
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-<name>
    requires:          # include only if skill has scripts
      anyBins:
        - bun
        - npx
---
```

## Steps

1. Create `skills/baoyu-<name>/SKILL.md` with YAML front matter
2. Add TypeScript in `skills/baoyu-<name>/scripts/` (if applicable)
3. Add prompt templates in `skills/baoyu-<name>/prompts/` if needed
4. Register in `marketplace.json` under appropriate category
5. Add Script Directory section to SKILL.md if skill has scripts
6. Add openclaw metadata to frontmatter

## Category Selection

| If your skill... | Use category |
|------------------|--------------|
| Generates visual content (images, slides, comics) | `content-skills` |
| Publishes to platforms (X, WeChat, Weibo) | `content-skills` |
| Provides AI generation backend | `ai-generation-skills` |
| Converts or processes content | `utility-skills` |

New category: add plugin object to `marketplace.json` with `name`, `description`, `skills[]`.

## Writing Descriptions

**MUST write in third person**:

```yaml
# Good
description: Generates Xiaohongshu infographic series from content. Use when user asks for "小红书图片", "XHS images".

# Bad
description: I can help you create Xiaohongshu images
```

## Script Directory Template

Every SKILL.md with scripts MUST include:

```markdown
## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `{baseDir}`
2. Script path = `{baseDir}/scripts/<script-name>.ts`
3. Resolve `${BUN_X}` runtime: if `bun` installed → `bun`; if `npx` available → `npx -y bun`; else suggest installing bun
4. Replace all `{baseDir}` and `${BUN_X}` in this document with actual values

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | Main entry point |
```

## Progressive Disclosure

For skills with extensive content:

```
skills/baoyu-example/
├── SKILL.md              # Main instructions (<500 lines)
├── references/
│   ├── styles.md         # Loaded as needed
│   └── examples.md       # Loaded as needed
└── scripts/
    └── main.ts
```

Link from SKILL.md (one level deep only):
```markdown
**Available styles**: See [references/styles.md](references/styles.md)
```

## Extension Support (EXTEND.md)

Every SKILL.md MUST include EXTEND.md loading. Add as Step 1.1 (workflow skills) or "Preferences" section (utility skills):

```markdown
**1.1 Load Preferences (EXTEND.md)**

Check EXTEND.md existence (priority order):

\`\`\`bash
test -f .baoyu-skills/<skill-name>/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/<skill-name>/EXTEND.md" && echo "xdg"
test -f "$HOME/.baoyu-skills/<skill-name>/EXTEND.md" && echo "user"
\`\`\`

| Path | Location |
|------|----------|
| `.baoyu-skills/<skill-name>/EXTEND.md` | Project directory |
| `$XDG_CONFIG_HOME/baoyu-skills/<skill-name>/EXTEND.md` | XDG config (~/.config) |
| `$HOME/.baoyu-skills/<skill-name>/EXTEND.md` | User home (legacy) |

| Result | Action |
|--------|--------|
| Found | Read, parse, display summary |
| Not found | Ask user with AskUserQuestion |
```

End of SKILL.md should include:
```markdown
## Extension Support
Custom configurations via EXTEND.md. See **Step 1.1** for paths and supported options.
```
