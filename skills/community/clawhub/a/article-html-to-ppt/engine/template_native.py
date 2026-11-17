"""Native PPTX template primitives.

Path C copies selected editable template objects at the OOXML-package level.
This first primitive is deliberately narrow: a chart graphic frame and every
internal relationship it needs (including its embedded workbook) move together.
"""
from __future__ import annotations

from copy import deepcopy
import posixpath
from pathlib import Path
from xml.etree import ElementTree as ET
import zipfile


CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
PRESENTATION_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CHART_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

for _prefix, _namespace in {
    "": CONTENT_TYPES_NS,
    "p": PRESENTATION_NS,
    "r": REL_NS,
    "c": CHART_NS,
}.items():
    ET.register_namespace(_prefix, _namespace)


def _q(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def _rels_name(part_name: str) -> str:
    return f"{posixpath.dirname(part_name)}/_rels/{posixpath.basename(part_name)}.rels"


def _resolve_target(part_name: str, target: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(part_name), target))


def _relative_target(source_part: str, target_part: str) -> str:
    return posixpath.relpath(target_part, posixpath.dirname(source_part))


def _part_name_in_use(part_name: str, parts: dict[str, bytes], part_map: dict[str, str]) -> bool:
    return part_name in parts or part_name in part_map.values()


def _next_part_name(source_part: str, destination_parts: dict[str, bytes], part_map: dict[str, str]) -> str:
    """Keep the familiar original name unless that exact package part exists."""
    if not _part_name_in_use(source_part, destination_parts, part_map):
        return source_part
    parent, filename = posixpath.dirname(source_part), posixpath.basename(source_part)
    stem, suffix = posixpath.splitext(filename)
    index = 2
    while True:
        candidate = f"{parent}/{stem}-templatecopy-{index}{suffix}"
        if not _part_name_in_use(candidate, destination_parts, part_map):
            return candidate
        index += 1


def _copy_content_type(
    source_types: ET.Element,
    destination_types: ET.Element,
    source_part: str,
    destination_part: str,
) -> None:
    source_override = next(
        (item for item in source_types.findall(_q(CONTENT_TYPES_NS, "Override"))
         if item.get("PartName") == f"/{source_part}"),
        None,
    )
    if source_override is not None:
        wanted = f"/{destination_part}"
        existing = {item.get("PartName") for item in destination_types.findall(_q(CONTENT_TYPES_NS, "Override"))}
        if wanted not in existing:
            ET.SubElement(destination_types, _q(CONTENT_TYPES_NS, "Override"), {
                "PartName": wanted,
                "ContentType": source_override.get("ContentType", ""),
            })
        return

    extension = posixpath.splitext(source_part)[1].lstrip(".")
    source_default = next(
        (item for item in source_types.findall(_q(CONTENT_TYPES_NS, "Default"))
         if item.get("Extension") == extension),
        None,
    )
    existing_extensions = {item.get("Extension") for item in destination_types.findall(_q(CONTENT_TYPES_NS, "Default"))}
    if source_default is not None and extension not in existing_extensions:
        ET.SubElement(destination_types, _q(CONTENT_TYPES_NS, "Default"), {
            "Extension": extension,
            "ContentType": source_default.get("ContentType", ""),
        })


def _copy_closure(
    source_parts: dict[str, bytes],
    destination_parts: dict[str, bytes],
    source_types: ET.Element,
    destination_types: ET.Element,
    source_part: str,
    part_map: dict[str, str],
    copied_parts: list[str],
) -> str:
    if source_part in part_map:
        return part_map[source_part]
    if source_part not in source_parts:
        raise ValueError(f"Template relationship target is missing: {source_part}")

    destination_part = _next_part_name(source_part, destination_parts, part_map)
    part_map[source_part] = destination_part
    destination_parts[destination_part] = source_parts[source_part]
    copied_parts.append(destination_part)
    _copy_content_type(source_types, destination_types, source_part, destination_part)

    source_rels_name = _rels_name(source_part)
    if source_rels_name not in source_parts:
        return destination_part

    relationships = ET.fromstring(source_parts[source_rels_name])
    for relationship in relationships.findall(_q(PACKAGE_REL_NS, "Relationship")):
        if relationship.get("TargetMode") == "External":
            continue
        target = relationship.get("Target")
        if not target:
            raise ValueError(f"Template relationship has no target: {source_rels_name}")
        source_target = _resolve_target(source_part, target)
        destination_target = _copy_closure(
            source_parts, destination_parts, source_types, destination_types,
            source_target, part_map, copied_parts,
        )
        relationship.set("Target", _relative_target(destination_part, destination_target))

    destination_parts[_rels_name(destination_part)] = ET.tostring(
        relationships, encoding="utf-8", xml_declaration=True,
    )
    return destination_part


def _slide_part(slide_index: int) -> str:
    if slide_index < 1:
        raise ValueError("slide indices are 1-based")
    return f"ppt/slides/slide{slide_index}.xml"


def _chart_frame(slide: ET.Element, chart_name: str | None) -> tuple[ET.Element, str, str]:
    matches: list[tuple[ET.Element, str, str]] = []
    for frame in slide.findall(f".//{_q(PRESENTATION_NS, 'graphicFrame')}"):
        chart = frame.find(f".//{_q(CHART_NS, 'chart')}")
        if chart is None:
            continue
        name_element = frame.find(f".//{_q(PRESENTATION_NS, 'cNvPr')}")
        name = name_element.get("name", "") if name_element is not None else ""
        relationship_id = chart.get(_q(REL_NS, "id"))
        if not relationship_id:
            raise ValueError("Chart frame has no relationship id")
        matches.append((frame, name, relationship_id))

    if chart_name is not None:
        matches = [match for match in matches if match[1] == chart_name]
    if not matches:
        requested = f" named {chart_name!r}" if chart_name else ""
        raise ValueError(f"No chart frame{requested} found on template slide")
    if len(matches) > 1:
        raise ValueError("Template slide has multiple chart frames; specify chart_name")
    return matches[0]


def _next_relationship_id(relationships: ET.Element) -> str:
    values = []
    for item in relationships.findall(_q(PACKAGE_REL_NS, "Relationship")):
        value = item.get("Id", "")
        if value.startswith("rId") and value[3:].isdigit():
            values.append(int(value[3:]))
    return f"rId{max(values, default=0) + 1}"


def _frame_name_element(frame: ET.Element) -> ET.Element:
    element = frame.find(f".//{_q(PRESENTATION_NS, 'cNvPr')}")
    if element is None:
        raise ValueError("Template graphic frame has no non-visual properties")
    return element


def _prepare_frame_for_destination(frame: ET.Element, destination_slide: ET.Element) -> str:
    """Avoid duplicate shape ids and names when adding a template graphic frame."""
    properties = _frame_name_element(frame)
    ids = [
        int(item.get("id", "0"))
        for item in destination_slide.findall(f".//{_q(PRESENTATION_NS, 'cNvPr')}")
        if item.get("id", "").isdigit()
    ]
    properties.set("id", str(max(ids, default=0) + 1))
    original_name = properties.get("name", "template-object")
    names = {
        item.get("name", "")
        for item in destination_slide.findall(f".//{_q(PRESENTATION_NS, 'cNvPr')}")
    }
    resolved_name = original_name
    index = 2
    while resolved_name in names:
        resolved_name = f"{original_name}-templatecopy-{index}"
        index += 1
    properties.set("name", resolved_name)
    return resolved_name


def _table_frame(slide: ET.Element, table_name: str | None) -> tuple[ET.Element, str]:
    matches: list[tuple[ET.Element, str]] = []
    for frame in slide.findall(f".//{_q(PRESENTATION_NS, 'graphicFrame')}"):
        if frame.find(f".//{_q(DRAWING_NS, 'tbl')}") is None:
            continue
        name = _frame_name_element(frame).get("name", "")
        matches.append((frame, name))
    if table_name is not None:
        matches = [match for match in matches if match[1] == table_name]
    if not matches:
        requested = f" named {table_name!r}" if table_name else ""
        raise ValueError(f"No table frame{requested} found on slide")
    if len(matches) > 1:
        raise ValueError("Slide has multiple table frames; specify table_name")
    return matches[0]


def _write_package(path: Path, parts: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(parts):
            archive.writestr(name, parts[name])


def clone_chart_shape(
    source_pptx: str | Path,
    destination_pptx: str | Path,
    *,
    source_slide_index: int,
    destination_slide_index: int,
    chart_name: str | None = None,
) -> dict:
    """Clone one editable chart into an existing slide, with its data workbook.

    The destination presentation is updated in place.  The copied chart keeps
    its OOXML chart part, chart relationships and embedded workbook instead of
    becoming a picture or retaining a relationship back to the source file.
    """
    source_path, destination_path = Path(source_pptx), Path(destination_pptx)
    with zipfile.ZipFile(source_path) as archive:
        source_parts = {item.filename: archive.read(item.filename) for item in archive.infolist()}
    with zipfile.ZipFile(destination_path) as archive:
        destination_parts = {item.filename: archive.read(item.filename) for item in archive.infolist()}

    source_slide_part = _slide_part(source_slide_index)
    destination_slide_part = _slide_part(destination_slide_index)
    if source_slide_part not in source_parts:
        raise ValueError(f"Template slide does not exist: {source_slide_index}")
    if destination_slide_part not in destination_parts:
        raise ValueError(f"Destination slide does not exist: {destination_slide_index}")

    source_slide = ET.fromstring(source_parts[source_slide_part])
    destination_slide = ET.fromstring(destination_parts[destination_slide_part])
    frame, resolved_name, source_relationship_id = _chart_frame(source_slide, chart_name)
    source_rels_part = _rels_name(source_slide_part)
    source_relationships = ET.fromstring(source_parts[source_rels_part])
    source_relationship = next(
        (item for item in source_relationships.findall(_q(PACKAGE_REL_NS, "Relationship"))
         if item.get("Id") == source_relationship_id),
        None,
    )
    if source_relationship is None or not source_relationship.get("Type", "").endswith("/chart"):
        raise ValueError("Chart frame does not resolve to a chart relationship")

    source_chart_part = _resolve_target(source_slide_part, source_relationship.get("Target", ""))
    source_types = ET.fromstring(source_parts["[Content_Types].xml"])
    destination_types = ET.fromstring(destination_parts["[Content_Types].xml"])
    part_map: dict[str, str] = {}
    copied_parts: list[str] = []
    destination_chart_part = _copy_closure(
        source_parts, destination_parts, source_types, destination_types,
        source_chart_part, part_map, copied_parts,
    )

    destination_rels_part = _rels_name(destination_slide_part)
    destination_relationships = ET.fromstring(destination_parts[destination_rels_part])
    destination_relationship_id = _next_relationship_id(destination_relationships)
    ET.SubElement(destination_relationships, _q(PACKAGE_REL_NS, "Relationship"), {
        "Id": destination_relationship_id,
        "Type": source_relationship.get("Type", ""),
        "Target": _relative_target(destination_slide_part, destination_chart_part),
    })

    copied_frame = deepcopy(frame)
    copied_chart = copied_frame.find(f".//{_q(CHART_NS, 'chart')}")
    assert copied_chart is not None
    copied_chart.set(_q(REL_NS, "id"), destination_relationship_id)
    destination_tree = destination_slide.find(f".//{_q(PRESENTATION_NS, 'spTree')}")
    if destination_tree is None:
        raise ValueError("Destination slide has no shape tree")
    copied_name = _prepare_frame_for_destination(copied_frame, destination_slide)
    destination_tree.append(copied_frame)

    destination_parts[destination_slide_part] = ET.tostring(destination_slide, encoding="utf-8", xml_declaration=True)
    destination_parts[destination_rels_part] = ET.tostring(destination_relationships, encoding="utf-8", xml_declaration=True)
    destination_parts["[Content_Types].xml"] = ET.tostring(destination_types, encoding="utf-8", xml_declaration=True)
    _write_package(destination_path, destination_parts)

    return {
        "chart_name": copied_name,
        "source_chart_name": resolved_name,
        "source_slide_index": source_slide_index,
        "destination_slide_index": destination_slide_index,
        "copied_parts": copied_parts,
    }


def clone_table_shape(
    source_pptx: str | Path,
    destination_pptx: str | Path,
    *,
    source_slide_index: int,
    destination_slide_index: int,
    table_name: str | None = None,
) -> dict:
    """Clone one native table frame while preserving its table XML and styling."""
    source_path, destination_path = Path(source_pptx), Path(destination_pptx)
    with zipfile.ZipFile(source_path) as archive:
        source_parts = {item.filename: archive.read(item.filename) for item in archive.infolist()}
    with zipfile.ZipFile(destination_path) as archive:
        destination_parts = {item.filename: archive.read(item.filename) for item in archive.infolist()}
    source_slide_part = _slide_part(source_slide_index)
    destination_slide_part = _slide_part(destination_slide_index)
    if source_slide_part not in source_parts:
        raise ValueError(f"Template slide does not exist: {source_slide_index}")
    if destination_slide_part not in destination_parts:
        raise ValueError(f"Destination slide does not exist: {destination_slide_index}")

    source_slide = ET.fromstring(source_parts[source_slide_part])
    destination_slide = ET.fromstring(destination_parts[destination_slide_part])
    frame, source_name = _table_frame(source_slide, table_name)
    copied_frame = deepcopy(frame)
    copied_name = _prepare_frame_for_destination(copied_frame, destination_slide)
    destination_tree = destination_slide.find(f".//{_q(PRESENTATION_NS, 'spTree')}")
    if destination_tree is None:
        raise ValueError("Destination slide has no shape tree")
    destination_tree.append(copied_frame)
    destination_parts[destination_slide_part] = ET.tostring(destination_slide, encoding="utf-8", xml_declaration=True)
    _write_package(destination_path, destination_parts)
    return {
        "table_name": copied_name,
        "source_table_name": source_name,
        "source_slide_index": source_slide_index,
        "destination_slide_index": destination_slide_index,
    }


def _validate_table_binding_name(binding_name: str) -> None:
    parts = binding_name.split(":")
    if len(parts) != 4 or parts[:2] != ["bind", "table"] or not all(parts[2:]):
        raise ValueError("binding_name must be bind:table:<slide_id>:<block_id>")


def _validate_chart_binding_name(binding_name: str) -> None:
    parts = binding_name.split(":")
    if len(parts) not in {3, 4} or parts[:2] != ["bind", "chart"] or not all(parts[2:]):
        raise ValueError(
            "binding_name must be bind:chart:<slide_id> or bind:chart:<slide_id>:<chart_id>"
        )


def bind_table_data(
    pptx_path: str | Path,
    *,
    slide_index: int,
    table_name: str,
    binding_name: str,
    rows: list[list[str]],
) -> dict:
    """Fill a cloned table without changing its fixed template row/column contract.

    The binding name is the existing Authoring Manifest table protocol.  Later
    source verification can therefore reject any cell that does not exactly
    match the source table window associated with that block.
    """
    _validate_table_binding_name(binding_name)
    path = Path(pptx_path)
    with zipfile.ZipFile(path) as archive:
        parts = {item.filename: archive.read(item.filename) for item in archive.infolist()}
    slide_part = _slide_part(slide_index)
    if slide_part not in parts:
        raise ValueError(f"Destination slide does not exist: {slide_index}")
    slide = ET.fromstring(parts[slide_part])
    frame, _ = _table_frame(slide, table_name)
    table = frame.find(f".//{_q(DRAWING_NS, 'tbl')}")
    assert table is not None
    xml_rows = table.findall(_q(DRAWING_NS, "tr"))
    if len(rows) != len(xml_rows):
        raise ValueError(f"Table row count mismatch: template has {len(xml_rows)}, data has {len(rows)}")
    for row_index, (values, xml_row) in enumerate(zip(rows, xml_rows)):
        cells = xml_row.findall(_q(DRAWING_NS, "tc"))
        if len(values) != len(cells):
            raise ValueError(
                f"Table column count mismatch at row {row_index}: template has {len(cells)}, data has {len(values)}"
            )
        for value, cell in zip(values, cells):
            text_nodes = cell.findall(f".//{_q(DRAWING_NS, 't')}")
            if not text_nodes:
                paragraph = cell.find(_q(DRAWING_NS, "p"))
                if paragraph is None:
                    paragraph = ET.SubElement(cell, _q(DRAWING_NS, "p"))
                run = ET.SubElement(paragraph, _q(DRAWING_NS, "r"))
                text_nodes = [ET.SubElement(run, _q(DRAWING_NS, "t"))]
            text_nodes[0].text = str(value)
            for extra in text_nodes[1:]:
                extra.text = ""
    _frame_name_element(frame).set("name", binding_name)
    parts[slide_part] = ET.tostring(slide, encoding="utf-8", xml_declaration=True)
    _write_package(path, parts)
    return {
        "binding_name": binding_name,
        "slide_index": slide_index,
        "row_count": len(rows),
        "column_count": len(rows[0]) if rows else 0,
    }


def bind_chart_shape(
    pptx_path: str | Path,
    *,
    slide_index: int,
    chart_name: str,
    binding_name: str,
) -> dict:
    """Give a cloned native chart its source-lock binding name."""
    _validate_chart_binding_name(binding_name)
    path = Path(pptx_path)
    with zipfile.ZipFile(path) as archive:
        package = {item.filename: archive.read(item.filename) for item in archive.infolist()}
    slide_part = _slide_part(slide_index)
    if slide_part not in package:
        raise ValueError(f"Destination slide does not exist: {slide_index}")
    slide = ET.fromstring(package[slide_part])
    frame, _name, _relationship = _chart_frame(slide, chart_name)
    _frame_name_element(frame).set("name", binding_name)
    package[slide_part] = ET.tostring(slide, encoding="utf-8", xml_declaration=True)
    _write_package(path, package)
    return {"binding_name": binding_name, "slide_index": slide_index}


def _iter_pptx_shapes(shapes):
    """Yield shapes recursively so grouped template charts remain addressable."""
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    for shape in shapes:
        yield shape
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _iter_pptx_shapes(shape.shapes)


def bind_chart_data(
    pptx_path: str | Path,
    *,
    slide_index: int,
    chart_name: str,
    binding_name: str,
    categories: list[str],
    series: list[dict],
) -> dict:
    """Replace data in one existing native chart and attach its source binding.

    ``python-pptx`` writes both the chart caches and the embedded workbook,
    which keeps the result editable in PowerPoint.  This operation is limited
    to category charts with a fixed, declared series matrix; it deliberately
    does not create charts, change geometry, or alter chart formatting.
    """
    _validate_chart_binding_name(binding_name)
    if slide_index < 1:
        raise ValueError("slide indices are 1-based")
    if not categories or any(not isinstance(category, str) or not category.strip() for category in categories):
        raise ValueError("chart categories must be a non-empty list of strings")
    if not series:
        raise ValueError("chart series must be a non-empty list")
    for item in series:
        values = item.get("values") if isinstance(item, dict) else None
        if not isinstance(item, dict) or not str(item.get("name", "")).strip():
            raise ValueError("each chart series requires a non-empty name")
        if not isinstance(values, list) or len(values) != len(categories):
            raise ValueError("each chart series must match the category count")
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
            raise ValueError("chart values must be numeric")

    from pptx import Presentation
    from pptx.chart.data import CategoryChartData

    path = Path(pptx_path)
    presentation = Presentation(path)
    if slide_index > len(presentation.slides):
        raise ValueError(f"Destination slide does not exist: {slide_index}")
    matches = [
        shape for shape in _iter_pptx_shapes(presentation.slides[slide_index - 1].shapes)
        if getattr(shape, "has_chart", False) and shape.name == chart_name
    ]
    if not matches:
        raise ValueError(f"No chart frame named {chart_name!r} found on slide")
    if len(matches) > 1:
        raise ValueError(f"Multiple chart frames named {chart_name!r} found on slide")

    data = CategoryChartData()
    data.categories = categories
    for item in series:
        data.add_series(str(item["name"]), tuple(item["values"]))
    shape = matches[0]
    shape.chart.replace_data(data)
    shape.name = binding_name
    presentation.save(path)
    return {
        "binding_name": binding_name,
        "slide_index": slide_index,
        "category_count": len(categories),
        "series_count": len(series),
    }


def bind_text_shape(
    pptx_path: str | Path,
    *,
    slide_index: int,
    shape_name: str,
    binding_name: str,
    text: str,
) -> dict:
    """Update one declared template text frame while retaining its run styling."""
    if not binding_name.startswith("bind:"):
        raise ValueError("binding_name must begin with bind:")
    if slide_index < 1:
        raise ValueError("slide indices are 1-based")
    from pptx import Presentation

    path = Path(pptx_path)
    presentation = Presentation(path)
    if slide_index > len(presentation.slides):
        raise ValueError(f"Destination slide does not exist: {slide_index}")
    matches = [
        shape for shape in _iter_pptx_shapes(presentation.slides[slide_index - 1].shapes)
        if getattr(shape, "has_text_frame", False) and shape.name == shape_name
    ]
    if not matches:
        raise ValueError(f"No text frame named {shape_name!r} found on slide")
    if len(matches) > 1:
        raise ValueError(f"Multiple text frames named {shape_name!r} found on slide")
    frame = matches[0].text_frame
    paragraph = frame.paragraphs[0]
    if paragraph.runs:
        paragraph.runs[0].text = text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run().text = text
    for extra_paragraph in frame.paragraphs[1:]:
        for run in extra_paragraph.runs:
            run.text = ""
    shape = matches[0]
    shape.name = binding_name
    presentation.save(path)
    return {"binding_name": binding_name, "slide_index": slide_index, "text_length": len(text)}


def fit_text_background(
    pptx_path: str | Path,
    *,
    slide_index: int,
    text_shape_name: str,
    background_shape_name: str,
    container_shape_name: str,
    padding_x_pt: float = 8.0,
    padding_y_pt: float = 3.0,
) -> dict:
    """Resize a reviewed label badge to its bound text inside a fixed card.

    Compact KPI cards often contain a small accent badge whose sample width is
    tied to the source copy.  Reusing that width for a longer model-authored
    title creates awkward wrapping.  The card remains fixed; only the text box
    and its explicitly reviewed companion badge grow within the card bounds.
    """
    if slide_index < 1:
        raise ValueError("slide indices are 1-based")
    from math import ceil
    from pptx import Presentation
    from pptx.util import Pt

    path = Path(pptx_path)
    presentation = Presentation(path)
    slide = presentation.slides[slide_index - 1]
    index = {shape.name: shape for shape in _iter_pptx_shapes(slide.shapes)}
    text_shape = index.get(text_shape_name)
    background = index.get(background_shape_name)
    container = index.get(container_shape_name)
    if text_shape is None or background is None or container is None:
        raise ValueError("responsive text background references a missing cloned shape")
    text = " ".join(str(getattr(text_shape, "text", "") or "").split())
    runs = [run for paragraph in text_shape.text_frame.paragraphs for run in paragraph.runs]
    font_pt = max((run.font.size.pt for run in runs if run.font.size), default=11.0)
    pad_x = int(Pt(padding_x_pt))
    pad_y = int(Pt(padding_y_pt))
    max_text_width = max(container.width - 2 * pad_x, 1)
    estimated_text_width = max(int(len(text) * font_pt * 0.55 * 12700), text_shape.width)
    lines = max(1, ceil(estimated_text_width / max_text_width))
    text_width = min(max_text_width, estimated_text_width)
    text_height = max(text_shape.height, int(lines * font_pt * 1.28 * 12700))
    text_shape.width = text_width
    text_shape.height = text_height
    text_shape.left = int(container.left + (container.width - text_width) / 2)
    background.width = min(container.width, text_width + 2 * pad_x)
    background.height = text_height + 2 * pad_y
    background.left = int(container.left + (container.width - background.width) / 2)
    background.top = max(container.top + pad_y, text_shape.top - pad_y)
    presentation.save(path)
    return {
        "text_shape_name": text_shape_name,
        "background_shape_name": background_shape_name,
        "line_count": lines,
        "width": int(background.width),
        "height": int(background.height),
    }


def fit_text_to_container(
    pptx_path: str | Path,
    *,
    slide_index: int,
    text_shape_name: str,
    container_shape_name: str,
    maximum_width_ratio: float = 0.5,
) -> dict:
    """Give a short KPI value enough width without moving it outside its card."""
    from pptx import Presentation
    from pptx.enum.text import PP_ALIGN

    path = Path(pptx_path)
    presentation = Presentation(path)
    slide = presentation.slides[slide_index - 1]
    index = {shape.name: shape for shape in _iter_pptx_shapes(slide.shapes)}
    text_shape = index.get(text_shape_name)
    container = index.get(container_shape_name)
    if text_shape is None or container is None:
        raise ValueError("responsive text field references a missing cloned shape")
    if not 0 < maximum_width_ratio <= 1:
        raise ValueError("maximum_width_ratio must be within 0..1")
    max_width = int(container.width * maximum_width_ratio)
    desired = min(
        max_width,
        max(text_shape.width, int((len(text_shape.text) * 12 * 0.72 + 12) * 12700)),
    )
    text_shape.width = desired
    text_shape.left = int(container.left + container.width - desired - container.width * 0.06)
    text_shape.height = max(text_shape.height, int(18 * 12700))
    for paragraph in text_shape.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.RIGHT
    presentation.save(path)
    return {"text_shape_name": text_shape_name, "width": int(text_shape.width)}


def clear_text_shape(
    pptx_path: str | Path,
    *,
    slide_index: int,
    shape_name: str,
    decoration_name: str,
) -> dict:
    """Remove reviewed sample copy and mark the now-empty frame as decoration."""
    if not decoration_name.startswith("decoration:cleared-text:"):
        raise ValueError("decoration_name must begin with decoration:cleared-text:")
    if slide_index < 1:
        raise ValueError("slide indices are 1-based")
    from pptx import Presentation

    path = Path(pptx_path)
    presentation = Presentation(path)
    if slide_index > len(presentation.slides):
        raise ValueError(f"Destination slide does not exist: {slide_index}")
    matches = [
        shape for shape in _iter_pptx_shapes(presentation.slides[slide_index - 1].shapes)
        if getattr(shape, "has_text_frame", False) and shape.name == shape_name
    ]
    if not matches:
        raise ValueError(f"No text frame named {shape_name!r} found on slide")
    if len(matches) > 1:
        raise ValueError(f"Multiple text frames named {shape_name!r} found on slide")
    shape = matches[0]
    shape.text_frame.clear()
    shape.name = decoration_name
    presentation.save(path)
    return {"decoration_name": decoration_name, "slide_index": slide_index}


def mark_native_shapes_as_decorations(
    pptx_path: str | Path,
    *,
    slide_index: int,
    shape_names: list[str],
    decoration_prefix: str,
) -> dict:
    """Give reviewed, non-content native shapes explicit visual-layer names."""
    if slide_index < 1:
        raise ValueError("slide indices are 1-based")
    if not decoration_prefix.startswith("decoration:component:"):
        raise ValueError("decoration_prefix must begin with decoration:component:")
    if any(not isinstance(name, str) or not name for name in shape_names):
        raise ValueError("shape_names must contain non-empty strings")
    if len(set(shape_names)) != len(shape_names):
        raise ValueError("shape_names must be distinct")
    from pptx import Presentation

    path = Path(pptx_path)
    presentation = Presentation(path)
    if slide_index > len(presentation.slides):
        raise ValueError(f"Destination slide does not exist: {slide_index}")
    all_shapes = list(_iter_pptx_shapes(presentation.slides[slide_index - 1].shapes))
    renamed: dict[str, str] = {}
    for index, source_name in enumerate(shape_names):
        matches = [shape for shape in all_shapes if shape.name == source_name]
        if not matches:
            raise ValueError(f"No native decoration shape named {source_name!r} found on slide")
        if len(matches) > 1:
            raise ValueError(f"Multiple native decoration shapes named {source_name!r} found on slide")
        shape = matches[0]
        if getattr(shape, "has_chart", False) or getattr(shape, "has_table", False):
            raise ValueError("native decoration shapes may not contain charts or tables")
        if getattr(shape, "has_text_frame", False) and str(shape.text or "").strip():
            raise ValueError("native decoration shapes may not contain business text")
        decoration_name = f"{decoration_prefix}:{index}"
        shape.name = decoration_name
        renamed[source_name] = decoration_name
    presentation.save(path)
    return {"slide_index": slide_index, "shape_names": renamed}


def _top_level_shapes_by_name(slide, names: list[str]) -> list:
    """Resolve an explicit component shell without guessing from its wording.

    A strict plan has to name its template primitives.  We deliberately do not
    scrape shapes by visual proximity or placeholder text: that would make a
    template's sample content part of the execution contract.
    """
    if not names or any(not isinstance(name, str) or not name for name in names):
        raise ValueError("component shape names must be a non-empty list of strings")
    by_name = {shape.name: shape for shape in slide.shapes}
    missing = [name for name in names if name not in by_name]
    if missing:
        raise ValueError(f"No top-level template component shape named {missing[0]!r} found on slide")
    if len(set(names)) != len(names):
        raise ValueError("component shape names must be distinct")
    return [by_name[name] for name in names]


def clone_native_shapes(
    pptx_path: str | Path,
    *,
    source_slide_index: int,
    destination_slide_index: int,
    shape_names: list[str],
) -> dict:
    """Copy selected editable template shapes to another slide in the same deck.

    Strict mode starts from a byte copy of the uploaded template, so the source
    and destination slides share one OPC package.  That lets native AutoShapes,
    text boxes and relationship-backed assets such as icons/pictures be moved
    without flattening them or copying the whole source page.
    """
    from pptx import Presentation

    path = Path(pptx_path)
    presentation = Presentation(path)
    if source_slide_index < 1 or source_slide_index > len(presentation.slides):
        raise ValueError(f"Source slide does not exist: {source_slide_index}")
    if destination_slide_index < 1 or destination_slide_index > len(presentation.slides):
        raise ValueError(f"Destination slide does not exist: {destination_slide_index}")
    source_slide = presentation.slides[source_slide_index - 1]
    destination_slide = presentation.slides[destination_slide_index - 1]
    prototypes = _top_level_shapes_by_name(source_slide, shape_names)

    existing_names = {shape.name for shape in destination_slide.shapes}
    existing_ids = {int(shape.shape_id) for shape in destination_slide.shapes}
    next_id = max(existing_ids, default=1) + 1
    name_map: dict[str, str] = {}

    for prototype in prototypes:
        cloned_element = deepcopy(prototype._element)

        # Rebind every relationship referenced by the copied XML.  This covers
        # image/icon embeds and hyperlinks while reusing the template package's
        # original binary part rather than flattening it.
        for element in cloned_element.iter():
            for attribute, relationship_id in list(element.attrib.items()):
                if not attribute.startswith(f"{{{REL_NS}}}"):
                    continue
                try:
                    relationship = source_slide.part.rels[relationship_id]
                except KeyError as exc:
                    raise ValueError(
                        f"Template shape {prototype.name!r} has a missing relationship {relationship_id!r}"
                    ) from exc
                if relationship.is_external:
                    resolved_id = destination_slide.part.relate_to(
                        relationship.target_ref,
                        relationship.reltype,
                        is_external=True,
                    )
                else:
                    resolved_id = destination_slide.part.relate_to(
                        relationship.target_part,
                        relationship.reltype,
                    )
                element.set(attribute, resolved_id)

        requested_name = prototype.name
        resolved_name = requested_name
        suffix = 2
        while resolved_name in existing_names:
            resolved_name = f"{requested_name}-componentcopy-{suffix}"
            suffix += 1
        existing_names.add(resolved_name)
        non_visual_properties = list(cloned_element.iter(_q(PRESENTATION_NS, "cNvPr")))
        for nested_index, properties in enumerate(non_visual_properties):
            while next_id in existing_ids:
                next_id += 1
            properties.set("id", str(next_id))
            existing_ids.add(next_id)
            next_id += 1
            if nested_index == 0:
                properties.set("name", resolved_name)
            else:
                nested_name = properties.get("name", "component-part")
                properties.set("name", f"{nested_name}-componentcopy-{next_id}")

        destination_slide.shapes._spTree.insert_element_before(cloned_element, "p:extLst")
        name_map[requested_name] = resolved_name

    presentation.save(path)
    return {
        "source_slide_index": source_slide_index,
        "destination_slide_index": destination_slide_index,
        "shape_names": name_map,
    }


def clone_native_shape_trees(
    pptx_path: str | Path,
    *,
    source_slide_index: int,
    destination_slide_index: int,
    shape_names: list[str],
) -> dict:
    """Clone the minimal top-level trees containing reviewed native shapes.

    PowerPoint stores charts and text inside grouped metric cards in the
    group's child coordinate space.  Flattening those descendants loses the
    parent transform, while reusing their chart relationship mutates the
    template's original workbook.  This primitive therefore copies each
    selected descendant's top-level ancestor once, duplicates every nested
    chart relationship closure, and returns a source-to-clone name map for
    later binding.
    """
    if source_slide_index < 1 or destination_slide_index < 1:
        raise ValueError("slide indices are 1-based")
    if source_slide_index == destination_slide_index:
        raise ValueError("native shape tree cloning requires distinct source and destination slides")
    if not shape_names or any(not isinstance(name, str) or not name for name in shape_names):
        raise ValueError("shape_names must be a non-empty list of strings")
    if len(set(shape_names)) != len(shape_names):
        raise ValueError("shape_names must be distinct")

    path = Path(pptx_path)
    with zipfile.ZipFile(path) as archive:
        source_parts = {item.filename: archive.read(item.filename) for item in archive.infolist()}
    destination_parts = dict(source_parts)
    source_slide_part = _slide_part(source_slide_index)
    destination_slide_part = _slide_part(destination_slide_index)
    if source_slide_part not in source_parts:
        raise ValueError(f"Source slide does not exist: {source_slide_index}")
    if destination_slide_part not in destination_parts:
        raise ValueError(f"Destination slide does not exist: {destination_slide_index}")

    source_slide = ET.fromstring(source_parts[source_slide_part])
    destination_slide = ET.fromstring(destination_parts[destination_slide_part])
    source_tree = source_slide.find(f".//{_q(PRESENTATION_NS, 'spTree')}")
    destination_tree = destination_slide.find(f".//{_q(PRESENTATION_NS, 'spTree')}")
    if source_tree is None or destination_tree is None:
        raise ValueError("Source and destination slides require shape trees")

    by_name: dict[str, ET.Element] = {}
    top_level_names: dict[int, str] = {}
    top_level_elements: list[ET.Element] = []
    for element in list(source_tree):
        properties = list(element.iter(_q(PRESENTATION_NS, "cNvPr")))
        if not properties:
            continue
        top_level_elements.append(element)
        top_name = properties[0].get("name", "template-object")
        top_level_names[id(element)] = top_name
        for item in properties:
            name = item.get("name", "")
            if not name:
                continue
            if name in by_name:
                raise ValueError(f"Multiple native shapes named {name!r} found on source slide")
            by_name[name] = element
    missing = [name for name in shape_names if name not in by_name]
    if missing:
        raise ValueError(f"No template component shape named {missing[0]!r} found on slide")
    selected_ids = {id(by_name[name]) for name in shape_names}
    selected = [element for element in top_level_elements if id(element) in selected_ids]

    source_rels_part = _rels_name(source_slide_part)
    destination_rels_part = _rels_name(destination_slide_part)
    if source_rels_part not in source_parts or destination_rels_part not in destination_parts:
        raise ValueError("Source and destination slides require relationship parts")
    source_relationships = ET.fromstring(source_parts[source_rels_part])
    destination_relationships = ET.fromstring(destination_parts[destination_rels_part])
    source_relationship_by_id = {
        item.get("Id", ""): item
        for item in source_relationships.findall(_q(PACKAGE_REL_NS, "Relationship"))
    }
    source_types = ET.fromstring(source_parts["[Content_Types].xml"])
    destination_types = ET.fromstring(destination_parts["[Content_Types].xml"])
    part_map: dict[str, str] = {}
    copied_parts: list[str] = []
    relationship_map: dict[str, str] = {}

    existing_properties = list(destination_slide.iter(_q(PRESENTATION_NS, "cNvPr")))
    existing_ids = {
        int(item.get("id", "0"))
        for item in existing_properties
        if item.get("id", "").isdigit()
    }
    existing_names = {item.get("name", "") for item in existing_properties}
    next_id = max(existing_ids, default=1) + 1
    name_map: dict[str, str] = {}
    cloned_top_level_names: list[str] = []

    for source_element in selected:
        cloned = deepcopy(source_element)
        for item in cloned.iter():
            for attribute, source_relationship_id in list(item.attrib.items()):
                if not attribute.startswith(f"{{{REL_NS}}}"):
                    continue
                destination_relationship_id = relationship_map.get(source_relationship_id)
                if destination_relationship_id is None:
                    relationship = source_relationship_by_id.get(source_relationship_id)
                    if relationship is None:
                        raise ValueError(
                            f"Template shape relationship {source_relationship_id!r} is missing"
                        )
                    relationship_type = relationship.get("Type", "")
                    target = relationship.get("Target", "")
                    if not target:
                        raise ValueError(
                            f"Template shape relationship {source_relationship_id!r} has no target"
                        )
                    attributes = {
                        "Id": _next_relationship_id(destination_relationships),
                        "Type": relationship_type,
                    }
                    if relationship.get("TargetMode") == "External":
                        attributes["Target"] = target
                        attributes["TargetMode"] = "External"
                    else:
                        source_target = _resolve_target(source_slide_part, target)
                        destination_target = source_target
                        if relationship_type.endswith("/chart"):
                            destination_target = _copy_closure(
                                source_parts,
                                destination_parts,
                                source_types,
                                destination_types,
                                source_target,
                                part_map,
                                copied_parts,
                            )
                        elif source_target not in destination_parts:
                            raise ValueError(
                                f"Template relationship target is missing: {source_target}"
                            )
                        attributes["Target"] = _relative_target(
                            destination_slide_part, destination_target,
                        )
                    ET.SubElement(
                        destination_relationships,
                        _q(PACKAGE_REL_NS, "Relationship"),
                        attributes,
                    )
                    destination_relationship_id = attributes["Id"]
                    relationship_map[source_relationship_id] = destination_relationship_id
                item.set(attribute, destination_relationship_id)

        for index, properties in enumerate(cloned.iter(_q(PRESENTATION_NS, "cNvPr"))):
            while next_id in existing_ids:
                next_id += 1
            properties.set("id", str(next_id))
            existing_ids.add(next_id)
            next_id += 1
            source_name = properties.get("name", "template-object")
            resolved_name = source_name
            suffix = 2
            while resolved_name in existing_names:
                resolved_name = f"{source_name}-componentcopy-{suffix}"
                suffix += 1
            properties.set("name", resolved_name)
            existing_names.add(resolved_name)
            name_map[source_name] = resolved_name
            if index == 0:
                cloned_top_level_names.append(resolved_name)
        destination_tree.insert(len(destination_tree), cloned)

    destination_parts[destination_slide_part] = ET.tostring(
        destination_slide, encoding="utf-8", xml_declaration=True,
    )
    destination_parts[destination_rels_part] = ET.tostring(
        destination_relationships, encoding="utf-8", xml_declaration=True,
    )
    destination_parts["[Content_Types].xml"] = ET.tostring(
        destination_types, encoding="utf-8", xml_declaration=True,
    )
    _write_package(path, destination_parts)
    return {
        "source_slide_index": source_slide_index,
        "destination_slide_index": destination_slide_index,
        "shape_names": {name: name_map[name] for name in shape_names},
        "top_level_shape_names": cloned_top_level_names,
        "source_top_level_shape_names": [top_level_names[id(element)] for element in selected],
        "copied_parts": copied_parts,
    }


def place_native_shapes(
    pptx_path: str | Path,
    *,
    slide_index: int,
    shape_names: list[str],
    placement: dict,
) -> dict:
    """Fit an explicitly declared native shape group into a slide-relative box."""
    if slide_index < 1:
        raise ValueError("slide indices are 1-based")
    from pptx import Presentation

    path = Path(pptx_path)
    presentation = Presentation(path)
    if slide_index > len(presentation.slides):
        raise ValueError(f"Destination slide does not exist: {slide_index}")
    slide = presentation.slides[slide_index - 1]
    shapes = _top_level_shapes_by_name(slide, shape_names)
    result = _place_component_shapes(
        shapes,
        slide_width=presentation.slide_width,
        slide_height=presentation.slide_height,
        placement=placement,
    )
    presentation.save(path)
    return result


def _clone_native_shape(slide, prototype, name: str):
    """Duplicate a template shape, retaining its native fill, line and effects."""
    cloned_element = deepcopy(prototype._element)
    slide.shapes._spTree.append(cloned_element)  # python-pptx has no public clone API.
    cloned = slide.shapes._shape_factory(cloned_element)
    cloned.name = name
    return cloned


def _remove_shape(shape) -> None:
    parent = shape._element.getparent()
    if parent is None:
        raise ValueError("Template component shape has no parent")
    parent.remove(shape._element)


def _component_bounds(shapes: list) -> tuple[int, int, int, int]:
    left = min(shape.left for shape in shapes)
    top = min(shape.top for shape in shapes)
    right = max(shape.left + shape.width for shape in shapes)
    bottom = max(shape.top + shape.height for shape in shapes)
    return left, top, right - left, bottom - top


def _component_elements(elements: list[dict]) -> list[dict]:
    if not isinstance(elements, list) or not elements:
        raise ValueError("component elements must be a non-empty list")
    prepared: list[dict] = []
    bindings: set[str] = set()
    for index, item in enumerate(elements):
        if not isinstance(item, dict):
            raise ValueError(f"component element {index} must be an object")
        text = item.get("text")
        binding = item.get("binding_name")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"component element {index} requires non-empty text")
        if not isinstance(binding, str) or not binding.startswith("bind:"):
            raise ValueError(f"component element {index} requires a bind:* binding_name")
        if binding in bindings:
            raise ValueError("component element binding names must be distinct")
        bindings.add(binding)
        value = item.get("value")
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0):
            raise ValueError(f"component element {index} value must be a non-negative number")
        prepared.append({"text": text, "binding_name": binding, "value": value})
    return prepared


def _expanded_component_shapes(slide, prototypes: list, count: int, *, kind: str) -> list:
    """Use template nodes first, then clone their final native prototype.

    This is the core difference from page-level fill: a component's capacity is
    not frozen by however many sample nodes happened to be in the source deck.
    """
    active = prototypes[:count]
    if count > len(prototypes):
        prototype = prototypes[-1]
        active.extend(
            _clone_native_shape(slide, prototype, f"decoration:component:{kind}:prototype:{index}")
            for index in range(len(prototypes), count)
        )
    for shape in prototypes[count:]:
        _remove_shape(shape)
    return active


def _expanded_component_groups(slide, prototype_groups: list[list], count: int, *, kind: str) -> list[list]:
    """Expand/remove logical levels while retaining every native part per level."""
    active = prototype_groups[:count]
    if count > len(prototype_groups):
        final_group = prototype_groups[-1]
        for index in range(len(prototype_groups), count):
            active.append([
                _clone_native_shape(slide, prototype, f"decoration:component:{kind}:prototype:{index}:part:{part}")
                for part, prototype in enumerate(final_group)
            ])
    for group in prototype_groups[count:]:
        for shape in group:
            _remove_shape(shape)
    return active


def _shape_geometry(shape) -> tuple[int, int, int, int]:
    return shape.left, shape.top, shape.width, shape.height


def _reflow_component_part(part, prototype_part_geometry, prototype_primary_geometry, target_primary) -> None:
    """Preserve a companion object's relative geometry to its level body."""
    prototype_left, prototype_top, prototype_width, prototype_height = prototype_part_geometry
    primary_left, primary_top, primary_width, primary_height = prototype_primary_geometry
    primary_width = max(primary_width, 1)
    primary_height = max(primary_height, 1)
    part.left = int(target_primary.left + (prototype_left - primary_left) / primary_width * target_primary.width)
    part.top = int(target_primary.top + (prototype_top - primary_top) / primary_height * target_primary.height)
    part.width = max(int(prototype_width / primary_width * target_primary.width), 1)
    part.height = max(int(prototype_height / primary_height * target_primary.height), 1)


def _reflow_card_grid(
    segments: list,
    *,
    left: int,
    top: int,
    width: int,
    height: int,
    minimum_height_ratio: float = 0.0,
) -> None:
    """Arrange editable cards in balanced rows while preserving their native aspect."""
    count = len(segments)
    columns = count if count <= 3 else 2 if count == 4 else 3
    rows = (count + columns - 1) // columns
    gap_x = max(int(width * 0.035), 1)
    gap_y = max(int(height * 0.08), 1)
    card_width = max(int((width - gap_x * (columns - 1)) / columns), 1)
    prototype_aspect = sum(
        max(segment.width, 1) / max(segment.height, 1) for segment in segments
    ) / count
    available_row_height = max(int((height - gap_y * (rows - 1)) / rows), 1)
    natural_height = int(card_width / max(prototype_aspect, 0.1))
    minimum_height = int(card_width * minimum_height_ratio)
    card_height = max(min(max(natural_height, minimum_height), available_row_height), 1)
    grid_height = rows * card_height + (rows - 1) * gap_y
    grid_top = int(top + (height - grid_height) / 2)

    for row in range(rows):
        row_start = row * columns
        row_count = min(columns, count - row_start)
        row_width = row_count * card_width + (row_count - 1) * gap_x
        row_left = int(left + (width - row_width) / 2)
        for column in range(row_count):
            segment = segments[row_start + column]
            segment.left = int(row_left + column * (card_width + gap_x))
            segment.top = int(grid_top + row * (card_height + gap_y))
            segment.width = card_width
            segment.height = card_height


def _reflow_card_grid_backgrounds(backgrounds: list, segments: list, *, left: int, width: int) -> None:
    row_tops = sorted({segment.top for segment in segments})
    for background, row_top in zip(backgrounds, row_tops):
        row_segments = [segment for segment in segments if segment.top == row_top]
        row_bottom = max(segment.top + segment.height for segment in row_segments)
        card_height = row_bottom - row_top
        pad_top = max(int(card_height * 0.32), 1)
        pad_bottom = max(int(card_height * 0.16), 1)
        background.left = left
        background.top = row_top - pad_top
        background.width = width
        background.height = card_height + pad_top + pad_bottom


def _place_component_shapes(
    shapes: list,
    *,
    slide_width: int,
    slide_height: int,
    placement: dict,
) -> dict:
    if not isinstance(placement, dict):
        raise ValueError("component placement must be an object")
    resolved: dict[str, float] = {}
    for key in ("x", "y", "w", "h"):
        value = placement.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"component placement {key} must be a number")
        resolved[key] = float(value)
    if resolved["x"] < 0 or resolved["y"] < 0 or resolved["w"] <= 0 or resolved["h"] <= 0:
        raise ValueError("component placement must have non-negative origin and positive size")
    if resolved["x"] + resolved["w"] > 1 or resolved["y"] + resolved["h"] > 1:
        raise ValueError("component placement must remain inside the slide")
    fit_mode = placement.get("fit_mode", "contain")
    if fit_mode not in {"contain", "stretch"}:
        raise ValueError("component placement fit_mode must be 'contain' or 'stretch'")

    left, top, width, height = _component_bounds(shapes)
    target_left = int(resolved["x"] * slide_width)
    target_top = int(resolved["y"] * slide_height)
    target_width = int(resolved["w"] * slide_width)
    target_height = int(resolved["h"] * slide_height)
    if fit_mode == "stretch":
        scale_x = target_width / max(width, 1)
        scale_y = target_height / max(height, 1)
        for shape in shapes:
            shape.left = int(target_left + (shape.left - left) * scale_x)
            shape.top = int(target_top + (shape.top - top) * scale_y)
            shape.width = max(int(shape.width * scale_x), 1)
            shape.height = max(int(shape.height * scale_y), 1)
        return {
            **resolved,
            "fit_mode": fit_mode,
            "scale_x": round(scale_x, 6),
            "scale_y": round(scale_y, 6),
            "fitted_bounds": {
                "left": target_left,
                "top": target_top,
                "width": target_width,
                "height": target_height,
            },
        }
    scale = min(target_width / max(width, 1), target_height / max(height, 1))
    placed_width = max(int(width * scale), 1)
    placed_height = max(int(height * scale), 1)
    offset_left = target_left + int((target_width - placed_width) / 2)
    offset_top = target_top + int((target_height - placed_height) / 2)
    for shape in shapes:
        shape.left = int(offset_left + (shape.left - left) * scale)
        shape.top = int(offset_top + (shape.top - top) * scale)
        shape.width = max(int(shape.width * scale), 1)
        shape.height = max(int(shape.height * scale), 1)
    return {
        **resolved,
        "fit_mode": fit_mode,
        "scale": round(scale, 6),
        "fitted_bounds": {
            "left": offset_left,
            "top": offset_top,
            "width": placed_width,
            "height": placed_height,
        },
    }


def _fit_component_label(label, text: str, *, force_white: bool = True) -> None:
    """Keep component labels readable as their native container reflows.

    Unlike a page title, a component label is allowed to wrap within its own
    declared geometry: its sibling segment grows or shrinks with the data and
    the text responds only inside that resulting component.  The conservative
    8--14pt range avoids an unreadable tiny fallback while preserving the
    template's text-frame styling, alignment, fills and effects.
    """
    from pptx.dml.color import RGBColor
    from pptx.enum.text import MSO_AUTO_SIZE
    from pptx.util import Pt

    frame = label.text_frame
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.NONE
    # EMU -> pt: 914400 / 72 = 12700. Estimate CJK/Latin labels alike by
    # character count; presentation rendering will still use the template font.
    width_pt = max(label.width / 12700, 1)
    height_pt = max(label.height / 12700, 1)
    usable_lines = max(1, int(height_pt / (8 * 1.25)))
    fitted_size = int(width_pt * usable_lines / max(len(text) * 0.95, 1))
    font_size = min(14, max(8, fitted_size))
    for paragraph in frame.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(font_size)
            # The template's sample labels are theme-coloured for a dark
            # side-tab.  Once a label is reflowed into a coloured segment,
            # force the same high-contrast white used by its native funnel.
            if force_white:
                run.font.color.rgb = RGBColor(255, 255, 255)


def _extended_component_elements(elements: list[dict], fields: set[str]) -> list[dict]:
    if not isinstance(elements, list) or not elements:
        raise ValueError("component elements must be a non-empty list")
    prepared: list[dict] = []
    bindings: set[str] = set()
    for index, item in enumerate(elements):
        if not isinstance(item, dict):
            raise ValueError(f"component element {index} must be an object")
        value = item.get("value")
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0
        ):
            raise ValueError(f"component element {index} value must be a non-negative number")
        labels = item.get("labels")
        if not isinstance(labels, dict) or set(labels) != fields:
            raise ValueError(
                f"component element {index} labels must exactly match {sorted(fields)!r}"
            )
        prepared_labels: dict[str, dict] = {}
        for field in sorted(fields):
            label = labels[field]
            if not isinstance(label, dict):
                raise ValueError(f"component element {index} label {field!r} must be an object")
            text = label.get("text")
            binding = label.get("binding_name")
            if not isinstance(text, str) or not text.strip():
                raise ValueError(
                    f"component element {index} label {field!r} requires non-empty text"
                )
            if not isinstance(binding, str) or not binding.startswith("bind:"):
                raise ValueError(
                    f"component element {index} label {field!r} requires a bind:* binding_name"
                )
            if binding in bindings:
                raise ValueError("component element binding names must be distinct")
            bindings.add(binding)
            prepared_labels[field] = {"text": text, "binding_name": binding}
        prepared.append({"value": value, "labels": prepared_labels})
    return prepared


def _write_component_label(label, *, text: str, binding_name: str) -> None:
    label.name = binding_name
    frame = label.text_frame
    paragraph = frame.paragraphs[0]
    if paragraph.runs:
        paragraph.runs[0].text = text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run().text = text
    for extra in frame.paragraphs[1:]:
        for run in extra.runs:
            run.text = ""


def _bind_extended_template_component(
    presentation,
    slide,
    *,
    component_type: str,
    layout_mode: str,
    item_groups: list[dict],
    shared_names: list[str],
    elements: list[dict],
    placement: dict | None,
    component_instance_id: str | None,
) -> dict:
    if not isinstance(item_groups, list) or not item_groups:
        raise ValueError("extended component item_groups must be a non-empty list")
    prototype_fields: set[str] | None = None
    segment_prototype_groups: list[list] = []
    label_prototype_groups: dict[str, list[list]] = {}
    for index, item_group in enumerate(item_groups):
        if not isinstance(item_group, dict):
            raise ValueError(f"extended component item group {index} must be an object")
        segment_names = item_group.get("segment_names")
        label_fields = item_group.get("label_fields")
        if not isinstance(segment_names, list) or not segment_names:
            raise ValueError(f"extended component item group {index} requires segment_names")
        if not isinstance(label_fields, dict) or not label_fields:
            raise ValueError(f"extended component item group {index} requires label_fields")
        fields = set(label_fields)
        if prototype_fields is None:
            prototype_fields = fields
            label_prototype_groups = {field: [] for field in fields}
        elif fields != prototype_fields:
            raise ValueError("extended component label fields must align across item groups")
        segment_prototype_groups.append(_top_level_shapes_by_name(slide, segment_names))
        for field, names in label_fields.items():
            if not isinstance(names, list) or len(names) != 1:
                raise ValueError(
                    f"extended component label field {field!r} requires exactly one shape per item"
                )
            label_prototype_groups[field].append(_top_level_shapes_by_name(slide, names))
    assert prototype_fields is not None
    prepared = _extended_component_elements(elements, prototype_fields)
    shared_prototypes = (
        _top_level_shapes_by_name(slide, shared_names)
        if shared_names else []
    )
    source_shared_count = len(shared_prototypes)

    segment_bounds = _component_bounds([
        shape for group in segment_prototype_groups for shape in group
    ])
    segment_geometry_templates = [
        [_shape_geometry(shape) for shape in group]
        for group in segment_prototype_groups
    ]
    label_geometry_templates = {
        field: [[_shape_geometry(shape) for shape in group] for group in groups]
        for field, groups in label_prototype_groups.items()
    }
    active_segments = _expanded_component_groups(
        slide, segment_prototype_groups, len(prepared), kind=component_type,
    )
    active_labels = {
        field: _expanded_component_groups(
            slide, groups, len(prepared), kind=f"{component_type}:{field}",
        )
        for field, groups in label_prototype_groups.items()
    }
    active_shared = shared_prototypes
    if layout_mode in {"card_grid", "icon_card_grid"} and shared_prototypes:
        columns = len(prepared) if len(prepared) <= 3 else 2 if len(prepared) == 4 else 3
        rows = (len(prepared) + columns - 1) // columns
        active_shared = _expanded_component_shapes(
            slide, shared_prototypes, rows, kind=f"{component_type}:row",
        )
    left, top, width, height = segment_bounds
    max_value = max((item["value"] or 0) for item in prepared)
    gap = max(int(height * 0.025), 1)
    component_prefix = f"decoration:component:{component_type}"
    if component_instance_id is not None:
        component_prefix = f"{component_prefix}:{component_instance_id}"

    for index, (segment_group, item) in enumerate(zip(active_segments, prepared)):
        segment = segment_group[0]
        if layout_mode in {
            "card_grid", "icon_card_grid", "fixed_cluster", "two_sided_contrast",
        }:
            pass
        elif layout_mode == "timeline":
            available_width = max(width - segment.width, 0)
            ratio = 0.5 if len(prepared) == 1 else index / (len(prepared) - 1)
            segment.left = int(left + available_width * ratio)
            segment.top = int(top + (height - segment.height) / 2)
        else:
            row_height = max(int((height - gap * (len(prepared) - 1)) / len(prepared)), 1)
            value_ratio = (item["value"] or 0) / max_value if max_value else None
            if value_ratio is None:
                value_ratio = (
                    (index + 1) / len(prepared)
                    if layout_mode == "pyramid"
                    else 1 - index / (len(prepared) + 1)
                )
            target_width = max(int(width * (0.22 + 0.78 * value_ratio)), 1)
            segment.width = target_width
            segment.height = row_height
            segment.left = int(left + (width - target_width) / 2)
            segment.top = int(top + index * (row_height + gap))

        if layout_mode in {"card_grid", "icon_card_grid"} and index == 0:
            card_segments = [group[0] for group in active_segments]
            layout_height = height
            if layout_mode == "icon_card_grid":
                columns = (
                    len(prepared)
                    if len(prepared) <= 3
                    else 2 if len(prepared) == 4 else 3
                )
                rows = (len(prepared) + columns - 1) // columns
                # Real icon-card templates commonly store all prototypes in one
                # compact source row. Give generated additional rows their own
                # vertical canvas before the final placement fit, otherwise the
                # cards are compressed into the original single-row height.
                layout_height = int(height * (rows + 0.35 * (rows - 1)))
                gap_x = max(int(width * 0.035), 1)
                card_width = max(
                    int((width - gap_x * (columns - 1)) / columns),
                    1,
                )
                minimum_card_height = int(card_width * 0.58)
                minimum_layout_height = int(
                    rows * minimum_card_height
                    / max(1 - 0.08 * (rows - 1), 0.1)
                )
                layout_height = max(layout_height, minimum_layout_height)
            _reflow_card_grid(
                card_segments,
                left=left,
                top=top,
                width=width,
                height=layout_height,
                minimum_height_ratio=0.58 if layout_mode == "icon_card_grid" else 0.0,
            )
            _reflow_card_grid_backgrounds(
                active_shared, card_segments, left=left, width=width,
            )

        template_index = min(index, len(segment_prototype_groups) - 1)
        prototype_geometry = segment_geometry_templates[template_index]
        segment.name = f"{component_prefix}:segment:{index}"
        for part_index, part in enumerate(segment_group[1:], start=1):
            _reflow_component_part(
                part, prototype_geometry[part_index], prototype_geometry[0], segment,
            )
            part.name = f"{component_prefix}:segment:{index}:part:{part_index}"

        for field in sorted(prototype_fields):
            label = active_labels[field][index][0]
            label_geometry = label_geometry_templates[field][template_index][0]
            _reflow_component_part(label, label_geometry, prototype_geometry[0], segment)
            if layout_mode == "two_sided_contrast" and field != "title":
                # The source slide stores the explanatory copy in separate
                # coloured bands outside the two reusable contrast wedges.
                # Once the wedges are extracted as a standalone component,
                # place that copy inside each native wedge so it remains
                # visible without importing the page-level bands.
                label.left = int(segment.left + segment.width * 0.08)
                label.width = max(int(segment.width * 0.84), 1)
                label.height = max(int(segment.height * 0.32), 1)
                label.top = int(
                    segment.top + segment.height * (0.62 if index % 2 == 0 else 0.08)
                )
            label_data = item["labels"][field]
            _write_component_label(
                label, text=label_data["text"], binding_name=label_data["binding_name"],
            )
            _fit_component_label(label, label_data["text"], force_white=False)

    for index, shared in enumerate(active_shared):
        shared.name = f"{component_prefix}:shared:{index}"

    all_shapes = (
        [shape for group in active_segments for shape in group]
        + [
            shape
            for field_groups in active_labels.values()
            for group in field_groups
            for shape in group
        ]
        + active_shared
    )
    placement_result = None
    if placement is not None:
        placement_result = _place_component_shapes(
            all_shapes,
            slide_width=presentation.slide_width,
            slide_height=presentation.slide_height,
            placement=placement,
        )
        for item_index, item in enumerate(prepared):
            for field in prototype_fields:
                label = active_labels[field][item_index][0]
                _fit_component_label(label, item["labels"][field]["text"], force_white=False)

    binding_names = [
        item["labels"][field]["binding_name"]
        for item in prepared
        for field in sorted(prototype_fields)
    ]
    return {
        "binding_schema_version": "2.0.0",
        "component_type": component_type,
        "component_instance_id": component_instance_id,
        "element_count": len(prepared),
        "binding_names": binding_names,
        "source_segment_count": len(segment_prototype_groups),
        "source_label_count": sum(len(groups) for groups in label_prototype_groups.values()),
        "source_shared_count": source_shared_count,
        "bounds": {"left": left, "top": top, "width": width, "height": height},
        "placement": placement_result,
    }


def bind_template_component(
    pptx_path: str | Path,
    *,
    slide_index: int,
    component_type: str,
    segment_names: list[str] | None,
    label_names: list[str] | None,
    elements: list[dict],
    segment_groups: list[list[str]] | None = None,
    item_groups: list[dict] | None = None,
    shared_names: list[str] | None = None,
    placement: dict | None = None,
    component_instance_id: str | None = None,
    layout_mode: str | None = None,
) -> dict:
    """Reflow a declared native template component from semantic data.

    ``segment_names`` and ``label_names`` identify the original template shell;
    no whole slide is duplicated or blindly filled.  Existing nodes are reused
    first, additional nodes are OOXML clones of the template prototype, and
    excess sample nodes are removed so old example content cannot leak.

        Supported components intentionally cover five geometric families that
    expose the key contract: funnels scale width by value, pyramids scale level
    width by value (or semantic depth when values are absent), and timelines
    re-space nodes as their count changes. Card grids balance editable cards in
        centered rows. Icon card grids use the same balanced rows with a taller
        minimum card ratio so an overlapping native icon and detail copy remain
        readable. All labels retain native text frames and carry their individual
        source bindings.
    """
    effective_layout = layout_mode or component_type
    if effective_layout not in {
        "funnel", "pyramid", "timeline", "card_grid", "icon_card_grid", "fixed_cluster",
        "two_sided_contrast",
    }:
        raise ValueError(f"Unsupported template component renderer: {effective_layout!r}")
    if component_instance_id is not None and (
        not isinstance(component_instance_id, str)
        or not component_instance_id
        or ":" in component_instance_id
    ):
        raise ValueError("component_instance_id must be a non-empty colon-free string")
    if slide_index < 1:
        raise ValueError("slide indices are 1-based")
    from pptx import Presentation

    path = Path(pptx_path)
    presentation = Presentation(path)
    if slide_index > len(presentation.slides):
        raise ValueError(f"Destination slide does not exist: {slide_index}")
    slide = presentation.slides[slide_index - 1]
    if item_groups is not None:
        if segment_names is not None or segment_groups is not None or label_names is not None:
            raise ValueError(
                "extended item_groups cannot be combined with legacy segment or label arguments"
            )
        result = _bind_extended_template_component(
            presentation,
            slide,
            component_type=component_type,
            layout_mode=effective_layout,
            item_groups=item_groups,
            shared_names=shared_names or [],
            elements=elements,
            placement=placement,
            component_instance_id=component_instance_id,
        )
        presentation.save(path)
        return {"slide_index": slide_index, **result}
    if effective_layout in {"card_grid", "icon_card_grid"}:
        raise ValueError(f"{component_type} components require extended item_groups")
    if shared_names:
        raise ValueError("shared_names requires extended item_groups")
    prepared = _component_elements(elements)
    if segment_groups is not None:
        if segment_names is not None:
            raise ValueError("Provide either segment_names or segment_groups, not both")
        if not isinstance(segment_groups, list) or not segment_groups or any(
            not isinstance(group, list) or not group for group in segment_groups
        ):
            raise ValueError("segment_groups must be a non-empty list of non-empty declared shape-name lists")
        segment_prototype_groups = [
            _top_level_shapes_by_name(slide, group)
            for group in segment_groups
        ]
    else:
        if not isinstance(segment_names, list) or not segment_names:
            raise ValueError("segment_names must be a non-empty list when segment_groups is omitted")
        segment_prototype_groups = [[shape] for shape in _top_level_shapes_by_name(slide, segment_names)]
    if not isinstance(label_names, list) or not label_names:
        raise ValueError("label_names must be a non-empty list for legacy components")
    label_prototypes = _top_level_shapes_by_name(slide, label_names)
    if len(segment_prototype_groups) != len(label_prototypes):
        raise ValueError("component segment_names and label_names must have the same length")

    segment_bounds = _component_bounds([shape for group in segment_prototype_groups for shape in group])
    segment_geometry_templates = [
        [_shape_geometry(shape) for shape in group]
        for group in segment_prototype_groups
    ]
    label_bounds = _component_bounds(label_prototypes)
    segment_groups_active = _expanded_component_groups(
        slide, segment_prototype_groups, len(prepared), kind=component_type,
    )
    labels = _expanded_component_shapes(slide, label_prototypes, len(prepared), kind=component_type)
    left, top, width, height = segment_bounds
    label_left, _label_top, label_width, _label_height = label_bounds
    max_value = max((item["value"] or 0) for item in prepared)
    gap = max(int(height * 0.025), 1)

    for index, (segment_group, label, item) in enumerate(zip(segment_groups_active, labels, prepared)):
        segment = segment_group[0]
        if effective_layout == "timeline":
            available_width = max(width - segment.width, 0)
            ratio = 0.5 if len(prepared) == 1 else index / (len(prepared) - 1)
            segment.left = int(left + available_width * ratio)
            segment.top = int(top + (height - segment.height) / 2)
            label.width = max(int(width / len(prepared) * 0.9), 1)
            label.left = int(left + width * ratio - label.width / 2)
            label.top = int(segment.top + segment.height + max(int(height * 0.08), 1))
        else:
            row_height = max(int((height - gap * (len(prepared) - 1)) / len(prepared)), 1)
            value_ratio = (item["value"] or 0) / max_value if max_value else None
            if value_ratio is None:
                value_ratio = (index + 1) / len(prepared) if effective_layout == "pyramid" else 1 - index / (len(prepared) + 1)
            target_width = max(int(width * (0.22 + 0.78 * value_ratio)), 1)
            segment.width = target_width
            segment.height = row_height
            segment.left = int(left + (width - target_width) / 2)
            segment.top = int(top + index * (row_height + gap))
            # Do not retain a sample label's narrow box when the data segment
            # is wider.  The label remains contained by the native segment.
            label.width = max(int(target_width * 0.9), min(max(label_width, 1), target_width))
            label.left = int(segment.left + (target_width - label.width) / 2)
            label.height = max(int(row_height * 0.7), 1)
            label.top = int(segment.top + (row_height - label.height) / 2)

        prototype_group = segment_prototype_groups[min(index, len(segment_prototype_groups) - 1)]
        prototype_geometry = segment_geometry_templates[min(index, len(segment_geometry_templates) - 1)]
        component_prefix = f"decoration:component:{component_type}"
        if component_instance_id is not None:
            component_prefix = f"{component_prefix}:{component_instance_id}"
        segment.name = f"{component_prefix}:segment:{index}"
        for part_index, part in enumerate(segment_group[1:], start=1):
            _reflow_component_part(part, prototype_geometry[part_index], prototype_geometry[0], segment)
            part.name = f"{component_prefix}:segment:{index}:part:{part_index}"
        label.name = item["binding_name"]
        frame = label.text_frame
        paragraph = frame.paragraphs[0]
        if paragraph.runs:
            paragraph.runs[0].text = item["text"]
            for run in paragraph.runs[1:]:
                run.text = ""
        else:
            paragraph.add_run().text = item["text"]
        for extra in frame.paragraphs[1:]:
            for run in extra.runs:
                run.text = ""
        _fit_component_label(label, item["text"])

    placement_result = None
    if placement is not None:
        placement_result = _place_component_shapes(
            [shape for group in segment_groups_active for shape in group] + labels,
            slide_width=presentation.slide_width,
            slide_height=presentation.slide_height,
            placement=placement,
        )
        for label, item in zip(labels, prepared):
            _fit_component_label(label, item["text"])

    presentation.save(path)
    return {
        "component_type": component_type,
        "component_instance_id": component_instance_id,
        "slide_index": slide_index,
        "element_count": len(prepared),
        "binding_names": [item["binding_name"] for item in prepared],
        "source_segment_count": len(segment_prototype_groups),
        "source_label_count": len(label_prototypes),
        "bounds": {"left": left, "top": top, "width": width, "height": height},
        "placement": placement_result,
    }
