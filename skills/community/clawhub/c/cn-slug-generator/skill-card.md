## Description: <br>
Converts Chinese titles into SEO-friendly URL slugs using dictionary-based English conversion or optional pinyin conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and SEO practitioners use this skill to turn Chinese article titles, documentation headings, and filenames into URL-safe slugs for publishing workflows. It can produce one slug at a time or process multiple titles in batch mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using --output can create or overwrite a local file at the requested path. <br>
Mitigation: Use --output only with paths the user intends to create or replace. <br>
Risk: Pinyin conversion may not work as expected unless the optional pypinyin dependency is installed. <br>
Mitigation: Install pypinyin before relying on --pinyin mode, or use the default dictionary-based conversion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-slug-generator) <br>
- [AISoBrand](https://aisobrand.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text slug output with Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write slug output to a user-specified local file when --output is used. Pinyin mode may require the optional pypinyin dependency.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
