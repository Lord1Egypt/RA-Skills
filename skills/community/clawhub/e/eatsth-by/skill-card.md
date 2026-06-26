## Description: <br>
Personal healthy eating assistant that records health notes and food inventory, then recommends meals using existing items and flags items nearing expiration; health-record features are limited to the main session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BiyaoShang](https://clawhub.ai/user/BiyaoShang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individual users use this skill to maintain local health and diet notes, track food inventory, ask about those records, and receive personalized meal recommendations that account for health constraints and available foods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health notes and food inventory may be stored in local plaintext Markdown files. <br>
Mitigation: Install only if local plaintext storage is acceptable; review or delete those files when the information should no longer be retained, and avoid storing medical details that other local tools or users should not access. <br>
Risk: Meal recommendations can be inappropriate if health records or inventory details are incomplete or outdated. <br>
Mitigation: Keep records current and review recommendations before acting, especially for allergies, symptoms, medical restrictions, or expiring foods. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BiyaoShang/eatsth-by) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Natural-language responses and local Markdown records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown files for health notes and food inventory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
