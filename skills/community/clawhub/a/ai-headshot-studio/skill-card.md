## Description:

Transform a casual selfie into a studio-quality professional headshot for LinkedIn, resume, company website, business card, or social media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

People who need a professional profile portrait use the skill to turn a selfie into a headshot tailored to their industry, intended platform, and preferred style, or to refine an accepted headshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports broad unrelated permissions and a shared credential broader than headshot generation.

Mitigation: Review the requested account access before authorizing, and check whether other Beatra skills rely on the shared connection before disconnecting it.

Risk: A selected selfie is uploaded for remote image generation, and the security guidance notes that the skill lacks a clear notice before upload.

Mitigation: Tell the user which photo will be uploaded and where it will be sent, then obtain their approval before uploading it.

Risk: ClawScan reports installation telemetry and warns that uninstalling may disrupt other skills; the review is incomplete because some local references could not be resolved.

Mitigation: Review the telemetry and shared-installation details, and resolve the unavailable references before relying on the skill.

## Reference(s):

- [AI Headshot Studio on ClawHub](https://clawhub.ai/beatra-ai/skills/ai-headshot-studio)
- [Beatra](https://beatra.ai)
- [Headshot workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Image files, Text guidance]

**Output Format:** [Generated headshot image with Markdown delivery details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One headshot per generation request; delivery details include artifact links, dimensions, task ID, and net credits when available.]

## Skill Version(s):

0.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
