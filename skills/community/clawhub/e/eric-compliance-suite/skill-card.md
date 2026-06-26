## Description: <br>
ERiC Compliance Suite helps agents run ERiC product compliance checks for intellectual property and ecommerce platform policy risks, including design patents, utility patents, graphic trademarks, text trademarks, copyright, and policy compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wteng2286](https://clawhub.ai/user/wteng2286) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and compliance operators use this skill to check product images, titles, descriptions, and policy feature words against ERiC patent, trademark, copyright, and platform-policy APIs before listing or reviewing products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill uploads product images, titles, descriptions, image URLs, and the API token to ERiC. <br>
Mitigation: Use only approved product data, start with non-sensitive test inputs, and keep ERIC_API_TOKEN scoped to a trusted environment. <br>
Risk: The security evidence says the skill can change remote feature-word settings. <br>
Mitigation: Require explicit operator confirmation before P005 or P006 changes and use a token with the minimum privileges available. <br>
Risk: The security evidence says the skill auto-installs a Python dependency at runtime. <br>
Mitigation: Prefer installing and reviewing dependencies yourself in a controlled environment before running the skill. <br>
Risk: The security evidence and artifact behavior show paid checks, radar-enabled checks, and optional automatic safe-word lookups. <br>
Mitigation: Confirm expected credit usage before running checks, especially default radar-enabled modes and automatic T002 safe-word lookups. <br>


## Reference(s): <br>
- [ERiC Compliance Suite ClawHub Page](https://clawhub.ai/wteng2286/eric-compliance-suite) <br>
- [ERiC Website](https://eric-bot.com) <br>
- [D001 Design Patent API Reference](artifact/references/design-patent.md) <br>
- [I001 Utility Patent API Reference](artifact/references/invention-patent.md) <br>
- [L001 Graphic Trademark API Reference](artifact/references/logo-detection.md) <br>
- [T001/T002 Text Trademark API Reference](artifact/references/trademark-detection.md) <br>
- [C001 Copyright API Reference](artifact/references/copyright-detection.md) <br>
- [Policy Compliance API Reference](artifact/references/policy-detection.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, JSON API responses when requested, and concise text summaries of compliance results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ERIC_API_TOKEN and may process product images, titles, descriptions, image URLs, and feature-word settings through ERiC APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
