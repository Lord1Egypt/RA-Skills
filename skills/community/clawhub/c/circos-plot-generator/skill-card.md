## Description: <br>
Generate Circos configuration files for circular genomics data visualization, including genomic variations, cell-cell communication networks, and custom track configurations for publication-ready circular plots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renhaosu2024](https://clawhub.ai/user/renhaosu2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and bioinformatics teams use this skill to generate Circos configuration and data files for circular genomics figures, including variation, chromosome ideogram, structural variant, and cell-cell communication visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Existing files such as circos.conf and data/*.txt may be overwritten in the selected output directory. <br>
Mitigation: Use a dedicated empty output folder for each run, especially in shared project directories. <br>
Risk: Optional rendering invokes a local Circos command and depends on locally installed packages. <br>
Mitigation: Review the render command before running it and install dependencies only from trusted package sources. <br>


## Reference(s): <br>
- [Circos Official Documentation](http://circos.ca/documentation) <br>
- [Circos Tutorials](http://circos.ca/documentation/tutorials) <br>
- [Bioconda Circos Recipe](https://bioconda.github.io/recipes/circos/README.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/renhaosu2024/circos-plot-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Configuration instructions, Shell commands, Code] <br>
**Output Format:** [Text configuration files, TSV data files, Markdown guidance, and optional PNG/SVG render outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes circos.conf and data/*.txt files to the selected output directory; optional rendering requires a local Circos installation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
