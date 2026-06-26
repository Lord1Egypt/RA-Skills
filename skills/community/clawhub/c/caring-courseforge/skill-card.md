## Description: <br>
Caring CourseForge helps agents create and manage online courses through the CourseForge API, including course structure, AI content generation, quizzes, accessibility validation, knowledge libraries, and SCORM/xAPI export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaeljmoody](https://clawhub.ai/user/michaeljmoody) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and course builders use this skill to manage Caring CourseForge courses, modules, lessons, content blocks, knowledge libraries, AI-assisted content, and course exports from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad account-changing actions in CourseForge, including deletes, revocations, rollbacks, uploads, exports, storage cleanup, and auto-fix actions. <br>
Mitigation: Use a least-privileged API key and require explicit user confirmation before destructive, administrative, export, upload, scraping, rollback, or auto-fix actions. <br>
Risk: The COURSEFORGE_API_KEY grants access to the user's CourseForge account. <br>
Mitigation: Store the key only in the gateway or shell environment, avoid plaintext workspace files, and rotate the key if exposure is suspected. <br>
Risk: AI-generated or externally sourced course content may be inaccurate, inappropriate, or not ready for publication. <br>
Mitigation: Review generated content, validate course quality and accessibility, and inspect exported packages before publishing or distributing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michaeljmoody/caring-courseforge) <br>
- [Publisher profile](https://clawhub.ai/user/michaeljmoody) <br>
- [CourseForge platform](https://caringcourseforge.com) <br>
- [courseforge-mcp-client npm package](https://www.npmjs.com/package/courseforge-mcp-client) <br>
- [Caring Consulting Co](https://caringcos.com) <br>
- [CourseForge Tool Reference](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and clean JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and COURSEFORGE_API_KEY; the wrapper strips the MCP envelope from tool responses.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
