## Description:

Provides a standard MCP gateway that lets agent frameworks call ten Chinese large language model providers through a unified interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT

## Use Case:

Developers use the gateway to connect MCP-compatible agents and supported agent frameworks to Chinese model providers through a single interface. They can request model responses, multimodal analysis, embeddings, reranking, transcription, and gateway usage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports undeclared capabilities and behavior that conflicts with the gateway's stated purpose, as well as unexpected network access and unsafe troubleshooting advice.

Mitigation: Review the skill carefully before installation, compare its behavior with its advertised purpose, and inspect troubleshooting guidance before following it.

Risk: The security guidance identifies possible model downloads, prompt transmission to providers, and local storage of prompts and votes; scanner coverage is partial because some referenced paths were missing.

Mitigation: Review provider data handling and local storage behavior, and inspect the referenced paths before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fyniujin/skills/cn-model-gateway)
- [Project homepage](https://skillhub.cn/skill/cn-model-gateway)
- [Provider error map](references/error_map.yaml)

## Skill Output:

**Output Type(s):** [Text, JSON, Embeddings, Ranked results, Transcriptions, Usage and health reports]

**Output Format:** [MCP JSON-RPC responses and provider-dependent model outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and supported modalities depend on the selected provider and model.]

## Skill Version(s):

2.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
