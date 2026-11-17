## Description:

Generate valid, ClawHub-ready SKILL.md files from product metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use Skillforge to generate ClawHub-ready SKILL.md files from product metadata, instructions, optional environment variables, and optional binary requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the local API server in an inappropriate environment may expose the generator service beyond intended local use.

Mitigation: Run it only where a local Python API server is acceptable, and do not expose the localhost service to untrusted networks.

Risk: Unpinned Python dependencies can reduce reproducibility or assurance for high-control deployments.

Mitigation: Review or pin FastAPI, Uvicorn, Pydantic, and PyYAML dependencies before use in reproducible or high-assurance environments.

Risk: Generated SKILL.md content is based on user-supplied metadata and instructions and may contain incomplete or incorrect skill guidance.

Mitigation: Review generated skill content before publishing or installing it.

## Reference(s):

- [ClawHub Skillforge listing](https://clawhub.ai/mirni/skills/gh-skillforge)
- [ClawHub publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [JSON response containing generated Markdown skill content and a normalized slug]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated SKILL.md includes YAML frontmatter, Markdown instructions, slug normalization, and optional OpenClaw requirements metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
