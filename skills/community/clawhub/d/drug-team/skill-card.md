## Description: <br>
Coordinates specialized AI agents to propose and rank drug candidates using synthesis planning, inventory checks, ADMET and toxicity proxies, pharmacology scoring, and patent scouting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to coordinate early-stage drug design workflows that generate candidate molecules, estimate synthesis feasibility, check reagent availability, score ADMET and toxicity properties, and surface patent novelty signals. Outputs are screening aids that require expert chemistry, safety, patent, and procurement review before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run external patent searches that may expose molecule ideas or target information. <br>
Mitigation: Use only non-confidential queries unless external patent lookups are acceptable for the project. <br>
Risk: The workflow may read or modify lab-inventory data while checking reagent stock and estimating synthesis costs. <br>
Mitigation: Run it only against approved inventory data and review any local inventory-file changes before relying on results. <br>
Risk: Drug design, toxicity, patent, and procurement outputs are rough screening signals. <br>
Mitigation: Require expert chemistry, safety, patent, and procurement review before acting on candidate recommendations. <br>
Risk: Broad trigger phrases can activate the workflow in general drug, synthesis, stock, patent, or novelty discussions. <br>
Mitigation: Enable the skill only in contexts where automated drug-design assistance is intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Cheminem/drug-team) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [Console text with ranked candidate summaries, SMILES strings, scores, route and inventory details, and generated visualization files when dependencies are available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces rough screening results based on local scripts, sibling skills, external patent queries, and chemistry proxy calculations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
