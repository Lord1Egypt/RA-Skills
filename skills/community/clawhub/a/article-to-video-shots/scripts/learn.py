#!/usr/bin/env python3
"""经验沉淀与读写。让这个 skill 越用越准。

设计要点：经验文件放在技能包外面（全局 ~/.workbuddy/avs/，项目级 .avs/），
这样升级技能包不会冲掉已经攒下来的东西。

子命令：
    add        记一条经验
    show       查看全部经验，按类别分组
    digest     输出一份精简版，适合塞进提示词
    promote    把项目级经验提升为全局经验
    forget     删除一条记错的

例子：
    python3 learn.py add --category 画面 --text "涉及食品的画面不要用特写到叉和嘴" --why "用户看了觉得恶心"
    python3 learn.py add --avoid "沙漏" --why "该模型渲染沙漏必崩"
    python3 learn.py show
    python3 learn.py promote 3
"""

import argparse
import json
import sys
import time
from pathlib import Path

GLOBAL_PATH = Path.home() / ".workbuddy" / "avs" / "learnings.jsonl"
PROJECT_PATH = Path(".avs") / "learnings.jsonl"

KIND_LESSON = "lesson"
KIND_AVOID = "avoid"


def load(scope):
    items = []
    paths = []
    if scope in ("all", "global"):
        paths.append(("global", GLOBAL_PATH))
    if scope in ("all", "project"):
        paths.append(("project", PROJECT_PATH))
    for name, p in paths:
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            obj["scope"] = name
            obj["file"] = str(p)
            items.append(obj)
    return items


def next_id(items):
    return max([i.get("id", 0) for i in items] + [0]) + 1


def append_entry(path, entry):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def target_path(scope):
    return GLOBAL_PATH if scope == "global" else PROJECT_PATH


def cmd_add(args):
    if not args.text and not args.avoid:
        sys.exit("至少给 --text 或 --avoid 其中一个")
    scope = args.scope
    path = target_path(scope)
    items = load(scope)
    ts = time.strftime("%Y-%m-%d %H:%M")

    if args.avoid:
        exist = [i for i in items if i.get("kind") == KIND_AVOID and i.get("text") == args.avoid]
        if exist:
            exist[0]["count"] = exist[0].get("count", 1) + 1
            exist[0]["ts"] = ts
            rewrite(path, items)
            print(f"已存在，命中次数更新为 {exist[0]['count']}：{args.avoid}")
            return
        entry = {
            "id": next_id(items),
            "ts": ts,
            "kind": KIND_AVOID,
            "text": args.avoid,
            "why": args.why or "",
            "count": 1,
        }
        append_entry(path, entry)
        print(f"已记录禁用词 #{entry['id']}：{args.avoid}（体检时会自动拦截）")
        return

    exist = [i for i in items if i.get("kind") == KIND_LESSON and i.get("text") == args.text]
    if exist:
        exist[0]["count"] = exist[0].get("count", 1) + 1
        exist[0]["ts"] = ts
        rewrite(path, items)
        print(f"已存在，命中次数更新为 {exist[0]['count']}")
        return
    entry = {
        "id": next_id(items),
        "ts": ts,
        "kind": KIND_LESSON,
        "category": args.category or "通用",
        "text": args.text,
        "why": args.why or "",
        "count": 1,
    }
    append_entry(path, entry)
    print(f"已记录 #{entry['id']} [{entry['category']}]")


def rewrite(path, items):
    own = [i for i in items if i.get("file") == str(path)]
    keep = [{k: v for k, v in i.items() if k not in ("scope", "file")} for i in own]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for i in keep:
            f.write(json.dumps(i, ensure_ascii=False) + "\n")


def cmd_show(args):
    items = load(args.scope)
    if not items:
        print("还没有沉淀任何经验。做完一条片子至少回写两三条，下次就会准很多。")
        return
    lessons = [i for i in items if i.get("kind") == KIND_LESSON]
    avoids = [i for i in items if i.get("kind") == KIND_AVOID]

    if avoids:
        print("画面禁用词（体检会自动拦截）")
        for a in sorted(avoids, key=lambda x: -x.get("count", 1)):
            why = f"  {a['why']}" if a.get("why") else ""
            print(f"  #{a['id']} [{a['scope']}] 「{a['text']}」命中 {a.get('count', 1)} 次{why}")
        print()

    if lessons:
        by_cat = {}
        for l in lessons:
            by_cat.setdefault(l.get("category", "通用"), []).append(l)
        print(f"经验 {len(lessons)} 条")
        for cat, group in by_cat.items():
            print()
            print(f"[{cat}]")
            for l in sorted(group, key=lambda x: -x.get("count", 1)):
                tail = f"  {l['why']}" if l.get("why") else ""
                print(f"  #{l['id']} [{l['scope']}] {l['text']}  x{l.get('count', 1)}{tail}")

    dup = [l for l in lessons if l.get("count", 1) >= 3]
    if dup:
        print()
        print("以下经验已重复出现三次以上，建议升级为 SKILL.md 里的硬规则")
        for l in dup:
            print(f"  #{l['id']} {l['text']}")


def cmd_digest(args):
    items = load(args.scope)
    lessons = [i for i in items if i.get("kind") == KIND_LESSON]
    avoids = [i for i in items if i.get("kind") == KIND_AVOID]
    if not items:
        print("（暂无历史经验）")
        return
    print("写分镜时必须遵守的既往经验：")
    for l in sorted(lessons, key=lambda x: -x.get("count", 1))[: args.top]:
        print(f"- [{l.get('category','通用')}] {l['text']}")
    if avoids:
        print()
        print("画面里禁止出现：")
        print("、".join(sorted({a["text"] for a in avoids})))


def cmd_promote(args):
    project_items = load("project")
    hit = [i for i in project_items if i.get("id") == args.id]
    if not hit:
        sys.exit(f"项目级经验里找不到 #{args.id}")
    item = {k: v for k, v in hit[0].items() if k not in ("scope", "file")}
    globals_items = load("global")
    same = [g for g in globals_items if g.get("text") == item["text"]]
    if same:
        print("全局里已经有同一条，跳过提升。")
        return
    item["id"] = next_id(globals_items)
    append_entry(GLOBAL_PATH, item)
    print(f"已提升为全局经验 #{item['id']}：{item['text']}")


def cmd_forget(args):
    items = load(args.scope)
    hit = [i for i in items if i.get("id") == args.id]
    if not hit:
        sys.exit(f"找不到 #{args.id}")
    path = Path(hit[0]["file"])
    rest = [i for i in load(hit[0]["scope"]) if i.get("id") != args.id]
    rewrite(path, rest)
    print(f"已删除 #{args.id}")


def main():
    ap = argparse.ArgumentParser(description="经验沉淀与读写")
    ap.add_argument("--scope", default="project", choices=["project", "global"], help="作用域，默认记到当前项目")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="记一条经验")
    a.add_argument("--category", help="类别，比如 画面 / 配音 / 用户偏好 / 模型表现")
    a.add_argument("--text", help="经验正文，一句话说清该怎么做")
    a.add_argument("--avoid", help="画面禁用词，会被体检脚本自动拦截")
    a.add_argument("--why", help="为什么，写清当时的具体失败或反馈")
    a.add_argument("--scope")
    a.set_defaults(func=cmd_add)

    s = sub.add_parser("show", help="查看全部经验")
    s.add_argument("--scope", default="all", choices=["all", "project", "global"])
    s.set_defaults(func=cmd_show)

    d = sub.add_parser("digest", help="输出精简版，适合塞进提示词")
    d.add_argument("--scope", default="all", choices=["all", "project", "global"])
    d.add_argument("--top", type=int, default=12, help="最多输出几条经验，默认 12")
    d.set_defaults(func=cmd_digest)

    p = sub.add_parser("promote", help="把项目级经验提升为全局经验")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_promote)

    f = sub.add_parser("forget", help="删除一条记错的")
    f.add_argument("id", type=int)
    f.add_argument("--scope", default="project", choices=["project", "global"])
    f.set_defaults(func=cmd_forget)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
