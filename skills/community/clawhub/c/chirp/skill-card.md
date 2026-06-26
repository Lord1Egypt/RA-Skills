## Description: <br>
X/Twitter CLI using OpenClaw browser tool. Use when the user wants to interact with X/Twitter: reading timeline, posting tweets, liking, retweeting, replying, or searching. Alternative to bird CLI for environments without Homebrew. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zizi-cat](https://clawhub.ai/user/zizi-cat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Social media operators, developers, and agents use Chirp to read X/Twitter timelines and perform user-approved actions such as posting, liking, reposting, replying, searching, and following through an OpenClaw browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to perform public, account-changing X/Twitter actions such as posting, replying, reposting, liking, and following. <br>
Mitigation: Confirm the exact account, target, and content before allowing any public action. <br>
Risk: The skill operates through a logged-in browser session, which can expose the user's active social media account to unintended actions. <br>
Mitigation: Use a separate browser profile or test account when possible, and limit use to sessions where the operator expects X/Twitter control. <br>
Risk: Browser UI references and X/Twitter controls can change between snapshots or sessions. <br>
Mitigation: Take a fresh browser snapshot before each action and verify that the selected control still matches the intended action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zizi-cat/chirp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with browser tool command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw browser profile with an authenticated X/Twitter session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
