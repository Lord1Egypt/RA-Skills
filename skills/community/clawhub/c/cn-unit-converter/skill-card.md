## Description: <br>
Cn Unit Converter helps agents convert numeric values across common Chinese and international units for length, weight, temperature, volume, area, data size, and time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform quick local unit conversions through a Python command-line script. It is suited for workflows that need structured conversion results without network access or API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capability metadata claims sensitive credentials are required even though the artifact does not use credentials. <br>
Mitigation: Do not provide API keys, tokens, or private data; run the local converter only with numeric values and unit names. <br>
Risk: The README includes external promotional links unrelated to conversion execution. <br>
Mitigation: Review external links before visiting them; the conversion script itself runs offline and does not contact those sites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-unit-converter) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON output from the Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script uses the Python standard library and returns rounded conversion results or an unsupported-conversion error.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
