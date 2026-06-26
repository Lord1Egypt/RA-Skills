# Fusion 360 CADStack Bridge Add-in
# Run this add-in in Fusion 360 to enable CAD automation via socket

import adsk.core, adsk.fusion, traceback
import socket
import json
import threading
import sys

# Configuration
HOST = 'localhost'
PORT = 8080
BUFFER_SIZE = 4096

class Fusion360Bridge:
    """Bridge between Fusion 360 and CADStack."""

    def __init__(self):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        self.running = False
        self.server_socket = None

    def start(self):
        """Start the bridge server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(1)
            self.server_socket.settimeout(1.0)  # Allow checking running flag

            self.running = True
            self.ui.messageBox(f'CADStack Bridge started on port {PORT}')

            # Start server thread
            thread = threading.Thread(target=self._server_loop)
            thread.daemon = True
            thread.start()

        except Exception as e:
            self.ui.messageBox(f'Failed to start bridge: {str(e)}')

    def stop(self):
        """Stop the bridge server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.ui.messageBox('CADStack Bridge stopped')

    def _server_loop(self):
        """Main server loop."""
        while self.running:
            try:
                self.server_socket.settimeout(0.5)
                client_socket, address = self.server_socket.accept()

                # Handle request
                data = client_socket.recv(BUFFER_SIZE)
                if data:
                    request = json.loads(data.decode('utf-8'))
                    response = self._handle_request(request)
                    client_socket.sendall((json.dumps(response) + '\n').encode('utf-8'))

                client_socket.close()

            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    adsk.core.Application.get().userInterface.messageBox(f'Bridge error: {str(e)}')

    def _handle_request(self, request):
        """Handle an incoming request."""
        action = request.get('action')

        try:
            if action == 'create_document':
                return self._create_document(request)
            elif action == 'create_box':
                return self._create_box(request)
            elif action == 'create_cylinder':
                return self._create_cylinder(request)
            elif action == 'create_sphere':
                return self._create_sphere(request)
            elif action == 'create_cone':
                return self._create_cone(request)
            elif action == 'create_torus':
                return self._create_torus(request)
            elif action == 'boolean_union':
                return self._boolean_union(request)
            elif action == 'boolean_cut':
                return self._boolean_cut(request)
            elif action == 'boolean_intersect':
                return self._boolean_intersect(request)
            elif action == 'fillet':
                return self._fillet(request)
            elif action == 'chamfer':
                return self._chamfer(request)
            elif action == 'move':
                return self._move(request)
            elif action == 'rotate':
                return self._rotate(request)
            elif action == 'export':
                return self._export(request)
            else:
                return {'success': False, 'error': f'Unknown action: {action}'}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _create_document(self, request):
        """Create a new Fusion 360 document."""
        name = request.get('name', 'Untitled')
        doc = self.app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        return {'success': True, 'document_id': doc.name}

    def _create_box(self, request):
        """Create a box primitive."""
        params = request.get('params', {})
        length = params.get('length', 10) / 10  # mm to cm
        width = params.get('width', 10) / 10
        height = params.get('height', 10) / 10
        name = request.get('name', 'Box')

        design = self.app.activeProduct
        root = design.rootComponent

        # Create sketch
        sketches = root.sketches
        xy_plane = root.xYConstructionPlane
        sketch = sketches.add(xy_plane)

        # Draw rectangle
        lines = sketch.sketchCurves.sketchLines
        point0 = adsk.core.Point3D.create(0, 0, 0)
        point1 = adsk.core.Point3D.create(length, width, 0)
        lines.addTwoPointRectangle(point0, point1)

        # Get profile and extrude
        profile = sketch.profiles.item(0)
        extrudes = root.features.extrudeFeatures

        ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(height)
        ext_input.setDistanceExtent(False, distance)

        ext = extrudes.add(ext_input)
        ext.bodies.item(0).name = name

        return {'success': True, 'object_id': name}

    def _create_cylinder(self, request):
        """Create a cylinder primitive."""
        params = request.get('params', {})
        radius = params.get('radius', 5) / 10  # mm to cm
        height = params.get('height', 10) / 10
        name = request.get('name', 'Cylinder')

        design = self.app.activeProduct
        root = design.rootComponent

        # Create sketch
        sketches = root.sketches
        xy_plane = root.xYConstructionPlane
        sketch = sketches.add(xy_plane)

        # Draw circle
        circles = sketch.sketchCurves.sketchCircles
        center = adsk.core.Point3D.create(0, 0, 0)
        circles.addByCenterRadius(center, radius)

        # Get profile and extrude
        profile = sketch.profiles.item(0)
        extrudes = root.features.extrudeFeatures

        ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(height)
        ext_input.setDistanceExtent(False, distance)

        ext = extrudes.add(ext_input)
        ext.bodies.item(0).name = name

        return {'success': True, 'object_id': name}

    def _create_sphere(self, request):
        """Create a sphere primitive."""
        params = request.get('params', {})
        radius = params.get('radius', 5) / 10  # mm to cm
        name = request.get('name', 'Sphere')

        design = self.app.activeProduct
        root = design.rootComponent

        # Create sphere using revolve
        sketches = root.sketches
        xy_plane = root.xYConstructionPlane
        sketch = sketches.add(xy_plane)

        # Draw semicircle
        arcs = sketch.sketchCurves.sketchArcs
        center = adsk.core.Point3D.create(0, 0, 0)
        arcs.addByCenterStartSweep(center, adsk.core.Point3D.create(radius, 0, 0), 3.14159)

        # Add line to close
        lines = sketch.sketchCurves.sketchLines
        lines.addByTwoPoints(adsk.core.Point3D.create(-radius, 0, 0), adsk.core.Point3D.create(radius, 0, 0))

        # Revolve
        profile = sketch.profiles.item(0)
        revolves = root.features.revolveFeatures

        rev_input = revolves.createInput(profile, sketch.sketchCurves.sketchLines.item(0),
                                          adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        angle = adsk.core.ValueInput.createByReal(6.28318)  # 360 degrees
        rev_input.setAngleExtent(False, angle)

        rev = revolves.add(rev_input)
        rev.bodies.item(0).name = name

        return {'success': True, 'object_id': name}

    def _create_cone(self, request):
        """Create a cone primitive."""
        params = request.get('params', {})
        radius1 = params.get('radius1', 5) / 10  # Bottom radius, mm to cm
        radius2 = params.get('radius2', 0) / 10  # Top radius, mm to cm (0 = apex)
        height = params.get('height', 10) / 10   # mm to cm
        name = request.get('name', 'Cone')

        design = self.app.activeProduct
        root = design.rootComponent

        # Create sketch
        sketches = root.sketches
        xy_plane = root.xYConstructionPlane
        sketch = sketches.add(xy_plane)

        # Draw circle for base
        circles = sketch.sketchCurves.sketchCircles
        center = adsk.core.Point3D.create(0, 0, 0)
        circles.addByCenterRadius(center, radius1)

        # Get profile and extrude with taper
        profile = sketch.profiles.item(0)
        extrudes = root.features.extrudeFeatures

        ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(height)

        # Calculate taper angle for the cone
        # Taper angle: if radius2 < radius1, we taper inward
        if radius1 > 0 and radius2 >= 0:
            # Taper angle in radians
            import math
            taper_angle = math.atan2(radius1 - radius2, height)
            ext_input.setDistanceExtent(False, distance)
            # Set taper angle
            ext_input.taperAngle = adsk.core.ValueInput.createByReal(taper_angle)
        else:
            ext_input.setDistanceExtent(False, distance)

        ext = extrudes.add(ext_input)
        ext.bodies.item(0).name = name

        return {'success': True, 'object_id': name}

    def _create_torus(self, request):
        """Create a torus primitive using revolve."""
        params = request.get('params', {})
        radius1 = params.get('radius1', 10) / 10  # Major radius (center to tube center), mm to cm
        radius2 = params.get('radius2', 2) / 10   # Minor radius (tube radius), mm to cm
        name = request.get('name', 'Torus')

        design = self.app.activeProduct
        root = design.rootComponent

        # Create sketch on XZ plane (so we can revolve around Z axis)
        sketches = root.sketches
        xz_plane = root.xZConstructionPlane
        sketch = sketches.add(xz_plane)

        # Draw circle for tube cross-section
        # Center of tube circle is at (radius1, 0) from torus center
        circles = sketch.sketchCurves.sketchCircles
        center = adsk.core.Point3D.create(radius1, 0, 0)  # XZ plane: X and Z axes
        circles.addByCenterRadius(center, radius2)

        # Add line along Z axis for revolve axis
        lines = sketch.sketchCurves.sketchLines
        lines.addByTwoPoints(
            adsk.core.Point3D.create(0, 0, -radius2),
            adsk.core.Point3D.create(0, 0, radius2)
        )

        # Get profile and revolve around Z axis
        profile = sketch.profiles.item(0)
        revolves = root.features.revolveFeatures

        # The axis line is the last line added
        axis_line = sketch.sketchCurves.sketchLines.item(sketch.sketchCurves.sketchLines.count - 1)

        rev_input = revolves.createInput(profile, axis_line,
                                          adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        angle = adsk.core.ValueInput.createByReal(6.28318)  # 360 degrees
        rev_input.setAngleExtent(False, angle)

        rev = revolves.add(rev_input)
        rev.bodies.item(0).name = name

        return {'success': True, 'object_id': name}

    def _boolean_union(self, request):
        """Boolean union operation using combine feature."""
        params = request.get('params', {})
        target_name = params.get('target')
        tool_names = params.get('tools', [])
        name = request.get('name', 'Fusion')

        design = self.app.activeProduct
        root = design.rootComponent

        # Get target body
        target_body = root.bRepBodies.itemByName(target_name)
        if not target_body:
            return {'success': False, 'error': f'Target body not found: {target_name}'}

        # Get tool bodies
        tool_bodies = adsk.core.ObjectCollection.create()
        for tool_name in tool_names:
            tool_body = root.bRepBodies.itemByName(tool_name)
            if not tool_body:
                return {'success': False, 'error': f'Tool body not found: {tool_name}'}
            tool_bodies.add(tool_body)

        # Create combine feature for union
        combines = root.features.combineFeatures
        combine_input = combines.createInput(target_body, tool_bodies)
        combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
        combine_input.isKeepToolBodies = False
        combine_input.isNewComponent = False

        combine = combines.add(combine_input)

        # Rename result
        if target_body:
            target_body.name = name

        return {'success': True, 'object_id': name}

    def _boolean_cut(self, request):
        """Boolean cut operation using combine feature."""
        params = request.get('params', {})
        target_name = params.get('target')
        tool_names = params.get('tools', [])
        name = request.get('name', 'Cut')

        design = self.app.activeProduct
        root = design.rootComponent

        # Get target body
        target_body = root.bRepBodies.itemByName(target_name)
        if not target_body:
            return {'success': False, 'error': f'Target body not found: {target_name}'}

        # Get tool bodies
        tool_bodies = adsk.core.ObjectCollection.create()
        for tool_name in tool_names:
            tool_body = root.bRepBodies.itemByName(tool_name)
            if not tool_body:
                return {'success': False, 'error': f'Tool body not found: {tool_name}'}
            tool_bodies.add(tool_body)

        # Create combine feature for cut
        combines = root.features.combineFeatures
        combine_input = combines.createInput(target_body, tool_bodies)
        combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        combine_input.isKeepToolBodies = False
        combine_input.isNewComponent = False

        combine = combines.add(combine_input)

        # Rename result
        if target_body:
            target_body.name = name

        return {'success': True, 'object_id': name}

    def _boolean_intersect(self, request):
        """Boolean intersection operation using combine feature."""
        params = request.get('params', {})
        target_name = params.get('target')
        tool_names = params.get('tools', [])
        name = request.get('name', 'Intersection')

        design = self.app.activeProduct
        root = design.rootComponent

        # Get target body
        target_body = root.bRepBodies.itemByName(target_name)
        if not target_body:
            return {'success': False, 'error': f'Target body not found: {target_name}'}

        # Get tool bodies
        tool_bodies = adsk.core.ObjectCollection.create()
        for tool_name in tool_names:
            tool_body = root.bRepBodies.itemByName(tool_name)
            if not tool_body:
                return {'success': False, 'error': f'Tool body not found: {tool_name}'}
            tool_bodies.add(tool_body)

        # Create combine feature for intersect
        combines = root.features.combineFeatures
        combine_input = combines.createInput(target_body, tool_bodies)
        combine_input.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation
        combine_input.isKeepToolBodies = False
        combine_input.isNewComponent = False

        combine = combines.add(combine_input)

        # Rename result
        if target_body:
            target_body.name = name

        return {'success': True, 'object_id': name}

    def _fillet(self, request):
        """Apply fillet to edges."""
        params = request.get('params', {})
        radius = params.get('radius', 1) / 10  # mm to cm

        design = self.app.activeProduct
        root = design.rootComponent

        # Get body by name
        body_name = params.get('body')
        body = root.bRepBodies.itemByName(body_name)

        if not body:
            return {'success': False, 'error': f'Body not found: {body_name}'}

        # Create fillet feature
        fillets = root.features.filletFeatures
        edge_collection = adsk.core.ObjectCollection.create()

        # Add all edges
        for edge in body.edges:
            edge_collection.add(edge)

        fillet_input = fillets.createInput()
        fillet_input.addConstantRadiusEdgeSet(edge_collection,
                                               adsk.core.ValueInput.createByReal(radius))

        fillet = fillets.add(fillet_input)
        return {'success': True, 'object_id': body_name}

    def _chamfer(self, request):
        """Apply chamfer to edges."""
        params = request.get('params', {})
        distance = params.get('distance', 1) / 10  # mm to cm

        design = self.app.activeProduct
        root = design.rootComponent

        body_name = params.get('body')
        body = root.bRepBodies.itemByName(body_name)

        if not body:
            return {'success': False, 'error': f'Body not found: {body_name}'}

        chamfers = root.features.chamferFeatures
        edge_collection = adsk.core.ObjectCollection.create()

        for edge in body.edges:
            edge_collection.add(edge)

        chamfer_input = chamfers.createInput(edge_collection, True)
        chamfer_input.setToEqualDistance(adsk.core.ValueInput.createByReal(distance))

        chamfer = chamfers.add(chamfer_input)
        return {'success': True, 'object_id': body_name}

    def _move(self, request):
        """Move a body."""
        params = request.get('params', {})
        translation = params.get('translation', [0, 0, 0])

        design = self.app.activeProduct
        root = design.rootComponent

        body_name = params.get('body')
        body = root.bRepBodies.itemByName(body_name)

        if not body:
            return {'success': False, 'error': f'Body not found: {body_name}'}

        # Create move feature
        moves = root.features.moveFeatures

        # Create transformation
        transform = adsk.core.Matrix3D.create()
        transform.translation = adsk.core.Vector3D.create(translation[0]/10,
                                                          translation[1]/10,
                                                          translation[2]/10)

        bodies = adsk.core.ObjectCollection.create()
        bodies.add(body)

        move_input = moves.createInput(bodies, transform)
        moves.add(move_input)

        return {'success': True}

    def _rotate(self, request):
        """Rotate a body using move feature."""
        params = request.get('params', {})
        axis = params.get('axis', [0, 0, 1])  # Default Z axis
        angle_deg = params.get('angle', 0)    # Angle in degrees
        origin = params.get('origin', [0, 0, 0])  # Rotation origin

        design = self.app.activeProduct
        root = design.rootComponent

        body_name = params.get('body')
        body = root.bRepBodies.itemByName(body_name)

        if not body:
            return {'success': False, 'error': f'Body not found: {body_name}'}

        # Create move feature with rotation
        moves = root.features.moveFeatures

        # Create transformation matrix with rotation
        transform = adsk.core.Matrix3D.create()

        # Convert angle to radians
        import math
        angle_rad = math.radians(angle_deg)

        # Normalize axis
        axis_vec = adsk.core.Vector3D.create(axis[0], axis[1], axis[2])
        axis_vec.normalize()

        # Set rotation on the transform
        # Rotation around an arbitrary axis through a point
        origin_point = adsk.core.Point3D.create(origin[0]/10, origin[1]/10, origin[2]/10)
        transform.setToRotation(angle_rad, axis_vec, origin_point)

        bodies = adsk.core.ObjectCollection.create()
        bodies.add(body)

        move_input = moves.createInput(bodies, transform)
        moves.add(move_input)

        return {'success': True}

    def _export(self, request):
        """Export the design."""
        format_type = request.get('format', 'step')
        filepath = request.get('filepath', 'output.step')

        design = self.app.activeProduct

        try:
            if format_type == 'step':
                # Export as STEP
                step_options = design.exportManager.createSTEPExportOptions(filepath)
                design.exportManager.execute(step_options)
            elif format_type == 'stl':
                # Export as STL
                stl_options = design.exportManager.createSTLExportOptions(design.rootComponent, filepath)
                design.exportManager.execute(stl_options)
            elif format_type == 'obj':
                # Export as OBJ
                obj_options = design.exportManager.createOBJExportOptions(filepath)
                design.exportManager.execute(obj_options)
            else:
                return {'success': False, 'error': f'Unknown format: {format_type}'}

            return {'success': True, 'filepath': filepath}

        except Exception as e:
            return {'success': False, 'error': str(e)}


# Global bridge instance
bridge = None

def run(context):
    """Run the add-in."""
    global bridge
    try:
        bridge = Fusion360Bridge()
        bridge.start()
    except:
        if bridge and bridge.ui:
            bridge.ui.messageBox('Failed to start CADStack Bridge:\n{}'.format(traceback.format_exc()))

def stop(context):
    """Stop the add-in."""
    global bridge
    try:
        if bridge:
            bridge.stop()
    except:
        if bridge and bridge.ui:
            bridge.ui.messageBox('Failed to stop CADStack Bridge:\n{}'.format(traceback.format_exc()))
