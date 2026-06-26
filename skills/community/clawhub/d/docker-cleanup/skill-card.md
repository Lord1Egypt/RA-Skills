## Description: <br>
Docker resource cleanup, pruning, and disk usage analysis toolkit for inspecting Docker containers, images, volumes, networks, and build cache usage, pruning unused resources, and generating cleanup reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze Docker disk usage, identify reclaimable resources, prune stopped or unused Docker resources, and generate JSON or HTML cleanup reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup flags such as --all, --volumes, and --force can permanently delete Docker resources. <br>
Mitigation: Run the default analysis or --report mode first, review unused resources, and use destructive cleanup flags only after confirming the target Docker environment. <br>
Risk: Generated HTML reports may contact jsDelivr for Bootstrap styling when opened. <br>
Mitigation: Open reports only in environments where that external request is acceptable, or remove the remote stylesheet before sharing or archiving the report. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus optional JSON output and generated HTML report files from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The default workflow is analysis-only; cleanup flags can prune Docker resources, and report mode writes a timestamped HTML file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
