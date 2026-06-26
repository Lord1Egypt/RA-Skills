## Description: <br>
Fetch web pages as clean Markdown and search the web via the distil.net proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikel](https://clawhub.ai/user/mikel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to fetch, search, render, screenshot, or retrieve raw web content through the Distil proxy using curl. It is useful when web pages need to be converted into concise Markdown for agent research or documentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs, searches, and fetched content are routed through the configured Distil proxy. <br>
Mitigation: Use this skill only with Distil or a self-hosted proxy that is approved for the data being sent. <br>
Risk: Secret-bearing URLs, private internal endpoints, regulated data, or sensitive research queries could be exposed to the proxy. <br>
Mitigation: Avoid sending sensitive URLs, private endpoints, regulated data, or sensitive queries unless the proxy is approved for that use. <br>
Risk: Fetched page content and proxy-inserted comments are untrusted source material. <br>
Mitigation: Review and validate fetched content before relying on it or using it to guide agent actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mikel/distil) <br>
- [Publisher Profile](https://clawhub.ai/user/mikel) <br>
- [Distil](https://distil.net) <br>
- [Distil Proxy](https://proxy.distil.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, images] <br>
**Output Format:** [Markdown, raw web content, or image files returned through curl commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and DISTIL_API_KEY; DISTIL_PROXY_URL can override the default proxy.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
