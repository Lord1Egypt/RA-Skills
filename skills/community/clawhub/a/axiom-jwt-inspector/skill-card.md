## Description: <br>
Decodes JWT headers and payloads, reports expiration details, and provides local HMAC verification and test-token creation utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect JWT structure, debug token contents, and perform local HMAC checks without treating the result as full authentication validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public skill description emphasizes inspection, but the artifact can verify HMAC signatures and create signed JWTs. <br>
Mitigation: Treat the skill as a local JWT signing and HMAC verification utility, and review the code and CLI options before installation or operational use. <br>
Risk: JWT secrets supplied on the command line may be exposed through shell history, process listings, or logs. <br>
Mitigation: Use test secrets where possible and avoid passing production JWT secrets through command-line arguments. <br>
Risk: The artifact does not provide complete JWT authentication validation, including audience, issuer, nbf, exp enforcement, asymmetric algorithms, or JWE support. <br>
Mitigation: Use a maintained JWT library with full validation for authentication decisions, and reserve this skill for debugging, inspection, and local testing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/axiom-jwt-inspector) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON, with Python and shell usage examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local stdlib Python utility; no network service or LLM dependency is indicated.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
