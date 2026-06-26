#!/usr/bin/env python3
"""Notes skill - AI handles all logic via SKILL.md"""
import os, json
SKILL_DIR = os.path.expanduser("~/.openclaw/skills/notes")
DATA_DIR   = os.path.expanduser("~/.openclaw/workspace/notes-data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")

def read(path):
    if os.path.exists(path):
        with open(path) as f: return json.load(f)
    return {"notes": []}

def write(path, data):
    with open(path, 'w') as f: json.dump(data, f, indent=2, ensure_ascii=False)

def path(file):
    return {
        "notes": f"{DATA_DIR}/notes.json",
    }[file]

def image_path(filename):
    return f"images/{filename}"

if __name__ == "__main__":
    print("按SKILL.md规则处理：记录/查询/更新/删除随笔，支持图片关联")
