## Description: <br>
Multi-hop evidence search and structured extraction over enterprise artifact datasets, with product grounding to reduce cross-product leakage and evidence pointers for returned entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and enterprise knowledge workers use this skill to delegate multi-hop retrieval across authorized documents, chats, meetings, pull requests, and URLs. It helps an agent return product-grounded employee IDs, document IDs, and supporting evidence pointers without loading large datasets into the main context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface employee or artifact identifiers from enterprise datasets if run over broad or unauthorized data. <br>
Mitigation: Keep the dataset root narrow, use only data the user is authorized to process, and review returned snippets or identifiers before sharing them. <br>
Risk: Incorrect product grounding or over-inclusive reviewer extraction can lead to wrong employee IDs or document IDs. <br>
Mitigation: Require product-grounded evidence pointers and reviewer-specific supporting snippets before relying on extracted results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wu-uk/enterprise-information-search-enterprise-artifact-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown with JSON-ready answer objects, evidence records, and recommendation labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes final extracted entities, an evidence map with artifact pointers, and a USE_EVIDENCE, NEED_MORE_SEARCH, or AMBIGUOUS recommendation.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
