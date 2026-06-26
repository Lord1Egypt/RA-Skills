## Description: <br>
Amazon listing audit skill for Chinese cross-border sellers that flags translation errors, cultural misfires, keyword gaps, and awkward phrasing that can reduce conversions with Western buyers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiwi-phantomworks](https://clawhub.ai/user/kiwi-phantomworks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and ecommerce operators use this skill to audit Amazon listing titles, bullets, and descriptions for translation quality, cultural fit, keyword coverage, conversion signals, and tone. It returns a scored audit with prioritized fixes and targeted rewrite suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may cause the skill to be invoked for generic listing-review requests. <br>
Mitigation: Specify the target marketplace, seller background, product category, and intended buyer audience when requesting an audit. <br>
Risk: External rewrite-service links may be mistaken for required functionality. <br>
Mitigation: Treat linked rewrite services as optional references; the audit itself does not require external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kiwi-phantomworks/cn-amazon-listing-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/kiwi-phantomworks) <br>
- [OpenClaw homepage](https://github.com/PhantomWorksIO/clawhub-skills) <br>
- [Multi-Platform Listing Optimizer for Non-Native Sellers](https://www.shopclawmart.com/listings/multi-platform-listing-optimizer-for-non-native-sellers-ea202e82) <br>
- [PhantomWorks](https://phantomworks.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with scores, a prioritized fix list, rewrite suggestions, and a summary of strengths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code, credentials, persistence, or hidden data access are identified in the security evidence.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
