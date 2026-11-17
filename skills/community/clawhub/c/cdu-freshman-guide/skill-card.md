## Description:

为成都大学新生提供选课、走读、住宿、医保、租房、就业等高频问题的一站式问答，并引导用户通过官方渠道核实重要信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[century0327](https://clawhub.ai/user/century0327)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially Chengdu University freshmen, use this skill to ask campus life and student-service questions and receive concise answers with source, timeliness, and cross-checking guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maintenance scripts can expose private chat-derived names or accidentally package local chat data if run on private exports.

Mitigation: Use the published curated campus guide for normal installation; review the release contents before running maintenance scripts on private data.

Risk: Campus guidance can become stale because parts of the knowledge base come from student group-chat experience and time-sensitive notices.

Mitigation: Treat answers as guidance, check the included source and timeliness notes, and verify important items through official Chengdu University channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/century0327/skills/cdu-freshman-guide)
- [Publisher documentation profile](https://github.com/Century0327)
- [成都大学官网](https://www.cdu.edu.cn)
- [成都大学教务处](https://jw.cdu.edu.cn/)
- [成都大学学生处](https://xsc.cdu.edu.cn/)
- [成都大学本科招生网](https://zhaosheng.cdu.edu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style campus Q&A answers with source links, timeliness notes, cross-check suggestions, and safety refusals.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use optional curated KB JSON entries and current web search results; prompts users to verify time-sensitive items against official channels.]

## Skill Version(s):

1.4.1 (source: ClawHub release metadata; artifact frontmatter and changelog show 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
