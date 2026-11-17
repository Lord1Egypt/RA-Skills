## Description:

Cn Geo Monitor helps agents plan Chinese AI search optimization across DeepSeek, Kimi, Doubao, Tongyi, and Ernie, with shell helpers for engine lookup and content performance prediction through a remote API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, and developers use this skill to compare brand visibility and content-fit strategies for major Chinese AI search engines. It can guide platform-specific content adaptation and call bundled shell scripts for engine data and prediction scoring.

### Deployment Geography for Use:

Global; intended for Chinese-market AI search optimization workflows.

## Known Risks and Mitigations:

Risk: The prediction script is unsafe with untrusted arguments.

Mitigation: Do not pass untrusted text to predict.sh until its payload construction is fixed; run the skill in a constrained environment.

Risk: Draft content, brand plans, competitor names, and search queries may be sent to the listed Tencent SCF API.

Mitigation: Require explicit confirmation before remote API calls and avoid submitting confidential or sensitive business material.

Risk: Remote data sharing is under-disclosed in the artifact.

Mitigation: Review the API endpoints and data handling expectations before installation or operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/cn-geo-monitor)
- [Publisher profile](https://clawhub.ai/user/lm203688)
- [Skill web app](https://1341839497-1w5tkesfb0.ap-shanghai.tencentscf.com/)
- [Remote API base URL](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, api calls]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote API behavior depends on Tencent SCF service availability; bundled scripts require curl and jq.]

## Skill Version(s):

4.4.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
