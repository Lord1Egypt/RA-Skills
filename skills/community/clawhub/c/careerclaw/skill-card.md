## Description: <br>
Run a job search briefing, find job matches, draft outreach emails, or track job applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orestes-garcia-martinez](https://clawhub.ai/user/orestes-garcia-martinez) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External job seekers use CareerClaw through an agent to fetch job listings, rank them against a local profile and resume, draft outreach, and maintain an application tracking log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume text, profile data, and tracking state may be stored in plaintext under .careerclaw. <br>
Mitigation: Review the local storage behavior before installation, keep .careerclaw out of version control, and use filesystem protections appropriate for resume and job-search data. <br>
Risk: Pro features may send derived candidate or job signals to OpenAI or Anthropic and validate a license with Gumroad. <br>
Mitigation: Use Pro features only after reviewing the configured provider, model, API key, and license validation behavior. <br>
Risk: Debug scripts can expose license keys if run with real credentials. <br>
Mitigation: Do not run debug scripts with real keys until raw key logging is removed or otherwise confirmed safe. <br>
Risk: The release under-discloses sensitive resume and key handling in its permissions surface. <br>
Mitigation: Require updated permissions documentation that explicitly covers resume.txt, profile.json, and .license_cache before broad deployment. <br>


## Reference(s): <br>
- [CareerClaw ClawHub listing](https://clawhub.ai/orestes-garcia-martinez/careerclaw) <br>
- [careerclaw-js npm package](https://www.npmjs.com/package/careerclaw-js) <br>
- [CareerClaw Pro purchase page](https://ogm.gumroad.com/l/careerclaw-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown summaries with CLI commands, optional JSON output, and outreach draft text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local CareerClaw runtime files such as profile, resume text, run logs, and application tracking state.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, package.json, CHANGELOG, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
