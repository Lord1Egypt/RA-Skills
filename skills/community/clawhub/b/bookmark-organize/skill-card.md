## Description: <br>
Organizes Chrome bookmarks through OpenClaw with preview, explicit confirmation, apply, undo, and a local Chrome executor bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoshidefeng](https://clawhub.ai/user/xiaoshidefeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect live Chrome bookmarks, preview conservative cleanup actions, and apply or undo supported bookmark organization changes through a local bridge after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local bridge and Chrome extension can read and change Chrome bookmarks without authentication outside the promised confirmation flow. <br>
Mitigation: Install only if the publisher is trusted with bookmark access, keep the bridge running only while needed, avoid changing the bridge URL, export bookmarks first, and disable or remove the extension and bridge after use unless a future version adds authentication, sender checks, and enforced confirmation for mutations. <br>
Risk: Incorrect or unwanted organization plans could move or rename bookmarks. <br>
Mitigation: Review the preview before applying changes, require explicit confirmation, rely on bridge-verified apply results, and use the latest undo record after a successful apply when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoshidefeng/bookmark-organize) <br>
- [Chrome Executor Extension README](apps/chrome-executor-extension/README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured action plans and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans include summary, warnings, and supported bookmark actions; mutations require explicit confirmation and bridge verification.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and Chrome extension manifest; skill frontmatter/package.json list 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
