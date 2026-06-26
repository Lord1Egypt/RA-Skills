## Description: <br>
Analyzes AFM force-distance curves and nanoindentation data to extract Young's modulus, adhesion, deformation maps, and related mechanical measurements using multiple indentation models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrayxiaoruiyang-pixel](https://clawhub.ai/user/xrayxiaoruiyang-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and engineers use this skill to process AFM force spectroscopy, nanoindentation, adhesion-map, and electrochemical cycling datasets and produce mechanical-property summaries for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scientific parsers and model fits are heuristic, so calculated moduli, adhesion values, and deformation summaries may be misleading if the input format, units, or model assumptions are wrong. <br>
Mitigation: Provide explicit input files, output paths, indenter geometry, tip radius, and Poisson ratio, then review the generated plots, fit quality, and summary values before using results. <br>
Risk: The analyzer reads local data files and writes reports and data products to a user-selected output directory. <br>
Mitigation: Run it in a controlled workspace with intended AFM datasets and inspect the output directory before sharing generated files. <br>


## Reference(s): <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/xrayxiaoruiyang-pixel/afm-force-curve-analyzer-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with bash command examples; generated analyzer outputs may include PNG dashboards, CSV tables, JSON metadata, and Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on explicit input data, output paths, and selected indentation parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
