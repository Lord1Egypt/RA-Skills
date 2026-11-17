## Description:

Mobile Use Agent starts and monitors natural-language mobile automation runs on Volcengine Cloud Phone using Doubao vision-based understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to launch, poll, retrieve results from, and cancel Volcengine Cloud Phone Mobile Use Agent runs for mobile app navigation, UI interaction, form filling, and screen-understanding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed mobile automation can act broadly within a cloud-phone environment.

Mitigation: Use least-privilege, rotated Volcengine or Ark Skill API credentials and restrict product and pod IDs to the intended task environment.

Risk: ARK_SKILL_API_BASE and VOLC_HOST can redirect requests to alternate provider endpoints.

Mitigation: Leave endpoint override variables unset unless the proxy or host is explicitly trusted and documented for the deployment.

Risk: Prompts, progress events, and raw service responses may expose sensitive task or account data.

Mitigation: Do not place long-lived secrets in prompts or logs, and review retention and redaction for JSONL output before production use.

Risk: Screen recording can capture app content and requires configured object storage.

Mitigation: Enable screen recording only when necessary, configure trusted TOS storage, and limit access to recorded artifacts.

Risk: Unpinned runtime dependencies can change behavior between installs.

Mitigation: Pin and review dependency versions for production deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-ai-mobileuse-agent)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)
- [SKILL.md](artifact/SKILL.md)
- [Mobile Use reference](artifact/references/mobile_use.md)
- [MUA Agent Instructions](artifact/references/MUA_Agent_Instructions.md)
- [Python requirements](artifact/references/requirements.txt)
- [Mobile Use Agent console](https://console.volcengine.com/ACEP/Business/6)
- [Volcengine API access keys](https://console.volcengine.com/iam/keymanage)
- [Volcengine app publishing instructions](https://www.volcengine.com/docs/6394/1223958?lang=zh)
- [Volcengine screen recording reference](https://www.volcengine.com/docs/6394/1997312?lang=zh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSONL progress and result events, JSON helper output, and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streams started, progress, result, and error events; helper commands may include raw service responses.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
