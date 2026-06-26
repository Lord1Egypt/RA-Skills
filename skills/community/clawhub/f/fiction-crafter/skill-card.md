## Description: <br>
fiction-crafter helps agents turn Chinese webnovel ideas into expanded prompts, outlines, chapter drafts, continuity notes, reviews, and optional story diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[followaf](https://clawhub.ai/user/followaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative-writing agents use this skill to plan and draft serialized Chinese webnovel chapters while tracking characters, locations, plot points, world rules, and generation issues across a local project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional initialization command with --clean can remove prior generated chapter markdown and reset stored story notes. <br>
Mitigation: Run the skill in a dedicated novel project folder and use --clean only after confirming earlier drafts and .learnings/ notes no longer need to be preserved. <br>


## Reference(s): <br>
- [fiction-crafter ClawHub page](https://clawhub.ai/followaf/fiction-crafter) <br>
- [Original novel-generator ClawHub page](https://clawhub.ai/ityhg/novel-generator) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [Prompt guide](references/prompt-guide.md) <br>
- [Plot structures](references/plot-structures.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, prose guidance, Mermaid diagrams, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local output/ chapter files and .learnings/ continuity notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
