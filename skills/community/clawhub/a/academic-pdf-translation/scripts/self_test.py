"""交付前的端到端自测：造一份合成论文，从建作业一路跑到发布归档。

这个脚本不再承载可以独立判断的单点用例。原来住在这里的 18 个 _test_*
函数和 run() 里的一长串内联断言，已经迁进 tests/ 变成命名 pytest 用例：

    tests/test_workflow_contracts.py
    tests/test_retained_source_dedup.py
    tests/test_retained_region_reconciliation.py
    tests/test_complex_page_routing.py
    tests/test_image_localization.py
    tests/test_anchor_and_markup_rules.py
    tests/test_exact_presence_rules.py
    tests/test_typography_search.py
    tests/test_selftest_cache_invalidation.py
    tests/test_translation_batch_units.py
    tests/test_cjk_markup_and_flow.py
    tests/test_qa_page_heuristics.py
    tests/test_complex_content_policy.py

留在 run() 里的是唯一一段真正无法脱离上下文的检查：一条从头到尾的交付
链路。它在同一个临时目录里依次建工作区、建作业、编排批次、写回译文、
做完整性审计、生成候选、跑质检、返修、注册、归档，每一步都吃上一步落
盘的结果。把它切成互相独立的 pytest 用例，等于把顺序依赖改写成夹具，
那是重写而不是迁移，会改变它正在验证的东西。所以它整段保留，
self_test.py 因此停在两千行上下，没有达到计划里 500 行的目标。

check_bundle 与 CI 依赖本脚本打印 SELF TEST PASS，这条输出保持不变。
"""

from __future__ import annotations

import sys

# 这两个工具要审计"交付物里有没有字节码缓存"，可它们自己一导入模块就会生成
# __pycache__——于是干净安装后按 README 跑一遍必然失败。先关掉字节码写入，
# 别让检查工具弄脏它正在检查的目录。
sys.dont_write_bytecode = True

import hashlib  # noqa: E402
import json  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

from _common import (  # noqa: E402
    SkillError,
    import_fitz,
    load_json,
    sha256_file,
    utc_now,
    write_json,
)
from audit_translation_completeness import (  # noqa: E402
    _repair_tasks,
    build_completeness_audit,
)
from build_candidate import (  # noqa: E402
    VectorPayloadFlowable,
    _reference_font_size,
    _styles,
    _table_flowables,
)
from check_bundle import check_bundle  # noqa: E402
from corpus_audit import audit_corpus  # noqa: E402
from extract_source_structure import extract_source_structure  # noqa: E402
from i18n import message  # noqa: E402
from init_job import (  # noqa: E402
    initialize_job,
)
from make_review_sheet import make_review_sheet  # noqa: E402
from pre_render_audit import build_pre_render_audit  # noqa: E402
from preflight_candidate import (  # noqa: E402
    _candidate_content_fingerprint,
    preflight_candidate,
)
from qa_pdf import (  # noqa: E402
    run_qa,
)
from record_review_round import record_review_round  # noqa: E402
from record_work_checkpoint import record_work_checkpoint  # noqa: E402
from register_candidate import register_candidate  # noqa: E402
from retained_source import (  # noqa: E402
    _reference_entries,
    _trim_reference_tail,
)
from review_risk_report import (  # noqa: E402
    build_review_risk_report,
)
from set_complex_content import set_complex_content  # noqa: E402
from set_complex_payload import validate_complex_payload_item  # noqa: E402
from set_review_mode import set_review_mode  # noqa: E402
from translation_truthfulness import refresh_coverage  # noqa: E402
from validate_job import (  # noqa: E402
    _adjacent_translation_overlaps,
    _validate_candidate_text_presence,
    _validate_source_text_coverage,
    _validate_translation,
    validate_job,
)
from workspace import (  # noqa: E402
    WORKSPACE_ROOT_NAME,
    create_workspace,
    workspace_job_dir,
)


def _font_path() -> Path:
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise RuntimeError("自测需要一份可嵌入的拉丁字体")


def _job_tree_digest(job_dir: Path) -> dict[str, str]:
    """作业目录内每个文件的哈希快照。

    排除 staging：注册前预检本来就会在那里追加自己的账本。
    """

    digests: dict[str, str] = {}
    for path in sorted(job_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(job_dir)
        if relative.parts and relative.parts[0] in {"staging", "__pycache__"}:
            continue
        digests[str(relative)] = sha256_file(path, use_cache=False)
    return digests


def _make_pdf(
    path: Path,
    paragraphs: list[list[str]],
    fontsize: float = 9.2,
    leading: float = 14.2,
) -> None:
    fitz = import_fitz()
    font_path = _font_path()
    document = fitz.open()
    for page_lines in paragraphs:
        page = document.new_page(width=595.276, height=841.89)
        page.insert_font(fontname="BodyFont", fontfile=str(font_path))
        y = 80.0
        for line in page_lines:
            page.insert_text(
                (72, y),
                line,
                fontname="BodyFont",
                fontfile=str(font_path),
                fontsize=fontsize,
            )
            y += leading
    document.save(path, garbage=4, deflate=True)
    document.close()


def _write_identity_page_map(
    candidate_path: Path,
    translation: dict,
) -> None:
    fitz = import_fitz()
    document = fitz.open(candidate_path)
    candidate_page_count = document.page_count
    document.close()
    source_page_count = max(
        int(unit.get("page") or 0)
        for unit in translation.get("units", [])
    )
    source_to_candidates = {
        page: [min(page, candidate_page_count)]
        for page in range(1, source_page_count + 1)
    }
    for candidate_page in range(source_page_count + 1, candidate_page_count + 1):
        source_to_candidates[source_page_count].append(candidate_page)
    candidate_to_sources: dict[int, list[int]] = {
        page: [] for page in range(1, candidate_page_count + 1)
    }
    for source_page, candidate_pages in source_to_candidates.items():
        for candidate_page in candidate_pages:
            candidate_to_sources[candidate_page].append(source_page)
    write_json(
        candidate_path.with_suffix(".page-map.json"),
        {
            "schema_version": "1.0",
            "generated_at": utc_now(),
            "mapping_mode": "flow-unit-anchors-v1",
            "layout_policy": "self-test-identity",
            "complete": True,
            "source_page_count": source_page_count,
            "candidate_page_count": candidate_page_count,
            "candidate_sha256": sha256_file(candidate_path),
            "source_pages": [
                {
                    "source_page": page,
                    "candidate_pages": source_to_candidates[page],
                }
                for page in range(1, source_page_count + 1)
            ],
            "candidate_pages": [
                {
                    "candidate_page": page,
                    "source_pages": candidate_to_sources[page],
                }
                for page in range(1, candidate_page_count + 1)
            ],
            "units": [
                {
                    "unit_id": str(unit["id"]),
                    "source_page": int(unit["page"]),
                    "candidate_pages": source_to_candidates[int(unit["page"])],
                }
                for unit in translation.get("units", [])
            ],
            "complex_items": [],
            "retained_regions": [],
        },
    )


def _assert_valid(report: dict, label: str) -> None:
    if not report["valid"]:
        raise AssertionError(f"{label} 未通过: {report['errors']}")


def run() -> None:
    bundle_report = check_bundle()
    if bundle_report["status"] != "PASS":
        raise AssertionError("Skill 包结构检查未通过")


    with tempfile.TemporaryDirectory(prefix="academic-pdf-skill-test-") as temp:
        root = Path(temp)
        source = root / "source.pdf"
        _make_pdf(
            source,
            [
                [
                    "Adaptive cache invalidation in distributed systems",
                    "This paper reports a small illustrative sample.",
                    "Association does not establish causation.",
                ],
                [
                    "Methods and results",
                    "The sample included 120 participants.",
                    "Limitations should be interpreted carefully.",
                ],
            ],
        )
        main_workspace = create_workspace(
            "self-test-main",
            [source],
            container=root / WORKSPACE_ROOT_NAME,
        )
        main_source = next(main_workspace.input.glob("*.pdf"))
        job_dir = workspace_job_dir(
            main_workspace,
            main_source,
            sha256_file(main_source),
        )
        formal_dir = main_workspace.output
        initialize_job(
            main_source,
            job_dir,
            "fr",
            "en",
            False,
            producer_id="self-test-producer",
            workspace=main_workspace,
        )
        draft = validate_job(job_dir, "draft")
        _assert_valid(draft, "draft")
        initialized_source_units = load_json(job_dir / "source_units.json")
        initialized_translation = load_json(job_dir / "translation.json")
        if initialized_source_units.get("unit_count", 0) < 2:
            raise AssertionError("初始化必须自动生成冻结原文单元")
        if (
            initialized_translation.get("mapping_mode")
            != "frozen-source-units-v1"
        ):
            raise AssertionError("初始化翻译骨架必须绑定冻结原文单元")

        standard_workspace = create_workspace(
            "self-test-structured",
            [source],
            container=root / WORKSPACE_ROOT_NAME,
        )
        structured_source = next(standard_workspace.input.glob("*.pdf"))
        structured_job_dir = workspace_job_dir(
            standard_workspace,
            structured_source,
            sha256_file(structured_source),
            job_name="structured-job",
        )
        initialize_job(
            structured_source,
            structured_job_dir,
            "fr",
            "en",
            False,
            producer_id="self-test-structured-producer",
            workspace=standard_workspace,
        )
        structured_job = load_json(structured_job_dir / "job.json")
        if structured_job.get("workspace", {}).get("output") != str(
            standard_workspace.output
        ):
            raise AssertionError("标准作业必须记录正式译本目录")
        structured_job["route"]["selected"] = "standard-auto"
        structured_job["route"]["decision_reason"] = "冻结原文单元自测。"
        structured_job["quality"]["selected_fonts"] = [str(_font_path())]
        write_json(structured_job_dir / "job.json", structured_job)
        set_complex_content(
            structured_job_dir,
            [],
            confirmed_none=True,
            notes="已确认两页均为规则正文。",
        )
        structured_translation = load_json(
            structured_job_dir / "translation.json"
        )
        french_by_source = {
            "Adaptive cache invalidation in distributed systems": (
                "Invalidation adaptative du cache dans les systèmes distribués"
            ),
            "This paper reports a small illustrative sample.": (
                "Cet article présente un petit échantillon illustratif."
            ),
            "Association does not establish causation.": (
                "Une association ne démontre pas une causalité."
            ),
            "Methods and results": "Méthodes et résultats",
            "The sample included 120 participants.": (
                "L’échantillon comprenait 120 participants."
            ),
            "Limitations should be interpreted carefully.": (
                "Les limites doivent être interprétées avec prudence."
            ),
        }
        for unit in structured_translation["units"]:
            source_text = unit["source"]
            if source_text not in french_by_source:
                raise AssertionError(
                    f"冻结原文单元拆分结果意外: {source_text!r}"
                )
            unit["translation"] = french_by_source[source_text]
        # 覆盖率不再手写：按真实性判定重算，夹具和产品用同一套规则。
        refresh_coverage(structured_translation)
        structured_translation["terminology_reviewed"] = True
        write_json(
            structured_job_dir / "translation.json",
            structured_translation,
        )
        _assert_valid(
            validate_job(structured_job_dir, "translated"),
            "frozen source units translated",
        )
        summarized_translation = load_json(
            structured_job_dir / "translation.json"
        )
        longest_unit = max(
            summarized_translation["units"],
            key=lambda unit: len(unit["source"]),
        )
        longest_unit["translation"] = "Bref."
        write_json(
            structured_job_dir / "translation.json",
            summarized_translation,
        )
        summarized_audit = build_completeness_audit(structured_job_dir)
        if summarized_audit["decision"] != "NEEDS_REPAIR":
            raise AssertionError("冻结单元被摘要化时必须自动进入返修")
        if not any(
            issue.get("source_ref") == longest_unit["source_ref"]
            for page in summarized_audit["pages"]
            for issue in page.get("unit_issues", [])
        ):
            raise AssertionError("返修证据必须定位到具体冻结原文单元")
        write_json(
            structured_job_dir / "translation.json",
            structured_translation,
        )
        tampered_translation = load_json(
            structured_job_dir / "translation.json"
        )
        tampered_translation["units"][0]["source"] += " changed"
        write_json(
            structured_job_dir / "translation.json",
            tampered_translation,
        )
        if validate_job(structured_job_dir, "translated")["valid"]:
            raise AssertionError("修改冻结原文后必须无法进入 translated 阶段")

        empty_table_payload = {
            "method": "structured-table-rebuild",
            "source_evidence": ["原页表格"],
            "payload": {"tables": []},
        }
        if not validate_complex_payload_item(empty_table_payload):
            raise AssertionError("空表格载荷不得被视为 ready")
        valid_vector_payload = {
            "method": "vector-rebuild",
            "source_evidence": ["原页模型图"],
            "payload": {
                "figures": [
                    {
                        "type": "directed-model",
                        "labels": ["自变量", "中介", "因变量"],
                        "nodes": [
                            {"id": "x", "translation": "自变量"},
                            {"id": "m", "translation": "中介"},
                            {"id": "y", "translation": "因变量"},
                        ],
                        "edges": [
                            {"source": "x", "target": "m"},
                            {"source": "m", "target": "y"},
                        ],
                    }
                ]
            },
        }
        if validate_complex_payload_item(valid_vector_payload):
            raise AssertionError("包含标签和边的矢量载荷应通过结构检查")
        vector_annotation_pdf = root / "vector-annotation.pdf"
        from reportlab.pdfgen.canvas import Canvas

        annotation_canvas = Canvas(str(vector_annotation_pdf), pagesize=(320, 220))
        annotation_figure = VectorPayloadFlowable(
            {
                "type": "directed-model",
                "nodes": [
                    {
                        "id": "source",
                        "translation": "Source",
                        "center_x_ratio": 0.32,
                        "center_y_ratio": 0.3,
                    },
                    {
                        "id": "target",
                        "translation": "Target",
                        "center_x_ratio": 0.76,
                        "center_y_ratio": 0.3,
                    },
                ],
                "edges": [{"source": "source", "target": "target"}],
                "annotations": [
                    {
                        "kind": "covariate-group",
                        "label_translation": "Covariates",
                        "items": [
                            {"translation": "Gender"},
                            {"translation": "Age"},
                        ],
                    }
                ],
            },
            width=300,
            regular_font="Helvetica",
            bold_font="Helvetica-Bold",
            body_font_pt=9,
            message_fn=message,
        )
        annotation_figure.drawOn(annotation_canvas, 10, 10)
        annotation_canvas.save()
        annotation_document = import_fitz().open(vector_annotation_pdf)
        annotation_text = annotation_document[0].get_text()
        annotation_document.close()
        if not all(
            token in annotation_text
            for token in ("Covariates", "Gender", "Age")
        ):
            raise AssertionError("定向模型必须实际渲染协变量分组文字")
        dense_vector_pdf = root / "dense-vector.pdf"
        dense_canvas = Canvas(str(dense_vector_pdf), pagesize=(420, 260))
        dense_figure = VectorPayloadFlowable(
            {
                "type": "directed-model",
                "height_pt": 220,
                "nodes": [
                    {
                        "id": "source",
                        "translation": "Source construct",
                        "center_x_ratio": 0.2,
                        "center_y_ratio": 0.55,
                        "width_ratio": 0.65,
                    },
                    {
                        "id": "mediator",
                        "translation": "Mediator construct",
                        "center_x_ratio": 0.5,
                        "center_y_ratio": 0.55,
                        "width_ratio": 0.65,
                    },
                    {
                        "id": "target",
                        "translation": "Target construct",
                        "center_x_ratio": 0.8,
                        "center_y_ratio": 0.55,
                        "width_ratio": 0.65,
                    },
                ],
                "edges": [
                    {
                        "source": "source",
                        "target": "mediator",
                        "direction": "bidirectional",
                        "path_type": "latent-covariance",
                        "label": "0.39",
                    },
                    {
                        "source": "mediator",
                        "target": "target",
                        "line_style": "dashed",
                        "label": "H2",
                    },
                    {
                        "source": "source",
                        "target": "target",
                        "via": ["mediator"],
                        "label": "H8 via mediator",
                    },
                ],
            },
            width=400,
            regular_font="Helvetica",
            bold_font="Helvetica-Bold",
            body_font_pt=10,
            message_fn=message,
        )
        dense_figure.drawOn(dense_canvas, 10, 20)
        dense_canvas.save()
        dense_document = import_fitz().open(dense_vector_pdf)
        dense_page = dense_document[0]
        dense_text = dense_page.get_text()
        dense_spans = [
            span
            for block in dense_page.get_text("dict").get("blocks", [])
            for line in block.get("lines", [])
            for span in line.get("spans", [])
        ]
        dense_document.close()
        if not all(
            token in dense_text
            for token in (
                "Source construct",
                "Mediator construct",
                "Target construct",
                "0.39",
                "H8 via mediator",
            )
        ):
            raise AssertionError("密集矢量图必须保留节点、协方差和间接路径图例")
        covariance_sizes = [
            float(span.get("size", 0))
            for span in dense_spans
            if str(span.get("text") or "").strip() == "0.39"
        ]
        if not covariance_sizes or min(covariance_sizes) < 7.15:
            raise AssertionError("矢量路径标签不得低于结构化内容可读字号")
        advanced_vector_pdf = root / "advanced-vector.pdf"
        advanced_canvas = Canvas(
            str(advanced_vector_pdf),
            pagesize=(420, 540),
        )
        advanced_figures = [
            (
                {
                    "type": "layout",
                    "height_pt": 500,
                    "axis_labels": {
                        "vertical": {
                            "dimension": "Interactivity",
                            "negative": "Low interactivity",
                            "positive": "High interactivity",
                        },
                        "horizontal": {
                            "dimension": "Volition",
                            "negative": "Low volition",
                            "positive": "High volition",
                        },
                    },
                    "panels": [
                        {
                            "position": "upper-left",
                            "title": "Passive immortality",
                            "semantics": "AI reconstruction",
                        },
                        {
                            "position": "upper-right",
                            "title": "Curated immortality",
                            "semantics": "Mind upload",
                        },
                        {
                            "position": "lower-left",
                            "title": "Passive legacy",
                            "semantics": "Search records",
                        },
                        {
                            "position": "lower-right",
                            "title": "Curated legacy",
                            "semantics": "Memorial archive",
                        },
                    ],
                    "shapes": [
                        {"type": "quadrant", "position": "upper-left"},
                        {"type": "quadrant", "position": "upper-right"},
                        {"type": "quadrant", "position": "lower-left"},
                        {"type": "quadrant", "position": "lower-right"},
                    ],
                },
                (
                    "Interactivity",
                    "Low interactivity",
                    "High interactivity",
                    "Volition",
                    "Low volition",
                    "High volition",
                    "Passive immortality",
                    "Curated immortality",
                    "Passive legacy",
                    "Curated legacy",
                ),
            ),
            (
                {
                    "type": "multi-panel-process",
                    "height_pt": 500,
                    "panels": [
                        {
                            "id": "panel-a",
                            "label": "A",
                            "title": "Process panel",
                        }
                    ],
                    "nodes": [
                        {
                            "id": "sensation",
                            "panel": "A",
                            "translation": "Sensation",
                        },
                        {
                            "id": "appraisal",
                            "panel": "A",
                            "translation": "Appraisal",
                        },
                    ],
                    "edges": [
                        {
                            "source": "sensation",
                            "target": "appraisal",
                            "direction": "inhibitory",
                        }
                    ],
                },
                ("Process panel", "Sensation", "Appraisal"),
            ),
            (
                {
                    "type": "nonlinear-case-trajectory",
                    "height_pt": 500,
                    "axis_labels": [
                        {"axis": "horizontal", "translation": "Time"},
                        {"axis": "vertical", "translation": "Well-being"},
                    ],
                    "nodes": [
                        {
                            "id": "n1",
                            "order": 1,
                            "translation": "Stress appraisal",
                            "x_ratio": 0.1,
                            "y_ratio": 0.2,
                        },
                        {
                            "id": "n2",
                            "order": 2,
                            "translation": "Positive reappraisal",
                            "x_ratio": 0.5,
                            "y_ratio": 0.65,
                        },
                        {
                            "id": "n3",
                            "order": 3,
                            "translation": "Meaningfulness",
                            "x_ratio": 0.9,
                            "y_ratio": 0.85,
                        },
                    ],
                    "series": [
                        {"point_ids": ["n1", "n2", "n3"]}
                    ],
                },
                (
                    "Time",
                    "Well-being",
                    "Stress appraisal",
                    "Positive reappraisal",
                    "Meaningfulness",
                ),
            ),
            (
                {
                    "type": "layout",
                    "height_pt": 500,
                    "panels": [
                        {
                            "id": "track-one",
                            "label": "Track I",
                            "title": "Functions over time",
                            "semantics": (
                                "1. Trauma; 2. Anxiety; 3. Growth. "
                                "Each item is illustrated over time."
                            ),
                        }
                    ],
                    "shapes": [
                        {
                            "id": "track-one-series-bank",
                            "type": "illustrative-time-series-bank",
                            "series_count": 3,
                            "items": [
                                {"translation": "Trauma"},
                                {"translation": "Anxiety"},
                                {"translation": "Growth"},
                            ],
                            "meaning": "fluctuation-only",
                        }
                    ],
                },
                ("Track I", "Trauma", "Anxiety", "Growth"),
            ),
            (
                {
                    "type": "expanding-spiral-process",
                    "height_pt": 500,
                    "axis_labels": [
                        {
                            "axis": "vertical",
                            "translation": "Time",
                        },
                        {
                            "axis": "horizontal-left",
                            "translation": "High well-being",
                        },
                        {
                            "axis": "horizontal-center",
                            "translation": "Low well-being",
                        },
                        {
                            "axis": "horizontal-right",
                            "translation": "High well-being",
                        },
                    ],
                    "nodes": [
                        {
                            "id": "stage-1",
                            "translation": "Stress appraisal",
                            "center_x_ratio": 0.3,
                            "center_y_ratio": 0.15,
                        },
                        {
                            "id": "stage-2",
                            "translation": "Meaningfulness",
                            "center_x_ratio": 0.7,
                            "center_y_ratio": 0.85,
                        },
                    ],
                    "shapes": [{"type": "expanding-spiral"}],
                },
                ("Time", "Stress appraisal", "Meaningfulness"),
            ),
            (
                {
                    "type": "simple-slope-chart",
                    "height_pt": 500,
                    "x_axis": {
                        "label": "Family functioning",
                        "categories": [
                            "Low family functioning",
                            "High family functioning",
                        ],
                    },
                    "y_axis": {
                        "label": "Adolescent defeat",
                        "minimum": -0.6,
                        "maximum": 0.6,
                        "ticks": [-0.6, 0.0, 0.6],
                    },
                    "series": [
                        {
                            "translation": "Low self-efficacy",
                            "line_color": "#000000",
                            "marker": "filled-triangle",
                            "values": [0.92, 0.27],
                            "value_semantics": (
                                "normalized-visual-position-only"
                            ),
                        },
                        {
                            "translation": "High self-efficacy",
                            "line_color": "#FF0000",
                            "marker": "open-square",
                            "values": [0.6, 0.17],
                            "value_semantics": (
                                "normalized-visual-position-only"
                            ),
                        },
                    ],
                },
                (
                    "Family functioning",
                    "Low family functioning",
                    "High family functioning",
                    "Adolescent defeat",
                    "Low self-efficacy",
                    "High self-efficacy",
                ),
            ),
            (
                {
                    "type": "line-chart",
                    "height_pt": 500,
                    "x_categories": [
                        "No implicit mind perception",
                        "Implicit mind perception",
                    ],
                    "y_min": 1,
                    "y_max": 7,
                    "y_ticks": [1, 4, 7],
                    "axis_labels": [
                        {
                            "axis": "horizontal",
                            "translation": "Mind perception group",
                        },
                        {
                            "axis": "vertical",
                            "translation": "Message effectiveness",
                        },
                    ],
                    "series": [
                        {
                            "translation": "Base condition",
                            "line_style": "solid",
                            "values": [4.6, 4.5],
                        },
                        {
                            "translation": "Emotional support",
                            "line_style": "dashed",
                            "values": [3.2, 4.5],
                        },
                    ],
                },
                (
                    "Mind perception group",
                    "No implicit mind perception",
                    "Implicit mind perception",
                    "Message effectiveness",
                    "Base condition",
                    "Emotional support",
                ),
            ),
        ]
        for figure, _ in advanced_figures:
            flowable = VectorPayloadFlowable(
                figure,
                width=400,
                regular_font="Helvetica",
                bold_font="Helvetica-Bold",
                body_font_pt=9,
                message_fn=message,
            )
            flowable.wrap(400, 500)
            flowable.drawOn(advanced_canvas, 10, 20)
            advanced_canvas.showPage()
        advanced_canvas.save()
        advanced_document = import_fitz().open(advanced_vector_pdf)
        for page_index, (_, expected_tokens) in enumerate(advanced_figures):
            page = advanced_document[page_index]
            page_text = page.get_text()
            if not all(token in page_text for token in expected_tokens):
                raise AssertionError(
                    "过程多面板、坐标轨迹和扩展螺旋必须实际渲染"
                    f"全部结构文字: 第{page_index + 1}页"
                )
            if len(page.get_drawings()) < 4:
                raise AssertionError(
                    "过程多面板、坐标轨迹和扩展螺旋不得退化为空框"
                )
        advanced_document.close()
        compact_label = VectorPayloadFlowable(
            {
                "type": "layout",
                "labels": ["Published online: 18 February 2020"],
                "shapes": [{"type": "text-region"}],
                "height_pt": 80,
            },
            width=300,
            regular_font="Helvetica",
            bold_font="Helvetica-Bold",
            body_font_pt=9,
            message_fn=message,
        )
        _, compact_height = compact_label.wrap(300, 200)
        if not 40 <= compact_height < 80:
            raise AssertionError("单行矢量文字不应被硬撑到复杂图最小高度")

        table_note_pdf = root / "table-note.pdf"
        from reportlab.platypus import SimpleDocTemplate, Table

        table_styles = _styles(
            regular_font="Helvetica",
            bold_font="Helvetica-Bold",
            reference_font="Helvetica",
            body_font_pt=9,
            leading_ratio=1.6,
            reference_font_pt=8.5,
        )
        table_note_flowables = _table_flowables(
            {
                "payload": {
                    "tables": [
                        {
                            "title": "Table 1",
                            "header_rows": 2,
                            "rows": [
                                ["Measure", "Results", ""],
                                ["", "Value", "95% CI"],
                                ["A", "1", "(0.8–1.2)"],
                                ["B", "2", "(1.4–2.6)"],
                            ],
                            "header_structure": {
                                "merged_cells": [
                                    {
                                        "row": 0,
                                        "column": 0,
                                        "row_span": 2,
                                        "col_span": 1,
                                    },
                                    {
                                        "row": 0,
                                        "column": 1,
                                        "row_span": 1,
                                        "col_span": 2,
                                    },
                                ]
                            },
                            "style_semantics": {
                                "excluded_data_rows": [2],
                            },
                            "footnote": {
                                "marker": "a",
                                "translation": "all tests use p < .001.",
                            },
                            "doi": "10.1000/table.1",
                        }
                    ]
                }
            },
            styles=table_styles,
            available_width=280,
        )
        rendered_table = next(
            flowable
            for flowable in table_note_flowables
            if isinstance(flowable, Table)
        )
        if ("SPAN", (0, 0), (0, 1)) not in rendered_table._spanCmds:
            raise AssertionError("多级表头的跨行关系必须进入实际表格")
        if ("SPAN", (1, 0), (2, 0)) not in rendered_table._spanCmds:
            raise AssertionError("多级表头的跨列关系必须进入实际表格")
        if (
            rendered_table._cellvalues[3][0].style.fontName
            != "Helvetica-Bold"
        ):
            raise AssertionError("结构语义标记的排除行必须实际加粗")
        if not any(
            command[0] == "BACKGROUND"
            and command[1] == (0, 3)
            and command[2] == (-1, 3)
            for command in rendered_table._bkgrndcmds
        ):
            raise AssertionError("无粗体字重时，强调行仍须有可见背景语义")
        SimpleDocTemplate(
            str(table_note_pdf),
            pagesize=(320, 220),
            leftMargin=20,
            rightMargin=20,
            topMargin=20,
            bottomMargin=20,
        ).build(table_note_flowables)
        table_note_document = import_fitz().open(table_note_pdf)
        table_note_text = table_note_document[0].get_text()
        table_note_document.close()
        if not all(
            token in table_note_text
            for token in (
                "a",
                "all tests use p < .001",
                "DOI: 10.1000/table.1",
            )
        ):
            raise AssertionError("结构化表格的表注、标记与DOI必须进入候选")

        heading_entries = _reference_entries(
            [
                {
                    "bbox": [0, 0, 300, 100],
                    "raw_text": (
                        "References 1. Alpha A. Example title. "
                        "Example Journal. 2020;1:1-2."
                    ),
                    "text": (
                        "References 1. Alpha A. Example title. "
                        "Example Journal. 2020;1:1-2."
                    ),
                    "role": "body",
                }
            ]
        )
        if (
            not heading_entries
            or heading_entries[0].get("role") != "heading"
            or any(
                str(entry.get("text") or "").startswith("References ")
                for entry in heading_entries[1:]
            )
        ):
            raise AssertionError("参考文献标题与首条题录连写时必须拆开")
        numbered_entries = _reference_entries(
            [
                {
                    "bbox": [0, 0, 300, 100],
                    "raw_text": (
                        "14. Alpha A (2004) First title. Journal 1: 1–2. "
                        "15. Beta B (2005) Second title. Journal 2: 3–4."
                    ),
                    "text": (
                        "14. Alpha A (2004) First title. Journal 1: 1–2. "
                        "15. Beta B (2005) Second title. Journal 2: 3–4."
                    ),
                    "role": "body",
                }
            ]
        )
        if len(numbered_entries) != 2:
            raise AssertionError("同一文字块中的相邻编号题录必须分行排版")
        multiline_numbered_entries = _reference_entries(
            [
                {
                    "bbox": [0, 0, 300, 100],
                    "raw_text": (
                        "6. Alpha A. First title. doi: 10.1000/12345\n"
                        "7. Beta B. Second title. Journal. 2021.\n"
                        "8. Gamma C. Third title. Journal. 2022."
                    ),
                    "text": (
                        "6. Alpha A. First title. doi: 10.1000/12345 "
                        "7. Beta B. Second title. Journal. 2021. "
                        "8. Gamma C. Third title. Journal. 2022."
                    ),
                    "role": "body",
                }
            ]
        )
        if [
            entry["text"].split()[0]
            for entry in multiline_numbered_entries
        ] != ["6.", "7.", "8."]:
            raise AssertionError(
                "原 PDF 换行中的编号题录必须在网址或数字结尾后正确分条"
            )
        linked_entries = _reference_entries(
            [
                {
                    "bbox": [0, 0, 300, 100],
                    "raw_text": (
                        "7. Alpha A. First title. Journal. 2020. [CrossRef] "
                        "8. Beta B. Second title. Journal. 2021."
                    ),
                    "text": (
                        "7. Alpha A. First title. Journal. 2020. [CrossRef] "
                        "8. Beta B. Second title. Journal. 2021."
                    ),
                    "role": "body",
                }
            ]
        )
        if len(linked_entries) != 2:
            raise AssertionError("数据库链接标记后的相邻编号题录必须分行排版")
        wrapped_number_entries = _reference_entries(
            [
                {
                    "bbox": [0, 0, 300, 100],
                    "raw_text": (
                        "10. Alpha A. First title. Journal. 2012;1:1-2. 11.\n"
                        "Frankl V. Second title. Boston: Press; 2006. 12.\n"
                        "Maslow A. Third title. New York: Press; 1968."
                    ),
                    "text": (
                        "10. Alpha A. First title. Journal. 2012;1:1-2. 11. "
                        "Frankl V. Second title. Boston: Press; 2006. 12. "
                        "Maslow A. Third title. New York: Press; 1968."
                    ),
                    "role": "body",
                }
            ]
        )
        if [entry["text"].split()[0] for entry in wrapped_number_entries] != [
            "10.",
            "11.",
            "12.",
        ]:
            raise AssertionError("行末编号必须与下一行的参考文献作者合并")
        author_year_entries = _reference_entries(
            [
                {
                    "bbox": [0, 0, 300, 100],
                    "raw_text": (
                        "Andriessen, Karl, Krysinska Karolina, and Onja Grad. "
                        "2017. First title. Boston: Hogrefe. "
                        "Beckford, James. 2014. Second title. [CrossRef] "
                        "Centers for Disease Control and Prevention. 2017. "
                        "Third title. [CrossRef] "
                        "Castelli Dransart, Dolores Angela. 2018. Fourth title."
                    ),
                    "text": (
                        "Andriessen, Karl, Krysinska Karolina, and Onja Grad. "
                        "2017. First title. Boston: Hogrefe. "
                        "Beckford, James. 2014. Second title. [CrossRef] "
                        "Centers for Disease Control and Prevention. 2017. "
                        "Third title. [CrossRef] "
                        "Castelli Dransart, Dolores Angela. 2018. Fourth title."
                    ),
                    "role": "body",
                }
            ]
        )
        if len(author_year_entries) != 4:
            raise AssertionError("未编号的作者—年份题录必须逐条分行")
        if not author_year_entries[2]["text"].startswith(
            "Centers for Disease Control"
        ):
            raise AssertionError("机构作者题录必须识别为独立条目")
        if not author_year_entries[3]["text"].startswith(
            "Castelli Dransart"
        ):
            raise AssertionError("复姓作者题录必须识别为独立条目")
        multi_author_entries = _reference_entries(
            [
                {
                    "bbox": [0, 0, 300, 100],
                    "raw_text": (
                        "Hipp, Tracy N., Alexandra L. Bellis, Bradley L. "
                        "Goodnight, Carolyn L. Brennan, Kevin M. Swartout, "
                        "and Sarah L. Cook. 2017. First title. [CrossRef] "
                        "Jahn, Danielle R., and Sally Spencer-Thomas. 2014. "
                        "Second title."
                    ),
                    "text": (
                        "Hipp, Tracy N., Alexandra L. Bellis, Bradley L. "
                        "Goodnight, Carolyn L. Brennan, Kevin M. Swartout, "
                        "and Sarah L. Cook. 2017. First title. [CrossRef] "
                        "Jahn, Danielle R., and Sally Spencer-Thomas. 2014. "
                        "Second title."
                    ),
                    "role": "body",
                }
            ]
        )
        if len(multi_author_entries) != 2:
            raise AssertionError("姓名缩写后的共同作者不得被误拆为新题录")
        article_number_entries = _reference_entries(
            [
                {
                    "bbox": [0, 0, 300, 500],
                    "raw_text": (
                        "Gallagher, S. (2013). First title. Article\n"
                        "443. Gerlitz, C., & Helmond, A. (2013). "
                        "Second title.\n"
                        "Hagendorff, T. (2024). Third title. Article\n"
                        "39. Henrickson, L. (2023). Fourth title.\n"
                        "De Freitas, J. (2025). Fifth title. "
                        "arXiv:2508.19258\n"
                        "den Hond, F., & Moser, C. (2023). Sixth title.\n"
                        "Jiménez-Alonso, B., & de Brescó\n"
                        "Luna, I. (2023). Seventh title.\n"
                        "Rindfleisch, A. (2009). Eighth title. 1-16. "
                        "Ringel\n"
                        "Morris, M., & Brubaker, J. (2025). "
                        "Ninth title. Article\n"
                        "536. Roberts, P., & Vidal, L. (2000). "
                        "Tenth title."
                    ),
                    "text": (
                        "Gallagher, S. (2013). First title. Article 443. "
                        "Gerlitz, C., & Helmond, A. (2013). Second title. "
                        "Hagendorff, T. (2024). Third title. Article 39. "
                        "Henrickson, L. (2023). Fourth title. "
                        "De Freitas, J. (2025). Fifth title. "
                        "arXiv:2508.19258 "
                        "den Hond, F., & Moser, C. (2023). Sixth title. "
                        "Jiménez-Alonso, B., & de Brescó Luna, I. "
                        "(2023). Seventh title. "
                        "Rindfleisch, A. (2009). Eighth title. 1-16. "
                        "Ringel Morris, M., & Brubaker, J. (2025). "
                        "Ninth title. Article 536. "
                        "Roberts, P., & Vidal, L. (2000). Tenth title."
                    ),
                    "role": "body",
                }
            ]
        )
        article_number_starts = [
            entry["text"].split()[0]
            for entry in article_number_entries
        ]
        if article_number_starts != [
            "Gallagher,",
            "Gerlitz,",
            "Hagendorff,",
            "Henrickson,",
            "De",
            "den",
            "Jiménez-Alonso,",
            "Rindfleisch,",
            "Ringel",
            "Roberts,",
        ]:
            raise AssertionError(
                "文章编号、姓名粒子和跨行复姓不得破坏作者—年份题录分段"
            )
        for index, article_number in (
            (0, "Article 443."),
            (2, "Article 39."),
            (8, "Article 536."),
        ):
            if article_number not in article_number_entries[index]["text"]:
                raise AssertionError("文章编号必须保留在所属参考文献条目中")
        trimmed_reference_tail = _trim_reference_tail(
            [
                {
                    "bbox": [0, 0, 300, 100],
                    "raw_text": (
                        "Zardiashvili, L. (2020). Final title. "
                        "Publisher’s note Springer Nature remains neutral."
                    ),
                    "text": (
                        "Zardiashvili, L. (2020). Final title. "
                        "Publisher’s note Springer Nature remains neutral."
                    ),
                    "role": "body",
                }
            ]
        )
        if (
            len(trimmed_reference_tail) != 1
            or trimmed_reference_tail[0]["text"]
            != "Zardiashvili, L. (2020). Final title."
        ):
            raise AssertionError(
                "题录末条与出版者声明同块时必须保留题录并剔除声明"
            )

        reference_job = {
            "quality": {
                "body_font_min_pt": 8.0,
                "typography_search": {
                    "reference_font_range_pt": [8.2, 10.5]
                },
            }
        }
        if _reference_font_size(reference_job, 10.0) != 9.0:
            raise AssertionError("参考文献字号必须使用配置范围而非固定最低值")
        if (
            _reference_font_size(
                {
                    "quality": {
                        "body_font_min_pt": 8.0,
                        "typography_search": None,
                    }
                },
                10.0,
            )
            != 9.0
        ):
            raise AssertionError("非简体中文配置缺少排版搜索参数时必须回退默认值")
        valid_bar_panels_payload = {
            "method": "vector-rebuild",
            "source_evidence": ["原页四联柱状图"],
            "payload": {
                "figures": [
                    {
                        "type": "bar-panels",
                        "panels": [
                            {
                                "title": "结果指标",
                                "y_min": 1.0,
                                "y_max": 5.0,
                                "groups": [
                                    {"translation": "干预组", "value": 4.2},
                                    {"translation": "控制组", "value": 3.1},
                                ],
                                "comparisons": [
                                    {
                                        "start": 0,
                                        "end": 1,
                                        "label": "**",
                                    }
                                ],
                            }
                        ],
                    }
                ]
            },
        }
        if validate_complex_payload_item(valid_bar_panels_payload):
            raise AssertionError("包含面板、组别和数值的柱状图载荷应通过结构检查")

        if validate_job(job_dir, "finalized")["valid"]:
            raise AssertionError("initialized 状态不应直接通过 finalized")

        try:
            register_candidate(job_dir, source, "invalid-source-copy", None, None)
        except SkillError:
            pass
        else:
            raise AssertionError("原文不应被注册为候选译本")

        job = load_json(job_dir / "job.json")
        job["route"]["selected"] = "standard-auto"
        job["route"]["decision_reason"] = "双页规则文本样本，用于流水线自测。"
        job["quality"]["selected_fonts"] = [str(_font_path())]
        job["translation"]["mapping_mode"] = "legacy-manual"
        write_json(job_dir / "job.json", job)

        escaped_job = load_json(job_dir / "job.json")
        escaped_job["files"]["candidate"] = "../escaped.pdf"
        write_json(job_dir / "job.json", escaped_job)
        path_probe = root / "path-probe.pdf"
        _make_pdf(path_probe, [["Distinct candidate used for path validation."]])
        try:
            register_candidate(
                job_dir,
                path_probe,
                "invalid-path",
                None,
                None,
            )
        except SkillError:
            pass
        else:
            raise AssertionError("候选内部路径不应越出作业目录")
        write_json(job_dir / "job.json", job)
        set_complex_content(
            job_dir,
            [],
            confirmed_none=True,
            notes="已按原尺寸检查两页原文，均为规则正文，无需专用重建。",
        )

        translation = load_json(job_dir / "translation.json")
        translation["units"] = [
            {
                "id": "p01-title-001",
                "page": 1,
                "kind": "title",
                "source": "Adaptive cache invalidation in distributed systems",
                "translation": (
                    "Invalidation adaptative du cache dans les systèmes distribués"
                ),
                "keep_source_reason": None,
                "review_flags": [],
            },
            {
                "id": "p01-body-001",
                "page": 1,
                "kind": "body",
                "source": "This paper reports a small illustrative sample.",
                "translation": "Cet article présente un petit échantillon illustratif.",
                "keep_source_reason": None,
                "review_flags": [],
            },
            {
                "id": "p01-body-002",
                "page": 1,
                "kind": "body",
                "source": "Association does not establish causation.",
                "translation": "Une association ne prouve pas un lien de causalité.",
                "keep_source_reason": None,
                "review_flags": ["semantic-boundary"],
            },
            {
                "id": "p02-title-001",
                "page": 2,
                "kind": "title",
                "source": "Methods and results",
                "translation": "Méthodes et résultats",
                "keep_source_reason": None,
                "review_flags": [],
            },
            {
                "id": "p02-body-001",
                "page": 2,
                "kind": "body",
                "source": "The sample included 120 participants.",
                "translation": "L'échantillon comprenait 120 participants.",
                "keep_source_reason": None,
                "review_flags": [],
            },
            {
                "id": "p02-body-002",
                "page": 2,
                "kind": "body",
                "source": "Limitations should be interpreted carefully.",
                "translation": "Les limites doivent être interprétées avec prudence.",
                "keep_source_reason": None,
                "review_flags": [],
            },
        ]
        translation["coverage"] = {
            "minimum_source_text_coverage_ratio": 0.85,
            "minimum_candidate_text_presence_ratio": 0.85,
        }
        refresh_coverage(translation)
        translation["terminology_reviewed"] = True
        write_json(job_dir / "translation.json", translation)
        checkpoint = record_work_checkpoint(
            job_dir,
            1,
            "translation",
            "已完成第1页并落盘。",
        )
        if checkpoint["next_page"] != 2:
            raise AssertionError("翻译检查点下一页计算错误")
        checkpoint = record_work_checkpoint(
            job_dir,
            2,
            "translation",
            "双页翻译已全部落盘。",
        )
        if checkpoint["status"] != "complete":
            raise AssertionError("全部页面完成时检查点状态应为 complete")
        try:
            record_work_checkpoint(
                job_dir,
                1,
                "translation",
                "负向测试：禁止倒退。",
            )
        except SkillError:
            pass
        else:
            raise AssertionError("翻译检查点不得倒退")
        translated = validate_job(job_dir, "translated", advance=True)
        _assert_valid(translated, "translated")

        repeated_page_source = json.loads(json.dumps(translation))
        repeated_page_source["units"][0]["source"] = (
            "Adaptive cache invalidation in distributed systems "
            "This paper reports a small illustrative sample. "
            "Association does not establish causation."
        )
        repeated_page_source["units"][1]["source"] = repeated_page_source[
            "units"
        ][0]["source"]
        repeated_source_errors: list[str] = []
        repeated_source_warnings: list[str] = []
        _validate_source_text_coverage(
            source,
            repeated_page_source,
            load_json(job_dir / "retained_source.json"),
            repeated_source_errors,
            repeated_source_warnings,
        )
        if not any(
            "重复绑定同一大段原文" in error
            for error in repeated_source_errors
        ):
            raise AssertionError("多个单元重复绑定整页原文时必须被阻断")

        repeated_translation = json.loads(json.dumps(translation))
        repeated_translation["units"][1]["translation"] = (
            "Première phrase. La même conclusion est répétée ici."
        )
        repeated_translation["units"][2]["translation"] = (
            "La même conclusion est répétée ici. Nouvelle phrase."
        )
        repeated_translation_hits = _adjacent_translation_overlaps(
            repeated_translation["units"]
        )
        if repeated_translation_hits != [
            ("p01-body-001", "p01-body-002", 29)
        ]:
            raise AssertionError(
                "相邻单元跨栏或跨页重复补全译文时必须被稳定识别"
            )
        repeated_translation_errors: list[str] = []
        _validate_translation(
            repeated_translation,
            page_count=2,
            target_language="fr",
            errors=repeated_translation_errors,
        )
        if not any(
            "相邻翻译单元存在源文未对应的重复译文" in error
            for error in repeated_translation_errors
        ):
            raise AssertionError("相邻译文重复必须在 translated 阶段阻断")

        unsourced_commentary = json.loads(json.dumps(translation))
        unsourced_commentary["target_language"] = "zh-Hans"
        unsourced_commentary["units"][1]["translation"] = (
            "本文报告一个小型示例样本，但不能外推为某一产品已经有效。"
        )
        unsourced_errors: list[str] = []
        _validate_translation(
            unsourced_commentary,
            page_count=2,
            target_language="zh-Hans",
            errors=unsourced_errors,
        )
        if not any(
            "含源文无依据的外推限制" in error
            for error in unsourced_errors
        ):
            raise AssertionError("源文没有外推限制时不得把审查意见写入译文正文")

        grounded_commentary = json.loads(json.dumps(unsourced_commentary))
        grounded_commentary["units"][1]["source"] = (
            "This small illustrative sample cannot be generalized to prove "
            "that any product is already effective."
        )
        grounded_errors: list[str] = []
        _validate_translation(
            grounded_commentary,
            page_count=2,
            target_language="zh-Hans",
            errors=grounded_errors,
        )
        if any(
            "含源文无依据的外推限制" in error
            for error in grounded_errors
        ):
            raise AssertionError("源文明示外推限制时不得误报为审查者增译")

        short_cjk_overlap = _adjacent_translation_overlaps(
            [
                {
                    "id": "p03-body-006",
                    "page": 3,
                    "kind": "body",
                    "source": "The difference between",
                    "translation": "上一段较长内容，间接效应2与3之间的差异显著",
                },
                {
                    "id": "p04-body-002",
                    "page": 4,
                    "kind": "body",
                    "source": "the two effects was significant.",
                    "translation": "间接效应2与3之间的差异显著。详细模型见图1。",
                },
            ]
        )
        if short_cjk_overlap != [
            ("p03-body-006", "p04-body-002", 14)
        ]:
            raise AssertionError("跨页重复的短中文续句也必须被识别")

        risk_drift_candidate = root / "risk-drift-candidate.pdf"
        _make_pdf(
            risk_drift_candidate,
            [
                [
                    "Invalidation adaptative du cache dans les systèmes distribués",
                    "Cet article présente un petit échantillon illustratif.",
                    "Une association établit un lien de causalité.",
                ],
                [
                    "Méthodes et résultats",
                    "L'échantillon comprenait 120 participants.",
                    "Les limites doivent être interprétées avec prudence.",
                ],
            ],
        )
        risk_errors: list[str] = []
        risk_warnings: list[str] = []
        _validate_candidate_text_presence(
            risk_drift_candidate,
            translation,
            None,
            risk_errors,
            risk_warnings,
        )
        if not any(
            "p01-body-002" in error and "高风险译文单元" in error
            for error in risk_errors
        ):
            raise AssertionError(
                "整体覆盖率足够时，高风险语义单元的静默改写仍应被阻断"
            )

        missing_heading_candidate = root / "missing-heading-candidate.pdf"
        _make_pdf(
            missing_heading_candidate,
            [
                [
                    "Titre remplacé par erreur",
                    "Cet article présente un petit échantillon illustratif.",
                    "Une association ne prouve pas un lien de causalité.",
                ],
                [
                    "Méthodes et résultats",
                    "L'échantillon comprenait 120 participants.",
                    "Les limites doivent être interprétées avec prudence.",
                ],
            ],
        )
        heading_errors: list[str] = []
        heading_warnings: list[str] = []
        _validate_candidate_text_presence(
            missing_heading_candidate,
            translation,
            None,
            heading_errors,
            heading_warnings,
        )
        if not any(
            "p01-title-001" in error and "高风险译文单元" in error
            for error in heading_errors
        ):
            raise AssertionError(
                "标题完整性必须依据实际译文单元检查，不能依赖固定章节词典"
            )

        english_impostor = root / "english-impostor.pdf"
        _make_pdf(
            english_impostor,
            [
                [
                    "Adaptive cache invalidation in distributed systems",
                    "This paper reports a small illustrative sample.",
                    "Association does not establish causation.",
                ],
                [
                    "Methods and results",
                    "The sample included 120 participants.",
                    "Limitations should be interpreted carefully.",
                ],
            ],
            fontsize=8.6,
            leading=12.0,
        )
        _write_identity_page_map(english_impostor, translation)
        register_candidate(
            job_dir,
            english_impostor,
            "adversarial-test",
            "1.0",
            "英文冒充法文的负向样本",
        )
        impostor_qa = run_qa(job_dir)
        impostor_codes = {
            failure["code"] for failure in impostor_qa["hard_failures"]
        }
        if "TARGET_LANGUAGE_MARKERS_MISSING" not in impostor_codes:
            raise AssertionError("英文候选冒充法文时应被目标语言标记检查阻断")
        if "COMPRESSED_WITH_UNUSED_SPACE" not in impostor_codes:
            raise AssertionError("偏小偏紧且页面留白充足时应被阻断")
        impostor_hash = sha256_file(job_dir / "candidate.pdf")

        generated_candidate = root / "generated-candidate.pdf"
        _make_pdf(
            generated_candidate,
            [
                [
                    "Invalidation adaptative du cache dans les systèmes distribués",
                    "Cet article présente un petit échantillon illustratif.",
                    "Une association ne prouve pas un lien de causalité.",
                ],
                [
                    "Méthodes et résultats",
                    "L'échantillon comprenait 120 participants.",
                    "Les limites doivent être interprétées avec prudence.",
                ],
            ],
        )
        _write_identity_page_map(generated_candidate, translation)
        try:
            register_candidate(
                job_dir,
                generated_candidate,
                "self-test",
                "1.0",
                None,
            )
        except SkillError:
            pass
        else:
            raise AssertionError("重新注册候选时必须记录修复原因")
        provenance_before_preflight = load_json(
            job_dir / "candidate_provenance.json"
        )
        pre_render_translation = load_json(job_dir / "translation.json")
        unit_ids = [
            str(unit["id"]) for unit in pre_render_translation["units"]
        ]
        write_json(
            job_dir / "generator-layout-log.json",
            {
                "algorithm": "self-test-layout",
                "body_font_pt": 9.2,
                "leading_ratio": 1.54,
                "render_contract": {
                    "all_units_consumed": True,
                    "unit_count": len(unit_ids),
                    "unit_ids_sha256": hashlib.sha256(
                        "\n".join(unit_ids).encode("utf-8")
                    ).hexdigest(),
                    "all_complex_items_consumed": True,
                    "complex_item_count": 0,
                    "complex_item_ids_sha256": hashlib.sha256(
                        b""
                    ).hexdigest(),
                    "all_retained_regions_consumed": True,
                    "retained_region_count": 0,
                    "retained_region_ids_sha256": hashlib.sha256(
                        b""
                    ).hexdigest(),
                    "all_text_regions_measured": True,
                    "unmeasured_text_regions": [],
                    "overflow_regions": [],
                    "heading_checks_performed": True,
                    "orphan_regions": [],
                    "cjk_kinsoku_enabled": False,
                    "font_paths": [str(_font_path())],
                },
            },
        )
        pre_render_inventory = load_json(job_dir / "figure_inventory.json")
        pre_render_inventory["inventory_complete"] = True
        pre_render_inventory["candidate_sha256"] = None
        pre_render_inventory["scope_note"] = "双页自测无图、表或截图。"
        write_json(job_dir / "figure_inventory.json", pre_render_inventory)
        readiness = build_pre_render_audit(job_dir)
        if readiness["status"] != "READY_TO_RENDER":
            raise AssertionError(
                f"正常候选导出前总检查失败: {readiness['issues']}"
            )
        metadata_variant = root / "generated-candidate-metadata-variant.pdf"
        fitz = import_fitz()
        metadata_document = fitz.open(generated_candidate)
        metadata = metadata_document.metadata
        metadata["producer"] = "metadata-only-variant"
        metadata_document.set_metadata(metadata)
        metadata_document.save(metadata_variant)
        metadata_document.close()
        _write_identity_page_map(metadata_variant, translation)
        if sha256_file(generated_candidate) == sha256_file(metadata_variant):
            raise AssertionError("元数据变化后的 PDF 文件哈希应不同")
        if _candidate_content_fingerprint(
            generated_candidate
        ) != _candidate_content_fingerprint(metadata_variant):
            raise AssertionError("页面内容相同的 PDF 应得到同一内容指纹")
        duplicate_first = preflight_candidate(
            job_dir,
            generated_candidate,
            "duplicate-content-test",
            "1",
        )
        duplicate_second = preflight_candidate(
            job_dir,
            metadata_variant,
            "duplicate-content-test",
            "1",
        )
        if duplicate_first["preflight_attempt"] != 1:
            raise AssertionError("同一内容首次预检必须记为第1次")
        if (
            duplicate_second["preflight_attempt"] != 1
            or duplicate_second["repeated_candidate"] is not True
            or duplicate_second["staging_ledger_updated"] is not True
        ):
            raise AssertionError(
                "只改变 PDF 元数据不得占用第二次预检，"
                "但必须刷新同一次检查记录"
            )

        limit_one = root / "limit-one.pdf"
        limit_two = root / "limit-two.pdf"
        limit_three = root / "limit-three.pdf"
        _make_pdf(limit_one, [["First broken English candidate."]])
        _make_pdf(
            limit_two,
            [
                ["Second broken English candidate."],
                ["Extra page keeps the failure fingerprint distinct."],
            ],
        )
        _make_pdf(
            limit_three,
            [
                ["Third broken English candidate."],
                ["The renderer should not reach another repair cycle."],
                ["This page exists only for the attempt-limit test."],
            ],
        )
        for candidate in (limit_one, limit_two, limit_three):
            _write_identity_page_map(candidate, translation)
        limit_reports = [
            preflight_candidate(
                job_dir,
                candidate,
                "preflight-limit-test",
                "1",
            )
            for candidate in (limit_one, limit_two, limit_three)
        ]
        if limit_reports[0]["status"] != "NEEDS_REPAIR":
            raise AssertionError("首次失败必须只产生一次集中返修清单")
        if limit_reports[1]["status"] != "GENERATOR_FIX_REQUIRED":
            raise AssertionError("返修版仍失败时必须转为修复排版器")
        if (
            limit_reports[2]["status"] != "GENERATOR_FIX_REQUIRED"
            or limit_reports[2]["preflight_attempt"] != 2
        ):
            raise AssertionError("第三个候选不得开启新的单篇返修轮次")
        tree_before_preflight = _job_tree_digest(job_dir)
        preflight = preflight_candidate(
            job_dir,
            generated_candidate,
            "self-test",
            "1.0",
        )
        if not preflight["valid"]:
            raise AssertionError(
                f"正常候选注册前预检失败: {preflight['validation_errors']}"
            )
        if provenance_before_preflight != load_json(
            job_dir / "candidate_provenance.json"
        ):
            raise AssertionError("注册前预检不得修改正式候选来源记录")
        tree_after_preflight = _job_tree_digest(job_dir)
        if tree_before_preflight != tree_after_preflight:
            changed = sorted(
                name
                for name in set(tree_before_preflight)
                | set(tree_after_preflight)
                if tree_before_preflight.get(name)
                != tree_after_preflight.get(name)
            )
            raise AssertionError(
                "注册前预检使用硬链接副本，正式作业必须逐字节不变；"
                "发生变化的文件: " + ", ".join(changed)
            )
        if not preflight.get("formal_job_unchanged"):
            raise AssertionError("预检必须声明正式作业未被修改")
        register_candidate(
            job_dir,
            generated_candidate,
            "self-test",
            "1.0",
            "确定性双页自测候选",
        )
        candidate = job_dir / "candidate.pdf"
        provenance = load_json(job_dir / "candidate_provenance.json")
        if provenance.get("iteration") != 2:
            raise AssertionError("第二次注册候选时迭代编号应为 2")
        if provenance.get("supersedes_candidate_sha256") != impostor_hash:
            raise AssertionError("新候选必须记录被替代候选的哈希")
        bound_inventory = load_json(job_dir / "figure_inventory.json")
        if (
            bound_inventory.get("inventory_complete") is not True
            or bound_inventory.get("candidate_sha256")
            != sha256_file(candidate)
        ):
            raise AssertionError(
                "已通过同哈希预检的候选注册后应自动绑定图表清单"
            )
        archive = job_dir / "history" / "iteration-0001"
        if not (archive / "candidate.pdf").is_file():
            raise AssertionError("上一轮候选 PDF 未归档")
        if not (archive / "qa.json").is_file():
            raise AssertionError("上一轮 QA 证据未归档")
        archive_manifest = load_json(archive / "archive_manifest.json")
        if archive_manifest.get("candidate_sha256") != impostor_hash:
            raise AssertionError("历史归档候选哈希不一致")
        if (
            archive_manifest.get("storage_strategy")
            != "hardlink-with-copy-fallback"
        ):
            raise AssertionError("历史归档必须记录轻量快照策略")
        third_candidate = root / "third-formal-candidate.pdf"
        _make_pdf(
            third_candidate,
            [
                ["Troisième version distincte."],
                ["Elle ne doit pas ouvrir une nouvelle réparation."],
            ],
        )
        _write_identity_page_map(third_candidate, translation)
        try:
            register_candidate(
                job_dir,
                third_candidate,
                "self-test",
                "2.0",
                "尝试登记第三个正式候选",
            )
        except SkillError:
            pass
        else:
            raise AssertionError("平衡档默认不得注册第三个正式候选")
        qa = run_qa(job_dir)
        if qa["automatic_decision"] != "READY_FOR_HUMAN_REVIEW":
            raise AssertionError(f"QA 未进入人工审查: {qa['hard_failures']}")
        if any(page["null_characters"] for page in qa["candidate_pages"]):
            raise AssertionError("正常候选不应含 PDF 文本层空字符")
        review_sheet = make_review_sheet(
            job_dir,
            dpi=72,
            pages_per_sheet=2,
            detail_page_spec="2",
            detail_dpi=120,
        )
        if review_sheet["sheet_count"] != 1:
            raise AssertionError("双页自测应合并为一张审查图")
        if len(review_sheet["detail_pairs"]) != 1:
            raise AssertionError("疑点页应能按需生成单页高清源译对照")
        cached_review_sheet = make_review_sheet(
            job_dir,
            dpi=72,
            pages_per_sheet=2,
        )
        if not cached_review_sheet["cache_hit"]:
            raise AssertionError("候选哈希未变化时应复用审查图缓存")
        cached_sheet_path = Path(cached_review_sheet["sheets"][0])
        cached_sheet_path.write_bytes(b"tampered")
        rebuilt_review_sheet = make_review_sheet(
            job_dir,
            dpi=72,
            pages_per_sheet=2,
        )
        if rebuilt_review_sheet["cache_hit"]:
            raise AssertionError("审查图内容哈希变化后不得复用缓存")
        candidate_report = validate_job(job_dir, "candidate", advance=True)
        _assert_valid(candidate_report, "candidate")
        risk_report = build_review_risk_report(job_dir)
        if risk_report["page_count"] != 2:
            raise AssertionError("复审风险报告页数不正确")
        if not all(
            "semantic_review_units" in page
            for page in risk_report["pages"]
        ):
            raise AssertionError("复审风险报告必须携带高风险语义单元")
        if any(
            page["suspicious_search_chars"]
            for page in risk_report["pages"]
        ):
            raise AssertionError("正常候选不应含检索层兼容字符")
        translation_with_year = load_json(job_dir / "translation.json")
        translation_with_year["units"][1]["source"] += " Published in 2016."
        translation_with_year["units"][1]["translation"] += " Publié récemment."
        write_json(job_dir / "translation.json", translation_with_year)
        year_risk_report = build_review_risk_report(job_dir)
        if "2016" not in year_risk_report["pages"][0]["missing_years"]:
            raise AssertionError("正文翻译单元缺失年份时应进入引文核对")
        write_json(job_dir / "translation.json", translation)
        structure = extract_source_structure(job_dir / "source.pdf")
        if structure["page_count"] != 2:
            raise AssertionError("原文结构提取页数不正确")
        write_json(job_dir / "source_structure.json", structure)
        completeness = build_completeness_audit(job_dir)
        if completeness["decision"] == "NEEDS_REPAIR":
            raise AssertionError(
                "正常双页候选不应被翻译完整性审计阻断: "
                f"{completeness['flag_counts']}"
            )
        repair_tasks = _repair_tasks(
            [
                {
                    "page": 2,
                    "flags": [
                        "SEVERE_TRANSLATION_COMPRESSION",
                        "STATISTICAL_ANCHOR_LOSS",
                    ],
                    "notes": [],
                    "translation_source_ratio": 0.12,
                    "sentence_retention_ratio": 0.5,
                    "missing_statistics": [".42", "95%"],
                    "missing_citations": [],
                    "missing_acronyms": [],
                    "missing_urls": [],
                    "missing_dois": [],
                    "missing_headings": [],
                    "shifted_headings": [],
                    "visual_rebuild_issues": [],
                }
            ]
        )
        if len(repair_tasks) != 1:
            raise AssertionError("完整性问题必须生成一项可执行返修任务")
        if "translation" not in repair_tasks[0]["layers"]:
            raise AssertionError("摘要化问题的返修任务必须返回翻译层")
        if not any("统计值" in action for action in repair_tasks[0]["actions"]):
            raise AssertionError("统计锚点丢失必须生成补回统计值的动作")

        inventory = load_json(job_dir / "figure_inventory.json")
        inventory["inventory_complete"] = True
        inventory["candidate_sha256"] = sha256_file(candidate)
        inventory["scope_note"] = "自测样本无图、表或截图。"
        write_json(job_dir / "figure_inventory.json", inventory)
        retained = load_json(job_dir / "retained_source.json")
        retained["regions"] = [
            {
                "page": 1,
                "bbox": [0, 0, 595.276, 841.89],
                "category": "references",
                "reason": "负向测试：错误地把正文整页标为参考文献。",
            }
        ]
        write_json(job_dir / "retained_source.json", retained)
        if validate_job(job_dir, "accepted")["valid"]:
            raise AssertionError("整页参考文献白名单不应覆盖普通正文页")
        retained["regions"] = []
        write_json(job_dir / "retained_source.json", retained)

        set_review_mode(job_dir, "off")
        job = load_json(job_dir / "job.json")
        if job["review"]["mode"] != "none":
            raise AssertionError("快速模式迁移未写入 job.review")
        if load_json(job_dir / "finalization.json")["review_mode"] != "none":
            raise AssertionError("快速模式迁移未同步正式记录")
        fast_accepted = validate_job(job_dir, "accepted")
        _assert_valid(fast_accepted, "fast accepted")

        set_review_mode(job_dir, "on")
        job = load_json(job_dir / "job.json")
        if job["review"]["mode"] != "independent":
            raise AssertionError("审校模式迁移未写入 job.review")
        if (
            load_json(job_dir / "finalization.json")["review_mode"]
            != "independent"
        ):
            raise AssertionError("审校模式迁移未同步正式记录")
        if validate_job(job_dir, "accepted")["valid"]:
            raise AssertionError("审校模式未完成独立检查时不应通过")

        review = load_json(job_dir / "reviews" / "independent.json")
        review["decision"] = "PASS"
        review["coverage"] = ["2/2 pages", "all translation units"]
        review["reviewed_pages"] = [1, 2]
        review["issues"] = []
        review["residual_risks"] = []
        review["reviewed_at"] = utc_now()
        review["reviewer_role"] = "independent"
        review["reviewer_id"] = "self-test-independent"
        review["source_sha256"] = sha256_file(job_dir / "source.pdf")
        review["candidate_sha256"] = sha256_file(candidate)
        write_json(job_dir / "reviews" / "independent.json", review)
        first_round = record_review_round(job_dir)
        if first_round["round_number"] != 1:
            raise AssertionError("平衡档应记录一轮完整独立复审")

        accepted = validate_job(job_dir, "accepted", advance=True)
        _assert_valid(accepted, "accepted")

        set_review_mode(job_dir, "precise")
        job = load_json(job_dir / "job.json")
        if job["review"]["mode"] != "precise":
            raise AssertionError("精细档迁移未写入 job.review")
        precise_accepted = validate_job(job_dir, "accepted")
        _assert_valid(precise_accepted, "precise accepted")
        try:
            record_review_round(job_dir)
        except SkillError:
            pass
        else:
            raise AssertionError("复审轮次不得超过作业配置上限")

        outside_dir = root / "outside-output"
        outside_dir.mkdir()
        outside_formal = outside_dir / "source_fr.pdf"
        outside_formal.write_bytes(candidate.read_bytes())
        finalization = load_json(job_dir / "finalization.json")
        finalization["formal_pdf"] = str(outside_formal)
        finalization["sha256"] = sha256_file(outside_formal)
        write_json(job_dir / "finalization.json", finalization)
        outside_report = validate_job(job_dir, "finalized")
        if not any(
            "当前批次的 output" in error
            for error in outside_report["errors"]
        ):
            raise AssertionError("批次正式译本不得写到 output 之外")

        formal = formal_dir / "source_fr.pdf"
        formal.write_bytes(source.read_bytes())
        finalization["formal_pdf"] = str(formal)
        finalization["sha256"] = sha256_file(formal)
        write_json(job_dir / "finalization.json", finalization)
        if validate_job(job_dir, "finalized")["valid"]:
            raise AssertionError("正式译本必须与通过 QA 的候选哈希一致")

        formal.write_bytes(candidate.read_bytes())
        finalization["formal_pdf"] = str(formal)
        finalization["sha256"] = sha256_file(formal)
        write_json(job_dir / "finalization.json", finalization)
        finalized = validate_job(job_dir, "finalized", advance=True)
        _assert_valid(finalized, "finalized")

        corpus = audit_corpus(root)
        if corpus["pdf_count"] < 2 or corpus["total_pages"] < 4:
            raise AssertionError("语料库审计未覆盖自测 PDF")
        corpus_paths = {item["path"] for item in corpus["documents"]}
        if any(
            path.endswith("/output/source_fr.pdf")
            for path in corpus_paths
        ):
            raise AssertionError("语料审计必须从语言配置识别拉丁语言译本")

        reviewed_translation = root / "systems_中文译版_审校版.pdf"
        _make_pdf(
            reviewed_translation,
            [["分布式系统中的自适应缓存失效策略。"]],
        )
        refreshed_corpus = audit_corpus(root)
        if any(
            item["path"] == reviewed_translation.name
            for item in refreshed_corpus["documents"]
        ):
            raise AssertionError("审校版后缀必须从语言配置识别，不能写死四种语言")


def main() -> int:
    try:
        run()
        print("SELF TEST PASS")
        return 0
    except Exception as exc:
        print(f"SELF TEST FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
