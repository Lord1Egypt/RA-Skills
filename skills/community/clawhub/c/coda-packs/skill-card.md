## Description: <br>
Manage Coda Packs via REST API v1 for listing, creating, updating metadata, and deleting private Packs with CODA_API_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x7466](https://clawhub.ai/user/0x7466) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Coda Pack maintainers use this skill to manage private Pack shells through Coda's REST API before using the Pack SDK CLI for builds, uploads, gallery release, analytics, or collaborator workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete private Coda Packs when run with a valid Coda API token. <br>
Mitigation: Use the least-privileged token available, keep it in CODA_API_TOKEN rather than command arguments, and verify Pack IDs before update or delete operations. <br>
Risk: Deleting a Pack can be irreversible, especially when --force bypasses confirmation. <br>
Mitigation: Avoid --force unless deletion was explicitly approved and confirm the Pack name, ID, and installation count before proceeding. <br>
Risk: The --readme option is treated as inline README text by the artifact behavior. <br>
Mitigation: Pass intended README content directly or fix the skill before assuming --readme reads from a file path. <br>


## Reference(s): <br>
- [Coda Skill Page](https://clawhub.ai/0x7466/coda-packs) <br>
- [Coda API v1 Documentation](https://coda.io/developers/apis/v1) <br>
- [Coda Pack SDK Guides](https://coda.io/packs/build/latest/guides/overview/) <br>
- [Coda Pack SDK Quickstart](https://coda.io/packs/build/latest/guides/quickstart/) <br>
- [Coda Pack SDK on npm](https://www.npmjs.com/package/@codahq/packs-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and Python CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Coda REST API calls that list, create, update, or delete private Packs when run with a Coda API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
