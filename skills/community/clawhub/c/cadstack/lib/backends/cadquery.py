"""CadQuery backend implementation - Pure Python, no external CAD required."""

from pathlib import Path
from typing import List, Any, Optional, Dict
import logging

from .base import CADBackend, CADObject, CADDocument
from ..exceptions import ExportFailedError, EmptyDocumentError, FeatureOpError

try:
    import cadquery as cq
    CADQUERY_AVAILABLE = True
except ImportError:
    CADQUERY_AVAILABLE = False
    cq = None

logger = logging.getLogger(__name__)


class CadQueryBackend(CADBackend):
    """CadQuery backend - Pure Python, headless, no license required.

    This is the recommended backend for most use cases as it requires
    only a pip install and no external CAD software.
    """

    name = "cadquery"
    supports_headless = True
    supported_formats = ["step", "stl", "obj", "dxf", "svg"]

    def __init__(self):
        if not CADQUERY_AVAILABLE:
            from ..exceptions import BackendNotAvailableError
            raise BackendNotAvailableError("cadquery")
        super().__init__()
        self._workplane = None

    def check_available(self) -> bool:
        return CADQUERY_AVAILABLE

    def create_document(self, name: str = "Untitled") -> CADDocument:
        """Create a new document (workplane)."""
        logger.debug(f"Creating document: {name}")
        self._workplane = cq.Workplane("XY")
        doc = CADDocument(name=name, objects=[], backend_ref=self._workplane)
        self._current_doc = doc
        return doc

    def create_box(self, length: float, width: float, height: float,
                   name: str = "Box") -> CADObject:
        """Create a box primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating box '{name}': {length}x{width}x{height}mm")

        wp = cq.Workplane("XY").box(length, width, height)
        obj = CADObject(name=name, object_type="Box", backend_ref=wp)
        self._objects[name] = wp

        if self._current_doc:
            self._current_doc.objects.append(obj)

        return obj

    def create_cylinder(self, radius: float, height: float,
                        name: str = "Cylinder") -> CADObject:
        """Create a cylinder primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating cylinder '{name}': r={radius}mm, h={height}mm")

        wp = cq.Workplane("XY").circle(radius).extrude(height)
        obj = CADObject(name=name, object_type="Cylinder", backend_ref=wp)
        self._objects[name] = wp

        if self._current_doc:
            self._current_doc.objects.append(obj)

        return obj

    def create_sphere(self, radius: float, name: str = "Sphere") -> CADObject:
        """Create a sphere primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating sphere '{name}': r={radius}mm")

        wp = cq.Workplane("XY").sphere(radius)
        obj = CADObject(name=name, object_type="Sphere", backend_ref=wp)
        self._objects[name] = wp

        if self._current_doc:
            self._current_doc.objects.append(obj)

        return obj

    def create_cone(self, radius1: float, radius2: float, height: float,
                    name: str = "Cone") -> CADObject:
        """Create a cone/frustum primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating cone '{name}': r1={radius1}mm, r2={radius2}mm, h={height}mm")

        wp = cq.Workplane("XY").circle(radius1).workplane(offset=height).circle(radius2).loft()
        obj = CADObject(name=name, object_type="Cone", backend_ref=wp)
        self._objects[name] = wp

        if self._current_doc:
            self._current_doc.objects.append(obj)

        return obj

    def create_torus(self, radius1: float, radius2: float,
                     name: str = "Torus") -> CADObject:
        """Create a torus primitive using revolve."""
        name = self._unique_name(name)
        logger.debug(f"Creating torus '{name}': R={radius1}mm, r={radius2}mm")

        # Create torus profile and revolve
        wp = (cq.Workplane("XZ")
              .workplane(offset=-radius2)
              .hLine(radius1 - radius2)
              .threePointArc(
                  (radius1, radius2),
                  (radius1 - radius2, radius2 * 2)
              )
              .lineTo(radius1 - radius2, 0)
              .close()
              .revolve())
        obj = CADObject(name=name, object_type="Torus", backend_ref=wp)
        self._objects[name] = wp

        if self._current_doc:
            self._current_doc.objects.append(obj)

        return obj

    def fuse(self, obj1: CADObject, obj2: CADObject,
             name: str = "Fusion") -> CADObject:
        """Boolean union of two objects."""
        name = self._unique_name(name)
        logger.debug(f"Fusing '{obj1.name}' and '{obj2.name}' -> '{name}'")

        result = obj1.backend_ref.union(obj2.backend_ref)
        obj = CADObject(name=name, object_type="Fusion", backend_ref=result)
        self._objects[name] = result

        if self._current_doc:
            self._current_doc.objects.append(obj)

        return obj

    def cut(self, obj1: CADObject, obj2: CADObject,
            name: str = "Cut") -> CADObject:
        """Boolean difference of two objects."""
        name = self._unique_name(name)
        logger.debug(f"Cutting '{obj1.name}' - '{obj2.name}' -> '{name}'")

        result = obj1.backend_ref.cut(obj2.backend_ref)
        obj = CADObject(name=name, object_type="Cut", backend_ref=result)
        self._objects[name] = result

        if self._current_doc:
            self._current_doc.objects.append(obj)

        return obj

    def intersect(self, obj1: CADObject, obj2: CADObject,
                  name: str = "Intersection") -> CADObject:
        """Boolean intersection of two objects."""
        name = self._unique_name(name)
        logger.debug(f"Intersecting '{obj1.name}' ∩ '{obj2.name}' -> '{name}'")

        result = obj1.backend_ref.intersect(obj2.backend_ref)
        obj = CADObject(name=name, object_type="Intersection", backend_ref=result)
        self._objects[name] = result

        if self._current_doc:
            self._current_doc.objects.append(obj)

        return obj

    def fillet(self, obj: CADObject, edges: List[Any], radius: float) -> CADObject:
        """Apply fillet to edges."""
        name = self._unique_name(f"{obj.name}_Fillet")
        logger.debug(f"Filleting '{obj.name}' with r={radius}mm -> '{name}'")

        try:
            if edges:
                result = obj.backend_ref.edges(edges).fillet(radius)
            else:
                result = obj.backend_ref.edges().fillet(radius)

            obj = CADObject(name=name, object_type="Fillet", backend_ref=result)
            self._objects[name] = result

            if self._current_doc:
                self._current_doc.objects.append(obj)

            return obj
        except Exception as e:
            raise FeatureOpError("fillet", str(e))

    def chamfer(self, obj: CADObject, edges: List[Any], distance: float) -> CADObject:
        """Apply chamfer to edges."""
        name = self._unique_name(f"{obj.name}_Chamfer")
        logger.debug(f"Chamfering '{obj.name}' with d={distance}mm -> '{name}'")

        try:
            if edges:
                result = obj.backend_ref.edges(edges).chamfer(distance)
            else:
                result = obj.backend_ref.edges().chamfer(distance)

            obj = CADObject(name=name, object_type="Chamfer", backend_ref=result)
            self._objects[name] = result

            if self._current_doc:
                self._current_doc.objects.append(obj)

            return obj
        except Exception as e:
            raise FeatureOpError("chamfer", str(e))

    def move(self, obj: CADObject, x: float, y: float, z: float) -> None:
        """Move object by offset."""
        logger.debug(f"Moving '{obj.name}' by ({x}, {y}, {z})mm")
        obj.backend_ref = obj.backend_ref.translate((x, y, z))
        self._objects[obj.name] = obj.backend_ref

    def rotate(self, obj: CADObject, axis: tuple, angle: float) -> None:
        """Rotate object around axis by angle (degrees)."""
        logger.debug(f"Rotating '{obj.name}' around {axis} by {angle}°")
        obj.backend_ref = obj.backend_ref.rotate(axis, angle)
        self._objects[obj.name] = obj.backend_ref

    def recompute(self, doc: Optional[CADDocument] = None) -> None:
        """Recompute document (no-op for CadQuery - it recomputes automatically)."""
        # CadQuery recomputes geometry automatically
        logger.debug("Recompute called (no-op for CadQuery)")
        pass

    def export(self, doc: CADDocument, filepath: Path, format: str = "step") -> bool:
        """Export document to file.

        Args:
            doc: Document to export
            filepath: Output file path
            format: Export format (step, stl, obj, dxf, svg)

        Returns:
            True if export succeeded

        Raises:
            EmptyDocumentError: If document has no objects
            ExportFailedError: If export fails
        """
        format = format.lower()
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Exporting to {format.upper()}: {filepath}")

        # Check for empty document
        if not doc.objects:
            raise EmptyDocumentError("export")

        # Combine all objects for export
        try:
            result = doc.objects[0].backend_ref
            for obj in doc.objects[1:]:
                result = result.union(obj.backend_ref)

            # Export using CadQuery's exporters
            cq.exporters.export(result, str(filepath))
            logger.info(f"Export complete: {filepath}")
            return True

        except EmptyDocumentError:
            raise
        except Exception as e:
            logger.error(f"Export failed: {e}")
            raise ExportFailedError(format, str(filepath), str(e))

    # =========================================================================
    # Mass and Geometry Properties
    # =========================================================================

    def get_bounding_box(self, obj: CADObject) -> Optional[tuple]:
        """Get bounding box of an object."""
        try:
            bb = obj.backend_ref.val().BoundingBox()
            return (bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax)
        except Exception:
            return None

    def get_volume(self, obj: CADObject) -> Optional[float]:
        """Get volume of an object in mm³."""
        try:
            return obj.backend_ref.val().Volume()
        except Exception:
            return None

    def get_mass(self, obj: CADObject) -> Optional[float]:
        """Calculate mass of an object in grams."""
        from ..materials import get_material

        if not obj.material:
            return None

        material = get_material(obj.material)
        if not material:
            return None

        volume_mm3 = self.get_volume(obj)
        if volume_mm3 is None:
            return None

        # Convert volume from mm³ to cm³, then multiply by density (g/cm³)
        volume_cm3 = volume_mm3 / 1000.0
        return volume_cm3 * material.density
