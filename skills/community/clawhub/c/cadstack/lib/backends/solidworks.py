"""SolidWorks backend implementation (Windows only)."""

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


class SolidWorksBackend(CADBackend):
    """SolidWorks backend - requires SolidWorks running on Windows."""

    name = "solidworks"
    supports_headless = False

    def __init__(self):
        if not WIN32_AVAILABLE:
            raise RuntimeError(
                "SolidWorks backend requires Windows with pywin32 installed."
            )
        self._app = None
        self._model = None
        self._part = None
        self._connect()

    def _connect(self):
        """Connect to running SolidWorks instance."""
        try:
            self._app = win32com.client.Dispatch("SldWorks.Application")
            self._model = self._app.ActiveDoc
        except Exception as e:
            raise RuntimeError(f"Failed to connect to SolidWorks: {e}")

    def check_available(self) -> bool:
        """Check if SolidWorks is available."""
        if not WIN32_AVAILABLE:
            return False
        try:
            app = win32com.client.Dispatch("SldWorks.Application")
            return True
        except:
            return False

    def create_document(self, name: str = "Untitled") -> CADDocument:
        """Create a new SolidWorks part document."""
        # Create new part document
        template = self._app.GetUserPreferenceStringValue(24)  # swDefaultTemplatePart
        self._model = self._app.NewDocument(template, 0, 0, 0)
        cad_doc = CADDocument(name=name, objects=[], backend_ref=self._model)
        return cad_doc

    def create_box(self, length: float, width: float, height: float,
                   name: str = "Box") -> CADObject:
        """Create a box using feature-based modeling."""
        # Select front plane and create sketch
        self._model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)

        # Insert sketch
        self._model.InsertSketch2(True)

        # Draw rectangle
        self._model.SketchManager.CreateCornerRectangle(
            0, 0, 0, length / 1000, width / 1000, 0  # Convert mm to m
        )

        # Exit sketch
        self._model.InsertSketch2(True)

        # Extrude
        feature = self._model.FeatureManager.FeatureExtrusion2(
            True, False, False, 0, 0, height / 1000, 0,
            False, False, False, False, 0, 0,
            False, False, False, False, True, True, True,
            0, 0, False
        )

        cad_obj = CADObject(name=name, object_type="Box", backend_ref=feature)
        return cad_obj

    def create_cylinder(self, radius: float, height: float,
                        name: str = "Cylinder") -> CADObject:
        """Create a cylinder using feature-based modeling."""
        # Select front plane
        self._model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
        self._model.InsertSketch2(True)

        # Draw circle
        self._model.SketchManager.CreateCircle(0, 0, 0, radius / 1000, 0, 0)

        # Exit sketch and extrude
        self._model.InsertSketch2(True)
        feature = self._model.FeatureManager.FeatureExtrusion2(
            True, False, False, 0, 0, height / 1000, 0,
            False, False, False, False, 0, 0,
            False, False, False, False, True, True, True,
            0, 0, False
        )

        cad_obj = CADObject(name=name, object_type="Cylinder", backend_ref=feature)
        return cad_obj

    def create_sphere(self, radius: float, name: str = "Sphere") -> CADObject:
        """Create a sphere using revolve feature."""
        # Select front plane
        self._model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
        self._model.InsertSketch2(True)

        # Draw semicircle arc for revolve
        r_m = radius / 1000
        self._model.SketchManager.CreateArc(0, 0, 0, r_m, 0, 0, -r_m, 0, 0, 1)
        self._model.SketchManager.CreateLine(-r_m, 0, 0, r_m, 0, 0)

        # Exit sketch and revolve
        self._model.InsertSketch2(True)
        feature = self._model.FeatureManager.FeatureRevolve(
            True, True, False, False, False, False,
            0, 0, False, False, 0, 0, 0, 0, 0,
            True, True, True
        )

        cad_obj = CADObject(name=name, object_type="Sphere", backend_ref=feature)
        return cad_obj

    def create_cone(self, radius1: float, radius2: float, height: float,
                    name: str = "Cone") -> CADObject:
        """Create a cone using loft feature between two circles."""
        # Select front plane and create first sketch (base circle)
        self._model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
        self._model.InsertSketch2(True)

        r1_m = radius1 / 1000  # Convert mm to m
        self._model.SketchManager.CreateCircle(0, 0, 0, r1_m, 0, 0)
        self._model.InsertSketch2(True)

        # Create reference plane at height for second circle
        # Get active sketch for reference
        sketch1 = self._model.Extension.GetLastFeatureAdded()

        # Create offset plane at height
        self._model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, True, 0, None, 0)
        height_m = height / 1000
        ref_plane = self._model.FeatureManager.InsertRefPlane(8, height_m, 0, 0, 0, 0)

        # Create second sketch on the new plane
        self._model.Extension.SelectByID2("", "PLANE", 0, 0, height_m, False, 0, None, 0)
        self._model.InsertSketch2(True)

        r2_m = radius2 / 1000 if radius2 > 0 else 0.001  # Minimum radius for apex
        self._model.SketchManager.CreateCircle(0, 0, 0, r2_m, 0, 0)
        self._model.InsertSketch2(True)

        # Select both sketches and create loft
        self._model.Extension.SelectByID2("", "SKETCH", 0, 0, 0, False, 4, None, 0)
        self._model.Extension.SelectByID2("", "SKETCH", 0, 0, height_m, True, 4, None, 0)

        feature = self._model.FeatureManager.InsertProtrusionBlend(
            False, True, False, 1, 0, 0, 1, 1, True,
            True, False, 0, 0, 0, True, True, True,
            None, None, None, None, None, None
        )

        cad_obj = CADObject(name=name, object_type="Cone", backend_ref=feature)
        return cad_obj

    def create_torus(self, radius1: float, radius2: float,
                     name: str = "Torus") -> CADObject:
        """Create a torus using revolve feature."""
        # Select front plane
        self._model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
        self._model.InsertSketch2(True)

        # Draw circle for tube cross-section, offset from origin
        r1_m = radius1 / 1000  # Major radius (center to tube center)
        r2_m = radius2 / 1000  # Minor radius (tube radius)

        # Create circle centered at (r1, 0) with radius r2
        self._model.SketchManager.CreateCircle(r1_m, 0, 0, r1_m + r2_m, 0, 0)

        # Draw centerline through origin for revolve axis
        self._model.SketchManager.CreateCenterLine(0, -r2_m, 0, 0, r2_m, 0)

        # Exit sketch and revolve 360 degrees
        self._model.InsertSketch2(True)

        # Select the sketch and centerline for revolve
        feature = self._model.FeatureManager.FeatureRevolve(
            True, True, False, False, False, False,
            0, 2 * 3.14159265, False, False, 0, 0, 0, 0, 0,
            True, True, True
        )

        cad_obj = CADObject(name=name, object_type="Torus", backend_ref=feature)
        return cad_obj

    def fuse(self, obj1: CADObject, obj2: CADObject,
             name: str = "Fusion") -> CADObject:
        """Boolean union of two bodies using InsertCombineFeature."""
        # Select the body of obj1 as target
        body1 = self._get_body_from_feature(obj1.backend_ref)
        body2 = self._get_body_from_feature(obj2.backend_ref)

        if body1 is None or body2 is None:
            raise RuntimeError("Could not find bodies for boolean operation")

        # Select body1 as target
        self._model.Extension.SelectByID2(body1.Name, "SOLIDBODY", 0, 0, 0, False, 0, None, 0)
        # Select body2 as tool (add to selection)
        self._model.Extension.SelectByID2(body2.Name, "SOLIDBODY", 0, 0, 0, True, 0, None, 0)

        # InsertCombineFeature with swBodyAdd = 1
        feature = self._model.FeatureManager.InsertCombineFeature(1, None, None)

        cad_obj = CADObject(name=name, object_type="Fusion", backend_ref=feature)
        return cad_obj

    def cut(self, obj1: CADObject, obj2: CADObject,
            name: str = "Cut") -> CADObject:
        """Boolean difference of two bodies."""
        body1 = self._get_body_from_feature(obj1.backend_ref)
        body2 = self._get_body_from_feature(obj2.backend_ref)

        if body1 is None or body2 is None:
            raise RuntimeError("Could not find bodies for boolean operation")

        # Select body1 as target
        self._model.Extension.SelectByID2(body1.Name, "SOLIDBODY", 0, 0, 0, False, 0, None, 0)
        # Select body2 as tool
        self._model.Extension.SelectByID2(body2.Name, "SOLIDBODY", 0, 0, 0, True, 0, None, 0)

        # InsertCombineFeature with swBodySubtract = 2
        feature = self._model.FeatureManager.InsertCombineFeature(2, None, None)

        cad_obj = CADObject(name=name, object_type="Cut", backend_ref=feature)
        return cad_obj

    def intersect(self, obj1: CADObject, obj2: CADObject,
                  name: str = "Intersection") -> CADObject:
        """Boolean intersection of two bodies."""
        body1 = self._get_body_from_feature(obj1.backend_ref)
        body2 = self._get_body_from_feature(obj2.backend_ref)

        if body1 is None or body2 is None:
            raise RuntimeError("Could not find bodies for boolean operation")

        # Select both bodies
        self._model.Extension.SelectByID2(body1.Name, "SOLIDBODY", 0, 0, 0, False, 0, None, 0)
        self._model.Extension.SelectByID2(body2.Name, "SOLIDBODY", 0, 0, 0, True, 0, None, 0)

        # InsertCombineFeature with swBodyIntersect = 3
        feature = self._model.FeatureManager.InsertCombineFeature(3, None, None)

        cad_obj = CADObject(name=name, object_type="Intersection", backend_ref=feature)
        return cad_obj

    def _get_body_from_feature(self, feature):
        """Get the solid body from a feature."""
        try:
            # Get bodies from the part document
            bodies = self._model.GetBodies2(0)  # swSolidBody = 0
            if bodies is None:
                return None
            # Return the first body (for simple features)
            for body in bodies:
                return body
            return None
        except:
            return None

    def fillet(self, obj: CADObject, edges: List[Any], radius: float) -> CADObject:
        """Apply fillet to edges."""
        radius_m = radius / 1000  # Convert mm to m

        # If no edges specified, select all edges of the body
        if not edges:
            body = self._get_body_from_feature(obj.backend_ref)
            if body:
                # Select the body
                self._model.Extension.SelectByID2(body.Name, "SOLIDBODY", 0, 0, 0, False, 0, None, 0)
                # Select all edges
                self._model.Extension.SelectAll()
        else:
            # Select specific edges
            for edge in edges:
                self._model.Extension.SelectByID2("", "EDGE", 0, 0, 0, True, 0, None, 0)

        # Insert fillet feature
        feature = self._model.FeatureManager.InsertFeatureFillet(
            2, radius_m, 0, 0, 0, 0, 0, 0  # swFilletAllFaces = 2
        )

        cad_obj = CADObject(name=obj.name, object_type="Fillet", backend_ref=feature)
        return cad_obj

    def chamfer(self, obj: CADObject, edges: List[Any], distance: float) -> CADObject:
        """Apply chamfer to edges."""
        distance_m = distance / 1000  # Convert mm to m

        # Select edges
        if not edges:
            body = self._get_body_from_feature(obj.backend_ref)
            if body:
                self._model.Extension.SelectByID2(body.Name, "SOLIDBODY", 0, 0, 0, False, 0, None, 0)
                self._model.Extension.SelectAll()
        else:
            for edge in edges:
                self._model.Extension.SelectByID2("", "EDGE", 0, 0, 0, True, 0, None, 0)

        # Insert chamfer feature (swChamferEqualDistance = 0)
        feature = self._model.FeatureManager.InsertFeatureChamfer(
            0, distance_m, distance_m, 0, 0, 0, 0
        )

        cad_obj = CADObject(name=obj.name, object_type="Chamfer", backend_ref=feature)
        return cad_obj

    def move(self, obj: CADObject, x: float, y: float, z: float) -> None:
        """Move body by offset using Move/Copy Body feature."""
        body = self._get_body_from_feature(obj.backend_ref)
        if body is None:
            raise RuntimeError("Could not find body to move")

        # Select the body
        self._model.Extension.SelectByID2(body.Name, "SOLIDBODY", 0, 0, 0, False, 0, None, 0)

        # Use FeatureManager.InsertMoveCopyBody2
        # Parameters: copy, numCopies, constrain, translateX, translateY, translateZ, rotateX, rotateY, rotateZ, rotateAngle
        x_m = x / 1000
        y_m = y / 1000
        z_m = z / 1000

        self._model.FeatureManager.InsertMoveCopyBody2(
            body, False, 0, False, x_m, y_m, z_m, 0, 0, 0, 0
        )

    def rotate(self, obj: CADObject, axis: tuple, angle: float) -> None:
        """Rotate body around axis using Move/Copy Body feature."""
        import math

        body = self._get_body_from_feature(obj.backend_ref)
        if body is None:
            raise RuntimeError("Could not find body to rotate")

        # Select the body
        self._model.Extension.SelectByID2(body.Name, "SOLIDBODY", 0, 0, 0, False, 0, None, 0)

        # Determine rotation axis and angle
        ax, ay, az = axis
        angle_rad = math.radians(angle)

        # SolidWorks uses separate X, Y, Z rotation components
        # For rotation around a principal axis, set the corresponding angle
        rot_x = angle_rad if abs(ax) > 0.9 else 0
        rot_y = angle_rad if abs(ay) > 0.9 else 0
        rot_z = angle_rad if abs(az) > 0.9 else 0

        self._model.FeatureManager.InsertMoveCopyBody2(
            body, False, 0, False, 0, 0, 0, rot_x, rot_y, rot_z, 1
        )

    def export(self, doc: CADDocument, filepath: Path, format: str = "step") -> bool:
        """Export document to file.

        Args:
            doc: Document to export
            filepath: Output file path
            format: Export format (step, stl, iges, parasolid)

        Returns:
            True if export succeeded
        """
        try:
            filepath = Path(filepath)

            # SolidWorks export type constants
            format_map = {
                "step": 2,    # swStepAP214
                "stp": 2,
                "stl": 10,    # swSTL
                "iges": 1,    # swIGES
                "igs": 1,
                "x_t": 6,     # swParasolidText
                "x_b": 7,     # swParasolidBinary
                "sat": 8,     # swACIS
            }

            sw_type = format_map.get(format.lower(), 2)  # Default to STEP

            # SaveAs with export options
            # Parameters: filename, saveAsVersion, saveAsCopy, exportData, options, silent
            result = self._model.Extension.SaveAs(
                str(filepath), sw_type, 1, None, 0, 0
            )
            return True

        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def export_step(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STEP format."""
        try:
            filepath = Path(filepath)
            # swStepAP214 = 2
            errors = self._model.Extension.SaveAs(
                str(filepath), 2, 1, None, 0, 0
            )
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def export_stl(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STL format."""
        try:
            filepath = Path(filepath)
            # swSTL = 10
            errors = self._model.Extension.SaveAs(
                str(filepath), 10, 1, None, 0, 0
            )
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def export_obj(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to OBJ format."""
        print("OBJ export may require additional add-in in SolidWorks")
        return False
