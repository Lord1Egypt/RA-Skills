## Description:

给一个行业或一家公司，把上游（原材料/零部件/设备）、中游（制造/集成）、下游（渠道/终端）三层列出来，每个环节点名代表公司与其在链条里的位置，每条挂 [S#] 与来源；链条上没查到的环节逐条写「未取到」，不补常识。不判景气、不判好坏、不选股。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

Analysts and researchers use this skill to map an industry's or company's upstream, midstream, and downstream links, tie each identified company and its role to a dated source, and list gaps without making industry-cycle or stock recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security assessment rates the release suspicious, citing a mismatch between its documented supply-chain mapping purpose and parts of its behavior.

Mitigation: Review the installed content and check that its behavior matches the documented task before enabling it.

Risk: The supplied security assessment notes an unpinned installer and an API key sent to a catalog-selected endpoint.

Mitigation: Review the installer source, resolved endpoint, credential handling, and information sent before use; keep the API key in a local credential facility.

## Reference(s):

- [CUE data MCP setup](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [CUE API key](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Six-section Markdown supply-chain map with source anchors and retrieval dates; optionally a fill-in skeleton.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates upstream, midstream, downstream, named gaps, and sources; does not assess industry prospects or recommend stocks.]

## Skill Version(s):

0.1.0 (source: frontmatter, changelog, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
