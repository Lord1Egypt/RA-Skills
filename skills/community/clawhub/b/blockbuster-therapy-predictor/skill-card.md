## Description:

Predicts which early-stage biotechnology platforms may have blockbuster therapy potential by scoring mock clinical, patent, funding, market, and momentum signals.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and biotech strategy teams can use this skill to generate demonstration rankings for therapeutic modalities such as PROTAC, mRNA, CRISPR, CAR-T, ADC, and related platforms. Outputs should support exploration only and should not replace expert due diligence, regulatory review, or authoritative investment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overstate the reliability of mock-data biotech investment analysis.

Mitigation: Treat outputs as demonstration decision support only and require expert due diligence plus authoritative clinical, patent, and funding data before R&D or investment decisions.

Risk: Saving reports can overwrite user-writable files when an unsafe or existing --save path is used.

Mitigation: Use only new workspace-relative output paths and avoid absolute paths, ../ paths, symlinks, or existing files until output-path validation and overwrite protection are added.

Risk: Installing requirements may use dependencies that are unpinned or unnecessary for modern Python environments.

Mitigation: Review, remove, or pin dependencies before running pip install -r requirements.txt.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/blockbuster-therapy-predictor)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Console text or JSON report, with optional saved JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranked technology scores include blockbuster index, maturity, market potential, momentum, recommendation, key drivers, risk factors, and predicted timeline.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
