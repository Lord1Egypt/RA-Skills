## Description: <br>
Automates PubMed literature retrieval and Feishu Bitable literature database creation or updates, including paper metadata, Chinese translations, impact factors, and formatted references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenruao](https://clawhub.ai/user/chenruao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, and assistants use this skill to build or supplement Feishu Bitable literature databases from PubMed search results. It is intended for workflows that need structured paper metadata, Chinese title and abstract translations, journal impact data, and GB/T 7714-2015 references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Feishu Bitable records and grant the requester full table access. <br>
Mitigation: Before running it, confirm the target Feishu table or folder, search topic, number of papers, and whether full_access should be granted; use it only with Feishu tables the user controls. <br>
Risk: Generated literature records may contain incomplete metadata, stale journal impact data, or translation issues. <br>
Mitigation: Review the populated records, especially abstracts, impact factors, journal partitions, and formatted references, before relying on the database. <br>


## Reference(s): <br>
- [Field Mapping Reference](artifact/references/field_mapping.md) <br>
- [Impact Factors and Journal Partitions](artifact/references/impact_factors.md) <br>
- [PubMed E-utilities ESearch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi) <br>
- [PubMed E-utilities EFetch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi) <br>
- [ClawHub Skill Page](https://clawhub.ai/chenruao/feishu-literature-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Feishu Bitable API operations that create fields, add records, and grant table permissions.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
