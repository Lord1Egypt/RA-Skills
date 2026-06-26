## Description: <br>
Search for and discover OpenClaw skills from ClawHub, the official skill registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrJordanDu](https://clawhub.ai/user/MrJordanDu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to search ClawHub for relevant skills, compare search results, and prepare explicit install commands when they want to extend an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes broader install, update, publish, sync, and memory-history guidance beyond basic search. <br>
Mitigation: Ask the user to approve each install, update, publish, or sync command before execution. <br>
Risk: Publishing or syncing can upload local skill files to ClawHub. <br>
Mitigation: Avoid publish or sync commands unless the user has reviewed exactly which local files would be uploaded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrJordanDu/find-skills-for-clawhub) <br>
- [ClawHub](https://clawhub.ai) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>
- [ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with summarized search results and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the ClawHub CLI or npx to search, install, update, publish, or sync skills after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
