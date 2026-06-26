---
name: environment-doc-author
description: Verify real local environment facts before an agent uses machine-specific commands, runtimes, compilers, services, or startup scripts, then create or refresh environment baseline JSON and related environment policy, AGENTS, or skill documents from those verified facts.
---

# Environment Doc Author

## Overview

Use this skill to turn the current machine state into reusable environment guardrails.
Probe the machine first, keep a machine-readable baseline JSON, and render human-readable policy fragments from verified facts only.

Use it not only when you need to generate or refresh environment documents, but also when an agent task depends on local commands, local runtimes, local package managers, local services, startup scripts, or machine-specific install roots.

This skill supports two standalone implementations:

- JavaScript
  - `scripts/detect_environment.js`
  - `scripts/render_environment_docs.js`
  - Pure Node.js.
- Python
  - `scripts/detect_environment.py`
  - `scripts/render_environment_docs.py`
  - Requires Python 3.7+.

## When To Use

- The task needs real local commands such as `java`, `mvn`, `node`, `npm`, `python`, `go`, `cargo`, `docker`, `kubectl`, `dotnet`, `bundle`, `composer`, or similar tools.
- The agent needs to decide which local executable, runtime manager, install root, env var, or startup script is actually present on this machine.
- The repository needs to create or refresh `environment-baseline.json`, `ENVIRONMENT_POLICY.md`, `AGENTS.environment.md`, `AGENTS.md` environment sections, or reusable environment skill snippets.
- A baseline already exists but may be stale after local toolchain changes, machine migration, shell profile updates, or package manager changes.
- If the repository already has an `AGENTS.md`, default to writing a separate environment snippet such as `AGENTS.environment.md` instead of overwriting the existing file.

## Input Constraints

- Treat the current machine as the authority. Existing docs are hints, not proof.
- Do not invent tools, versions, install roots, symlink targets, env vars, services, ports, package managers, or PATH entries.
- If the task depends on a machine-specific command and the baseline does not already verify it, probe first.
- If the user gives a path or command, verify that it exists before treating it as fact.
- Distinguish a launcher, shim, alias, wrapper, symlink, `.cmd`/`.bat` script, and the real install directory.
- If evidence is missing, say it is unverified. Do not fill the gap with guesses.
- Do not overwrite an existing `AGENTS.md` unless the user explicitly asks for that file to be updated.
- If a command would install, upgrade, uninstall, enable, or reconfigure software, stop and obtain explicit approval first.

## Execution Flow

### 1. Read the existing baseline before probing

- If a machine-level policy already exists, read it first and treat it as the current baseline.
- Prefer a machine-readable JSON baseline when available. Recommended names:
  - `environment-baseline.json`
  - `ENVIRONMENT_POLICY.md`
  - `AGENTS.md` or a dedicated environment snippet
- If your team or machine already has a master environment policy, treat it as the primary source of truth before probing anything else.

### 2. Create the initial baseline when none exists

- Run one implementation against the current machine and save the result as JSON.
- If the immediate task only depends on a small set of local tools, you may still start with a targeted probe, but keep the baseline JSON authoritative once facts are verified.
- Render the JSON into the human-readable docs that the repository or agent stack needs.
- When an `AGENTS.md` already exists, write a separate environment snippet by default and keep merge work explicit and local to the relevant section.
- Keep the JSON and human docs in sync. Do not maintain only one of them.
- Both implementations auto-detect the current machine language and generate Chinese or English docs. If the language cannot be recognized, they default to English.

JavaScript:

```bash
node scripts/detect_environment.js --output ./environment-baseline.json
node scripts/render_environment_docs.js ./environment-baseline.json \
  --policy-out ./ENVIRONMENT_POLICY.md \
  --agents-out ./AGENTS.environment.md \
  --skill-snippet-out ./SKILL.environment.md
```

Python:

```bash
python3 scripts/detect_environment.py --output ./environment-baseline.json
python3 scripts/render_environment_docs.py ./environment-baseline.json \
  --policy-out ./ENVIRONMENT_POLICY.md \
  --agents-out ./AGENTS.environment.md \
  --skill-snippet-out ./SKILL.environment.md
```

Windows note for Python:

- Do not assume the default `python` command is new enough.
- Verify that the selected interpreter is Python 3.7+ before running the Python entry points.

### 3. Use targeted verification when a baseline already exists

- Do not re-probe everything by default when only one tool or task changed.
- If a task mentions a tool not covered by the current baseline, probe that tool first, then update the docs.
- If the current machine state does not match the baseline, record the verified change and refresh both JSON and human docs.
- When the task is "run a local command safely", use the baseline plus a fresh targeted probe to confirm the exact executable, version, and relevant env vars before choosing the command.

JavaScript:

```bash
node scripts/detect_environment.js \
  --baseline ./environment-baseline.json \
  --tools java,maven \
  --output ./environment-baseline.json

node scripts/render_environment_docs.js ./environment-baseline.json \
  --policy-out ./ENVIRONMENT_POLICY.md \
  --agents-out ./AGENTS.environment.md
```

Python:

```bash
python3 scripts/detect_environment.py \
  --baseline ./environment-baseline.json \
  --tools java,maven \
  --output ./environment-baseline.json

python3 scripts/render_environment_docs.py ./environment-baseline.json \
  --policy-out ./ENVIRONMENT_POLICY.md \
  --agents-out ./AGENTS.environment.md
```

### 4. Extend the probe set only when the task requires it

- The built-in detector covers common local tools and core env vars:
  - Git
  - Java
  - `javac`
  - Maven
  - Gradle
  - Node
  - npm
  - pnpm
  - Yarn
  - Python
  - Go
  - Rust (`rustc`, Cargo, Rustup)
  - Clang, Clang++, GCC, G++, CMake, Make, Ninja
  - Ruby, RubyGems, Bundler
  - PHP, Composer
  - .NET SDK
  - Docker
  - kubectl
  - `JAVA_HOME`
  - `MAVEN_HOME`
  - `GRADLE_HOME`, `GOROOT`, `GOPATH`, `CARGO_HOME`, `RUSTUP_HOME`, `DOTNET_ROOT`, `CC`, `CXX`
  - common runtime managers such as `NVM_DIR`, `PYENV_ROOT`, `RBENV_ROOT`, `SDKMAN_DIR`, `HOMEBREW_PREFIX`, `VIRTUAL_ENV`
  - important `PATH` entries
- For services, databases, startup scripts, or project-specific tooling, add an extra probe file and run a targeted scan.
- Read [probe-file.md](./references/probe-file.md) only when you need extra probes.

### 5. Apply the hard rules consistently

- Do not invent tools, versions, install roots, services, or env vars.
- Verify executables with absolute paths and version commands whenever possible.
- Distinguish shims, wrappers, symlinks, aliases, and launchers from real install directories.
- Prefer facts captured in `environment-baseline.json` plus fresh verification over memory or generic platform assumptions.
- If a tool is missing:
  1. Tell the user which tool is missing.
  2. Explain why it is needed.
  3. Ask for the executable path or install directory after installation.
  4. Prefer user-managed installation.
  5. Only install it yourself if the user explicitly requests and authorizes that action.
  6. Update both the JSON baseline and the human docs after verification.
- If a command would modify the machine environment, stop and obtain explicit approval first.

## Output Contract

- Keep these roles distinct:
  - `environment-baseline.json`: machine-readable source of truth for detected facts
  - `ENVIRONMENT_POLICY.md`: human-readable policy and approved environment inventory
  - `AGENTS.environment.md` or `AGENTS.md` snippet: hard rules for agents
  - `SKILL.environment.md` snippet: environment section that can be reused in other skills
- Read [document-contracts.md](./references/document-contracts.md) when you need the exact document shape, language behavior, or update checklist.

## Resources

### `scripts/detect_environment.js`

Standalone Node.js detector. Probes the current machine, merges with an existing baseline when requested, and emits normalized JSON.

### `scripts/render_environment_docs.js`

Standalone Node.js renderer. Generates localized `ENVIRONMENT_POLICY.md`, `AGENTS` snippets, and skill snippets from the baseline JSON.

### `scripts/detect_environment.py`

Python detector. Probes the current machine, merges with an existing baseline when requested, and emits normalized JSON.

### `scripts/render_environment_docs.py`

Python renderer. Generates localized `ENVIRONMENT_POLICY.md`, `AGENTS` snippets, and skill snippets from the baseline JSON.

### `references/document-contracts.md`

Use when you need the exact structure and maintenance rules for the generated docs.

### `references/probe-file.md`

Use when you need to extend the default detector for services, databases, compilers, startup scripts, or project-specific tools.
