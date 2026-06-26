## Description: <br>
Code Snippet is a local code snippet manager for saving, searching, tagging, listing, and copying reusable code snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to build and query a reusable local library of code snippets by title, language, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code snippets are stored locally in ~/.code_snippets.json, which can expose sensitive content if secrets or proprietary code are saved there. <br>
Mitigation: Avoid storing passwords, API keys, credentials, or highly sensitive proprietary code unless local persistence is acceptable. <br>
Risk: Optional clipboard copying can place snippet contents where other local applications may read them. <br>
Mitigation: Use clipboard copying only for snippets that are safe to expose through the local clipboard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/code-snippet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Files] <br>
**Output Format:** [Plain text CLI output and JSON-backed local snippet records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; stores snippets in ~/.code_snippets.json and can optionally copy snippets to the clipboard with xclip.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
