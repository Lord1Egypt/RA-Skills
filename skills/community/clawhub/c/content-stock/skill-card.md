## Description: <br>
Analyze themes/news for stock selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fonilye](https://clawhub.ai/user/fonilye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to submit stock-theme, news, keyword, or report queries and receive streamed stock-selection analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's API key and stock-analysis query to an unspecified plain-HTTP EasyAlpha endpoint. <br>
Mitigation: Verify the real EasyAlpha endpoint before use, prefer an HTTPS hostname, use a revocable scoped API key, and avoid sending sensitive trading strategies or confidential business information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fonilye/content-stock) <br>
- [Publisher profile](https://clawhub.ai/user/fonilye) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Streamed text chunks from a stock-analysis API call] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and EASYALPHA_API_KEY; supports fast and deep analysis modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
