## Description: <br>
Document to Mindmap turns documents, long text, Markdown, webpages, and image text into structured ProcessOn mind-map Markdown for editable mind maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leilizhang](https://clawhub.ai/user/leilizhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill to summarize documents, meeting notes, study materials, reports, and other source content into structured ProcessOn mind maps for review, editing, and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document content may be uploaded to ProcessOn during conversion. <br>
Mitigation: Use the skill only with documents appropriate for ProcessOn processing, and remove sensitive material before conversion. <br>
Risk: The skill includes a runtime update path that can modify the installed skill when the force-update command is approved. <br>
Mitigation: Review the update prompt and referenced repository before approving any forced update command. <br>
Risk: Cleanup options and temporary-file handling can delete Markdown input files. <br>
Mitigation: Use disposable temp or cache copies for conversion inputs, and avoid cleanup flags on files that must be preserved. <br>
Risk: The client creates and reuses a ProcessOn partner flag for tracking or attribution. <br>
Mitigation: Review the partner-flag behavior before installation and avoid using the skill where that identifier is unsuitable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leilizhang/document-to-mindmap) <br>
- [Artifact README](artifact/README.md) <br>
- [ProcessOn skill update path referenced by the artifact](https://github.com/processonai/processon-skills/tree/main/skills/document-to-mindmap) <br>
- [ProcessOn Markdown transform API referenced by the client](https://smart.processon.com/v1/api/transform/md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, shell commands, links, guidance] <br>
**Output Format:** [Markdown plus complete ProcessOn image and online-view URLs; the client script returns JSON that the agent presents as text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated from user-provided source content and may include a ProcessOn image URL and editable online-view URL.] <br>

## Skill Version(s): <br>
1.1.10 (source: SKILL.md frontmatter, artifact/version/github-version.json, artifact/version/coze-version.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
