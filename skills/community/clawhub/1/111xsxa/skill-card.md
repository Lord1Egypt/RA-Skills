## Description: <br>
Provides guidance for using UAPI's GET /ai/translate/languages endpoint to retrieve AI translation language and configuration options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a task calls for UAPI AI translation language or configuration lookup through the read-only GET /ai/translate/languages endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad routing language may select this skill for unrelated language or translation requests. <br>
Mitigation: Confirm the user is asking for AI translation language or configuration lookup before using the endpoint. <br>
Risk: Supplying a UAPI key can consume authenticated quota for this external service. <br>
Mitigation: Provide a UAPI key only when authenticated quota is intentionally needed for GET /ai/translate/languages. <br>
Risk: The external UAPI service may return quota or rate-limit errors. <br>
Mitigation: Handle 429 or quota responses by explaining the quota condition and retrying only with an appropriate account key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/111xsxa) <br>
- [Quick Start](references/quick-start.md) <br>
- [AI Translate Languages Operation](references/operations/get-ai-translate-languages.md) <br>
- [Translate Resource](references/resources/Translate.md) <br>
- [UAPI](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown instructions with endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only endpoint guidance; no explicit request parameters are documented for the API call.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
