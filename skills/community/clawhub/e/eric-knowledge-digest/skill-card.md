## Description:

Converts textbooks or PDFs into personalized, multimodal interactive learning materials including handwritten notes, quiz webpages, slides, audio courses, and mind maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericn26-star](https://clawhub.ai/user/ericn26-star)

### License/Terms of Use:

MIT-0

## Use Case:

External learners, educators, and developers can use this skill to convert PDFs, textbooks, or topic descriptions into grade-adapted study materials such as notes, quizzes, slides, mind maps, and audio lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded documents may contain private or sensitive material that the skill will parse and transform into study assets.

Mitigation: Use the skill only with documents intended for learning-material generation, and avoid unrelated private documents.

Risk: Topic-only requests may use searched educational material before downstream study assets are generated.

Mitigation: Review and confirm compiled source material before proceeding with generated notes, quizzes, slides, mind maps, or audio.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericn26-star/skills/eric-knowledge-digest)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown deliver_assets block containing local file paths for PDFs, PPTX, HTML, PNG, MP3, and optional Mermaid text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final assets are returned as file paths only; previews, autoplay, and intermediate files are avoided.]

## Skill Version(s):

11.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
