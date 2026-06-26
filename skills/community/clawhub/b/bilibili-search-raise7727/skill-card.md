## Description: <br>
Real-time Bilibili video search and structured extraction of trending video titles through a local Playwright-backed API for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raise7727](https://clawhub.ai/user/raise7727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to search Bilibili by keyword, retrieve current video results, and support follow-on summarization, trend tracking, or competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided search keywords to a local service automatically. <br>
Mitigation: Review search terms before use when they may contain sensitive information. <br>
Risk: The local FastAPI and Playwright service performs the actual browser automation and Bilibili access. <br>
Mitigation: Install and run only a trusted local service, and verify it is listening on the expected localhost port before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raise7727/bilibili-search-raise7727) <br>
- [Publisher profile](https://clawhub.ai/user/raise7727) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Text returned from a local API, intended to contain structured Bilibili search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local FastAPI and Playwright service on port 8000.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
