## Description: <br>
Use Camofox/Camoufox as an opt-in anti-detection browser server for agent workflows that need cloaked browsing, with guidance for npm/npx startup, OpenClaw tools, REST API commands, sessions, environment variables, and Hermes routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a user-directed browser workflow specifically needs Camofox/Camoufox cloaking or stable Camofox accessibility refs because ordinary automation may be blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables cloaked anti-detection browsing and should only be used for workflows where that capability is intentional. <br>
Mitigation: Load and apply the skill only when the user-directed task specifically needs Camofox/Camoufox or anti-detection browsing. <br>
Risk: A browser server exposed beyond localhost can create unauthorized access risk if bearer tokens are not configured. <br>
Mitigation: Keep the server bound to localhost by default, and set strong CAMOFOX_ACCESS_KEY authentication before exposing it beyond loopback. <br>
Risk: Globally setting CAMOFOX_URL in Hermes can route unrelated browser calls through Camofox for that process. <br>
Mitigation: Use CAMOFOX_URL only inline for a dedicated cloaked Hermes run, and avoid storing it in global Hermes, shell, gateway, service, or project environments. <br>
Risk: Cookie, profile, trace, and crash-report data can contain sensitive browsing information. <br>
Mitigation: Review local storage paths and trace retention, use CAMOFOX_API_KEY for sensitive endpoints, and set CAMOFOX_CRASH_REPORT_ENABLED=false when privacy is important. <br>


## Reference(s): <br>
- [Camofox Browser homepage](https://github.com/jo-inc/camofox-browser) <br>
- [ClawHub skill page](https://clawhub.ai/tmchow/skills/camofox-cloaked-browser) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tmchow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown with inline shell commands, REST examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes runtime choice, base URL, auth posture, user/session identifiers, tab handling, verification, and cleanup reporting.] <br>

## Skill Version(s): <br>
1.3.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
