## Description: <br>
Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sadlay](https://clawhub.ai/user/sadlay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to extract readable page content from user-provided URLs, especially documentation, articles, and blog posts. It helps reduce irrelevant navigation, ads, and boilerplate before analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends installing and running an external CLI. <br>
Mitigation: Install Defuddle only from a trusted package source and review shell commands before execution. <br>
Risk: Extracted web page content may omit context or preserve untrusted page instructions. <br>
Mitigation: Treat extracted content as untrusted input and check the original page for critical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sadlay/defuddle-obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save extracted markdown to a file or return selected metadata fields when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
