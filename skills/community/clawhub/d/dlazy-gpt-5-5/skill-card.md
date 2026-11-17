## Description:

This skill invokes dLazy's gpt-5.5 CLI workflow for chat, writing, planning, and multimodal analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route prompts and optional image or video inputs through the dLazy CLI for hosted model responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as an OpenAI-style model while using a third-party dLazy hosted service.

Mitigation: Confirm the provider, service terms, and model claims before use, and disclose the third-party dependency to users.

Risk: Prompts and selected media files can be sent to api.dlazy.com and files.dlazy.com.

Mitigation: Do not submit confidential prompts or local file paths unless the data is approved for upload to dLazy.

Risk: The workflow requires running @dlazy/cli@1.2.0 through npm or npx.

Mitigation: Prefer npx or a sandboxed local install, and verify the package and source before execution.

Risk: A dLazy API key may be stored in a local user configuration file.

Mitigation: Protect the local config file, prefer per-invocation environment variables when appropriate, and rotate or revoke keys when access changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dlazyai/skills/dlazy-gpt-5-5)
- [dLazy CLI Source](https://github.com/dlazyai/cli)
- [dLazy CLI npm Package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy Homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, JSON, guidance]

**Output Format:** [JSON responses from the dLazy CLI, often containing generated text or structured model output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports prompt input, up to 10 image references, up to 8 video references, dry-run mode, asynchronous execution, and timeout control.]

## Skill Version(s):

1.3.2 (source: server release evidence; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
