## Description: <br>
Ai Interview provides paired AI job-seeker and recruiter agents for Feishu group-chat interviews with an optional local web viewer for observing conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeeban-G](https://clawhub.ai/user/jeeban-G) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or hiring teams use this skill to configure a two-agent simulated interview workflow in Feishu, with one agent acting as a frontend candidate and another as an interviewer. It also supports local observation through a web viewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local viewer can expose OpenClaw session history and interview content. <br>
Mitigation: Run the viewer only on a trusted machine, bind or firewall port 8091 to localhost, stop it when not in use, and obtain consent before observing interview content. <br>
Risk: Viewer actions can delete OpenClaw session history. <br>
Mitigation: Back up OpenClaw session logs before using any clear-history function. <br>
Risk: Feishu App Secrets and interview transcripts are sensitive. <br>
Mitigation: Use dedicated low-privilege Feishu apps and keep App Secrets out of source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeeban-G/ai-interview-system) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Job-seeker identity template](artifact/config/job-seeker/IDENTITY.md) <br>
- [Recruiter identity template](artifact/config/recruiter/IDENTITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and a MoonShot API key; includes an optional localhost web viewer for conversation observation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
