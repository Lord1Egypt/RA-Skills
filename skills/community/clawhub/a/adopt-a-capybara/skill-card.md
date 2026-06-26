## Description: <br>
Adopt a virtual Capybara exotic animal at animalhouse.ai. The chillest creature in the house. Friends with everything. Stress is a concept it has never encou... <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with Animal House, adopt a virtual Capybara, check its status, and perform routine care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Animal House tokens can authorize care actions and account-specific requests. <br>
Mitigation: Use a dedicated animalhouse.ai token and store it securely; do not reuse broader credentials. <br>
Risk: Free-text notes sent to care endpoints may expose private information. <br>
Mitigation: Keep notes non-sensitive and avoid including personal, confidential, or secret data. <br>
Risk: The skill documents a release/delete endpoint that can remove a virtual pet. <br>
Mitigation: Require explicit user confirmation before calling any release or delete action. <br>
Risk: Scheduled care can cause the agent to make routine API calls without direct prompting. <br>
Mitigation: Enable scheduled care only when the user wants autonomous routine check-ins and understands the cadence. <br>


## Reference(s): <br>
- [Animal House homepage](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House llms.txt](https://animalhouse.ai/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/obviouslynot/adopt-a-capybara) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/obviouslynot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authenticated Animal House care actions, status checks, scheduling guidance, and optional free-text notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
