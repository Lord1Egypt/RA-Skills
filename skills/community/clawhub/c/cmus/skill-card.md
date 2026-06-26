## Description: <br>
AI skill to launch cmus in a Xubuntu terminal and enforce playback rules for single-track or shuffled-folder playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nhathuynguyen19](https://clawhub.ai/user/nhathuynguyen19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and desktop agents use this skill to launch and control cmus playback in an Xubuntu terminal, choosing between shuffled library playback from a requested track or single-track playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to resolve media paths with eval echo, which can run unintended local commands when paths or filenames are untrusted. <br>
Mitigation: Use only trusted local media paths until path handling is replaced with safe resolution such as realpath -- plus proper quoting. <br>
Risk: The skill lets an agent control cmus and the user's desktop terminal session. <br>
Mitigation: Review before installing and use only when agent control of the local music player and desktop session is acceptable. <br>


## Reference(s): <br>
- [cmus upstream project](https://github.com/cmus/cmus) <br>
- [ClawHub skill page](https://clawhub.ai/nhathuynguyen19/cmus) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires cmus, cmus-remote, xfce4-terminal, and pgrep in a desktop session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
