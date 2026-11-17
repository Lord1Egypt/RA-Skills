"""Story 构建的第二层：表格与图片的 Flowable。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。这一层把已经整形好的
表格矩阵和图片载荷变成 ReportLab 对象，只关心"画成什么样"，不关心
"这一页该放谁"——那是 ``story`` 的事。

只依赖 ``story_text``（拿注入包和异常类）与表格数据整形，不回指上层。
PyMuPDF 与界面文案照 ``StoryDeps`` 的约定由调用侧注入。
"""

from __future__ import annotations

import html
import io
import math
from typing import Any

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from .font_runs import _markup
from .story_text import StoryDeps, StoryError
from .table_data import (
    TableDataError,
    _column_widths,
    _table_emphasis_rows,
    _table_matrix,
    _table_note_text,
)


def _table_matrix_or_story_error(
    table: dict[str, Any],
) -> tuple[list[list[str]], list[tuple]]:
    """表格数据层的异常翻译成 Story 层的异常，文案原样透传。

    再往上由 ``scripts/build_candidate.py`` 翻回 SkillError，对外行为不变。
    """

    try:
        return _table_matrix(table)
    except TableDataError as exc:
        raise StoryError(str(exc)) from exc


def _table_flowables(
    item: dict[str, Any],
    *,
    styles: dict[str, ParagraphStyle],
    available_width: float,
) -> list[Flowable]:
    result: list[Flowable] = []
    for table_index, table in enumerate(
        item.get("payload", {}).get("tables", [])
    ):
        if not isinstance(table, dict):
            continue
        title = str(
            table.get("translated_title")
            or table.get("title_translation")
            or table.get("title")
            or table.get("caption")
            or ""
        ).strip()
        if title:
            result.append(Paragraph(_markup(title), styles["caption"]))
        matrix, spans = _table_matrix_or_story_error(table)
        header_rows = min(
            max(int(table.get("header_rows") or 1), 1),
            len(matrix),
        )
        emphasis_rows = _table_emphasis_rows(
            table,
            row_count=len(matrix),
            header_rows=header_rows,
        )
        table_font_size = styles["table"].fontSize
        configured_font_size = table.get("font_size_pt")
        if isinstance(configured_font_size, (int, float)):
            table_font_size = min(
                table_font_size,
                max(6.0, float(configured_font_size)),
            )
        table_style = ParagraphStyle(
            f"table-{table_index}",
            parent=styles["table"],
            fontSize=table_font_size,
            leading=max(table_font_size * 1.24, table_font_size + 1.6),
        )
        table_header_style = ParagraphStyle(
            f"table-header-{table_index}",
            parent=styles["table_header"],
            fontSize=table_font_size,
            leading=max(table_font_size * 1.24, table_font_size + 1.6),
        )
        bold_cells = table.get("bold_cells")
        bold_font_name = styles["table_header"].fontName

        def _cell_paragraph(
            row_index: int,
            col_index: int,
            cell: str,
            *,
            # 下面几个都是循环内的变量。用默认值在定义时当场绑定，
            # 取值和原来的闭包写法一模一样，只是不再依赖晚绑定。
            bold_cells: Any = bold_cells,
            bold_font_name: str = bold_font_name,
            header_rows: int = header_rows,
            emphasis_rows: Any = emphasis_rows,
            table_header_style: ParagraphStyle = table_header_style,
            table_style: ParagraphStyle = table_style,
        ):
            markup = _markup(cell)
            if (
                isinstance(bold_cells, list)
                and row_index < len(bold_cells)
                and isinstance(bold_cells[row_index], list)
                and col_index < len(bold_cells[row_index])
                and bold_cells[row_index][col_index]
            ):
                # 原表用粗体标各列最优值，这是语义不是装饰，必须跟到中文表里。
                markup = (
                    f'<font name="{html.escape(bold_font_name, quote=True)}">'
                    f"{markup}</font>"
                )
            return Paragraph(
                markup,
                (
                    table_header_style
                    if row_index < header_rows
                    or row_index in emphasis_rows
                    else table_style
                ),
            )

        data = [
            [
                _cell_paragraph(row_index, col_index, cell)
                for col_index, cell in enumerate(row)
            ]
            for row_index, row in enumerate(matrix)
        ]
        cell_padding = table.get("cell_padding_pt")
        cell_padding_pt = (
            min(6.0, max(1.5, float(cell_padding)))
            if isinstance(cell_padding, (int, float))
            else 4.0
        )
        table_flowable = Table(
            data,
            colWidths=_column_widths(
                matrix,
                available_width,
                table.get("column_width_weights"),
            ),
            repeatRows=header_rows,
            hAlign="CENTER",
            splitByRow=1,
        )
        commands: list[tuple] = [
            ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#7A858D")),
            (
                "BACKGROUND",
                (0, 0),
                (-1, header_rows - 1),
                colors.HexColor("#E9EFF1"),
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                table_style.fontName,
            ),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), cell_padding_pt),
            ("RIGHTPADDING", (0, 0), (-1, -1), cell_padding_pt),
            ("TOPPADDING", (0, 0), (-1, -1), cell_padding_pt),
            ("BOTTOMPADDING", (0, 0), (-1, -1), cell_padding_pt),
        ]
        for row_index in sorted(emphasis_rows):
            commands.append(
                (
                    "BACKGROUND",
                    (0, row_index),
                    (-1, row_index),
                    colors.HexColor("#FFF6DD"),
                )
            )
        commands.extend(spans)
        table_flowable.setStyle(TableStyle(commands))
        result.append(table_flowable)
        raw_notes = (
            table.get("notes")
            or table.get("footnotes")
            or table.get("note")
            or table.get("footnote")
            or []
        )
        if isinstance(raw_notes, (str, dict)):
            raw_notes = [raw_notes]
        for raw_note in raw_notes if isinstance(raw_notes, list) else []:
            note = _table_note_text(raw_note)
            if note:
                result.append(Paragraph(_markup(note), styles["table_note"]))
        doi = str(table.get("doi") or "").strip()
        if doi:
            result.append(
                Paragraph(_markup(f"DOI: {doi}"), styles["table_note"])
            )
        if table_index + 1 < len(item.get("payload", {}).get("tables", [])):
            result.append(Spacer(1, 10))
    return result


def _image_clip_bbox(region: dict[str, Any]) -> list[float] | None:
    source_bbox = region.get("source_bbox")
    if not (
        isinstance(source_bbox, list)
        and len(source_bbox) == 4
        and all(isinstance(value, (int, float)) for value in source_bbox)
    ):
        return None
    x0, y0, x1, y1 = map(float, source_bbox)
    localized_caption = region.get("localized_caption")
    caption_bbox = (
        localized_caption.get("source_bbox")
        if isinstance(localized_caption, dict)
        else None
    )
    if not (
        isinstance(caption_bbox, list)
        and len(caption_bbox) == 4
        and all(isinstance(value, (int, float)) for value in caption_bbox)
    ):
        return [x0, y0, x1, y1]
    caption_x0, caption_y0, caption_x1, caption_y1 = map(
        float,
        caption_bbox,
    )
    horizontal_overlap = max(
        0.0,
        min(x1, caption_x1) - max(x0, caption_x0),
    )
    minimum_overlap = min(x1 - x0, caption_x1 - caption_x0) * 0.35
    if horizontal_overlap < minimum_overlap:
        return [x0, y0, x1, y1]
    midpoint = (y0 + y1) / 2
    if midpoint <= caption_y0 < y1:
        adjusted_bottom = caption_y0 - 0.75
        if adjusted_bottom - y0 >= 24.0:
            y1 = adjusted_bottom
    elif y0 < caption_y1 <= midpoint:
        adjusted_top = caption_y1 + 0.75
        if y1 - adjusted_top >= 24.0:
            y0 = adjusted_top
    return [x0, y0, x1, y1]


def _image_flowables(
    item: dict[str, Any],
    *,
    deps: StoryDeps,
    source_document: Any,
    styles: dict[str, ParagraphStyle],
    available_width: float,
    available_height: float,
    target_language: str = "zh-Hans",
) -> list[Flowable]:
    payload = (
        item.get("payload")
        if isinstance(item.get("payload"), dict)
        else {}
    )
    regions = [
        region
        for region in payload.get("regions", [])
        if isinstance(region, dict)
    ]
    def build_panel(
        region: dict[str, Any],
        *,
        panel_width: float,
        side_by_side: bool,
    ) -> list[Flowable]:
        image_bytes: bytes | None = None
        xref = region.get("xref")
        if isinstance(xref, int):
            try:
                image_bytes = source_document.extract_image(xref)["image"]
            except Exception:
                image_bytes = None
        if image_bytes is None:
            page_number = int(region.get("page") or item["page"])
            page = source_document[page_number - 1]
            clip = _image_clip_bbox(region)
            rectangle = (
                deps.import_fitz_fn().Rect(*map(float, clip))
                if isinstance(clip, list) and len(clip) == 4
                else page.rect
            )
            pixmap = page.get_pixmap(
                matrix=deps.import_fitz_fn().Matrix(1.6, 1.6),
                clip=rectangle,
                alpha=False,
            )
            image_bytes = pixmap.tobytes("png")
        image = Image(io.BytesIO(image_bytes))
        default_width_ratio = 0.48 if side_by_side else 0.72
        width_ratio = _bounded_float(
            region.get(
                "display_width_ratio",
                payload.get("display_width_ratio"),
            ),
            default=default_width_ratio,
            lower=0.3,
            upper=0.49 if side_by_side else 1.0,
        )
        max_height = _bounded_float(
            region.get(
                "display_max_height_pt",
                payload.get("display_max_height_pt"),
            ),
            default=260.0,
            lower=120.0,
            upper=520.0,
        )
        max_width = min(
            panel_width,
            available_width * width_ratio,
        )
        scale = min(
            max_width / max(image.imageWidth, 1),
            max_height / max(image.imageHeight, 1),
        )
        image.drawWidth = image.imageWidth * scale
        image.drawHeight = image.imageHeight * scale
        image.hAlign = "CENTER"
        caption = str(
            region.get("translation")
            or region.get("caption")
            or ""
        ).strip()
        media: list[Flowable] = [image]
        if caption:
            media.extend(
                [
                    Spacer(1, 4),
                    Paragraph(_markup(caption), styles["caption"]),
                ]
            )
        panel: list[Flowable] = (
            [KeepTogether(media)]
            if caption and not side_by_side
            else media
        )
        localized_labels = _localized_image_labels(region)
        if localized_labels:
            panel.extend(
                _localized_image_label_flowables(
                    localized_labels,
                    deps=deps,
                    styles=styles,
                    available_width=panel_width,
                    target_language=target_language,
                    show_source=any(
                        source for source, _ in localized_labels
                    ),
                    keep_heading_with_first=not side_by_side,
                )
            )
        return panel

    if not regions:
        return []
    if len(regions) == 1:
        return build_panel(
            regions[0],
            panel_width=available_width,
            side_by_side=False,
        )
    columns = 2
    panel_width = available_width / columns - 8
    panels = [
        build_panel(
            region,
            panel_width=panel_width,
            side_by_side=True,
        )
        for region in regions
    ]
    rows = [
        panels[index : index + columns]
        for index in range(0, len(panels), columns)
    ]
    for row in rows:
        row.extend(
            [[Spacer(1, 1)] for _ in range(columns - len(row))]
        )
    data = rows
    widths = [available_width / columns] * columns
    table = Table(data, colWidths=widths, hAlign="CENTER")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    styles["caption"].fontName,
                ),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    try:
        _, table_height = table.wrap(available_width, available_height)
    except Exception:
        table_height = available_height + 1
    if table_height <= available_height:
        return [table]

    sequential: list[Flowable] = []
    for index, region in enumerate(regions):
        if index:
            sequential.append(Spacer(1, 12))
        sequential.extend(
            build_panel(
                region,
                panel_width=available_width,
                side_by_side=False,
            )
        )
    return sequential


def _bounded_float(
    value: Any,
    *,
    default: float,
    lower: float,
    upper: float,
) -> float:
    if isinstance(value, bool):
        return default
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(parsed):
        return default
    return min(max(parsed, lower), upper)


def _localized_image_labels(
    region: dict[str, Any],
) -> list[tuple[str, str]]:
    raw_labels = region.get("localized_labels")
    if not isinstance(raw_labels, list):
        return []
    labels: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for raw_label in raw_labels:
        if isinstance(raw_label, str):
            translation = raw_label.strip()
            pair = ("", translation)
            if translation and pair not in seen:
                labels.append(pair)
                seen.add(pair)
            continue
        if not isinstance(raw_label, dict):
            continue
        source = _image_label_text(
            raw_label.get("source")
            or raw_label.get("source_text")
            or raw_label.get("label")
            or raw_label.get("original")
            or ""
        )
        translation = _image_label_text(
            raw_label.get("translation")
            or raw_label.get("target")
            or raw_label.get("localized")
            or ""
        )
        if source and translation and source == translation:
            continue
        pair = (source, translation)
        if (source or translation) and pair not in seen:
            labels.append(pair)
            seen.add(pair)
    return labels


def _image_label_text(value: Any) -> str:
    if isinstance(value, list):
        return "、".join(
            str(item).strip()
            for item in value
            if str(item).strip()
        )
    return str(value or "").strip()


def _localized_image_label_flowables(
    labels: list[tuple[str, str]],
    *,
    deps: StoryDeps,
    styles: dict[str, ParagraphStyle],
    available_width: float,
    target_language: str = "zh-Hans",
    show_source: bool = False,
    keep_heading_with_first: bool = True,
) -> list[Flowable]:
    cells: list[Flowable] = []
    for source, translation in labels:
        if show_source and source:
            text = (
                f"<font color='#60727A'>{_markup(source)}</font>"
                f"<br/>{_markup(translation or source)}"
            )
        else:
            text = _markup(translation or source)
        if text:
            cells.append(Paragraph(text, styles["table_note"]))
    if not cells:
        return []

    rows: list[list[Flowable]] = []
    for index in range(0, len(cells), 2):
        row = cells[index : index + 2]
        if len(row) == 1:
            row.append(Spacer(1, 1))
        rows.append(row)

    def make_table(table_rows: list[list[Flowable]]) -> Table:
        table = Table(
            table_rows,
            colWidths=[available_width / 2] * 2,
            hAlign="CENTER",
            splitByRow=1,
        )
        commands: list[tuple[Any, ...]] = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B0BEC5")),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]
        for row_index in range(1, len(table_rows), 2):
            commands.append(
                (
                    "BACKGROUND",
                    (0, row_index),
                    (-1, row_index),
                    colors.HexColor("#F7F8F9"),
                )
            )
        table.setStyle(TableStyle(commands))
        return table

    heading = Paragraph(
        deps.message_fn(target_language, "image_text_legend"),
        styles["table_note"],
    )
    if not keep_heading_with_first:
        return [
            Spacer(1, 5),
            heading,
            make_table(rows),
        ]
    result: list[Flowable] = [
        Spacer(1, 5),
        KeepTogether([heading, make_table(rows[:1])]),
    ]
    if len(rows) > 1:
        result.append(make_table(rows[1:]))
    return result
