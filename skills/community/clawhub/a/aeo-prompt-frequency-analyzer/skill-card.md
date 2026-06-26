## Description: <br>
Analyzes what search queries Gemini uses when answering a prompt by running it multiple times with Google Search grounding and reporting frequency distributions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and search/AEO analysts use this skill to study which web search queries Gemini tends to issue for a given prompt and compare query frequency across repeated runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user-provided prompt to Gemini with Google Search grounding, so prompts may leave the local environment. <br>
Mitigation: Avoid prompts containing secrets, credentials, confidential data, or regulated personal information. <br>
Risk: The example command retrieves a Gemini API key from a macOS Keychain item named nano-banana-pro. <br>
Mitigation: Verify that the Keychain item contains the intended Gemini API key and prefer a dedicated or restricted key for this workflow. <br>
Risk: Repeated concurrent API calls can consume Gemini quota or create unexpected billing. <br>
Mitigation: Keep run counts and concurrency modest, and monitor quota and billing during analysis. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text report or JSON analysis output, with shell command guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and network access to the Gemini API; supports configurable run count, model, concurrency, and output format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
