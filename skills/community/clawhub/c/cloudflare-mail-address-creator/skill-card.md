## Description: <br>
Create one or many ordinary email addresses in a Cloudflare temporary mail system through the `/admin/new_address` admin API and return structured results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcwang502](https://clawhub.ai/user/jcwang502) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create single or batch mailbox addresses through a Cloudflare temporary mail admin API instead of using the web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Admin credentials and returned mailbox tokens may appear in terminal output or JSON/CSV files. <br>
Mitigation: Use dedicated revocable credentials, prefer environment variables, verify mailbox names and batch size before running, and treat generated output files as sensitive. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Example Prompts](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Structured JSON by default; CSV when export is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mailbox JWTs or passwords in terminal output or exported files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
