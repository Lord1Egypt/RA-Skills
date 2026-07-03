## Description: <br>
Build and maintain AlphaGBM company research profiles generated from fundamentals, PE/PB band history, financial red flags, and event radar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders, investors, and agent developers use this skill to create, view, refresh, delete, and summarize AlphaGBM company research profiles for watchlists and PE/PB valuation-band checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an AlphaGBM API key to create, refresh, and archive saved company research profiles. <br>
Mitigation: Review and confirm profile creation, refresh, and deletion actions before allowing the agent to call AlphaGBM endpoints. <br>
Risk: Broad phrases such as knowledge base or research brain may trigger profile-management behavior. <br>
Mitigation: Confirm the requested ticker and action when user intent is ambiguous before creating, refreshing, or deleting profiles. <br>
Risk: The AlphaGBM API key provides access to saved company research profile operations. <br>
Mitigation: Store ALPHAGBM_API_KEY in approved secret storage and provide it only to trusted agent runtimes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clementgu/skills/alphagbm-company-profile) <br>
- [AlphaGBM](https://alphagbm.com) <br>
- [AlphaGBM API Base URL](https://alphagbm.zeabur.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries and tables with JSON API request and response examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ALPHAGBM_API_KEY to manage saved company profiles; profile creation can be limited by the user's AlphaGBM tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
