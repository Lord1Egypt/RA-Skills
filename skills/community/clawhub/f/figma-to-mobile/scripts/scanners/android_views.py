#!/usr/bin/env python3
"""
Custom View scanner for project_scan.

Scans Kotlin/Java source files to find custom View subclasses
that the project defines, so generated code can reference them.
"""

import re
from pathlib import Path


# Common Android View base classes that we want to detect subclasses of
VIEW_BASE_CLASSES = {
    "View", "ViewGroup",
    "TextView", "EditText", "Button", "ImageView", "ImageButton",
    "LinearLayout", "FrameLayout", "RelativeLayout", "ConstraintLayout",
    "ScrollView", "HorizontalScrollView", "NestedScrollView",
    "CardView", "MaterialCardView",
    "Switch", "SwitchCompat", "MaterialSwitch",
    "CheckBox", "RadioButton", "ToggleButton",
    "Toolbar", "AppBarLayout", "TabLayout",
    "ProgressBar", "SeekBar", "Slider", "WebView",
    "AppCompatTextView", "AppCompatImageView", "AppCompatButton",
    "AppCompatEditText", "AppCompatCheckBox",
}

# Classes that are NOT custom UI views — skip these even if they match heuristics
# (Adapters, ViewHolders, ItemDecorations, Dialogs, data models, listeners, etc.)
NON_VIEW_PATTERNS = {
    "Adapter", "ViewHolder", "ItemDecoration", "LayoutManager",
    "Listener", "Callback", "Observer", "Handler",
    "Model", "Entity", "Bean", "Data",
    "Fragment", "Activity", "Service", "Receiver",
}

# Parent classes that are NOT View bases — even if their name ends with a View suffix
# (e.g. RemoteImage is a data model, not android.widget.ImageView)
NON_VIEW_PARENT_NAMES = {
    "RemoteImage",
}

# Parent classes that indicate non-view inheritance
# (e.g. RecyclerView.Adapter shows up as just "RecyclerView" in simple regex)
NON_VIEW_PARENTS = {
    "RecyclerView",  # Almost always RecyclerView.Adapter/ViewHolder/ItemDecoration
}

# Directories to skip
SKIP_DIRS = {"build", ".gradle", ".idea", "test", "androidTest", "generated"}


def scan_custom_views(module_dir: Path) -> list[dict]:
    """
    Scan Kotlin/Java source files for custom View subclasses.
    
    Returns list of:
        {
            'name': 'CompactSwitchCompat',
            'parent': 'SwitchCompat',
            'package': 'com.example.widget',
            'file': 'src/main/java/.../CompactSwitchCompat.kt',
        }
    """
    views = []
    src_dir = module_dir / "src" / "main"
    if not src_dir.is_dir():
        return views
    
    for ext in ("*.kt", "*.java"):
        for source_file in src_dir.rglob(ext):
            if _should_skip(source_file):
                continue
            views.extend(_scan_file(source_file, module_dir))
    
    return views


def _scan_file(source_file: Path, module_dir: Path) -> list[dict]:
    """Scan a single source file for View subclasses."""
    results = []
    try:
        text = source_file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return results
    
    # Extract package
    pkg_match = re.search(r"^package\s+([\w.]+)", text, re.MULTILINE)
    package = pkg_match.group(1) if pkg_match else ""
    
    # Find class declarations that extend View-related classes
    # Kotlin: class MyView(...) : BaseView(...)
    # Java:   class MyView extends BaseView
    
    # Kotlin: class MyView(...) : ParentView(...)
    # Also handles: class MyView @JvmOverloads constructor(...) : View(...)
    # Skip data classes — they're never Views
    # The regex allows optional annotations + 'constructor' keyword between class name and params
    for match in re.finditer(
        r"(?<!data )class\s+(\w+)"
        r"(?:\s+(?:@\w+\s+)*constructor)?"
        r"(?:\s*(?:<[^>]*>)?\s*\([^)]*\))?"
        r"\s*:\s*([\w.]+)",
        text
    ):
        class_name = match.group(1)
        parent_full = match.group(2)  # Could be "RecyclerView.ViewHolder" or "SwitchCompat"
        parent_simple = parent_full.split(".")[-1]  # Last segment
        
        if _is_custom_view(class_name, parent_simple, parent_full):
            results.append({
                "name": class_name,
                "parent": parent_full,
                "package": package,
                "file": str(source_file.relative_to(module_dir)),
            })
    
    # Java: class MyView extends ParentView
    for match in re.finditer(
        r"class\s+(\w+)\s+extends\s+([\w.]+)",
        text
    ):
        class_name = match.group(1)
        parent_full = match.group(2)
        parent_simple = parent_full.split(".")[-1]
        
        if _is_custom_view(class_name, parent_simple, parent_full):
            results.append({
                "name": class_name,
                "parent": parent_full,
                "package": package,
                "file": str(source_file.relative_to(module_dir)),
            })
    
    return results


def _is_custom_view(class_name: str, parent_simple: str, parent_full: str) -> bool:
    """
    Determine if a class is a custom UI View worth reporting.
    
    Filters out Adapters, ViewHolders, ItemDecorations, Fragments, etc.
    """
    # Skip if class name matches non-view patterns
    for pattern in NON_VIEW_PATTERNS:
        if class_name.endswith(pattern) or pattern in class_name:
            return False
    
    # Skip if parent is in non-view parent list (e.g. RecyclerView)
    # Unless the class itself looks like a real View
    parent_first = parent_full.split(".")[0]
    if parent_first in NON_VIEW_PARENTS:
        return False
    
    # Accept if parent is a known View base class
    if parent_simple in VIEW_BASE_CLASSES:
        return True
    
    # Skip known non-view parents
    if parent_simple in NON_VIEW_PARENT_NAMES:
        return False
    
    # Accept if parent name looks like a View
    return _looks_like_view(parent_simple)


def _looks_like_view(name: str) -> bool:
    """Heuristic: class name ends with View/Layout/Button/etc."""
    view_suffixes = (
        "View", "Layout", "Button", "Text", "Image", "Switch",
        "Bar", "Card", "Picker", "Spinner",
    )
    return any(name.endswith(suffix) for suffix in view_suffixes)


def _should_skip(path: Path) -> bool:
    """Check if a file path should be skipped."""
    parts = path.parts
    return any(skip in parts for skip in SKIP_DIRS)
