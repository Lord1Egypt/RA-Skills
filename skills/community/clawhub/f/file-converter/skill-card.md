## Description: <br>
File format converter. Detect formats, convert between JSON/YAML/XML/CSV/Markdown, minify and prettify code. Commands: detect, json2yaml, yaml2json, csv2md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to ask an agent for local file-format conversion commands and guidance for inspecting, transforming, minifying, or prettifying structured text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The utility can read local files and print converted content, file statistics, or hex dumps into the agent session. <br>
Mitigation: Run it only on files you are comfortable displaying in the session, and review converted output before sharing it elsewhere. <br>
Risk: The artifact contains documentation drift across the manifest, SKILL.md, and scripts, so the available commands are broader than the short manifest implies. <br>
Mitigation: Use the command help and inspect the script command list before relying on a specific conversion path. <br>


## Reference(s): <br>
- [File Converter on ClawHub](https://clawhub.ai/ckchzh/file-converter) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>
- [Publisher Profile](https://clawhub.ai/user/ckchzh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output may be plain text, JSON, CSV, XML, HTML, SQL, or Markdown depending on the command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and may print converted file contents or file statistics into the agent session.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
