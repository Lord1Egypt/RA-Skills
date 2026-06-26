## Description: <br>
Baoyu Slide Deck generates professional slide deck images from content by creating outlines, style instructions, and individual slide images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nengnengZ](https://clawhub.ai/user/nengnengZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and developers use this skill to turn markdown or pasted content into shareable slide decks with selected styles, audience settings, language, and slide counts. It can produce slide images and merge them into PPTX or PDF exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and renames files under slide-deck output folders. <br>
Mitigation: Run it in a trusted workspace, review the target output directory, and use the documented existing-content checks before regenerating decks. <br>
Risk: Deck content and prompts may be used by an image-generation workflow. <br>
Mitigation: Use outline or prompt review for important decks, and avoid confidential content unless the image-generation service is approved for that data. <br>
Risk: PPTX and PDF export depends on merge scripts run through bun or npx. <br>
Mitigation: Verify the referenced runtime and merge script source before relying on exported PPTX or PDF files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nengnengZ/baoyu-slide-deck-2) <br>
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-slide-deck) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown workflow guidance with generated outline and prompt files, PNG slide images, and optional PPTX/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun or npx for export merge scripts; image generation can be skipped with outline-only, prompts-only, or images-only modes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence; artifact frontmatter reports 1.56.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
