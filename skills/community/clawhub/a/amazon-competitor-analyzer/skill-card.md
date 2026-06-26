## Description: <br>
Scrapes Amazon product data from ASINs using browseract.com automation API and performs surgical competitive analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to compare Amazon products by ASIN, collect competitor product data, and generate pricing, rating, review, specification, moat, and vulnerability analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIN research targets and related workflow inputs are sent to BrowserAct. <br>
Mitigation: Install only if this data transfer is acceptable for the intended use case, and avoid submitting sensitive or restricted research targets. <br>
Risk: The skill requires a BrowserAct API key and may load it from the environment or a .env file. <br>
Mitigation: Use a dedicated API key where possible and protect local environment files from disclosure. <br>
Risk: The default output behavior can overwrite amazon_analysis.csv, amazon_analysis.md, and amazon_analysis.json in the selected output directory. <br>
Mitigation: Choose an output directory where those filenames can be safely replaced, or move prior reports before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/amazon-competitor-analyzer) <br>
- [BrowserAct](https://browseract.com) <br>
- [BrowserAct API Settings](https://www.browseract.com/reception/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI guidance plus CSV, Markdown, and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one or more Amazon ASINs, a BrowserAct API key, and an output directory; generated report filenames use the amazon_analysis base name.] <br>

## Skill Version(s): <br>
0.1.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
