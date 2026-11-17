#!/usr/bin/env python3
"""
UI Design Specification Validation Script

Zero-dependency Python script that statically analyzes UI code for compliance
with selected design specifications.
Supports the three major spec systems: HIG / Fluent / Material.

Usage:
    python validate_ui.py --spec hig --file path/to/file.tsx
    python validate_ui.py --spec material --text "<div class='...'>..."
    python validate_ui.py --spec fluent --file path/to/file.css --check-color

Options:
    --spec          Spec: hig | fluent | material | all
    --file          File path
    --text          Pass code text directly
    --check-color   Enable color checking (skipped by default)
    --format        Output format: json | markdown (default json)
"""

import argparse
import json
import re
import sys
from pathlib import Path


# =============================================================================
# Spec Data
# =============================================================================

HIG_COLORS = {
    "systemBlue": ("#007AFF", "#0A84FF"),
    "systemGreen": ("#34C759", "#30D158"),
    "systemIndigo": ("#5856D6", "#5E5CE6"),
    "systemOrange": ("#FF9500", "#FF9F0A"),
    "systemPink": ("#FF2D55", "#FF375F"),
    "systemPurple": ("#AF52DE", "#BF5AF2"),
    "systemRed": ("#FF3B30", "#FF453A"),
    "systemTeal": ("#5AC8FA", "#64D2FF"),
    "systemYellow": ("#FFCC00", "#FFD60A"),
    "systemGray": ("#8E8E93", "#8E8E93"),
    "label": ("#000000", "#FFFFFF"),
    "secondaryLabel": ("#3C3C4399", "#EBEBF599"),
    "tertiaryLabel": ("#3C3C434D", "#EBEBF54D"),
    "systemBackground": ("#FFFFFF", "#000000"),
    "secondarySystemBackground": ("#F2F2F7", "#1C1C1E"),
    "tertiarySystemBackground": ("#FFFFFF", "#2C2C2E"),
    "separator": ("#C6C6C8", "#38383A"),
}

FLUENT_COLORS = {
    "brandBackground": ("#0078D4", "#0078D4"),
    "brandBackgroundHover": ("#006CBE", "#006CBE"),
    "neutralForeground1": ("#242424", "#FFFFFF"),
    "neutralForeground2": ("#424242", "#D6D6D6"),
    "neutralForeground3": ("#616161", "#ADADAD"),
    "neutralBackground1": ("#FFFFFF", "#292929"),
    "neutralBackground2": ("#FAFAFA", "#1F1F1F"),
    "neutralBackground3": ("#F5F5F5", "#141414"),
    "neutralStroke1": ("#D1D1D1", "#666666"),
    "neutralStroke2": ("#E0E0E0", "#525252"),
    "success": ("#107C10", "#54B054"),
    "warning": ("#FFC107", "#FDBA3B"),
    "error": ("#D13438", "#E9838A"),
    "info": ("#0099BC", "#60CDFF"),
}

MATERIAL_COLORS = {
    "primary": ("#6750A4", "#D0BCFF"),
    "onPrimary": ("#FFFFFF", "#381E72"),
    "primaryContainer": ("#EADDFF", "#4F378B"),
    "secondary": ("#625B71", "#CCC2DC"),
    "secondaryContainer": ("#E8DEF8", "#4A4458"),
    "tertiary": ("#7D5260", "#EFB8C8"),
    "surface": ("#FFFBFE", "#1C1B1F"),
    "onSurface": ("#1C1B1F", "#E6E1E5"),
    "surfaceVariant": ("#E7E0EC", "#49454F"),
    "background": ("#FFFBFE", "#1C1B1F"),
    "error": ("#B3261E", "#F2B8B5"),
    "onError": ("#FFFFFF", "#601410"),
    "outline": ("#79747E", "#938F99"),
    "outlineVariant": ("#CAC4D0", "#49454F"),
}

SPEC_FONTS = {
    "hig": ["SF Pro", "-apple-system", "BlinkMacSystemFont"],
    "fluent": ["Segoe UI", "Roboto", "Helvetica Neue"],
    "material": ["Roboto", "Noto Sans", "-apple-system"],
}

SPEC_SPACING = {
    "hig": [2, 4, 8, 12, 16, 20, 24, 32, 48, 64],
    "fluent": [0, 2, 4, 8, 12, 16, 20, 24, 32, 48],
    "material": [0, 4, 8, 12, 16, 24, 32, 48, 64],
}

SPEC_BORDER_RADIUS = {
    "hig": [8, 10, 13, 20, 27],
    "fluent": [0, 2, 4, 6, 8],
    "material": [0, 4, 8, 12, 16, 28],
}

SPEC_MIN_TOUCH = {
    "hig": 44,
    "fluent": 32,
    "material": 48,
}

# =============================================================================
# Parser
# =============================================================================

def parse_file(filepath):
    """Read file contents."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    return path.read_text(encoding="utf-8")

def extract_css_blocks(content):
    """Extract CSS blocks from HTML/JSX/Vue."""
    blocks = []
    # <style> tags
    blocks.extend(re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE))
    # CSS class definitions (simplified class selectors)
    blocks.extend(re.findall(r'\.([a-zA-Z_-][a-zA-Z0-9_-]*)\s*\{([^}]*)\}', content, re.DOTALL))
    # style attributes
    blocks.extend(re.findall(r'style="([^"]*)"', content, re.IGNORECASE))
    return blocks

def extract_inline_styles(content):
    """Extract all style attributes."""
    return re.findall(r'style="([^"]*)"', content, re.IGNORECASE)

def extract_classes(content):
    """Extract all class/className attributes."""
    classes = re.findall(r'className="([^"]*)"', content)
    classes.extend(re.findall(r'class="([^"]*)"', content))
    return classes

def extract_jsx_components(content):
    """Extract JSX component tags."""
    return re.findall(r'<([A-Z][a-zA-Z0-9]*)[^>]*>', content)

def extract_html_tags(content):
    """Extract HTML tags."""
    return re.findall(r'<([a-z][a-z0-9]*)[^>]*>', content, re.IGNORECASE)

# =============================================================================
# Validation Rules
# =============================================================================

def check_color(content, spec, line_map=None):
    """Check if color values are within the spec's range."""
    issues = []
    color_map = {
        "hig": HIG_COLORS,
        "fluent": FLUENT_COLORS,
        "material": MATERIAL_COLORS,
    }

    if spec not in color_map:
        return issues

    valid_colors = set()
    for light, dark in color_map[spec].values():
        valid_colors.add(light.lower())
        valid_colors.add(dark.lower())

    # Match color values
    color_pattern = re.compile(r'#([0-9A-Fa-f]{3,8})\b')

    for match in color_pattern.finditer(content):
        color = match.group(0).lower()
        # Ignore transparent colors
        if color in ('#00000000', '#fff0', '#0000', '#ffffff00'):
            continue
        # Expand shorthand to full form
        if len(color) == 4:
            color = '#' + ''.join(c * 2 for c in color[1:])

        if color not in valid_colors:
            line = content[:match.start()].count('\n') + 1
            issues.append({
                "type": "warn",
                "rule": "color-value",
                "message": f"Color {match.group(0)} is not in the {spec.upper()} default palette",
                "line": line,
            })

    return issues

def check_font(content, spec):
    """Check font usage."""
    issues = []
    expected_fonts = SPEC_FONTS.get(spec, [])

    # Match font-family
    font_pattern = re.compile(r'font-family\s*:\s*([^;}]*)', re.IGNORECASE)

    for match in font_pattern.finditer(content):
        fonts = match.group(1)
        # Check if expected fonts are included
        has_expected = any(ef.lower() in fonts.lower() for ef in expected_fonts)
        if not has_expected:
            line = content[:match.start()].count('\n') + 1
            issues.append({
                "type": "warn",
                "rule": "font-family",
                "message": f"Font '{fonts.strip()}' does not include {spec.upper()}-recommended fonts",
                "line": line,
            })

    return issues

def check_spacing(content, spec):
    """Check if spacing follows the grid."""
    issues = []
    valid_spacings = SPEC_SPACING.get(spec, [])

    # Match padding/margin/gap/width/height values
    spacing_pattern = re.compile(r'(padding|margin|gap|top|right|bottom|left)\s*:\s*(\d+)(pt|px|dp|rem|em)?', re.IGNORECASE)
    size_pattern = re.compile(r'(width|height)\s*:\s*(\d+)(pt|px|dp|rem|em)?', re.IGNORECASE)

    for pattern in [spacing_pattern, size_pattern]:
        for match in pattern.finditer(content):
            value = int(match.group(2))
            unit = (match.group(3) or 'px').lower()
            prop = match.group(1).lower()

            # Only check common units
            if unit not in ('pt', 'px', 'dp'):
                continue

            # Ignore 0 and large values
            if value == 0 or value > 128:
                continue

            # Check if in the spec spacing list (allow +-1 tolerance)
            is_valid = any(abs(value - vs) <= 1 for vs in valid_spacings)
            if not is_valid:
                line = content[:match.start()].count('\n') + 1
                issues.append({
                    "type": "warn",
                    "rule": "spacing-grid",
                    "message": f"{prop}: {value}{unit} is not in the {spec.upper()} recommended spacing values",
                    "line": line,
                })

    return issues

def check_border_radius(content, spec):
    """Check border radius values."""
    issues = []
    valid_radii = SPEC_BORDER_RADIUS.get(spec, [])

    radius_pattern = re.compile(r'border-radius\s*:\s*(\d+)(pt|px|dp|rem|em)?', re.IGNORECASE)

    for match in radius_pattern.finditer(content):
        value = int(match.group(1))
        unit = (match.group(2) or 'px').lower()

        if unit not in ('pt', 'px', 'dp'):
            continue

        # Ignore full rounded corners
        if value >= 999:
            continue

        is_valid = any(abs(value - vr) <= 1 for vr in valid_radii)
        if not is_valid:
            line = content[:match.start()].count('\n') + 1
            issues.append({
                "type": "warn",
                "rule": "border-radius",
                "message": f"border-radius: {value}{unit} is not in the {spec.upper()} recommended radius values",
                "line": line,
            })

    return issues

def check_shadow(content, spec):
    """Check shadow usage."""
    issues = []

    shadow_pattern = re.compile(r'box-shadow\s*:', re.IGNORECASE)
    shadow_count = len(shadow_pattern.findall(content))

    if spec == "hig":
        # HIG minimizes shadow usage
        if shadow_count > 0:
            issues.append({
                "type": "warn",
                "rule": "shadow-usage",
                "message": f"HIG recommends minimizing shadow usage; detected {shadow_count} box-shadow(s)",
                "line": 0,
            })

    elif spec == "fluent":
        # Fluent uses specific shadow tokens
        shadow_values = re.findall(r'box-shadow\s*:\s*([^;}]*)', content, re.IGNORECASE)
        for sv in shadow_values:
            # Check if standard shadow values are used
            if 'rgba(0,0,0,0.14)' not in sv and 'rgba(0, 0, 0, 0.14)' not in sv:
                issues.append({
                    "type": "warn",
                    "rule": "shadow-token",
                    "message": f"Fluent recommends using standard shadow tokens; non-standard shadow detected: {sv.strip()}",
                    "line": 0,
                })

    elif spec == "material":
        # Material uses elevation
        shadow_values = re.findall(r'box-shadow\s*:\s*([^;}]*)', content, re.IGNORECASE)
        for sv in shadow_values:
            # Check if Material standard shadow format is used
            if 'rgba(0,0,0,0.12)' not in sv and 'rgba(0, 0, 0, 0.12)' not in sv:
                issues.append({
                    "type": "warn",
                    "rule": "shadow-token",
                    "message": f"Material recommends using standard elevation shadows; non-standard shadow detected: {sv.strip()}",
                    "line": 0,
                })

    return issues

def check_touch_target(content, spec):
    """Check touch target size."""
    issues = []
    min_size = SPEC_MIN_TOUCH.get(spec, 44)

    # Match width/height on interactive elements
    # Simplified check: look for potentially small interactive elements
    small_pattern = re.compile(
        r'(width|height)\s*:\s*(\d+)(pt|px|dp)',
        re.IGNORECASE
    )

    found_sizes = {}
    for match in small_pattern.finditer(content):
        prop = match.group(1).lower()
        value = int(match.group(2))
        unit = match.group(3).lower()

        if value < min_size and value > 0:
            line = content[:match.start()].count('\n') + 1
            # Only report once per line
            if line not in found_sizes:
                found_sizes[line] = True
                issues.append({
                    "type": "error",
                    "rule": "touch-target",
                    "message": f"{prop}: {value}{unit} is smaller than {spec.upper()} minimum touch target of {min_size}{unit}",
                    "line": line,
                })

    return issues

def check_accessibility(content):
    """Check accessibility."""
    issues = []

    # Check aria-label
    interactive_tags = ['button', 'a', 'input', 'select', 'textarea']
    for tag in interactive_tags:
        pattern = re.compile(rf'<{tag}[^>]*>', re.IGNORECASE)
        for match in pattern.finditer(content):
            tag_str = match.group(0)
            if 'aria-label' not in tag_str and 'aria-labelledby' not in tag_str:
                # Check if there is text content
                if '>' in tag_str:
                    line = content[:match.start()].count('\n') + 1
                    issues.append({
                        "type": "warn",
                        "rule": "aria-label",
                        "message": f"<{tag}> element is missing aria-label or aria-labelledby",
                        "line": line,
                    })

    # Check focus styles
    if 'focus' not in content.lower() and ':focus' not in content.lower():
        issues.append({
            "type": "warn",
            "rule": "focus-style",
            "message": "No focus style definitions detected",
            "line": 0,
        })

    # Check disabled styles
    if 'disabled' not in content.lower() and ':disabled' not in content.lower():
        issues.append({
            "type": "warn",
            "rule": "disabled-style",
            "message": "No disabled style definitions detected",
            "line": 0,
        })

    return issues

def check_component_structure(content, spec):
    """Check component structure."""
    issues = []

    # Check Button structure
    if '<button' in content.lower() or 'Button' in content:
        # Check for text content or aria-label
        button_pattern = re.compile(r'<button[^>]*>(.*?)</button>', re.IGNORECASE | re.DOTALL)
        for match in button_pattern.finditer(content):
            inner = match.group(1).strip()
            if not inner and 'aria-label' not in match.group(0):
                line = content[:match.start()].count('\n') + 1
                issues.append({
                    "type": "error",
                    "rule": "button-content",
                    "message": "Button element lacks text content or aria-label",
                    "line": line,
                })

    # Check Input label association
    if '<input' in content.lower():
        input_pattern = re.compile(r'<input[^>]*>', re.IGNORECASE)
        for match in input_pattern.finditer(content):
            tag = match.group(0)
            has_id = 'id=' in tag
            has_aria = 'aria-label' in tag or 'aria-labelledby' in tag
            if not has_id and not has_aria:
                line = content[:match.start()].count('\n') + 1
                issues.append({
                    "type": "warn",
                    "rule": "input-label",
                    "message": "Input element is missing an id (cannot be associated with a label) or aria-label",
                    "line": line,
                })

    # Check Dialog focus management
    if 'dialog' in content.lower() or 'modal' in content.lower():
        if 'role="dialog"' not in content.lower() and 'role="alertdialog"' not in content.lower():
            issues.append({
                "type": "warn",
                "rule": "dialog-role",
                "message": "Dialog/Modal elements should have role='dialog'",
                "line": 0,
            })

    return issues

def check_token_naming(content, spec):
    """Check CSS variable / Tailwind class naming conventions."""
    issues = []

    # Check CSS variable naming
    css_var_pattern = re.compile(r'--([a-zA-Z0-9-]+)\s*:')

    if spec == "hig":
        expected_prefixes = ['color-', 'spacing-', 'radius-', 'font-']
    elif spec == "fluent":
        expected_prefixes = ['color-', 'spacing-', 'radius-', 'shadow-']
    elif spec == "material":
        expected_prefixes = ['md-', 'color-', 'elevation-']
    else:
        expected_prefixes = []

    for match in css_var_pattern.finditer(content):
        var_name = match.group(1)
        # Simple check: variable name too short
        if len(var_name) < 3:
            line = content[:match.start()].count('\n') + 1
            issues.append({
                "type": "warn",
                "rule": "token-naming",
                "message": f"CSS variable name '{var_name}' is too short; use semantic naming",
                "line": line,
            })

    return issues

# =============================================================================
# Main Validation Logic
# =============================================================================

def validate(content, spec, enable_color_check=False):
    """Run full validation."""
    issues = []

    # Color check (optional)
    if enable_color_check:
        issues.extend(check_color(content, spec))

    # Font check
    issues.extend(check_font(content, spec))

    # Spacing check
    issues.extend(check_spacing(content, spec))

    # Border radius check
    issues.extend(check_border_radius(content, spec))

    # Shadow check
    issues.extend(check_shadow(content, spec))

    # Touch target check
    issues.extend(check_touch_target(content, spec))

    # Accessibility check
    issues.extend(check_accessibility(content))

    # Component structure check
    issues.extend(check_component_structure(content, spec))

    # Token naming check
    issues.extend(check_token_naming(content, spec))

    return issues

def validate_all(content, check_color=False):
    """Run validation against all specs."""
    all_issues = {}
    for spec in ["hig", "fluent", "material"]:
        all_issues[spec] = validate(content, spec, check_color)
    return all_issues

def generate_report(issues, spec, format="json"):
    """Generate a validation report."""
    error_count = sum(1 for i in issues if i["type"] == "error")
    warn_count = sum(1 for i in issues if i["type"] == "warn")
    pass_count = max(0, 15 - error_count - warn_count)  # estimate

    if format == "json":
        return json.dumps({
            "spec": spec,
            "summary": {
                "pass": pass_count,
                "warn": warn_count,
                "error": error_count,
            },
            "issues": issues,
        }, ensure_ascii=False, indent=2)

    else:  # markdown
        lines = [
            f"# UI Design Specification Validation Report ({spec.upper()})",
            "",
            "## Summary",
            f"- Pass: {pass_count}",
            f"- Warning: {warn_count}",
            f"- Error: {error_count}",
            f"- Pass rate: {pass_count / max(1, pass_count + warn_count + error_count) * 100:.0f}%",
            "",
            "## Issues",
            "",
        ]

        if error_count > 0:
            lines.append("### Errors")
            for i, issue in enumerate(issues, 1):
                if issue["type"] == "error":
                    lines.append(f"{i}. **{issue['rule']}** (line {issue['line']})")
                    lines.append(f"   - {issue['message']}")
            lines.append("")

        if warn_count > 0:
            lines.append("### Warnings")
            for i, issue in enumerate(issues, 1):
                if issue["type"] == "warn":
                    lines.append(f"{i}. **{issue['rule']}** (line {issue['line']})")
                    lines.append(f"   - {issue['message']}")
            lines.append("")

        if error_count == 0 and warn_count == 0:
            lines.append("All checks passed!")

        return "\n".join(lines)

# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="UI Design Specification Validation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_ui.py --spec hig --file button.tsx
  python validate_ui.py --spec material --text "<button style='padding:8px'>Click</button>"
  python validate_ui.py --spec fluent --file styles.css --check-color --format markdown
        """
    )
    parser.add_argument("--spec", required=True, choices=["hig", "fluent", "material", "all"],
                        help="Select design specification")
    parser.add_argument("--file", help="Path to the file to validate")
    parser.add_argument("--text", help="Pass code text directly")
    parser.add_argument("--check-color", action="store_true",
                        help="Enable color checking (skipped by default)")
    parser.add_argument("--format", choices=["json", "markdown"], default="json",
                        help="Output format")

    args = parser.parse_args()

    # Get content
    if args.file:
        try:
            content = parse_file(args.file)
        except FileNotFoundError as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    elif args.text:
        content = args.text
    else:
        print(json.dumps({"error": "Please provide --file or --text"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    # Run validation
    if args.spec == "all":
        all_issues = validate_all(content, args.check_color)
        if args.format == "json":
            output = json.dumps(all_issues, ensure_ascii=False, indent=2)
        else:
            lines = ["# UI Design Specification Combined Validation Report", ""]
            for spec, issues in all_issues.items():
                lines.append(generate_report(issues, spec, "markdown"))
                lines.append("---")
            output = "\n".join(lines)
    else:
        issues = validate(content, args.spec, args.check_color)
        output = generate_report(issues, args.spec, args.format)

    print(output)

if __name__ == "__main__":
    main()
