## Description: <br>
Auto-generates comparison tables for concepts, drugs, or study results in Markdown format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to generate Markdown comparison-table skeletons for concepts, drugs, treatments, or study results from command-line item and attribute lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional --output argument writes directly to the specified path and could overwrite an important workspace file. <br>
Mitigation: Choose a deliberate workspace filename, keep output inside the intended workspace, and review the generated JSON before using it. <br>
Risk: Generated tables provide structure only and do not validate medical or research claims. <br>
Mitigation: Fill and review table values against appropriate source material before using the output in medical, research, or decision-support contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/comparison-table-gen) <br>
- [Comparison Table Gen References](references/guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, text] <br>
**Output Format:** [JSON object containing a Markdown table string plus item and attribute metadata; printed to stdout or written to an optional JSON file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external Python packages are required; table cells are generated as placeholders for user-supplied comparison attributes.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
