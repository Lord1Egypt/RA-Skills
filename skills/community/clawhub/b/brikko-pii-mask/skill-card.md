## Description:

Brikko PII Mask helps agents mask Russian personal data in text before LLM use and restore placeholders in the final response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbchort](https://clawhub.ai/user/bbchort)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when prompts or documents may contain Russian personal data that should be masked before calling an LLM and restored afterward for the user-facing answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext PII and an API key can be sent to a configurable network endpoint.

Mitigation: Use the default HTTPS endpoint only when appropriate for the data, or use a reviewed and pinned self-hosted endpoint for regulated data.

Risk: BRIKKO_API_URL can redirect sensitive traffic to an unsafe remote HTTP endpoint.

Mitigation: Restrict who can set BRIKKO_API_URL and do not configure remote HTTP endpoints.

Risk: Restoration depends on a mapping_id that may expire after the retention window.

Mitigation: Restore placeholders promptly and re-run masking if the mapping_id has expired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbchort/skills/brikko-pii-mask)
- [Publisher profile](https://clawhub.ai/user/bbchort)
- [Brikko homepage](https://brikko.ru)
- [Brikko PII mask documentation](https://brikko.ru/docs/skills/pii-mask)
- [Brikko PII skill repository](https://github.com/brikkoAI/brikko-pii-skill)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; mask.py returns JSON and restore.py returns restored text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BRIKKO_API_KEY; BRIKKO_API_URL may point to a controlled self-hosted endpoint.]

## Skill Version(s):

0.1.0 (source: evidence.release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
