## Description:

Guides agents in using arkcli +understand for 12 multimodal understanding recipes, including temporary endpoint credentials and no-side-effect dry runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose and run arkcli recipes for tasks such as transcription, document extraction, image description or localization, and video understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found no reported issues in the reviewed material, but missing local prerequisite references leave some authentication and execution guidance incomplete.

Mitigation: Review the referenced shared arkcli authentication and execution-context guidance before relying on those procedures.

Risk: Input files can be sent to remote inference services, and audio is inlined with a documented 25 MB limit.

Mitigation: Confirm the input is appropriate to share before running a recipe, and prepare oversized audio by splitting or converting it first.

## Reference(s):

- [arkcli-understand command reference](artifact/references/arkcli-understand.md)
- [Sub-skill recipes and expected outputs](artifact/references/sub-skills.md)
- [Evaluation cases](artifact/references/evals.md)
- [ClawHub release page](https://clawhub.ai/jasonstarlight/skills/arkcli-understand)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Markdown, JSON]

**Output Format:** [Natural-language guidance and arkcli command examples; task results may be plain text, Markdown, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output format depends on the selected multimodal recipe; JSON-like results may need parsing from the response content.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
