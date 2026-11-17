## Description:

Automates Banjixiaoguanjia homework capture by controlling Chrome with Playwright to enter a course, scroll student lists, capture homework screenshots, download original images, and optionally analyze homework with DashScope/Qwen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wosuiyu](https://clawhub.ai/user/wosuiyu)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers or authorized school staff use this skill to collect, download, and optionally AI-review student homework from Banjixiaoguanjia courses. It is intended for bulk screenshot capture and grading-support workflows where the operator has permission to process the students' work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes student homework and may capture personal or educational records.

Mitigation: Use it only with authorization to process the relevant students' work, minimize collected data, and add explicit confirmation and retention controls before deployment.

Risk: Homework images may be sent to DashScope/Qwen for AI analysis.

Mitigation: Confirm that the external AI service is approved for this data before use, or disable AI analysis when such transfer is not allowed.

Risk: The artifact includes credential handling issues, including a hard-coded API key and shell profile reads.

Mitigation: Remove hard-coded secrets, rotate any exposed key, stop reading .zshrc, and use approved secret storage or environment variables.

Risk: Some scripts use shell-based curl calls and generated Python execution.

Mitigation: Replace shell execution and generated scripts with safer API clients, validate paths and URLs, and avoid executing generated code from untrusted inputs.

Risk: Browser automation uses a logged-in Chrome session and remote debugging port.

Mitigation: Run with an isolated browser profile, restrict access to the debugging port, and confirm the operator is logged into the intended authorized account.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wosuiyu/skills/banjixiaoguanjia)
- [Banjixiaoguanjia web app](https://service.banjixiaoguanjia.com/appweb/)
- [Alibaba Bailian console](https://bailian.console.aliyun.com)
- [DashScope compatible-mode API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JavaScript/Python code examples; bundled scripts produce image files, text reports, and Word documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime outputs are written to local course folders and may include student homework screenshots, downloaded images, AI analysis text, and generated DOCX reports.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
