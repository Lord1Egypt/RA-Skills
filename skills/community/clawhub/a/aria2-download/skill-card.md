## Description:

Adds download tasks through Aria2 RPC and supports real-time progress monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ingress007](https://clawhub.ai/user/ingress007)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to add, inspect, list, and monitor Aria2 download jobs through an RPC endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aria2 RPC access can expose control over downloads if port 6800 or a remote endpoint is reachable by untrusted parties.

Mitigation: Use only trusted localhost or private-network RPC endpoints, require a strong unique RPC secret, and avoid exposing port 6800 publicly.

Risk: Remote Aria2 RPC use may expose requests or credentials without transport protection.

Mitigation: Use TLS or equivalent network protection for remote access.

Risk: The security review notes shell parsing and JSON handling that can expose local code execution risk.

Mitigation: Review before installing and patch the script to build JSON with a real encoder and parse RPC responses as data rather than interpolating them into node -e.

Risk: The documented Docker setup relies on an external Aria2 image.

Mitigation: Pin the Docker image before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Aria2 RPC configuration from environment variables and reports download identifiers, status, progress, and completion details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
