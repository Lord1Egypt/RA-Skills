"""Abstract base class for CAD backends.

This module defines the interface that all CAD backends must implement.
The interface is divided into:
- Required operations: Must be implemented by all backends
- Optional operations: May raise NotImplementedError if not supported
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Any, Dict
import logging

logger = logging.getLogger(__name__)


@dataclass
class CADObject:
    """Represents a CAD object in the scene.

    Attributes:
        name: Unique identifier for this object
        object_type: Type of object (Box, Cylinder, Fusion, etc.)
        backend_ref: Reference to backend-specific object
        material: Optional material assignment
    """
    name: str
    object_type: str
    backend_ref: Any = None
    material: Optional[str] = None


@dataclass
class CADDocument:
    """Represents a CAD document containing multiple objects.

    Attributes:
        name: Document name
        objects: List of CAD objects in this document
        backend_ref: Reference to backend-specific document
        metadata: Additional document metadata
    """
    name: str
    objects: List[CADObject] = field(default_factory=list)
    backend_ref: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Material:
    """Material properties for CAD objects.

    Attributes:
        name: Material identifier (e.g., "aluminum_6061")
        density: Density in g/cm³
        color: Hex color code for visualization
        description: Human-readable description
    """
    name: str
    density: float = 1.0  # g/cm³
    color: str = "#808080"
    description: str = ""


class CADBackend(ABC):
    """Abstract base class for CAD backends.

    All CAD backends must implement the required abstract methods.
    Optional methods have default implementations that raise
    NotImplementedError.

    Attributes:
        name: Backend identifier (e.g., "cadquery", "freecad")
        supports_headless: Whether backend can run without GUI
        supported_formats: List of supported export formats
    """

    name: str = "base"
    supports_headless: bool = False
    supported_formats: List[str] = ["step", "stl", "obj"]

    def __init__(self):
        self._objects: Dict[str, CADObject] = {}
        self._current_doc: Optional[CADDocument] = None
        self._name_counter: Dict[str, int] = {}

    def _unique_name(self, base_name: str) -> str:
        """Generate a unique name for an object.

        If the name already exists, appends _2, _3, etc.

        Args:
            base_name: Desired name for the object

        Returns:
            A unique name that doesn't conflict with existing objects
        """
        if base_name not in self._objects and base_name not in self._name_counter:
            return base_name

        if base_name not in self._name_counter:
            self._name_counter[base_name] = 1

        self._name_counter[base_name] += 1
        unique_name = f"{base_name}_{self._name_counter[base_name]}"

        # Keep incrementing until we find a truly unique name
        while unique_name in self._objects:
            self._name_counter[base_name] += 1
            unique_name = f"{base_name}_{self._name_counter[base_name]}"

        return unique_name

    # =========================================================================
    # Required Operations - Must be implemented by all backends
    # =========================================================================

    @abstractmethod
    def create_document(self, name: str = "Untitled") -> CADDocument:
        """Create a new CAD document.

        Args:
            name: Document name

        Returns:
            The created CADDocument
        """
        pass

    @abstractmethod
    def create_box(self, length: float, width: float, height: float,
                   name: str = "Box") -> CADObject:
        """Create a box primitive.

        Args:
            length: Box length in mm
            width: Box width in mm
            height: Box height in mm
            name: Object name

        Returns:
            The created CADObject
        """
        pass

    @abstractmethod
    def create_cylinder(self, radius: float, height: float,
                        name: str = "Cylinder") -> CADObject:
        """Create a cylinder primitive.

        Args:
            radius: Cylinder radius in mm
            height: Cylinder height in mm
            name: Object name

        Returns:
            The created CADObject
        """
        pass

    @abstractmethod
    def create_sphere(self, radius: float, name: str = "Sphere") -> CADObject:
        """Create a sphere primitive.

        Args:
            radius: Sphere radius in mm
            name: Object name

        Returns:
            The created CADObject
        """
        pass

    @abstractmethod
    def create_cone(self, radius1: float, radius2: float, height: float,
                    name: str = "Cone") -> CADObject:
        """Create a cone/frustum primitive.

        Args:
            radius1: Bottom radius in mm
            radius2: Top radius in mm
            height: Cone height in mm
            name: Object name

        Returns:
            The created CADObject
        """
        pass

    @abstractmethod
    def create_torus(self, radius1: float, radius2: float,
                     name: str = "Torus") -> CADObject:
        """Create a torus primitive.

        Args:
            radius1: Major radius (center to tube center) in mm
            radius2: Minor radius (tube radius) in mm
            name: Object name

        Returns:
            The created CADObject
        """
        pass

    @abstractmethod
    def fuse(self, obj1: CADObject, obj2: CADObject,
             name: str = "Fusion") -> CADObject:
        """Boolean union of two objects.

        Args:
            obj1: First object
            obj2: Second object
            name: Result name

        Returns:
            The fused CADObject
        """
        pass

    @abstractmethod
    def cut(self, obj1: CADObject, obj2: CADObject,
            name: str = "Cut") -> CADObject:
        """Boolean difference of two objects.

        Args:
            obj1: Object to cut from
            obj2: Object to cut with
            name: Result name

        Returns:
            The resulting CADObject
        """
        pass

    @abstractmethod
    def intersect(self, obj1: CADObject, obj2: CADObject,
                  name: str = "Intersection") -> CADObject:
        """Boolean intersection of two objects.

        Args:
            obj1: First object
            obj2: Second object
            name: Result name

        Returns:
            The intersected CADObject
        """
        pass

    @abstractmethod
    def move(self, obj: CADObject, x: float, y: float, z: float) -> None:
        """Move object by offset.

        Args:
            obj: Object to move
            x: X offset in mm
            y: Y offset in mm
            z: Z offset in mm
        """
        pass

    @abstractmethod
    def rotate(self, obj: CADObject, axis: tuple, angle: float) -> None:
        """Rotate object around axis.

        Args:
            obj: Object to rotate
            axis: Rotation axis as (x, y, z) tuple
            angle: Rotation angle in degrees
        """
        pass

    @abstractmethod
    def export(self, doc: CADDocument, filepath: Path, format: str = "step") -> bool:
        """Export document to file.

        Args:
            doc: Document to export
            filepath: Output file path
            format: Export format (step, stl, obj)

        Returns:
            True if export succeeded

        Raises:
            ExportFailedError: If export fails
            EmptyDocumentError: If document has no objects
        """
        pass

    # =========================================================================
    # Optional Operations - May raise NotImplementedError
    # =========================================================================

    def fillet(self, obj: CADObject, edges: List[Any], radius: float) -> CADObject:
        """Apply fillet to edges.

        This is an optional operation. Some backends may not support it.

        Args:
            obj: Object to fillet
            edges: List of edges to fillet (empty = all edges)
            radius: Fillet radius in mm

        Returns:
            The filleted CADObject

        Raises:
            NotImplementedError: If backend doesn't support fillet
        """
        raise NotImplementedError(
            f"{self.name} backend does not support fillet operation"
        )

    def chamfer(self, obj: CADObject, edges: List[Any], distance: float) -> CADObject:
        """Apply chamfer to edges.

        This is an optional operation. Some backends may not support it.

        Args:
            obj: Object to chamfer
            edges: List of edges to chamfer (empty = all edges)
            distance: Chamfer distance in mm

        Returns:
            The chamfered CADObject

        Raises:
            NotImplementedError: If backend doesn't support chamfer
        """
        raise NotImplementedError(
            f"{self.name} backend does not support chamfer operation"
        )

    def recompute(self, doc: Optional[CADDocument] = None) -> None:
        """Recompute the document to update all objects.

        This is needed for some backends (like FreeCAD) to update
        geometry after operations. For backends that don't need it,
        this is a no-op.

        Args:
            doc: Document to recompute (uses current doc if None)
        """
        # Default: no-op for backends that don't need explicit recomputation
        pass

    # =========================================================================
    # Legacy Export Methods - For backwards compatibility
    # =========================================================================

    def export_step(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STEP format (legacy method).

        Deprecated: Use export(doc, filepath, "step") instead.
        """
        logger.warning("export_step() is deprecated, use export() with format='step'")
        return self.export(doc, filepath, "step")

    def export_stl(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STL format (legacy method).

        Deprecated: Use export(doc, filepath, "stl") instead.
        """
        logger.warning("export_stl() is deprecated, use export() with format='stl'")
        return self.export(doc, filepath, "stl")

    def export_obj(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to OBJ format (legacy method).

        Deprecated: Use export(doc, filepath, "obj") instead.
        """
        logger.warning("export_obj() is deprecated, use export() with format='obj'")
        return self.export(doc, filepath, "obj")

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def check_available(self) -> bool:
        """Check if this backend is available.

        Returns:
            True if backend can be used
        """
        return True

    def get_info(self) -> dict:
        """Get backend information.

        Returns:
            Dictionary with backend metadata
        """
        return {
            "name": self.name,
            "supports_headless": self.supports_headless,
            "supported_formats": self.supported_formats,
            "available": self.check_available()
        }

    def get_last_object(self) -> Optional[CADObject]:
        """Get the last created object.

        Returns:
            The most recently created CADObject, or None
        """
        if self._current_doc and self._current_doc.objects:
            return self._current_doc.objects[-1]
        return None

    def get_object(self, name: str) -> Optional[CADObject]:
        """Get an object by name.

        Args:
            name: Object name

        Returns:
            The CADObject, or None if not found
        """
        if self._current_doc:
            for obj in self._current_doc.objects:
                if obj.name == name:
                    return obj
        return None

    def list_objects(self) -> List[str]:
        """List all object names.

        Returns:
            List of object names
        """
        return list(self._objects.keys())

    # =========================================================================
    # Material and Mass Properties (Optional)
    # =========================================================================

    def set_material(self, obj: CADObject, material: str) -> None:
        """Set material for an object.

        Args:
            obj: Object to modify
            material: Material name
        """
        obj.material = material

    def get_mass(self, obj: CADObject) -> Optional[float]:
        """Calculate mass of an object.

        Requires material to be set and density available.

        Args:
            obj: Object to calculate mass for

        Returns:
            Mass in grams, or None if cannot calculate
        """
        # Default implementation - override in backend if supported
        return None

    def get_bounding_box(self, obj: CADObject) -> Optional[tuple]:
        """Get bounding box of an object.

        Args:
            obj: Object to measure

        Returns:
            Tuple of (min_x, min_y, min_z, max_x, max_y, max_z) or None
        """
        # Default implementation - override in backend if supported
        return None
