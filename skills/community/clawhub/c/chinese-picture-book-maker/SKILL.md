---
name: chinese-picture-book-maker
description: Use when turning any Chinese children's story, fable, classroom reading text, or original plot into a cute picture book for preschool or primary school readers, especially when the task needs age-appropriate rewriting, page-by-page storyboard captions, consistent character design, and image-generation prompts.
---

# Chinese Picture Book Maker

## Overview

Create a Chinese children's picture book from a source story. Adapt the language to the target age, split the story into visual page beats, define stable character anchors, and prepare prompts for coherent illustrations with short readable Chinese captions.

## Workflow

1. Identify the target audience, such as age 5, grade 1-2, or grade 3+. If absent, ask only when the choice materially changes the output; otherwise choose a reasonable default.
2. Extract the core story arc: beginning, discovery or problem, attempts, change, ending, and feeling.
3. Split the story into 5-8 pages. Keep one visible action or emotional moment per page.
4. Rewrite each page caption in Chinese for the target audience. Use short, vivid, child-friendly sentences.
5. Define recurring character anchors before image generation: color, body shape, accessories, expression, and any unique marks.
6. Generate a coherent picture set. Use a grid storyboard for preview, or one image per page when the user wants printable pages.
7. Verify scene order, caption readability, character consistency, and age suitability.

## Reading Level Guide

| Audience | Caption Style | Typical Length |
| --- | --- | --- |
| Age 4-5 | Simple phrases, concrete nouns, repeated rhythm | 5-12 Chinese characters |
| Grade 1-2 | Short complete sentences, vivid verbs, sound words | 12-24 Chinese characters |
| Grade 3+ | Richer description, simple emotion and cause-effect | 20-40 Chinese characters |

For grade 1-2, prefer lively words such as `摇呀摇`, `哗啦啦`, `蹦蹦跳跳`, `亮晶晶`, `甜甜`, `热闹`, `出发`, `帮忙`. Keep sentences easy to read aloud.

## Storyboard Rules

- Use 5-8 pages for most stories.
- Put only one main action in each page.
- Keep captions short enough to fit in a picture-book caption area.
- Preserve the story's main lesson or feeling, but remove repetitive or confusing details.
- If the source story has many events, combine nearby actions into one visual beat.
- If the source story is very short, expand through setting, action, reaction, and ending.

## Character Anchor Template

Write anchors before image prompts:

```text
Main characters, keep consistent in every panel:
1) <Name>: <color>, <body shape>, <face/expression>, <accessory>, <personality cue>.
2) <Name>: <color>, <body shape>, <face/expression>, <accessory>, <personality cue>.
Important object: <shape>, <color/markings>, <how it changes or is used>.
```

Repeat these anchors in every image prompt so separate pages look like one book.

## Caption Style

Prefer:

- Concrete action: `小兔举起红伞，轻轻跳过水坑。`
- Sound and rhythm: `哗啦啦，下雨了！`
- Child-sized emotion: `大家笑眯眯地说：“太棒啦！”`

Avoid:

- Long explanations.
- Abstract morals inside the image text.
- Many names in one caption.
- Text that repeats every detail already visible in the picture.

## Image Prompt Pattern

Use this prompt shape with the image generation tool:

```text
Use case: illustration-story
Asset type: children's picture book page set
Primary request: Create a cute, lively Chinese children's picture book based on "<story title>" for <target readers>. Make <page count> coherent panels/pages. Each panel includes short Chinese text suitable for <target readers>.

Main characters, keep consistent in every panel:
<character anchors>

Style/medium: adorable children's book illustration, soft watercolor + colored pencil texture, rounded shapes, bright colors, expressive faces, clear storytelling, no clutter.

Layout and text:
<page-by-page scene and exact caption list>

Composition/framing: rounded picture-book borders, clear story order, consistent character designs, captions in a light caption area without covering characters.
Constraints: Chinese text exactly as listed; no extra words; no watermark; no logo; no photorealism; child-friendly expressions.
```

## Example

If the user provides the story `神奇的鸡蛋壳`, use `references/magical-eggshell-grade-2-example.md` as an optional example of page splitting, captions, and character anchors. Do not treat it as the default story for unrelated tasks.

## Common Mistakes

- Do not make the skill about one fixed story; extract a fresh storyboard from the user's story each time.
- Do not keep the original story as long paragraphs; picture books need one visual beat per page.
- Do not change character colors or accessories between pages.
- Do not put too much text inside generated images.
- Do not make tense scenes frightening for young children; show safety, warmth, and resolution.
