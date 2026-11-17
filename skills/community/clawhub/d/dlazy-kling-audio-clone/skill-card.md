## Description:

Generates customized speech from uploaded reference audio using Kling Audio Clone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to authenticate with the dLazy CLI, upload an authorized voice reference, and request custom speech generation through the Kling Audio Clone service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected voice reference audio to dLazy-hosted services.

Mitigation: Use only audio the user is authorized to submit, avoid sensitive voice samples, and confirm consent from the speaker before cloning.

Risk: The skill depends on a third-party CLI package, hosted API, and API key.

Mitigation: Prefer temporary npx execution or review the pinned package before global installation, and use a revocable API key.

Risk: The security summary notes inconsistent documentation about commands and returned outputs.

Mitigation: Check the CLI help or use dry-run behavior before relying on parameters, cost, or output shape in an automated workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dlazyai/skills/dlazy-kling-audio-clone)
- [dLazy CLI Source](https://github.com/dlazyai/cli)
- [@dlazy/cli npm Package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy Homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm or npx and a dLazy API key; may upload local audio references to dLazy-hosted services and return hosted output URLs.]

## Skill Version(s):

1.3.8 (source: server release metadata; artifact frontmatter lists 1.3.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
