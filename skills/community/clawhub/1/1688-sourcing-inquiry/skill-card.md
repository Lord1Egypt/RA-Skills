## Description: <br>
Transforms vague 1688 procurement intent into structured sourcing inquiries so suppliers can be matched and quotations can be requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External procurement users and agents use this skill before selecting a specific product or supplier to submit 1688 sourcing inquiries from a product name, quantity, and requirements. It is intended for quote-seeking and supplier matching, not product browsing, supplier directory lookup, order placement, payment, or logistics tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 1688 Access Key and stores credentials locally. <br>
Mitigation: Use a limited and revocable credential where available, configure it only through the documented flow, and rotate or revoke it when access is no longer needed. <br>
Risk: The security review source flags token-management and telemetry behavior for careful review. <br>
Mitigation: Review credential handling, token storage, and usage-reporting behavior before deployment in shared or business environments. <br>
Risk: Procurement inquiries create sourcing tasks and may send incomplete or unintended requirements if the agent guesses missing fields. <br>
Mitigation: Require explicit product name, numeric quantity, and demand details before running procurement commands. <br>


## Reference(s): <br>
- [1688 Sourcing Inquiry on ClawHub](https://clawhub.ai/1688aiinfra/1688-sourcing-inquiry) <br>
- [Procurement capability guide](references/capabilities/procurement.md) <br>
- [Configuration guide](references/capabilities/configure.md) <br>
- [Common error handling](references/common/error-handling.md) <br>
- [1688 authorization page](https://air.1688.com/app/tai/oauth_page/index.html) <br>
- [1688 skills gateway](https://skills-gateway.1688.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON objects containing a success flag, user-facing markdown, and optional structured data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent should display the markdown field directly and use structured data only as supporting context.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
