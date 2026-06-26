import json
import os
from typing import Dict, Any, List
from datetime import datetime

def export_gedcom(data: Dict[str, Any], output_file: str = "family_tree.ged"):
    """Exports extracted family data to a standard GEDCOM (.ged) file."""
    
    lines = [
        "0 HEAD",
        "1 SOUR genealogy-agent",
        "2 NAME Genealogy Agent by flobo3",
        "2 VERS 1.0",
        "1 DEST ANY",
        f"1 DATE {datetime.now().strftime('%d %b %Y').upper()}",
        "1 CHAR UTF-8",
    ]
    
    # Map our IDs to GEDCOM IDs (e.g., @I1@)
    id_map = {}
    gedcom_id_counter = 1
    
    # Write Individuals (INDI)
    for person in data.get("people", []):
        ged_id = f"@I{gedcom_id_counter}@"
        id_map[person["id"]] = ged_id
        gedcom_id_counter += 1
        
        lines.append(f"0 {ged_id} INDI")
        
        # Name
        name_parts = person["name"].split(" ", 1)
        first_name = name_parts[0]
        last_name = f"/{name_parts[1]}/" if len(name_parts) > 1 else ""
        lines.append(f"1 NAME {first_name} {last_name}")
        
        # Birth
        if person.get("birth_date") or person.get("birth_place"):
            lines.append("1 BIRT")
            if person.get("birth_date"):
                lines.append(f"2 DATE {person['birth_date']}")
            if person.get("birth_place"):
                lines.append(f"2 PLAC {person['birth_place']}")
                
        # Death
        if person.get("death_date"):
            lines.append("1 DEAT")
            lines.append(f"2 DATE {person['death_date']}")
            
        # Notes
        if person.get("notes"):
            lines.append(f"1 NOTE {person['notes']}")
            
    # Write Families (FAM)
    # Group relationships by parents to create families
    families = {}
    fam_id_counter = 1
    
    for rel in data.get("relationships", []):
        if rel["type"] == "parent":
            parent = rel["source_id"]
            child = rel["target_id"]
            
            # Find or create a family for this parent
            fam_id = None
            for fid, fam in families.items():
                if parent in fam["parents"]:
                    fam_id = fid
                    break
                    
            if not fam_id:
                fam_id = f"@F{fam_id_counter}@"
                families[fam_id] = {"parents": [parent], "children": []}
                fam_id_counter += 1
                
            if child not in families[fam_id]["children"]:
                families[fam_id]["children"].append(child)
                
        elif rel["type"] == "spouse":
            p1 = rel["source_id"]
            p2 = rel["target_id"]
            
            # Find or create a family for these spouses
            fam_id = None
            for fid, fam in families.items():
                if p1 in fam["parents"] or p2 in fam["parents"]:
                    fam_id = fid
                    if p1 not in fam["parents"]: fam["parents"].append(p1)
                    if p2 not in fam["parents"]: fam["parents"].append(p2)
                    break
                    
            if not fam_id:
                fam_id = f"@F{fam_id_counter}@"
                families[fam_id] = {"parents": [p1, p2], "children": []}
                fam_id_counter += 1
                
    # Write FAM records
    for fam_id, fam in families.items():
        lines.append(f"0 {fam_id} FAM")
        for parent in fam["parents"]:
            if parent in id_map:
                # In GEDCOM, HUSB is male parent, WIFE is female. We'll just use HUSB/WIFE arbitrarily for now.
                role = "HUSB" if fam["parents"].index(parent) == 0 else "WIFE"
                lines.append(f"1 {role} {id_map[parent]}")
        for child in fam["children"]:
            if child in id_map:
                lines.append(f"1 CHIL {id_map[child]}")
                
    # Link Individuals to Families
    for fam_id, fam in families.items():
        for parent in fam["parents"]:
            if parent in id_map:
                # Find the INDI record and append FAMS
                idx = lines.index(f"0 {id_map[parent]} INDI")
                lines.insert(idx + 1, f"1 FAMS {fam_id}")
        for child in fam["children"]:
            if child in id_map:
                # Find the INDI record and append FAMC
                idx = lines.index(f"0 {id_map[child]} INDI")
                lines.insert(idx + 1, f"1 FAMC {fam_id}")
                
    lines.append("0 TRLR")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"GEDCOM file saved to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "family_tree.ged"
        
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        export_gedcom(data, output_file)
    else:
        print("Usage: python export_gedcom.py input_data.json [output_tree.ged]")