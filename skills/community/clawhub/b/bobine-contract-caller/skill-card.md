## Description: <br>
Use when you need to call deployed Bobine modules with typed params or perform a signed Ed25519 call through an auth module. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccamel](https://clawhub.ai/user/ccamel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to call Bobine contracts through /api/execute, prepare typed parameters, and perform optional signed Ed25519 calls with nonce handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signed calls require private Ed25519 key material. <br>
Mitigation: Treat sigkey values as private credentials and avoid sharing generated private keys in chat or logs. <br>
Risk: Bobine calls use user-provided servers, modules, methods, and parameters, and signed calls may be state-changing. <br>
Mitigation: Verify the server, module, method, params, and auth module before running any signed or state-changing call. <br>
Risk: Inline spark generation is CPU-bound. <br>
Mitigation: Use spark-effort deliberately and avoid unnecessarily high effort settings in constrained environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ccamel/bobine-contract-caller) <br>
- [Bobine Project](https://github.com/hazae41/bobine) <br>
- [Bobine Concept Overview](https://www.bobine.tech/) <br>
- [Standard Bobine Libraries](https://github.com/hazae41/stdbob) <br>
- [Bobine Param Grammar](references/params.md) <br>
- [Runtime and Env](references/runtime.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful calls print one JSON object to stdout; diagnostics and failures are emitted on stderr.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
