## Description: <br>
Scan Reddit for trending stocks and sentiment spikes using the ApeWisdom API (free). Use this to find "meme stocks", retail momentum, and sentiment shifts on r/wallstreetbets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stuhorsman](https://clawhub.ai/user/stuhorsman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch ApeWisdom Reddit ticker sentiment and identify high-mention or fast-rising symbols for further review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts ApeWisdom for live Reddit market-sentiment data. <br>
Mitigation: Install and run it only in environments where outbound requests to ApeWisdom are allowed. <br>
Risk: Ticker sentiment output can be volatile, incomplete, or mistaken for financial advice. <br>
Mitigation: Treat results as informational signals and verify decisions with independent analysis before acting. <br>
Risk: The script depends on the Python requests package being available. <br>
Mitigation: Prepare the runtime dependency before execution or run in an environment that already includes requests. <br>


## Reference(s): <br>
- [ApeWisdom API endpoint](https://apewisdom.io/api/v1.0/filter) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON printed to stdout, with Markdown usage guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound access to ApeWisdom and the Python requests package; results are live market-sentiment data and should be treated as informational.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
