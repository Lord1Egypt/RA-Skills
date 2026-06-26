## Description: <br>
Use the included Brickset CLI for LEGO set search, details, images, instructions, reviews, login, user hash, collection, wishlist, and notes with guarded account writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musketyr](https://clawhub.ai/user/musketyr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External LEGO hobbyists, collectors, and agent builders use this skill to query Brickset for set metadata, images, instructions, and community reviews, and to manage Brickset collection, wishlist, rating, quantity, and note workflows when credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill can send Brickset credentials to a configurable server. <br>
Mitigation: Keep BRICKSET_BASE_URL unset or limited to https://brickset.com/api/v3.asmx, and avoid --base-url unless the endpoint is fully trusted. <br>
Risk: The skill uses Brickset API keys, user hashes, and optional username/password credentials. <br>
Mitigation: Store credentials in environment variables or an approved secret store, prefer BRICKSET_USER_HASH over username/password, and never print, commit, or paste real secrets. <br>
Risk: The skill can make live Brickset collection, wishlist, rating, quantity, or note changes. <br>
Mitigation: Use --dry-run first and require explicit confirmation of the exact Brickset account change before running a mutating command with --yes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/musketyr/afol-brickset) <br>
- [Brickset OpenAPI reference](references/openapi/brickset.yaml) <br>
- [Brickset public prompt guidance](references/prompts/brickset-tools.txt) <br>
- [Brickset private prompt guidance](references/prompts/brickset-private-tools.txt) <br>
- [Brickset API documentation](https://brickset.com/article/52664/api-version-3-documentation) <br>
- [Brickset API key request](https://brickset.com/tools/webservices/requestkey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from the Brickset CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Brickset API credentials for live calls and a Brickset user hash for private account reads or writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
