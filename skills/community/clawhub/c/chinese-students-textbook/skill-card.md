## Description: <br>
教科书目录读取。用户问「这学期要学哪些古诗词」「《朝花夕拾》在哪个单元」时，直接读取对应 JSON 文件回答。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makiwinster72](https://clawhub.ai/user/makiwinster72) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and learning assistants use this skill to answer questions about bundled Chinese middle-school textbook tables of contents, including units, required readings, poems, authors, and chapter topics. Maintainers can add new textbook directory JSON files after reviewing the supplied content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The add-new-book workflow writes local textbook data and could overwrite or place files incorrectly if unchecked user text controls names or paths. <br>
Mitigation: Confirm the book name, keep writes limited to the skill's textbooks folder, and review before overwriting existing files. <br>
Risk: Answers are only as current and accurate as the bundled textbook JSON files. <br>
Mitigation: Use the skill for local directory lookup and verify important curriculum decisions against the official textbook or school materials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/makiwinster72/chinese-students-textbook) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration] <br>
**Output Format:** [Markdown or plain text answers derived from local JSON textbook目录 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local textbook JSON file when the user asks to add a new book.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
