## Description:

Generates CBETA-based academic citations and footnotes for Chinese Buddhist canon references, including publisher, place, year, volume, page, column, and line details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gouchunlei2-png](https://clawhub.ai/user/gouchunlei2-png)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, editors, and writers working with Chinese Buddhist texts use this skill to turn known CBETA locations or quoted passages into citation-ready footnotes and bibliographic entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Zhonghua Dazangjing locator can use a full browser session cookie and may read it from a plaintext fo_cookie.txt file in the skill directory.

Mitigation: Use FO_COOKIE only in the current shell session, do not store fo_cookie.txt in the skill directory, and avoid sharing or committing the folder after placing any cookie there.

Risk: The main citation scripts make network requests and can write citation text to the clipboard when requested.

Mitigation: Review commands before execution and avoid clipboard-copy options in shared or sensitive clipboard environments.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gouchunlei2-png/skills/dazangjing-xueshu-yinyong)
- [CBETA citation copy format](https://cbeta.org/citation-copy-format)
- [CBETA Online](https://cbetaonline.dila.edu.tw)
- [CBETA collection notation](https://cbeta.org/collection-notation)
- [CBETA archive data format reference](https://archive.cbeta.org/data-format/zrx.htm)
- [CBData stable API works endpoint](https://cbdata.dila.edu.tw/stable/works)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with citation lines and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is Simplified Chinese; normal citation results are two lines unless expanded formats are requested.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
