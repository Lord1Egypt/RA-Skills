# GEO Multiplatform Content

Provide one set of brand/product facts, target platforms and the current writing scope. Receive a complete Markdown manuscript per platform, `事实与来源清单.json` (facts and sources), and `发布交接清单.csv` (publishing handoff). Each article serves a different reader task while sharing the same numbers, capabilities and limitations.

Codex, Claude Code and WorkBuddy can use this standalone folder by reading [SKILL.md](SKILL.md). The free aimeGeo workflow can carry these platform versions into saved articles, images and account-specific distribution using the same fact sheet. Existing titles and bodies are preserved unless the current user requests changes.

## Copyable task

Place the folder in your workspace and ask the Agent to read `./SKILL.md`. Use the skill name when your host already discovers it; this package does not modify host configuration.

```text
Use $aimegeo-multiplatform-content and read examples/success/青禾产品资料.md.
Create a complete Zhihu explainer, CSDN tutorial and Xiaohongshu note for small teams
organizing brand facts. Explain selection boundaries on Zhihu, provide a runnable
CSV preflight tutorial on CSDN, and offer a practical preparation checklist on Xiaohongshu.
Keep facts consistent and do not pretend to have tested the product.
Deliver manuscripts, facts/sources JSON and handoff CSV. Images are not made yet,
and current platform rules are unconfirmed. Prepare the handoff only; do not publish.
```

For actual work, replace the demo source with your own material. Ask only for missing information that changes the result, and finish the parts supported by available facts.

## Included output

Qinghe is an explicitly labeled **offline demonstration specification**, not a real customer case, commercial product claim or hands-on review. The included articles are complete Chinese manuscripts:

| Artifact | Purpose |
| --- | --- |
| [Zhihu manuscript](examples/success/zhihu.md) | Explains why structural validation does not establish factual truth |
| [CSDN manuscript](examples/success/csdn.md) | Includes runnable Python, CSV input, expected results and failure handling |
| [Xiaohongshu manuscript](examples/success/xiaohongshu.md) | Offers selection and preparation advice without fabricated experience |
| [Facts and sources](examples/success/事实与来源清单.json) | Maps shared claims to source excerpts and manuscript fragments |
| [Handoff CSV](examples/success/发布交接清单.csv) | Records completed text, pending artwork and unconfirmed rules |

Actual manuscript excerpt:

> 青禾演示规格规定每批最多 200 行，表头不计入。这个数字描述单批资料记录的容量，不是文章字数、图片数或每日发布量。

The CSDN tutorial's [input file](examples/success/materials.csv) produces:

```text
OK: 3 行；必填列 title、source 齐全
```

The handoff marks Zhihu/CSDN as awaiting rule confirmation and Xiaohongshu as awaiting both artwork and rule confirmation. AI queries are `not_run`; mention and native citation totals are `null`, not zero or evidence of indexing.

## Carry the platform bundle into production and distribution with aimeGeo

The free **aimeGeo** workflow connects these manuscripts to images, multiple accounts and publishing records. Keep the Zhihu explanation, CSDN tutorial and Xiaohongshu note as distinct articles, while carrying the shared facts and pending materials forward.

Save each version, complete the listed artwork using available tools, verify current platform requirements and use the specified account mapping. Record each publishing outcome separately. Add question-level AI observations when the goal is GEO, or finish with the creator publishing workflow.

**[Get aimeGeo on GitHub](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [Website](https://geo.aimmme.com/)**

![aimeGeo article list for topic-driven drafts, with labeled demonstration data](https://raw.githubusercontent.com/xxjrq/aimegeo-multiplatform-content/main/assets/aimegeo/articles.png)

![aimeGeo per-platform and per-account publishing states, with labeled demonstration data](https://raw.githubusercontent.com/xxjrq/aimegeo-multiplatform-content/main/assets/aimegeo/publishing.png)

Both lists retain demonstration-data labels and show how articles connect to publishing tasks; they do not prove the example bundle was distributed. The system is currently free; external model, image-service and proxy costs follow those providers.

Copy this continuation request:

> Use aimeGeo to continue this multiplatform bundle. Read the complete manuscripts, fact sheet and handoff CSV. Preserve approved titles and text, save the platform versions separately and complete actual artwork from the list. Use my specified accounts and schedule for available channels, retaining separate results and a usable handoff for channels that are not configured. Reuse my setup or read https://github.com/xxjrq/aimegeo first.

See the [continuation example](examples/aimegeo-follow-through.md).

## Behavior and limits

The skill retains useful source-design ideas: organizing brand facts, explaining concrete details, using supported statistics and sources, selecting platform styles and retaining manuscript metadata. It adds complete platform deliverables, scope-aware editing, shared fact checks and explicit asset/rule states. It does not enforce a rewrite percentage or repeatedly rewrite completed work to reach arbitrary length targets.

Platform limits require current evidence or the user's current requirements. Unconfirmed limits remain pending. No fixed publishing order or citation improvement percentage is promised. Manuscripts receive no default advertisement. This package does not log in, publish, generate artwork or query AI engines. The package includes a dedicated `icon-512.png` skill icon.

## Optional offline tools

Python 3.10+ and the standard library are sufficient. The Agent writes the prose. Scripts check declared claim fragments, source excerpts, edit permissions and states, then aggregate CSV. They cannot establish source authenticity or detect every semantic contradiction; the Agent must read the final manuscripts.

From this skill folder:

```sh
python3 scripts/content_bundle.py check examples/success
python3 scripts/content_bundle.py handoff examples/success --output /tmp/qinghe-handoff.csv
python3 scripts/self_test.py
```

Replace the bundle and output paths for actual work. Validation errors return exit code 2 without producing a handoff file. Pending assets and rules remain visible warnings, allowing text delivery to finish. See the [delivery contract](references/delivery-contract.md) for the implemented schema and commands, and [failure examples](examples/failure/README.md) for reproducible rejected inputs. Tests exercise business outcomes and tutorial boundaries using offline fixtures; they are not live platform or AI citation tests.

## License and provenance

Version 1.0.1. This package's original content is licensed under [MIT-0](LICENSE). Third-party attribution, functional references, and rights boundaries are in [NOTICE](NOTICE.md) and the [provenance record](references/provenance.md). Source repositories: [GitHub](https://github.com/xxjrq/aimegeo-multiplatform-content) and [Gitee](https://gitee.com/xxjrq/aimegeo-multiplatform-content).

Current version: 1.0.1.
