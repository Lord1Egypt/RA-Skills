## Description: <br>
Queries Amazon Best Sellers rankings through the Clawec API, optionally filtered by supported category, for product and competitor research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace operators and agents use this skill to fetch and summarize Amazon Best Sellers data by category for product selection, competitor research, and market scanning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Clawec API key and sends Amazon category queries to Clawec. <br>
Mitigation: Store the key in CLAWEC_API_KEY, avoid hardcoding it, avoid adding unrelated private business data to prompts, and rotate the key if it is exposed. <br>
Risk: Unsupported category codes can cause failed or misleading API responses. <br>
Mitigation: Validate category codes against the documented list and fall back to the all-category query when no supported mapping is available. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/anyunzhong/clawec-amazon-best-seller) <br>
- [Amazon Best Sellers response schema](references/response-schema.md) <br>
- [Clawec API base URL](https://www.clawec.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, JSON API responses, and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWEC_API_KEY; category filtering is optional and limited to the documented category codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
