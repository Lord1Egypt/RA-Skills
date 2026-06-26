## Description: <br>
Converts PPT, PPTX, and PDF presentation files into per-slide images and narration data for prepared presentation playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianglingling007](https://clawhub.ai/user/jianglingling007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Presentation creators and agent users use this skill to prepare PPT, PPTX, or PDF files for narration workflows. It extracts slide images and text, preserves speaker notes when present, and guides the agent to generate page-by-page scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency setup may request system package installation with sudo on some platforms. <br>
Mitigation: Review setup.sh before installation and prefer a virtual environment or sandbox when possible. <br>
Risk: Presentation text, speaker notes, and generated narration are saved locally in presentations/<name>/presentation.json. <br>
Mitigation: Avoid processing untrusted or highly sensitive decks unless local extraction and storage of that content is acceptable. <br>


## Reference(s): <br>
- [Claw Presenter release page](https://clawhub.ai/jianglingling007/claw-presenter) <br>
- [LibreOffice download](https://www.libreoffice.org/download/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Presentation output directory with PNG slide images and a presentation.json file containing slide metadata, extracted text, notes, and narration scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to presentations/<name>/ by default and may reuse speaker notes as initial narration scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
