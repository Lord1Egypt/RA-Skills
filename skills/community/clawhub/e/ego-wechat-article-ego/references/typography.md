# Typography

Three inline treatments follow the caller's exported HTML of the default theme. The numbers were re-typed into `scripts/lib/pure.mjs`. This file does not contain theme source from the GPL editor.

## What this is not

`https://wechat.bmpi.dev/` is the visual reference the caller asked for. That site is the mdnice / TaleAi `markdown2html` line, which is GPL-3.0. This skill does not vendor that CSS, those theme files, or the hosted editor.

`doocs/md` (`https://github.com/doocs/md`, WTFPL) is the permissive project that documents the same paste path: Markdown to HTML, then inline styles, then paste into the editor. This skill does not depend on `@md/core`, juice, or a copy of their theme files. The implementation in `scripts/lib/pure.mjs` is original. The only borrowed fact is the widely known one: WeChat keeps inline `color` more reliably when a link's text is also wrapped in a `<span>` with the same color.

## What WeChat is asked to keep

- Figure: `margin:0; margin-top:10px; margin-bottom:10px`, column flex, centered. The image is `display:block; margin:0 auto; max-width:100%`. The caption is a `figcaption` with `margin-top:5px`, `padding:0`, `color:#888`, `font-size:14px`. It is not a body paragraph, so it does not get the paragraph's 8px vertical padding.
- Body paragraph: `font-size:16px; padding-top:8px; padding-bottom:8px; margin:0; line-height:26px; color:black`.
- Quote: `border-left:3px solid rgb(239,112,96)`, `background:#fff9f9`, `color:#6a737d`, `padding:10px 10px 10px 20px`, `margin:20px 0`. The inner paragraph stays black, 16px, line-height 26px, padding 8px 0, margin 0.
- Heading 2: `margin-top:30px; margin-bottom:15px; padding:0; font-size:1.3em; border-bottom:2px solid rgb(239,112,96)`. The words sit in a coral label (`background:rgb(239,112,96); color:#fff; padding:3px 10px 1px; border-top-left-radius:3px; border-top-right-radius:3px`). A following empty span draws the tail with `border-bottom:36px solid #efebe9; border-right:20px solid transparent`.
- Links: bold `#ef7060`, `text-decoration:none`, `border-bottom:1px solid #ef7060`, repeated on an inner span.
- After upload, the editor pass sets the caption's padding back to 0 and its top margin to 5px, and clears the image wrapper's bottom padding, because the Official Account editor may turn the caption into a padded paragraph.

Code stays a plain block. There is no syntax highlighter.

Images are still uploaded as files. The editor sizes them. A caption under an image is the italic line from the Markdown, not a burned-in picture.
