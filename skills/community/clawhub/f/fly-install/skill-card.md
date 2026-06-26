## Description: <br>
Installs ClawHub skills through fallback methods when the ClawHub CLI is rate-limited or unavailable, including GitHub clone, ClawHub ZIP download, and manual guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shensiglea-collab](https://clawhub.ai/user/shensiglea-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install ClawHub skills when the normal CLI install path is blocked by rate limits or failures. It provides automated fallback installation attempts plus manual installation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install unverified third-party skills into the agent skills directory. <br>
Mitigation: Use it only when the exact skill source is already trusted, verify the GitHub owner/repo or ClawHub download page, and review the installed SKILL.md before agent use. <br>
Risk: Batch installs, path-like skill names, or broad custom install directories can expand the impact of a mistaken or malicious install. <br>
Mitigation: Avoid batch installs for untrusted sources, avoid path-like skill names, and use a narrow, expected skills directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shensiglea-collab/fly-install) <br>
- [Publisher profile](https://clawhub.ai/user/shensiglea-collab) <br>
- [GitHub repository listed in README](https://github.com/shensiglea-collab/fly-install) <br>
- [ClawHub skills directory](https://clawhub.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose network downloads, repository clones, ZIP extraction, and local skill-directory changes.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
