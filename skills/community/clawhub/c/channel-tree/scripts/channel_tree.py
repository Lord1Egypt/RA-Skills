#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
频道层级管理系统
殿堂 → 宇宙 → 世界 → 森林 → 树 → 频道

用法:
  python3 channel_tree.py create hall <name>
  python3 channel_tree.py create universe <name> [hall_id]
  python3 channel_tree.py create world <name> [universe_id]
  python3 channel_tree.py create forest <name> [world_id]
  python3 channel_tree.py create tree <name> [forest_id]
  python3 channel_tree.py create channel <type> <name> [parent_id]
  
  python3 channel_tree.py list [hall_id|universe_id|world_id|forest_id|tree_id]
  python3 channel_tree.py switch <path>
  python3 channel_tree.py monitor
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/root/.openclaw/workspace/channel_tree")
BASE_DIR.mkdir(exist_ok=True)

STATE_FILE = BASE_DIR / "universe.json"

# 当前上下文
CURRENT_HALL = os.environ.get("CHANNEL_TREE_HALL", "default")
CURRENT_UNIVERSE = os.environ.get("CHANNEL_TREE_UNIVERSE", "default")
CURRENT_WORLD = os.environ.get("CHANNEL_TREE_WORLD", "default")
CURRENT_FOREST = os.environ.get("CHANNEL_TREE_FOREST", "default")
CURRENT_TREE = os.environ.get("CHANNEL_TREE_SESSION", "default")

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"version": "2.0.0", "halls": {}}

def save_state(data):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_or_create(data, path, creator_fn):
    """通用路径获取/创建"""
    current = data
    for key in path[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    last_key = path[-1]
    if last_key not in current:
        current[last_key] = creator_fn()
    return current[last_key]

def create_hall(name):
    """创建殿堂"""
    data = load_state()
    hall_id = name.lower().replace(" ", "-")
    if hall_id not in data["halls"]:
        data["halls"][hall_id] = {
            "id": hall_id,
            "name": name,
            "universes": {},
            "created": datetime.now().astimezone().isoformat()
        }
    save_state(data)
    print(f"✅ 殿堂已创建: {hall_id}")
    print(f"   名称: {name}")
    return hall_id

def create_universe(name, hall_id=None):
    """创建宇宙"""
    data = load_state()
    hall_id = hall_id or CURRENT_HALL
    hall = data["halls"].get(hall_id)
    if not hall:
        print(f"殿堂 {hall_id} 不存在")
        return None
    universe_id = name.lower().replace(" ", "-")
    if universe_id not in hall["universes"]:
        hall["universes"][universe_id] = {
            "id": universe_id,
            "name": name,
            "worlds": {},
            "created": datetime.now().astimezone().isoformat()
        }
    save_state(data)
    print(f"✅ 宇宙已创建: {universe_id}")
    print(f"   殿堂: {hall_id} → {hall['name']}")
    print(f"   名称: {name}")
    return universe_id

def create_world(name, universe_id=None):
    """创建世界"""
    data = load_state()
    universe_id = universe_id or CURRENT_UNIVERSE
    for hall_id, hall in data["halls"].items():
        if universe_id in hall["universes"]:
            universe = hall["universes"][universe_id]
            world_id = name.lower().replace(" ", "-")
            if world_id not in universe["worlds"]:
                universe["worlds"][world_id] = {
                    "id": world_id,
                    "name": name,
                    "forests": {},
                    "created": datetime.now().astimezone().isoformat()
                }
            save_state(data)
            print(f"✅ 世界已创建: {world_id}")
            print(f"   宇宙: {universe_id}")
            print(f"   名称: {name}")
            return world_id
    print(f"宇宙 {universe_id} 不存在")
    return None

def create_forest(name, world_id=None):
    """创建森林"""
    data = load_state()
    world_id = world_id or CURRENT_WORLD
    for hall in data["halls"].values():
        for universe in hall["universes"].values():
            if world_id in universe["worlds"]:
                world = universe["worlds"][world_id]
                forest_id = name.lower().replace(" ", "-")
                if forest_id not in world["forests"]:
                    world["forests"][forest_id] = {
                        "id": forest_id,
                        "name": name,
                        "trees": {},
                        "created": datetime.now().astimezone().isoformat()
                    }
                save_state(data)
                print(f"✅ 森林已创建: {forest_id}")
                print(f"   世界: {world_id}")
                print(f"   名称: {name}")
                return forest_id
    print(f"世界 {world_id} 不存在")
    return None

def create_tree(name, forest_id=None):
    """创建树"""
    data = load_state()
    forest_id = forest_id or CURRENT_FOREST
    for hall in data["halls"].values():
        for universe in hall["universes"].values():
            for world in universe["worlds"].values():
                if forest_id in world["forests"]:
                    forest = world["forests"][forest_id]
                    tree_id = name.lower().replace(" ", "-")
                    if tree_id not in forest["trees"]:
                        forest["trees"][tree_id] = {
                            "id": tree_id,
                            "name": name,
                            "root": {
                                "id": "root",
                                "type": "root",
                                "name": "主会话",
                                "created": datetime.now().astimezone().isoformat(),
                                "last_active": datetime.now().astimezone().isoformat(),
                                "status": "active",
                                "children": [],
                                "metadata": {
                                    "inheritance_L1": ["identity", "core_memory"],
                                    "inheritance_L2": ["preferences", "current_project"]
                                }
                            },
                            "channels": {}
                        }
                    save_state(data)
                    print(f"✅ 树已创建: {tree_id}")
                    print(f"   森林: {forest_id}")
                    print(f"   名称: {name}")
                    return tree_id
    print(f"森林 {forest_id} 不存在")
    return None

def create_channel(channel_type, name, parent_id="root"):
    """创建频道"""
    data = load_state()
    tree_id = CURRENT_TREE
    
    for hall in data["halls"].values():
        for universe in hall["universes"].values():
            for world in universe["worlds"].values():
                for forest in world["forests"].values():
                    if tree_id in forest["trees"]:
                        tree = forest["trees"][tree_id]
                        
                        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                        prefix_map = {"task": "TASK", "qa": "QA", "branch": "BRANCH"}
                        prefix = prefix_map.get(channel_type, "CHAN")
                        same_type = sum(1 for c in tree["channels"].values() if c.get("type") == channel_type)
                        channel_id = f"{prefix}-{timestamp}-{same_type + 1:02d}"
                        
                        if parent_id == "root":
                            path = ["root"]
                        elif parent_id in tree["channels"]:
                            parent = tree["channels"][parent_id]
                            path = parent.get("path", ["root"]) + [parent_id]
                        else:
                            path = ["root"]
                        
                        channel = {
                            "id": channel_id,
                            "type": channel_type,
                            "name": name,
                            "parent_id": parent_id,
                            "path": path,
                            "created": datetime.now().astimezone().isoformat(),
                            "last_active": datetime.now().astimezone().isoformat(),
                            "status": "active",
                            "inheritance": {
                                "L1": tree["root"]["metadata"]["inheritance_L1"],
                                "L2": tree["root"]["metadata"]["inheritance_L2"],
                                "L3": []
                            },
                            "children": []
                        }
                        
                        tree["channels"][channel_id] = channel
                        if parent_id == "root":
                            tree["root"]["children"].append(channel_id)
                        else:
                            tree["channels"][parent_id]["children"].append(channel_id)
                        
                        save_state(data)
                        print(f"✅ 频道已创建: {channel_id}")
                        print(f"   路径: {hall['id']} → {universe['id']} → {world['id']} → {forest['id']} → {tree_id}")
                        print(f"   类型: {channel_type}")
                        print(f"   名称: {name}")
                        return channel_id
    print(f"树 {tree_id} 不存在")
    return None

def list_all(target_id=None):
    """列出层级"""
    data = load_state()
    
    if not target_id:
        print("\n🏛️ 殿堂全貌")
        print("=" * 60)
        if not data["halls"]:
            print("   (空)")
            return
        for hall_id, hall in data["halls"].items():
            uni_count = len(hall["universes"])
            print(f"\n🏛️ {hall['name']} ({hall_id})")
            print(f"   宇宙: {uni_count}")
            for uni_id, uni in hall["universes"].items():
                print(f"   🌌 {uni['name']} ({uni_id})")
                for world_id, world in uni["worlds"].items():
                    print(f"      🌍 {world['name']} ({world_id})")
                    for forest_id, forest in world["forests"].items():
                        print(f"         🌲 {forest['name']} ({forest_id})")
                        for tree_id, tree in forest["trees"].items():
                            ch_count = len(tree["channels"])
                            print(f"            📁 {tree_id}: {tree['name']} ({ch_count}频道)")
    else:
        # 精确查找
        parts = target_id.split("/")
        if len(parts) == 1:
            # Hall
            if parts[0] in data["halls"]:
                hall = data["halls"][parts[0]]
                print(f"\n🏛️ 殿堂: {hall['name']} ({parts[0]})")
                for uni_id, uni in hall["universes"].items():
                    print(f"   🌌 {uni['name']} ({uni_id})")

def switch_path(path_str):
    """切换路径"""
    parts = path_str.split("/")
    if len(parts) >= 1:
        os.environ["CHANNEL_TREE_HALL"] = parts[0]
    if len(parts) >= 2:
        os.environ["CHANNEL_TREE_UNIVERSE"] = parts[1]
    if len(parts) >= 3:
        os.environ["CHANNEL_TREE_WORLD"] = parts[2]
    if len(parts) >= 4:
        os.environ["CHANNEL_TREE_FOREST"] = parts[3]
    if len(parts) >= 5:
        os.environ["CHANNEL_TREE_SESSION"] = parts[4]
    print(f"✅ 已切换: {path_str}")
    show_context()

def show_context():
    """显示当前上下文"""
    print(f"\n📍 当前上下文:")
    print(f"   殿堂: {CURRENT_HALL}")
    print(f"   宇宙: {CURRENT_UNIVERSE}")
    print(f"   世界: {CURRENT_WORLD}")
    print(f"   森林: {CURRENT_FOREST}")
    print(f"   树: {CURRENT_TREE}")

def monitor():
    """监控"""
    data = load_state()
    print("\n🔭 殿堂监控")
    print("=" * 60)
    if not data["halls"]:
        print("   (空)")
        return
    
    total_halls = len(data["halls"])
    total_unis = sum(len(h["universes"]) for h in data["halls"].values())
    total_worlds = sum(len(u["worlds"]) for h in data["halls"].values() for u in h["universes"].values())
    total_forests = sum(len(w["forests"]) for h in data["halls"].values() 
                       for u in h["universes"].values() for w in u["worlds"].values())
    total_trees = sum(len(f["trees"]) for h in data["halls"].values() 
                      for u in h["universes"].values() for w in u["worlds"].values()
                      for f in w["forests"].values())
    total_channels = sum(len(t["channels"]) for h in data["halls"].values() 
                        for u in h["universes"].values() for w in u["worlds"].values()
                        for f in w["forests"].values() for t in f["trees"].values())
    
    print(f"总计: {total_halls}殿堂 | {total_unis}宇宙 | {total_worlds}世界 | {total_forests}森林 | {total_trees}树 | {total_channels}频道")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        show_context()
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "create":
        if len(sys.argv) < 3:
            print("用法: create <hall|universe|world|forest|tree|channel> ...")
            sys.exit(1)
        sub = sys.argv[2]
        
        if sub == "hall":
            if len(sys.argv) < 4:
                print("用法: create hall <name>")
                sys.exit(1)
            create_hall(sys.argv[3])
        elif sub == "universe":
            create_universe(sys.argv[3] if len(sys.argv) > 3 else "default",
                          sys.argv[4] if len(sys.argv) > 4 else None)
        elif sub == "world":
            create_world(sys.argv[3] if len(sys.argv) > 3 else "default",
                        sys.argv[4] if len(sys.argv) > 4 else None)
        elif sub == "forest":
            create_forest(sys.argv[3] if len(sys.argv) > 3 else "default",
                         sys.argv[4] if len(sys.argv) > 4 else None)
        elif sub == "tree":
            create_tree(sys.argv[3] if len(sys.argv) > 3 else "default",
                       sys.argv[4] if len(sys.argv) > 4 else None)
        elif sub == "channel":
            if len(sys.argv) < 5:
                print("用法: create channel <type> <name> [parent_id]")
                sys.exit(1)
            create_channel(sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "root")
        else:
            print(f"未知: {sub}")
    
    elif cmd == "list":
        list_all(sys.argv[2] if len(sys.argv) > 2 else None)
    
    elif cmd == "switch":
        if len(sys.argv) < 3:
            print("用法: switch <hall[/universe[/world[/forest[/tree]]]]>")
            sys.exit(1)
        switch_path(sys.argv[2])
    
    elif cmd == "context":
        show_context()
    
    elif cmd == "monitor":
        monitor()
    
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
