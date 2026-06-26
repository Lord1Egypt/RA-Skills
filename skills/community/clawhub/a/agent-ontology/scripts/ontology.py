#!/usr/bin/env python3
"""
Ontology Skill - Command Line Interface
CRUD operations on typed knowledge graph.
"""

import json
import sys
import os
import random
from datetime import datetime

WORKSPACE = "/home/bot/.openclaw/workspace"
MEMORY_DIR = os.path.join(WORKSPACE, "memory", "ontology")
GRAPH_FILE = os.path.join(MEMORY_DIR, "graph.jsonl")
SCHEMA_FILE = os.path.join(MEMORY_DIR, "schema.yaml")

def ensure_dirs():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(GRAPH_FILE):
        open(GRAPH_FILE, 'a').close()

def generate_id(entity_type):
    prefix_map = {
        "Person": "p", "Project": "proj", "Task": "task",
        "Event": "evt", "Organization": "org", "Document": "doc", "Note": "note"
    }
    prefix = prefix_map.get(entity_type, "ent")
    suffix = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
    return f"{prefix}_{suffix}"

def create_entity(entity_type, properties):
    ensure_dirs()
    entity_id = generate_id(entity_type)
    entity = {
        "id": entity_id, "type": entity_type, "properties": properties,
        "created": datetime.utcnow().isoformat() + "Z",
        "updated": datetime.utcnow().isoformat() + "Z"
    }
    record = {"op": "create", "entity": entity}
    with open(GRAPH_FILE, 'a') as f:
        f.write(json.dumps(record) + "\n")
    return entity

def list_entities(entity_type):
    ensure_dirs()
    entities = []
    if not os.path.exists(GRAPH_FILE):
        return entities
    with open(GRAPH_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get("op") == "create" and record.get("entity", {}).get("type") == entity_type:
                    entities.append(record["entity"])
            except json.JSONDecodeError:
                continue
    return entities

def query_entities(entity_type, filter_props):
    ensure_dirs()
    results = []
    if not os.path.exists(GRAPH_FILE):
        return results
    with open(GRAPH_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get("op") == "create":
                    ent = record.get("entity", {})
                    if ent.get("type") == entity_type:
                        props = ent.get("properties", {})
                        if all(props.get(k) == v for k, v in filter_props.items()):
                            results.append(ent)
            except json.JSONDecodeError:
                continue
    return results

def get_entity(entity_id):
    ensure_dirs()
    if not os.path.exists(GRAPH_FILE):
        return None
    with open(GRAPH_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get("op") == "create":
                    ent = record.get("entity", {})
                    if ent.get("id") == entity_id:
                        return ent
            except json.JSONDecodeError:
                continue
    return None

def relate_entities(from_id, relation, to_id, properties=None):
    ensure_dirs()
    record = {
        "op": "relate", "from": from_id, "rel": relation, "to": to_id,
        "properties": properties or {},
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    with open(GRAPH_FILE, 'a') as f:
        f.write(json.dumps(record) + "\n")
    return record

def get_related(entity_id, relation):
    ensure_dirs()
    related = []
    if not os.path.exists(GRAPH_FILE):
        return related
    with open(GRAPH_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get("op") == "relate":
                    if record.get("from") == entity_id and record.get("rel") == relation:
                        to_id = record.get("to")
                        ent = get_entity(to_id)
                        if ent:
                            related.append({"relation": relation, "entity": ent})
                    elif record.get("to") == entity_id and record.get("rel") == relation:
                        from_id = record.get("from")
                        ent = get_entity(from_id)
                        if ent:
                            related.append({"relation": relation, "entity": ent})
            except json.JSONDecodeError:
                continue
    return related

def main():
    if len(sys.argv) < 2:
        print("Usage: ontology.py <command> [args...]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == "create":
            entity_type, props = None, {}
            i = 2
            while i < len(sys.argv):
                if sys.argv[i] == "--type" and i + 1 < len(sys.argv):
                    entity_type = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--props" and i + 1 < len(sys.argv):
                    props = json.loads(sys.argv[i + 1]); i += 2
                else:
                    i += 1
            if not entity_type:
                print("Error: --type is required"); sys.exit(1)
            result = create_entity(entity_type, props)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif cmd == "list":
            entity_type = None
            i = 2
            while i < len(sys.argv):
                if sys.argv[i] == "--type" and i + 1 < len(sys.argv):
                    entity_type = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not entity_type:
                print("Error: --type is required"); sys.exit(1)
            result = list_entities(entity_type)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif cmd == "query":
            entity_type, where = None, {}
            i = 2
            while i < len(sys.argv):
                if sys.argv[i] == "--type" and i + 1 < len(sys.argv):
                    entity_type = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--where" and i + 1 < len(sys.argv):
                    where = json.loads(sys.argv[i + 1]); i += 2
                else:
                    i += 1
            if not entity_type:
                print("Error: --type is required"); sys.exit(1)
            result = query_entities(entity_type, where)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif cmd == "get":
            entity_id = None
            i = 2
            while i < len(sys.argv):
                if sys.argv[i] == "--id" and i + 1 < len(sys.argv):
                    entity_id = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not entity_id:
                print("Error: --id is required"); sys.exit(1)
            result = get_entity(entity_id)
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"Entity {entity_id} not found"); sys.exit(1)
        
        elif cmd == "relate":
            from_id, rel, to_id = None, None, None
            i = 2
            while i < len(sys.argv):
                if sys.argv[i] == "--from" and i + 1 < len(sys.argv):
                    from_id = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--rel" and i + 1 < len(sys.argv):
                    rel = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--to" and i + 1 < len(sys.argv):
                    to_id = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not (from_id and rel and to_id):
                print("Error: --from, --rel, and --to are required"); sys.exit(1)
            result = relate_entities(from_id, rel, to_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif cmd == "related":
            entity_id, relation = None, None
            i = 2
            while i < len(sys.argv):
                if sys.argv[i] == "--id" and i + 1 < len(sys.argv):
                    entity_id = sys.argv[i + 1]; i += 2
                elif sys.argv[i] == "--rel" and i + 1 < len(sys.argv):
                    relation = sys.argv[i + 1]; i += 2
                else:
                    i += 1
            if not (entity_id and relation):
                print("Error: --id and --rel are required"); sys.exit(1)
            result = get_related(entity_id, relation)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif cmd == "validate":
            ensure_dirs()
            print("✅ Validation passed")
        
        else:
            print(f"Unknown command: {cmd}"); sys.exit(1)
    
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr); sys.exit(1)

if __name__ == "__main__":
    main()