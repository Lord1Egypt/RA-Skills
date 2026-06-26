# Blender Script Generation Patterns

## Operator Template

```python
import bpy


class EXAMPLE_OT_do_work(bpy.types.Operator):
    bl_idname = "wm.example_do_work"
    bl_label = "Do Work"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context is not None

    def execute(self, context):
        # Implement behavior here.
        self.report({"INFO"}, "Done")
        return {"FINISHED"}
```

## Panel Template

```python
import bpy


class EXAMPLE_PT_panel(bpy.types.Panel):
    bl_label = "Example"
    bl_idname = "VIEW3D_PT_example"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.example_do_work", icon="PLAY")
```

## Registration Template

```python
import bpy

classes = (
    EXAMPLE_OT_do_work,
    EXAMPLE_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```

## Compatibility Template

```python
import bpy


def is_blender_50_or_newer():
    return bpy.app.version >= (5, 0, 0)


def active_asset(context):
    return getattr(context, "asset", None) or getattr(context, "active_file", None)
```

## Script Quality Checklist

1. Use explicit imports and stable `bl_idname` values.
2. Keep compatibility code in helper functions.
3. Avoid removed Blender 4/5 APIs.
4. Keep `register()` and `unregister()` symmetric.
5. Guard context-dependent code in `poll()` and runtime checks.
