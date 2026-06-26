## Description: <br>
FatSecret nutrition API integration for food search, nutritional lookup, barcode scanning, recipe search, and food diary logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f-liva](https://clawhub.ai/user/f-liva) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to look up FatSecret nutrition data, search recipes, check barcodes, and log meals to a FatSecret diary through guided commands and helper code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed credential handling and local storage of credentials and tokens. <br>
Mitigation: Install only when comfortable granting FatSecret account access, treat config and token files as secrets, and avoid shared or logged environments. <br>
Risk: The security review notes third-party data-flow concerns involving FatSecret and possible Open Food Facts lookups. <br>
Mitigation: Verify which external services receive lookups before using the skill with sensitive diet, barcode, or diary data. <br>
Risk: The security guidance recommends a patched version for token printing, OAuth documentation, config directory validation, and external service disclosure. <br>
Mitigation: Prefer an updated release that addresses those items before deploying the skill in routine workflows. <br>


## Reference(s): <br>
- [FatSecret API Reference](references/api.md) <br>
- [FatSecret Platform](https://platform.fatsecret.com) <br>
- [FatSecret API Documentation](https://platform.fatsecret.com/docs) <br>
- [FatSecret OAuth1 Authentication Guide](https://platform.fatsecret.com/docs/guides/authentication/oauth1/three-legged) <br>
- [Open Food Facts API](https://wiki.openfoodfacts.org/API) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python helper code, and JSON-style configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FatSecret API credentials for core features; diary logging requires user authorization and stores local tokens.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
