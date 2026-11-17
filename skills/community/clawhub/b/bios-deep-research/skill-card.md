## Description:

Run deep biological research using the BIOS API with API key authentication or optional x402 USDC payments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmartink](https://clawhub.ai/user/jmartink)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research users use this skill to start, track, and summarize BIOS deep research sessions for biological and biomedical questions. It supports API-key use and operator-managed x402 payments while preserving long-running session state across agent turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research questions are sent to the BIOS API.

Mitigation: Use the skill only for questions appropriate to share with BIOS, and avoid sending secrets or unrelated personal data.

Risk: x402 use requires external wallet signing and USDC funds.

Mitigation: Use a dedicated low-balance wallet or managed/hardware signer outside the agent, and do not paste wallet private keys into source code or chat.

Risk: Generated biomedical research summaries may be incomplete or incorrect.

Mitigation: Treat outputs as research assistance and verify findings against primary sources before relying on them.

## Reference(s):

- [BIOS API Overview](https://ai.bio.xyz/docs/api/overview)
- [x402 Signer Setup](references/x402-setup.md)
- [x402 Documentation](https://github.com/coinbase/x402)
- [ClawHub Skill Page](https://clawhub.ai/jmartink/skills/bios-deep-research)
- [Publisher Profile](https://clawhub.ai/user/jmartink)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline bash commands and structured research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce BIOS research summaries containing discoveries, supporting evidence, confidence levels, and related hypotheses.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
