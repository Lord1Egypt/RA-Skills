## Description: <br>
内容蒸馏器 helps agents distill reusable methodologies from ebooks, links, videos, articles, and pasted text, then package them as structured WorkBuddy skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn long-form content, media, links, or pasted text into reusable methodology skills. It supports knowledge-base and action-guide skill packages with references, examples, boundaries, and limitation analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent skill files in the user's WorkBuddy skills directory. <br>
Mitigation: Review generated skill directories before allowing them to persist or before invoking them. <br>
Risk: PDF and EPUB helper scripts may silently install Python packages. <br>
Mitigation: Preinstall required dependencies in a controlled environment or remove the automatic pip installation behavior before processing ebooks. <br>
Risk: The workflow may fetch or use external discussion content while collecting objections and limitations. <br>
Mitigation: Use trusted sources, avoid sensitive private content, and review fetched material before incorporating it into generated skills. <br>


## Reference(s): <br>
- [蒸馏框架](references/蒸馏框架.md) <br>
- [方法论索引](references/方法论索引.md) <br>
- [ClawHub skill listing](https://clawhub.ai/guipi888/content-distiller) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, generated skill files, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate persistent WorkBuddy skill directories and optional helper scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
