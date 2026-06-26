## Description: <br>
Faces helps an agent create, compile, compare, compose, and chat through persona-like Faces using the Faces CLI and Faces Platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sybileak](https://clawhub.ai/user/sybileak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the Faces CLI for account setup, persona creation, source compilation, chat, semantic comparison, boolean composition, billing, and API-key workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send source material, persona attributes, and chat content to the Faces service. <br>
Mitigation: Use it only when the user intends to share that content, and avoid uploading confidential or third-party material without consent. <br>
Risk: Persona creation can involve sensitive personal data, including demographic attributes and uploaded documents. <br>
Mitigation: Minimize sensitive data collection and do not provide government identifiers such as SSNs or tax IDs. <br>
Risk: Authentication examples include account credentials and API keys. <br>
Mitigation: Prefer scoped API keys with budgets and expiry, and avoid typing real passwords directly into reusable command-line examples. <br>
Risk: Registration, compilation, inference, and subscription workflows can incur charges. <br>
Mitigation: Confirm paid actions with the user, review plan terms, and check balances, quotas, and budgets before use. <br>


## Reference(s): <br>
- [Quickstart](references/QUICKSTART.md) <br>
- [Full command reference](references/REFERENCE.md) <br>
- [Authentication & Registration](references/AUTH.md) <br>
- [What is Faces](references/CONCEPTS.md) <br>
- [Instruction Scope](references/SCOPE.md) <br>
- [Face Templates](references/TEMPLATES.md) <br>
- [Accepted Attribute Keys](references/ATTRIBUTES.md) <br>
- [OAuth - Connect ChatGPT](references/OAUTH.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-aware CLI output handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the faces CLI, Faces Platform credentials, and internet access to api.faces.sh or the configured FACES_BASE_URL.] <br>

## Skill Version(s): <br>
1.6.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
