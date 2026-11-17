## Description:

Generates text-to-video outputs through the Crazyrouter API using supported models such as Sora 2, Kling V2, Veo 3, Seedance, Pika, MiniMax Hailuo, and Runway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xujfcn](https://clawhub.ai/user/xujfcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent to generate short videos from text prompts through Crazyrouter-supported video models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key could be exposed if CRAZYROUTER_BASE_URL is pointed at an untrusted endpoint.

Mitigation: Keep CRAZYROUTER_BASE_URL unset unless the endpoint is intentionally trusted, and use a narrowly scoped Crazyrouter key with spending limits.

Risk: The skill can download arbitrary remote video URLs without strong local limits.

Mitigation: Run it in an isolated environment where outbound downloads cannot reach private services or exhaust local resources.

Risk: Prompts are sent to a third-party video generation service and may be sensitive.

Mitigation: Avoid confidential prompts and review provider terms before using the skill with private or regulated content.

## Reference(s):

- [Crazyrouter](https://crazyrouter.com)
- [ClawHub Skill Page](https://clawhub.ai/xujfcn/skills/crazyrouter-video-gen)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration]

**Output Format:** [Video file when a downloadable video URL is returned, otherwise text status or URL output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY; CRAZYROUTER_BASE_URL should stay unset unless the endpoint is intentionally trusted.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
