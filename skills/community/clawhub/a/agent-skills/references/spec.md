# Agent Skills Specification Reference

> SKILL.md format specification, integration flow, and runtime behavior reference.

---

## 1. Format Specification

### 1.1 Directory Structure

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + Markdown instructions
├── scripts/          # Optional: executable scripts
├── references/       # Optional: on-demand reference docs
├── assets/           # Optional: templates, resource files
```

### 1.2 SKILL.md — Frontmatter

File begins with YAML frontmatter wrapped in `---`:

| Field | Required | Constraints |
|-------|:--------:|-------------|
| `name` | ✅ | 1–64 chars, lowercase letters/digits/hyphens, no leading/trailing hyphens, no consecutive hyphens, must match directory name |
| `description` | ✅ | 1–1024 chars, describes functionality and trigger scenarios |
| `license` | — | License name or reference |
| `compatibility` | — | ≤500 chars, environment requirements |
| `metadata` | — | Arbitrary key-value pairs |
| `allowed-tools` | — | Space-separated list of pre-approved tools (experimental) |

### 1.3 Body Content

Markdown body after frontmatter, no format restrictions. Recommended: step-by-step instructions, input/output examples, common edge cases. Split to `references/` when body exceeds 500 lines; keep overview + routing table in main file.

---

## 2. Discovery

### 2.1 Scan Locations

Agent scans the following paths at startup, collecting subdirectories containing `SKILL.md`:

| Scope | Path | Description |
|-------|------|-------------|
| Project-level | `<project>/.<client>/skills/` | Client-native |
| Project-level | `<project>/.agents/skills/` | Cross-client interop |
| User-level | `~/.<client>/skills/` | Client-native |
| User-level | `~/.agents/skills/` | Cross-client interop |

### 2.2 Scan Rules

- Recursive scan, max depth 4–6 levels; skip `.git/`, `node_modules/`
- Name conflicts: project-level overrides user-level
- Untrusted sources may be skipped or gated
- Cloud/sandbox environments inject via Git clone, URL install, or Web UI

---

## 3. Parsing

Extract YAML between `---` → get `name`, `description`. Error tolerance: retry with quoted values → retry with block scalar → mark as unparseable.

Lenient validation: `name` mismatch/too long → warn but load; `description` missing → skip; YAML completely unparseable → skip.

Storage: `name`, `description`, `location` (absolute path), `body` (store or read on demand), `baseDir`.

---

## 4. Disclosure (Tier 1)

Agent injects catalog into system prompt at startup:

```xml
<available_skills>
  <skill><name>pdf</name>
  <description>Extract PDF text, fill forms, merge files.</description>
  <location>/path/to/pdf/SKILL.md</location></skill>
</available_skills>
```

Accompanying instruction: `When a task matches, use file-read tool to load SKILL.md` or `call activate_skill(name)`. Disabled/unauthorized skills are completely hidden; no catalog shown when zero skills.

---

## 5. Activation (Tier 2)

### 5.1 Progressive Loading

| Tier | Content | When | Tokens |
|------|---------|------|--------|
| 1 | name + description | Session start | ~50–100/skill |
| 2 | Full SKILL.md body | On activation | <5000 (recommended) |
| 3 | scripts/references/assets | On demand | Varies |

### 5.2 Activation Methods

- **File read**: Model uses standard read tool on `location` path (simplest)
- **Dedicated Tool**: `activate_skill(name)`, name constrained to enum to prevent hallucination; can control returning frontmatter/body, wrap in `<skill_content>` tags, list resources
- **User explicit**: `/skill-name` syntax, harness intercepts and injects; autocomplete recommended

### 5.3 Structured Wrapping (Recommended)

```xml
<skill_content name="pdf">
  <!-- body content -->
  <skill_resources>
    <file>scripts/extract.py</file>
  </skill_resources>
</skill_content>
```

Resource list is not pre-loaded; agent references on demand. Cap large directories. Allowlist restricts to skill directory.

---

## 6. Context Management

- **Compaction**: Mark skill content as non-compactable, preserve `<skill_content>` tags; or replace with short reference for next reload (leverage prompt cache)
- **Caching**: Static catalog in system prompt prefix for cache; dynamic conversation at suffix
- **Command exposure**: `/skill-name args`
- **Shared path**: `.agents/skills/` is the most widely adopted cross-product path

---

## Validation

```bash
skills-ref validate ./my-skill
```
