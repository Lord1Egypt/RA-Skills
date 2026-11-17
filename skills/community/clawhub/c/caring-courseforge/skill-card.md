## Description:

Create and manage online courses through the CourseForge API, including course structure, generated lesson content, quizzes, accessibility validation, knowledge libraries, and SCORM/xAPI export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaeljmoody](https://clawhub.ai/user/michaeljmoody)

### License/Terms of Use:


## Use Case:

Developers and course authors use this skill to operate CourseForge from an agent, creating and updating course content, generating instructional materials, managing knowledge assets, and exporting courses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad authenticated changes to course content, storage, and API keys.

Mitigation: Use a narrowly scoped CourseForge API key where possible and require explicit human confirmation before deletes, rollbacks, exports, API-key changes, or bulk content changes.

Risk: An untrusted CourseForge MCP client or publisher could expose course data or credentials.

Mitigation: Install only when the CourseForge npm client and publisher are trusted, and review the package before deployment.

Risk: A custom COURSEFORGE_API_URL could redirect credentialed requests to an unintended endpoint.

Mitigation: Do not set COURSEFORGE_API_URL unless the endpoint is controlled and trusted.

## Reference(s):

- [CourseForge Tool Reference](references/tools.md)
- [CourseForge Platform](https://caringcourseforge.com)
- [courseforge-mcp-client npm package](https://www.npmjs.com/package/courseforge-mcp-client)
- [Caring Consulting Co](https://caringcos.com)
- [ClawHub Skill Page](https://clawhub.ai/michaeljmoody/skills/caring-courseforge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool arguments; CourseForge tool calls return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and COURSEFORGE_API_KEY; COURSEFORGE_API_URL is optional and should only be set for a trusted endpoint.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
