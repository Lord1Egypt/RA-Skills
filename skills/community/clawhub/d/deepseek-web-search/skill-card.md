## Description:

DeepSeek Web Search lets agents ask time-sensitive questions through DeepSeek's server-side web_search tool and receive synthesized answers with source URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingzeng21](https://clawhub.ai/user/mingzeng21)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to answer current-events or time-sensitive questions in Chinese or English when a synthesized answer with consulted URLs is more useful than a raw search result list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A floating npx GitHub install can fetch code that has not been pinned or reviewed.

Mitigation: Install only from a reviewed pinned commit or release.

Risk: Search queries and the DeepSeek API key are sent to DeepSeek over HTTPS during use.

Mitigation: Use a limited-use API key with billing limits and avoid sending sensitive queries.

Risk: The default installer copies the skill into every supported harness directory.

Mitigation: Use the single-harness install flags when only one agent environment should receive the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingzeng21/skills/deepseek-web-search)
- [DeepSeek platform](https://platform.deepseek.com)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with synthesized answer text, source URLs, query, model, usage, and engine fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default max output is 8000 tokens, capped at 16384; requests can run for up to 120 seconds.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
