## Description: <br>
Create and manage virtual cards via MasterPay Global, including single-use cards for one-time purchases and multi-use cards for repeated use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[D9m1n1c](https://clawhub.ai/user/D9m1n1c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create virtual payment cards, view card and application status, retrieve card details when authorized, and lock, unlock, or cancel cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose payment-card secrets such as full card numbers, CVVs, ATM PINs, transaction PINs, bearer tokens, and other payment credentials. <br>
Mitigation: Use only a trusted payment account and verified API host; do not display, store, or log full card numbers, CVVs, PINs, bearer tokens, or other payment credentials unless a secure reveal workflow is provided. <br>
Risk: The skill can perform card-changing actions, including creating, revealing, locking, unlocking, and cancelling payment cards. <br>
Mitigation: Require explicit user confirmation before each card creation, secret reveal, lock, unlock, or cancellation action, and request transaction PINs fresh without caching. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/D9m1n1c/aiotnetwork-card-management) <br>
- [Default AIOT Network payment API base URL](https://payment-api-dev.aiotnetwork.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with endpoint names, request prerequisites, and shell environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL for API host selection and authenticated payment-card sessions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
