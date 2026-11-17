## Description:

FatSecret nutrition API integration for food search, nutritional lookup, barcode scanning, recipe search, and food diary logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-liva](https://clawhub.ai/user/f-liva)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to search FatSecret nutrition data, look up foods by barcode, retrieve recipes, and log meals to a FatSecret diary after user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted CLI input can execute Python through the shell wrapper.

Mitigation: Fix the CLI interpolation issue before use and avoid passing untrusted text to CLI commands until it is corrected.

Risk: FatSecret consumer credentials and long-lived OAuth1 tokens are stored locally and can expose account access.

Mitigation: Store credentials in a restricted config directory, avoid printing or returning token secrets, and revoke FatSecret app access when uninstalling or rotating credentials.

Risk: Diary logging can write to the user's FatSecret account.

Mitigation: Require explicit user confirmation before any diary write operation.

Risk: Dependencies are version-ranged rather than pinned.

Mitigation: Pin and review dependencies before deployment in a shared or production environment.

## Reference(s):

- [FatSecret skill page](https://clawhub.ai/f-liva/skills/fatsecret)
- [FatSecret API documentation](https://platform.fatsecret.com/docs)
- [FatSecret OAuth1 guide](https://platform.fatsecret.com/docs/guides/authentication/oauth1/three-legged)
- [Open Food Facts API](https://wiki.openfoodfacts.org/API)
- [FatSecret API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python examples, shell commands, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API-derived food, recipe, barcode, and diary logging results after FatSecret authentication.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
