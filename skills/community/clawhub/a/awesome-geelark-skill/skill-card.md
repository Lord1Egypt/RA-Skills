## Description: <br>
Interact with GeeLark Cloud Phone API for managing cloud phones, automation tasks, and social media operations. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[geelarkbot](https://clawhub.ai/user/geelarkbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure GeeLark API access, manage cloud phones, run diagnostics, install apps, and guide social-media RPA workflows with human review for sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access GeeLark account credentials, cloud phones, ADB sessions, and social-media automation workflows. <br>
Mitigation: Keep assets/config.json and logs private, restrict file permissions, and install only when this level of access is acceptable. <br>
Risk: Automation may post or delete external social-media content or perform destructive cloud-phone actions. <br>
Mitigation: Require explicit human confirmation before posting, deleting, enabling ADB, or running credential-dependent RPA tasks. <br>
Risk: Android permission prompts can expose device data if granted automatically. <br>
Mitigation: Prefer denying permissions or manually reviewing permission prompts unless the user has confirmed the requested access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geelarkbot/awesome-geelark-skill) <br>
- [GeeLark website](https://www.geelark.com/) <br>
- [GeeLark OpenAPI](https://openapi.geelark.com) <br>
- [GeeLark API Reference](references/api_reference.md) <br>
- [GeeLark API Best Practices](references/best_practices.md) <br>
- [ADB Operations Guide](references/cloudphone_operations.md) <br>
- [Auto-Close Mechanism](references/auto_close.md) <br>
- [GeeLark API Error Codes](references/error_codes.md) <br>
- [RPA Tasks Guide](references/rpa_tasks.md) <br>
- [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local configuration steps, diagnostic commands, and automation guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
