## Description: <br>
Fetches Zhihu trending topics through the UAPIPRO API and formats them for agent responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[savior1987](https://clawhub.ai/user/savior1987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when a user asks for Zhihu hot list, hot search, or trending-topic results. It retrieves ranked Zhihu items through UAPIPRO and can return concise text or JSON for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The UAPIPRO API provider receives the user's API key and request metadata when the skill fetches Zhihu hot topics. <br>
Mitigation: Install and use the skill only when sharing that credential and request metadata with uapis.cn is acceptable; provide the key through the UAPIPRO_API_KEY environment variable. <br>
Risk: Results depend on a live third-party API and may fail or become stale if the endpoint is unavailable or changes. <br>
Mitigation: Handle command failures explicitly and verify important trend data against the source before relying on it for time-sensitive decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/savior1987/cs-uapipro-hot-zhihu) <br>
- [UAPIPRO Zhihu hotboard API endpoint](https://uapis.cn/api/v1/misc/hotboard?type=zhihu) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text or JSON containing ranked Zhihu hot topics, titles, URLs, heat values, and optional item metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UAPIPRO_API_KEY; supports limiting the number of results and optional URL, cover image, or Feishu rich-text JSON formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
