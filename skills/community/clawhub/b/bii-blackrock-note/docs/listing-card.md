## Description:

Re-skins an existing **BII-format single-stock research note** — A4 landscape, cover + 9 core pages + 12 supplementary pages, left text column + right chart column — into the **BlackRock Investment Institute** visual system, and delivers `pptx` + `pdf` + `html` from one command.

It is a *content engine + visual layer* combination, not a report generator. The 22-page structure, the two-column skeleton, all 5 canvases and 12 SVG charts, and every line of body copy and data come from the upstream `bii-equity-note` skill. This skill only changes the visual system on top:

1. **Global palette redirect** — 35 source colour classes → brand tokens, applied across CSS, inline styles, SVG `fill` and canvas JS. Seven categorical series hues are kept as seven *distinguishable* hues; brand identity is carried by black + yellow + structural decoration rather than by collapsing category colours.
2. **Structural decoration injection** — left black spine, top black band, brand-yellow bookmark tabs, black holdings panel, yellow-header summary box, and a three-section `disclaimer | page number | document code` footer.
3. **Zero-net-increment decoration constraint** — the source pages sit exactly at `793.7px`, i.e. the A4 landscape paper height, so any positive box-height addition silently adds a page. All decoration is built to add exactly 0px.
4. **Seven QA gates**, including a **verbatim content-unchanged gate** that tokenises visible text into a multiset and fails if the product contains any token the injection did not itself introduce.

This skill is for research and development only.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers who already produce BII-style single-stock briefings use this skill when the same content has to go out under an institutional visual identity, or when one source HTML has to be delivered simultaneously as an editable web page, a print-grade PDF and a presentable deck. Typical scenarios: re-branding a research note for a different distribution channel, producing the same note for a client meeting and an internal archive, or enforcing a house style across a recurring note series.

It is framed as engineering and design tooling. It does not generate investment advice, and every output carries a layout-provenance statement making clear that the note is an independent analysis piece and not a BlackRock publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewers may mistake the branded output for an actual BlackRock / BlackRock Investment Institute publication.

Mitigation: The cover footer carries a mandatory layout-provenance statement, and the skill forbids omitting it. The visual system is applied to the operator's own analysis content only — no third-party report text is ingested.

Risk: The visual overlay can silently overflow a page and add a page to the PDF, breaking the 22-page contract.

Mitigation: Decoration is constrained to zero net height increment, and gate 1 asserts `sections == bookmarks == footer codes == expected pages`; gate 6 asserts the PDF page count and page size. A per-page height measurement script is included to localise any overflow to a specific page.

Risk: A palette remap can collapse distinct chart series into visually identical colours, making a chart unreadable.

Mitigation: Gate 4 asserts all seven categorical hues survive as distinguishable hues. The first release shipped with two collisions that merged four series in one boxplot; that failure mode is now a regression gate.

Risk: A regex-based palette remap can corrupt body text or chart JavaScript, and a hard-coded whitelist would hide the damage instead of reporting it.

Mitigation: Gate 5 compares the visible-text token multiset before and after, and derives its allow-list by reverse-engineering what was actually injected into the DOM rather than hard-coding expected strings.

Risk: Image-backed PPTX slides are not text-editable.

Mitigation: Page text is written into speaker notes to remain searchable and copyable, and the skill instructs the operator to disclose this trade-off and to re-render from HTML when wording must change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yjkj999999/skills/bii-blackrock-note)
- [Publisher profile](https://clawhub.ai/user/yjkj999999)
- [Project homepage](https://github.com/yjkj999999/bii-blackrock-note)
- [README](README.md)
- [Sichuan Gold (SZ001337) 22-page run case study](examples/sz001337_case.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands plus generated HTML, PDF and PPTX decks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output page size matches the source exactly (841.92x594.96pt, A4 landscape). PDF page count equals the source section count. PPTX slide size is probed from the PDF first page and requires no scaling.]

## Skill Version(s):

1.0.1 (supersedes `brand-pdf-deck-replica`, retired at the same release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. The visual identity applied by this skill belongs to BlackRock, Inc.; users are responsible for ensuring they have the right to reproduce any institutional visual identity, and must not present the output as an official publication of the brand whose identity was applied.
