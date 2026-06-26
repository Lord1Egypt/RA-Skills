#!/usr/bin/env python3
"""Scaffold a Blender add-on package for Blender 4.x and 5.x."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from textwrap import dedent


def normalize_module_name(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    if not value:
        raise ValueError("Module name cannot be empty after normalization.")
    return value


def parse_version(value: str) -> tuple[int, int, int]:
    parts = value.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ValueError(f"Invalid version '{value}'. Use MAJOR.MINOR.PATCH.")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def tuple_literal(values: tuple[int, int, int]) -> str:
    return f"({values[0]}, {values[1]}, {values[2]})"


def build_init_py(
    addon_name: str,
    module_name: str,
    author: str,
    description: str,
    category: str,
    addon_version: tuple[int, int, int],
    blender_min_version: tuple[int, int, int],
) -> str:
    return dedent(
        f'''\
        bl_info = {{
            "name": "{addon_name}",
            "author": "{author}",
            "version": {tuple_literal(addon_version)},
            "blender": {tuple_literal(blender_min_version)},
            "location": "View3D > Sidebar",
            "description": "{description}",
            "warning": "",
            "doc_url": "",
            "category": "{category}",
        }}

        import bpy

        from .operators import classes as operator_classes
        from .ui import classes as ui_classes

        classes = (*operator_classes, *ui_classes)


        def register():
            for cls in classes:
                bpy.utils.register_class(cls)


        def unregister():
            for cls in reversed(classes):
                bpy.utils.unregister_class(cls)


        if __name__ == "__main__":
            register()
        '''
    )


def build_compat_py() -> str:
    return dedent(
        '''\
        import bpy


        def blender_version():
            return bpy.app.version


        def is_blender_50_or_newer():
            return bpy.app.version >= (5, 0, 0)


        def active_asset(context):
            # Blender 4+ favors `context.asset`; fallback is kept for wider compatibility.
            return getattr(context, "asset", None) or getattr(context, "active_file", None)


        def eevee_engine_id():
            # Blender 5.0 uses BLENDER_EEVEE (EEVEE Next identifier was removed).
            return "BLENDER_EEVEE"
        '''
    )


def build_operators_py(module_name: str) -> str:
    class_prefix = "".join(part.capitalize() for part in module_name.split("_"))
    return dedent(
        f'''\
        import bpy

        from . import compat


        class {class_prefix}_OT_print_compat_info(bpy.types.Operator):
            bl_idname = "wm.{module_name}_print_compat_info"
            bl_label = "Print Compatibility Info"
            bl_options = {{"REGISTER", "UNDO"}}

            def execute(self, context):
                version = ".".join(str(v) for v in compat.blender_version())
                is_v5 = compat.is_blender_50_or_newer()
                asset = compat.active_asset(context)
                asset_name = getattr(asset, "name", "None")
                self.report(
                    {{"INFO"}},
                    f"Blender {{version}}, v5+={{is_v5}}, active asset={{asset_name}}",
                )
                return {{"FINISHED"}}


        classes = (
            {class_prefix}_OT_print_compat_info,
        )
        '''
    )


def build_ui_py(module_name: str, addon_name: str) -> str:
    class_prefix = "".join(part.capitalize() for part in module_name.split("_"))
    return dedent(
        f'''\
        import bpy


        class {class_prefix}_PT_panel(bpy.types.Panel):
            bl_label = "{addon_name}"
            bl_idname = "VIEW3D_PT_{module_name}_panel"
            bl_space_type = "VIEW_3D"
            bl_region_type = "UI"
            bl_category = "Tool"

            def draw(self, context):
                layout = self.layout
                layout.label(text="Blender 4/5 Compatible Add-on")
                layout.operator("wm.{module_name}_print_compat_info", icon="INFO")


        classes = (
            {class_prefix}_PT_panel,
        )
        '''
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Blender add-on skeleton compatible with Blender 4.x and 5.x."
    )
    parser.add_argument("--name", required=True, help="Human-friendly add-on name.")
    parser.add_argument("--module", help="Python package name. Defaults to normalized --name.")
    parser.add_argument("--author", default="Codex", help="Author field for bl_info.")
    parser.add_argument(
        "--description",
        default="Generated add-on scaffold with Blender 4/5 compatibility helpers.",
        help="Description field for bl_info.",
    )
    parser.add_argument("--category", default="Development", help="Category field for bl_info.")
    parser.add_argument("--version", default="0.1.0", help="Add-on version MAJOR.MINOR.PATCH.")
    parser.add_argument(
        "--blender-min",
        default="4.0.0",
        help="Minimum Blender version MAJOR.MINOR.PATCH for bl_info.",
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Directory where the add-on package folder will be created.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in an existing add-on directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    module_name = normalize_module_name(args.module or args.name)
    addon_version = parse_version(args.version)
    blender_min = parse_version(args.blender_min)

    base_dir = Path(args.output).expanduser().resolve()
    addon_dir = base_dir / module_name
    addon_dir.mkdir(parents=True, exist_ok=True)

    targets = [
        addon_dir / "__init__.py",
        addon_dir / "compat.py",
        addon_dir / "operators.py",
        addon_dir / "ui.py",
    ]

    if not args.force:
        existing = [path for path in targets if path.exists()]
        if existing:
            names = ", ".join(path.name for path in existing)
            raise FileExistsError(
                f"Refusing to overwrite existing files: {names}. Use --force to overwrite."
            )

    write_text(
        addon_dir / "__init__.py",
        build_init_py(
            addon_name=args.name,
            module_name=module_name,
            author=args.author,
            description=args.description,
            category=args.category,
            addon_version=addon_version,
            blender_min_version=blender_min,
        ),
    )
    write_text(addon_dir / "compat.py", build_compat_py())
    write_text(addon_dir / "operators.py", build_operators_py(module_name))
    write_text(addon_dir / "ui.py", build_ui_py(module_name, args.name))

    print(f"Generated Blender add-on scaffold at: {addon_dir}")
    print("Files: __init__.py, compat.py, operators.py, ui.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
