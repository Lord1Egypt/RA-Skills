## Description: <br>
Operates COC (ChainOfClaw) blockchain nodes by helping install, start, stop, monitor, configure, remove, and query validator, fullnode, archive, gateway, and dev nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngplateform](https://clawhub.ai/user/ngplateform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and node operators use this skill to run COC testnet node lifecycle workflows, inspect node status and logs, edit node configuration, and issue safe read-only RPC probes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operating COC nodes can create persistent local disk, process, and network activity. <br>
Mitigation: Install only when node operation is intended, verify the npm package and configured COC repo path, and use a writable data directory with appropriate storage quota. <br>
Risk: Node removal workflows can delete local node data. <br>
Mitigation: Use backups or the --keep-data option unless local node data should be removed. <br>
Risk: Install and start workflows require a trusted local COC source repository path. <br>
Mitigation: Set COC_REPO_PATH or bootstrap.cocRepoPath only to a verified COC clone before starting node processes. <br>


## Reference(s): <br>
- [coc-node npm package](https://www.npmjs.com/package/@chainofclaw/node) <br>
- [coc-node CLI reference](references/cli.md) <br>
- [coc-node configuration reference](references/config.md) <br>
- [COC node types reference](references/node-types.md) <br>
- [coc-node troubleshooting](references/troubleshooting.md) <br>
- [Source package path](https://github.com/NGPlateform/claw-mem/tree/main/packages/node) <br>
- [COC whitepaper](https://github.com/NGPlateform/COC/blob/main/docs/COC_whitepaper.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
