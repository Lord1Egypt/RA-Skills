# AI PPT Designer
### 千题千境 · Custom AI PPTX Generator

**Create custom, content-driven PowerPoint presentations — not template-based slides.**

AI PPT Designer turns your notes, documents, emails, spreadsheets, images, or ideas into a professionally structured and visually designed PowerPoint presentation.

Instead of simply converting text into slides or repeatedly applying a fixed template, it first understands the content, audience, and communication goal, then develops a visual direction that fits the topic.

You stay in control of the important design decisions. The workflow lets you review the structure, storyboard, and visual preview before the final PPTX is built.

The final deliverable is a **native, editable PowerPoint (.pptx)** — not a collection of full-page images.

> **Content determines Design.**
>
> **千题千境 · Every topic, a different design.**

## What it can do

- Turn ideas, notes, documents, emails, tables, and images into presentations
- Analyze content and build a clear presentation structure
- Propose a topic-specific visual direction
- Create an ASCII storyboard for page-by-page review
- Generate a visual prototype before the final PPTX
- Produce native, editable PowerPoint slides
- Preserve source facts, numbers, wording, and user-approved content
- Perform visual and technical checks before delivery

## Typical users

Useful for anyone who regularly needs presentations but does not want to design every slide from scratch:

- HR / People & Culture
- Consultants
- Trainers / L&D
- Project managers
- Sales & marketing teams
- Business managers
- Teachers and students
- Founders and small teams

## Supported input

You can start with:

- Text or prompts
- Word / DOCX
- PDF
- PowerPoint / PPTX
- Email / EML
- Images
- Excel / spreadsheets
- Logos, icons, photos, and other user-provided assets

## How it works

1. **Understand the content** — extract the key messages, facts, numbers, structure, and audience.
2. **Plan the presentation** — turn the source material into a logical slide structure.
3. **Create a storyboard** — define the content and visual role of every slide before production.
4. **Preview the design** — create a near-final visual preview for review.
5. **Build the PPTX** — recreate the approved design as native, editable PowerPoint objects.
6. **Check and deliver** — validate the result and provide the final presentation and supporting renders.

The workflow includes user approval at the key structure, storyboard, and visual-preview stages.

## What makes it different

### Content-driven design

The Skill does not rely on a fixed page-template library as its core approach.

A process may work best as a journey or flow. A comparison may work best as a visual contrast. A data-heavy topic may need data visualization. A people-focused story may benefit from human-centered visuals.

The visual expression changes with the content.

### Native editable PPTX

The final presentation is rebuilt with native PowerPoint text boxes, shapes, and other editable objects whenever practical.

### Human-in-the-loop

You approve the important design direction before the final presentation is built.

### Content integrity

The original source material and approved storyboard remain the content source of truth. Visual-generation tools must not silently change important facts, numbers, labels, or wording.

### Visual variety

The Skill reuses design principles and production techniques — not the same page layouts over and over again.

## Workflow at a glance

```text
Your content + assets
        ↓
Content analysis
        ↓
Design intent
        ↓
Structure review
        ↓
ASCII storyboard review
        ↓
Visual prototype review
        ↓
Native editable PPTX
        ↓
Visual & technical QA
        ↓
Final presentation
```

If a generated visual does not meet expectations, the workflow can switch to a prompt-delivery fallback instead of repeatedly generating images.

## Install

Copy the `custom-ai-pptx-generator/` folder into your Skill directory and reload the application.

Typical locations:

- WorkBuddy: `~/.workbuddy/skills/custom-ai-pptx-generator/`
- CodeBuddy: `~/.codebuddy/skills/custom-ai-pptx-generator/`

## Requirements

| Component | Purpose |
|---|---|
| Python 3.10+ and `python-pptx` | Native PPTX generation |
| Windows desktop PowerPoint | Visual rendering and QA |
| Optional image-generation tool / API | Visual prototypes and image assets |

## License

MIT
