## Description:

Formal verification with Lean 4, Coq, and Z3 SMT solver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willamhou](https://clawhub.ai/user/willamhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and engineers use this skill to check Lean 4 and Coq proofs, compile Coq files, solve SMT-LIB2 satisfiability problems with Z3, and inspect local prover availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lean and Coq inputs run through local prover binaries without a documented sandbox or constrained environment.

Mitigation: Use the skill for trusted proofs by default; run third-party Lean or Coq files inside a container or other sandbox with a cleaned environment and restricted filesystem access.

Risk: Lean and Coq may read installed standard libraries, toolchains, package search paths, and environment-dependent configuration during normal verification.

Mitigation: Review local Lean and Coq configuration before use and constrain include paths, package search paths, and environment variables when checking untrusted material.

Risk: Unresolved Lean imports could trigger package-management behavior outside the skill's direct network behavior.

Mitigation: Avoid placing lake project files with checked inputs and disable or isolate package-manager network access when evaluating unfamiliar Lean code.

## Reference(s):

- [Prismer project homepage](https://github.com/Prismer-AI/Prismer)
- [Lean 4 setup documentation](https://leanprover.github.io/lean4/doc/setup.html)
- [Coq download documentation](https://coq.inria.fr/download)
- [Z3 project repository](https://github.com/Z3Prover/z3)
- [ClawHub skill page](https://clawhub.ai/willamhou/skills/formal-provers)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON tool results and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lean, Coq, and Z3 checks depend on locally installed prover binaries and use a 60-second timeout.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
