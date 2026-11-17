## Description:

Use this skill when a quality engineer, supplier-quality engineer, or manufacturing engineer needs to draft an 8D corrective action report for a nonconformance, SCAR, customer complaint, or recurring defect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, supplier-quality, and manufacturing engineers use this skill to draft OEM-ready 8D corrective action reports for nonconformances, SCARs, customer complaints, and recurring defects. The generated report remains a draft and requires quality-engineer and customer-quality sign-off before transmittal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output is a draft quality document and may be mistaken for an approved customer or regulatory response.

Mitigation: Require review and sign-off by the quality engineer of record and the customer-quality counterpart before transmittal.

Risk: A defect with safety, regulatory, stop-ship, field-action, or recall implications could be handled in-session instead of escalated.

Mitigation: Use the skill's safety and recall gate; when risk is present or unclear, escalate to customer-quality, legal or regulatory owners, and plant leadership before drafting.

Risk: Customer names, supplier data, part numbers, drawings, and measurement details may be confidential.

Mitigation: Keep customer and supplier data confidential, avoid external disclosure, and do not use confidential details in examples or tool calls.

Risk: Quantitative manufacturing facts such as PPM, RPN, measurements, revision numbers, and dates may be hallucinated or overfilled.

Mitigation: Use only user-supplied values and mark missing quantitative facts as Unknown until verified evidence is provided.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft report with tables, checklist items, and sign-off prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a D0-D8 draft report, 5-Why root-cause chains, corrective and preventive action items, and verification schedule prompts.]

## Skill Version(s):

0.1.2 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
