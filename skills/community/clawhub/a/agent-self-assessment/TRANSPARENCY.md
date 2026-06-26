# Behavior & Transparency

Honest disclosure of exactly what this skill does, what it can access, and where
it stops. A security/compliance skill should be the most transparent thing in
your toolchain, so this document describes the real behavior rather than a
marketing summary.

## What this skill does

It runs a structured self-assessment. The agent answers a fixed set of
RED/AMBER/GREEN security and compliance questions using only the knowledge
already present in its own context and system prompt, then formats the answers
into a report. That is the entire mechanism.

## Data access

- Reads nothing from disk. No files, no `.env`, no keystores, no configuration.
- Reads no secrets or credentials.
- Does not inspect the host, environment variables, or process state.
- Operates only on information the agent already holds in its current context.

## Tool use

- Requires no tools to run the assessment.
- Makes no network calls.
- The companion note `AGIRAILS-INSTALL.md` lists optional package-install
  commands for separate transaction infrastructure. Those are disclosed as **not
  required** to run the assessment, are never executed by it, and are the
  reader's choice to run or ignore.

## State changes

- Writes no files and modifies no state.
- The report is produced as text in the conversation. Persisting it anywhere is
  the user's decision, not an action this skill takes.

## Limitations (read these)

- The assessment is only as good as what the agent already knows. It is a
  prompt for honest self-reflection, not an external audit, penetration test, or
  certification.
- Anything the agent cannot verify from existing context is scored **RED
  ("Cannot verify")** by design. A RED is an instruction to go check, not a
  failure of the skill.
- Framework dates and obligations (EU AI Act, NIST, OWASP) are current as of
  2026 and must be re-verified against the official sources before any
  compliance claim is made.
- The output is advisory. It does not constitute legal advice or a regulatory
  determination.

## Design principle

Least privilege and transparent disclosure. The skill claims to be read-only and
tool-free, and the instructions in `SKILL.md` enforce exactly that — there is no
gap between what it says it does and what it does.
