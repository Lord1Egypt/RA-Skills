## Description: <br>
Scores B2B leads from CSV input using a local rule-based script and produces lead scores, probability labels, risk levels, and top-factor labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and operations users can ask an agent to run this skill against a CSV of B2B leads to create a ranked scoring file for review. The scores should be treated as prototype prioritization signals rather than a validated predictive model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation claims LightGBM, SHAP explainability, and API support, while the evidence shows a local rule-based CSV scorer. <br>
Mitigation: Treat generated scores as prototype prioritization hints and require corrected documentation or shipped model, explainability, dependency, and API functionality before relying on them. <br>
Risk: Lead scores may influence sales or procurement decisions without validated model performance or fairness evidence. <br>
Mitigation: Use human review for downstream decisions and validate the scoring behavior against representative data before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1477009639zw-blip/betaleadscore) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [CSV output file with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and local CSV input; runtime imports include pandas and numpy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
