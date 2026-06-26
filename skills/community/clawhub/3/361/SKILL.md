---
name: 361scan
description: Scan and analyze installed skills. Use when user wants to (1) scan a specific skill directory to view its name, description, and details, or (2) scan all installed skills to list all available skills with their names and descriptions. Triggers on phrases like "scan skill", "list skills", "361 scan", "scan all skills".
---

# 361scan - Skill Scanner

Scan and analyze installed skills in the OpenClaw workspace's skills directory.

## Setup
```
pip install skill-361
```

## Usage

### Scan a specific skill
```
361 scan <skill-path>
```
Example: `361 scan ~/.openclaw/skills/my-skill`

### Scan all installed skills
```
361 scan-all <skills-directory>
```
Example: `361 scan-all ~/.openclaw/skills`

## How It Works

1. **Validate the target path** - Check if the directory exists
2. **Find all SKILL.md files** - Recursively search for SKILL.md in subdirectories
3. **Parse skill metadata** - Extract name and description from YAML frontmatter
4. **Display results** - Show skill name, path, and description in a readable format

## Output Format

For each skill found:
- **Name**: Extracted from frontmatter `name` field
- **Path**: Relative or absolute path to the skill
- **Description**: Extracted from frontmatter `description` field

## Examples

**Scan specific skill:**
```
361 scan ~/.openclaw/workspace/skills/clawbackup
```
Output:
```
Skill:  clawbackup
  Status: 🟢 SAFE
  Score:  87/100
  Issues: 4
  Breakdown: ☠️ 0  🚨 0  ⚠️ 1  ℹ️ 1
```

**Scan all skills:**
```
361 scan-all ~/.openclaw/workspace/skills
```

## Implementation Notes

- Skills are directories containing a SKILL.md file
- YAML frontmatter must have `name` and `description` fields
- Recursive search allows scanning nested skill directories
- Handle missing or malformed SKILL.md files gracefully
