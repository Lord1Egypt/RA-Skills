## Description: <br>
Terminal ASCII chart toolkit. Create bar charts, sparklines, histograms, and gauges from CSV or JSON data in the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate terminal charts, summarize CSV or JSON data, normalize and pivot datasets, and export simple SVG or HTML views from local data files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SVG and HTML export commands can create unsafe browser-opened files from untrusted CSV content. <br>
Mitigation: Use SVG and HTML export only with trusted CSV files until export escaping is fixed, and review generated browser-opened files before sharing or opening them in sensitive contexts. <br>
Risk: The skill runs local shell and Python code against user-selected data files. <br>
Mitigation: Install and run it only in environments where local script execution is acceptable, and limit input files to data the user trusts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xueyetianya/data-visualizer) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Terminal text, CSV text, SVG files, HTML files, and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write history under DATAVIZ_DIR or the user's XDG data directory and can export adjacent .svg or .html files from CSV inputs.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
