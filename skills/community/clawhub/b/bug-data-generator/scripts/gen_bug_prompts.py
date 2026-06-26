#!/usr/bin/python3
"""
gen_bug_prompts.py — 根据 BUG 描述生成工具名 + 用户指令列表

此脚本不生成 JSONL，仅输出结构化的指令列表供用户确认。
确认后由 data-generator 技能完成 JSONL 生成。

用法:
  python3 gen_bug_prompts.py \
    --bug "用户说X分钟后开空调，系统却立即执行" \
    --correct-tool scene_generator \
    --count 20
"""

import sys, os, json, argparse, random

DEVICE_TYPES = [
    "空调","窗帘","风扇","空气净化器","智能开关","灯",
    "电暖器","净水机","扫地机","除湿机","加湿器",
    "电饭煲","热水器","冰箱","净饮机","壁挂炉",
    "智能插座","新风机","油烟机","洗碗机","洗衣机",
]

TEMPLATES = {
    "delay_minute": [
        "{N}分钟后打开{D}","{N}分钟后关闭{D}",
        "{N}分钟后把{D}打开","{N}分钟后把{D}关闭",
        "等{N}分钟再开{D}","等{N}分钟再关{D}",
        "帮我{N}分钟后打开{D}","帮我{N}分钟后关闭{D}",
        "{N}分钟后开{D}","{N}分钟后关{D}",
        "过{N}分钟帮我开{D}","过{N}分钟帮我关{D}",
        "{N}min后开{D}","{N}min后关{D}",
    ],
    "delay_second": [
        "{N}秒后打开{D}","{N}秒后关闭{D}",
        "{N}秒后开{D}","{N}秒后关{D}",
        "等{N}秒再开{D}","等{N}秒再关{D}",
    ],
    "delay_hour": [
        "{H}小时后打开{D}","{H}小时后关闭{D}",
        "{H}小时后开{D}","{H}小时后关{D}",
        "等{H}小时再开{D}","等{H}小时再关{D}",
    ],
    "today": [
        "今天{H}点打开{D}","今天{H}点关闭{D}",
        "今晚{H}点开{D}","今晚{H}点关{D}",
        "今天{H}:{M}打开{D}","今天{H}:{M}关闭{D}",
    ],
    "tomorrow": [
        "明天{H}点开{D}","明天{H}点关{D}",
        "明天{H}:{M}打开{D}","明天{H}:{M}关闭{D}",
    ],
    "repeat": [
        "每天{H}点打开{D}","每天{H}点关闭{D}",
        "每天{H}:{M}开{D}","每天{H}:{M}关{D}",
        "工作日{H}点打开{D}","工作日{H}点关闭{D}",
        "周末{H}点打开{D}","周末{H}点关闭{D}",
        "每周一{H}点开{D}","每周三{H}点关{D}",
    ],
}

NM=[1,2,3,5,8,10,15,20,30,45,60]
NH=[1,2,3,5,8,10,12]
NS=[5,10,15,20,30,45,60]
TH=[8,9,10,12,14,16,18,20,21,22]
TM=[0,15,30,45]

def detect_types(bug_desc: str) -> list:
    bug = bug_desc.lower()
    if "分钟后" in bug or "min后" in bug: return ["delay_minute"]
    if "秒后" in bug: return ["delay_second"]
    if "小时后" in bug: return ["delay_hour"]
    if "今晚" in bug or "今天" in bug: return ["today"]
    if "明天" in bug: return ["tomorrow"]
    if "每天" in bug or "工作日" in bug or "循环" in bug: return ["repeat"]
    return ["delay_minute", "delay_second", "delay_hour", "today", "repeat"]

def fill(tpl: str) -> str:
    dev = random.choice(DEVICE_TYPES)
    result = tpl.replace("{D}", dev)
    if "{N}" in result:
        pool = NM if "minute" in tpl else NM
        result = result.replace("{N}", str(random.choice(pool)))
    if "{H}" in result:
        result = result.replace("{H}", str(random.choice(TH)))
    if "{M}" in result:
        result = result.replace("{M}", str(random.choice(TM)))
    return result

def generate(tool_name: str, bug_desc: str, count: int, seed: int = 42) -> dict:
    """返回结构化结果 dict"""
    random.seed(seed)
    bug_types = detect_types(bug_desc)
    per_type = max(1, count // len(bug_types))

    instructions = []
    for bt in bug_types:
        pool = TEMPLATES.get(bt, TEMPLATES["delay_minute"])
        for _ in range(per_type):
            tpl = random.choice(pool)
            instructions.append(fill(tpl))
    # 补齐
    while len(instructions) < count:
        tpl = random.choice(TEMPLATES[random.choice(bug_types)])
        instructions.append(fill(tpl))
    instructions = instructions[:count]

    type_map = {}
    for bt in bug_types:
        for t in TEMPLATES[bt]:
            type_map[t] = bt

    result_instructions = []
    for i, text in enumerate(instructions, 1):
        tpl_match = text
        for t, bt in type_map.items():
            if t.replace("{D}","").replace("{N}","").replace("{H}","").replace("{M}","") in text:
                tpl_match = bt
                break
        result_instructions.append({
            "id": i,
            "text": text,
            "type": type_map.get(tpl_match, "其他")
        })

    return {
        "tool_name": tool_name,
        "bug_description": bug_desc,
        "instruction_count": len(result_instructions),
        "instructions": result_instructions,
        "note": "以上为由 AI 根据 BUG 分析生成的指令列表，请审核或修改后确认，确认后调用 data-generator 生成 JSONL。",
    }

def output_text(result: dict) -> str:
    """输出供用户阅读的文本格式"""
    lines = [
        f"工具: {result['tool_name']}",
        f"指令数量: {result['instruction_count']} 条",
        "",
        "用户指令列表:",
    ]
    for item in result["instructions"]:
        lines.append(f"  {item['id']}. [{item['type']}] {item['text']}")
    lines.extend(["", result["note"]])
    return "\n".join(lines)

def output_json(result: dict) -> str:
    """输出 JSON 格式（供 data-generator 调用）"""
    return json.dumps({
        "tool_name": result["tool_name"],
        "user_instructions": [item["text"] for item in result["instructions"]]
    }, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description="生成 BUG 修复用用户指令列表")
    parser.add_argument("--bug", required=True, help="BUG 描述")
    parser.add_argument("--correct-tool", required=True, help="正确工具名")
    parser.add_argument("--count", type=int, default=20, help="生成指令数量（默认20）")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    parser.add_argument("--format", choices=["text","json","both"], default="both", help="输出格式")
    parser.add_argument("--output", help="输出文件路径（可选）")
    args = parser.parse_args()

    result = generate(args.correct_tool, args.bug, args.count, args.seed)

    if args.format in ("text","both"):
        text = output_text(result)
        print(text)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\n[已写出文本格式: {args.output}]")

    if args.format in ("json","both"):
        json_str = output_json(result)
        json_path = args.output.replace(".txt","") + "_for_datagen.json" if args.output else "/tmp/bug_instructions_for_datagen.json"
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"\n[JSON 格式（供 data-generator 调用）: {json_path}]")
        if args.format == "json":
            print(json_str)

if __name__ == "__main__":
    main()
