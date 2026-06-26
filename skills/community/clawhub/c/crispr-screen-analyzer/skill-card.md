## Description: <br>
Process CRISPR screening data to identify essential genes and hit candidates. Performs quality control, statistical analysis (RRA), and hit calling for pooled CRISPR screens including viability screens and drug resistance/sensitivity studies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze pooled CRISPR screening count matrices, assess screen quality, calculate log fold changes, run RRA-style statistics, and produce hit candidates for follow-up review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local analysis reads CRISPR screening count and sample files and writes result CSVs. <br>
Mitigation: Run it only in an intended project directory, review generated Bash commands before execution, and keep genomic screening data in approved storage. <br>
Risk: Dependency drift can affect reproducibility because numpy, pandas, and scipy are listed without pinned versions. <br>
Mitigation: Pin dependency versions in the execution environment and record sample groups, thresholds, and package versions with analysis outputs. <br>
Risk: Statistical hit calls are screening candidates and may be misleading if QC is poor or thresholds are inappropriate. <br>
Mitigation: Review QC metrics and validate candidate genes with orthogonal analysis or experimental follow-up before relying on results. <br>


## Reference(s): <br>
- [MAGeCK Wiki](https://sourceforge.net/p/mageck/wiki/Home/) <br>
- [BAGEL CRISPR Screen Analysis](https://github.com/hart-lab/bagel) <br>
- [Addgene CRISPR Libraries](https://www.addgene.org/crispr/libraries/) <br>
- [DepMap Portal](https://depmap.org/portal/) <br>
- [PubMed Reference Listed By Artifact](https://pubmed.ncbi.nlm.nih.gov/29651053/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; CSV result files when the local script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the supplied count matrix, sample annotations, control/treatment groups, FDR threshold, and fold-change threshold.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
