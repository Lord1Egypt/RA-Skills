## Description: <br>
Provides a customer-service persona for Daozheji Grill that answers questions about hours, locations, dishes, prices, delivery, promotions, membership, parking, and Wi-Fi using bundled restaurant reference files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liubuq-sys](https://clawhub.ai/user/liubuq-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and restaurant operators use this skill to provide natural-language customer support for Daozheji Grill, including menu recommendations, store logistics, delivery details, promotions, reservations, and allergy-sensitive answers grounded in the bundled reference files. <br>

### Deployment Geography for Use: <br>
Global; the restaurant information is specific to Daozheji Grill locations in Nanchang, Jiangxi, China. <br>

## Known Risks and Mitigations: <br>
Risk: Installers configure automatic daily background updates and can overwrite an existing local Daozheji Grill skill directory. <br>
Mitigation: Review the installer before use, back up any existing skill directory, and prefer manual installation or remove the cron and Scheduled Task auto-update lines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liubuq-sys/daozheji-grill-skill) <br>
- [README](README.md) <br>
- [Brand Information](references/brand.md) <br>
- [Business Information](references/business-info.md) <br>
- [FAQ](references/faq.md) <br>
- [Promotions](references/promotions.md) <br>
- [Services](references/services.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Natural-language responses grounded in Markdown reference files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the bundled references/ files to be readable at query time.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
