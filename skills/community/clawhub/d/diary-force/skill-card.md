## Description:

Diary Force helps agents prompt daily journaling, structure diary entries, run thinking-model analysis, and sync entries into local memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhlorra](https://clawhub.ai/user/yhlorra)

### License/Terms of Use:

原创技能，可商用

## Use Case:

External users and AI-native developers use Diary Force to keep a daily journal, convert free-form reflections into structured Markdown entries, and optionally analyze entries with thinking models before syncing them into a local memory system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive diary content may be written to local diary and memory paths, committed into Git history, and pushed to the configured remote.

Mitigation: Configure paths before use, restrict repository contents, review generated entries, and require confirmation before any commit or push.

Risk: Broad Git staging can include unrelated local files from the memory vault parent directory.

Mitigation: Replace broad staging with explicit file paths and inspect Git status before committing.

Risk: Thinking-model analysis can send diary text to an external OpenCode-backed model.

Mitigation: Avoid submitting sensitive entries unless the model provider is approved; redact private content or disable external analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhlorra/skills/diary-force)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diary content, plain-text prompts, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local diary and memory files and trigger Git commands when its scripts are run.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
