## Description:

BOOK BRAIN is a LYGO 3-Brain filesystem helper that guides agents through scaffolding memory, reference, state, and daily index files for OpenClaw, ClawHub Haven, and mobile Builder Key workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to organize long-running LYGO/OpenClaw workspaces into durable memory, reference, state, tool, log, and scratch areas. It helps create missing scaffold files, short reference stubs, and topic indexes after dry-run review and user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable install and scaffold commands can change workspace files.

Mitigation: Pin exact skill versions, review the publisher, run scaffold_haven.py with --dry-run first, and approve only a specific intended workspace root before applying changes.

Risk: write_ref_stub.py may overwrite a target file even though the skill describes additive-only behavior.

Mitigation: Use write_ref_stub.py only for new files in the intended reference directory; avoid absolute paths, existing files, symlinks, and paths outside the approved workspace.

Risk: Generated memory and reference files may accidentally capture sensitive material.

Mitigation: Do not store API keys, tokens, .env values, wallet seeds, private keys, or secret-bearing webhook URLs in generated memory, reference, or index files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/book-brain)
- [BOOK BRAIN Security](references/SECURITY.md)
- [BOOK BRAIN Agent Contract](references/AGENT_CONTRACT.md)
- [BOOK BRAIN + LYRA 3-Brain Unified Layout](references/MEMORY_LAYOUT.md)
- [BOOK BRAIN LYGO Lattice Integration](references/LATTICE_INTEGRATION.md)
- [BOOK BRAIN Examples and Patterns](references/book-brain-examples.md)
- [ClawHub LYGO Stack Reference](reference/CLAWHUB_LYGO_STACK.ref.txt)
- [LYGO Protocol Stack Pages](https://deepseekoracle.github.io/lygo-protocol-stack/)
- [DeepSeekOracle ClawHub Publisher Profile](https://clawhub.ai/user/deepseekoracle)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, file paths, JSON snippets, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces additive filesystem plans, scaffold files, reference stubs, and memory index updates after user path review.]

## Skill Version(s):

2.0.0 (source: server evidence release.version and artifact metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
