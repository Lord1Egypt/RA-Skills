## Description:

Analyze and visualize project dependency trees from manifest files for Node.js, Python, Go, Rust, Ruby, and PHP projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect dependency manifests, view dependency trees, compare production and development dependencies, and audit dependency counts across common project types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal tree output may print untrusted dependency names or versions from project manifests.

Mitigation: Use JSON output for downstream processing and treat manifest-derived output from untrusted repositories as untrusted text.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown guidance with terminal text or JSON output from the dependency analyzer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include grouped dependency trees, summary counts, version constraints, and manifest-specific dependency categories.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
