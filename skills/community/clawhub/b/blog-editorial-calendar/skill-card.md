## Description: <br>
Blog Editorial Calendar helps content teams manage an evidence-backed topic backlog, choose balanced blog topics, and schedule posts through their configured publishing workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content teams, founders, and developers use this skill to keep a blog backlog moving through topic selection, scheduling, status checks, and completion tracking. It is intended for recurring long-tail SEO publishing workflows that rely on configured CMS and writer skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create drafts or schedule posts in a connected CMS from broad prompts. <br>
Mitigation: Use it only with CMS accounts and sites where automated drafts or scheduled posts are acceptable, and confirm before running publishing commands such as `next`, `sync`, or `mark-done`. <br>
Risk: Concurrent `next` jobs may pick or schedule overlapping work because concurrency controls are under-specified. <br>
Mitigation: Run one publishing job at a time until a real lock or transaction mechanism is available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/automatelab/blog-editorial-calendar) <br>
- [Publisher Profile](https://clawhub.ai/user/automatelab) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger configured publishing workflows and update local backlog status files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
