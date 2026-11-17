## Description:

Generates a structured Chinese morning briefing on LLM and agent industry developments from configured news, KOL, and arXiv sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[519989179](https://clawhub.ai/user/519989179)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to generate scheduled Chinese Markdown briefings covering LLM and agent news, KOL posts, and arXiv papers, with optional text-to-speech and delivery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic delivery and scheduling can send generated reports to an unintended destination.

Mitigation: Review and edit delivery and cron configuration before installation, and keep external push disabled until the destination is explicitly chosen.

Risk: A hard-coded DingTalk session can route report content to a fixed group.

Mitigation: Remove or parameterize the DingTalk session identifier and require an operator-supplied destination.

Risk: The documented cron flow can invoke an external script under /root rather than only files packaged with the skill.

Mitigation: Replace the cron command with a reviewed local script path and verify logs and output paths before enabling scheduling.

Risk: The network fetcher disables TLS verification and does not document private-address blocking.

Mitigation: Keep TLS certificate and hostname verification enabled, and block private, loopback, link-local, and metadata-service URLs before fetching remote content.

Risk: Optional broad credentials such as GITHUB_TOKEN may be unnecessary for normal report generation.

Mitigation: Provide only the credentials required for reviewed features, prefer least-privilege tokens, and omit optional tokens when not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/519989179/skills/ai-industry-morning-brief)
- [README](artifact/readme.md)
- [Install guide](artifact/install.md)
- [Source configuration](artifact/config/sources.json)
- [Prompt templates](artifact/config/prompts.md)
- [Sample output](artifact/samples/sample-output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report files with optional MP3 audio output and validation logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and curl; optional API credentials affect external search, API limits, and LLM processing.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
