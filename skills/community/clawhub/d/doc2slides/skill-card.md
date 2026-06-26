## Description: <br>
Doc2slides converts PDF, Word, and Markdown documents into designer-grade PPTX slide decks with auto-layout, built-in charts, and optional LLM-assisted analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifei68801](https://clawhub.ai/user/lifei68801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn documents or prepared slide outlines into PPTX presentations for reports, training, pitches, academic presentations, and technical sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document text may be processed by configured external AI providers despite local-first positioning. <br>
Mitigation: Verify model configuration before using confidential documents, avoid setting API keys unless external processing is intended, and prefer JSON/template-only or truly local endpoint modes when needed. <br>
Risk: Setup installs packages and generated HTML may be rendered in a browser. <br>
Mitigation: Review setup steps before installation, run in a controlled environment, and render only trusted local/generated HTML. <br>
Risk: The workflow modifies local files while producing presentations and intermediate artifacts. <br>
Mitigation: Use an explicit output directory, keep source documents backed up, and inspect generated PPTX, preview, and validation files before sharing. <br>


## Reference(s): <br>
- [ClawHub Doc2slides Skill Page](https://clawhub.ai/lifei68801/doc2slides) <br>
- [Design Principles](artifact/references/design-principles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PPTX files with optional HTML slides, PNG previews, JSON work files, validation reports, and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local output and work files; optional LLM configuration can affect whether document text is processed by an external provider or local compatible endpoint.] <br>

## Skill Version(s): <br>
3.8.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
