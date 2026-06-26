## Description: <br>
Download purchased tracks from Beatport using the openclaw headless browser tool (CDP). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esanle](https://clawhub.ai/user/esanle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to automate downloading already-purchased Beatport tracks through a Beatport-authenticated browser session. It helps manage Beatport library downloads, download queues, and local file saving through CDP-based browser control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle Beatport credentials, session cookies, access tokens, and browser downloads. <br>
Mitigation: Use a dedicated browser profile with no unrelated logged-in accounts, and avoid exposing or logging cookies, tokens, or passwords. <br>
Risk: The skill can perform bulk account actions against a Beatport-authenticated session. <br>
Mitigation: Confirm the exact tracks, queue state, and download folder before running bulk download actions. <br>
Risk: Security review marked the release suspicious because credential handling, browser downloads, and account actions have weak scoping. <br>
Mitigation: Install only after reviewing the skill behavior and run it only in a controlled browser session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/esanle/beatport-dl-with-browser-tool) <br>
- [Beatport account login](https://account.beatport.com/) <br>
- [Beatport library](https://www.beatport.com/library) <br>
- [Beatport library downloads](https://www.beatport.com/library/downloads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser automation guidance and helper commands for a local Beatport-authenticated CDP session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
