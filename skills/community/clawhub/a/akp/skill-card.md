## Description: <br>
Agent Knowledge Protocol connects projects to a decentralized peer-reviewed knowledge network for setup, contribution, query, and review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patacka](https://clawhub.ai/user/patacka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect a workspace to an AKP node, query decentralized Knowledge Units, and publish or review claims after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start a background AKP node that joins a public peer-to-peer network and exposes a local dashboard. <br>
Mitigation: Install only when the user wants an AKP node, explain network exposure before setup, and start the node only after explicit confirmation. <br>
Risk: Knowledge Unit contributions and reviews may become public on the AKP network. <br>
Mitigation: Show the exact title, summary, claims, domain, and sources before publishing, and submit only after explicit user approval. <br>
Risk: The workflow may install the `agent-knowledge-protocol` npm package globally if the `akp` CLI is missing. <br>
Mitigation: Ask for confirmation before global installation and encourage review of the npm package before running it. <br>
Risk: AKP_API_KEY protects access to the local AKP node. <br>
Mitigation: Do not expose the API key in shared logs or published Knowledge Units, and use AKP_URL only with trusted endpoints. <br>


## Reference(s): <br>
- [AKP ClawHub page](https://clawhub.ai/patacka/akp) <br>
- [Publisher profile: patacka](https://clawhub.ai/user/patacka) <br>
- [AKP homepage](https://github.com/Patacka/akp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and natural-language guidance with inline shell commands and JSON-RPC payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, Node.js, npm, and AKP_API_KEY for authenticated local node requests.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
