## Description: <br>
Provides physics-based, data-grounded Earth science reasoning with explicit uncertainty for geology, wells, seismic, petrophysics, and subsurface analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariffazil](https://clawhub.ai/user/ariffazil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and domain specialists use this skill to make Earth-domain responses separate observation, derivation, interpretation, and speculation while preserving uncertainty. It is most relevant for geology, wells, seismic interpretation, petrophysics, basin modeling, and other subsurface reasoning tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad activation language can trigger evidence-labeling behavior on generic terms outside a geoscience context. <br>
Mitigation: Apply the skill when Earth-domain reasoning is relevant, and review unexpectedly activated outputs before relying on them. <br>
Risk: Geoscience outputs can be mistaken for operational conclusions in wells, seismic interpretation, reserves, or safety-critical workflows. <br>
Mitigation: Treat outputs as advisory and require qualified human review, source data checks, and explicit authorization before operational use. <br>


## Reference(s): <br>
- [Geox Ground on ClawHub](https://clawhub.ai/ariffazil/geox-ground) <br>
- [GEOX Epistemic Labels](references/epistemic-labels.md) <br>
- [GEOX Hold Conditions](references/hold-conditions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown or plain text with explicit epistemic labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OBS, DER, INT, and SPEC labels to distinguish evidence levels; safety-critical or operational outputs remain advisory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
