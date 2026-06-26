## Description: <br>
Use this skill when an agent needs to operate the `cosin` CLI from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcipher0](https://clawhub.ai/user/0xcipher0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate the `cosin` CLI for COS API calls, skill catalog discovery, and `/cos/...` skill requests from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: COS bearer tokens can be exposed through shell history, logs, or CI output when passed directly as `--key <token>`. <br>
Mitigation: Use a protected environment variable, stdin prompt, or secret manager for tokens where possible, and rotate any token that may have been exposed. <br>
Risk: `/cos/...` paths are converted into x402 pay-and-call requests to the COS backend. <br>
Mitigation: Confirm the request path, method, and user intent before running commands that invoke `/cos/...` skill paths. <br>


## Reference(s): <br>
- [Cosin on ClawHub](https://clawhub.ai/0xcipher0/cosin) <br>
- [COS Skills Catalog](https://skills.bankofuniverse.org/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI command shapes, input validation guidance, and response-reading guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
