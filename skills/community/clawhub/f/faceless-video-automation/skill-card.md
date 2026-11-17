## Description:

AI-powered workflow for producing faceless videos across Bilibili, YouTube, and Douyin, including topic discovery, scripts, voiceover text, visual prompts, subtitles, and publishing plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and channel operators use this skill to plan and produce batches of faceless short-form and long-form videos. It helps generate scripts, voiceover text, visual search keywords, subtitles, cover copy, tags, and publishing schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes persistent self-learning behavior that stores usage, errors, notes, and preferences in a local JSON file and can influence later outputs.

Mitigation: Review or remove the learner before deployment; avoid entering credentials, personal data, private business information, or instruction-like text in notes and preferences.

Risk: Batch faceless-video generation can publish incorrect, rights-sensitive, or platform-policy-violating content if outputs are used without review.

Mitigation: Require human review for factual accuracy, asset rights, disclosures, and platform policy compliance before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/faceless-video-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown plus plain-text, SRT, CSV, and shell-command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include batch deliverable sets for multiple videos.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
