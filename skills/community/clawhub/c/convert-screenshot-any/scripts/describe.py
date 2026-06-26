#!/usr/bin/env python3
"""
Extract UI elements from a screenshot description and generate
a detailed AI image generation prompt.
"""
import sys, os, re

def extract_ui_prompt(description):
    """Generate a prompt from a textual description of a UI screenshot."""
    if not description or len(description.strip()) < 5:
        print("ERROR: Please provide a description of the screenshot")
        sys.exit(1)

    lines = [l.strip() for l in description.split("\n") if l.strip()]

    elements = []
    colors = []
    layout = "unknown"

    for line in lines:
        low = line.lower()
        if any(k in low for k in ["button", "btn", "click"]):
            elements.append("button")
        if any(k in low for k in ["nav", "menu", "sidebar"]):
            elements.append("navigation bar")
        if any(k in low for k in ["input", "field", "text box"]):
            elements.append("input field")
        if any(k in low for k in ["card", "box", "panel"]):
            elements.append("card container")
        if any(k in low for k in ["header", "title", "heading"]):
            elements.append("header section")
        if any(k in low for k in ["blue", "red", "green", "dark", "light", "white", "black"]):
            colors.append(line)
        if any(k in low for k in ["grid", "list", "stacked", "column", "row"]):
            layout = line

    style = description[:200]

    prompt = f"""A clean {layout} UI design with {', '.join(elements[:5])} if elements else 'modern interface elements'}, {style}"""
    return prompt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        description = sys.stdin.read()
    else:
        with open(sys.argv[1]) as f:
            description = f.read()

    print(extract_ui_prompt(description))