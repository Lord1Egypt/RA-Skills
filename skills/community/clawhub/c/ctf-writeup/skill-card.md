## Description: <br>
Generates a single standardized submission-style CTF writeup for competition handoff and organizer review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gandli](https://clawhub.ai/user/gandli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, CTF competitors, and security teams use this skill after solving a challenge to produce a concise, reproducible submission writeup with metadata, solution steps, scripts, and the final flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated writeups may include real flags, file paths, command output, screenshots, or other challenge artifacts. <br>
Mitigation: Review the writeup before sharing and redact sensitive details when the competition or team policy requires it. <br>
Risk: Workspace searches can surface files outside the intended challenge materials when run from a broad directory. <br>
Mitigation: Run the skill from the specific challenge directory and inspect included artifacts before publishing the writeup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gandli/ctf-writeup) <br>
- [Publisher profile](https://clawhub.ai/user/gandli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with YAML frontmatter and fenced code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a submission-style writeup file such as writeup.md or writeup-<challenge-name>.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
