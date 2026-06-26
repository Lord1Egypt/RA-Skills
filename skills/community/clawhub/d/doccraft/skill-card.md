## Description: <br>
Create source-grounded professional documents from existing materials, outlines, or templates, then generate, edit, review, or redline final Word documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bloom-u](https://clawhub.ai/user/Bloom-u) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external contributors, and developers use Doccraft to turn PDFs, DOCX, TXT, Markdown, templates, outlines, and mixed project sources into formal proposals, technical plans, implementation schemes, reports, and review-ready Word deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with local source materials and Word documents, which can expose sensitive files or alter important deliverables. <br>
Mitigation: Use a narrow project folder, work from copies of important files, and keep working drafts separate from final deliverables. <br>
Risk: Unfamiliar DOCX, PPTX, or XLSX files may carry document-processing risks when unpacked or validated. <br>
Mitigation: Isolate unfamiliar office files before processing them and keep document-processing tools updated. <br>
Risk: An untrusted SGDB_DOCX_MODULE value could change which Node docx module is loaded for Word generation. <br>
Mitigation: Use only trusted module paths or workspace dependencies when generating DOCX files. <br>
Risk: Source-grounded drafting can still introduce unsupported or misleading claims if source gaps are ignored. <br>
Mitigation: Build a source manifest, draft against section briefs, and run the consistency review before final delivery. <br>


## Reference(s): <br>
- [Doccraft ClawHub Skill Page](https://clawhub.ai/Bloom-u/doccraft) <br>
- [Doccraft Publisher Profile](https://clawhub.ai/user/Bloom-u) <br>
- [Source Manifest](references/source-manifest.md) <br>
- [Section Briefs](references/section-briefs.md) <br>
- [Drafting Rules](references/drafting-rules.md) <br>
- [Consistency Review](references/consistency-review.md) <br>
- [Word Format Profile](references/word-format-profile.md) <br>
- [Word Delivery Brief](references/word-delivery-brief.md) <br>
- [Word Assembly Plan](references/word-assembly-plan.md) <br>
- [DOCX JavaScript Workflow](docx-js.md) <br>
- [OOXML Editing Workflow](ooxml.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, plain text, JSON working briefs, Python or JavaScript helper commands, and generated or edited DOCX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local working files such as source manifests, section briefs, format profiles, delivery briefs, merged Markdown drafts, review notes, ZIP packages, and DOCX artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
