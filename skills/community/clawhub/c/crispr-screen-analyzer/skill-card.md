## Description:

Process CRISPR screening data to identify essential genes and hit candidates. Performs quality control, statistical analysis (RRA), and hit calling for pooled CRISPR screens including viability screens and drug resistance/sensitivity studies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, bioinformatics analysts, and research teams use this skill to assess pooled CRISPR screen quality, calculate sgRNA fold changes, and produce exploratory hit candidates for viability or drug response studies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill documentation overstates the statistical method and safety controls, which could mislead scientific use.

Mitigation: Treat outputs as simplified exploratory analysis, not validated RRA or robust gene-level hit calling; confirm findings with established tools and experimental validation before making scientific decisions.

Risk: Generated CSV outputs may be opened in spreadsheet software.

Mitigation: Avoid opening generated CSVs in spreadsheets unless identifier columns are treated as text or escaped.

Risk: Dependency behavior can change across environments.

Mitigation: Pin dependencies in a controlled environment before running the skill on real experimental data.

## Reference(s):

- [CRISPR Libraries - Addgene](https://www.addgene.org/crispr/libraries/)
- [DepMap Portal](https://depmap.org/portal/)
- [MAGeCK Wiki](https://sourceforge.net/p/mageck/wiki/Home/)
- [Hart Lab BAGEL](https://github.com/hart-lab/bagel)
- [PubMed 29651053](https://pubmed.ncbi.nlm.nih.gov/29651053/)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/crispr-screen-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; the bundled analyzer can produce CSV result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local tabular count and sample files as inputs and can write sgRNA result CSVs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
