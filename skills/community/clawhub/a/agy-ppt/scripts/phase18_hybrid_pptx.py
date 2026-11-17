#!/usr/bin/env python3
"""Phase 18.3 conservative hybrid PowerPoint production.

The renderer consumes an approved element production plan.  It never chooses
evidence, wording, or narrative meaning; unsupported native representations
fall back to the explicitly supplied locked visual.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from phase18_contract import (
    ElementBox,
    PlateProvenanceMode,
    PlateRequirement,
    ProductionStrategy,
    ReservedEditableZone,
)
from phase18_production_plan import ElementProductionPlan
from presentation_workflow import SampleArtifact
from presentation_layout_grammar import (
    DEFAULT_LAYOUT_GRAMMAR,
    SLIDE_HEIGHT_16_9,
    SLIDE_WIDTH_16_9,
    suggested_font_size,
)


ERROR_HYBRID_PPTX_INVALID = "PHASE18_HYBRID_PPTX_INVALID"


class HybridPptxError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


@dataclass(frozen=True)
class TextStyle:
    font_name: str = "Aptos"
    east_asian_font_name: str = "Microsoft JhengHei"
    font_size: float = 17.0
    bold: bool = False
    color: str = "000000"
    alignment: str = "left"
    vertical_alignment: str = "top"
    line_spacing: float = 1.10
    space_after: float = 4.0
    margin_left: float = 0.04
    margin_right: float = 0.04
    margin_top: float = 0.02
    margin_bottom: float = 0.02

    def __post_init__(self) -> None:
        if (
            not isinstance(self.font_name, str) or not self.font_name.strip()
            or not isinstance(self.east_asian_font_name, str) or not self.east_asian_font_name.strip()
            or self.font_size <= 0
        ):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "text style is invalid")
        if len(self.color) != 6 or any(char not in "0123456789ABCDEFabcdef" for char in self.color):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "text color must be six hex digits")
        if self.alignment not in {"left", "center", "right"}:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "text alignment is invalid")
        if self.vertical_alignment not in {"top", "middle", "bottom"}:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "text vertical alignment is invalid")
        if self.line_spacing <= 0 or self.space_after < 0:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "text spacing is invalid")
        margins = (self.margin_left, self.margin_right, self.margin_top, self.margin_bottom)
        if any(not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0 for value in margins):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "text margins are invalid")


def text_style_for_role(role, *, language: str = "zh-TW", color: str = "172033") -> TextStyle:
    """Return a restrained native typography default based on semantic role."""
    from phase18_production_plan import ElementRole

    if not isinstance(role, ElementRole):
        raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "element role is required for typography")
    size = suggested_font_size(role)
    bold = role in {ElementRole.TITLE, ElementRole.KPI, ElementRole.PRICE, ElementRole.CTA, ElementRole.NAME}
    alignment = "center" if role in {ElementRole.KPI, ElementRole.PRICE} else "left"
    vertical = "middle" if role in {ElementRole.KPI, ElementRole.PRICE, ElementRole.CTA} else "top"
    return TextStyle(
        font_name="Aptos Display" if role is ElementRole.TITLE else "Aptos",
        east_asian_font_name="Microsoft JhengHei",
        font_size=size,
        bold=bold,
        color=color,
        alignment=alignment,
        vertical_alignment=vertical,
        line_spacing=1.02 if role in {ElementRole.TITLE, ElementRole.KPI, ElementRole.PRICE} else 1.12,
        space_after=0 if role in {ElementRole.TITLE, ElementRole.KPI, ElementRole.PRICE} else 4,
        margin_left=0,
        margin_right=0,
        margin_top=0,
        margin_bottom=0,
    )


@dataclass(frozen=True)
class ShapeStyle:
    kind: str = "rectangle"
    fill_color: str = "FFFFFF"
    line_color: str = "FFFFFF"
    line_width: float = 0.75

    def __post_init__(self) -> None:
        if self.kind not in {"rectangle", "rounded_rectangle", "divider", "right_arrow"}:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "native shape kind is unsupported")
        for color in (self.fill_color, self.line_color):
            if len(color) != 6 or any(char not in "0123456789ABCDEFabcdef" for char in color):
                raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "shape color is invalid")
        if self.line_width < 0:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "shape line width is invalid")


@dataclass(frozen=True)
class ImageStyle:
    crop_mode: str = "cover"
    focal_x: float = 0.5
    focal_y: float = 0.5
    frame_color: str | None = None
    frame_width: float = 0.0

    def __post_init__(self) -> None:
        if self.crop_mode not in {"cover", "contain", "stretch"}:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "image crop mode is invalid")
        if not 0 <= self.focal_x <= 1 or not 0 <= self.focal_y <= 1:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "image focal point is invalid")
        if self.frame_color is not None and (
            len(self.frame_color) != 6
            or any(char not in "0123456789ABCDEFabcdef" for char in self.frame_color)
        ):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "image frame color is invalid")
        if self.frame_width < 0:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "image frame width is invalid")


@dataclass(frozen=True)
class ChartStyle:
    series_colors: tuple[str, ...] = ("246BFD", "10A37F", "F59E0B", "7C3AED")
    text_color: str = "334155"
    show_legend: bool | None = None
    show_gridlines: bool = False
    show_data_labels: bool = True
    number_format: str = "0.#"
    gap_width: int = 65

    def __post_init__(self) -> None:
        colors = (*self.series_colors, self.text_color)
        if not self.series_colors or any(
            len(color) != 6 or any(char not in "0123456789ABCDEFabcdef" for char in color)
            for color in colors
        ):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart colors are invalid")
        if not isinstance(self.show_gridlines, bool) or not isinstance(self.show_data_labels, bool):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart visibility settings are invalid")
        if type(self.gap_width) is not int or not 0 <= self.gap_width <= 500:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart gap width must be between 0 and 500")


@dataclass(frozen=True)
class ChartSeries:
    name: str
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip() or not self.values:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart series is invalid")
        if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in self.values):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart values must be numeric")


@dataclass(frozen=True)
class ChartSpec:
    categories: tuple[str, ...]
    series: tuple[ChartSeries, ...]
    kind: str = "column"

    def __post_init__(self) -> None:
        if not self.categories or any(not isinstance(item, str) or not item for item in self.categories):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart categories are required")
        if not self.series or any(not isinstance(item, ChartSeries) for item in self.series):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart series are required")
        if any(len(item.values) != len(self.categories) for item in self.series):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart values must match categories")
        if self.kind not in {"column", "bar", "line"}:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "chart kind is unsupported")


@dataclass(frozen=True)
class HybridElement:
    plan: ElementProductionPlan
    box: ElementBox
    text_style: TextStyle | None = None
    shape_style: ShapeStyle | None = None
    image_path: str | None = None
    vector_fallback_path: str | None = None
    chart: ChartSpec | None = None
    image_style: ImageStyle = ImageStyle()
    chart_style: ChartStyle = ChartStyle()

    def __post_init__(self) -> None:
        if not isinstance(self.plan, ElementProductionPlan) or not isinstance(self.box, ElementBox):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "approved element plan and box are required")
        strategy = self.plan.contract.strategy
        if strategy is ProductionStrategy.NATIVE_TEXT and self.text_style is None:
            object.__setattr__(self, "text_style", text_style_for_role(self.plan.role))
        if strategy is ProductionStrategy.NATIVE_SHAPE and not isinstance(self.shape_style, ShapeStyle):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "native shape requires shape style")
        if strategy in {ProductionStrategy.NATIVE_IMAGE, ProductionStrategy.RASTER_REGION, ProductionStrategy.LOCKED_VISUAL, ProductionStrategy.FULL_RASTER_SLIDE}:
            if not self.image_path or not Path(self.image_path).is_file():
                raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "image-backed strategy requires an existing image")
        if strategy is ProductionStrategy.VECTOR_GRAPHIC and not self.image_path:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "vector strategy requires a vector source")
        if strategy is ProductionStrategy.NATIVE_CHART and not isinstance(self.chart, ChartSpec):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "native chart requires structured data")
        if not isinstance(self.image_style, ImageStyle) or not isinstance(self.chart_style, ChartStyle):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "visual styling contract is invalid")


@dataclass(frozen=True)
class HybridSlide:
    slide_id: str
    elements: tuple[HybridElement, ...]
    speaker_notes: str = ""
    background_color: str = "FFFFFF"
    plate_mode: PlateProvenanceMode = PlateProvenanceMode.CLEAN_PLATE
    reserved_zones: tuple[ReservedEditableZone, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.slide_id, str) or not self.slide_id.strip():
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "slide id is required")
        elements = tuple(self.elements)
        if not elements or any(not isinstance(item, HybridElement) for item in elements):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "slide elements are required")
        if len({item.plan.element_id for item in elements}) != len(elements):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "element ids must be unique per slide")
        full = [item for item in elements if item.plan.contract.strategy is ProductionStrategy.FULL_RASTER_SLIDE]
        if full and len(elements) != 1:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "full-raster fallback cannot hide other planned objects")
        if len(self.background_color) != 6:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "background color is invalid")
        if not isinstance(self.plate_mode, PlateProvenanceMode):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "plate mode is invalid")
        for item in elements:
            if not DEFAULT_LAYOUT_GRAMMAR.inside_slide(item.box):
                raise HybridPptxError(
                    ERROR_HYBRID_PPTX_INVALID,
                    f"element '{item.plan.element_id}' extends outside the canonical 10 x 5.625 inch slide",
                )
        zones = tuple(self.reserved_zones)
        if any(not isinstance(z, ReservedEditableZone) for z in zones):
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "reserved zones are invalid")

        # Composite conflict enforcement:
        # 1. FULL_COMPOSITE prohibits native editable overlays
        if self.plate_mode is PlateProvenanceMode.FULL_COMPOSITE:
            for item in elements:
                if item.plan.contract.strategy in {
                    ProductionStrategy.NATIVE_TEXT,
                    ProductionStrategy.NATIVE_IMAGE,
                    ProductionStrategy.NATIVE_CHART,
                }:
                    raise HybridPptxError(
                        ERROR_HYBRID_PPTX_INVALID,
                        f"composite conflict: cannot overlay native element '{item.plan.element_id}' on FULL_COMPOSITE plate",
                    )
        # 2. PARTIAL_COMPOSITE requires a CONTENT_FREE reserved zone for each native overlay
        elif self.plate_mode is PlateProvenanceMode.PARTIAL_COMPOSITE:
            content_free_ids = {
                z.element_id for z in zones if z.plate_requirement is PlateRequirement.CONTENT_FREE
            }
            for item in elements:
                if item.plan.contract.strategy in {
                    ProductionStrategy.NATIVE_TEXT,
                    ProductionStrategy.NATIVE_IMAGE,
                    ProductionStrategy.NATIVE_CHART,
                }:
                    if item.plan.element_id not in content_free_ids:
                        raise HybridPptxError(
                            ERROR_HYBRID_PPTX_INVALID,
                            f"composite conflict: native element '{item.plan.element_id}' lacks CONTENT_FREE reserved zone on PARTIAL_COMPOSITE plate",
                        )

        object.__setattr__(self, "elements", elements)
        object.__setattr__(self, "reserved_zones", zones)


def _shape_type(kind: str):
    from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
    return {
        "rectangle": MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        "rounded_rectangle": MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        "divider": MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        "right_arrow": MSO_AUTO_SHAPE_TYPE.RIGHT_ARROW,
    }[kind]


def _set_object_name(shape, element: HybridElement, suffix: str = "") -> None:
    shape.name = f"agy:{element.plan.element_id}{suffix}"


def _set_east_asian_font(run, typeface: str) -> None:
    from pptx.oxml.ns import qn
    from pptx.oxml.xmlchemy import OxmlElement

    properties = run._r.get_or_add_rPr()
    existing = properties.find(qn("a:ea"))
    if existing is None:
        existing = OxmlElement("a:ea")
        properties.append(existing)
    existing.set("typeface", typeface)


def _add_picture_with_treatment(slide, element: HybridElement, source: str, geometry):
    from PIL import Image
    from pptx.dml.color import RGBColor
    from pptx.util import Pt

    style = element.image_style
    shape = slide.shapes.add_picture(source, *geometry)
    if style.crop_mode == "cover":
        with Image.open(source) as image:
            source_ratio = image.width / image.height
        target_ratio = element.box.width / element.box.height
        if source_ratio > target_ratio:
            crop = 1 - target_ratio / source_ratio
            shape.crop_left = crop * style.focal_x
            shape.crop_right = crop * (1 - style.focal_x)
        elif source_ratio < target_ratio:
            crop = 1 - source_ratio / target_ratio
            shape.crop_top = crop * style.focal_y
            shape.crop_bottom = crop * (1 - style.focal_y)
    if style.frame_color and style.frame_width > 0:
        shape.line.color.rgb = RGBColor.from_string(style.frame_color)
        shape.line.width = Pt(style.frame_width)
    return shape


def _add_element(slide, element: HybridElement) -> None:
    from pptx.chart.data import ChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt

    box = element.box
    geometry = (Inches(box.left), Inches(box.top), Inches(box.width), Inches(box.height))
    strategy = element.plan.contract.strategy
    if strategy is ProductionStrategy.NATIVE_TEXT:
        shape = slide.shapes.add_textbox(*geometry)
        frame = shape.text_frame
        frame.clear()
        frame.word_wrap = True
        frame.margin_left = Inches(element.text_style.margin_left)
        frame.margin_right = Inches(element.text_style.margin_right)
        frame.margin_top = Inches(element.text_style.margin_top)
        frame.margin_bottom = Inches(element.text_style.margin_bottom)
        frame.vertical_anchor = {
            "top": MSO_ANCHOR.TOP,
            "middle": MSO_ANCHOR.MIDDLE,
            "bottom": MSO_ANCHOR.BOTTOM,
        }[element.text_style.vertical_alignment]
        lines = element.plan.approved_content.splitlines() or [element.plan.approved_content]
        frame.paragraphs[0].text = lines[0]
        for line in lines[1:]:
            frame.add_paragraph().text = line
        alignments = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
        for paragraph in frame.paragraphs:
            paragraph.alignment = alignments[element.text_style.alignment]
            paragraph.line_spacing = element.text_style.line_spacing
            paragraph.space_after = Pt(element.text_style.space_after)
            for run in paragraph.runs:
                run.font.name = element.text_style.font_name
                _set_east_asian_font(run, element.text_style.east_asian_font_name)
                run.font.size = Pt(element.text_style.font_size)
                run.font.bold = element.text_style.bold
                run.font.color.rgb = RGBColor.from_string(element.text_style.color)
        _set_object_name(shape, element)
    elif strategy is ProductionStrategy.NATIVE_SHAPE:
        shape = slide.shapes.add_shape(_shape_type(element.shape_style.kind), *geometry)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor.from_string(element.shape_style.fill_color)
        shape.line.color.rgb = RGBColor.from_string(element.shape_style.line_color)
        shape.line.width = Pt(element.shape_style.line_width)
        _set_object_name(shape, element)
    elif strategy is ProductionStrategy.NATIVE_CHART:
        data = ChartData()
        data.categories = element.chart.categories
        for series in element.chart.series:
            data.add_series(series.name, series.values)
        chart_types = {
            "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
            "bar": XL_CHART_TYPE.BAR_CLUSTERED,
            "line": XL_CHART_TYPE.LINE,
        }
        graphic_frame = slide.shapes.add_chart(chart_types[element.chart.kind], *geometry, data)
        chart = graphic_frame.chart
        style = element.chart_style
        chart.has_title = False
        chart.has_legend = style.show_legend if style.show_legend is not None else len(element.chart.series) > 1
        if chart.has_legend:
            chart.legend.font.size = Pt(11)
            chart.legend.font.color.rgb = RGBColor.from_string(style.text_color)
        if chart.value_axis is not None:
            chart.value_axis.has_major_gridlines = style.show_gridlines
            chart.value_axis.tick_labels.font.size = Pt(10)
            chart.value_axis.tick_labels.font.color.rgb = RGBColor.from_string(style.text_color)
            chart.value_axis.tick_labels.number_format = style.number_format
        if chart.category_axis is not None:
            chart.category_axis.tick_labels.font.size = Pt(10)
            chart.category_axis.tick_labels.font.color.rgb = RGBColor.from_string(style.text_color)
        if style.show_data_labels:
            plot = chart.plots[0]
            if hasattr(plot, "gap_width"):
                plot.gap_width = style.gap_width
            plot.has_data_labels = True
            plot.data_labels.font.size = Pt(10)
            plot.data_labels.font.bold = True
            plot.data_labels.font.color.rgb = RGBColor.from_string(style.text_color)
            plot.data_labels.number_format = style.number_format
        elif hasattr(chart.plots[0], "gap_width"):
            chart.plots[0].gap_width = style.gap_width
        for index, series in enumerate(chart.series):
            color = style.series_colors[index % len(style.series_colors)]
            series.format.fill.solid()
            series.format.fill.fore_color.rgb = RGBColor.from_string(color)
            series.format.line.color.rgb = RGBColor.from_string(color)
        _set_object_name(graphic_frame, element)
    else:
        source = element.image_path
        suffix = ""
        if strategy is ProductionStrategy.VECTOR_GRAPHIC:
            try:
                shape = slide.shapes.add_picture(source, *geometry)
                _set_object_name(shape, element)
                return
            except Exception as exc:
                fallback = element.vector_fallback_path
                if not fallback or not Path(fallback).is_file():
                    raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "vector source needs a compatible raster fallback") from exc
                source = fallback
                suffix = ":vector-fallback"
        if element.image_style.crop_mode == "contain":
            shape = slide.shapes.add_picture(source, geometry[0], geometry[1], width=geometry[2])
        elif element.image_style.crop_mode == "stretch":
            shape = slide.shapes.add_picture(source, *geometry)
        else:
            shape = _add_picture_with_treatment(slide, element, source, geometry)
        _set_object_name(shape, element, suffix)


def create_hybrid_presentation(
    slides: Iterable[HybridSlide],
    output_path: str,
    *,
    aspect_ratio: str = "16:9",
) -> bool:
    """Create a hybrid PPTX without changing approved semantic content."""
    clean = tuple(slides)
    if not clean or any(not isinstance(item, HybridSlide) for item in clean):
        raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "hybrid slides are required")
    if len({item.slide_id for item in clean}) != len(clean):
        raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "slide ids must be unique")
    try:
        from pptx import Presentation
        from pptx.dml.color import RGBColor
        from pptx.util import Inches

        prs = Presentation()
        if aspect_ratio == "16:9":
            prs.slide_width, prs.slide_height = Inches(SLIDE_WIDTH_16_9), Inches(SLIDE_HEIGHT_16_9)
        elif aspect_ratio == "4:3":
            prs.slide_width, prs.slide_height = Inches(10), Inches(7.5)
        else:
            raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "unsupported aspect ratio")
        for spec in clean:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            background = slide.background.fill
            background.solid()
            background.fore_color.rgb = RGBColor.from_string(spec.background_color)
            for element in spec.elements:
                _add_element(slide, element)
            if spec.speaker_notes:
                notes = slide.notes_slide.notes_text_frame
                notes.clear()
                notes.text = spec.speaker_notes
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        prs.save(destination)
        return True
    except HybridPptxError:
        raise
    except Exception as exc:
        raise HybridPptxError(ERROR_HYBRID_PPTX_INVALID, "hybrid PowerPoint production failed") from exc


def render_hybrid_sample_preview(
    slide: HybridSlide,
    output_path: str | Path,
    *,
    aspect_ratio: str = "16:9",
) -> SampleArtifact:
    """Render a deterministic hybrid sample preview artifact from a HybridSlide specification."""
    dest = Path(output_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    create_hybrid_presentation((slide,), str(dest), aspect_ratio=aspect_ratio)
    manifest = {
        "slide_id": slide.slide_id,
        "speaker_notes": slide.speaker_notes,
        "background_color": slide.background_color,
        "plate_mode": slide.plate_mode.value,
        "reserved_zones": [zone.internal_dict() for zone in slide.reserved_zones],
        "elements": [
            {
                "plan": element.plan.internal_dict(),
                "box": element.box.internal_dict(),
                "text_style": asdict(element.text_style) if element.text_style else None,
                "shape_style": asdict(element.shape_style) if element.shape_style else None,
                "chart": asdict(element.chart) if element.chart else None,
                "image_style": asdict(element.image_style),
                "chart_style": asdict(element.chart_style),
                "image_sha256": (
                    hashlib.sha256(Path(element.image_path).read_bytes()).hexdigest()
                    if element.image_path and Path(element.image_path).is_file()
                    else None
                ),
            }
            for element in slide.elements
        ],
    }
    manifest_hash = hashlib.sha256(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    preview_hash = hashlib.sha256(dest.read_bytes()).hexdigest()
    return SampleArtifact(
        artifact_ref=str(dest),
        provenance={
            "artifact_kind": "HYBRID_PREVIEW",
            "artifact_ref": str(dest),
            "hybrid_manifest_sha256": manifest_hash,
            "rendered_preview_sha256": preview_hash,
        },
    )


__all__ = [
    "ERROR_HYBRID_PPTX_INVALID", "ChartSeries", "ChartSpec", "ElementBox",
    "ChartStyle", "HybridElement", "HybridPptxError", "HybridSlide", "ImageStyle",
    "ShapeStyle", "TextStyle", "text_style_for_role",
    "create_hybrid_presentation", "render_hybrid_sample_preview",
]
