## Description: <br>
Universal AI memory infrastructure that stores, understands, and learns from past interactions for cross-app persistent memory across AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engsathiago](https://clawhub.ai/user/engsathiago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use CogniMemo Memory to add persistent cross-session memory to AI applications, including storing, retrieving, updating, and deleting user preferences, decisions, tasks, facts, and context through CogniMemo APIs and SDKs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain sensitive interaction history, preferences, decisions, tasks, and other personal context beyond the current session. <br>
Mitigation: Enable the skill only with user approval, avoid storing secrets or regulated data unless approved, and confirm deletion and revocation controls before automatic capture. <br>
Risk: Production use requires CogniMemo and storage-provider API keys that could expose memory data if mishandled. <br>
Mitigation: Store credentials in environment variables or a secrets manager, rotate and revoke keys when needed, and verify SDK packages and provider terms before deployment. <br>
Risk: Cross-app memory sharing can disclose data to broader contexts than intended if permissions are too permissive. <br>
Mitigation: Use scoped permissions, check access before storing or retrieving memory, and review app permission and revocation settings regularly. <br>


## Reference(s): <br>
- [CogniMemo Memory on ClawHub](https://clawhub.ai/engsathiago/cognimemo-memory) <br>
- [CogniMemo Website](https://cognimemo.com) <br>
- [CogniMemo Documentation](https://docs.cognimemo.com) <br>
- [CogniMemo API Reference](https://api.cognimemo.com/docs) <br>
- [CogniMemo SDK GitHub Resource](https://github.com/cognimemo/sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API-key environment configuration and example integrations; bundled memory manager script uses mock storage for demonstration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
