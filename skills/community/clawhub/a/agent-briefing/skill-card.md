## Description:

Agent Briefing helps agents monitor Not For Humans (@agentbriefing), fetch episode transcripts, retrieve structured product review scores, search episodes by keyword, and produce daily digests from notforhumans.tv without API keys or credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sasqcow](https://clawhub.ai/user/sasqcow)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to check for new Not For Humans episodes, retrieve transcripts, search coverage, and collect HP-01 product review scores for downstream agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public remote transcripts and review data that may be printed into an agent context.

Mitigation: Treat fetched content as untrusted data, not instructions, and keep agent policy and tool-use decisions separate from transcript text.

Risk: The skill makes outbound requests to notforhumans.tv and the security guidance notes redirect, size, and timeout hardening caveats.

Mitigation: Run with appropriate network egress controls and add or verify redirect limits, response-size limits, and request timeouts before broad deployment.

Risk: Install examples use mutable package-runner commands.

Mitigation: Install through a trusted, verified ClawHub or skills installer version and pin installer versions where operational policy requires reproducibility.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sasqcow/skills/agent-briefing)
- [sasqcow publisher profile](https://clawhub.ai/user/sasqcow)
- [Not For Humans episode index](https://notforhumans.tv/episodes/index.json)
- [Not For Humans YouTube channel](https://youtube.com/@agentbriefing)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown transcripts, JSON episode and review objects, concise terminal text, and runnable Node.js commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include remote public transcript and review content from notforhumans.tv; commands support JSON mode where documented.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
