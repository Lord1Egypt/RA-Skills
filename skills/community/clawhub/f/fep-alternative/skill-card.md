## Description:

Relative binding free-energy and activity-label prediction workflows using PBCNet 2.0 on SciMiner, with Gnina docking and PDB/database retrieval to complete missing inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and computational chemistry teams use this skill to predict relative binding affinity or activity labels for candidate small molecules against a known target. It helps complete missing receptor, pocket, docking, or conformation inputs before invoking SciMiner PBCNet 2.0.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable remote SciMiner documentation to construct authenticated API calls.

Mitigation: Review the resolved SciMiner documentation and generated payloads before execution, allowlist only required SciMiner endpoints, and do not execute code copied directly from remote Markdown.

Risk: The workflow uses outbound network calls and can save raw RCSB responses to caller-selected paths.

Mitigation: Run the skill in a sandbox with restricted filesystem access, allowlist SciMiner and RCSB destinations, and restrict or disable raw response writes unless an approved output path is provided.

Risk: The skill requires a SciMiner API token for authenticated calls.

Mitigation: Use a scoped SciMiner token stored outside the repository at the documented credentials path, and prevent token values from being printed, logged, or committed.

## Reference(s):

- [FEP Alternative on ClawHub](https://clawhub.ai/sciminer/skills/fep-alternative)
- [SciMiner API key utility](https://sciminer.tech/utility)
- [SciMiner tool API documentation](https://sciminer.tech/tool_api_files/)
- [RCSB PDB Data API](https://data.rcsb.org/rest/v1)
- [RCSB PDB Search API](https://search.rcsb.org/rcsbsearch/v2)
- [Bundled RCSB PDB sub-skill](rcsb-pdb-skill/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, JSON request payloads, and SciMiner share URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare API payloads, file-upload steps, docking workflow decisions, compact RCSB summaries, and final task links.]

## Skill Version(s):

1.0.1 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
