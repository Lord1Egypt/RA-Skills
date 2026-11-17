## Description:

Download, search, and analyze Patent-Mol-Wiki biomedical-patent packages. Use when users ask what happened in a recent patent period, need portfolio or trend statistics from wiki index.md files, ask whether a target, disease, modality, organization, or patent is present, need charts of patent distributions, or need molecular-structure analysis from selected patent folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

External patent analysts, biomedical researchers, and developers use this skill to retrieve Patent-Mol-Wiki packages, search local patent wiki corpora, compute trend and portfolio statistics, and inspect selected molecular-structure records with reproducible evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader may send the SciMiner API key to URLs returned by the provider.

Mitigation: Use a rotateable SciMiner API key, review provider result URLs before download, and prefer a fixed download allowlist or header-free package downloads.

Risk: Downloaded corpora, manifests, and raw provider responses may contain task IDs, paths, raw API responses, or private patent text.

Mitigation: Keep downloaded data and manifests private until reviewed and redacted for sensitive identifiers or private content.

Risk: Keyword counts and search matches can be incomplete or may not prove patent claim coverage.

Mitigation: Report corpus coverage and aliases, treat matches as retrieval evidence, and inspect claims before making scope conclusions.

## Reference(s):

- [Patent-Mol-Wiki download API](references/patent-mol-wiki-api.md)
- [Structure-analysis rules](references/structure-analysis.md)
- [Biomedical Patent Trends on ClawHub](https://clawhub.ai/sciminer/skills/biomedical-patent-trends)
- [SciMiner API key utility](https://sciminer.tech/utility)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, CSV, SVG]

**Output Format:** [Markdown guidance with inline shell commands plus generated JSON, CSV, and SVG analysis artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include coverage, source paths or hashes, retrieval timestamps, command provenance, and caveats for incomplete corpora, aliases, and claim scope.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
