## Description: <br>
BNBot lets agents operate Twitter/X through a real browser session with CLI tools for posting, engagement, scraping, profiles, content fetching, articles, and job search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackleeio](https://clawhub.ai/user/jackleeio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use BNBot to let an agent manage Twitter/X workflows through the bnbot CLI and Chrome extension, including drafting, posting, engagement, scraping, account analytics, article publishing, and related content retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BNBot gives an agent broad control over a logged-in Twitter/X account, including posting, deleting, following, unfollowing, replying, retweeting, publishing articles, and scraping. <br>
Mitigation: Use a dedicated browser profile or test account and require explicit approval before account-changing actions. <br>
Risk: The skill depends on a local daemon and Chrome extension that operate through an authenticated browser session. <br>
Mitigation: Verify the npm package and Chrome extension permissions, confirm the extension connection before use, and stop the local daemon when finished. <br>
Risk: Media and content-fetching commands can process local files or external URLs. <br>
Mitigation: Avoid passing sensitive local files and review fetched or uploaded content before publishing. <br>


## Reference(s): <br>
- [BNBot ClawHub listing](https://clawhub.ai/jackleeio/bnbot) <br>
- [jackleeio publisher profile](https://clawhub.ai/user/jackleeio) <br>
- [bnbot-cli npm package](https://www.npmjs.com/package/bnbot-cli) <br>
- [BNBot Chrome extension](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; bnbot command results are JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the bnbot-cli binary, a running local daemon on port 18900, and a connected Chrome extension session.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
