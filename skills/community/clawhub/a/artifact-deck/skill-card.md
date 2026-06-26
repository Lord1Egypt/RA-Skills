## Description: <br>
Public OpenClaw skill for generating reproducible PPTX decks from project notes, status bullets, and screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
Developers, project leads, and release teams use Artifact Deck to turn curated project notes, status bullets, release summaries, audit outputs, and screenshots into a reproducible stakeholder-ready PPTX deck plus a share-safe markdown summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local notes and screenshots selected by the user, so sensitive content can be included in generated deck artifacts. <br>
Mitigation: Provide curated inputs only and review the PPTX, manifest, build JSON, and summary before sharing. <br>
Risk: Deck generation writes files to user-specified output paths. <br>
Mitigation: Write outputs inside a known workspace folder and inspect the generated paths before distributing artifacts. <br>
Risk: The workflow depends on local Python scripts and python-pptx. <br>
Mitigation: Run it in a trusted Python environment and install dependencies from trusted sources. <br>


## Reference(s): <br>
- [Artifact Deck ClawHub Page](https://clawhub.ai/zack-dev-cm/artifact-deck) <br>
- [Artifact Deck Homepage](https://github.com/zack-dev-cm/artifact-deck) <br>
- [Publisher Profile](https://clawhub.ai/user/zack-dev-cm) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Configuration] <br>
**Output Format:** [PPTX deck file, JSON manifest and build reports, markdown summary, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.9+ and python-pptx; reads user-selected local notes and screenshots and writes outputs to user-specified paths.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
