## Description: <br>
Access Cookidoo (Thermomix) recipes, shopping lists, and meal planning via the unofficial cookidoo-api Python package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thekie](https://clawhub.ai/user/thekie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to access their Cookidoo recipes, meal planning information, account details, and shopping lists from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Cookidoo account credentials and can access account-linked recipe and list data. <br>
Mitigation: Install only if this account access is acceptable, and provide credentials through the shell or a secret manager rather than storing long-lived plaintext credentials. <br>
Risk: The skill depends on an unofficial Cookidoo API package that may stop working if Cookidoo changes its service behavior. <br>
Mitigation: Review command output before relying on it and update or pin the cookidoo-api dependency when compatibility changes. <br>
Risk: Shopping-list or meal-plan actions may affect a user's Cookidoo account if extended or automated by an agent workflow. <br>
Mitigation: Require explicit user review before allowing any workflow to modify shopping-list or meal-plan data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thekie/cookidoo) <br>
- [cookidoo-api on PyPI](https://pypi.org/project/cookidoo-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON from CLI commands, with Markdown guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Cookidoo account credentials and an active subscription; CLI options include --json and --limit.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json, server release metadata, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
