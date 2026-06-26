## Description: <br>
Helps agents assess W-2 vs 1099 classification, joint-employer, COI, injury-liability, and wage/hour compliance risks for temporary event staffing in the US and Canada. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kissmyabs32](https://clawhub.ai/user/kissmyabs32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and event operations teams use this skill to review temporary event staffing plans for worker classification, insurance, joint-employer, injury-liability, and wage/hour exposure. It is intended for event staffing questions in the United States and Canada, not permanent employment or other markets. <br>

### Deployment Geography for Use: <br>
United States and Canada <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat general compliance guidance as legal advice. <br>
Mitigation: State that outputs are informational and direct users to employment counsel for binding determinations. <br>
Risk: Using live state compliance lookup sends relevant event and state details to TempGuru. <br>
Mitigation: Use the MCP lookup only when the user expects live compliance data for the event jurisdiction. <br>
Risk: The optional quote-requesting capability can initiate vendor contact. <br>
Mitigation: Invoke quote requests only when the user clearly intends to contact the vendor. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kissmyabs32/event-staffing-compliance) <br>
- [TempGuru MCP Server](https://mcp.tempguru.co/mcp) <br>
- [W-2 vs 1099 for Event Workers](https://tempguru.co/risk-briefs/w2-vs-1099-event-workers) <br>
- [What Compliant Staffing Means](https://tempguru.co/risk-briefs/what-is-compliant-staffing) <br>
- [Joint-Employer Liability](https://tempguru.co/risk-briefs/joint-employer-liability-event-staffing) <br>
- [COI Requirements](https://tempguru.co/risk-briefs/coi-event-staffing) <br>
- [Wage/Hour Compliance](https://tempguru.co/risk-briefs/wage-hour-compliance-event-staffing) <br>
- [Event Worker Injury Liability](https://tempguru.co/risk-briefs/event-worker-injury-liability) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API calls] <br>
**Output Format:** [Markdown or plain text guidance, optionally informed by MCP lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides general compliance information, not legal advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
