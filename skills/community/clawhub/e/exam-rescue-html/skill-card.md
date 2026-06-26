## Description: <br>
Generates a printable three-section exam rescue checklist HTML from knowledge_map.json, covering core formulas, high-frequency points, and common mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoucha833-lang](https://clawhub.ai/user/zhoucha833-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and exam-prep users use this skill after exam-question-generator analysis to turn a knowledge map into a concise last-minute review checklist. It creates formula, hotspot, and mistake cards as printable HTML plus brief completion guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically writes local output files and may overwrite prior generated review material. <br>
Mitigation: Install and run it only in the intended exam workspace, and preserve any generated HTML that should not be replaced before regenerating. <br>
Risk: Generated study guidance can be incomplete or misleading if the source knowledge map or retrieved notes are weak. <br>
Mitigation: Review the generated HTML before relying on it for exam preparation. <br>
Risk: Opening the generated HTML may contact unpkg.com to load KaTeX for math rendering. <br>
Mitigation: Use the generated HTML only in environments where loading the KaTeX CDN is acceptable, or review the template before opening it. <br>


## Reference(s): <br>
- [Content Rules](references/content-rules.md) <br>
- [HTML Template](assets/template.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhoucha833-lang/exam-rescue-html) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [HTML file, JSON notes record, and short text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes exam-rescue-YYYYMMDD.html in the workspace root and records rescue_notes.json when possible.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
