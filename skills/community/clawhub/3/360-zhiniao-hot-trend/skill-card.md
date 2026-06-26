## Description: <br>
Organizes and summarizes public 360 Zhiniao and 360 large-model product pages, documentation, pricing, and announcement information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect concise summaries and link lists from public 360 Zhiniao product, pricing, announcement, and documentation pages. It is intended for lightweight public information organization, not account actions or private-data handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may surface stale or incomplete public pricing, quota, model, or service-status information from dynamically loaded pages. <br>
Mitigation: Verify important details against the current public 360 Zhiniao pages before relying on them for business or integration decisions. <br>
Risk: Using the skill with credentials, private business data, or sensitive documents would exceed the artifact's stated public-information boundary. <br>
Mitigation: Keep use limited to public pages and do not provide credentials, private business data, or sensitive documents unless a future release explicitly justifies that access. <br>
Risk: High-frequency page retrieval could conflict with platform access expectations. <br>
Mitigation: Apply rate limits and respect the target site's platform rules when collecting public pages. <br>


## Reference(s): <br>
- [360 Zhiniao public homepage](https://ai.360.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/360-zhiniao-hot-trend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and link lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public-page information only; no credentials, API calls, account actions, code execution, or private data are requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
