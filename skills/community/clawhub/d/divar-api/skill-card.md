## Description: <br>
Use this skill when a user wants to search, query, or extract data from Divar (divar.ir), including real-estate listings, filters, pagination, post details, contact information, or Divar API request structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hadifarnoud](https://clawhub.ai/user/hadifarnoud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to build or answer questions about Divar search workflows, listing extraction, API payloads, pagination, and post-detail lookup. It is most relevant when translating Divar web searches into structured JSON API requests or interpreting widget-based API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes authenticated access to seller contact information and account-related endpoints. <br>
Mitigation: Use authenticated requests only for accounts and data you are authorized to access, and avoid collecting, storing, or redisplaying seller phone numbers unless there is a clear permitted purpose. <br>
Risk: The skill references cookies, JWTs, device IDs, and session state. <br>
Mitigation: Do not provide Divar cookies, JWTs, device IDs, or session data unless explicitly authorizing authenticated requests for your own account. <br>
Risk: Automated listing extraction can create privacy, compliance, or platform-abuse concerns. <br>
Mitigation: Use reasonable request pacing, respect Divar terms and applicable regulations, and keep telemetry or account-state endpoints out of scope unless specifically authorized. <br>


## Reference(s): <br>
- [Divar API Reference](references/api-reference.md) <br>
- [Divar API Documentation](divar-api-documentation.md) <br>
- [Divar API Base URL](https://api.divar.ir) <br>
- [Protocol Buffers](https://protobuf.dev/) <br>
- [ClawHub Skill Page](https://clawhub.ai/hadifarnoud/divar-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Configuration] <br>
**Output Format:** [Markdown with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint paths, typed JSON payloads, filter mappings, authentication notes, and parsing guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
