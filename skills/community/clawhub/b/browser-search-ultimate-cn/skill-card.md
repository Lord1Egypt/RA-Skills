## Description: <br>
Runs Chinese web searches through public search pages and returns a concise answer summary plus source-labeled result links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chn012cjus](https://clawhub.ai/user/chn012cjus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Chinese-language web searches for current information, news, and general lookup tasks, then inspect the returned snippets and URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to external search providers. <br>
Mitigation: Do not enter secrets, credentials, confidential customer data, or private project names as search terms. <br>
Risk: The skill invokes curl.exe from PATH. <br>
Mitigation: Confirm that PATH resolves to the trusted system curl.exe before use. <br>
Risk: Parsed search snippets can be noisy, incomplete, or unavailable when providers block automated requests. <br>
Mitigation: Review source URLs directly and treat returned snippets as leads rather than authoritative answers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chn012cjus/browser-search-ultimate-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text search summary with source-labeled result list and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted Windows curl.exe on PATH and sends query terms to external search providers.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
