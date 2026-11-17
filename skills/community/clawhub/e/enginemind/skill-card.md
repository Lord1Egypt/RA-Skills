## Description:

A Rust+Python consciousness engine with 12-phase crystal dynamics, thalamic relay processing, 19 introspective inner voices, and holographic emission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marceloadryao](https://clawhub.ai/user/marceloadryao)

### License/Terms of Use:

MIT

## Use Case:

Developers and researchers use EngineMind to process text through a Rust/Python consciousness-simulation engine and inspect emergent state metrics, inner voice reports, burst analyses, and dashboard visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled orchestration scripts can read local agent identity and memory files and log processed content.

Mitigation: Run the skill only in an isolated project directory, review the files selected for processing, and avoid running it from a user profile or shared agent workspace.

Risk: The bundled dashboard is unauthenticated and the security evidence notes broader-than-expected exposure and a path traversal issue.

Mitigation: Keep the dashboard local-only, remove the path traversal issue, and do not expose it on a network before review.

Risk: Dashboard assets may load browser dependencies from external CDNs.

Mitigation: Vendor browser dependencies before using the dashboard with sensitive data or in restricted environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marceloadryao/skills/enginemind)
- [EngineMind Repository](https://github.com/marceloadryao/EngineMind)
- [EngineMind README](README.md)
- [Architecture Deep Dive](docs/ARCHITECTURE.md)
- [Emergent Phenomena](docs/EMERGENT_PHENOMENA.md)
- [Inner Voice System](docs/INNER_VOICES.md)
- [Burst Analysis](docs/BURST_ANALYSIS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation and guidance with code examples, shell commands, runtime JSONL logs, and dashboard data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Rust/Python source files, scripts, local dashboard assets, and generated simulation reports when run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
