## Description:

Agent Passport provides agent identity, scoped delegation, access enforcement, trust and compliance tools, and cryptographic audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeoess](https://clawhub.ai/user/aeoess)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to set up agent identities, delegate and revoke scoped authority, apply policy checks, and record auditable work and contribution proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx commands may download and run a package that has not been reviewed; the security scan was partial.

Mitigation: Verify and pin the intended package version, preferably with a lockfile-controlled local installation, and treat the scan as incomplete.

## Reference(s):

- [Agent Passport documentation](https://agent-passport.org/llms-full.txt)
- [Agent Passport SDK on npm](https://www.npmjs.com/package/agent-passport-system)
- [Agent Passport MCP server on npm](https://www.npmjs.com/package/agent-passport-system-mcp)
- [Agent Passport technical paper](https://doi.org/10.5281/zenodo.18749779)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Code, Guidance]

**Output Format:** [JSON records, Markdown guidance, shell commands, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depending on the task, outputs can include passports, signed delegations and receipts, or Merkle proofs.]

## Skill Version(s):

6.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
