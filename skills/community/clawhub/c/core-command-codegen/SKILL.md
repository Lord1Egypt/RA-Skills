---
name: 框架核心工程师-命令与代码生成
description: Framework core engineer skill for CLI commands, code generation standards, PHP 8.4 compatibility, and framework-safe scaffolding.
version: 1.1.0
---

# Role

This skill owns framework-safe command creation, code generation quality, and PHP compatibility rules for generated or scaffolded code. It keeps command entry points thin and ensures generated code follows Weline conventions instead of generic PHP habits.

# When To Use

- Use for CLI commands, console registration, scaffolding, code templates, or repository-wide code-generation rules.
- Use for keywords such as command, console, generator, scaffold, `command:upgrade`, strict typing, PHP 8.4, and Windows command composition.
- Use when implementation work introduces new command-line entry points or reusable code templates.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/create-framework-command/SKILL.md`
- `dev/ai/skills/code-generation-standards/SKILL.md`
- `dev/ai/skills/php84-performance/SKILL.md`
- `dev/ai/skills/windows-command-quoting/SKILL.md`

# Responsibilities

- Build commands that orchestrate work cleanly without burying business logic inside console handlers.
- Keep generated code aligned with Weline object access, i18n, and testability expectations.
- Apply PHP 8.4-safe null handling and type declarations where appropriate.
- Prevent command-line quoting errors on Windows-sensitive execution paths.

# Workflow

1. Confirm whether the task is command creation, command repair, or code-template generation.
2. Check existing command patterns before introducing new framework APIs or signatures.
3. Implement the command entry point and keep business logic in services.
4. Register or refresh command metadata through the framework command upgrade flow.
5. Apply code-generation guardrails, typing rules, and i18n rules to the produced code.
6. Validate on the intended platform, especially when shell composition or Windows quoting is involved.
7. Report command usage, dependencies, and any environment assumptions.

# Weline Rules

- Do not edit `generated/` directly.
- Run `php bin/w command:upgrade` after creating or changing command registration.
- Do not hardcode user-facing text; use i18n-aware patterns.
- Do not use `declare(strict_types=1)` inside `.phtml`.
- In WLS-sensitive code, do not use `sleep`, `die`, or `exit`.

# Inputs Required

- Command purpose and expected inputs or flags.
- Owning module and related service layer.
- Target environment, including Windows-specific command behavior if relevant.
- Validation path for the command and any generated files.

# Expected Output

- A command or generated-code change that follows Weline conventions.
- Registration and execution validation evidence.
- Notes about platform assumptions, quoting safety, and affected services.

# Validation

- Run `php bin/w command:upgrade` when command registration changes.
- Run the new or updated command with a focused scenario.
- Check for PHP 8.4-safe null and typing behavior in changed code.
- Check that command handlers do not absorb domain logic that belongs in services.

# Constraints

- Do not leave command registration stale after implementation.
- Do not invent helper APIs that are not present in the repository.
- Do not put complex business rules directly inside console execute methods.
- Do not build fragile Windows command strings without explicit quoting discipline.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

