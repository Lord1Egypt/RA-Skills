## Description: <br>
Validate Rust Cargo.toml manifests for dependency issues, missing metadata, feature conflicts, workspace config, and crates.io publishing readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate Rust Cargo.toml files, audit dependency and feature configuration, and check crates.io publishing readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled local Python validator against Cargo.toml files selected by the user. <br>
Mitigation: Review the script before use in sensitive projects and run it only against manifests intended for local analysis. <br>
Risk: Publisher provenance is limited because server-resolved GitHub import provenance is unavailable for this version. <br>
Mitigation: Rely on the ClawHub publisher profile and release evidence, and perform additional publisher review before high-trust deployment. <br>


## Reference(s): <br>
- [Cargo Toml Validator on ClawHub](https://clawhub.ai/charlie-morrison/cargo-toml-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, JSON, or compact summary output from the validator, plus human-facing validation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on a user-selected Cargo.toml file and can return errors, warnings, info findings, suggestions, and CI-friendly exit codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
