## Description: <br>
Fetches current library documentation through the Context7 API so agents can search libraries and retrieve documentation context for library-dependent work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[am-will](https://clawhub.ai/user/am-will) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to find up-to-date API documentation, implementation patterns, and library-specific behavior before building or debugging features that depend on external packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an embedded fallback Context7 API key when CONTEXT7_API_KEY is not configured. <br>
Mitigation: Require users to provide their own CONTEXT7_API_KEY, remove the fallback key before deployment, and document that library names, library IDs, and queries are sent to Context7. <br>


## Reference(s): <br>
- [Context7 API endpoint](https://context7.com/api/v2) <br>
- [ClawHub skill page](https://clawhub.ai/am-will/context7-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text, markdown-formatted text, or JSON returned by a Python CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports search and context commands; context responses can be limited with --tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
