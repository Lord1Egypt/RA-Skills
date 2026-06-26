## Description: <br>
Helps agents maintain a local WeChat article asset library for product descriptions, product images, and .aws preset bundles, including controlled import of presets and related configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, brand teams, and design support roles use this skill to store product-specific business copy and images, then import .aws theme and preset bundles for WeChat article production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Importing a .aws preset bundle can add or overwrite repository-level credentials in aws.env. <br>
Mitigation: Review bundles before import, run --dry-run first, keep aws.env backups, and verify the intended keys and values before relying on imported credentials. <br>
Risk: Using --allow-any-host weakens the default host restriction for remote .aws bundles. <br>
Mitigation: Use the default aiworkskills.cn HTTPS allowlist for normal use and reserve --allow-any-host for fully trusted sources. <br>
Risk: Imported preset bundles can replace local preset directories and affect local article production settings. <br>
Mitigation: Inspect the bundle source and review diff output before accepting changes; use retained downloads, extraction output, and backups for audit or rollback. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aiworkskills/aws-wechat-article-assets) <br>
- [Publisher profile](https://clawhub.ai/user/aiworkskills) <br>
- [Artifact-declared homepage](https://aiworkskills.cn) <br>
- [Artifact-declared project URL](https://github.com/aiworkskills/wechat-article-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes product material, image descriptions, presets, downloads, and temporary extraction files under .aws-article/; .aws imports may update the root aws.env.] <br>

## Skill Version(s): <br>
1.0.24 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
