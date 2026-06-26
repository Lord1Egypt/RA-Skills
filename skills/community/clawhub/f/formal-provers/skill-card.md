## Description: <br>
Formal verification with Lean 4, Coq, and Z3 SMT solver. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willamhou](https://clawhub.ai/user/willamhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical users use this skill to check Lean 4 proofs, verify Coq theories, solve Z3 SMT-LIB2 satisfiability problems, and inspect local prover availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proof, Coq, or SMT inputs are written to local temporary storage during checks. <br>
Mitigation: Avoid including secrets or sensitive data in prover inputs. <br>
Risk: Lean and Coq may read local standard libraries, toolchains, package paths, and environment-defined search paths during normal prover execution. <br>
Mitigation: Install Lean, Coq, and Z3 from trusted sources, keep them updated, and run the skill in an environment with appropriate filesystem boundaries. <br>
Risk: Unresolved Lean imports could trigger package tooling behavior outside the skill's direct network requests. <br>
Mitigation: Avoid lake-managed project files in the temporary working area and review Lean imports before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/willamhou/formal-provers) <br>
- [Prismer source and homepage](https://github.com/Prismer-AI/Prismer) <br>
- [Lean 4 setup documentation](https://leanprover.github.io/lean4/doc/setup.html) <br>
- [Coq download documentation](https://coq.inria.fr/download) <br>
- [Z3 project](https://github.com/Z3Prover/z3) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Structured tool results with stdout, stderr, return codes, prover status, satisfiability results, and model text when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local lean, coqc, and z3 binaries; prover invocations use temporary files and a 60-second timeout.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
