# README Generation Guide

A README serves developers and terminal users; a Skill serves AI agents. They share fact sources but should not duplicate each other.

## Contents

1. Sources and structure
2. Installation copy
3. Authentication variants
4. Output and development
5. Release checks

## 1. Sources and structure

Extract facts from implementation rather than filling a template from memory:

| README content                 | Source of truth                                    |
| ------------------------------ | -------------------------------------------------- |
| Package, bin, Node.js version  | `package.json`                                     |
| Positioning, commands, domains | `defineCli`, `defineCommand`                       |
| Installation effects           | `defineInstaller` plugin options in `defineCliApp` |
| Authentication                 | Auth implementation and real `--help`              |
| Output and pagination          | Command returns and `defaultFormat`                |
| Development commands           | `package.json.scripts`                             |

Keep only sections that add value:

1. One-sentence purpose and scope.
2. Installation, verification, and material side effects.
3. Three to eight frequent commands.
4. Authentication or environment configuration when required.
5. Output contract and important limitations.
6. Development, test, and release commands for source projects.

Do not add empty sections, marketing claims, invented links, or scripts that do not exist.

## 2. Installation copy

When the entry point implements the install wizard:

````markdown
## Installation

Requires Node.js {{engines.node}}. This command globally installs the CLI and synchronizes bundled Skills to detected AI-tool directories:

```bash
npx {{package-name}} install
```

Verify:

```bash
{{bin}} --help
{{bin}} skills list --json
```
````

Describe actual effects: global npm package, network downloads, Skill directories, configuration, and credentials. Do not claim steps the source does not perform.

Offer manual installation for troubleshooting:

```bash
npm install -g {{package-name}}
{{bin}} skills sync --json
{{bin}} --help
```

If the app has no `defineInstaller` plugin, do not document `npx <pkg> install`.

## 3. Authentication variants

### No authentication

State that no login is required and omit an empty credentials section.

### OAuth / `defineAuth`

For human terminal users:

```bash
{{bin}} auth register
{{bin}} auth login
{{bin}} auth status --json
```

Include registration only when the implementation requires dynamic client registration. Current interactive registration input is not masked, so instruct users to work in a private terminal. Never ask them to paste a real token into chat or recommend `--token <real-value>` in the README.

The business Skill must document split-flow login for an agent; do not copy the blocking human command unchanged.

### Static credentials or custom auth

Do not show long-lived secrets as command arguments. Prefer controlled environment variables or a genuinely masked prompt implemented by the product:

```bash
export MY_CLI_API_KEY="<read from your secure credential system>"
{{bin}} auth status --json
```

Never claim at-rest encryption unless the storage implementation and tests prove it.

## 4. Output and development

Match output copy to `defaultFormat`:

```markdown
Agents and scripts should pass `--json`. Successful data goes to stdout; errors and logs go to stderr.
```

Do not claim pagination is automatic. Mention `complete` and `nextToken` only for commands that return `meta.pagination`.

Derive command examples from `--help` and execute each one. Never invent `--dryRun`; structured operations expose the kebab-case `--dry-run` and `--yes` flags only when declared by `operation`.

For a structured command, show one safe file or stdin invocation plus discovery rather than a long inline payload:

```bash
{{bin}} orders create --input-file ./order.json --idempotency-key <stable-key> --yes
{{bin}} orders create --input-schema
```

Explain that exactly one input source is required and that inline secrets may leak through shell history or process listings.

List only real scripts:

```bash
pnpm --filter {{package-name}} typecheck
pnpm --filter {{package-name}} build
pnpm --filter {{package-name}} test
```

Record only maintenance-critical decisions, such as package/bin/namespace mapping, auth strategy, and error mapping.

## 5. Release checks

- [ ] Package, bin, Node.js version, and scripts match `package.json`.
- [ ] Every example matches current `--help` and runs.
- [ ] Installation, login, writes, and network effects are disclosed.
- [ ] Examples contain no real credentials, personal data, production IDs, or private endpoints.
- [ ] JSON, errors, pagination, and exit-code descriptions match execution.
- [ ] Human README and agent Skill installation semantics agree.
- [ ] Package dry-run contains README, dist, Skills, and references.
