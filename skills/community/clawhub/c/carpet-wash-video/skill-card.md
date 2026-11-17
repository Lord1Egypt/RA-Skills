## Description:

Carpet Wash Video helps agents generate satisfying vertical carpet deep-clean shorts with WeryAI from text prompts or dirty rug photo URLs, emphasizing rinse action, grime runoff, and fiber revival.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn carpet-cleaning briefs or HTTPS rug images into WeryAI video-generation requests for vertical satisfying shorts. Agents use it to expand prompts, confirm parameters, run the WeryAI CLI helper, and return playable video URLs or clear error guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed prompts, optional HTTPS image URLs, and the WERYAI_API_KEY bearer token are sent to the configured WeryAI endpoint.

Mitigation: Set WERYAI_API_KEY only in trusted environments and run the skill only when sending that content to WeryAI is acceptable.

Risk: WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL overrides can redirect requests and credentials away from the default WeryAI hosts.

Mitigation: Review or unset those override variables before use unless the alternate endpoint is explicitly approved.

Risk: The skill is intended for paid WeryAI video generation and may consume account credits.

Mitigation: Install and run it only when paid WeryAI use is intended, and keep the documented confirmation step before submission.

Risk: Generation depends on network access, Node.js 18 or newer, valid model parameters, and WeryAI service availability.

Mitigation: Use the documented dry-run, status, and error outputs to verify requests and provide clear recovery guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/carpet-wash-video)
- [WeryAI generation API host](https://api.weryai.com)
- [WeryAI models API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON CLI command examples and WeryAI video URL results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return playable video URLs, task status, or structured error guidance after API polling.]

## Skill Version(s):

0.1.0 (source: server release evidence and target metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
