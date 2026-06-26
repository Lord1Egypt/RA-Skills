## Description: <br>
A web form reverse-engineering tool that intercepts a manually submitted login-required form, analyzes the real API request structure, and generates reusable API documentation and call code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longway-code](https://clawhub.ai/user/longway-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to understand the API behind an existing web form and produce reusable curl or Python examples for authorized form automation and bulk operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects authenticated browser traffic and handles session cookies, which may expose sensitive account data if used in the wrong browser session or on unauthorized systems. <br>
Mitigation: Use only with accounts and systems you are authorized to automate, prefer a dedicated browser profile or test account, keep unrelated sensitive pages closed, and review generated API calls before running them. <br>
Risk: Captured requests, analysis output, and cookies are stored in predictable temporary files. <br>
Mitigation: Delete /tmp/form_api_raw.json, /tmp/form_api_analysis.json, and /tmp/form_api_cookies after use, especially on shared machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longway-code/form2api) <br>
- [Output template](references/output_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with curl and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated API documentation, request parameter annotations, cookie extraction commands, and example API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
