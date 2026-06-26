#!/usr/bin/env python3
"""EvoMind CLI — five-layer memory engine for AI agents."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from memory_core import MemoryCore

def main():
    mem = MemoryCore()

    if len(sys.argv) < 2:
        print("EvoMind v1.1.2 — Five-Layer Memory Engine")
        print()
        print("Commands:")
        print("  remember <text>           Store a fact in L1")
        print("  forget <id>               Delete a L1 entry by ID")
        print("  forget-all                Delete ALL L1 entries (careful!)")
        print("  recall <query>            Search across all layers (L5 FTS)")
        print("  recall-l1                 List all L1 entries")
        print("  skill-save <name> <file>  Save a skill to L2")
        print("  skill-load <name>         Load a skill from L2")
        print("  skill-list                List all L2 skills")
        print("  skill-find <query>        Find skills by name/description")
        print("  skill-delete <name>       Delete a skill from L2")
        print("  curate                    Run L4 curation cycle")
        print("  stats                     Show memory stats")
        print("  health                    Run health check")
        print()
        print("Python API:")
        print("  from memory_core import MemoryCore")
        print("  mem = MemoryCore('./my_agent.db')")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "remember":
        content = " ".join(sys.argv[2:])
        eid = mem.remember(content, source="cli")
        print(f"✅ L1 remembered (id={eid}): {content[:60]}...")

    elif cmd == "forget":
        if len(sys.argv) < 3:
            print("Usage: python cli.py forget <id>")
            sys.exit(1)
        try:
            entry_id = int(sys.argv[2])
        except ValueError:
            print("Invalid ID: must be an integer")
            sys.exit(1)
        if mem.forget(entry_id):
            print(f"✅ L1 entry {entry_id} deleted")
        else:
            print(f"❌ L1 entry {entry_id} not found")

    elif cmd == "forget-all":
        confirm = input("⚠️  Delete ALL L1 entries? Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            count = mem.forget_all()
            print(f"✅ Deleted {count} L1 entries")
        else:
            print("Cancelled.")

    elif cmd == "recall":
        query = " ".join(sys.argv[2:])
        results = mem.recall(query)
        if results:
            for r in results:
                print(f"  [{r['layer']}] {r['content'][:100]}")
        else:
            print("No results.")

    elif cmd == "recall-l1":
        entries = mem.recall_l1()
        for e in entries:
            print(f"  [{e['id']}] pri={e['priority']} {e['content'][:80]}")
        print(f"\n{len(entries)} entries total.")

    elif cmd == "skill-save":
        name, filepath = sys.argv[2], sys.argv[3]
        with open(filepath) as f:
            content = f.read()
        new = mem.skill_save(name, content)
        print(f"✅ Skill '{name}' {'created' if new else 'updated'}")

    elif cmd == "skill-load":
        skill = mem.skill_load(sys.argv[2])
        if skill:
            print(f"Name: {skill['name']} v{skill['version']}")
            print(f"Used: {skill['usage_count']}x")
            print(skill['content'][:500])
        else:
            print(f"❌ Skill '{sys.argv[2]}' not found")

    elif cmd == "skill-list":
        skills = mem.skill_list()
        for s in skills:
            print(f"  {s['name']} v{s['version']} — used {s['usage_count']}x")

    elif cmd == "skill-find":
        skills = mem.skill_find(sys.argv[2])
        for s in skills:
            print(f"  {s['name']}: {s['description']} ({s['usage_count']}x)")

    elif cmd == "skill-delete":
        if len(sys.argv) < 3:
            print("Usage: python cli.py skill-delete <name>")
            sys.exit(1)
        name = sys.argv[2]
        if mem.skill_delete(name):
            print(f"✅ Skill '{name}' deleted")
        else:
            print(f"❌ Skill '{name}' not found")

    elif cmd == "curate":
        result = mem.curate()
        print(f"L1: {result['before']['l1']} → {result['after']['l1']}")
        print(f"L2: {result['before']['l2']} → {result['after']['l2']}")
        for a in result["actions"]:
            print(f"  ⚡ {a}")

    elif cmd == "stats":
        for k, v in mem.stats().items():
            print(f"  {k}: {v}")

    elif cmd == "health":
        result = mem.health_check()
        all_ok = True
        for layer, ok in result.items():
            if layer != "all_ok":
                print(f"  {layer}: {'✅' if ok else '❌'}")
                if not ok:
                    all_ok = False
        print(f"  Overall: {'✅ 五层全通' if all_ok else '❌ 存在异常'}")

    else:
        print(f"Unknown command: {cmd}")
        print("Run 'python cli.py' for help")

    mem.close()


if __name__ == "__main__":
    main()
