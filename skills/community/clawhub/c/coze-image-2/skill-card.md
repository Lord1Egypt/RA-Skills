## Description:

Coze Image helps an agent generate images from text prompts by calling a configured Coze Seedream 4.5 image-generation workflow and returning the generated image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rookiebug1216](https://clawhub.ai/user/rookiebug1216)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to satisfy image-generation requests by collecting a prompt, running the bundled Coze image script, and returning either a Coze image URL or an optionally saved local image file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to place a Coze API token in source code.

Mitigation: Keep real tokens out of source files; use environment variables or a secret store and review the configured script before use.

Risk: Prompts and related content are sent to Coze through the configured workflow.

Mitigation: Do not include sensitive, confidential, or regulated information in image-generation prompts.

Risk: The optional save path downloads remote content from the returned image URL without validation.

Mitigation: Use the save option only for trusted workflow outputs and write to intentional, non-sensitive paths.

## Reference(s):

- [Coze homepage](https://www.coze.cn)
- [Coze workflow API endpoint](https://api.coze.cn/v1/workflow/run)
- [ClawHub skill page](https://clawhub.ai/rookiebug1216/skills/coze-image-2)
- [Publisher profile](https://clawhub.ai/user/rookiebug1216)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-like command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Coze-hosted image URL and can optionally save a downloaded image file when an output path is supplied.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
