## Description:

Calculate complex buffer recipes with precise measurements for molecular biology and biochemistry applications, including mass and volume calculations, pH considerations, and step-by-step preparation instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and lab teams use this skill to draft buffer preparation calculations and protocols for common molecular biology and biochemistry buffers such as PBS, RIPA, and TAE. Treat generated quantities as draft calculations that require correction and independent validation before real lab preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safety-relevant lab calculations may be incorrect.

Mitigation: Correct and independently validate the calculation code before using any quantities for real buffer preparation.

Risk: Generated recipes may be mistaken for approved laboratory protocols.

Mitigation: Check all output against trusted protocols, reagent labels, safety data sheets, and institutional lab procedures before preparation.

Risk: The skill requests broad local Write/Edit and shell access despite mainly producing calculations and guidance.

Mitigation: Run it in a restricted workspace and avoid granting broad filesystem or shell permissions unless they are needed for a reviewed workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/buffer-calculator)
- [Cold Spring Harbor Protocols](https://cshprotocols.org)
- [Thermo Fisher Buffer Reference](https://www.thermofisher.com/buffers)
- [Sigma-Aldrich Buffer Calculator](https://www.sigmaaldrich.com/biochemicals)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline Python and bash examples plus text calculation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft buffer recipes, component quantities, preparation steps, troubleshooting guidance, and optional local Python command examples.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
