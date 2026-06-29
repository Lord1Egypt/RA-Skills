## Description: <br>
Builds, compiles, and deploys WebAssembly HTTP apps to Gcore FastEdge edge computing using the Rust SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geri4](https://clawhub.ai/user/geri4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold Rust WebAssembly HTTP apps, build Wasm artifacts, upload binaries, and create or update Gcore FastEdge apps with configuration for environment variables, secrets, and KV storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Upload, create, update, and release commands can publish a selected Wasm binary to a live Gcore FastEdge endpoint. <br>
Mitigation: Confirm app names, app IDs, binary IDs, and the target Wasm artifact before running deployment commands. <br>
Risk: GCORE_API_KEY is required for upload and deployment and could grant access to Gcore resources if exposed. <br>
Mitigation: Treat the key as sensitive, keep it out of logs and shared shells, and rotate it after suspected exposure. <br>
Risk: A shadowed or overridden Rust toolchain can affect build output or cause misleading build failures. <br>
Mitigation: Run the helper from a trusted repository and clean shell environment, and verify CARGO and RUSTC resolve through rustup before building. <br>


## Reference(s): <br>
- [ClawHub Gcore FastEdge skill page](https://clawhub.ai/geri4/skills/gcore-fastedge) <br>
- [Gcore FastEdge docs](https://gcore.com/docs/fastedge) <br>
- [Gcore FastEdge LLM API reference](https://gcore.com/docs/fastedge/llms.txt) <br>
- [Gcore Edge Storage API](https://gcore.com/docs/api-reference/fastedge/edge-storage/create-a-new-edge-store) <br>
- [Gcore API tokens](https://accounts.gcore.com/account-settings/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Rust, TOML, JSON, bash, and Python command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of a bundled Rust starter template and Python build/deploy helper.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
