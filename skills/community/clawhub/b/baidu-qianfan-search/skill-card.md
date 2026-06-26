## Description: <br>
Comprehensive search API integration for Baidu Qianfan Web Search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsall357357](https://clawhub.ai/user/lsall357357) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Baidu Qianfan enterprise web searches from an agent, including time-filtered, site-filtered, image, video, and safe-search queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, filters, and result requests are sent to Baidu Qianfan using the user's API key. <br>
Mitigation: Use a dedicated key where possible and avoid secrets, personal data, or confidential business queries unless that provider flow is approved. <br>
Risk: The skill depends on a local API key or .env file for authentication. <br>
Mitigation: Keep any .env file private, do not publish credentials with the skill, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [Baidu Qianfan Search API Reference](references/api-reference.md) <br>
- [Baidu Cloud](https://cloud.baidu.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/lsall357357/baidu-qianfan-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and command output; raw JSON is available with the --raw option.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied BAIDU_QIANFAN_API_KEY and sends search queries to Baidu Qianfan.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, _meta.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
