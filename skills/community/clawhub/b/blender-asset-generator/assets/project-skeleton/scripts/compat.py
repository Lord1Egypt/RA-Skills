# pyright: reportMissingImports=false
import math
from typing import Sequence

import bpy  # type: ignore
from mathutils import Vector  # type: ignore


def blender_version_string() -> str:
    # Example: "5.0.1"
    return getattr(bpy.app, "version_string", "unknown")


def set_render_engine_best_effort() -> str:
    scene = bpy.context.scene
    engines = scene.render.bl_rna.properties["engine"].enum_items
    available = {e.identifier for e in engines}

    if "BLENDER_EEVEE_NEXT" in available:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    elif "BLENDER_EEVEE" in available:
        scene.render.engine = "BLENDER_EEVEE"
    else:
        scene.render.engine = "CYCLES"

    return scene.render.engine


def enable_auto_smooth_best_effort(obj, angle_deg: float = 30.0) -> None:
    mesh = getattr(obj, "data", None)
    if mesh is None:
        return

    if hasattr(mesh, "use_auto_smooth"):
        mesh.use_auto_smooth = True
        if hasattr(mesh, "auto_smooth_angle"):
            mesh.auto_smooth_angle = math.radians(angle_deg)
        return

    # Some versions expose an operator.
    if hasattr(bpy.ops.object, "shade_auto_smooth"):
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_auto_smooth(angle=math.radians(angle_deg))


def look_at(cam_obj, target_xyz: Sequence[float]) -> None:
    target = Vector(
        (
            float(target_xyz[0]),
            float(target_xyz[1]),
            float(target_xyz[2]),
        )
    )
    direction = target - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def export_glb(filepath: str) -> None:
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format="GLB",
        export_apply=True,
    )


def export_fbx(filepath: str) -> None:
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        apply_unit_scale=True,
        bake_space_transform=True,
        axis_forward="-Z",
        axis_up="Y",
    )


def export_usd_best_effort(filepath: str) -> None:
    # USD export operator name can vary; prefer bpy.ops.wm.usd_export.
    if hasattr(bpy.ops.wm, "usd_export"):
        bpy.ops.wm.usd_export(filepath=filepath)
        return

    # Fallback: older builds may register under export_scene.
    if hasattr(bpy.ops, "export_scene") and hasattr(
        bpy.ops.export_scene, "usd"
    ):
        bpy.ops.export_scene.usd(filepath=filepath)
        return

    raise RuntimeError(
        "USD export is not available in this Blender build."
    )
