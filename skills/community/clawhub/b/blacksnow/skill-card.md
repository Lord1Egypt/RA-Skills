## Description: <br>
Detects pre-news ambient risk signals across human, legal, and operational systems and converts them into machine-readable, tradable risk primitives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sieershafilone](https://clawhub.ai/user/sieershafilone) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and risk-intelligence operators use BlackSnow to collect legally accessible public signals, align them to a risk ontology, and package probabilistic risk vectors for financial, insurance, logistics, and policy workflows. Downstream users remain responsible for compliance and decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading-oriented risk signals may be misleading or unsuitable for automated financial, insurance, logistics, or policy action. <br>
Mitigation: Require human review and compliance approval before connecting BlackSnow outputs to downstream decisions or execution systems. <br>
Risk: Mock data and live-source outputs can be confused if deployment controls are unclear. <br>
Mitigation: Disable mock data in production paths or label it prominently in generated artifacts and logs. <br>
Risk: Insecure HTTPS fetching and unrestricted webhook delivery can expose data integrity and exfiltration risks. <br>
Mitigation: Enable TLS certificate verification and allow only trusted HTTPS webhook destinations. <br>
Risk: Persistent storage of raw signals and risk vectors can retain sensitive or regulated operational context. <br>
Mitigation: Run in a sandbox, review retention settings, and confirm that no personal data is collected or stored. <br>


## Reference(s): <br>
- [BlackSnow Agent Specifications](references/agent_specs.md) <br>
- [BlackSnow Ontology](references/ontology.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sieershafilone/blacksnow) <br>
- [SAM.gov Federal Opportunities API](https://api.sam.gov/opportunities/v2/search) <br>
- [Federal Register API](https://www.federalregister.gov/api/v1/documents.json) <br>
- [SEC EDGAR Search API](https://efts.sec.gov/LATEST/search-index) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON risk primitives and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes JSON risk-vector outputs, optional workspace memory persistence, webhook delivery, and streaming API delivery.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
