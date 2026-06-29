## Description: <br>
Explains U.S. state-by-state consumer data privacy law using bundled, source-cited jurisdiction snapshots, including coverage thresholds, privacy-policy duties, consumer rights, opt-outs, enforcement, and private-right-of-action limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to understand U.S. state consumer privacy-law requirements from bundled practice notes. It is suited for general legal information, issue spotting, and pointing users to source-cited state law summaries, not for legal advice or a final compliance verdict on a user's specific facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The legal content is a dated snapshot and privacy law can change after the bundled review date. <br>
Mitigation: State the snapshot and last-reviewed dates, point users to the canonical source for currency checks, and avoid presenting the content as current legal advice. <br>
Risk: Users may ask whether their own business is compliant or must comply with a law. <br>
Mitigation: Explain thresholds and obligations at a general level, do not give a yes/no compliance verdict, and direct users to qualified privacy counsel for advice on their facts. <br>
Risk: Optional canonical-URL refreshes could expose user facts if the agent sends user-provided details upstream. <br>
Mitigation: Fetch only the fixed canonical URL after user approval and do not send private business facts, data inventories, or policies with the request. <br>
Risk: Server and artifact license evidence disagree. <br>
Mitigation: Use the server-resolved release license for this context and require human confirmation before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/data-privacy-law-explainer) <br>
- [OpenAgreements privacy-law index](https://openagreements.org/legal/privacy) <br>
- [Bundled jurisdiction manifest](artifact/manifest.json) <br>
- [Server-resolved provenance](unavailable) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown legal-information explanation with source citations and optional canonical-link refresh guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state the snapshot date, avoid legal-advice or compliance-verdict language, and cite bundled note sources when stating rules.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
