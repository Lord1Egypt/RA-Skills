## Description:

帮助地球人做人生选择的 AI 判断技能 - 你只管 do it，判断交给滚滚

This skill is ready for commercial/non-commercial use.

## Publisher:

[alsoforever](https://clawhub.ai/user/alsoforever)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to frame personal decisions such as career, relationship, investment, and life choices, compare available options, and receive a recommended choice with reasons, action steps, risks, and follow-up prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide sensitive personal, financial, employment, or relationship details.

Mitigation: Review before installing and avoid entering sensitive details unless data handling, storage, and retention are understood.

Risk: The security summary reports unsafe network exposure and weak privacy controls.

Mitigation: Bind any API service to localhost, add authentication before wider exposure, and document privacy and retention controls.

Risk: Bundled case records may contain personal or sensitive decision examples.

Mitigation: Remove, anonymize, or replace bundled case records before distribution or production use.

Risk: Plaintext or mutable external resources can change or expose data unexpectedly.

Mitigation: Replace mutable external resources with reviewed, pinned, or locally controlled alternatives where practical.

## Reference(s):

- [Skill README](README.md)
- [Usage Guide](USAGE-GUIDE.md)
- [Multi-agent Decision Workflow](GUNGUN-FAMILY-2.0.md)
- [Decision Database Schema](references/database-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/alsoforever/skills/do-it-gungun)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown decision recommendation with optional JSON API response examples and local-use shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a recommendation, reasoning, action plan, risk warnings, emotional support text, and feedback prompts.]

## Skill Version(s):

1.0.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
