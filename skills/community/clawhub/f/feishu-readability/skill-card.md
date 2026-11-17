## Description:

Provides Feishu document formatting and safe editing guidance for agents before modifying mi.feishu.cn documents, covering minimal edits, rich-text protection, spacing, and bold text conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:


## Use Case:

Agents and document editors use this skill to safely improve Feishu/Lark document readability while preserving existing content, comments, image tokens, and rich text. It is intended for workflows that modify mi.feishu.cn documents or use Feishu MCP update-doc operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer document style choices in legal, compliance, multilingual, or externally governed documents.

Mitigation: Tell the agent to preserve the document's existing style guide when applying the skill to governed or sensitive documents.

Risk: Incorrect Feishu edit ranges can damage comments, history, images, or rich-text tokens.

Mitigation: Use the skill's minimal-edit guidance, avoid broad overwrite operations, and fetch complete tokens before editing paragraphs that contain special blocks.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline examples and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is bundled; outputs guide safe document-editing behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
