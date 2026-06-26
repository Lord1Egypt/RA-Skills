## Description: <br>
Guides agents in maintaining or safely modifying existing non-framework frontend code such as vanilla JavaScript, jQuery, HTML/CSS, MPA pages, server-rendered templates, and legacy plugins without migrating stacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to make focused maintenance changes in legacy frontend projects while preserving the existing stack, style, and architecture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated changes can mishandle legacy DOM rendering or user input, especially around direct HTML insertion and URL parameter rendering. <br>
Mitigation: Review generated changes for escaped output and avoid inserting user-controlled content through innerHTML or jQuery .html(). <br>
Risk: Ajax and form updates can miss loading, error, empty, duplicate-submit, or CSRF handling in older code paths. <br>
Mitigation: Verify request state handling, duplicate-submit protection, and CSRF token behavior before shipping changes. <br>


## Reference(s): <br>
- [Legacy Frontend Maintenance Patterns](references/legacy-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
2.4.0 (source: release evidence, README.md, metadata.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
