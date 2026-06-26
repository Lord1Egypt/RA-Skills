#!/usr/bin/env python3
"""
Analyze a UI screenshot description and generate
a React / HTML+CSS implementation prompt.
"""
import sys, re

KNOWN_COMPONENTS = {
    r"(?i)button|btn": "Button",
    r"(?i)input|text.field|search": "Input",
    r"(?i)nav|menu|navbar|toolbar": "NavigationBar",
    r"(?i)card|panel|container": "Card",
    r"(?i)header|title.bar": "Header",
    r"(?i)footer|bottom": "Footer",
    r"(?i)list.item|row|table.row": "ListItem",
    r"(?i)form": "Form",
    r"(?i)modal|popup|dialog": "Modal",
    r"(?i)tab": "Tab",
    r"(?i)dropdown|select": "Dropdown",
    r"(?i)avatar|image|icon": "Image",
    r"(?i)text|label|paragraph": "Text",
    r"(?i)checkbox|toggle": "Checkbox",
    r"(?i)slider|range": "Slider",
}

def extract_components(description):
    found = []
    for pattern, component in KNOWN_COMPONENTS.items():
        if re.search(pattern, description):
            found.append(component)
    return list(dict.fromkeys(found))

def to_react_prompt(description, components):
    layout = "flex" if "flex" in description.lower() or "row" in description.lower() else "grid"
    component_list = ", ".join(components) if components else "div"

    prompt = f"""Generate a React functional component implementing this UI:

**Components detected:** {component_list}
**Layout:** {layout}-based

**Description:**
{description}

**Requirements:**
- Use TypeScript + Tailwind CSS
- Export as default functional component
- Include proper type definitions
- Handle basic state where needed (forms, toggles)
"""
    return prompt.strip()

if __name__ == "__main__":
    description = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    components = extract_components(description)
    print(to_react_prompt(description, components))