---
name: analyze-json-data
description: >
  Use when (1) Analyze JSON data and generate a structured API design document or OpenAPI specification. 
license: MIT
metadata:
  version: "1.0"
  category: design
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---
## Core Position

This skill solves the specific engineering problem described in the trigger conditions. It focuses on **reliable, auditable execution** with clear error reporting.

## Modes

### `/analyze-json-data`
**Default mode.** Performs the core task with standard configuration.

### `/analyze-json-data --verbose`
**Verbose mode.** Includes detailed logging and intermediate results.

## Execution Steps

1. **Parse input** — Validate and parse the input data; report any structural issues
2. **Validate** — Confirm all required fields/parameters are present and well-formed
3. **Execute** — Perform the transformation/action with validated input
4. **Verify** — Check the output is well-formed and complete
5. **Report** — Return structured output with a brief summary of what was done

## Mandatory Rules

### Do not

- Do not make up facts or claim actions were taken that were not
- Do not hardcode API keys — use `os.getenv("API_KEY")` instead
- Do not store sensitive user data beyond the current session
- Do not exceed token budget without warning the user first
- Do not activate for off-topic requests — return a brief decline message

### Do

- Validate all inputs before acting
- Handle errors gracefully with actionable error messages
- Log actions taken for auditability
- State explicitly when you are uncertain or data is insufficient

## Quality Bar

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Task completion | Core task completes without error | Full task with all edge cases handled |
| Error reporting | Clear error message on failure | Actionable error with suggested fix |
| User communication | Brief summary of what was done | Detailed log with reasoning for decisions |
| Input validation | Rejects malformed input | Accepts valid input, explains rejection for invalid |

A good output is one where all edge cases are handled gracefully with clear user communication.

## Good vs. Bad Examples

| Scenario | Bad | Good |
|---------|-----|------|
| Task unclear | Attempts anyway, may be wrong | Asks for clarification before proceeding |
| Error | Technical error message | "Cannot [action]: [reason] — suggest [alternative]" |
| Partial success | Reports "Done" | Reports "Done, but [partial] not completed — see details" |
| Edge case | Silently skips or crashes | Documents edge case and handles gracefully |
