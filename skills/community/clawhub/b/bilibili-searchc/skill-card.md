## Description: <br>
Real-time Bilibili video search that retrieves top video titles for a requested keyword through a user-run local API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raise7727](https://clawhub.ai/user/raise7727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query current Bilibili video results by keyword and receive structured titles for trend tracking, creator monitoring, or competitive research. It depends on a local FastAPI service backed by Playwright. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls a user-run local FastAPI and Playwright service, so installation and use depend on trusting that local service. <br>
Mitigation: Run only the expected local service, keep it bound to localhost, and review the service before using the skill with sensitive workflows. <br>
Risk: Search keywords may be sent through the local service to Bilibili, and headless browser activity can consume local resources. <br>
Mitigation: Avoid sensitive search terms and monitor local browser automation resource usage during execution. <br>


## Reference(s): <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [OpenAPI specification](artifact/openapi.json) <br>
- [ClawHub release page](https://clawhub.ai/raise7727/bilibili-searchc) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON search results containing Bilibili video titles, with optional agent-authored text or Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are driven by a keyword query and the availability of the local FastAPI and Playwright service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
