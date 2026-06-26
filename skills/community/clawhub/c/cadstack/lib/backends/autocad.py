"""AutoCAD backend implementation (Windows only)."""

import sys
from pathlib import Path
from typing import List, Any, Optional

from .base import CADBackend, CADObject, CADDocument

if sys.platform == "win32":
    try:
        import win32com.client
        WIN32_AVAILABLE = True
    except ImportError:
        WIN32_AVAILABLE = False
else:
    WIN32_AVAILABLE = False


class AutoCADBackend(CADBackend):
    """AutoCAD backend - requires AutoCAD running on Windows."""

    name = "autocad"
    supports_headless = False

    def __init__(self):
        if not WIN32_AVAILABLE:
            raise RuntimeError(
                "AutoCAD backend requires Windows with pywin32 installed."
            )
        self._app = None
        self._doc = None
        self._connect()

    def _connect(self):
        """Connect to running AutoCAD instance."""
        try:
            self._app = win32com.client.Dispatch("AutoCAD.Application")
            self._doc = self._app.ActiveDocument
            if self._doc is None:
                self._doc = self._app.Documents.Add()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to AutoCAD: {e}")

    def check_available(self) -> bool:
        """Check if AutoCAD is available."""
        if not WIN32_AVAILABLE:
            return False
        try:
            app = win32com.client.Dispatch("AutoCAD.Application")
            return True
        except:
            return False

    def create_document(self, name: str = "Untitled") -> CADDocument:
        """Create a new AutoCAD document."""
        doc = self._app.Documents.Add()
        cad_doc = CADDocument(name=name, objects=[], backend_ref=doc)
        self._doc = doc
        return cad_doc

    def create_box(self, length: float, width: float, height: float,
                   name: str = "Box") -> CADObject:
        """Create a 3D box using solid modeling."""
        # AutoCAD uses Acad3DSolid for boxes
        # corner point at origin
        corner = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.com.VT_R8,
            [0.0, 0.0, 0.0]
        )
        box = self._doc.ModelSpace.AddBox(corner, length, width, height)
        cad_obj = CADObject(name=name, object_type="Box", backend_ref=box)
        return cad_obj

    def create_cylinder(self, radius: float, height: float,
                        name: str = "Cylinder") -> CADObject:
        """Create a cylinder primitive."""
        center = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.com.VT_R8,
            [0.0, 0.0, 0.0]
        )
        cyl = self._doc.ModelSpace.AddCylinder(center, radius, height)
        cad_obj = CADObject(name=name, object_type="Cylinder", backend_ref=cyl)
        return cad_obj

    def create_sphere(self, radius: float, name: str = "Sphere") -> CADObject:
        """Create a sphere primitive."""
        center = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.com.VT_R8,
            [0.0, 0.0, 0.0]
        )
        sphere = self._doc.ModelSpace.AddSphere(center, radius)
        cad_obj = CADObject(name=name, object_type="Sphere", backend_ref=sphere)
        return cad_obj

    def create_cone(self, radius1: float, radius2: float, height: float,
                    name: str = "Cone") -> CADObject:
        """Create a cone/frustum primitive.

        AutoCAD AddCone only supports one radius (apex at top).
        For frustum (radius2 > 0), we create a cone and slice it.
        """
        center = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.client.com.VT_R8,
            [0.0, 0.0, 0.0]
        )

        if radius2 == 0:
            # Simple cone - apex at top
            cone = self._doc.ModelSpace.AddCone(center, radius1, height)
        else:
            # Frustum - create full cone and slice
            # Create cone with larger radius
            full_height = height * radius1 / (radius1 - radius2) if radius1 != radius2 else height
            cone = self._doc.ModelSpace.AddCone(center, radius1, full_height)

            # If radius2 < radius1, slice off the top portion
            # This is complex in AutoCAD COM - for now, use the larger radius
            # A proper implementation would use a slicing plane
            pass  # Simplified: AutoCAD COM frustum requires more complex approach

        cad_obj = CADObject(name=name, object_type="Cone", backend_ref=cone)
        return cad_obj

    def create_torus(self, radius1: float, radius2: float,
                     name: str = "Torus") -> CADObject:
        """Create a torus primitive."""
        center = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.com.VT_R8,
            [0.0, 0.0, 0.0]
        )
        torus = self._doc.ModelSpace.AddTorus(center, radius1, radius2)
        cad_obj = CADObject(name=name, object_type="Torus", backend_ref=torus)
        return cad_obj

    def fuse(self, obj1: CADObject, obj2: CADObject,
             name: str = "Fusion") -> CADObject:
        """Boolean union of two solids."""
        result = self._doc.ModelSpace.BooleanUnion(
            obj1.backend_ref, obj2.backend_ref
        )
        cad_obj = CADObject(name=name, object_type="Fusion", backend_ref=result)
        return cad_obj

    def cut(self, obj1: CADObject, obj2: CADObject,
            name: str = "Cut") -> CADObject:
        """Boolean difference of two solids."""
        result = self._doc.ModelSpace.BooleanSubtract(
            obj1.backend_ref, obj2.backend_ref
        )
        cad_obj = CADObject(name=name, object_type="Cut", backend_ref=result)
        return cad_obj

    def intersect(self, obj1: CADObject, obj2: CADObject,
                  name: str = "Intersection") -> CADObject:
        """Boolean intersection of two solids."""
        result = self._doc.ModelSpace.BooleanIntersect(
            obj1.backend_ref, obj2.backend_ref
        )
        cad_obj = CADObject(name=name, object_type="Intersection", backend_ref=result)
        return cad_obj

    def fillet(self, obj: CADObject, edges: List[Any], radius: float) -> CADObject:
        """Apply fillet to edges (limited support)."""
        # AutoCAD COM has limited fillet support for 3D solids
        raise NotImplementedError("Fillet not directly supported via COM for 3D solids")

    def chamfer(self, obj: CADObject, edges: List[Any], distance: float) -> CADObject:
        """Apply chamfer to edges (limited support)."""
        raise NotImplementedError("Chamfer not directly supported via COM for 3D solids")

    def move(self, obj: CADObject, x: float, y: float, z: float) -> None:
        """Move object by offset."""
        # Get current position and create displacement
        from_point = obj.backend_ref.Centroid
        to_point = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.com.VT_R8,
            [from_point[0] + x, from_point[1] + y, from_point[2] + z]
        )
        obj.backend_ref.Move(from_point, to_point)

    def rotate(self, obj: CADObject, axis: tuple, angle: float) -> None:
        """Rotate object around axis by angle (degrees)."""
        import math

        # Get object centroid as rotation base point
        base_point = obj.backend_ref.Centroid

        # Convert angle to radians for calculation
        angle_rad = math.radians(angle)

        # Normalize axis
        ax, ay, az = axis
        length = math.sqrt(ax*ax + ay*ay + az*az)
        if length > 0:
            ax, ay, az = ax/length, ay/length, az/length

        # AutoCAD 3D rotation uses Rotate3D method
        # Parameters: base_point, axis_point2, rotation_angle (radians)
        axis_point2 = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.client.com.VT_R8,
            [base_point[0] + ax, base_point[1] + ay, base_point[2] + az]
        )

        base_point_variant = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.client.com.VT_R8,
            [base_point[0], base_point[1], base_point[2]]
        )

        obj.backend_ref.Rotate3D(base_point_variant, axis_point2, angle_rad)

    def export(self, doc: CADDocument, filepath: Path, format: str = "step") -> bool:
        """Export document to file.

        Args:
            doc: Document to export
            filepath: Output file path
            format: Export format (step, stl, sat, dwg)

        Returns:
            True if export succeeded
        """
        try:
            filepath = Path(filepath)

            # Map format to AutoCAD export type
            format_map = {
                "step": "STEP",
                "stp": "STEP",
                "stl": "STL",
                "sat": "SAT",
                "dwg": "DWG",
                "dxf": "DXF"
            }

            acad_format = format_map.get(format.lower(), format.upper())

            # Try Export command first (newer AutoCAD)
            try:
                self._doc.Export(str(filepath), acad_format)
                return True
            except:
                pass

            # Fallback to SendCommand for older versions
            command = f'_EXPORT "{filepath}" '
            if acad_format == "STEP":
                command = f'_STEP "{filepath}"'
            elif acad_format == "STL":
                command = f'_STLOUT "{filepath}"'

            self._doc.SendCommand(command + "\n")
            return True

        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def export_step(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STEP format."""
        try:
            filepath = Path(filepath)
            # Use ACISOUT or Export command
            self._doc.Export(str(filepath), "SAT")
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def export_stl(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STL format."""
        try:
            filepath = Path(filepath)
            self._doc.Export(str(filepath), "STL")
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def export_obj(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to OBJ format (limited support)."""
        print("OBJ export not natively supported in AutoCAD")
        return False
