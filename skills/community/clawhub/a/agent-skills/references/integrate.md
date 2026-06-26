# Agent Skills Integration Guide

## Progressive Loading

Tier 1: name+desc (session start, ~50-100t) → Tier 2: full body (on activation, <5000t) → Tier 3: refs/scripts (on demand)

## Step 1: Discovery

### Scan Paths

Project + user level, client directories + `.agents/skills/` (cross-client), optionally `.claude/skills/` for compatibility. Find `SKILL.md` in subdirectories, skip `.git/`/`node_modules/`, cap at 4-6 levels deep.

Name collisions: project overrides user. Untrusted repos: consider skipping or setting a trust gate. Cloud/sandbox agents need external provisioning (clone repo / URL install / Web UI).

## Step 2: Parsing

Extract YAML between `---` → name, description. Fault-tolerant: wrap unquoted colon values in quotes or retry with block scalars.

Lenient validation: name mismatch dir/too long → warn but load; description missing → skip; YAML unparseable → skip.

Store: name, description, location (absolute path), body (store or read on demand), base dir (derived from location).

## Step 3: Disclosure (Tier 1)

Catalog format (in system prompt or tool description):
```xml
<available_skills>
  <skill><name>pdf</name><description>Extract PDF text...</description>
  <location>/path/to/SKILL.md</location></skill>
</available_skills>
```

Behavior instruction: "When a task matches, use file-read tool to load SKILL.md" or "call activate_skill(name) tool". Hide disabled/permission-denied skills. No skills → no catalog, no tool registration.

## Step 4: Activation (Tier 2)

**File-read activation**: model reads path with standard read tool (simplest).

**Dedicated tool activation**: `activate_skill(name)`, constrain name as enum to prevent hallucination. Can: control frontmatter return, wrap `<skill_content>` tags, list resources/, permission checks.

**User explicit activation**: `/skill-name` syntax, harness intercepts and injects. Suggest autocomplete.

**Return content**: full file or body-only (strip frontmatter).

**Structured wrapping** (recommended):
```xml
<skill_content name="pdf"><skill_resources>
  <file>scripts/extract.py</file></skill_resources></skill_content>
```

List resources without eager reading. Allowlist skill directory to avoid permission prompts.

## Step 5: Context Management

- During compaction: mark skill content as non-compressible, preserve `<skill_content>` tags; or replace with short ref and reload on next activation (leverage prompt cache)
- Static catalog in system prompt prefix for caching; dynamic conversation in suffix
- Expose skills as commands: `/skill-name args`
- `.agents/skills/` is the most widely adopted cross-product sharing path
