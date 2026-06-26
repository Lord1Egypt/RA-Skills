## Description: <br>
Use this skill when the user says "daydream", "start daydreaming", "force a daydream", "run daydream cycles", or when a scheduled daydream is triggered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhuckobey](https://clawhub.ai/user/jhuckobey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Daydreamer to maintain a local memory log and run scheduled or manual associative brainstorming sessions. The skill traverses saved memories and optional web search results to produce ideas, observations, recommendations, questions, warnings, or other synthesized guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist summaries of prior work and reuse them later, including content derived from session logs. <br>
Mitigation: Skip or closely supervise starter-memory seeding, review Daydreams.MD and ideas/*.md for sensitive content, and remove entries that should not persist. <br>
Risk: Memory and idea files are written into the selected workspace and could mix unrelated projects or sensitive context. <br>
Mitigation: Set DAYDREAM_WORKSPACE to a dedicated folder before use and keep that folder separate from unrelated repositories. <br>
Risk: Scheduled daydream sessions may run automatically after setup. <br>
Mitigation: Choose manual scheduling if automated sessions are not desired. <br>


## Reference(s): <br>
- [Daydreamer ClawHub page](https://clawhub.ai/jhuckobey/daydreamer) <br>
- [Publisher profile: jhuckobey](https://clawhub.ai/user/jhuckobey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with inline shell commands and JSON-backed local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory, configuration, session, log, and idea files in the selected workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
