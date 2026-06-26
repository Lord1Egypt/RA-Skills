## Description: <br>
1688 Source Suppliers queries the 1688 platform for supplier and factory information using a user-provided keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up 1688 suppliers and factories by supplier name, product category, region, or other search keyword. It helps surface supplier listings while preserving the user's query intent and avoiding fabricated supplier information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive 1688 access key. <br>
Mitigation: Use platform-managed secrets or environment variables instead of pasting the key into chat, and rotate the key if it appears in chat or command history. <br>
Risk: Access-key setup may affect a separate 1688-shopkeeper configuration entry. <br>
Mitigation: Verify the target configuration before and after setup so an unrelated 1688-shopkeeper credential is not overwritten. <br>
Risk: Supplier data comes from an external lookup service and may be incomplete, unavailable, rate-limited, or returned with authentication errors. <br>
Mitigation: Show the tool's returned markdown errors to the user, retry after rate limits, and confirm supplier details before commercial action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-source-suppliers) <br>
- [Publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [1688 supplier query guide](references/capabilities/ali_1688_source_suppliers.md) <br>
- [Access key configuration guide](references/capabilities/configure.md) <br>
- [1688 supplier search](https://s.1688.com/company/company_search.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON object with success, markdown, and data fields; markdown contains supplier listings or user-readable error guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided query and a configured ALI_1688_AK access key; supplier records are filtered for company name, cooperation mode, and services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
