## Description: <br>
FMTWiki supports operation and maintenance of an evidence-focused fecal microbiota transplantation knowledge base, including literature-backed content updates, PubMed validation, and quality review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical knowledge-base maintainers, developers, and medical reviewers use this skill to update FMTWiki content with source links, PubMed-backed citations, and Generator-to-Evaluator review before publishing medical entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real MiniMax or GLM API key placed in VITE_GLM_API_KEY for a public Vite frontend may be exposed to users. <br>
Mitigation: Route AI requests through a backend or secret store, restrict the key scope, and rotate keys before deployment. <br>
Risk: Medical knowledge-base updates could publish incorrect or misleading clinical content if automated outputs are accepted directly. <br>
Mitigation: Require human medical review and the documented Generator-to-Evaluator PubMed verification workflow before publishing content changes. <br>
Risk: Scheduled literature trackers may introduce unreviewed changes if enabled without maintainers monitoring their output. <br>
Mitigation: Run trackers under maintainer control and review generated reports before writing updates into knowledge-base data files. <br>


## Reference(s): <br>
- [FMTWiki ClawHub release](https://clawhub.ai/zmy1006-sudo/fmtwiki) <br>
- [FMTWiki deployment](https://pvphcoybalzc.space.minimaxi.com) <br>
- [MiniMax API documentation](https://www.minimaxi.com/document) <br>
- [PubMed PMID lookup](https://pubmed.ncbi.nlm.nih.gov/?term={PMID}) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript data edits, source-link requirements, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include medical-content update proposals and must be reviewed before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
