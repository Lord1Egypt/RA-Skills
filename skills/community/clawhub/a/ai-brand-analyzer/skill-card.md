## Description: <br>
AI Brand Analyzer uses Gemini Flash with Google Search grounding to generate reusable brand identity profiles as JSON for ad generation and creative workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative workflow operators use this skill to research a brand and produce or update a structured brand identity JSON profile for ad generation, Ad-Ready, Morpheus, or custom creative pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand analysis prompts and researched brand context are sent to Google/Gemini. <br>
Mitigation: Use the skill only when that data handling is acceptable, and provide the Gemini API key deliberately through the environment or command option. <br>
Risk: The --output and --auto-save options can create or overwrite JSON files where the agent has write permission. <br>
Mitigation: Prefer stdout for review first, or choose an explicit output path and review the generated JSON before reuse in downstream creative workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, json, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON brand identity profile, with optional Markdown-facing shell command guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key. Output may be written to stdout, a user-specified JSON path, or the configured Ad-Ready brands catalog when auto-save is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
