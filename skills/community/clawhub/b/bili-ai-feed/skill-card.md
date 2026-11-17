## Description:

AI B站信息源 generates Bilibili AI trend reports by querying RedFox data, clustering popular videos, and producing structured intelligence briefings with an HTML daily report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External AI researchers, industry intelligence analysts, and content operators use this skill to monitor Bilibili AI video trends, discover popular topics, and generate structured topic investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags credential handling, plaintext key storage, and a hardcoded key as review concerns.

Mitigation: Use only a revocable, low-scope RedFox key, keep it out of prompts and shared outputs, and rotate or revoke it if exposed.

Risk: The security review flags scheduled subscription behavior as needing review before use.

Mitigation: Avoid enabling daily subscription until the scheduler behavior and key storage are reviewed and fixed.

Risk: Generated HTML reports may contain untrusted content from retrieved video metadata or investigation sources.

Mitigation: Review generated reports before sharing them and treat embedded links and rendered content as untrusted.

Risk: The security review flags the people-background investigation mode as a privacy concern.

Mitigation: Avoid person-background investigations unless clear privacy safeguards and user controls are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/bili-ai-feed)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?souce=github)
- [Engine strategy](references/engine-strategy.md)
- [Investigation modes](references/investigation-modes.md)
- [Investigation templates](references/investigation-templates.md)
- [Investigator config](references/investigator-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Structured Markdown response plus locally generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RedFox API key; reports may include Bilibili links, cover images, engagement data, credibility labels, and local HTML output.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
