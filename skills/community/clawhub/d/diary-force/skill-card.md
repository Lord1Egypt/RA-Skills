## Description: <br>
Diary Force prompts daily journaling, structures diary input, applies thinking-model analysis, and can internalize entries into a local memory workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YHlorra](https://clawhub.ai/user/YHlorra) <br>

### License/Terms of Use: <br>
原创技能，可商用 <br>


## Use Case: <br>
External users and developers use this skill to maintain a daily journaling habit, turn personal reflections into structured Markdown, and optionally analyze entries with thinking models before saving them to a memory repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal diary entries, memory files, or AI-generated reflections may be committed and pushed automatically through Git. <br>
Mitigation: Use only a private intended repository, verify repository remotes before use, and disable or gate Git push behavior unless automatic upload is desired. <br>
Risk: Hard-coded diary and memory paths may point to unintended local locations. <br>
Mitigation: Review and change the diary and memory paths before running the scripts. <br>
Risk: Scheduled cron execution may prompt, analyze, save, or upload diary content without a fresh per-entry confirmation. <br>
Mitigation: Disable cron or require explicit confirmation before writing files, calling the model, or pushing changes. <br>
Risk: Sensitive personal, medical, financial, or work content may be sent to the configured model or stored in a repository. <br>
Mitigation: Avoid highly sensitive content unless model privacy behavior and repository visibility have been verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YHlorra/diary-force) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Evaluation prompts](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diary entries, thinking-model analysis, and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write diary and memory files locally and may trigger Git commit and push behavior when configured.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
