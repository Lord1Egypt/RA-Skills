"""矢量图 Flowable：把结构化图载荷直接画进候选 PDF。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。它只依赖
reportlab 与包内的字体分段工具，不碰作业目录，也不读写文件。

两处原来的 scripts 层依赖按包内规则改写：异常改成本模块自己的
``VectorFigureError``，由调用侧翻译回 SkillError；界面文案由调用侧
用 ``message_fn`` 注入。
"""

from __future__ import annotations

import html
import math
from collections import defaultdict
from collections.abc import Callable
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Flowable, Paragraph

from .font_runs import _edge_label_lines, _markup

#: 载荷里能真的画出东西的键。少了它们，VectorPayloadFlowable 只会把
#: ``labels`` 排成几行字——一张图都没有，检查却全绿。所以这份名单同时
#: 是渲染依据和"这份载荷画得出来吗"的判据。
DRAWABLE_FIGURE_KEYS = (
    "nodes",
    "edges",
    "connectors",
    "series",
    "panels",
    "circles",
    "levels",
)


def figure_payload_is_drawable(figure: Any) -> bool:
    """这份图载荷能画出真实绘图对象吗。"""

    if not isinstance(figure, dict):
        return False
    return any(figure.get(key) for key in DRAWABLE_FIGURE_KEYS)


class VectorFigureError(RuntimeError):
    """矢量图载荷不合法。

    以前抛的是 scripts 层的 SkillError；包不该依赖 scripts，所以这里
    自己定义。调用侧把它翻译回 SkillError，对外行为不变。
    """


class VectorPayloadFlowable(Flowable):
    def __init__(
        self,
        figure: dict[str, Any],
        *,
        width: float,
        regular_font: str,
        bold_font: str,
        body_font_pt: float,
        target_language: str = "zh-Hans",
        message_fn: Callable[..., str],
    ) -> None:
        super().__init__()
        self.figure = figure
        self.message_fn = message_fn
        self.width = width
        self.regular_font = regular_font
        self.bold_font = bold_font
        self.body_font_pt = body_font_pt
        self.target_language = target_language
        self.maximum_height = float(
            figure.get("height_pt")
            or min(300, max(150, width * 0.48))
        )
        self.height = self.maximum_height

    def wrap(self, available_width: float, available_height: float) -> tuple[float, float]:
        self.width = min(self.width, available_width)
        has_structured_graph = figure_payload_is_drawable(self.figure)
        if has_structured_graph:
            measured_height = self.maximum_height
        else:
            measured_height = self._label_layout_height(self.width)
        minimum_height = 80 if has_structured_graph else 42
        self.height = min(
            max(measured_height, minimum_height),
            self.maximum_height,
            max(available_height, minimum_height),
        )
        return self.width, self.height

    def _label_style(self, index: int, label: str) -> ParagraphStyle:
        compact = " ".join(label.split())
        title_like = index in {0, 3}
        heading_like = (
            not title_like
            and len(compact) <= 12
            and not compact.endswith(("。", "；", ".", ";"))
        )
        metadata_like = index in {1, 2, 4, 5}
        if title_like:
            font_size = max(12.5, self.body_font_pt * 1.35)
            leading = max(18, self.body_font_pt * 1.65)
            alignment = TA_CENTER
            font_name = self.bold_font
        elif heading_like:
            font_size = max(11.0, self.body_font_pt * 1.12)
            leading = max(16, self.body_font_pt * 1.5)
            alignment = TA_LEFT
            font_name = self.bold_font
        elif metadata_like:
            font_size = max(8.5, self.body_font_pt * 0.86)
            leading = max(12.5, self.body_font_pt * 1.25)
            alignment = TA_CENTER
            font_name = self.regular_font
        else:
            font_size = self.body_font_pt
            leading = self.body_font_pt * 1.58
            alignment = TA_LEFT
            font_name = self.regular_font
        return ParagraphStyle(
            f"vector-label-{index}",
            fontName=font_name,
            fontSize=font_size,
            leading=leading,
            alignment=alignment,
            textColor=colors.HexColor("#17252B"),
            wordWrap="CJK",
            spaceAfter=3,
        )

    def _label_layout_height(self, width: float) -> float:
        labels = [
            str(value)
            for value in self.figure.get("labels", [])
            if str(value).strip()
        ]
        height = 16.0
        for index, label in enumerate(labels):
            paragraph = Paragraph(
                _markup(label),
                self._label_style(index, label),
            )
            _, paragraph_height = paragraph.wrap(width - 16, 10000)
            height += paragraph_height + 4
        return height

    def _draw_edge_label(
        self,
        canvas,
        label: str,
        x: float,
        y: float,
    ) -> None:
        lines = _edge_label_lines(label)
        if not lines:
            return
        font_size = max(7.2, self.body_font_pt * 0.72)
        line_height = font_size * 1.25
        text_width = max(
            pdfmetrics.stringWidth(
                line,
                self.regular_font,
                font_size,
            )
            for line in lines
        )
        first_baseline = y + (len(lines) - 1) * line_height / 2
        box_bottom = y - (len(lines) - 1) * line_height / 2 - 2.0
        box_height = (
            (len(lines) - 1) * line_height
            + font_size
            + 3.5
        )
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#FAFCFC"))
        canvas.roundRect(
            x - text_width / 2 - 2.5,
            box_bottom,
            text_width + 5.0,
            box_height,
            1.5,
            stroke=0,
            fill=1,
        )
        canvas.setFillColor(colors.HexColor("#26383F"))
        canvas.setFont(self.regular_font, font_size)
        for index, line in enumerate(lines):
            canvas.drawCentredString(
                x,
                first_baseline - index * line_height,
                line,
            )
        canvas.restoreState()

    @staticmethod
    def _arrow_head(
        canvas,
        tip: tuple[float, float],
        tail: tuple[float, float],
    ) -> None:
        x2, y2 = tip
        x1, y1 = tail
        angle = math.atan2(y2 - y1, x2 - x1)
        size = 5.5
        for delta in (2.55, -2.55):
            canvas.line(
                x2,
                y2,
                x2 + size * math.cos(angle + delta),
                y2 + size * math.sin(angle + delta),
            )

    def _arrow(
        self,
        canvas,
        start: tuple[float, float],
        end: tuple[float, float],
        label: str = "",
        *,
        direction: str = "forward",
        line_style: str = "solid",
        label_t: float = 0.5,
        label_offset: float = 4.0,
        label_position: tuple[float, float] | None = None,
    ) -> None:
        x1, y1 = start
        x2, y2 = end
        canvas.saveState()
        if line_style == "dashed":
            canvas.setDash(4, 3)
        canvas.line(x1, y1, x2, y2)
        canvas.setDash()
        if direction == "inhibitory":
            angle = math.atan2(y2 - y1, x2 - x1)
            bar = 4.5
            perpendicular = angle + math.pi / 2
            canvas.line(
                x2 - bar * math.cos(perpendicular),
                y2 - bar * math.sin(perpendicular),
                x2 + bar * math.cos(perpendicular),
                y2 + bar * math.sin(perpendicular),
            )
        else:
            self._arrow_head(canvas, end, start)
        if direction == "bidirectional":
            self._arrow_head(canvas, start, end)
        canvas.restoreState()
        if label:
            if label_position is None:
                label_x = x1 + (x2 - x1) * label_t
                label_y = y1 + (y2 - y1) * label_t
                line_length = math.hypot(x2 - x1, y2 - y1) or 1.0
                label_x += -(y2 - y1) / line_length * label_offset
                label_y += (x2 - x1) / line_length * label_offset
            else:
                label_x, label_y = label_position
            self._draw_edge_label(
                canvas,
                label,
                label_x,
                label_y,
            )

    def _curved_covariance(
        self,
        canvas,
        source: tuple[float, float, float, float],
        target: tuple[float, float, float, float],
        label: str,
        *,
        variant: int,
    ) -> None:
        source_center = (
            source[0] + source[2] / 2,
            source[1] + source[3] / 2,
        )
        target_center = (
            target[0] + target[2] / 2,
            target[1] + target[3] / 2,
        )
        delta_x = target_center[0] - source_center[0]
        delta_y = target_center[1] - source_center[1]
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#45636F"))
        canvas.setLineWidth(0.8)
        if abs(delta_y) >= abs(delta_x):
            start = (source[0], source_center[1])
            end = (target[0], target_center[1])
            span = abs(delta_y)
            offset = min(
                self.width * 0.34,
                28.0 + span * 0.18 + (variant % 3) * 5.0,
            )
            control_1 = (start[0] - offset, start[1])
            control_2 = (end[0] - offset, end[1])
        else:
            start = (source_center[0], source[1] + source[3])
            end = (target_center[0], target[1] + target[3])
            span = abs(delta_x)
            offset = min(
                self.height * 0.28,
                24.0 + span * 0.14 + (variant % 3) * 5.0,
            )
            control_1 = (start[0], start[1] + offset)
            control_2 = (end[0], end[1] + offset)
        canvas.bezier(
            start[0],
            start[1],
            control_1[0],
            control_1[1],
            control_2[0],
            control_2[1],
            end[0],
            end[1],
        )
        self._arrow_head(canvas, start, control_1)
        self._arrow_head(canvas, end, control_2)
        canvas.restoreState()
        if label:
            label_x = (
                start[0]
                + 3 * control_1[0]
                + 3 * control_2[0]
                + end[0]
            ) / 8
            label_y = (
                start[1]
                + 3 * control_1[1]
                + 3 * control_2[1]
                + end[1]
            ) / 8
            self._draw_edge_label(canvas, label, label_x, label_y)

    def _node_paragraph(
        self,
        index: int,
        label: str,
    ) -> Paragraph:
        return Paragraph(
            _markup(label),
            ParagraphStyle(
                f"vector-node-{index}",
                fontName=self.regular_font,
                fontSize=max(7.2, self.body_font_pt * 0.72),
                leading=max(10, self.body_font_pt * 1.0),
                alignment=TA_CENTER,
                textColor=colors.HexColor("#17313A"),
                wordWrap="CJK",
            ),
        )

    def _draw_nodes(self, canvas, nodes: list[dict[str, Any]], edges: list[Any]) -> None:
        count = len(nodes)
        columns = max(1, math.ceil(math.sqrt(count)))
        rows = max(1, math.ceil(count / columns))
        cell_width = self.width / columns
        cell_height = self.height / rows
        positions: dict[str, tuple[float, float, float, float]] = {}
        centers: dict[str, tuple[float, float]] = {}
        labels: dict[str, str] = {}
        node_order: list[str] = []
        for index, node in enumerate(nodes):
            column = index % columns
            row = rows - 1 - index // columns
            width = float(
                node.get("width_pt")
                or (
                    float(node["width_ratio"]) * self.width
                    if isinstance(node.get("width_ratio"), (int, float))
                    else min(140, cell_width * 0.7)
                )
            )
            height = float(
                node.get("height_pt")
                or (
                    float(node["height_ratio"]) * self.height
                    if isinstance(node.get("height_ratio"), (int, float))
                    else min(48, cell_height * 0.45)
                )
            )
            width = min(max(width, 18.0), self.width - 8.0)
            height = min(max(height, 12.0), self.height - 8.0)
            if str(node.get("type") or "").lower() == "latent-variable":
                width = min(
                    width,
                    max(72.0, min(88.0, self.width * 0.16)),
                )
            center_x_ratio = (
                node.get("center_x_ratio")
                if isinstance(node.get("center_x_ratio"), (int, float))
                else node.get("x_ratio")
            )
            if isinstance(center_x_ratio, (int, float)):
                center_x = float(center_x_ratio) * self.width
            else:
                x = float(
                    node.get("x_pt")
                    or column * cell_width + (cell_width - width) / 2
                )
                center_x = x + width / 2
            center_y_ratio = (
                node.get("center_y_ratio")
                if isinstance(node.get("center_y_ratio"), (int, float))
                else node.get("y_ratio")
            )
            if isinstance(center_y_ratio, (int, float)):
                center_y = float(center_y_ratio) * self.height
            else:
                y = float(
                    node.get("y_pt")
                    or row * cell_height + (cell_height - height) / 2
                )
                center_y = y + height / 2
            node_id = str(node.get("id") or f"node-{index + 1}")
            label = str(
                node.get("translation")
                or node.get("label")
                or node.get("text")
                or node_id
            )
            centers[node_id] = (center_x, center_y)
            labels[node_id] = label
            node_order.append(node_id)
            positions[node_id] = (0.0, 0.0, width, height)

        for left_index, left_id in enumerate(node_order):
            left_center = centers[left_id]
            left_box = positions[left_id]
            for right_id in node_order[left_index + 1 :]:
                right_center = centers[right_id]
                right_box = positions[right_id]
                same_lane = abs(left_center[1] - right_center[1]) <= max(
                    6.0,
                    min(left_box[3], right_box[3]) * 0.45,
                )
                center_gap = abs(left_center[0] - right_center[0])
                if (
                    same_lane
                    and center_gap > 0
                    and (left_box[2] + right_box[2]) / 2 > center_gap - 4
                ):
                    width_cap = max(18.0, center_gap - 6.0)
                    positions[left_id] = (
                        0.0,
                        0.0,
                        min(left_box[2], width_cap),
                        left_box[3],
                    )
                    positions[right_id] = (
                        0.0,
                        0.0,
                        min(right_box[2], width_cap),
                        right_box[3],
                    )
                    left_box = positions[left_id]

        for index, node_id in enumerate(node_order):
            _, _, width, height = positions[node_id]
            paragraph = self._node_paragraph(index, labels[node_id])
            _, required_height = paragraph.wrap(max(width - 8, 10), 10000)
            positions[node_id] = (
                0.0,
                0.0,
                width,
                min(
                    max(height, required_height + 6.0),
                    self.height - 8.0,
                ),
            )

        for upper_index, upper_id in enumerate(node_order):
            upper_center = centers[upper_id]
            upper_box = positions[upper_id]
            for lower_id in node_order[upper_index + 1 :]:
                lower_center = centers[lower_id]
                lower_box = positions[lower_id]
                same_lane = abs(upper_center[0] - lower_center[0]) <= max(
                    8.0,
                    min(upper_box[2], lower_box[2]) * 0.38,
                )
                center_gap = abs(upper_center[1] - lower_center[1])
                if (
                    same_lane
                    and center_gap > 0
                    and (upper_box[3] + lower_box[3]) / 2 > center_gap - 3
                ):
                    height_cap = max(10.0, center_gap - 4.0)
                    positions[upper_id] = (
                        0.0,
                        0.0,
                        upper_box[2],
                        min(upper_box[3], height_cap),
                    )
                    positions[lower_id] = (
                        0.0,
                        0.0,
                        lower_box[2],
                        min(lower_box[3], height_cap),
                    )
                    upper_box = positions[upper_id]

        for node_id in node_order:
            center_x, center_y = centers[node_id]
            _, _, width, height = positions[node_id]
            x = min(
                max(center_x - width / 2, 4.0),
                self.width - width - 4.0,
            )
            y = min(
                max(center_y - height / 2, 4.0),
                self.height - height - 4.0,
            )
            positions[node_id] = (x, y, width, height)

        for edge in edges:
            if (
                not isinstance(edge, dict)
                or str(edge.get("path_type") or "").lower()
                != "measurement-error"
            ):
                continue
            source_id = str(edge.get("source") or edge.get("from") or "")
            target_id = str(edge.get("target") or edge.get("to") or "")
            source = positions.get(source_id)
            target = positions.get(target_id)
            if not source or not target:
                continue
            source_center = (
                source[0] + source[2] / 2,
                source[1] + source[3] / 2,
            )
            target_center = (
                target[0] + target[2] / 2,
                target[1] + target[3] / 2,
            )
            label = str(edge.get("label") or "")
            label_width = pdfmetrics.stringWidth(
                label,
                self.regular_font,
                max(7.2, self.body_font_pt * 0.72),
            )
            desired_corridor = max(14.0, label_width + 6.0)
            delta_x = target_center[0] - source_center[0]
            delta_y = target_center[1] - source_center[1]
            if abs(delta_x) >= abs(delta_y):
                direction = 1.0 if delta_x >= 0 else -1.0
                corridor = abs(delta_x) - (source[2] + target[2]) / 2
                deficit = max(0.0, desired_corridor - corridor)
                if deficit <= 0:
                    continue
                source_room = (
                    source[0] - 4.0
                    if direction > 0
                    else self.width - source[0] - source[2] - 4.0
                )
                source_shift = min(deficit / 2, max(source_room, 0.0))
                remaining = deficit - source_shift
                target_room = (
                    self.width - target[0] - target[2] - 4.0
                    if direction > 0
                    else target[0] - 4.0
                )
                target_shift = min(remaining, max(target_room, 0.0))
                remaining -= target_shift
                if remaining > 0:
                    extra_source = min(
                        remaining,
                        max(source_room - source_shift, 0.0),
                    )
                    source_shift += extra_source
                positions[source_id] = (
                    source[0] - direction * source_shift,
                    source[1],
                    source[2],
                    source[3],
                )
                positions[target_id] = (
                    target[0] + direction * target_shift,
                    target[1],
                    target[2],
                    target[3],
                )
            else:
                direction = 1.0 if delta_y >= 0 else -1.0
                corridor = abs(delta_y) - (source[3] + target[3]) / 2
                deficit = max(0.0, desired_corridor - corridor)
                if deficit <= 0:
                    continue
                source_room = (
                    source[1] - 4.0
                    if direction > 0
                    else self.height - source[1] - source[3] - 4.0
                )
                source_shift = min(deficit / 2, max(source_room, 0.0))
                remaining = deficit - source_shift
                target_room = (
                    self.height - target[1] - target[3] - 4.0
                    if direction > 0
                    else target[1] - 4.0
                )
                target_shift = min(remaining, max(target_room, 0.0))
                remaining -= target_shift
                if remaining > 0:
                    extra_source = min(
                        remaining,
                        max(source_room - source_shift, 0.0),
                    )
                    source_shift += extra_source
                positions[source_id] = (
                    source[0],
                    source[1] - direction * source_shift,
                    source[2],
                    source[3],
                )
                positions[target_id] = (
                    target[0],
                    target[1] + direction * target_shift,
                    target[2],
                    target[3],
                )

        canvas.setStrokeColor(colors.HexColor("#45636F"))
        canvas.setLineWidth(0.8)
        legend_entries: list[str] = []
        covariance_index = 0
        duplicate_edges: defaultdict[tuple[str, str], int] = defaultdict(int)
        for _edge_index, edge in enumerate(edges):
            if not isinstance(edge, dict):
                continue
            source_id = str(edge.get("source") or edge.get("from") or "")
            target_id = str(edge.get("target") or edge.get("to") or "")
            source = positions.get(source_id)
            target = positions.get(target_id)
            if not source or not target:
                continue
            label = str(edge.get("label") or "")
            via = edge.get("via")
            if isinstance(via, list) and via:
                if label:
                    legend_entries.append(label)
                continue
            path_type = str(edge.get("path_type") or "").lower()
            direction = str(edge.get("direction") or "forward").lower()
            if path_type == "latent-covariance" or direction == "bidirectional":
                self._curved_covariance(
                    canvas,
                    source,
                    target,
                    label,
                    variant=covariance_index,
                )
                covariance_index += 1
                continue
            source_center = (
                source[0] + source[2] / 2,
                source[1] + source[3] / 2,
            )
            target_center = (
                target[0] + target[2] / 2,
                target[1] + target[3] / 2,
            )
            delta_x = target_center[0] - source_center[0]
            delta_y = target_center[1] - source_center[1]
            if abs(delta_x) >= abs(delta_y):
                if delta_x >= 0:
                    start = (
                        source[0] + source[2],
                        source_center[1],
                    )
                    end = (target[0], target_center[1])
                else:
                    start = (source[0], source_center[1])
                    end = (
                        target[0] + target[2],
                        target_center[1],
                    )
            elif delta_y >= 0:
                start = (
                    source_center[0],
                    source[1] + source[3],
                )
                end = (target_center[0], target[1])
            else:
                start = (source_center[0], source[1])
                end = (
                    target_center[0],
                    target[1] + target[3],
                )
            if len(label) > 24:
                legend_entries.append(label)
                drawn_label = ""
            else:
                drawn_label = label
            pair_key = (source_id, target_id)
            pair_slot = duplicate_edges[pair_key]
            duplicate_edges[pair_key] += 1
            label_t = (
                0.72
                if path_type == "measurement"
                else 0.52
                if path_type == "measurement-error"
                else 0.5
            )
            label_offset = 4.0 + pair_slot * 7.0
            if (
                abs(end[0] - start[0]) >= abs(end[1] - start[1])
                and path_type == ""
            ):
                label_offset = max(
                    label_offset,
                    max(source[3], target[3]) / 2 + 4.0,
                )
            explicit_label_position = None
            if (
                isinstance(edge.get("label_x_ratio"), (int, float))
                and isinstance(edge.get("label_y_ratio"), (int, float))
            ):
                explicit_label_position = (
                    float(edge["label_x_ratio"]) * self.width,
                    float(edge["label_y_ratio"]) * self.height,
                )
            self._arrow(
                canvas,
                start,
                end,
                drawn_label,
                direction=direction,
                line_style=str(
                    edge.get("line_style")
                    or edge.get("style")
                    or "solid"
                ).lower(),
                label_t=label_t,
                label_offset=label_offset,
                label_position=explicit_label_position,
            )
        for index, node in enumerate(nodes):
            node_id = str(node.get("id") or f"node-{index + 1}")
            x, y, width, height = positions[node_id]
            canvas.setFillColor(colors.HexColor("#F1F6F7"))
            canvas.roundRect(x, y, width, height, 4, stroke=1, fill=1)
            paragraph = self._node_paragraph(index, labels[node_id])
            _, paragraph_height = paragraph.wrap(width - 8, height - 6)
            paragraph.drawOn(
                canvas,
                x + 4,
                y + max((height - paragraph_height) / 2, 3),
            )
        if legend_entries:
            legend = Paragraph(
                "<br/>".join(
                    _markup(entry)
                    for entry in legend_entries
                ),
                ParagraphStyle(
                    "vector-edge-legend",
                    fontName=self.regular_font,
                    fontSize=max(7.2, self.body_font_pt * 0.72),
                    leading=max(10, self.body_font_pt),
                    alignment=TA_LEFT,
                    textColor=colors.HexColor("#26383F"),
                    wordWrap="CJK",
                ),
            )
            _, legend_height = legend.wrap(self.width - 16, self.height * 0.24)
            legend.drawOn(canvas, 8, 6)
        self._draw_node_annotations(canvas)

    def _draw_node_annotations(self, canvas) -> None:
        covariate_groups = [
            annotation
            for annotation in self.figure.get("annotations", [])
            if (
                isinstance(annotation, dict)
                and str(annotation.get("kind") or "").lower()
                == "covariate-group"
            )
        ]
        for index, annotation in enumerate(covariate_groups):
            label = str(
                annotation.get("label_translation")
                or annotation.get("translation")
                or annotation.get("label")
                or "Covariates"
            ).strip()
            items = [
                str(
                    item.get("translation")
                    or item.get("text")
                    or item.get("source")
                    or ""
                ).strip()
                for item in annotation.get("items", [])
                if isinstance(item, dict)
            ]
            lines = [value for value in [label, *items] if value]
            if not lines:
                continue
            width_ratio = float(annotation.get("width_ratio", 0.2))
            width = max(72.0, min(self.width * width_ratio, 118.0))
            center_x = float(annotation.get("x_ratio", 0.12)) * self.width
            center_y = float(
                annotation.get("y_ratio", 0.78 - index * 0.22)
            ) * self.height
            style = ParagraphStyle(
                f"vector-covariates-{index}",
                fontName=self.regular_font,
                fontSize=max(6.8, self.body_font_pt * 0.68),
                leading=max(9.4, self.body_font_pt * 0.94),
                alignment=TA_LEFT,
                textColor=colors.HexColor("#26383F"),
                wordWrap="CJK",
            )
            paragraph = Paragraph(
                "<br/>".join(_markup(value) for value in lines),
                style,
            )
            _, paragraph_height = paragraph.wrap(width - 12, self.height)
            x = max(6.0, min(center_x - width / 2, self.width - width - 6))
            y = max(
                6.0,
                min(
                    center_y - paragraph_height / 2,
                    self.height - paragraph_height - 6,
                ),
            )
            paragraph.drawOn(canvas, x, y)
            brace_x = x + width - 4
            brace_bottom = y - 2
            brace_top = y + paragraph_height + 2
            canvas.setStrokeColor(colors.HexColor("#66777E"))
            canvas.setLineWidth(0.7)
            canvas.line(brace_x, brace_bottom, brace_x, brace_top)
            canvas.line(brace_x - 5, brace_bottom, brace_x, brace_bottom)
            canvas.line(brace_x - 5, brace_top, brace_x, brace_top)

    def _draw_venn(self, canvas, figure: dict[str, Any]) -> None:
        circles = figure.get("circles")
        if not isinstance(circles, list) or len(circles) < 2:
            circles = [
                {"label": label}
                for label in figure.get("labels", [])[:3]
            ]
        radius = min(self.width, self.height) * 0.22
        centers = [
            (self.width * 0.42, self.height * 0.55),
            (self.width * 0.58, self.height * 0.55),
            (self.width * 0.50, self.height * 0.38),
        ]
        palette = [
            colors.Color(0.23, 0.55, 0.66, alpha=0.22),
            colors.Color(0.72, 0.42, 0.33, alpha=0.22),
            colors.Color(0.35, 0.63, 0.40, alpha=0.22),
        ]
        canvas.setStrokeColor(colors.HexColor("#536873"))
        for index, circle in enumerate(circles[:3]):
            x, y = centers[index]
            canvas.setFillColor(palette[index])
            canvas.circle(x, y, radius, stroke=1, fill=1)
            canvas.setFillColor(colors.HexColor("#20323A"))
            canvas.setFont(self.bold_font, max(7.2, self.body_font_pt * 0.75))
            label = str(
                circle.get("translation")
                or circle.get("label")
                or circle.get("text")
                or ""
            )
            canvas.drawCentredString(x, y + radius * 0.7, label)
        for annotation in figure.get("annotations", []):
            if not isinstance(annotation, dict):
                continue
            x = float(annotation.get("x_ratio", 0.5)) * self.width
            y = float(annotation.get("y_ratio", 0.5)) * self.height
            canvas.setFillColor(colors.HexColor("#17252B"))
            canvas.setFont(self.regular_font, max(7.0, self.body_font_pt * 0.72))
            canvas.drawCentredString(
                x,
                y,
                str(annotation.get("translation") or annotation.get("text") or ""),
            )

    def _draw_series(self, canvas, figure: dict[str, Any]) -> None:
        series = [
            item
            for item in figure.get("series", [])
            if isinstance(item, dict)
        ]
        x_axis = (
            figure.get("x_axis")
            if isinstance(figure.get("x_axis"), dict)
            else {}
        )
        y_axis = (
            figure.get("y_axis")
            if isinstance(figure.get("y_axis"), dict)
            else {}
        )
        axis_labels = [
            item
            for item in figure.get("axis_labels", [])
            if isinstance(item, dict)
        ]
        if not x_axis:
            x_axis = {
                "label": next(
                    (
                        str(
                            item.get("translation")
                            or item.get("label")
                            or ""
                        )
                        for item in axis_labels
                        if str(item.get("axis") or "")
                        .lower()
                        .startswith("horizontal")
                    ),
                    "",
                ),
                "categories": figure.get("x_categories", []),
            }
        if not y_axis:
            y_axis = {
                "label": next(
                    (
                        str(
                            item.get("translation")
                            or item.get("label")
                            or ""
                        )
                        for item in axis_labels
                        if str(item.get("axis") or "")
                        .lower()
                        .startswith("vertical")
                    ),
                    "",
                ),
                "minimum": figure.get("y_min"),
                "maximum": figure.get("y_max"),
                "ticks": figure.get("y_ticks", []),
            }
        categories = [
            str(value)
            for value in x_axis.get("categories", [])
            if str(value).strip()
        ]
        ticks = [
            float(value)
            for value in y_axis.get("ticks", [])
            if isinstance(value, (int, float))
        ]
        left = 72 if ticks or y_axis.get("label") else 42
        bottom = 58 if categories or x_axis.get("label") else 34
        top = 38 if any(
            str(
                item.get("translation")
                or item.get("label")
                or item.get("source_label")
                or ""
            ).strip()
            for item in series
        ) else 18
        width = self.width - left - 24
        height = self.height - bottom - top
        canvas.setStrokeColor(colors.HexColor("#6E7880"))
        canvas.setLineWidth(0.8)
        canvas.line(left, bottom, left, bottom + height)
        canvas.line(left, bottom, left + width, bottom)
        values = [
            float(value)
            for item in series
            for value in item.get("values", [])
            if isinstance(value, (int, float))
        ]
        numeric_minimum = min(values, default=0.0)
        numeric_maximum = max(values, default=1.0)
        axis_minimum = (
            float(y_axis["minimum"])
            if isinstance(y_axis.get("minimum"), (int, float))
            else min(0.0, numeric_minimum)
        )
        axis_maximum = (
            float(y_axis["maximum"])
            if isinstance(y_axis.get("maximum"), (int, float))
            else max(1.0, numeric_maximum)
        )
        if axis_maximum <= axis_minimum:
            axis_maximum = axis_minimum + 1.0
        palette = [
            colors.HexColor("#2D7584"),
            colors.HexColor("#B45D4C"),
            colors.HexColor("#5B8D61"),
            colors.HexColor("#8064A2"),
        ]
        text_color = colors.HexColor("#20323A")
        label_font = max(6.8, self.body_font_pt * 0.68)
        canvas.setFillColor(text_color)
        canvas.setFont(self.regular_font, label_font)
        for tick in ticks:
            ratio = (tick - axis_minimum) / (
                axis_maximum - axis_minimum
            )
            if not 0.0 <= ratio <= 1.0:
                continue
            y = bottom + ratio * height
            canvas.setStrokeColor(colors.HexColor("#AAB3B7"))
            canvas.setLineWidth(0.45)
            canvas.line(left - 4, y, left, y)
            canvas.drawRightString(left - 8, y - 2.2, str(tick))
        if categories:
            category_count = len(categories)
            for index, category in enumerate(categories):
                x = (
                    left + width / 2
                    if category_count == 1
                    else left + index * width / (category_count - 1)
                )
                canvas.drawCentredString(x, bottom - 16, category)
        x_label = str(x_axis.get("label") or "").strip()
        if x_label:
            canvas.setFont(self.bold_font, label_font)
            canvas.drawCentredString(
                left + width / 2,
                8,
                x_label,
            )
        y_label = str(y_axis.get("label") or "").strip()
        if y_label:
            canvas.saveState()
            canvas.translate(12, bottom + height / 2)
            canvas.rotate(90)
            canvas.setFont(self.bold_font, label_font)
            canvas.drawCentredString(0, 0, y_label)
            canvas.restoreState()

        for series_index, item in enumerate(series):
            item_values = [
                float(value)
                for value in item.get("values", [])
                if isinstance(value, (int, float))
            ]
            if not item_values:
                continue
            step = width / max(len(item_values) - 1, 1)
            normalized_positions = (
                str(item.get("value_semantics") or "").lower()
                == "normalized-visual-position-only"
            )
            points = [
                (
                    left + index * step,
                    bottom
                    + (
                        min(max(value, 0.0), 1.0)
                        if normalized_positions
                        else (
                            (value - axis_minimum)
                            / (axis_maximum - axis_minimum)
                        )
                    )
                    * height,
                )
                for index, value in enumerate(item_values)
            ]
            color_value = str(item.get("line_color") or "").strip()
            try:
                line_color = (
                    colors.HexColor(color_value)
                    if color_value
                    else palette[series_index % len(palette)]
                )
            except ValueError:
                line_color = palette[series_index % len(palette)]
            canvas.setStrokeColor(line_color)
            canvas.setLineWidth(1.4)
            line_style = str(item.get("line_style") or "solid").lower()
            if line_style == "dashed":
                canvas.setDash(5, 4)
            for first, second in zip(points, points[1:], strict=False):
                canvas.line(first[0], first[1], second[0], second[1])
            canvas.setDash()
            marker = str(item.get("marker") or "none").lower()
            if marker not in {"", "none", "no-marker"}:
                for x, y in points:
                    canvas.setFillColor(line_color)
                    if "triangle" in marker:
                        path = canvas.beginPath()
                        path.moveTo(x, y + 3.2)
                        path.lineTo(x - 3.2, y - 2.6)
                        path.lineTo(x + 3.2, y - 2.6)
                        path.close()
                        canvas.drawPath(path, stroke=1, fill=1)
                    elif "square" in marker:
                        canvas.rect(
                            x - 2.8,
                            y - 2.8,
                            5.6,
                            5.6,
                            stroke=1,
                            fill=0 if "open" in marker else 1,
                        )
                    else:
                        canvas.circle(x, y, 2.4, stroke=1, fill=1)

            label = str(
                item.get("translation")
                or item.get("label")
                or item.get("source_label")
                or ""
            ).strip()
            if label:
                legend_x = left + width * 0.58
                legend_y = (
                    self.height - 13 - series_index * 13
                )
                canvas.setStrokeColor(line_color)
                canvas.setLineWidth(1.4)
                if line_style == "dashed":
                    canvas.setDash(5, 4)
                canvas.line(
                    legend_x,
                    legend_y,
                    legend_x + 18,
                    legend_y,
                )
                canvas.setDash()
                if marker not in {"", "none", "no-marker"}:
                    canvas.setFillColor(line_color)
                    canvas.circle(
                        legend_x + 9,
                        legend_y,
                        2.1,
                        stroke=1,
                        fill=1,
                    )
                canvas.setFillColor(text_color)
                canvas.setFont(self.regular_font, label_font)
                canvas.drawString(
                    legend_x + 23,
                    legend_y - 2.2,
                    label,
                )

    @staticmethod
    def _has_numeric_series(figure: dict[str, Any]) -> bool:
        return any(
            isinstance(series, dict)
            and any(
                isinstance(value, (int, float))
                for value in series.get("values", [])
            )
            for series in figure.get("series", [])
        )

    @staticmethod
    def _panel_tokens(panel: dict[str, Any]) -> set[str]:
        values = {
            str(panel.get("id") or "").casefold(),
            str(panel.get("label") or "").casefold(),
        }
        panel_id = str(panel.get("id") or "")
        if "-" in panel_id:
            values.add(panel_id.rsplit("-", 1)[-1].casefold())
        return {value for value in values if value}

    @staticmethod
    def _numbered_panel_items(
        shape: dict[str, Any],
        expected_count: int,
    ) -> list[str]:
        raw_items = shape.get("items")
        if not isinstance(raw_items, list):
            raise VectorFigureError(
                "illustrative-time-series-bank 必须显式提供 items"
            )
        items = [
            str(
                item.get("translation")
                or item.get("target")
                or item.get("label")
                or item.get("text")
                or ""
            ).strip()
            if isinstance(item, dict)
            else str(item).strip()
            for item in raw_items
        ]
        if len(items) != expected_count or not all(items):
            raise VectorFigureError(
                "illustrative-time-series-bank.items "
                "必须与 series_count 一一对应"
            )
        return items

    def _draw_illustrative_time_series_bank(
        self,
        canvas,
        shape: dict[str, Any],
        semantics: str,
        *,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        series_count = max(1, int(shape.get("series_count") or 1))
        labels = self._numbered_panel_items(shape, series_count)
        label_width = width * 0.48
        plot_x0 = x + label_width + 12.0
        plot_x1 = x + width - 8.0
        rows_top = y + height - 15.0
        rows_bottom = y + 10.0
        row_height = (rows_top - rows_bottom) / series_count
        label_style = ParagraphStyle(
            f"series-bank-label-{id(shape)}",
            fontName=self.regular_font,
            fontSize=max(7.0, self.body_font_pt * 0.7),
            leading=max(8.4, self.body_font_pt * 0.84),
            textColor=colors.HexColor("#26383F"),
            wordWrap="CJK",
        )

        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#C4CDD1"))
        canvas.setLineWidth(0.45)
        canvas.line(
            plot_x0 - 7.0,
            rows_bottom,
            plot_x0 - 7.0,
            rows_top,
        )
        canvas.setFillColor(colors.HexColor("#5F6D74"))
        canvas.setFont(
            self.regular_font,
            max(6.8, self.body_font_pt * 0.68),
        )
        canvas.drawCentredString(
            (plot_x0 + plot_x1) / 2,
            rows_top + 2.0,
            self.message_fn(self.target_language, "over_time"),
        )

        for index, label in enumerate(labels):
            center_y = rows_top - (index + 0.5) * row_height
            paragraph = Paragraph(
                _markup(f"{index + 1}. {label}"),
                label_style,
            )
            _, paragraph_height = paragraph.wrap(
                label_width - 6.0,
                max(row_height, 1.0),
            )
            paragraph.drawOn(
                canvas,
                x,
                center_y - paragraph_height / 2,
            )

            canvas.saveState()
            canvas.setStrokeColor(colors.HexColor("#D6DDE0"))
            canvas.setDash(1.5, 2.0)
            canvas.line(plot_x0, center_y, plot_x1, center_y)
            canvas.restoreState()

            amplitude = min(row_height * 0.28, 4.2)
            phase = index * 0.73
            path = canvas.beginPath()
            for point_index in range(25):
                ratio = point_index / 24
                point_x = plot_x0 + (plot_x1 - plot_x0) * ratio
                wave = (
                    math.sin(
                        ratio
                        * math.tau
                        * (1.0 + (index % 3) * 0.22)
                        + phase
                    )
                    * 0.72
                    + math.sin(ratio * math.tau * 2.0 + phase * 0.5)
                    * 0.18
                )
                point_y = center_y + amplitude * wave
                if point_index == 0:
                    path.moveTo(point_x, point_y)
                else:
                    path.lineTo(point_x, point_y)
            canvas.setStrokeColor(colors.HexColor("#496B78"))
            canvas.setLineWidth(0.8)
            canvas.drawPath(path, stroke=1, fill=0)

        canvas.setStrokeColor(colors.HexColor("#708087"))
        canvas.setLineWidth(0.55)
        canvas.line(plot_x0, rows_bottom - 3.0, plot_x1, rows_bottom - 3.0)
        self._arrow_head(
            canvas,
            (plot_x1, rows_bottom - 3.0),
            (plot_x0, rows_bottom - 3.0),
        )
        canvas.restoreState()

    @staticmethod
    def _normalized_panel_nodes(
        nodes: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        result = [dict(node) for node in nodes]
        for axis in ("x", "y"):
            source_keys = (f"center_{axis}_ratio", f"{axis}_ratio")
            positioned = []
            for node in result:
                value = next(
                    (
                        node.get(key)
                        for key in source_keys
                        if isinstance(node.get(key), (int, float))
                    ),
                    None,
                )
                if isinstance(value, (int, float)):
                    positioned.append((node, float(value)))
            if len(positioned) < 2:
                continue
            minimum = min(value for _, value in positioned)
            maximum = max(value for _, value in positioned)
            if maximum - minimum < 0.02:
                continue
            for node, value in positioned:
                node[f"center_{axis}_ratio"] = (
                    0.14 + (value - minimum) / (maximum - minimum) * 0.72
                )
        return result

    def _draw_process_panels(
        self,
        canvas,
        figure: dict[str, Any],
    ) -> None:
        panels = [
            panel
            for panel in figure.get("panels", [])
            if isinstance(panel, dict)
        ]
        nodes = [
            node
            for node in figure.get("nodes", [])
            if isinstance(node, dict)
        ]
        edges = [
            edge
            for edge in (
                figure.get("edges")
                or figure.get("connectors")
                or []
            )
            if isinstance(edge, dict)
        ]
        if not panels:
            self._draw_nodes(canvas, nodes, edges)
            return

        columns = max(1, min(int(figure.get("columns") or 2), len(panels)))
        rows = math.ceil(len(panels) / columns)
        outer = 8.0
        gap_x = 10.0
        gap_y = 10.0
        panel_width = (
            self.width - 2 * outer - gap_x * (columns - 1)
        ) / columns
        panel_height = (
            self.height - 2 * outer - gap_y * (rows - 1)
        ) / rows

        for panel_index, panel in enumerate(panels):
            column = panel_index % columns
            row_from_top = panel_index // columns
            x = outer + column * (panel_width + gap_x)
            y = (
                outer
                + (rows - row_from_top - 1) * (panel_height + gap_y)
            )
            tokens = self._panel_tokens(panel)
            panel_nodes = [
                node
                for node in nodes
                if str(node.get("panel") or "").casefold() in tokens
            ]
            legend_nodes = [
                node
                for node in panel_nodes
                if str(node.get("type") or "").lower() == "legend"
            ]
            graph_nodes = [
                node for node in panel_nodes if node not in legend_nodes
            ]
            node_ids = {
                str(node.get("id") or "") for node in graph_nodes
            }
            panel_edges = [
                edge
                for edge in edges
                if str(edge.get("source") or edge.get("from") or "")
                in node_ids
                and str(edge.get("target") or edge.get("to") or "")
                in node_ids
            ]
            panel_shapes = [
                shape
                for shape in self.figure.get("shapes", [])
                if (
                    isinstance(shape, dict)
                    and str(shape.get("type") or "").lower()
                    == "illustrative-time-series-bank"
                    and any(
                        token
                        and token
                        in str(shape.get("id") or "").casefold()
                        for token in tokens
                    )
                )
            ]

            label = str(panel.get("label") or "").strip()
            title = str(panel.get("title") or "").strip()
            heading = " ".join(value for value in (label, title) if value)
            canvas.setFillColor(colors.HexColor("#20323A"))
            canvas.setFont(
                self.bold_font,
                max(7.2, self.body_font_pt * 0.76),
            )
            canvas.drawCentredString(
                x + panel_width / 2,
                y + panel_height - 11,
                heading,
            )

            legend_height = 0.0
            if legend_nodes:
                legend_height = 18.0
                legend_text = "；".join(
                    str(
                        node.get("translation")
                        or node.get("label")
                        or node.get("text")
                        or ""
                    )
                    for node in legend_nodes
                )
                legend = Paragraph(
                    _markup(legend_text),
                    ParagraphStyle(
                        f"process-panel-legend-{panel_index}",
                        fontName=self.regular_font,
                        fontSize=max(6.2, self.body_font_pt * 0.62),
                        leading=max(8.2, self.body_font_pt * 0.82),
                        alignment=TA_CENTER,
                        textColor=colors.HexColor("#34444B"),
                        wordWrap="CJK",
                    ),
                )
                _, measured = legend.wrap(panel_width - 12, 42)
                legend_height = min(max(measured + 4, 18.0), 42.0)
                legend.drawOn(canvas, x + 6, y + 4)

            inner_height = max(panel_height - 24 - legend_height, 54.0)
            inner_width = max(panel_width - 8, 60.0)
            if graph_nodes:
                child = VectorPayloadFlowable(
                    {
                        "type": "directed-model",
                        "height_pt": inner_height,
                        "nodes": self._normalized_panel_nodes(graph_nodes),
                        "edges": panel_edges,
                    },
                    width=inner_width,
                    regular_font=self.regular_font,
                    bold_font=self.bold_font,
                    body_font_pt=max(8.0, self.body_font_pt * 0.86),
                    message_fn=self.message_fn,
                )
                child.wrap(inner_width, inner_height)
                child.drawOn(
                    canvas,
                    x + 4,
                    y + 4 + legend_height,
                )
            elif panel_shapes:
                self._draw_illustrative_time_series_bank(
                    canvas,
                    panel_shapes[0],
                    str(panel.get("semantics") or ""),
                    x=x + 8.0,
                    y=y + 5.0,
                    width=panel_width - 16.0,
                    height=inner_height - 2.0,
                )
            else:
                semantics = str(panel.get("semantics") or "").strip()
                if semantics:
                    paragraph = Paragraph(
                        _markup(semantics),
                        self._label_style(panel_index + 6, semantics),
                    )
                    _, paragraph_height = paragraph.wrap(
                        panel_width - 16,
                        inner_height,
                    )
                    paragraph.drawOn(
                        canvas,
                        x + 8,
                        y + legend_height
                        + max((inner_height - paragraph_height) / 2, 4),
                    )

    @staticmethod
    def _is_quadrant_panel_figure(
        figure: dict[str, Any],
    ) -> bool:
        axis_labels = figure.get("axis_labels")
        if not isinstance(axis_labels, dict):
            return False
        if not all(
            isinstance(axis_labels.get(axis), dict)
            for axis in ("vertical", "horizontal")
        ):
            return False
        positions = {
            str(panel.get("position") or "").lower()
            for panel in figure.get("panels", [])
            if isinstance(panel, dict)
        }
        return {
            "upper-left",
            "upper-right",
            "lower-left",
            "lower-right",
        }.issubset(positions)

    def _draw_quadrant_panels(
        self,
        canvas,
        figure: dict[str, Any],
    ) -> None:
        axis_labels = figure["axis_labels"]
        vertical = axis_labels["vertical"]
        horizontal = axis_labels["horizontal"]
        x0 = 50.0
        x1 = self.width - 18.0
        y0 = 30.0
        y1 = self.height - 15.0
        middle_x = (x0 + x1) / 2
        middle_y = (y0 + y1) / 2
        bounds = {
            "upper-left": (x0, middle_y, middle_x, y1),
            "upper-right": (middle_x, middle_y, x1, y1),
            "lower-left": (x0, y0, middle_x, middle_y),
            "lower-right": (middle_x, y0, x1, middle_y),
        }

        for position, (left, bottom, right, top) in bounds.items():
            canvas.saveState()
            canvas.setFillColor(
                colors.HexColor(
                    "#EEF2F3"
                    if position.startswith("upper")
                    else "#F8FAFA"
                )
            )
            canvas.setStrokeColor(colors.HexColor("#D0D9DD"))
            canvas.rect(
                left,
                bottom,
                right - left,
                top - bottom,
                stroke=1,
                fill=1,
            )
            canvas.restoreState()

        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#53656D"))
        canvas.setLineWidth(1.1)
        canvas.line(x0, middle_y, x1, middle_y)
        canvas.line(middle_x, y0, middle_x, y1)
        canvas.line(x1, middle_y, x1 - 6, middle_y + 3)
        canvas.line(x1, middle_y, x1 - 6, middle_y - 3)
        canvas.line(middle_x, y1, middle_x - 3, y1 - 6)
        canvas.line(middle_x, y1, middle_x + 3, y1 - 6)
        canvas.restoreState()

        heading_style = ParagraphStyle(
            "quadrant-panel-heading",
            fontName=self.bold_font,
            fontSize=max(7.4, self.body_font_pt * 0.8),
            leading=max(10.0, self.body_font_pt * 1.05),
            alignment=TA_CENTER,
            textColor=colors.HexColor("#20323A"),
            wordWrap="CJK",
        )
        body_style = ParagraphStyle(
            "quadrant-panel-body",
            fontName=self.regular_font,
            fontSize=max(7.2, self.body_font_pt * 0.76),
            leading=max(10.0, self.body_font_pt * 1.08),
            alignment=TA_CENTER,
            textColor=colors.HexColor("#34444B"),
            wordWrap="CJK",
        )
        panels_by_position = {
            str(panel.get("position") or "").lower(): panel
            for panel in figure.get("panels", [])
            if isinstance(panel, dict)
        }
        for position, (left, bottom, right, top) in bounds.items():
            panel = panels_by_position[position]
            width = right - left - 14
            title = str(
                panel.get("title")
                or panel.get("label")
                or ""
            ).strip()
            semantics = str(
                panel.get("semantics")
                or panel.get("description")
                or ""
            ).strip()
            title_height = 0.0
            if title:
                title_paragraph = Paragraph(
                    _markup(title),
                    heading_style,
                )
                _, title_height = title_paragraph.wrap(
                    width,
                    max(top - bottom, 1),
                )
                title_paragraph.drawOn(
                    canvas,
                    left + 7,
                    top - title_height - 8,
                )
            if semantics:
                body_paragraph = Paragraph(
                    _markup(semantics),
                    body_style,
                )
                _, body_height = body_paragraph.wrap(
                    width,
                    max(top - bottom - title_height - 18, 1),
                )
                body_y = bottom + max(
                    8,
                    (top - bottom - body_height) / 2 - 5,
                )
                body_paragraph.drawOn(
                    canvas,
                    left + 7,
                    min(
                        body_y,
                        top - title_height - body_height - 12,
                    ),
                )

        label_font = max(6.8, self.body_font_pt * 0.72)
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#34444B"))
        canvas.setFont(self.regular_font, label_font)
        vertical_positive = str(
            vertical.get("positive") or ""
        ).strip()
        vertical_negative = str(
            vertical.get("negative") or ""
        ).strip()
        vertical_dimension = str(
            vertical.get("dimension") or ""
        ).strip()
        horizontal_negative = str(
            horizontal.get("negative") or ""
        ).strip()
        horizontal_positive = str(
            horizontal.get("positive") or ""
        ).strip()
        horizontal_dimension = str(
            horizontal.get("dimension") or ""
        ).strip()
        if vertical_positive:
            canvas.drawString(4, y1 - label_font, vertical_positive)
        if vertical_negative:
            canvas.drawString(4, y0 + 2, vertical_negative)
        if vertical_dimension:
            canvas.saveState()
            canvas.translate(16, middle_y)
            canvas.rotate(90)
            canvas.drawCentredString(0, 0, vertical_dimension)
            canvas.restoreState()
        if horizontal_negative:
            canvas.drawString(x0, 9, horizontal_negative)
        if horizontal_positive:
            canvas.drawRightString(x1, 9, horizontal_positive)
        if horizontal_dimension:
            canvas.drawCentredString(middle_x, 9, horizontal_dimension)
        canvas.restoreState()

    def _draw_trajectory(
        self,
        canvas,
        figure: dict[str, Any],
    ) -> None:
        nodes = [
            node
            for node in figure.get("nodes", [])
            if isinstance(node, dict)
            and isinstance(
                node.get("x_ratio", node.get("center_x_ratio")),
                (int, float),
            )
            and isinstance(
                node.get("y_ratio", node.get("center_y_ratio")),
                (int, float),
            )
        ]
        nodes.sort(
            key=lambda node: (
                int(node.get("order") or 10**6),
                float(node.get("x_ratio", node.get("center_x_ratio", 0))),
            )
        )
        if not nodes:
            self._draw_nodes(
                canvas,
                [
                    node
                    for node in figure.get("nodes", [])
                    if isinstance(node, dict)
                ],
                list(figure.get("edges") or []),
            )
            return

        legend_height = min(max(self.height * 0.38, 145.0), 190.0)
        left = 42.0
        right = 18.0
        bottom = legend_height + 22.0
        top = 22.0
        plot_width = max(self.width - left - right, 80.0)
        plot_height = max(self.height - bottom - top, 90.0)
        points = [
            (
                left
                + min(max(float(
                    node.get("x_ratio", node.get("center_x_ratio", 0))
                ), 0.0), 1.0)
                * plot_width,
                bottom
                + min(max(float(
                    node.get("y_ratio", node.get("center_y_ratio", 0))
                ), 0.0), 1.0)
                * plot_height,
            )
            for node in nodes
        ]

        canvas.setStrokeColor(colors.HexColor("#405A64"))
        canvas.setLineWidth(1.0)
        canvas.line(left, bottom, left, bottom + plot_height)
        self._arrow_head(
            canvas,
            (left, bottom + plot_height),
            (left, bottom + plot_height - 12),
        )
        canvas.line(left, bottom, left + plot_width, bottom)
        self._arrow_head(
            canvas,
            (left + plot_width, bottom),
            (left + plot_width - 12, bottom),
        )

        canvas.setStrokeColor(colors.HexColor("#1F5668"))
        canvas.setLineWidth(1.8)
        path = canvas.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for x, y in points[1:]:
            path.lineTo(x, y)
        canvas.drawPath(path, stroke=1, fill=0)
        canvas.setFillColor(colors.HexColor("#1F5668"))
        canvas.setFont(
            self.bold_font,
            max(5.8, self.body_font_pt * 0.58),
        )
        for index, (x, y) in enumerate(points, 1):
            canvas.circle(x, y, 4.2, stroke=1, fill=1)
            canvas.setFillColor(colors.white)
            canvas.drawCentredString(x, y - 2.0, str(index))
            canvas.setFillColor(colors.HexColor("#1F5668"))

        axis_labels = [
            item
            for item in figure.get("axis_labels", [])
            if isinstance(item, dict)
        ]
        horizontal_label = next(
            (
                str(item.get("translation") or item.get("label") or "")
                for item in axis_labels
                if str(item.get("axis") or "").lower().startswith("horizontal")
            ),
            "",
        )
        vertical_label = next(
            (
                str(item.get("translation") or item.get("label") or "")
                for item in axis_labels
                if str(item.get("axis") or "").lower().startswith("vertical")
            ),
            "",
        )
        canvas.setFillColor(colors.HexColor("#20323A"))
        canvas.setFont(
            self.bold_font,
            max(7.0, self.body_font_pt * 0.72),
        )
        if horizontal_label:
            canvas.drawCentredString(
                left + plot_width / 2,
                bottom - 14,
                horizontal_label,
            )
        if vertical_label:
            canvas.saveState()
            canvas.translate(12, bottom + plot_height / 2)
            canvas.rotate(90)
            canvas.drawCentredString(0, 0, vertical_label)
            canvas.restoreState()

        entries = [
            f"{index}. "
            + str(
                node.get("translation")
                or node.get("label")
                or node.get("text")
                or node.get("id")
                or ""
            )
            for index, node in enumerate(nodes, 1)
        ]
        columns = 2
        rows = math.ceil(len(entries) / columns)
        column_width = (self.width - 18.0) / columns
        font_size = max(6.8, self.body_font_pt * 0.68)
        leading = max(8.8, self.body_font_pt * 0.88)
        style = ParagraphStyle(
            "trajectory-legend",
            fontName=self.regular_font,
            fontSize=font_size,
            leading=leading,
            textColor=colors.HexColor("#26383F"),
            wordWrap="CJK",
        )
        for column in range(columns):
            y = legend_height - 2.0
            for row in range(rows):
                index = column * rows + row
                if index >= len(entries):
                    break
                paragraph = Paragraph(_markup(entries[index]), style)
                _, paragraph_height = paragraph.wrap(
                    column_width - 12,
                    legend_height,
                )
                y -= paragraph_height
                if y < 3:
                    break
                paragraph.drawOn(
                    canvas,
                    8 + column * column_width,
                    y,
                )
                y -= 1.5

    def _draw_expanding_spiral(
        self,
        canvas,
        figure: dict[str, Any],
    ) -> None:
        bottom = 48.0
        top = self.height - 34.0
        center_x = self.width / 2
        available_height = max(top - bottom, 80.0)
        samples = 140
        spiral_points = []
        for index in range(samples):
            t = index / (samples - 1)
            amplitude = 10.0 + t * self.width * 0.24
            angle = t * math.pi * 10.0
            spiral_points.append(
                (
                    center_x + math.sin(angle) * amplitude,
                    bottom + t * available_height,
                )
            )
        canvas.setStrokeColor(colors.HexColor("#A9B3B7"))
        canvas.setLineWidth(9.0)
        path = canvas.beginPath()
        path.moveTo(*spiral_points[0])
        for point in spiral_points[1:]:
            path.lineTo(*point)
        canvas.drawPath(path, stroke=1, fill=0)
        canvas.setStrokeColor(colors.HexColor("#385B68"))
        canvas.setLineWidth(1.1)
        canvas.drawPath(path, stroke=1, fill=0)

        canvas.line(center_x, bottom - 5, center_x, top + 8)
        self._arrow_head(
            canvas,
            (center_x, top + 8),
            (center_x, top - 5),
        )
        axis_payloads = [
            item
            for item in figure.get("axis_labels", [])
            if isinstance(item, dict)
        ]
        vertical_label = next(
            (
                str(item.get("translation") or item.get("label") or "")
                for item in axis_payloads
                if str(item.get("axis") or "").lower().startswith("vertical")
            ),
            "",
        )
        canvas.setFillColor(colors.HexColor("#20323A"))
        canvas.setFont(
            self.bold_font,
            max(7.0, self.body_font_pt * 0.72),
        )
        if vertical_label:
            canvas.saveState()
            canvas.translate(center_x + 8, bottom + available_height / 2)
            canvas.rotate(90)
            canvas.drawCentredString(0, 0, vertical_label)
            canvas.restoreState()

        axis_y = 25.0
        canvas.line(50.0, axis_y, self.width - 50.0, axis_y)
        self._arrow_head(canvas, (50.0, axis_y), (63.0, axis_y))
        self._arrow_head(
            canvas,
            (self.width - 50.0, axis_y),
            (self.width - 63.0, axis_y),
        )
        axis_labels = [
            str(item.get("translation") or item.get("label") or "")
            for item in axis_payloads
            if str(item.get("axis") or "").lower().startswith("horizontal")
        ]
        if axis_labels:
            labels = (axis_labels + [""] * 3)[:3]
            canvas.setFont(
                self.regular_font,
                max(6.2, self.body_font_pt * 0.62),
            )
            canvas.drawString(18, 8, labels[0])
            canvas.drawCentredString(center_x, 8, labels[1])
            canvas.drawRightString(self.width - 18, 8, labels[2])

        nodes = [
            node
            for node in figure.get("nodes", [])
            if isinstance(node, dict)
            and isinstance(node.get("center_y_ratio"), (int, float))
        ]
        label_style = ParagraphStyle(
            "spiral-stage-label",
            fontName=self.regular_font,
            fontSize=max(7.0, self.body_font_pt * 0.70),
            leading=max(9.2, self.body_font_pt * 0.92),
            alignment=TA_CENTER,
            textColor=colors.HexColor("#26383F"),
            wordWrap="CJK",
        )
        for _index, node in enumerate(nodes):
            ratio = min(max(float(node["center_y_ratio"]), 0.0), 1.0)
            y = bottom + ratio * available_height
            sample_index = min(
                samples - 1,
                max(0, round(ratio * (samples - 1))),
            )
            spiral_x = spiral_points[sample_index][0]
            left_side = float(node.get("center_x_ratio") or 0.5) < 0.5
            label_width = min(132.0, self.width * 0.28)
            label_x = 8.0 if left_side else self.width - label_width - 8.0
            text = str(
                node.get("translation")
                or node.get("label")
                or node.get("text")
                or ""
            )
            paragraph = Paragraph(_markup(text), label_style)
            _, paragraph_height = paragraph.wrap(label_width, 48)
            label_y = min(
                max(y - paragraph_height / 2, 35.0),
                self.height - paragraph_height - 8.0,
            )
            paragraph.drawOn(canvas, label_x, label_y)
            target_x = (
                label_x + label_width
                if left_side
                else label_x
            )
            canvas.setStrokeColor(colors.HexColor("#6D7C82"))
            canvas.setLineWidth(0.55)
            canvas.line(
                spiral_x,
                y,
                target_x,
                label_y + paragraph_height / 2,
            )

    def _draw_bar_panels(self, canvas, figure: dict[str, Any]) -> None:
        panels = [
            panel
            for panel in figure.get("panels", [])
            if isinstance(panel, dict)
        ]
        if not panels:
            return

        note = str(figure.get("note") or "").strip()
        note_height = 0.0
        note_paragraph: Paragraph | None = None
        if note:
            note_paragraph = Paragraph(
                _markup(note),
                ParagraphStyle(
                    "bar-panels-note",
                    fontName=self.regular_font,
                    fontSize=max(6.6, self.body_font_pt * 0.66),
                    leading=max(9.2, self.body_font_pt * 0.92),
                    textColor=colors.HexColor("#34444B"),
                    wordWrap="CJK",
                ),
            )
            _, note_height = note_paragraph.wrap(self.width - 20, 56)

        columns = max(
            1,
            min(int(figure.get("columns") or 2), len(panels)),
        )
        rows = math.ceil(len(panels) / columns)
        outer = 10.0
        gap_x = 14.0
        gap_y = 12.0
        content_bottom = outer + note_height + (8 if note else 0)
        content_height = (
            self.height
            - content_bottom
            - outer
            - gap_y * (rows - 1)
        )
        panel_width = (
            self.width - 2 * outer - gap_x * (columns - 1)
        ) / columns
        panel_height = content_height / rows
        palette = (
            colors.HexColor("#4C7A86"),
            colors.HexColor("#778187"),
            colors.HexColor("#B46A55"),
            colors.HexColor("#698C69"),
        )

        for panel_index, panel in enumerate(panels):
            column = panel_index % columns
            row_from_top = panel_index // columns
            x = outer + column * (panel_width + gap_x)
            y = (
                content_bottom
                + (rows - row_from_top - 1) * (panel_height + gap_y)
            )
            title = str(panel.get("title") or "").strip()
            canvas.setFillColor(colors.HexColor("#1D2C32"))
            canvas.setFont(
                self.bold_font,
                max(7.2, self.body_font_pt * 0.76),
            )
            canvas.drawCentredString(
                x + panel_width / 2,
                y + panel_height - 11,
                title,
            )

            plot_left = x + 30
            plot_bottom = y + 24
            plot_width = max(panel_width - 38, 40)
            plot_height = max(panel_height - 47, 44)
            canvas.setStrokeColor(colors.HexColor("#56656C"))
            canvas.setLineWidth(0.6)
            canvas.line(
                plot_left,
                plot_bottom,
                plot_left,
                plot_bottom + plot_height,
            )
            canvas.line(
                plot_left,
                plot_bottom,
                plot_left + plot_width,
                plot_bottom,
            )

            groups = [
                group
                for group in panel.get("groups", [])
                if isinstance(group, dict)
                and isinstance(group.get("value"), (int, float))
            ]
            if not groups:
                continue
            values = [float(group["value"]) for group in groups]
            y_min = float(panel.get("y_min", min(0.0, min(values))))
            y_max = float(panel.get("y_max", max(values) * 1.12 or 1.0))
            if y_max <= y_min:
                y_max = y_min + 1.0

            ticks = [
                float(value)
                for value in panel.get("y_ticks", [])
                if isinstance(value, (int, float))
                and y_min <= float(value) <= y_max
            ]
            if not ticks:
                ticks = [
                    y_min + (y_max - y_min) * index / 4
                    for index in range(5)
                ]

            def y_position(
                value: float,
                *,
                y_min: float = y_min,
                y_max: float = y_max,
                plot_bottom: float = plot_bottom,
                plot_height: float = plot_height,
            ) -> float:
                clipped = min(max(value, y_min), y_max)
                return (
                    plot_bottom
                    + (clipped - y_min) / (y_max - y_min) * plot_height
                )

            canvas.setFont(
                self.regular_font,
                max(5.7, self.body_font_pt * 0.56),
            )
            for tick in ticks:
                tick_y = y_position(tick)
                canvas.setStrokeColor(colors.HexColor("#D6DDE0"))
                canvas.setLineWidth(0.35)
                canvas.line(
                    plot_left,
                    tick_y,
                    plot_left + plot_width,
                    tick_y,
                )
                canvas.setFillColor(colors.HexColor("#425158"))
                tick_label = f"{tick:.2f}".rstrip("0").rstrip(".")
                canvas.drawRightString(plot_left - 4, tick_y - 2, tick_label)

            slot_width = plot_width / len(groups)
            bar_width = min(30.0, slot_width * 0.48)
            centers: list[float] = []
            for group_index, group in enumerate(groups):
                center = plot_left + slot_width * (group_index + 0.5)
                centers.append(center)
                top = y_position(float(group["value"]))
                canvas.setFillColor(palette[group_index % len(palette)])
                canvas.rect(
                    center - bar_width / 2,
                    plot_bottom,
                    bar_width,
                    max(top - plot_bottom, 0.8),
                    stroke=0,
                    fill=1,
                )

                low_error = float(
                    group.get("error_low", group.get("error", 0.0)) or 0.0
                )
                high_error = float(
                    group.get("error_high", group.get("error", 0.0)) or 0.0
                )
                if low_error > 0 or high_error > 0:
                    low = y_position(float(group["value"]) - low_error)
                    high = y_position(float(group["value"]) + high_error)
                    canvas.setStrokeColor(colors.HexColor("#27363C"))
                    canvas.setLineWidth(0.7)
                    canvas.line(center, low, center, high)
                    canvas.line(center - 4, low, center + 4, low)
                    canvas.line(center - 4, high, center + 4, high)

                canvas.setFillColor(colors.HexColor("#26363D"))
                canvas.setFont(
                    self.regular_font,
                    max(5.8, self.body_font_pt * 0.58),
                )
                canvas.drawCentredString(
                    center,
                    plot_bottom - 12,
                    str(
                        group.get("translation")
                        or group.get("label")
                        or group_index + 1
                    ),
                )

            for comparison_index, comparison in enumerate(
                panel.get("comparisons", [])
            ):
                if not isinstance(comparison, dict):
                    continue
                start = int(comparison.get("start", 0))
                end = int(comparison.get("end", 0))
                if not (
                    0 <= start < len(centers)
                    and 0 <= end < len(centers)
                    and start != end
                ):
                    continue
                level = int(comparison.get("level", comparison_index))
                bracket_y = (
                    plot_bottom + plot_height - 8 - max(level, 0) * 13
                )
                x1, x2 = sorted((centers[start], centers[end]))
                canvas.setStrokeColor(colors.HexColor("#26343A"))
                canvas.setLineWidth(0.65)
                canvas.line(x1, bracket_y - 4, x1, bracket_y)
                canvas.line(x1, bracket_y, x2, bracket_y)
                canvas.line(x2, bracket_y, x2, bracket_y - 4)
                canvas.setFillColor(colors.HexColor("#1D2C32"))
                canvas.setFont(
                    self.bold_font,
                    max(6.2, self.body_font_pt * 0.62),
                )
                canvas.drawCentredString(
                    (x1 + x2) / 2,
                    bracket_y + 2,
                    str(comparison.get("label") or ""),
                )

        if note_paragraph is not None:
            note_paragraph.drawOn(canvas, 10, 7)

    def _draw_pyramid(self, canvas, figure: dict[str, Any]) -> None:
        levels = [
            level
            for level in figure.get("levels", [])
            if isinstance(level, dict)
        ]
        if not levels:
            return
        margin = 18.0
        triangle_width = self.width * 0.54
        panel_x = triangle_width + 24
        panel_width = self.width - panel_x - margin
        usable_height = self.height - 2 * margin
        level_height = usable_height / len(levels)
        center_x = triangle_width / 2 + margin / 2
        half_base = triangle_width / 2 - margin
        shades = (
            colors.HexColor("#E7EAEC"),
            colors.HexColor("#CCD2D5"),
            colors.HexColor("#AEB7BC"),
            colors.HexColor("#87939A"),
            colors.HexColor("#65737B"),
        )
        canvas.setStrokeColor(colors.HexColor("#66737A"))
        canvas.setLineWidth(0.6)
        for index, level in enumerate(levels):
            y0 = margin + index * level_height
            y1 = y0 + level_height
            lower_ratio = 1 - (y0 - margin) / usable_height
            upper_ratio = 1 - (y1 - margin) / usable_height
            lower_left = center_x - half_base * lower_ratio
            lower_right = center_x + half_base * lower_ratio
            upper_left = center_x - half_base * upper_ratio
            upper_right = center_x + half_base * upper_ratio
            path = canvas.beginPath()
            path.moveTo(lower_left, y0)
            path.lineTo(lower_right, y0)
            path.lineTo(upper_right, y1)
            path.lineTo(upper_left, y1)
            path.close()
            canvas.setFillColor(shades[min(index, len(shades) - 1)])
            canvas.drawPath(path, stroke=1, fill=1)
            title = str(
                level.get("translation")
                or level.get("title")
                or level.get("label")
                or ""
            )
            title_paragraph = Paragraph(
                _markup(title),
                ParagraphStyle(
                    f"pyramid-title-{index}",
                    fontName=self.bold_font,
                    fontSize=max(7.2, self.body_font_pt * 0.78),
                    leading=max(10.5, self.body_font_pt * 1.05),
                    alignment=TA_CENTER,
                    textColor=(
                        colors.white
                        if index >= len(levels) - 1
                        else colors.HexColor("#1E2B31")
                    ),
                    wordWrap="CJK",
                ),
            )
            title_width = max(upper_right - upper_left - 10, 70)
            _, title_height = title_paragraph.wrap(
                title_width,
                level_height - 8,
            )
            title_paragraph.drawOn(
                canvas,
                center_x - title_width / 2,
                y0 + max((level_height - title_height) / 2, 4),
            )

            items = [
                str(value)
                for value in level.get("items", [])
                if str(value).strip()
            ]
            panel_text = "<br/>".join(
                f"• {html.escape(value)}" for value in items
            )
            if panel_text:
                panel_style = ParagraphStyle(
                    f"pyramid-items-{index}",
                    fontName=self.regular_font,
                    fontSize=max(7.0, self.body_font_pt * 0.72),
                    leading=max(10.0, self.body_font_pt * 1.0),
                    textColor=colors.HexColor("#243239"),
                    wordWrap="CJK",
                )
                panel = Paragraph(panel_text, panel_style)
                _, panel_height = panel.wrap(
                    panel_width - 10,
                    level_height - 6,
                )
                canvas.setFillColor(
                    colors.HexColor("#F4F6F7")
                    if index % 2 == 0
                    else colors.HexColor("#E9EDEF")
                )
                canvas.rect(
                    panel_x,
                    y0,
                    panel_width,
                    level_height,
                    stroke=1,
                    fill=1,
                )
                panel.drawOn(
                    canvas,
                    panel_x + 5,
                    y0 + max((level_height - panel_height) / 2, 3),
                )

    def _draw_label_layout(self, canvas, figure: dict[str, Any]) -> None:
        labels = [
            str(value)
            for value in figure.get("labels", [])
            if str(value).strip()
        ]
        if not labels:
            return
        y = self.height - 8
        for index, label in enumerate(labels):
            style = self._label_style(index, label)
            paragraph = Paragraph(_markup(label), style)
            _, paragraph_height = paragraph.wrap(self.width - 16, max(y, 1))
            if y - paragraph_height < 4:
                break
            y -= paragraph_height
            if index in {0, 3}:
                canvas.setFillColor(colors.HexColor("#EDF3F4"))
                canvas.roundRect(
                    4,
                    y - 3,
                    self.width - 8,
                    paragraph_height + 6,
                    3,
                    stroke=0,
                    fill=1,
                )
            paragraph.drawOn(canvas, 8, y)
            y -= 4

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#8A969D"))
        canvas.setLineWidth(0.6)
        canvas.roundRect(0, 0, self.width, self.height, 4, stroke=1, fill=0)
        figure_type = str(self.figure.get("type") or "").lower()
        nodes = [
            node
            for node in self.figure.get("nodes", [])
            if isinstance(node, dict)
        ]
        edges = (
            self.figure.get("edges")
            or self.figure.get("connectors")
            or []
        )
        shape_types = {
            str(shape.get("type") or "").lower()
            for shape in self.figure.get("shapes", [])
            if isinstance(shape, dict)
        }
        if (
            figure_type == "expanding-spiral-process"
            or "expanding-spiral" in shape_types
        ):
            self._draw_expanding_spiral(canvas, self.figure)
        elif figure_type in {"bar-panels", "grouped-bar-panels"} or (
            self.figure.get("panels")
            and any(
                isinstance(panel, dict) and panel.get("groups")
                for panel in self.figure.get("panels", [])
            )
        ):
            self._draw_bar_panels(canvas, self.figure)
        elif self._is_quadrant_panel_figure(self.figure):
            self._draw_quadrant_panels(canvas, self.figure)
        elif self.figure.get("panels"):
            self._draw_process_panels(canvas, self.figure)
        elif figure_type == "venn" or self.figure.get("circles"):
            self._draw_venn(canvas, self.figure)
        elif figure_type == "pyramid" or self.figure.get("levels"):
            self._draw_pyramid(canvas, self.figure)
        elif (
            figure_type == "nonlinear-case-trajectory"
            or (
                self.figure.get("series")
                and not self._has_numeric_series(self.figure)
                and nodes
            )
        ):
            self._draw_trajectory(canvas, self.figure)
        elif self._has_numeric_series(self.figure):
            self._draw_series(canvas, self.figure)
        elif nodes:
            self._draw_nodes(canvas, nodes, list(edges))
        else:
            self._draw_label_layout(canvas, self.figure)
        canvas.restoreState()
