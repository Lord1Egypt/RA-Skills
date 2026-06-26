## Description: <br>
Submits Chinese gaokao essay prompts and student essays to InkCraft for automated correction, then returns structured feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diyanqi](https://clawhub.ai/user/diyanqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, teachers, and writing-support agents use this skill to submit a gaokao-style Chinese essay prompt and essay body to InkCraft and receive a status, score-oriented feedback, strengths, improvement areas, rewrite suggestions, and a detail link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Essay prompts, essay bodies, and optional reference text are sent to InkCraft for correction. <br>
Mitigation: Install only if you trust InkCraft for this data, and avoid submitting sensitive personal information unless that sharing is acceptable. <br>
Risk: The skill requires an InkCraft API key for API calls. <br>
Mitigation: Use a revocable API key and do not expose it in prompts, logs, or shared output. <br>
Risk: INKCRAFT_BASE_URL can redirect requests away from the official service. <br>
Mitigation: Keep INKCRAFT_BASE_URL set to https://www.inkcraft.cn unless you intentionally trust another endpoint. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/diyanqi/composition-correction) <br>
- [InkCraft homepage](https://www.inkcraft.cn) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>
- [OpenClaw configuration example](artifact/openclaw.skills-config.example.json5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured correction feedback and optional curl commands for API submission and polling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and INKCRAFT_API_KEY; may use INKCRAFT_BASE_URL; returns correction status, summary, scoring dimensions when available, highlights, improvement points, rewrite suggestions, and an InkCraft detail link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
