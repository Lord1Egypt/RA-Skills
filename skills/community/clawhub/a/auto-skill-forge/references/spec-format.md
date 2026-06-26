# Skill Spec Format (`skill_spec.yaml`)

A structured YAML specification for generating a new Skill via `--from-spec` mode.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier (alphanumeric, hyphens, underscores; max 50 chars) |
| `purpose` | string | One-sentence description of what the skill does |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `inputs` | list[{name, type, description}] | What the skill takes as input |
| `outputs` | list[{name, format, description}] | What the skill produces |
| `quality_criteria` | list[{name, description, weight}] | How to judge output quality |
| `domain_knowledge` | list[string] | Key domain facts the skill should encode |
| `reference_skills` | list[string] | Related skills for cross-references |

## Example

```yaml
name: release-notes-generator
purpose: Generate structured release notes from git commit history

inputs:
  - name: commits
    type: git-log
    description: "Git commit log between two tags"
  - name: platform
    type: enum
    description: "Target platform (ios/android/harmony/all)"

outputs:
  - name: release-notes
    format: markdown
    description: "Structured release notes with sections"

quality_criteria:
  - name: platform-isolation
    description: "Notes only reference the target platform"
    weight: 0.3
  - name: categorization
    description: "Commits correctly classified into feat/fix/refactor"
    weight: 0.3
  - name: completeness
    description: "All commits accounted for in the notes"
    weight: 0.2
  - name: readability
    description: "Human-readable, not just commit messages"
    weight: 0.2

domain_knowledge:
  - "NanoCompose has 4 platforms: iOS, Android, HarmonyOS, Core C++"
  - "Conventional commit prefixes: feat, fix, refactor, perf, test, docs, chore"
  - "Core C++ changes affect all platforms"

reference_skills:
  - changelog-gen
  - code-review-enhanced
```

## Validation Rules

1. `name` must be non-empty, max 50 chars, alphanumeric with hyphens/underscores
2. `purpose` must be non-empty
3. `quality_criteria` weights should sum to ~1.0 (not enforced but recommended)
4. `inputs` and `outputs` should each have a `name` field at minimum
