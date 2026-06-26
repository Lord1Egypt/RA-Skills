import json
import os
import sys
from datetime import datetime

def generate_obsidian_vault(input_file: str, output_dir: str):
    """Generates an Obsidian-formatted vault from extracted family data."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    people = {p['id']: p for p in data.get('people', [])}
    relationships = data.get('relationships', [])

    # Build relationship maps
    parents_map = {p_id: [] for p_id in people}
    children_map = {p_id: [] for p_id in people}
    spouses_map = {p_id: [] for p_id in people}

    for rel in relationships:
        src = rel['source_id']
        tgt = rel['target_id']
        rtype = rel['type'].lower()

        if rtype == 'parent':
            if tgt in children_map and src in parents_map:
                children_map[src].append(tgt)
                parents_map[tgt].append(src)
        elif rtype == 'child':
            if tgt in parents_map and src in children_map:
                parents_map[src].append(tgt)
                children_map[tgt].append(src)
        elif rtype == 'spouse':
            if tgt in spouses_map and src in spouses_map:
                spouses_map[src].append(tgt)
                spouses_map[tgt].append(src)

    today = datetime.now().strftime("%Y-%m-%d")

    for p_id, person in people.items():
        name = person.get('name', 'Unknown')
        b_date = person.get('birth_date', '')
        b_place = person.get('birth_place', '')
        d_date = person.get('death_date', '')
        d_place = person.get('death_place', '')
        notes = person.get('notes', '')

        # Resolve relationships
        parents = [f"[[{people[pid]['name']}]]" for pid in parents_map.get(p_id, []) if pid in people]
        father = parents[0] if len(parents) > 0 else ""
        mother = parents[1] if len(parents) > 1 else ""
        
        spouses = [f"[[{people[sid]['name']}]]" for sid in spouses_map.get(p_id, []) if sid in people]
        spouse_str = spouses[0] if spouses else ""

        children = [f"\"{people[cid]['name']}\"" for cid in children_map.get(p_id, []) if cid in people]
        children_yaml = "\n  - ".join([""] + children) if children else " []"

        md_content = f"""---
full_name: "{name}"
birth_date: "{b_date}"
birth_place: "{b_place}"
death_date: "{d_date}"
death_place: "{d_place}"
father: "{father}"
mother: "{mother}"
spouse: "{spouse_str}"
children:{children_yaml}
confidence: "Moderate Signal"
sources: []
open_questions: []
last_updated: "{today}"
---

# {name}

## Life Events

| Event | Date | Place | Source |
|-------|------|-------|--------|
| Birth | {b_date} | {b_place} | |
| Marriage | | | |
| Death | {d_date} | {d_place} | |

## Sources

1. 

## Open Questions

- [ ] 

## Notes

{notes}
"""
        safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).rstrip()
        file_path = os.path.join(output_dir, f"{safe_name}.md")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

    print(f"Successfully generated {len(people)} Obsidian markdown files in '{output_dir}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_obsidian.py <input_json_file> <output_directory>")
        sys.exit(1)
    
    generate_obsidian_vault(sys.argv[1], sys.argv[2])
