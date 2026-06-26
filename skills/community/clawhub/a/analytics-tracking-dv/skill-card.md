## Description: <br>
Provides utilities and templates for UTM campaign links, conversion pixel snippets, attribution rules, and product tracking plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketing operators, and product teams use this skill to standardize campaign links, conversion pixel setup, attribution rules, and tracking-plan documentation for digital products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics and pixel guidance can create privacy or consent obligations when deployed with GA4, Facebook Pixel, Gumroad, webhooks, or Segment. <br>
Mitigation: Confirm consent requirements, update the privacy notice, avoid unnecessary personal data, and test tracking only after the deployment context is approved. <br>
Risk: The release evidence flags a mismatch between Segment-oriented skill text and UTM/pixel-oriented documentation. <br>
Mitigation: Resolve the documentation mismatch before operators rely on the skill so the intended tracking approach is clear. <br>
Risk: Pixel IDs, measurement IDs, conversion IDs, and labels are placeholders, and the artifact does not verify installation or firing. <br>
Mitigation: Replace placeholders with authorized platform identifiers and manually test conversion tracking end to end before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/analytics-tracking-dv) <br>
- [README.md](README.md) <br>
- [TRACKING-PLAN.md](TRACKING-PLAN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, JSON configuration, and code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes placeholder pixel IDs and tracking templates that require operator configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
