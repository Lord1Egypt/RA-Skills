"""Rendered-layout fingerprints for Template-route rhythm validation."""

from __future__ import annotations

from collections import Counter
from math import ceil
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat


GRID_COLUMNS = 16
GRID_ROWS = 9


def _distance(first: list[float], second: list[float]) -> float:
    return sum(abs(left - right) for left, right in zip(first, second)) / max(len(first), 1)


def _mirror(signature: list[float]) -> list[float]:
    rows = [
        signature[index:index + GRID_COLUMNS]
        for index in range(0, len(signature), GRID_COLUMNS)
    ]
    return [value for row in rows for value in reversed(row)]


def fingerprint_distance(first: list[float], second: list[float]) -> float:
    """Treat left/right mirrors as one visual skeleton."""
    return min(_distance(first, second), _distance(first, _mirror(second)))


def canonical_fingerprint(signature: list[float]) -> list[float]:
    """Give mirrored layouts one stable orientation before centroid updates."""
    mirrored = _mirror(signature)
    return list(min(tuple(signature), tuple(mirrored)))


def image_layout_fingerprint(path: str | Path) -> list[float]:
    image = Image.open(path).convert("RGB")
    image.thumbnail((480, 270))
    # Template decks intentionally repeat title bars, rules, footers and page
    # numbers.  They are brand rhythm, not the page's information skeleton.
    # Fingerprint the authored body so a line chart with bottom cards does not
    # collapse into the same cluster as a radar chart with a side narrative.
    width, height = image.size
    image = image.crop((0, round(height * 0.16), width, round(height * 0.91)))
    width, height = image.size
    corner = max(2, min(width, height) // 30)
    corners = [
        image.crop((0, 0, corner, corner)),
        image.crop((width - corner, 0, width, corner)),
        image.crop((0, height - corner, corner, height)),
        image.crop((width - corner, height - corner, width, height)),
    ]
    background = tuple(
        sum(ImageStat.Stat(item).mean[channel] for item in corners) / len(corners)
        for channel in range(3)
    )
    edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
    occupancy_signature: list[float] = []
    edge_signature: list[float] = []
    for row in range(GRID_ROWS):
        top = round(row * height / GRID_ROWS)
        bottom = round((row + 1) * height / GRID_ROWS)
        for column in range(GRID_COLUMNS):
            left = round(column * width / GRID_COLUMNS)
            right = round((column + 1) * width / GRID_COLUMNS)
            pixels = list(image.crop((left, top, right, bottom)).getdata())
            occupied = sum(
                sum((pixel[channel] - background[channel]) ** 2 for channel in range(3)) ** 0.5 > 34
                for pixel in pixels
            ) / max(len(pixels), 1)
            # Quantisation makes the signature insensitive to antialiasing and
            # renderer-specific one-pixel differences.
            occupancy_signature.append(round(occupied * 10) / 10)
            edge_mean = ImageStat.Stat(edges.crop((left, top, right, bottom))).mean[0] / 255
            edge_signature.append(round(edge_mean * 10) / 10)
    return [*occupancy_signature, *edge_signature]


def evaluate_rendered_layout_rhythm(
    render_report: dict,
    *,
    page_composition: dict | None = None,
    similarity_threshold: float = 0.055,
) -> dict:
    """Cluster real-rendered slides by geometry instead of declared names."""
    composition_pages = [
        page for page in (page_composition or {}).get("pages", [])
        if isinstance(page, dict)
    ]
    rendered = [
        slide for slide in render_report.get("slides", [])
        if isinstance(slide, dict) and isinstance(slide.get("image"), str)
    ]
    pages: list[dict] = []
    for index, slide in enumerate(rendered):
        composition = composition_pages[index] if index < len(composition_pages) else {}
        if composition.get("page_role", "body") != "body":
            continue
        path = Path(slide["image"])
        if not path.is_file():
            continue
        pages.append({
            "slide_index": slide.get("slide_index", index + 1),
            "slide_id": composition.get("slide_id", f"S{index + 1:02d}"),
            "series_context": composition.get("series_context"),
            "signature": canonical_fingerprint(image_layout_fingerprint(path)),
        })

    clusters: list[dict] = []
    for page in pages:
        match = next((
            cluster for cluster in clusters
            if fingerprint_distance(page["signature"], cluster["centroid"]) <= similarity_threshold
        ), None)
        if match is None:
            clusters.append({"cluster_id": len(clusters) + 1, "centroid": page["signature"], "pages": [page]})
        else:
            match["pages"].append(page)
            count = len(match["pages"])
            match["centroid"] = [
                ((value * (count - 1)) + new) / count
                for value, new in zip(match["centroid"], page["signature"])
            ]

    issues: list[dict] = []
    page_cluster: dict[int, int] = {}
    for cluster in clusters:
        for page in cluster["pages"]:
            page_cluster[int(page["slide_index"])] = cluster["cluster_id"]

    ordered = sorted(pages, key=lambda page: page["slide_index"])
    for start in range(max(0, len(ordered) - 2)):
        window = ordered[start:start + 3]
        cluster_ids = {page_cluster[int(page["slide_index"])] for page in window}
        if len(cluster_ids) != 1:
            continue
        series = [page.get("series_context") for page in window]
        explicit_comparison = all(
            isinstance(item, dict)
            and item.get("purpose") == "comparison"
            and item.get("shared_scale") is True
            and item.get("group_id") == series[0].get("group_id")
            for item in series
        )
        if not explicit_comparison:
            issues.append({
                "code": "TEMPLATE_RENDERED_LAYOUT_CONSECUTIVE_LIMIT",
                "cluster_id": next(iter(cluster_ids)),
                "slide_indices": [page["slide_index"] for page in window],
            })
            break

    body_count = len(pages)
    maximum_cluster_count = max(4, ceil(body_count * 0.25))
    if body_count >= 8:
        for cluster in clusters:
            if len(cluster["pages"]) <= maximum_cluster_count:
                continue
            series_groups = {
                page.get("series_context", {}).get("group_id")
                for page in cluster["pages"] if isinstance(page.get("series_context"), dict)
            }
            explicit_comparison = (
                len(series_groups) == 1 and None not in series_groups
                and all(
                    isinstance(page.get("series_context"), dict)
                    and page["series_context"].get("purpose") == "comparison"
                    and page["series_context"].get("shared_scale") is True
                    for page in cluster["pages"]
                )
            )
            if not explicit_comparison:
                issues.append({
                    "code": "TEMPLATE_RENDERED_LAYOUT_OVERUSED",
                    "cluster_id": cluster["cluster_id"],
                    "page_count": len(cluster["pages"]),
                    "body_page_count": body_count,
                    "maximum_cluster_count": maximum_cluster_count,
                    "slide_indices": [page["slide_index"] for page in cluster["pages"]],
                })

    cluster_sizes = Counter(page_cluster.values())
    return {
        "status": "pass" if not issues else "fail",
        "body_page_count": body_count,
        "unique_rendered_layout_count": len(clusters),
        "cluster_sizes": dict(sorted(cluster_sizes.items())),
        "clusters": [{
            "cluster_id": cluster["cluster_id"],
            "slide_indices": [page["slide_index"] for page in cluster["pages"]],
            "slide_ids": [page["slide_id"] for page in cluster["pages"]],
        } for cluster in clusters],
        "issues": issues,
    }
