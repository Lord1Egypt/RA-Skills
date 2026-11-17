## Description:

Harvests tagged art images and metadata from supported sites into a dataset for reference, LoRA training, or fine-tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schizofighter](https://clawhub.ai/user/schizofighter)

### License/Terms of Use:

MIT

## Use Case:

Developers and artists use this skill to collect image datasets with tags and source attribution for reference or permitted model training. It can prepare local datasets and optionally upload selected files to external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scraping art sites may conflict with site terms or rights to use and publish images.

Mitigation: Confirm rights and site terms before collecting, training on, or publishing images; start with a small dry run.

Risk: Logged-in browser automation can expose an everyday browsing session.

Mitigation: Use a dedicated browser profile and review which sites and accounts the skill accesses.

Risk: Publishing datasets or sending images to ChatGPT/OpenAI or Hugging Face discloses files to external services.

Mitigation: Use local mode first and inspect exactly which files will be uploaded before approving any external transfer.

## Reference(s):

- [AgentEpstein ClawHub release](https://clawhub.ai/schizofighter/skills/agent-epstein)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and a local image dataset with JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dataset records retain tags and source attribution; external uploads are optional.]

## Skill Version(s):

1.0.3 (source: ClawHub release; bundled frontmatter says 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
