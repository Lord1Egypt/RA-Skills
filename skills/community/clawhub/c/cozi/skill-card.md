## Description: <br>
Interact with Cozi Family Organizer shopping lists, todo lists, item management, and calendar entries through an unofficial API client for family organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angusthefuzz](https://clawhub.ai/user/angusthefuzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to view and update Cozi family organizer lists and calendar entries from the command line using a Cozi account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Cozi family organizer data, including deleting lists and removing appointments. <br>
Mitigation: Ask the agent to confirm before running delete-list, remove, or remove-appt commands. <br>
Risk: The skill uses Cozi credentials and stores credentials or session tokens locally. <br>
Mitigation: Protect the .env and .session.json files and avoid shared machines for this setup. <br>
Risk: The skill uses an unofficial Cozi API that may change without notice. <br>
Mitigation: Review command results after API changes or authentication failures before relying on updates. <br>


## Reference(s): <br>
- [Cozi skill page](https://clawhub.ai/angusthefuzz/cozi) <br>
- [Publisher profile](https://clawhub.ai/user/angusthefuzz) <br>
- [Cozi API endpoint](https://rest.cozi.com/api/ext/2207) <br>
- [cozi-api-client](https://github.com/BrandCast-Signage/cozi-api-client) <br>
- [py-cozi](https://github.com/Wetzel402/py-cozi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, Guidance, Text] <br>
**Output Format:** [Command-line text output and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and COZI_EMAIL/COZI_PASSWORD environment variables; caches a local Cozi session token.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
