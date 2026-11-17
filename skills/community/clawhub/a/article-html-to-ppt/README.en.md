# PPT Smith

[简体中文](README.md) · [Skill entry](SKILL.md) · [Native-template workflow](references/native-template-workflow.md) · [Installation](#installation-and-local-checks)

Turn source documents, approved slide designs or native PPTX templates into presentations with traceable content, editable objects and real previews. The model authors; fixed tools execute and verify.

**Current version: `5.3.1` · Apache-2.0.** Install as `article-html-to-ppt`; public slug `meowclaw-pptsmith`; compatibility alias `meowclaw-decksmith`.

## Showcase

### Template-route result · Xiaomi Group Q2/H1 2025 business review · 36 slides

From the executive summary and operating drivers to validation questions, action planning and management decisions, the deck retains a coherent template language. The overview below comes from the user-supplied PPTX rendered by an actual office engine, not a redrawn promotional image. Click to enlarge.

[![Xiaomi Q2/H1 2025: actual rendered overview of the 36-slide template-route result](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.3-xiaomi-2025-q2-h1-template-36page-overview.jpg)](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.3-xiaomi-2025-q2-h1-template-36page-overview.jpg)

<table>
  <tr>
    <td width="33%"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.3-xiaomi-template-page-02.jpg"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.3-xiaomi-template-page-02.jpg" alt="Slide 2: executive summary and key metrics" width="100%"></a><br><strong>Executive summary</strong><br>Metrics and conclusions in distinct layers</td>
    <td width="33%"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.3-xiaomi-template-page-15.jpg"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.3-xiaomi-template-page-15.jpg" alt="Slide 15: expenses and two-period comparison" width="100%"></a><br><strong>Expense comparison</strong><br>Data grouped with its interpretation</td>
    <td width="33%"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.3-xiaomi-template-page-30.jpg"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.3-xiaomi-template-page-30.jpg" alt="Slide 30: action schedule and acceptance gates" width="100%"></a><br><strong>Action schedule</strong><br>From conclusions to execution</td>
  </tr>
</table>

<details>
<summary>Object inventory and validation scope</summary>

- **36 actual 16:9 slides**, with nonempty speaker-note bodies on all 36; LibreOffice rendered **36/36 successfully**.
- 1,398 top-level objects: 1,383 native shapes, including 772 nonempty text frames, plus 4 native tables and 11 picture objects. Text frames are a subset, not an additional count.
- This deck has **no data-backed native charts or embedded chart workbooks**. Visible bars and rings are native drawing shapes, not chart-data editing capability.
- This is a user-supplied finished template-route result. This release checked the file, rendered it and inspected representative pages; it **did not repeat the complete generation run** or certify it as an end-to-end v5.3.0 run.
- Original local line-break and annotation-spacing imperfections remain. Financial facts were not re-audited; PowerPoint/WPS GUI edit-save-reopen was not tested.
- Only this overview, three representative images and [concise evidence](assets/samples/v5.3-xiaomi-template-evidence.json) are public. The original PPTX, inputs and complete logs are excluded.

</details>

### More real examples

<table>
  <tr>
    <td width="33%"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.2-xiaomi-q2-h1-22page-overview.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.2-xiaomi-q2-h1-22page-overview.png" alt="22-slide decorative business review" width="100%"></a><br><strong>22-slide business review</strong><br>Body-layout variety and deck coherence</td>
    <td width="33%"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-native-4page-2col-overview.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-native-4page-2col-overview.png" alt="Four-slide native template comparison" width="100%"></a><br><strong>Native component reuse</strong><br>Four-slide same-source comparison</td>
    <td width="33%"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-01.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-01.png" alt="Cover from the six-slide policy example" width="100%"></a><br><strong>No-image-generation design</strong><br>Six Chinese policy slides with actual previews</td>
  </tr>
</table>

Earlier examples retain their original versions and evidence limits; see the [historical gallery](references/cases/legacy-showcase.en.md). Counts and version labels are not aesthetic scores or general compatibility certification.

## 5.3.1 security maintenance

This release retains the 5.3.0 native-template workflow and makes substantive fixes identified during platform review:

- Stage output in an exclusive temporary directory; replacing existing output requires an ownership marker and explicit `--overwrite`. Preserve or restore previous artifacts on failure.
- Contribution export requires explicit sharing consent and reconstructs bounded structural statistics rather than copying private text or arbitrary evidence.
- Advanced author-Python execution is denied by default and requires operator-reviewed, per-process entry-source SHA-256 consent. This is not a sandbox and does not weaken required OS isolation.
- Pin Pillow 13.0.0 and scoped image-size 2.0.4; the compatibility Windows renderer no longer quits the user's PowerPoint application.

**Support boundaries:** Python >=3.11; Node >=18 only for the optional PptxGenJS route. Real Windows/PowerPoint, minimum Node 18 and every image format were not exercised. Mocks are not real-Office validation. Some image-size advisories contain conflicting affected/fixed metadata; local tests do not establish universal vulnerability clearance. Read the [security and compatibility boundaries](references/security-boundaries.md).

Independent platform checks must evaluate this exact release. The earlier 5.3.0 review record is retained; local validation is not platform approval.

## What is new in 5.3.0

- **Clone original pages, then edit content.** Output pages bind real source slides and retain native layout/master/theme relationships instead of merely copying a palette onto blank pages.
- **Fixed Python tools.** Edit supported text, chart/table data, same-source styled objects, page order and notes. The host agent owns narrative and orchestration, without a website account, second model runtime or new Node dependency.
- **Recoverable local revisions.** Stable page IDs, revision checks, frozen template bytes and atomic transactions preserve valid work on failure; unselected source slides cannot be smuggled into the output.
- **Evidence belongs to the current file.** Source preservation, decoration/type-scale floors, real rendering and independent page observations are separate checks. Missing or stale evidence does not become final acceptance.
- **Existing tasks stay compatible.** The three user intents remain `create / recreate / template`; Atlas/component tasks retain their original contract.

Runtime limits are listed below. Inspection of the showcased finished deck is separate from the synthetic tool regressions and render validations; they are not presented as the same acceptance run.

## Three ways to use it

| Task | Input | Route |
| --- | --- | --- |
| Make a presentation from a report, policy, PRD, article or data | Source material; optional brand/style references | **create**: design native pages, then render and review |
| Rebuild an approved complete slide design | Full-page designs and checked source text/data | **recreate**: native reconstruction against a frozen target |
| Preserve a company/client PPTX template | Native template and current content | **template**: original-page editing; retain Atlas for existing component tasks |

A template used only as a style reference belongs to create. Native asset preservation belongs to template. Source page count does not set slide count; the current audience, content and brand determine typography, composition and rhythm.

**Image generation is optional.** A vision-capable model can author native objects and inspect real renders. Generated illustrations or an explicitly approved external design target are optional; a text-only model still needs a human or vision reviewer for visual acceptance.

## How to use it with an agent

Load [SKILL.md](SKILL.md), attach material and state the audience, purpose, language, slide budget and target software. Users do not need to write object JSON.

**Reuse a native template:**

```text
Use PPT Smith to create about 20 Chinese slides from this company PPTX template
and the attached business material. Audience: management.
Lead with conclusions, then explain changes and decisions.
Retain the original-page visual language, master and layouts; select, copy and
adapt pages to the content rather than copying the template's sample text.
Preserve important numbers, definitions, sources and notes.
Check representative pages before expanding the deck, render actual PPTX pages,
obtain independent review and disclose chart/image/application editing limits.
```

**Design from sources:**

```text
Use PPT Smith to make about 12 editable Chinese slides from this material.
Audience: business owners. Conclusions first; vary the body with the information
while keeping the deck coherent. Do not invent missing numbers.
Separate source facts, calculations and advice; retain page sources and notes.
Image generation is not required. Deliver actual PPTX, previews, review results
and material editing limitations.
```

For reconstruction, identify approved full-page targets. For a small revision, retain the task directory and identify affected pages/objects. Review reuse follows each route's dependency checks; the new original-page tools do not automatically inherit old candidate approval.

## Installation and local checks

From the Skill root, using Bash on macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_identity.py
python scripts/quick_validate_skill.py
python -m engine design capabilities
python -m engine template capabilities
```

Real previews require **LibreOffice, Poppler, Fontconfig and the actual fonts**. Capability discovery checks local tools, not the host model's vision or image-generation abilities.

- The new original-page executor requires **POSIX `fcntl` and `O_NOFOLLOW`**. It was tested on macOS; Windows is unsupported. Source and output decks are each limited to 100 slides.
- See the [declarative workflow](references/declarative-design.md) for create/recreate requirements; do not apply the new executor's restrictions to every legacy route or claim all platforms were tested.
- Only PptxGenJS compatibility builders require Node/npm and `python scripts/bootstrap_pptxgenjs_runtime.py`; the new executor adds no Node dependency.

Tool sequence: `capabilities → init → inspect → apply → export → render → review → verify`. Exact JSON and rejection/review contracts are in the [native-template guide](references/native-template-workflow.md), not duplicated here.

## Delivery and compatibility boundaries

| Area | Current boundary |
| --- | --- |
| New chart editing | Single-plot category charts with real data/workbooks, not arbitrary chart types |
| Tables | Existing unmerged rectangular cells; no row/column or merge restructuring |
| Pictures | Additions clone embedded same-source pictures; no arbitrary external photo replacement; image internals are not native objects |
| Preservation | Conservative exact-source checks plus decoration/type-scale floors; unresolved evidence may block and is not an aesthetic score |
| Review | Bound to current candidate, template and actual page images; reviewer identity declared, not authenticated |
| Office applications | Native objects and LibreOffice rendering do not prove PowerPoint/WPS GUI edit-save-reopen compatibility |

Final delivery includes editable PPTX, real previews, source/gap records, review decisions and editing limitations. An unapproved whole-page screenshot cannot substitute for editable reconstruction. Business/scientific facts still require checking. Model-side source handling depends on the host; local tools do not mean model calls are necessarily offline. Cloud creation, uploading and sharing require the corresponding authorization.

Quality and OS isolation are separate. Explicit isolation requirements remain binding. Bespoke is an advanced compatibility route; Standard/Engineering is only for explicit engineering drafts and diagnostics.

## Documentation and distribution

- [Skill contract](SKILL.md) · [Original-page template workflow](references/native-template-workflow.md)
- [Declarative design and acceptance](references/declarative-design.md) · [Compact authoring/revisions](references/declarative-authoring.md)
- [Existing template component workflow](references/routes/v4-template-route.md) · [Template-inspired design](references/template-visual-design.md)
- [Decorative business design](references/decorative-business-design.md) · [Page planning sheet](templates/decorative-page-plan.md)
- [Historical examples and evidence limits](references/cases/legacy-showcase.en.md) · [Public bundle scope](references/BUNDLE-MANIFEST.md)

GitHub retains source and focused regressions. ClawHub/SkillHub runtime packages exclude tests, raw inputs, full logs, worktrees and private material. Platform limits and adaptation/review status are checked separately; a version label alone does not mean a platform has listed it.

Maintained by **MeowClaw Lab / SkillMelody**. The core engine, general components and QA use **Apache-2.0**. Brands and examples imply no company partnership or endorsement. Enterprise brand adaptations, dedicated masters and managed generation are separate commercial deliveries, not part of the public bundle.

---
ClawHub hosted text distribution 5.3.1; frozen source `298f2c54920c9744246dbbace0f0e413945b085f`. Gallery assets are unchanged and use public immutable asset commit `3d66f434001c544ff0ac79b7230586b3d0c1690a`. All runtime code and Skill instructions match the tested local source; this security revision has not been pushed to GitHub by this task.
