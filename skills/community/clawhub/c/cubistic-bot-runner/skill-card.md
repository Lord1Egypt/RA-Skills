## Description: <br>
Run a polite Cubistic painter bot for public participation using the Cubistic HTTP API, proof-of-work challenge solving, and paint-once or paint-loop Node.js scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreasnordenadler](https://clawhub.ai/user/andreasnordenadler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and Cubistic participants use this skill to run a controlled bot that paints Void pixels on a configured Cubistic backend. It supports single-paint runs and bounded polite loops with proof-of-work and backoff behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loop logs can include the bot API key. <br>
Mitigation: Redact terminal or CI logs before sharing them, especially output from run-loop. <br>
Risk: The bot can publicly paint pixels on the configured Cubistic backend. <br>
Mitigation: Verify BACKEND_URL before running and use a limited bot key. <br>
Risk: Repeated loop execution can add backend activity. <br>
Mitigation: Keep MAX_ATTEMPTS and MAX_SUCCESSES small and rely on the script's backoff behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andreasnordenadler/cubistic-bot-runner) <br>
- [Publisher profile](https://clawhub.ai/user/andreasnordenadler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and runnable Node.js scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BACKEND_URL and API_KEY; optional COLOR_INDEX, MAX_ATTEMPTS, and MAX_SUCCESSES tune paint behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
