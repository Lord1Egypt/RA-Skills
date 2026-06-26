## Description: <br>
AEO Keyword Selector helps an agent select one question-format SEO/AEO blog keyword from a business topic after checking sitemap coverage, fetched page intent, and Semrush validation for cannibalization risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coreydomidocs-droid](https://clawhub.ai/user/coreydomidocs-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content strategists, SEO operators, and agentic writing workflows use this skill before drafting a blog post to decide whether a business topic should become a new URL, an expansion of an existing page, or no new content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sitemap parsing and page checks can use network or file inputs outside the intended scope. <br>
Mitigation: Run the sitemap parser only on trusted HTTPS sitemaps or known workspace XML files, and keep any output path inside the workspace. <br>
Risk: An unchecked keyword decision can send a writing workflow toward duplicate, cannibalizing, or strategically weak content. <br>
Mitigation: Review important content-strategy decisions before handing the selected keyword to a writing or publishing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coreydomidocs-droid/aeo-keyword-selector) <br>
- [DomiDocs profile](artifact/references/domidocs-profile.md) <br>
- [Semrush playbook](artifact/references/semrush-playbook.md) <br>
- [Verdict rubric](artifact/references/verdict-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Plain text decision block with key-value fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exactly one keyword decision: new-url, expand-existing, or no-go.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
