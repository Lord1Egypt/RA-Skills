## Description: <br>
Founder Video helps agents create Pexo founder videos by relaying a founder story, pitch, website text, or uploaded media to Pexo for scriptwriting, shot generation, model selection, music, and final delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders, solo builders, and small teams use this skill to turn a founder story, pitch, product description, website text, or uploaded media into a finished Pexo video for fundraising, Product Hunt, or personal brand content. Agents use the included shell scripts to create a project, upload assets, send the exact user request, poll status, relay Pexo choices or questions, and deliver the final asset URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Founder-video prompts, pasted website text, and uploaded media are sent to Pexo for processing. <br>
Mitigation: Submit only material acceptable under Pexo data-handling terms, and avoid secrets or regulated/confidential content unless that use is approved. <br>
Risk: The skill uses a local Pexo API key from ~/.pexo/config or environment variables. <br>
Mitigation: Store the config with restrictive permissions, do not commit or share the key, and rotate the key if it is exposed. <br>
Risk: Creating projects can consume Pexo credits and may require the user to add credits. <br>
Mitigation: Confirm the user wants to start or continue production, surface credit-balance or purchase links when returned, and do not buy credits on the user's behalf. <br>


## Reference(s): <br>
- [Pexo homepage](https://pexo.ai) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with shell command invocations, status updates, project links, and final asset URLs; helper scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL configuration plus curl, jq, and file; video generation is asynchronous and typically requires polling.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
