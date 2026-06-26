"""Lock-in tests for free-flow Bezier arrow rendering.

The free-flow renderer used straight ``<line>`` segments before, which led to
visual crossings on dense graphs. v2 switches to cubic Bezier curves that bend
along the dominant flow direction.
"""
import re

from business_blueprint.export_svg import _bezier_path_d, _render_arrow_line


def test_bezier_path_emits_cubic_bezier():
    d = _bezier_path_d(10, 20, 200, 80)
    # Cubic Bezier: M ... C c1x c1y, c2x c2y, x2 y2
    assert d.startswith("M 10 20 C ")
    assert d.endswith(" 200 80")
    assert " C " in d


def test_bezier_horizontal_bias_for_horizontal_flow():
    """When dx >> dy, control points should bend horizontally (same y as endpoints)."""
    d = _bezier_path_d(0, 100, 400, 110)
    # extract numbers after C
    m = re.search(r"C\s+([\d.]+)\s+([\d.]+),\s+([\d.]+)\s+([\d.]+),", d)
    assert m, f"expected control points in {d!r}"
    c1x, c1y, c2x, c2y = (float(g) for g in m.groups())
    # Control y should equal endpoint y (horizontal-bias)
    assert c1y == 100.0
    assert c2y == 110.0
    # Control x should be offset horizontally
    assert c1x > 0
    assert c2x < 400


def test_bezier_vertical_bias_for_vertical_flow():
    """When dy >> dx, control points should bend vertically."""
    d = _bezier_path_d(50, 0, 60, 400)
    m = re.search(r"C\s+([\d.]+)\s+([\d.]+),\s+([\d.]+)\s+([\d.]+),", d)
    assert m
    c1x, c1y, c2x, c2y = (float(g) for g in m.groups())
    # Control x should equal endpoint x (vertical-bias)
    assert c1x == 50.0
    assert c2x == 60.0
    # Control y offset
    assert c1y > 0
    assert c2y < 400


def test_render_arrow_line_uses_path_not_line():
    """Free-flow arrows must emit <path> with cubic Bezier, not <line>."""
    colors = {"arrow": "#10B981", "arrow_muted": "#9CA3AF"}
    result = _render_arrow_line(
        sx=0, sy=0, tx=200, ty=100,
        arrow={"relation_type": "supports"},
        colors=colors,
    )
    assert '<path d="M' in result
    assert " C " in result
    assert '<line ' not in result
    assert 'marker-end="url(#arrow-solid)"' in result


def test_render_arrow_line_dashed_for_depends():
    colors = {"arrow": "#10B981", "arrow_muted": "#9CA3AF"}
    result = _render_arrow_line(
        sx=0, sy=0, tx=200, ty=100,
        arrow={"relation_type": "depends-on"},
        colors=colors,
    )
    assert "stroke-dasharray=" in result
    assert '<path d="M' in result


def test_render_arrow_line_owned_by_yellow_dotted():
    colors = {"arrow": "#10B981", "arrow_muted": "#9CA3AF"}
    result = _render_arrow_line(
        sx=0, sy=0, tx=200, ty=0,
        arrow={"relation_type": "owned-by"},
        colors=colors,
    )
    assert '#FBBF24' in result
    assert 'stroke-dasharray="3,3"' in result
    assert 'marker-end="url(#arrow-dot)"' in result
