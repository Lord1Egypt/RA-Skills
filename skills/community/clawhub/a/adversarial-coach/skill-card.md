## Description:

Adversarial implementation review based on Block's g3 dialectical autocoding research for validating implementation completeness against requirements with fresh objectivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killerapp](https://clawhub.ai/user/killerapp)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to run an adversarial implementation review against requirements, test results, and common security or functional gaps before accepting a change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect requirements, source code, and test results, which can expose repository details beyond the intended review scope.

Mitigation: Run the review only in the intended workspace with normal repository access controls, and keep unrelated sensitive files out of scope.

Risk: The approval signal can be misleading if requirements are incomplete or compilation and test claims are accepted without verification.

Mitigation: Provide explicit requirements and verify build or test claims against actual tool results before accepting IMPLEMENTATION_APPROVED.

## Reference(s):

- [Adversarial Cooperation in Code Synthesis](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf)
- [g3 implementation](https://github.com/dhanji/g3)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review verdict with concise bullets and optional file or line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the IMPLEMENTATION_APPROVED termination signal when all stated approval criteria are met.]

## Skill Version(s):

0.9.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
