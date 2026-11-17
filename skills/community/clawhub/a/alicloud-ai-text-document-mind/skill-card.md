## Description:

Use Document Mind (DocMind) via Node.js SDK to submit document parsing jobs and poll results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to submit documents to Alibaba Cloud DocMind, poll asynchronous parsing jobs, and incorporate document structure, text, and layout results into Claude Code or Codex workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive documents may be exposed when submitted through publicly accessible URLs.

Mitigation: Use tightly controlled, short-lived document URLs, revoke access after processing, or use local file upload for sensitive documents when appropriate.

Risk: Alibaba Cloud access keys can grant broader cloud access than the document parsing task requires.

Mitigation: Use least-privileged Alibaba Cloud credentials and avoid printing, saving, or committing access keys.

Risk: DocMind jobs are asynchronous and long polling can delay agent workflows or hide timeout failures.

Mitigation: Set bounded polling intervals and maximum poll counts, then record job IDs, regions, and status summaries for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-text-document-mind)
- [cinience publisher profile](https://clawhub.ai/user/cinience)
- [Artifact source list](references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DocMind job identifiers, polling status, parsed document result summaries, and saved evidence paths.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
