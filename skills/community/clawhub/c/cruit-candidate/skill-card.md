## Description: <br>
Create and maintain a Cruit candidate profile for an AI-native developer, including join, publish, refresh, and weekly update workflows for recruiter discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
Developers use this skill in a coding agent to create, publish, and refresh a recruiter-searchable Cruit profile from approved project metadata, optional resume facts, and user-provided work preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch live instructions from Cruit on each run, so reviewed behavior may change after installation. <br>
Mitigation: Review before installing, prefer a pinned or marketplace-reviewed update path when available, and enforce the documented rule that only the configured Cruit instruction URL may be fetched. <br>
Risk: The workflow stores a local access token and sends approved resume or project profile facts to Cruit's servers. <br>
Mitigation: Use only approved folders and approved profile drafts, avoid publishing secrets or private contact details, and remove ~/.cruit/credentials.json to clear the saved session. <br>


## Reference(s): <br>
- [Cruit Candidate ClawHub Page](https://clawhub.ai/nwang783/cruit-candidate) <br>
- [Cruit Candidate Instructions](https://cruit.dev/skills/candidate/INSTRUCTIONS.md) <br>
- [Cruit Website](https://cruit.dev) <br>
- [Security Notes](SECURITY.md) <br>
- [Example Candidate Flow](examples/candidate-profile-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational Markdown with structured profile drafts, setup prompts, and occasional JSON-shaped API payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contacts https://cruit.dev, stores local credentials under ~/.cruit/, and requires user approval before publishing unless automatic refresh is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
