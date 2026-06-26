## Description: <br>
Client for a local or private Claw Skill Nest service that lets agents list, upload, install, and update skills, including Xiahua alias triggers; it is not for clawhub.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklldog](https://clawhub.ai/user/kklldog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage skills in a local or private Claw Skill Nest by listing available skills, uploading skill archives, and installing or updating skills into an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update active agent skills with limited safeguards. <br>
Mitigation: Use it only with a Skill Nest service you operate or strongly trust, and inspect downloaded skill packages before installing or updating them. <br>
Risk: The security evidence reports an unsafe Windows extraction path. <br>
Mitigation: Avoid installing untrusted ZIP packages on Windows; inspect archives and filenames before extraction or use a hardened extraction workflow. <br>
Risk: Skill Nest credentials or endpoints could be exposed through prompts, logs, or defaults. <br>
Mitigation: Set an explicit local or private SKILLHUB_URL, use a unique scoped API key, and avoid exposing the key in prompts or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kklldog/claw-skill-nest-client) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline command examples and script-backed terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SKILLHUB_URL and SKILLHUB_API_KEY to target a trusted local or private Skill Nest service.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
