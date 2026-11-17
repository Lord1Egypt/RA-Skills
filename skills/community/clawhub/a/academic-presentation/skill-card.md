## Description:

Academic Presentation automates turning a paper PDF or pasted text into Chinese translation notes, a structured summary, a slide deck, and speech notes, then sends the generated files to WeChat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-feng12](https://clawhub.ai/user/j-feng12)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and academic presenters use this skill to convert papers into presentation-ready materials: translated Word notes, structured summaries, 10-15 slide presentation drafts, and speaker notes. It is most appropriate for papers the user is comfortable processing through the selected presentation provider and WeChat delivery workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send research materials to external presentation providers and to WeChat.

Mitigation: Use it only with papers approved for those services, or choose the skip/local-only path and confirm that no messaging occurs.

Risk: The artifact claims privacy protections that conflict with the external upload and WeChat delivery behavior summarized by the security evidence.

Mitigation: Review provider data handling and avoid confidential, embargoed, unpublished, or restricted papers unless external delivery is explicitly disabled or corrected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/j-feng12/skills/academic-presentation)
- [Publisher Profile](https://clawhub.ai/user/j-feng12)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Anygen](https://www.anygen.io)
- [Gamma](https://gamma.app)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown guidance with file outputs including DOCX, PPTX, and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated artifacts under /tmp/academic-ppt/ and may send them through the configured WeChat channel.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact files list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
