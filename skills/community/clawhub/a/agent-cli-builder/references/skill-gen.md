# Skill Generation, Synchronization, and Distribution

Generate mechanical command facts from source and write trigger, workflow, and safety semantics by hand. Never maintain a duplicate command index manually.

## Contents

1. Commands and generation workflow
2. Frontmatter and semantic content
3. AUTO-GEN block
4. References and independent installation
5. Synchronization and install wizard
6. Security and validation

## 1. Commands and generation workflow

Setting `skillsDir: "./skills"` adds:

| Command                                      | Behavior                            |
| -------------------------------------------- | ----------------------------------- |
| `<bin> skills list`                          | List bundled Skills                 |
| `<bin> skills read <name>`                   | Print a `SKILL.md`                  |
| `<bin> skills read <name>/references/<file>` | Print a reference                   |
| `<bin> skills gen <name> --init [--lang zh]` | Create a skeleton and command index |
| `<bin> skills gen <name>`                    | Refresh only AUTO-GEN               |
| `<bin> skills sync`                          | Synchronize discovery directories   |

Workflow:

```bash
# Commands already use defineCommand and every argument has desc.
my-cli skills gen my-skill --init

# Edit semantic content outside AUTO-GEN.
my-cli skills gen my-skill

my-cli skills list --json
my-cli skills sync --json
```

Use `--init` only for initial creation. Refresh an existing file without it to preserve semantic content.

## 2. Frontmatter and semantic content

The current generator creates:

```yaml
---
name: my-skill
description: <capability, trigger phrases, and nearest exclusion boundary>
metadata:
  requires:
    bins: ["my-cli"]
  category: business
---
```

- Match `name` to the directory and use lowercase letters, digits, and hyphens.
- Put all invocation criteria in `description`: capability, natural-language triggers, and nearest exclusion.
- Set `metadata.requires.bins` to the real bin.
- Keep version information in `package.json`, not Skill frontmatter.

Example:

```yaml
description: Query and manage todos. Use when the user wants to list, create, or complete todos; calendar events and project milestones are out of scope.
```

Do not repeat a complete trigger table in the body. Keep routing after invocation, non-obvious arguments, multi-step dependencies, safety limits, and recovery. Apply `skill-optimization.md` before release.

## 3. AUTO-GEN block

```markdown
<!-- AUTO-GEN:START commands -->

## Commands

| Operation  | Command                                |
| ---------- | -------------------------------------- |
| List todos | `my-cli todos list [--limit <number>]` |

<!-- AUTO-GEN:END -->
```

AUTO-GEN contains operation descriptions and signatures, not detailed argument tables. When scoped commands use JSON args, it also emits transport plus `--input-schema` / `--input-example` discovery commands. Regenerate it after command or args-schema changes.

Generated signatures follow source schema:

| Argument            | Signature             |
| ------------------- | --------------------- |
| Required positional | `<id>`                |
| Optional positional | `[offset]`            |
| Required flag       | `--status <string>`   |
| Optional flag       | `[--limit <number>]`  |
| Optional boolean    | `[--force]`           |
| Optional array      | `[--tag <string>...]` |

Put enums, ranges, fields, and pagination in references.

Do not copy a structured payload's complete JSON Schema into `SKILL.md`. Link a focused field/workflow reference when semantic guidance is needed and let agents retrieve the current machine contract with `--input-schema`.

## 4. References and independent installation

```text
skills/my-skill/
├── SKILL.md
└── references/
    └── domain-fields.md
```

- Link every reference directly from `SKILL.md` and state when to read it.
- Put detailed arguments, fields, enums, and complex workflows in references, not both places.
- Keep every required file inside the Skill. Do not use symlinks or cross-Skill relative paths.
- Ensure `package.json.files` includes `dist` and `skills`; verify the package listing.

Installation references should first check whether the bin exists, disclose global install, file synchronization, and network effects, obtain any required approval, and verify with `<bin> --help`.

## 5. Synchronization and install wizard

Without `skillsTargets`, `skills sync` always writes `~/.agents/skills` and writes Claude, Codex, Cursor, ZCode, OpenClaw, and Pi directories only when their parent tool directories exist.

Explicit `skillsTargets` replaces the default candidates and forces all specified destinations. An empty array disables synchronization targets.

```ts
defineCli({
  skillsTargets: [
    { key: "claude", dir: "~/.claude/skills" },
    { key: "codex", dir: "~/.codex/skills" },
  ],
});
```

`defineInstaller({ skillsSource })` (a plugin in `defineCliApp`'s `plugins`) provides the top-level `install` command; it uses local `<bin> skills sync` when `skillsSource` is empty and tries `npx skills add <url>` with local fallback when set. The local state comes from `defineCliApp({ dir })` via `apply(services)` — the installer takes no directory parameter. `defineCli({ skillsSource })` does not forward the value to the wizard; pass it explicitly to `defineInstaller`.

The wizard may create a global package, Skill files, configuration, and credentials. Disclose those effects in agent-facing installation instructions.

## 6. Security and validation

`skills read` and `skills gen` reject absolute paths, `..`, realpaths outside `skillsDir`, and outward symlinks. Do not bypass these protections.

Before release:

1. Run `skills gen` and confirm content outside AUTO-GEN is unchanged.
2. Verify all references and links.
3. Run the Skill validator and TRACE checklist in `skill-optimization.md`.
4. Evaluate should-trigger, paraphrase-trigger, and should-not-trigger requests.
5. Dry-run packaging and confirm every Skill is independently readable.
6. Forward-test complex or public Skills as described in `testing.md`.
