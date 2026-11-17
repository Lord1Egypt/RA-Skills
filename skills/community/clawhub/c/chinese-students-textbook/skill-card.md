## Description:

教科书目录读取：根据本地 JSON 课本目录回答古诗词、单元、篇目、作者和必读内容等查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[makiwinster72](https://clawhub.ai/user/makiwinster72)

### License/Terms of Use:

MIT-0

## Use Case:

Students, parents, educators, and agents use this skill to answer questions about bundled Chinese middle-school textbook catalogs, including units, readings, poems, authors, and required reading. The skill can also help structure newly provided textbook catalogs as JSON files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The new-book workflow may add or update local textbook JSON files from user-provided book names.

Mitigation: Require explicit user confirmation before writing files, sanitize book names, reject path separators, `..`, and absolute paths, and avoid overwriting existing files unless the user confirms the exact target.

Risk: Malformed bundled JSON can prevent reliable textbook lookup or cause incomplete answers.

Mitigation: Validate all textbook JSON files before release or deployment and repair invalid entries before relying on those books for answers.

Risk: Bundled catalog coverage is limited to the included textbook files and may not match every school, edition, or future curriculum update.

Mitigation: Tell users which textbook file was used and recommend checking against the relevant official or school-provided textbook when accuracy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/makiwinster72/skills/chinese-students-textbook)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text answers, with JSON textbook data when adding new books]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled local textbook JSON files; new-book additions may create or update JSON data files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
