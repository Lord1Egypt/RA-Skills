"""Fusion 360 backend implementation via socket bridge."""

import json
import socket
from pathlib import Path
from typing import List, Any, Optional

from .base import CADBackend, CADObject, CADDocument


class Fusion360Backend(CADBackend):
    """Fusion 360 backend - requires Fusion 360 bridge add-in running."""

    name = "fusion360"
    supports_headless = False

    DEFAULT_PORT = 8080

    def __init__(self, port: int = None):
        self.port = port or self.DEFAULT_PORT
        self._socket = None
        self._check_connection()

    def _check_connection(self):
        """Check if Fusion 360 bridge is available."""
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(2)
            test_socket.connect(('localhost', self.port))
            test_socket.close()
            return True
        except (socket.error, socket.timeout):
            raise RuntimeError(
                f"Fusion 360 bridge not running on port {self.port}. "
                "Start the bridge add-in in Fusion 360 first."
            )

    def check_available(self) -> bool:
        """Check if Fusion 360 bridge is available."""
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(2)
            test_socket.connect(('localhost', self.port))
            test_socket.close()
            return True
        except:
            return False

    def _send_command(self, command: dict) -> dict:
        """Send command to Fusion 360 bridge and get response."""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(30)
            self._socket.connect(('localhost', self.port))

            message = json.dumps(command) + '\n'
            self._socket.sendall(message.encode('utf-8'))

            response = b''
            while True:
                chunk = self._socket.recv(4096)
                if not chunk:
                    break
                response += chunk
                if b'\n' in response:
                    break

            self._socket.close()
            return json.loads(response.decode('utf-8').strip())
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_document(self, name: str = "Untitled") -> CADDocument:
        """Create a new Fusion 360 document."""
        result = self._send_command({
            "action": "create_document",
            "name": name
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to create document: {result.get('error')}")

        return CADDocument(
            name=name,
            objects=[],
            backend_ref=result.get("document_id")
        )

    def create_box(self, length: float, width: float, height: float,
                   name: str = "Box") -> CADObject:
        """Create a box primitive."""
        result = self._send_command({
            "action": "create_box",
            "name": name,
            "params": {
                "length": length,
                "width": width,
                "height": height
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to create box: {result.get('error')}")

        return CADObject(
            name=name,
            object_type="Box",
            backend_ref=result.get("object_id")
        )

    def create_cylinder(self, radius: float, height: float,
                        name: str = "Cylinder") -> CADObject:
        """Create a cylinder primitive."""
        result = self._send_command({
            "action": "create_cylinder",
            "name": name,
            "params": {
                "radius": radius,
                "height": height
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to create cylinder: {result.get('error')}")

        return CADObject(
            name=name,
            object_type="Cylinder",
            backend_ref=result.get("object_id")
        )

    def create_sphere(self, radius: float, name: str = "Sphere") -> CADObject:
        """Create a sphere primitive."""
        result = self._send_command({
            "action": "create_sphere",
            "name": name,
            "params": {
                "radius": radius
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to create sphere: {result.get('error')}")

        return CADObject(
            name=name,
            object_type="Sphere",
            backend_ref=result.get("object_id")
        )

    def create_cone(self, radius1: float, radius2: float, height: float,
                    name: str = "Cone") -> CADObject:
        """Create a cone/frustum primitive."""
        result = self._send_command({
            "action": "create_cone",
            "name": name,
            "params": {
                "radius1": radius1,
                "radius2": radius2,
                "height": height
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to create cone: {result.get('error')}")

        return CADObject(
            name=name,
            object_type="Cone",
            backend_ref=result.get("object_id")
        )

    def create_torus(self, radius1: float, radius2: float,
                     name: str = "Torus") -> CADObject:
        """Create a torus primitive."""
        result = self._send_command({
            "action": "create_torus",
            "name": name,
            "params": {
                "major_radius": radius1,
                "minor_radius": radius2
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to create torus: {result.get('error')}")

        return CADObject(
            name=name,
            object_type="Torus",
            backend_ref=result.get("object_id")
        )

    def fuse(self, obj1: CADObject, obj2: CADObject,
             name: str = "Fusion") -> CADObject:
        """Boolean union of two bodies."""
        result = self._send_command({
            "action": "boolean_union",
            "name": name,
            "params": {
                "target": obj1.backend_ref,
                "tool": obj2.backend_ref
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to fuse: {result.get('error')}")

        return CADObject(
            name=name,
            object_type="Fusion",
            backend_ref=result.get("object_id")
        )

    def cut(self, obj1: CADObject, obj2: CADObject,
            name: str = "Cut") -> CADObject:
        """Boolean difference of two bodies."""
        result = self._send_command({
            "action": "boolean_cut",
            "name": name,
            "params": {
                "target": obj1.backend_ref,
                "tool": obj2.backend_ref
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to cut: {result.get('error')}")

        return CADObject(
            name=name,
            object_type="Cut",
            backend_ref=result.get("object_id")
        )

    def intersect(self, obj1: CADObject, obj2: CADObject,
                  name: str = "Intersection") -> CADObject:
        """Boolean intersection of two bodies."""
        result = self._send_command({
            "action": "boolean_intersect",
            "name": name,
            "params": {
                "target": obj1.backend_ref,
                "tool": obj2.backend_ref
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to intersect: {result.get('error')}")

        return CADObject(
            name=name,
            object_type="Intersection",
            backend_ref=result.get("object_id")
        )

    def fillet(self, obj: CADObject, edges: List[Any], radius: float) -> CADObject:
        """Apply fillet to edges."""
        result = self._send_command({
            "action": "fillet",
            "params": {
                "body": obj.backend_ref,
                "edges": edges,
                "radius": radius
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to fillet: {result.get('error')}")

        return CADObject(
            name=f"{obj.name}_Fillet",
            object_type="Fillet",
            backend_ref=result.get("object_id")
        )

    def chamfer(self, obj: CADObject, edges: List[Any], distance: float) -> CADObject:
        """Apply chamfer to edges."""
        result = self._send_command({
            "action": "chamfer",
            "params": {
                "body": obj.backend_ref,
                "edges": edges,
                "distance": distance
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to chamfer: {result.get('error')}")

        return CADObject(
            name=f"{obj.name}_Chamfer",
            object_type="Chamfer",
            backend_ref=result.get("object_id")
        )

    def move(self, obj: CADObject, x: float, y: float, z: float) -> None:
        """Move body by offset."""
        result = self._send_command({
            "action": "move",
            "params": {
                "body": obj.backend_ref,
                "translation": [x, y, z]
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to move: {result.get('error')}")

    def rotate(self, obj: CADObject, axis: tuple, angle: float) -> None:
        """Rotate body around axis."""
        result = self._send_command({
            "action": "rotate",
            "params": {
                "body": obj.backend_ref,
                "axis": list(axis),
                "angle": angle
            }
        })

        if not result.get("success"):
            raise RuntimeError(f"Failed to rotate: {result.get('error')}")

    def export_step(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STEP format."""
        result = self._send_command({
            "action": "export",
            "format": "step",
            "filepath": str(filepath)
        })
        return result.get("success", False)

    def export_stl(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to STL format."""
        result = self._send_command({
            "action": "export",
            "format": "stl",
            "filepath": str(filepath)
        })
        return result.get("success", False)

    def export_obj(self, doc: CADDocument, filepath: Path) -> bool:
        """Export to OBJ format."""
        result = self._send_command({
            "action": "export",
            "format": "obj",
            "filepath": str(filepath)
        })
        return result.get("success", False)
