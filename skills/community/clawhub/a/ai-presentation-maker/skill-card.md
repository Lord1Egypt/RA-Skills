## Description: <br>
AI Presentation Maker guides an agent through an interview-driven workflow to generate factual presentation decks with speaker notes, validation checks, and Markdown, HTML, Gamma, PPTX, or PDF export paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffjhunter](https://clawhub.ai/user/jeffjhunter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, consultants, speakers, and business users use this skill to turn real project details into presentation decks for pitches, talks, demos, and audience-specific briefings. It emphasizes interview-sourced facts, speaker notes, and validation prompts to reduce speculative or unsupported claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation content may include sensitive business details stored in local deck and metadata files. <br>
Mitigation: Use the skill only where local storage under ~/workspace/presentations is acceptable, and review generated files before sharing or archiving them. <br>
Risk: HTML exports may preserve untrusted HTML-like slide content and may contact Google Fonts. <br>
Mitigation: Review HTML output before presenting or publishing it, and modify the exporter for offline or sensitive environments. <br>
Risk: Speaker profile prefill from SOUL.md or AGENTS.md can carry personal or organizational details into a deck. <br>
Mitigation: Confirm any prefilled speaker information before generating or exporting presentations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffjhunter/ai-presentation-maker) <br>
- [Publisher homepage](https://jeffjhunter.com) <br>
- [HTML slide exporter](references/export-html-slides.py) <br>
- [PPTX exporter](references/export-pptx.py) <br>
- [Gamma export script](references/export-gamma.sh) <br>
- [Slide templates](references/slide-templates.py) <br>
- [Gamma.app](https://gamma.app) <br>
- [AI Persona Method](https://aipersonamethod.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown decks, JSON metadata, HTML slide files, optional PPTX/PDF exports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local presentation files under ~/workspace/presentations; PPTX export requires python3 and python-pptx, and PDF export requires pandoc or HTML print.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
