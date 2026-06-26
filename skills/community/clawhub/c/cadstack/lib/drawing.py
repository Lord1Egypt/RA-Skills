"""2D Drawing generation for CAD models.

This module provides functionality for generating 2D technical drawings
from 3D CAD models, including orthographic projections, dimensions,
and exports to DXF, SVG, and PDF formats.

Architecture:
┌─────────────────────────────────────────────────────────────────┐
│                      Drawing Generator                           │
│  3D Model → Orthographic Views → Dimensions → Export            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      View Projections                            │
│  Top | Front | Right | Isometric | Section                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Export Formats                              │
│  DXF (AutoCAD) | SVG (Web) | PDF (Print)                        │
└─────────────────────────────────────────────────────────────────┘
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from pathlib import Path
import logging
import math

logger = logging.getLogger(__name__)


class ViewType(Enum):
    """Types of drawing views."""
    TOP = "top"
    FRONT = "front"
    RIGHT = "right"
    LEFT = "left"
    BACK = "back"
    BOTTOM = "bottom"
    ISOMETRIC = "isometric"
    SECTION = "section"


class DimensionType(Enum):
    """Types of dimensions."""
    LINEAR = "linear"
    ANGULAR = "angular"
    RADIAL = "radial"
    DIAMETER = "diameter"
    ORDINATE = "ordinate"


class ExportFormat(Enum):
    """Export formats for drawings."""
    DXF = "dxf"
    SVG = "svg"
    PDF = "pdf"


@dataclass
class Point2D:
    """2D point."""
    x: float
    y: float

    def __iter__(self):
        return iter((self.x, self.y))


@dataclass
class Dimension:
    """A dimension annotation on a drawing.

    Attributes:
        dimension_type: Type of dimension
        start: Start point
        end: End point
        value: Measured value
        text: Override text (e.g., for tolerances)
        offset: Offset from the dimension line
        unit: Unit string (e.g., "mm")
    """
    dimension_type: DimensionType
    start: Point2D
    end: Point2D
    value: float
    text: Optional[str] = None
    offset: float = 10.0
    unit: str = "mm"

    @property
    def text_value(self) -> str:
        """Get the dimension text."""
        if self.text:
            return self.text
        return f"{self.value:.2f} {self.unit}"


@dataclass
class ViewProjection:
    """A 2D projection view of a 3D model.

    Attributes:
        view_type: Type of view
        lines: List of line segments [(x1,y1,x2,y2), ...]
        arcs: List of arcs [(cx,cy,r,start,end), ...]
        dimensions: List of dimensions
        scale: View scale
        offset: View offset on sheet (x, y)
        label: View label (e.g., "A-A" for section)
    """
    view_type: ViewType
    lines: List[Tuple[float, float, float, float]] = field(default_factory=list)
    arcs: List[Tuple[float, float, float, float, float]] = field(default_factory=list)
    dimensions: List[Dimension] = field(default_factory=list)
    scale: float = 1.0
    offset: Tuple[float, float] = (0.0, 0.0)
    label: Optional[str] = None

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """Get bounding box (min_x, min_y, max_x, max_y)."""
        if not self.lines:
            return (0, 0, 0, 0)

        min_x = min(min(l[0], l[2]) for l in self.lines)
        max_x = max(max(l[0], l[2]) for l in self.lines)
        min_y = min(min(l[1], l[3]) for l in self.lines)
        max_y = max(max(l[1], l[3]) for l in self.lines)

        return (min_x, min_y, max_x, max_y)

    @property
    def width(self) -> float:
        """View width."""
        b = self.bounds
        return b[2] - b[0]

    @property
    def height(self) -> float:
        """View height."""
        b = self.bounds
        return b[3] - b[1]


@dataclass
class DrawingSheet:
    """A drawing sheet with multiple views.

    Attributes:
        title: Drawing title
        sheet_size: Sheet size (width, height) in mm
        views: List of views
        title_block: Title block information
        margin: Sheet margin
    """
    title: str
    sheet_size: Tuple[float, float] = (420.0, 297.0)  # A3 landscape
    views: List[ViewProjection] = field(default_factory=list)
    title_block: Dict[str, str] = field(default_factory=dict)
    margin: float = 20.0

    # Standard sheet sizes
    SIZES = {
        "A4": (210.0, 297.0),
        "A4_L": (297.0, 210.0),
        "A3": (297.0, 420.0),
        "A3_L": (420.0, 297.0),
        "A2": (420.0, 594.0),
        "A2_L": (594.0, 420.0),
        "A1": (594.0, 841.0),
        "A1_L": (841.0, 594.0),
        "A0": (841.0, 1189.0),
        "A0_L": (1189.0, 841.0),
    }

    @classmethod
    def standard_size(cls, size_name: str) -> Tuple[float, float]:
        """Get a standard sheet size."""
        return cls.SIZES.get(size_name.upper(), cls.SIZES["A3_L"])


class DrawingGenerator:
    """Generate 2D drawings from 3D models.

    Example:
        >>> from lib.drawing import DrawingGenerator, ViewType
        >>> gen = DrawingGenerator()
        >>> gen.set_model(my_3d_shape)
        >>> gen.add_view(ViewType.TOP)
        >>> gen.add_view(ViewType.FRONT)
        >>> gen.add_dimension(ViewType.TOP, (0, 0), (100, 0))
        >>> gen.export("drawing.dxf", ExportFormat.DXF)
    """

    def __init__(self):
        """Initialize the drawing generator."""
        self._model = None
        self._model_bounds: Tuple[float, float, float, float, float, float] = (0, 0, 0, 0, 0, 0)
        self._views: List[ViewProjection] = []
        self._title = "Untitled Drawing"
        self._sheet_size = DrawingSheet.standard_size("A3_L")
        self._title_block: Dict[str, str] = {}

    def set_model(self, model: Any, bounds: Optional[Tuple[float, float, float, float, float, float]] = None):
        """Set the 3D model to generate drawings from.

        Args:
            model: The 3D model (backend-specific)
            bounds: Optional bounding box (min_x, min_y, min_z, max_x, max_y, max_z)
        """
        self._model = model

        # Try to get bounds from model if not provided
        if bounds is None and hasattr(model, 'BoundBox'):
            bb = model.BoundBox
            self._model_bounds = (bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax)
        elif bounds:
            self._model_bounds = bounds
        else:
            self._model_bounds = (0, 0, 0, 100, 100, 100)  # Default

    def set_title(self, title: str):
        """Set the drawing title."""
        self._title = title

    def set_sheet_size(self, size: Tuple[float, float] | str):
        """Set the sheet size.

        Args:
            size: Either a (width, height) tuple or a standard size name like "A3_L"
        """
        if isinstance(size, str):
            self._sheet_size = DrawingSheet.standard_size(size)
        else:
            self._sheet_size = size

    def set_title_block(self, **fields):
        """Set title block fields.

        Common fields: title, part_number, material, scale, drawn_by, date, revision
        """
        self._title_block.update(fields)

    def add_view(
        self,
        view_type: ViewType,
        scale: float = 1.0,
        offset: Tuple[float, float] = (0.0, 0.0),
        label: Optional[str] = None
    ) -> ViewProjection:
        """Add a view to the drawing.

        Args:
            view_type: Type of view
            scale: View scale (1.0 = full size)
            offset: Offset position on sheet
            label: Optional view label

        Returns:
            The created ViewProjection
        """
        view = self._project_view(view_type, scale)
        view.offset = offset
        view.label = label
        self._views.append(view)
        return view

    def _project_view(self, view_type: ViewType, scale: float) -> ViewProjection:
        """Create a 2D projection from the 3D model.

        This is a simplified projection that extracts edges from bounding box.
        A full implementation would use the actual model geometry.

        Args:
            view_type: Type of view
            scale: Scale factor

        Returns:
            ViewProjection with projected geometry
        """
        view = ViewProjection(view_type=view_type, scale=scale)

        if not self._model:
            return view

        # Get bounds
        min_x, min_y, min_z, max_x, max_y, max_z = self._model_bounds
        w, h, d = max_x - min_x, max_y - min_y, max_z - min_z

        # Generate projection based on view type
        if view_type == ViewType.TOP:
            # XY plane (looking down Z)
            view.lines = [
                (0, 0, w * scale, 0),
                (w * scale, 0, w * scale, h * scale),
                (w * scale, h * scale, 0, h * scale),
                (0, h * scale, 0, 0),
            ]
            # Add depth dimension
            view.dimensions.append(Dimension(
                dimension_type=DimensionType.LINEAR,
                start=Point2D(0, 0),
                end=Point2D(w * scale, 0),
                value=w,
                offset=15.0
            ))
            view.dimensions.append(Dimension(
                dimension_type=DimensionType.LINEAR,
                start=Point2D(0, 0),
                end=Point2D(0, h * scale),
                value=h,
                offset=15.0
            ))

        elif view_type == ViewType.FRONT:
            # XZ plane (looking from Y)
            view.lines = [
                (0, 0, w * scale, 0),
                (w * scale, 0, w * scale, d * scale),
                (w * scale, d * scale, 0, d * scale),
                (0, d * scale, 0, 0),
            ]
            view.dimensions.append(Dimension(
                dimension_type=DimensionType.LINEAR,
                start=Point2D(0, 0),
                end=Point2D(w * scale, 0),
                value=w,
                offset=15.0
            ))
            view.dimensions.append(Dimension(
                dimension_type=DimensionType.LINEAR,
                start=Point2D(0, 0),
                end=Point2D(0, d * scale),
                value=d,
                offset=15.0
            ))

        elif view_type == ViewType.RIGHT:
            # YZ plane (looking from X)
            view.lines = [
                (0, 0, h * scale, 0),
                (h * scale, 0, h * scale, d * scale),
                (h * scale, d * scale, 0, d * scale),
                (0, d * scale, 0, 0),
            ]
            view.dimensions.append(Dimension(
                dimension_type=DimensionType.LINEAR,
                start=Point2D(0, 0),
                end=Point2D(h * scale, 0),
                value=h,
                offset=15.0
            ))
            view.dimensions.append(Dimension(
                dimension_type=DimensionType.LINEAR,
                start=Point2D(0, 0),
                end=Point2D(0, d * scale),
                value=d,
                offset=15.0
            ))

        elif view_type == ViewType.ISOMETRIC:
            # Isometric projection
            angle = math.radians(30)
            cos_a, sin_a = math.cos(angle), math.sin(angle)

            # Transform corners
            def iso(x, y, z):
                return (
                    (x - y) * cos_a * scale,
                    (x + y) * sin_a * scale - z * scale
                )

            # Box corners
            corners = [
                iso(0, 0, 0), iso(w, 0, 0), iso(w, h, 0), iso(0, h, 0),
                iso(0, 0, d), iso(w, 0, d), iso(w, h, d), iso(0, h, d)
            ]

            # Visible edges
            view.lines = [
                (*corners[0], *corners[1]),  # Front bottom
                (*corners[1], *corners[2]),  # Front right
                (*corners[2], *corners[3]),  # Front top (hidden)
                (*corners[3], *corners[0]),  # Front left
                (*corners[4], *corners[5]),  # Back bottom
                (*corners[5], *corners[6]),  # Back right
                (*corners[6], *corners[7]),  # Back top
                (*corners[7], *corners[4]),  # Back left
                (*corners[0], *corners[4]),  # Left vertical
                (*corners[1], *corners[5]),  # Right vertical
                (*corners[2], *corners[6]),  # Top vertical
                (*corners[3], *corners[7]),  # Top vertical
            ]

        return view

    def add_dimension(
        self,
        view_index: int,
        start: Tuple[float, float],
        end: Tuple[float, float],
        dimension_type: DimensionType = DimensionType.LINEAR,
        text: Optional[str] = None
    ):
        """Add a dimension to a view.

        Args:
            view_index: Index of the view
            start: Start point (x, y)
            end: End point (x, y)
            dimension_type: Type of dimension
            text: Override text
        """
        if 0 <= view_index < len(self._views):
            view = self._views[view_index]

            # Calculate value from distance
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            value = math.sqrt(dx * dx + dy * dy) / view.scale

            dimension = Dimension(
                dimension_type=dimension_type,
                start=Point2D(*start),
                end=Point2D(*end),
                value=value,
                text=text
            )
            view.dimensions.append(dimension)

    def layout_views(self, spacing: float = 30.0):
        """Automatically layout views on the sheet.

        Args:
            spacing: Spacing between views in mm
        """
        if not self._views:
            return

        sheet_w, sheet_h = self._sheet_size
        margin = 20.0

        # Calculate total width and max height
        total_width = sum(v.width + spacing for v in self._views) - spacing
        max_height = max(v.height for v in self._views)

        # Center vertically
        y_offset = (sheet_h - max_height) / 2

        # Layout horizontally
        x_offset = (sheet_w - total_width) / 2

        for view in self._views:
            view.offset = (x_offset, y_offset)
            x_offset += view.width + spacing

    def create_sheet(self) -> DrawingSheet:
        """Create a drawing sheet with all views.

        Returns:
            DrawingSheet instance
        """
        return DrawingSheet(
            title=self._title,
            sheet_size=self._sheet_size,
            views=list(self._views),
            title_block=dict(self._title_block)
        )

    def export(self, filepath: Path | str, format: ExportFormat) -> bool:
        """Export the drawing to a file.

        Args:
            filepath: Output file path
            format: Export format

        Returns:
            True if export succeeded
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        sheet = self.create_sheet()

        if format == ExportFormat.DXF:
            return self._export_dxf(filepath, sheet)
        elif format == ExportFormat.SVG:
            return self._export_svg(filepath, sheet)
        elif format == ExportFormat.PDF:
            return self._export_pdf(filepath, sheet)

        return False

    def _export_dxf(self, filepath: Path, sheet: DrawingSheet) -> bool:
        """Export to DXF format."""
        try:
            import ezdxf
        except ImportError:
            logger.warning("ezdxf not installed, cannot export DXF")
            return False

        doc = ezdxf.new()
        msp = doc.modelspace()

        # Add views
        for view in sheet.views:
            ox, oy = view.offset

            # Add lines
            for line in view.lines:
                msp.add_line(
                    (line[0] + ox, line[1] + oy),
                    (line[2] + ox, line[3] + oy)
                )

            # Add dimensions
            for dim in view.dimensions:
                msp.add_linear_dim(
                    base=(dim.start.x + ox, dim.start.y + oy + dim.offset),
                    p1=(dim.start.x + ox, dim.start.y + oy),
                    p2=(dim.end.x + ox, dim.end.y + oy),
                ).render()

        doc.saveas(str(filepath))
        logger.info(f"Exported DXF: {filepath}")
        return True

    def _export_svg(self, filepath: Path, sheet: DrawingSheet) -> bool:
        """Export to SVG format."""
        w, h = sheet.sheet_size

        svg_lines = [f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="white" stroke="black" stroke-width="1"/>
  <g id="drawing">
''']

        for view in sheet.views:
            ox, oy = view.offset
            view_id = view.view_type.value

            svg_lines.append(f'    <g id="{view_id}">\n')

            # Add lines
            for line in view.lines:
                svg_lines.append(
                    f'      <line x1="{line[0]+ox}" y1="{line[1]+oy}" '
                    f'x2="{line[2]+ox}" y2="{line[3]+oy}" '
                    f'stroke="black" stroke-width="0.5"/>\n'
                )

            # Add dimensions
            for dim in view.dimensions:
                # Dimension line
                mid_x = (dim.start.x + dim.end.x) / 2 + ox
                mid_y = (dim.start.y + dim.end.y) / 2 + oy + dim.offset

                svg_lines.append(
                    f'      <text x="{mid_x}" y="{mid_y}" '
                    f'font-size="8" text-anchor="middle">{dim.text_value}</text>\n'
                )

            svg_lines.append('    </g>\n')

        svg_lines.append('  </g>\n</svg>')

        filepath.write_text(''.join(svg_lines), encoding='utf-8')
        logger.info(f"Exported SVG: {filepath}")
        return True

    def _export_pdf(self, filepath: Path, sheet: DrawingSheet) -> bool:
        """Export to PDF format."""
        try:
            from reportlab.lib.pagesizes import mm
            from reportlab.pdfgen import canvas
        except ImportError:
            logger.warning("reportlab not installed, cannot export PDF")
            return False

        w, h = sheet.sheet_size
        c = canvas.Canvas(str(filepath), pagesize=(w * mm, h * mm))

        # Draw border
        c.rect(10 * mm, 10 * mm, (w - 20) * mm, (h - 20) * mm)

        # Draw views
        for view in sheet.views:
            ox, oy = view.offset

            # Draw lines
            for line in view.lines:
                c.line(
                    (line[0] + ox) * mm, (line[1] + oy) * mm,
                    (line[2] + ox) * mm, (line[3] + oy) * mm
                )

            # Draw dimensions
            for dim in view.dimensions:
                mid_x = (dim.start.x + dim.end.x) / 2 + ox
                mid_y = (dim.start.y + dim.end.y) / 2 + oy + dim.offset
                c.setFont("Helvetica", 8)
                c.drawCentredString(mid_x * mm, mid_y * mm, dim.text_value)

        c.save()
        logger.info(f"Exported PDF: {filepath}")
        return True


# =============================================================================
# Convenience Functions
# =============================================================================

def create_drawing(title: str = "Drawing") -> DrawingGenerator:
    """Create a new drawing generator.

    Args:
        title: Drawing title

    Returns:
        DrawingGenerator instance
    """
    gen = DrawingGenerator()
    gen.set_title(title)
    return gen


def quick_drawing(model: Any, views: List[ViewType] = None, output: Path | str = None,
                  format: ExportFormat = ExportFormat.SVG) -> DrawingGenerator:
    """Quickly generate a drawing with standard views.

    Args:
        model: 3D model
        views: List of view types (default: TOP, FRONT, RIGHT)
        output: Output file path
        format: Export format

    Returns:
        DrawingGenerator instance
    """
    if views is None:
        views = [ViewType.TOP, ViewType.FRONT, ViewType.RIGHT]

    gen = DrawingGenerator()
    gen.set_model(model)

    for view_type in views:
        gen.add_view(view_type)

    gen.layout_views()

    if output:
        gen.export(output, format)

    return gen
