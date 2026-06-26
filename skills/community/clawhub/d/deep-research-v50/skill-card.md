## Description: <br>
Guides agents through sourced deep research by extracting structured source cards, scoring evidence quality, synthesizing thematic briefs, and producing reports that separate verified conclusions from pending leads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueylee-dotcom](https://clawhub.ai/user/xueylee-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and strategy teams use this skill to gather evidence, create quality-scored source cards, identify contradictions, and produce narrative research reports with clear sourcing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled synthesis script can generate fixed medical and insurance conclusions that appear sourced but are not derived from the user's inputs. <br>
Mitigation: Do not rely on scripts/synthesize.sh for real analysis unless it is rewritten to derive outputs from verified source cards and pass citation validation. <br>
Risk: Private PDFs or extracted article text may remain in temporary files during research extraction workflows. <br>
Mitigation: Avoid private PDFs unless temporary-file handling is reviewed, and remove extracted intermediates after use. <br>
Risk: Unsafe card IDs or path characters could affect generated file paths. <br>
Mitigation: Use simple card IDs without path separators and review generated paths before running helper scripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xueylee-dotcom/deep-research-v50) <br>
- [PubMed](https://pubmed.ncbi.nlm.nih.gov) <br>
- [OpenAlex API](https://api.openalex.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown research reports, source cards, thematic briefs, and command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes quality scoring and sourcing checks; final reports should separate verified conclusions from pending leads.] <br>

## Skill Version(s): <br>
5.0.1 (source: server release evidence and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
