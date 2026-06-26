## Description: <br>
Automates an academic presentation workflow by turning a paper PDF or pasted text into a Chinese translation, structured summary, slide deck, speech notes, and WeChat-delivered files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-feng12](https://clawhub.ai/user/j-feng12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, and academic presenters use this skill to convert a paper into editable translation and summary documents, a 10-15 slide presentation, and matching speaking notes. It is intended for normal document-preparation workflows where the user is comfortable sending paper-derived content to the selected PPT provider and through WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper content and generated materials may be sent to external PPT services and WeChat. <br>
Mitigation: Use skip-PPT or local-only handling for confidential, unpublished, or restricted documents, and verify provider, recipient, and API-key settings before sending. <br>
Risk: The privacy claim in the artifact conflicts with behavior that can transmit paper-derived files outside the local environment. <br>
Mitigation: Review the workflow and obtain explicit user consent before uploading paper-derived content or automatically sending generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j-feng12/academic-presentation) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Anygen](https://www.anygen.io) <br>
- [Gamma](https://gamma.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Word documents, PowerPoint files, Markdown speech notes, status text, and provider command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written under /tmp/academic-ppt/ and may be sent through WeChat after completion.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact files report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
