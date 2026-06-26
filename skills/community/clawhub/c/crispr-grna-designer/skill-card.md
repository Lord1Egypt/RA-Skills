## Description: <br>
Design CRISPR gRNA sequences for specific gene exons with off-target prediction and efficiency scoring. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bioinformatics practitioners use this skill to generate candidate CRISPR guide RNAs, score predicted on-target efficiency, and review off-target summaries for gene-editing planning. Current evidence supports demonstration and review use only, not direct experimental decision-making. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that the skill presents CRISPR guide design as real while the implementation silently uses mock sequence data and simulated off-target checks. <br>
Mitigation: Treat outputs as demonstration-only until real gene and exon retrieval, real genome-wide off-target analysis, clear mock-mode labeling, tests, and benchmarks are independently verified. <br>
Risk: Guide RNA efficiency and off-target predictions can be misleading for laboratory or clinical decisions. <br>
Mitigation: Require independent computational review and experimental validation of candidate guides before any wet-lab use. <br>
Risk: The artifact includes executable Python and unpinned scientific dependencies. <br>
Mitigation: Run in a sandboxed environment, pin and audit dependencies, and constrain output paths before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/crispr-grna-designer) <br>
- [Scoring algorithms reference](references/scoring_algorithms.md) <br>
- [Off-target databases reference](references/off_target_databases.md) <br>
- [Efficiency benchmarks reference](references/efficiency_benchmarks.md) <br>
- [GUIDE-seq dataset reference](https://github.com/tsailabSJ/guideseq) <br>
- [Cas-OFFinder](http://www.rgenome.net/cas-offinder/) <br>
- [CHOPCHOP](https://chopchop.cbu.uib.no/) <br>
- [Ensembl REST API](https://rest.ensembl.org/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON results with candidate guides, predicted scores, off-target summaries, and warnings; Markdown guidance may include command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are computational predictions and, per security evidence, may be mock or simulated unless the implementation is independently verified.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
