## Description:

Routes multi-image generation work through ChatGPT, built-in image generation, manual handoff, or local rendering while preserving resumable state, stable filenames, strict readable-text boundaries, import checks, and visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to prepare, route, resume, import, and QA batches of generated images when direct ImageGen is unavailable, unreliable, or needs a controlled ChatGPT/manual fallback. It is especially useful when readable text, filenames, metrics, hashes, or other factual details must be constrained and checked before downstream publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed prompts or approved reference images may be sent to ChatGPT through an authenticated browser session.

Mitigation: Request action-time confirmation for the destination, exact prompt files, reference files, and purpose before any submission or upload.

Risk: Runtime handoff directories may contain local paths, working files, prompts, and imported image evidence.

Mitigation: Keep handoff directories out of public commits and review file lists before transmission or publication.

Risk: Generated images can invent readable text such as filenames, metrics, hashes, timestamps, or labels.

Mitigation: Use the skill's allowlist text policy, forbidden pattern tracking, local import records, and required visual/text QA before marking images as passed.

Risk: Returned ZIP archives are inbound content and may contain unsafe paths, extra files, or incomplete image sets.

Mitigation: Import archives through the bundled batch importer, preserve the original archive, reject unsafe entries, and treat qa-report.json as evidence rather than approval.

Risk: Browser automation may encounter login, verification, CAPTCHA, quota, billing, or unexpected destination states.

Mitigation: Stop and hand control to the user for account or quota gates, and keep account/session details out of public artifacts.

## Reference(s):

- [UI Recovery Rules](references/ui-recovery.md)
- [Optional ChatGPT ZIP batches](references/zip-batch.md)
- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/chatgpt-image-handoff)
- [Source homepage](https://github.com/yangchao228/my_open_skills/tree/main/skills/content/chatgpt-image-handoff)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, JSON state files, shell commands, configuration snippets, and local image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces resumable handoff directories, prompt packs, jobs.json state, import records, contact sheets, and QA status; final image approval remains human-confirmed.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
