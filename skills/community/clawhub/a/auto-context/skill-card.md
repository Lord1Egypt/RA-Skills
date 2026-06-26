## Description: <br>
Automatically reads relevant project context files before major actions so agents can operate with current situational awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-agent users use this skill to load TODOs, roadmaps, task plans, handoffs, findings, changelogs, and session notes before starting, resuming, planning, debugging, refactoring, or handing off work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically reads local planning, roadmap, handoff, and session documents that may contain secrets or unrelated confidential notes. <br>
Mitigation: Install it only in projects where that local context is appropriate for the agent to read, and keep credentials and confidential notes out of those files. <br>
Risk: Installing from an unpinned source can make the installed behavior harder to review and reproduce. <br>
Mitigation: Prefer the ClawHub install path or another reviewed, pinned source. <br>
Risk: Outdated project context can cause the agent to rely on stale plans or obsolete decisions. <br>
Mitigation: Use the skill's file-age checks and stale-context warnings before relying on loaded context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wpank/auto-context) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/wpank) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown context summary with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads bounded local project planning files and reports stale-context warnings when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
