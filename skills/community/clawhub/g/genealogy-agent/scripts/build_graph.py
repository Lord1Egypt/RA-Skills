import json
import os
from typing import Dict, Any, List

def build_graph(data: Dict[str, Any], output_file: str = "family_graph.jsonl"):
    """Saves extracted family data into a local JSONL ontology graph."""
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        # Write people as nodes
        for person in data.get("people", []):
            node = {
                "type": "node",
                "id": person["id"],
                "label": "Person",
                "props": {
                    "name": person["name"],
                    "birth_date": person.get("birth_date"),
                    "death_date": person.get("death_date"),
                    "birth_place": person.get("birth_place"),
                    "notes": person.get("notes"),
                }
            }
            f.write(json.dumps(node, ensure_ascii=False) + "\n")
            
        # Write relationships as edges
        for rel in data.get("relationships", []):
            edge = {
                "type": "edge",
                "source": rel["source_id"],
                "target": rel["target_id"],
                "label": rel["type"],
                "props": {}
            }
            f.write(json.dumps(edge, ensure_ascii=False) + "\n")
            
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "family_graph.jsonl"
        
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        build_graph(data, output_file)
    else:
        print("Usage: python build_graph.py input_data.json [output_graph.jsonl]")