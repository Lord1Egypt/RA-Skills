# Word Format Profile

Use this reference when the output is a formal Word deliverable.

## Format authority order

Resolve the document format in this order:

1. User-provided template file such as `.docx` or `.dotx`
2. Explicit written formatting requirements from the user
3. An accepted sample document in the same domain
4. The default profile in this file

If higher-priority sources conflict, stop and ask the user to confirm which one wins.

## When to confirm with the user

Ask for confirmation before final Word delivery when:

- The user did not provide a template
- The format affects an external or formal deliverable
- Multiple signals conflict
- The current document must match an institutional style closely

Do not force confirmation before text drafting when the task is still in the planning or Markdown stage. Text generation can proceed with the default profile recorded as a working assumption.

## Default profile

Use this as the generic default for formal Chinese long-form documents, especially bids, implementation plans, and project schemes.

### Page setup

- Paper: A4, portrait
- Margins: top 2.5 cm, bottom 2.5 cm, left 3.0 cm, right 2.5 cm
- Default paragraph alignment: justified
- First-line indent: 2 characters
- Paragraph spacing: before 0 pt, after 0 pt
- Default line spacing: exact 28 pt

### Fonts and heading levels

- Body: `FangSong_GB2312`, size 16 pt, black
- Heading 1: `SimHei`, size 16 pt, bold
- Heading 2: `KaiTi_GB2312`, size 16 pt, bold
- Heading 3: `FangSong_GB2312`, size 16 pt, bold
- Heading 4: `FangSong_GB2312`, size 16 pt, regular, line spacing 30 pt, before 6 pt, after 3 pt

### Tables and figures

- Table caption: `SimHei`, 12 pt, bold, centered
- Table header: `SimHei`, 12 pt, bold, centered
- Table body: `SimSun`, 12 pt
- Preferred table style: three-line table
- Table row spacing: exact 18-20 pt when 28 pt is too loose
- Figure caption: `FangSong_GB2312`, 12 pt, centered

### Header and footer

- Header: none by default
- Footer page number: centered, `SimSun`, 9 pt
- Page number style: `- 1 -` by default

## Practical rule

If a template exists, match the template exactly.

If no template exists, use this default profile and present it to the user as the resolved proposal when confirmation is required. Do not ask the user vague questions such as "What formatting do you want?" if you can present a concrete profile first.

## Minimal confirmation payload

Use a short checklist or note with these fields:

- format_authority
- needs_confirmation
- page_setup
- heading_fonts
- table_style
- footer_style
- exceptions

## Tooling

Use [scripts/init_format_profile.py](../scripts/init_format_profile.py) to generate a first-pass format profile for review or record keeping.
