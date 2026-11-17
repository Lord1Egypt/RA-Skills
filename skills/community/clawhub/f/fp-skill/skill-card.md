## Description:

Checks nationwide VAT invoice authenticity by automating browser queries against China's official VAT invoice verification platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serendipity2430](https://clawhub.ai/user/serendipity2430)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users can use this skill to automate VAT invoice verification workflows and return whether invoice information is consistent with the verification result. The skill is most relevant where invoice documents and browser-based verification need to be handled by an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive invoice data through browser uploads and screenshot capture.

Mitigation: Run it only in a tightly isolated, non-root environment and avoid real invoice data until file paths, screenshot handling, and upload confirmation behavior are reviewed.

Risk: The security evidence flags unsafe browser and file behaviors, including certificate-warning handling and an auxiliary patch script that adds unverified URL fetching.

Mitigation: Review the code before installation, pin the expected destination domain, preserve certificate validation, and avoid running patch_fp.py unless it has been audited.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/serendipity2430/skills/fp-skill)
- [Publisher Profile](https://clawhub.ai/user/serendipity2430)
- [Official VAT Invoice Verification Platform](https://inv-veri.chinatax.gov.cn/fpcygzfw/national-invoice-check)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text result messages with optional screenshot image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload invoice files and save screenshots during browser automation.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
