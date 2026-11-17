## Description:

Human-friendly Brickset API v3 access for LEGO set lookup and Brickset automation. Use when you need to search LEGO sets, browse themes, years, or subthemes, validate a Brickset API key, fetch building instructions or additional images, inspect API usage, or build scripts and agents on top of Brickset web services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Brickset API v3 for LEGO set search, catalog metadata, instructions, additional images, API usage, and direct method calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Brickset API key, and passing it on the command line or keeping broad secrets in workspace .env files can expose credentials.

Mitigation: Prefer BRICKSET_API_KEY in the environment, avoid placing unrelated secrets in workspace .env files, and do not share command histories or logs that contain keys.

Risk: Raw mode can call arbitrary Brickset API methods and parameters, including collection-related methods.

Mitigation: Use raw mode only when the intended Brickset method and parameters are known and reviewed.

Risk: getSets calls consume Brickset API quota.

Mitigation: Check usage statistics when needed and keep page sizes and repeated searches appropriate for the task.

## Reference(s):

- [Brickset API v3 quick reference](references/api.md)
- [Brickset API v3 endpoint](https://brickset.com/api/v3.asmx)
- [ClawHub skill page](https://clawhub.ai/stanestane/skills/brickset)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON by default, or readable text summaries when requested with --format text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs reflect Brickset API responses and may include catalog entries, usage statistics, instruction links, image URLs, or raw method result summaries.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
