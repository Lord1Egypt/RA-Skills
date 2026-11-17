## Description:

Verify Bitcoin SV (BSV) Merkle proofs against bsv.cx block headers, returning confirmed, rejected, or inconclusive outcomes and optionally fetching BEEF or BUMP proofs for a txid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bsv-cx](https://clawhub.ai/user/bsv-cx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fetch or verify Bitcoin SV transaction inclusion proofs through bsv.cx using curl, jq, and standard proof formats. It is suited for read-only proof checks where no wallet keys, signing, or spending actions are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends BSV txids, BEEF/BUMP data, or raw proof material to bsv.cx.

Mitigation: Use the skill only when that proof material is acceptable to share with bsv.cx; for confidential or unpublished transactions, use local verification or a self-hosted verifier.

Risk: The skill says the live bsv.cx SPV contract is the source of truth over the reviewed local instructions.

Mitigation: Treat the live contract as endpoint documentation for proof retrieval and verification only, and require review before following any future behavior outside that scope.

Risk: Verification depends on the remote service and the block headers bsv.cx has synced.

Mitigation: Treat inconclusive results as unresolved, retry after the service tip advances, or cross-check proofs with an independent local verifier.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bsv-cx/skills/bsv-cx-verify)
- [bsv.cx SPV live contract](https://bsv.cx/spv)
- [bsv.cx service map](https://bsv.cx/)
- [bsv.cx health endpoint](https://bsv.cx/health)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JavaScript code blocks; remote API calls return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; may send BSV txids, BEEF/BUMP data, or raw proof material to bsv.cx.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
