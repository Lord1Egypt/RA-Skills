## Description: <br>
Doc Sync helps agents synchronize frontend project documentation with source-of-truth files such as package metadata, configuration, environment examples, routes, APIs, schemas, tests, CI, and deployment facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to keep README files, docs, ADRs, changelogs, setup and deploy notes, environment documentation, API and route descriptions, and multilingual documentation aligned with project facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation updates could misstate environment variables, API behavior, route behavior, deployment steps, or translated README content. <br>
Mitigation: Review generated documentation changes against source-of-truth files before committing, with extra attention to environment variables, APIs, deployment steps, and translations. <br>
Risk: Multi-entrypoint or multilingual documentation can drift if only one README or docs location is updated. <br>
Mitigation: Check all relevant README and docs entrypoints, list which language files were synchronized, and flag any files that need human translation or product-copy review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-doc-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown documentation edits, synchronization summaries, validation command lists, and human-review notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports synchronized documents, checked documentation entrypoints, validation results, old-terminology checks, and remaining manual review items.] <br>

## Skill Version(s): <br>
2.6.0 (source: server evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
