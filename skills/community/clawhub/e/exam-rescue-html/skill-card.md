## Description:

Generates a printable three-section exam rescue checklist HTML from knowledge_map.json, covering core formulas, high-frequency points, and common mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoucha833-lang](https://clawhub.ai/user/zhoucha833-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and exam-preparation agents use this skill to turn an existing exam knowledge map into a compact printable review sheet before a test. It is designed for Chinese-language study workflows that need formula, hotspot, and mistake cards generated into HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suppresses confirmations and errors during generation.

Mitigation: Review the generated HTML and rescue notes before relying on them, especially when the input knowledge map may be incomplete or malformed.

Risk: The generated HTML may include unescaped study content.

Mitigation: Use trusted knowledge_map.json content or ensure fields are escaped before opening or sharing the generated HTML.

Risk: Opening the generated HTML can load and execute JavaScript from unpkg.com.

Mitigation: Open the file only in environments where CDN access and client-side KaTeX rendering are acceptable.

Risk: The workflow writes and may overwrite files in the workspace.

Mitigation: Run the skill in a workspace where exam-rescue-YYYYMMDD.html and .exam-session/rescue_notes.json writes are expected.

## Reference(s):

- [Content Rules](references/content-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/zhoucha833-lang/skills/exam-rescue-html)
- [Publisher Profile](https://clawhub.ai/user/zhoucha833-lang)

## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [JSON study notes plus generated HTML file and a concise completion message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .exam-session/rescue_notes.json when possible and creates exam-rescue-YYYYMMDD.html in the workspace root.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
