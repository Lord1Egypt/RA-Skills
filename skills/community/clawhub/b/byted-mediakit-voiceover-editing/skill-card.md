## Description:

Volcano Engine AI MediaKit talking-head video editing skill that guides agents through environment setup, media management, audio processing, talking-head cuts, video export, review UI, and iterative refinement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-ai-mediakit](https://clawhub.ai/user/volc-ai-mediakit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn video or audio URLs, local media, VOD IDs, or DirectUrl assets into reviewed talking-head video edits with ASR correction, speech-cut decisions, and export artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local review server can expose readable local files and allows unauthenticated requests to change or export projects.

Mitigation: Bind review and export servers only to 127.0.0.1, avoid exposing them to other hosts, and close them when review or export is complete.

Risk: Cloud and gateway modes require credentials for media, speech recognition, and VOD operations.

Mitigation: Use tightly scoped credentials, keep secrets out of committed files, and prefer a separate VOD space for testing.

Risk: Local dependency or model setup can execute third-party code.

Mitigation: Install and run the skill in an isolated environment and review setup steps before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volc-ai-mediakit/skills/byted-mediakit-voiceover-editing)
- [Skill README](README.md)
- [Environment Template](templates/env.md)
- [Environment Check](references/执行步骤/1. 环境检查.md)
- [URL to ASR Pipeline](references/执行步骤/3. URL到ASR流水线与候选生成.md)
- [Speech Cut Workflow](references/执行步骤/5. 口播剪辑.md)
- [Review and Export](references/执行步骤/6b. 审核与导出.md)
- [EDL Editing Decision Format](references/内置/EDL编辑决策格式.md)
- [User Editing Rules](references/用户规则/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands, configuration steps, and JSON artifact specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides generation and review of ASR-corrected segments, speech-cut decisions, review data, export requests, and exported video metadata.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
