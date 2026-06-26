## Description: <br>
GAIN predicts rice agronomic traits from genotype and environmental data using pre-trained MMoE deep learning models, with support for climate stress simulations in Chinese and English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianlvdouhua](https://clawhub.ai/user/qianlvdouhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agronomy researchers, crop modelers, and developers use GAIN to answer rice trait prediction questions, run genotype and environment predictions, and compare climate stress scenarios for supported locations or uploaded VAE genotype files. <br>

### Deployment Geography for Use: <br>
Global; predictions are documented for seven built-in Chinese stations and arbitrary coordinates with nearest-station matching. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact NASA POWER for weather enrichment and cache weather CSVs locally, which can expose or retain requested coordinates. <br>
Mitigation: Use built-in or offline environmental data when location disclosure is a concern, and review or clear local weather caches as needed. <br>
Risk: Genotype CSVs can contain sensitive research data. <br>
Mitigation: Treat genotype files as sensitive inputs, keep processing local, and avoid sharing uploaded or derived CSVs outside the intended environment. <br>
Risk: The skill depends on Python packages and local model/data files for execution. <br>
Mitigation: Install in an isolated Python environment, review dependency versions before use, and run the provided environment check before predictions. <br>


## Reference(s): <br>
- [GAIN ClawHub skill page](https://clawhub.ai/qianlvdouhua/gain) <br>
- [Qianlvdouhua publisher profile](https://clawhub.ai/user/qianlvdouhua) <br>
- [NASA POWER daily point API](https://power.larc.nasa.gov/api/temporal/daily/point) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; local prediction scripts can return JSON or human-readable tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include location details, genotype predictions, environment predictions, stress scenario predictions, and trait metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
