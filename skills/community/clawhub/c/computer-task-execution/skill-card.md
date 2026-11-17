## Description:

Execute real user tasks across websites and local applications with a reliability-first strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gift-is-coding](https://clawhub.ai/user/gift-is-coding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and task-execution agents use this skill to choose reliable, minimally intrusive paths for completing user-requested computer tasks across web apps and local applications. It emphasizes selecting verifiable execution surfaces, handling high-risk actions carefully, and reusing documented target-specific patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored patterns can introduce recipients, destinations, message text, or side effects that the current user did not explicitly request.

Mitigation: Review and clean stored patterns before installation; limit pattern memory to non-sensitive operational facts and require clear user control over retention and deletion.

Risk: A stored WeChat pattern can cause a real message to be sent to a hard-coded contact during a test.

Mitigation: Remove hard-coded contacts and test messages from stored patterns, and require explicit current-user confirmation before sending messages or performing other high-risk actions.

## Reference(s):

- [Pattern Memory](references/pattern-memory.md)
- [Site Patterns README](references/site-patterns/README.md)
- [Site Pattern Template](references/site-patterns/TEMPLATE.md)
- [Microsoft Excel Pattern](references/site-patterns/excel.md)
- [Feishu Pattern](references/site-patterns/feishu.md)
- [Microsoft Teams Pattern](references/site-patterns/microsoft-teams.md)
- [Feishu Web Pattern](references/site-patterns/my.feishu.cn.md)
- [Outlook Web Pattern](references/site-patterns/outlook.office.com.md)
- [Microsoft PowerPoint Pattern](references/site-patterns/powerpoint.md)
- [WeChat Pattern](references/site-patterns/wechat.md)

## Skill Output:

**Output Type(s):** [guidance, text, shell commands, configuration]

**Output Format:** [Markdown guidance with execution plans, command snippets, verification notes, and pattern-memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include target-specific action sequences and recommendations for browser, app, or scripted execution paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
