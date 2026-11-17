## Description:

Use when working with Document Mind (DocMind) via Node.js SDK to submit document parsing jobs and poll results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Alibaba Cloud DocMind document parsing jobs, poll asynchronous results, and integrate extracted structure, text, and layout into Claude Code or Codex document understanding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected document URLs or uploaded document content to Alibaba Cloud DocMind for processing.

Mitigation: Use the skill only for documents approved for Alibaba Cloud processing, avoid confidential or internal URLs unless authorized, and choose the intended Alibaba Cloud region before submitting jobs.

Risk: The workflow uses cloud credentials for Alibaba Cloud API calls.

Mitigation: Use least-privilege Alibaba Cloud credentials supplied through environment variables and avoid embedding access keys in prompts, scripts, or output artifacts.

Risk: The artifact validation section references Python compilation even though the included quickstart is Node.js.

Mitigation: Replace or supplement that validation with Node.js checks before relying on the validation result for release or deployment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-docmind-extract)
- [Artifact source list](references/sources.md)
- [Example document URL from artifact references](https://example.com/example.pdf)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Alibaba Cloud credential setup, DocMind request parameters, polling guidance, and result-validation instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
