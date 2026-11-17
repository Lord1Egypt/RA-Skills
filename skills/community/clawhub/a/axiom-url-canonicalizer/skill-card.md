## Description:

Normalize URLs by lowercasing hosts, sorting query parameters, stripping tracking parameters and default ports, and normalizing percent-encoding for SEO and comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SEO or platform engineers use this skill to canonicalize URLs for comparison, cache deduplication, and tracking-parameter cleanup. It is suited for local normalization workflows where deterministic URL strings or JSON analysis are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake canonicalization output for URL safety validation.

Mitigation: Use this skill only for normalization and comparison; apply separate URL safety, redirect, DNS, and TLS checks before making security decisions.

Risk: The security evidence notes stale manifest and mixed-language documentation, which can make release review harder.

Mitigation: Compare server release metadata, file hashes, and the primary English SKILL.md before installing or approving the release.

Risk: Artifact behavior documents partial IDN and percent-encoding support and unsupported javascript:, mailto:, and data: schemes.

Mitigation: Test representative URL corpora and handle unsupported schemes or internationalized URL edge cases upstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-url-canonicalizer)
- [Publisher profile](https://clawhub.ai/user/kofna3369)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Canonical URL strings, JSON analysis objects, Python snippets, shell command examples, and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local URL normalization; no network requests, redirect following, DNS checks, or TLS validation.]

## Skill Version(s):

0.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
