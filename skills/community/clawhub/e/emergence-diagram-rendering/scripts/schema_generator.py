import json
import sys

def generate_mermaid_flowchart(data):
    """
    input: {"nodes": [{"id": "A", "label": "Start"}, ...], "edges": [{"from": "A", "to": "B", "label": "Next"}]}
    output: graph TD; ...
    """
    lines = ["graph TD"]
    for node in data.get("nodes", []):
        label = node.get("label", node["id"])
        # Handle different shapes
        shape = node.get("shape", "round")
        if shape == "diamond":
            lines.append(f'    {node["id"]}{{{label}}}')
        elif shape == "square":
            lines.append(f'    {node["id"]}[{label}]')
        else:
            lines.append(f'    {node["id"]}({label})')
            
    for edge in data.get("edges", []):
        label = edge.get("label", "")
        if label:
            lines.append(f'    {edge["from"]} -->|{label}| {edge["to"]}')
        else:
            lines.append(f'    {edge["from"]} --> {edge["to"]}')
            
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generator.py <json_string>")
        sys.exit(1)
        
    try:
        data = json.loads(sys.argv[1])
        print(generate_mermaid_flowchart(data))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
