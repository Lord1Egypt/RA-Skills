## Description:

Ezviz safety production inspection skill. Captures device images and sends to Ezviz AI for workplace safety analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to run workplace safety inspections from Ezviz camera snapshots, including PPE, fall, cleanliness, and fire or smoke checks. It is intended for environments where users can authorize Ezviz API access, image capture, and remote AI analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles camera images and sends image URLs to Ezviz AI analysis.

Mitigation: Review privacy requirements before use, test with non-production cameras first, and run only where Ezviz image capture and AI analysis are authorized.

Risk: The skill uses Ezviz credentials and may persist access tokens in a local temporary cache.

Mitigation: Use a dedicated least-privilege Ezviz app, prefer environment variables over command-line secrets, and set EZVIZ_TOKEN_CACHE=0 in shared environments.

Risk: The skill may create or rename a persistent Ezviz intelligent agent.

Mitigation: Confirm remote side effects before running and use credentials scoped to capture and agent APIs only.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ezviz-open/skills/ezviz-open-safety-production-inspection)
- [Ezviz Open API Domain](https://open.ys7.com)
- [Ezviz Token API Endpoint](https://open.ys7.com/api/lapp/token/get)
- [Ezviz AI Analysis Endpoint](https://aidialoggw.ys7.com/api/service/open/intelligent/agent/engine/agent/anaylsis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown-style guidance with API analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ezviz app credentials and device serials; may use token caching unless disabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
