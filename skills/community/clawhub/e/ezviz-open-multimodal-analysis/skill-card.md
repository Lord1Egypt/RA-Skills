## Description:

Analyzes Ezviz camera snapshots by capturing device images and sending image URLs to an Ezviz AI agent for multimodal scene understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to analyze Ezviz camera views for scene understanding, behavior review, object detection, and safety checks across one or more devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Ezviz camera credentials and access tokens that could expose camera access if stored or shared improperly.

Mitigation: Use a dedicated least-privilege Ezviz application, keep secrets in protected environment or secret-manager configuration, and avoid passing AppSecret on the command line.

Risk: Token caching on shared systems can leave reusable access material in the system temp directory.

Mitigation: Set EZVIZ_TOKEN_CACHE=0 on shared systems or review cache permissions and lifecycle before deployment.

Risk: Camera images and signed image URLs can reveal sensitive visual data or temporary access links.

Mitigation: Review output and logging paths before scheduled use, and remove signed image URLs from normal output and logs.

## Reference(s):

- [Ezviz Agent API Reference](references/ezviz-agent-api.md)
- [ClawHub Skill Page](https://clawhub.ai/ezviz-open/skills/ezviz-open-multimodal-analysis)
- [Ezviz Open Platform](https://openai.ys7.com/)
- [Ezviz Access Token API](https://openai.ys7.com/help/81)
- [Ezviz Device Capture API](https://openai.ys7.com/help/687)
- [Ezviz Agent Analysis API](https://openai.ys7.com/help/5006)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [Console text with parsed JSON analysis results and setup command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ezviz credentials, device serials, and an agent ID; captured image URLs are short-lived and analysis shape depends on the configured Ezviz agent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
