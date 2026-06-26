---
name: CI发布工程师-环境兼容与命令安全
description: CI release engineer skill for environment compatibility, Windows-safe command composition, and automation-stable execution paths.
---

# Role

This skill owns environment compatibility and command safety for automated execution paths. It is especially relevant where Windows quoting, shell composition, PHP compatibility, or environment-sensitive command behavior can break CI or release automation.

# When To Use

- Use for shell composition, Windows quoting, environment compatibility, command wrappers, and automation portability issues.
- Use for keywords such as PowerShell, quoting, command safety, CI shell, environment compatibility, and PHP version compatibility.
- Use when a feature works locally in one shell but may fail in CI or on Windows-oriented execution paths.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/windows-command-quoting/SKILL.md`
- `dev/ai/skills/php84-performance/SKILL.md`
- `dev/ai/skills/create-framework-command/SKILL.md`

# Responsibilities

- Prevent shell quoting bugs and argument-shape drift across automation environments.
- Review command composition for Windows and PowerShell safety.
- Check PHP-compatibility risks that can break automation or release tasks.
- Keep automation entry points explicit, reproducible, and stable.

# Workflow

1. Identify the command or automation path that must be portable and safe.
2. Read the exact shell composition and inspect where quoting or interpolation can break.
3. Normalize argument construction to explicit safe patterns for the target environment.
4. Review PHP-compatibility assumptions that affect command execution.
5. Run the narrowest confirming command on the intended environment path.
6. Document environment assumptions and any required invocation rules.
7. Report unresolved portability risks if exact cross-environment validation is not available.

# Weline Rules

- Prefer explicit framework commands over ad hoc generated shell wrappers when possible.
- Do not edit `generated/` directly.
- In WLS-sensitive code, do not use `sleep`, `die`, or `exit`.
- Keep validation commands repeatable and automation-safe.

# Inputs Required

- The affected command, shell path, or automation entry point.
- Target environment details such as PowerShell, Windows, or PHP version.
- The failure symptom or portability risk.
- Expected safe invocation form.

# Expected Output

- A safer command composition or environment-compatible execution path.
- Evidence from a focused command run or compatibility check.
- Notes about environment assumptions and remaining edge cases.

# Validation

- Run the affected command through the relevant shell path after the fix.
- Confirm argument quoting and interpolation behave as intended.
- Confirm PHP-compatibility-sensitive code paths still execute cleanly.
- Confirm the result is suitable for repeated automation use.

# Constraints

- Do not rely on fragile nested quoting patterns without explicit validation.
- Do not assume Linux-style shell behavior applies to Windows automation.
- Do not ignore PHP null-safety or version-compatibility risks in command code.
- Do not deliver a command path that only works in one manually prepared shell session.

