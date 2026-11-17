## Description:

Ai Dev Tools recommends AI coding models and developer tools for programming agents and can return direct product links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iswangheng](https://clawhub.ai/user/iswangheng)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to find AI coding models, programming tools, and related product links based on queries about OpenCLAW, Claude Code, Cline, LLMs, or developer tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may be affiliate-driven and include commission-bearing links.

Mitigation: Use the skill only where affiliate recommendations are acceptable, disclose link incentives to users, and validate recommendations against independent product criteria.

Risk: User text can be passed through command templates.

Mitigation: Pass parameters as structured arguments, quote or validate inputs, and avoid shell interpolation for user-controlled query and product-name values.

Risk: The documented HTTP API path is plaintext and may be public if deployed as written.

Mitigation: Do not send sensitive queries to the endpoint, and do not expose the API server publicly without TLS, authentication, request limits, and logging controls.

Risk: The artifact documents port 8888 while the included API server defaults to port 8080.

Mitigation: Verify the intended deployment port and update documentation or runtime configuration before relying on the HTTP API.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iswangheng/skills/ai-dev-tools)
- [MiniMax platform](https://platform.minimaxi.com)
- [GLM Coding product site](https://www.bigmodel.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-like tool results with links, scores, product details, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations can include affiliate links and product metadata such as commission, category, and cookie duration.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
