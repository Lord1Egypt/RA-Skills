## Description: <br>
Secure environment variable and secret management with AES-256 encryption, auto-redaction, permission controls, and credential leak prevention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ayalili](https://clawhub.ai/user/Ayalili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to store, retrieve, redact, list, delete, and bulk-load environment variables and credentials while reducing accidental secret exposure in logs or agent output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weak secret protections could expose credentials if the skill is invoked too broadly or trusted without review. <br>
Mitigation: Review the skill before installing and allow invocation only in tightly controlled agent contexts. <br>
Risk: Broad loadFromEnv prefixes can import more environment variables than intended. <br>
Mitigation: Use narrow prefixes and verify which variables will be loaded before enabling bulk import. <br>
Risk: allowSecret and showSecrets are request flags, not durable authorization controls. <br>
Mitigation: Do not rely on these flags as the sole access control for sensitive values. <br>
Risk: Generated encryption keys may appear in logs if a secure key is not supplied. <br>
Mitigation: Provide encryption keys through a secure channel and avoid logging generated keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ayalili/env-secure-manager) <br>
- [Deno zod dependency](https://deno.land/x/zod@v3.22.4/mod.ts) <br>
- [Deno crypto dependency](https://deno.land/std@0.214.0/crypto/mod.ts) <br>
- [Deno hex encoding dependency](https://deno.land/std@0.214.0/encoding/hex.ts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [JSON-like structured action results and redacted text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions include init, set, get, list, delete, redact, and loadFromEnv.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
