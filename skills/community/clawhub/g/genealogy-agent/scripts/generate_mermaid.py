import json
import os
from typing import Dict, Any, List

def generate_mermaid(data: Dict[str, Any], output_file: str = "family_tree.md"):
    """Generates a Mermaid diagram from extracted family data."""
    
    mermaid_lines = [
        "```mermaid",
        "graph TD",
        "%% Family Tree Diagram",
    ]
    
    # Add nodes
    for person in data.get("people", []):
        node_id = person["id"]
        name = person["name"]
        birth = person.get("birth_date", "")
        death = person.get("death_date", "")
        
        label = f"{name}"
        if birth or death:
            label += f"<br>({birth} - {death})"
            
        mermaid_lines.append(f'    {node_id}["{label}"]')
        
    # Add edges
    for rel in data.get("relationships", []):
        source = rel["source_id"]
        target = rel["target_id"]
        rel_type = rel["type"]
        
        if rel_type == "parent":
            mermaid_lines.append(f'    {source} -->|parent| {target}')
        elif rel_type == "child":
            mermaid_lines.append(f'    {target} -->|parent| {source}')
        elif rel_type == "spouse":
            mermaid_lines.append(f'    {source} ---|spouse| {target}')
        elif rel_type == "sibling":
            mermaid_lines.append(f'    {source} -.-|sibling| {target}')
            
    mermaid_lines.append("```")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(mermaid_lines))
        
    print(f"Mermaid diagram saved to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "family_tree.md"
        
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        generate_mermaid(data, output_file)
    else:
        print("Usage: python generate_mermaid.py input_data.json [output_tree.md]")