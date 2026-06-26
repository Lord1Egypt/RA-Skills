## Description: <br>
Helps agents plan and write Chinese-language long-form novels using the Snowflake Method and a three-layer memory workflow, with prompt templates and Node.js scripts for manuscript state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waitli](https://clawhub.ai/user/waitli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and writing-focused agents use this skill to structure a novel from seed concept through character, world, plot, chapter outline, draft generation, and continuity updates. It is intended for Chinese-language fiction workflows that need persistent local manuscript state across many chapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill initializes and updates local manuscript state on disk. <br>
Mitigation: Use a dedicated project directory and confirm the exact path before initialization or resume. <br>
Risk: Long-form generation can continue across multiple chapters and save outputs after each chapter. <br>
Mitigation: Require chapter-by-chapter confirmation when the user does not want automatic multi-chapter writing and saving. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/waitli/dream-novel-skill) <br>
- [Architecture Prompt Templates](artifact/resources/architecture.md) <br>
- [Chapter Blueprint Template](artifact/resources/chapter.md) <br>
- [Utility Prompt Templates](artifact/resources/utility.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose, JSON state updates, local manuscript files, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local novel project files, including chapter markdown and JSON memory databases.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
