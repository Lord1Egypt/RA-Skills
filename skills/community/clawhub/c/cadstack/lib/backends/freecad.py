"""FreeCAD backend implementation."""

from pathlib import Path
from typing import List, Any, Optional
import logging

from .base import CADBackend, CADObject, CADDocument
from ..exceptions import ExportFailedError, EmptyDocumentError, FeatureOpError

try:
    import FreeCAD
    import Part
    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False
    FreeCAD = None
    Part = None

logger = logging.getLogger(__name__)


class FreeCADBackend(CADBackend):
    """FreeCAD backend - supports headless mode.

    FreeCAD is a free and open-source parametric 3D CAD modeler.
    It runs in headless mode without GUI, making it suitable for
    automation and server environments.
    """

    name = "freecad"
    supports_headless = True
    supported_formats = ["step", "stl", "obj", "dxf", "svg", "fcstd"]

    def __init__(self):
        if not FREECAD_AVAILABLE:
            from ..exceptions import BackendNotAvailableError
            raise BackendNotAvailableError("freecad")

        super().__init__()
        self._documents: dict = {}
        self._current_doc: Optional[CADDocument] = None

    def check_available(self) -> bool:
        return FREECAD_AVAILABLE

    def create_document(self, name: str = "Untitled") -> CADDocument:
        """Create a new FreeCAD document."""
        logger.debug(f"Creating document: {name}")
        doc = FreeCAD.newDocument(name)
        cad_doc = CADDocument(name=name, objects=[], backend_ref=doc)
        self._documents[name] = cad_doc
        self._current_doc = cad_doc
        return cad_doc

    def get_or_create_doc(self) -> CADDocument:
        """Get current document or create one."""
        if self._current_doc is None:
            return self.create_document()
        return self._current_doc

    def create_box(self, length: float, width: float, height: float,
                   name: str = "Box") -> CADObject:
        """Create a box primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating box '{name}': {length}x{width}x{height}mm")

        doc = self.get_or_create_doc()
        box = doc.backend_ref.addObject("Part::Box", name)
        box.Length = length
        box.Width = width
        box.Height = height

        cad_obj = CADObject(name=name, object_type="Box", backend_ref=box)
        doc.objects.append(cad_obj)
        self._objects[name] = cad_obj
        return cad_obj

    def create_cylinder(self, radius: float, height: float,
                        name: str = "Cylinder") -> CADObject:
        """Create a cylinder primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating cylinder '{name}': r={radius}mm, h={height}mm")

        doc = self.get_or_create_doc()
        cyl = doc.backend_ref.addObject("Part::Cylinder", name)
        cyl.Radius = radius
        cyl.Height = height

        cad_obj = CADObject(name=name, object_type="Cylinder", backend_ref=cyl)
        doc.objects.append(cad_obj)
        self._objects[name] = cad_obj
        return cad_obj

    def create_sphere(self, radius: float, name: str = "Sphere") -> CADObject:
        """Create a sphere primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating sphere '{name}': r={radius}mm")

        doc = self.get_or_create_doc()
        sphere = doc.backend_ref.addObject("Part::Sphere", name)
        sphere.Radius = radius

        cad_obj = CADObject(name=name, object_type="Sphere", backend_ref=sphere)
        doc.objects.append(cad_obj)
        self._objects[name] = cad_obj
        return cad_obj

    def create_cone(self, radius1: float, radius2: float, height: float,
                    name: str = "Cone") -> CADObject:
        """Create a cone/frustum primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating cone '{name}': r1={radius1}mm, r2={radius2}mm, h={height}mm")

        doc = self.get_or_create_doc()
        cone = doc.backend_ref.addObject("Part::Cone", name)
        cone.Radius1 = radius1
        cone.Radius2 = radius2
        cone.Height = height

        cad_obj = CADObject(name=name, object_type="Cone", backend_ref=cone)
        doc.objects.append(cad_obj)
        self._objects[name] = cad_obj
        return cad_obj

    def create_torus(self, radius1: float, radius2: float,
                     name: str = "Torus") -> CADObject:
        """Create a torus primitive."""
        name = self._unique_name(name)
        logger.debug(f"Creating torus '{name}': R={radius1}mm, r={radius2}mm")

        doc = self.get_or_create_doc()
        torus = doc.backend_ref.addObject("Part::Torus", name)
        torus.Radius1 = radius1  # Major radius
        torus.Radius2 = radius2  # Minor radius

        cad_obj = CADObject(name=name, object_type="Torus", backend_ref=torus)
        doc.objects.append(cad_obj)
        self._objects[name] = cad_obj
        return cad_obj

    def fuse(self, obj1: CADObject, obj2: CADObject,
             name: str = "Fusion") -> CADObject:
        """Boolean union of two objects."""
        name = self._unique_name(name)
        logger.debug(f"Fusing '{obj1.name}' and '{obj2.name}' -> '{name}'")

        doc = self.get_or_create_doc()
        fusion = doc.backend_ref.addObject("Part::Fuse", name)
        fusion.Base = obj1.backend_ref
        fusion.Tool = obj2.backend_ref

        cad_obj = CADObject(name=name, object_type="Fusion", backend_ref=fusion)
        doc.objects.append(cad_obj)
        self._objects[name] = cad_obj
        return cad_obj

    def cut(self, obj1: CADObject, obj2: CADObject,
            name: str = "Cut") -> CADObject:
        """Boolean difference of two objects."""
        name = self._unique_name(name)
        logger.debug(f"Cutting '{obj1.name}' - '{obj2.name}' -> '{name}'")

        doc = self.get_or_create_doc()
        cut = doc.backend_ref.addObject("Part::Cut", name)
        cut.Base = obj1.backend_ref
        cut.Tool = obj2.backend_ref

        cad_obj = CADObject(name=name, object_type="Cut", backend_ref=cut)
        doc.objects.append(cad_obj)
        self._objects[name] = cad_obj
        return cad_obj

    def intersect(self, obj1: CADObject, obj2: CADObject,
                  name: str = "Intersection") -> CADObject:
        """Boolean intersection of two objects."""
        name = self._unique_name(name)
        logger.debug(f"Intersecting '{obj1.name}' ∩ '{obj2.name}' -> '{name}'")

        doc = self.get_or_create_doc()
        common = doc.backend_ref.addObject("Part::Common", name)
        common.Base = obj1.backend_ref
        common.Tool = obj2.backend_ref

        cad_obj = CADObject(name=name, object_type="Intersection", backend_ref=common)
        doc.objects.append(cad_obj)
        self._objects[name] = cad_obj
        return cad_obj

    def fillet(self, obj: CADObject, edges: List[Any], radius: float) -> CADObject:
        """Apply fillet to edges."""
        name = self._unique_name(f"{obj.name}_Fillet")
        logger.debug(f"Filleting '{obj.name}' with r={radius}mm -> '{name}'")

        try:
            doc = self.get_or_create_doc()
            fillet = doc.backend_ref.addObject("Part::Fillet", name)
            fillet.Base = obj.backend_ref
            fillet.Radius = radius
            # If edges is empty, fillet all edges
            if edges:
                fillet.Edges = edges

            cad_obj = CADObject(name=name, object_type="Fillet", backend_ref=fillet)
            doc.objects.append(cad_obj)
            self._objects[name] = cad_obj
            return cad_obj
        except Exception as e:
            raise FeatureOpError("fillet", str(e))

    def chamfer(self, obj: CADObject, edges: List[Any], distance: float) -> CADObject:
        """Apply chamfer to edges."""
        name = self._unique_name(f"{obj.name}_Chamfer")
        logger.debug(f"Chamfering '{obj.name}' with d={distance}mm -> '{name}'")

        try:
            doc = self.get_or_create_doc()
            chamfer = doc.backend_ref.addObject("Part::Chamfer", name)
            chamfer.Base = obj.backend_ref
            chamfer.Size = distance
            if edges:
                chamfer.Edges = edges

            cad_obj = CADObject(name=name, object_type="Chamfer", backend_ref=chamfer)
            doc.objects.append(cad_obj)
            self._objects[name] = cad_obj
            return cad_obj
        except Exception as e:
            raise FeatureOpError("chamfer", str(e))

    def move(self, obj: CADObject, x: float, y: float, z: float) -> None:
        """Move object by offset."""
        logger.debug(f"Moving '{obj.name}' by ({x}, {y}, {z})mm")
        obj.backend_ref.Placement.Base.x += x
        obj.backend_ref.Placement.Base.y += y
        obj.backend_ref.Placement.Base.z += z

    def rotate(self, obj: CADObject, axis: tuple, angle: float) -> None:
        """Rotate object around axis by angle (degrees)."""
        logger.debug(f"Rotating '{obj.name}' around {axis} by {angle}°")
        import math
        from FreeCAD import Rotation
        rotation = Rotation(axis, angle)
        obj.backend_ref.Placement.Rotation = rotation.multiply(obj.backend_ref.Placement.Rotation)

    def recompute(self, doc: Optional[CADDocument] = None) -> None:
        """Recompute the document to update all objects."""
        if doc is None:
            doc = self._current_doc
        if doc and doc.backend_ref:
            logger.debug(f"Recomputing document: {doc.name}")
            doc.backend_ref.recompute()

    def export(self, doc: CADDocument, filepath: Path, format: str = "step") -> bool:
        """Export document to file.

        Args:
            doc: Document to export
            filepath: Output file path
            format: Export format (step, stl, obj, dxf, svg, fcstd)

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

        # Recompute before export
        self.recompute(doc)

        try:
            if format == "step":
                return self._export_step(doc, filepath)
            elif format == "stl":
                return self._export_stl(doc, filepath)
            elif format == "obj":
                return self._export_obj(doc, filepath)
            elif format == "fcstd":
                return self._save_fcstd(doc, filepath)
            else:
                raise ExportFailedError(format, str(filepath), f"Unsupported format")

        except EmptyDocumentError:
            raise
        except ExportFailedError:
            raise
        except Exception as e:
            logger.error(f"Export failed: {e}")
            raise ExportFailedError(format, str(filepath), str(e))

    def _export_step(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STEP format."""
        import Import
        Import.export(
            [obj.backend_ref for obj in doc.objects if obj.backend_ref],
            str(filepath)
        )
        logger.info(f"Export complete: {filepath}")
        return True

    def _export_stl(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STL format."""
        import Mesh

        shapes = [obj.backend_ref.Shape for obj in doc.objects
                 if obj.backend_ref and hasattr(obj.backend_ref, 'Shape')]

        if not shapes:
            raise EmptyDocumentError("export")

        mesh = Mesh.Mesh()
        for shape in shapes:
            mesh.addMesh(Mesh.Mesh(shape.tessellate(0.1)))
        mesh.write(str(filepath))

        logger.info(f"Export complete: {filepath}")
        return True

    def _export_obj(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to OBJ format."""
        import Mesh

        shapes = [obj.backend_ref.Shape for obj in doc.objects
                 if obj.backend_ref and hasattr(obj.backend_ref, 'Shape')]

        if not shapes:
            raise EmptyDocumentError("export")

        mesh = Mesh.Mesh()
        for shape in shapes:
            mesh.addMesh(Mesh.Mesh(shape.tessellate(0.1)))
        mesh.write(str(filepath))

        logger.info(f"Export complete: {filepath}")
        return True

    def _save_fcstd(self, doc: CADDocument, filepath: Path) -> bool:
        """Save as FreeCAD native format."""
        doc.backend_ref.saveAs(str(filepath))
        logger.info(f"Saved: {filepath}")
        return True

    def save(self, doc: CADDocument, filepath: Path) -> bool:
        """Save document as FreeCAD (.FCStd) file (legacy method)."""
        return self._save_fcstd(doc, filepath)

    # =========================================================================
    # Mass and Geometry Properties
    # =========================================================================

    def get_bounding_box(self, obj: CADObject) -> Optional[tuple]:
        """Get bounding box of an object."""
        try:
            if hasattr(obj.backend_ref, 'Shape'):
                bb = obj.backend_ref.Shape.BoundBox
                return (bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax)
        except Exception:
            pass
        return None

    def get_volume(self, obj: CADObject) -> Optional[float]:
        """Get volume of an object in mm³."""
        try:
            if hasattr(obj.backend_ref, 'Shape'):
                return obj.backend_ref.Shape.Volume
        except Exception:
            pass
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
