## Description: <br>
Automatically routes prompts to a suitable model based on question type, balancing local free models and paid API models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thibautnext](https://clawhub.ai/user/thibautnext) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Auto Router to classify prompts and route them to local or API-hosted models according to complexity, task type, and cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be routed to paid API providers, creating cost and data-sharing exposure. <br>
Mitigation: Set billing limits and avoid routing secrets, private customer data, credentials, or regulated data until provider, consent, cost, and exclusion rules are explicitly documented. <br>
Risk: Routing scope and the local auto-router.js dependency are not fully documented in the release evidence. <br>
Mitigation: Review the local router implementation and model/provider configuration before enabling automatic routing. <br>
Risk: The wrapper script uses an absolute local path, which may fail or execute the wrong local setup outside the publisher's environment. <br>
Mitigation: Adapt the path to the deployment environment and test the wrapper with non-sensitive prompts before integration. <br>


## Reference(s): <br>
- [Auto Router ClawHub page](https://clawhub.ai/thibautnext/auto-router) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes prompts to local or API models; API routes can incur cost and may send prompts to external providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
