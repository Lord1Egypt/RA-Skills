## Description:

Manage browser sessions for jimeng.jianying.com with Playwright by importing cookies and browser storage to automate Jimeng video generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyingzl](https://clawhub.ai/user/flyingzl)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to preserve and replay Jimeng browser sessions for authenticated video generation workflows, including image upload, prompt entry, and page-state checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles raw Jimeng login session data that can function like account credentials.

Mitigation: Store session JSON locally with restricted access, keep it out of shared temporary paths and source control, and rotate or delete it when no longer needed.

Risk: The automation can submit authenticated account actions, including uploads and generation requests that may spend credits.

Mitigation: Run the browser in a contained environment and review each generation request before allowing it to upload private inputs or consume account credits.

## Reference(s):

- [Jimeng Session Data Usage Guide](references/jimeng-usage.md)
- [Browser Session Manager ClawHub Page](https://clawhub.ai/flyingzl/skills/browser-session-manager)
- [Jimeng Web Application](https://jimeng.jianying.com/ai-tool/home?type=video)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Playwright automation steps, session JSON handling guidance, and screenshot or troubleshooting instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
