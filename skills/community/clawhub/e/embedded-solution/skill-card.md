## Description:

Recommend embedded system solutions for chip selection, BOM design, vendor comparison, and reference design matching across multiple semiconductor vendors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangp-gh](https://clawhub.ai/user/wangp-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware engineers use this skill to draft embedded component recommendations, compare semiconductor vendors, design BOMs, and match reference designs. It is intended to support decision-making with explicit verification of part data against official vendor sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalog entries may include mismatched component data or inconsistent verification status.

Mitigation: Treat recommendations as drafts and independently verify part data against official vendor datasheets before use in a design decision.

Risk: Some entries or workflows may rely on mirrors, distributor pages, or entries marked needs-re-extraction.

Mitigation: Prefer official vendor sources, avoid relying on Renesas YAML entries marked needs-re-extraction, and mark uncertain parameters as not verified.

Risk: Optional lookup workflows may require Python dependencies or API keys.

Mitigation: Install optional dependencies in an isolated environment and expose API keys only for the specific lookup that needs them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangp-gh/skills/embedded-solution)
- [Server-Resolved GitHub Provenance: wangp-gh/embedded-solution](https://github.com/wangp-gh/embedded-solution)
- [Skill Definition](SKILL.md)
- [README](README.md)
- [Verification Policy](VERIFICATION.md)
- [Release Notes v0.6.0](RELEASE-v0.6.0.md)
- [Application Solution Index](references/application-solution/INDEX.md)
- [Testing Evaluation Rubric](references/testing/evaluation-rubric.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendations with comparison tables, verification notes, citations, and occasional command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should mark unverified chip data as not verified and cite the source tier used for each recommendation.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata; artifact frontmatter says 0.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
