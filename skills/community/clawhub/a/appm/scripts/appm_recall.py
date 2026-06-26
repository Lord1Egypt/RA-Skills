import json
import os

REGISTRY_PATH = os.path.expanduser('~/.openclaw/workspace/data/appm_registry.json')

def get_project_brief(path):
    snapshot_path = os.path.join(path, ".openclaw/SNAPSHOT.md")
    brief = {"path": path, "name": "未知專案", "version": "N/A", "next_move": "無資料"}
    
    if os.path.exists(snapshot_path):
        with open(snapshot_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if "版本" in line or "**版本**" in line:
                    brief["version"] = line.split(":")[-1].strip().replace("*", "")
                if "下一步" in line or "**下一步**" in line:
                    idx = lines.index(line)
                    for next_line in lines[idx+1:]:
                        if next_line.strip().startswith("- [ ]") or next_line.strip().startswith("1.") or next_line.strip().startswith("- **"):
                            brief["next_move"] = next_line.strip()
                            break
    return brief

def recall():
    if not os.path.exists(REGISTRY_PATH):
        print("No registry found.")
        return

    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    print("\n[APPM 活躍專案彙報]")
    for p in registry['projects'][:3]:
        brief = get_project_brief(p['path'])
        print(f"- 專案: {p['name']} (權重: {p['weight']})")
        print(f"  版本: {brief['version']}")
        print(f"  下一步: {brief['next_move']}")
        print(f"  路徑: {p['path']}")

if __name__ == "__main__":
    recall()
