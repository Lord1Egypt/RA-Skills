## Description: <br>
Create, inspect, and edit Microsoft PowerPoint presentations and PPTX decks with reliable layouts, templates, placeholders, notes, charts, and visual QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and presentation authors use this skill to inspect, create, and modify PowerPoint decks while preserving template fidelity, placeholders, charts, speaker notes, comments, and visual quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerPoint edits can place content in the wrong placeholder, layer, notes area, or chart when the deck structure is assumed instead of inspected. <br>
Mitigation: Inventory layouts, placeholders, notes, comments, media, and chart structures before making edits, then verify affected slides after each change. <br>
Risk: A deck can pass text inspection while still containing visual defects such as overflow, clipping, weak contrast, leftover template content, or inconsistent themes. <br>
Mitigation: Run separate content and visual QA, including rendered-slide or thumbnail inspection, before delivering the final deck. <br>
Risk: The skill may cause an agent to read or modify user-provided PPTX files even though the package itself has no scripts or hidden high-privilege behavior. <br>
Mitigation: Use it only on intended presentation files and review proposed file changes before accepting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/chen-powerpoint-pptx) <br>
- [Skill homepage](https://clawic.com/skills/powerpoint-pptx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional code, shell commands, and file-editing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to read, inspect, render, or modify user-provided PPTX files; the package itself is documentation-only and declares no required binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved ClawHub release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
