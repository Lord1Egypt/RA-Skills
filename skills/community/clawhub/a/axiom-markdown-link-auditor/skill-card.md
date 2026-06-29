## Description: <br>
Markdown link auditor that finds broken internal links, optionally checks external links with HEAD requests, and reports link audit results for documentation maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to audit Markdown files before publishing, gate CI on broken links, and identify orphaned documentation pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote link checks contact third-party URLs from the user's environment. <br>
Mitigation: Leave remote checking disabled for private repositories or sensitive drafts unless outbound requests to those external links are acceptable. <br>
Risk: The auditor reads the Markdown files supplied by the user. <br>
Mitigation: Run it only on documentation paths intended for audit and avoid pointing it at unrelated sensitive files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/axiom-markdown-link-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python examples; the bundled auditor can emit text or JSON reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional remote URL checking sends HEAD requests to external sites; JSON output is available for CI integration.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
