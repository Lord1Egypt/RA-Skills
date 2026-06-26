#!/usr/bin/python3
"""
gen_bug_data.py — 根据 BUG 描述 + 错误原因生成修复训练数据

用法:
  python3 gen_bug_data.py \
    --bug "用户说X分钟后开空调，系统却立即执行" \
    --correct-tool scene_generator \
    --wrong-tool dev_control \
    --output /workspace/bug_fix.jsonl \
    --count 100

工作流:
  1. 解析 BUG 描述 → 提取「触发指令特征」
  2. 生成用户指令列表（N条）
  3. 调用 data-generator/gen_data.py 生成完整 JSONL
"""

import sys, os, json, argparse, random

# ── 内嵌指令模板（根据 BUG 特征生成用户指令）─────────────────
INSTRUCTION_TEMPLATES = {
    # 延时类（分钟）
    "delay_minute": [
        "{N}分钟后打开{D}", "{N}分钟后关闭{D}",
        "{N}分钟后把{D}打开", "{N}分钟后把{D}关闭",
        "等{N}分钟再开{D}", "等{N}分钟再关{D}",
        "帮我{N}分钟后打开{D}", "帮我{N}分钟后关闭{D}",
        "{N}分钟后开{D}", "{N}分钟后关{D}",
        "过{N}分钟帮我开{D}", "过{N}分钟帮我关{D}",
    ],
    # 延时类（秒）
    "delay_second": [
        "{N}秒后打开{D}", "{N}秒后关闭{D}",
        "{N}秒后开{D}", "{N}秒后关{D}",
        "等{N}秒再开{D}", "等{N}秒再关{D}",
    ],
    # 延时类（小时）
    "delay_hour": [
        "{H}小时后打开{D}", "{H}小时后关闭{D}",
        "{H}小时后开{D}", "{H}小时后关{D}",
        "等{H}小时再开{D}", "等{H}小时再关{D}",
    ],
    # 定时类（今天/今晚）
    "today": [
        "今天{H}点打开{D}", "今天{H}点关闭{D}",
        "今晚{H}点开{D}", "今晚{H}点关{D}",
        "今天{H}:{M}打开{D}", "今天{H}:{M}关闭{D}",
    ],
    # 定时类（明天）
    "tomorrow": [
        "明天{H}点开{D}", "明天{H}点关{D}",
    ],
    # 循环类
    "repeat": [
        "每天{H}点打开{D}", "每天{H}点关闭{D}",
        "工作日{H}点开{D}", "工作日{H}点关{D}",
        "周末{H}点打开{D}", "周末{H}点关闭{D}",
    ],
    # 设备开关
    "device_onoff": [
        "打开{D}", "关闭{D}", "把{D}打开", "把{D}关闭",
        "{D}开机", "{D}关机",
    ],
}

# 设备类型
DEVICE_TYPES = [
    "空调","窗帘","风扇","空气净化器","智能开关","灯",
    "电暖器","净水机","扫地机","除湿机","加湿器",
    "电饭煲","热水器","冰箱","净饮机","壁挂炉",
    "智能插座","新风机","油烟机","洗碗机","洗衣机",
]

# 时间值池
NM = [1,2,3,5,8,10,15,20,30,45,60]
NH = [1,2,3,5,8,10,12]
NS = [5,10,15,20,30,45,60]
TH = [8,9,10,12,14,16,18,20,21,22]
TM = [0,15,30,45]

def detect_bug_type(bug_desc: str) -> list:
    """从 BUG 描述中检测应使用的指令模板类型"""
    bug = bug_desc.lower()
    if any(w in bug for w in ["分钟后","min后","分钟后","等几分"]):
        return ["delay_minute"]
    if any(w in bug for w in ["秒后","几秒"]):
        return ["delay_second"]
    if any(w in bug for w in ["小时后","小时后再","等几小时"]):
        return ["delay_hour"]
    if any(w in bug for w in ["今晚","今天几点","今天定时","定时开","定时关"]):
        return ["today"]
    if any(w in bug for w in ["明天"]):
        return ["tomorrow"]
    if any(w in bug for w in ["每天","工作日","周末","循环"]):
        return ["repeat"]
    if any(w in bug for w in ["立即","马上","立刻","马上开","立即开"]):
        return ["delay_minute", "delay_second"]
    # 默认：覆盖多种类型
    return ["delay_minute", "today", "repeat"]

def generate_instructions(bug_type: str, count: int, seed: int = 42) -> list:
    """根据 BUG 类型生成用户指令列表"""
    random.seed(seed)
    templates = INSTRUCTION_TEMPLATES.get(bug_type, INSTRUCTION_TEMPLATES["delay_minute"])
    instructions = []
    for _ in range(count):
        tpl = random.choice(templates)
        dev = random.choice(DEVICE_TYPES)
        N = random.choice(NM)
        H = random.choice(TH)
        M = random.choice(TM)
        S = random.choice(NS)
        hour2 = random.choice([h for h in TH if h >= 18])  # 偏晚时间
        instr = (tpl
            .replace("{N}", str(N))
            .replace("{H}", str(H))
            .replace("{H2}", str(hour2))
            .replace("{M}", str(M))
            .replace("{S}", str(S))
            .replace("{D}", dev))
        instructions.append(instr)
    return instructions

def main():
    parser = argparse.ArgumentParser(description="生成 BUG 修复训练数据")
    parser.add_argument("--bug", required=True, help="BUG 描述")
    parser.add_argument("--correct-tool", required=True, help="正确工具名")
    parser.add_argument("--wrong-tool", default="", help="错误工具名（用于说明）")
    parser.add_argument("--output", default="/workspace/bug_fix.jsonl", help="输出文件")
    parser.add_argument("--count", type=int, default=100, help="生成数量")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    args = parser.parse_args()

    print(f"[BugDataGenerator] BUG: {args.bug[:50]}...")
    print(f"[BugDataGenerator] 正确工具: {args.correct_tool}  错误工具: {args.wrong_tool or '无'}")

    # 1. 检测 BUG 类型 → 生成触发指令
    bug_types = detect_bug_type(args.bug)
    print(f"[BugDataGenerator] 检测到 BUG 类型: {bug_types}")

    # 平均分配各类型数量
    instructions = []
    per_type = max(1, args.count // len(bug_types))
    for bt in bug_types:
        instructions += generate_instructions(bt, per_type, seed=args.seed)
    # 补齐剩余
    while len(instructions) < args.count:
        instructions.append(random.choice(instructions))
    instructions = instructions[:args.count]

    print(f"[BugDataGenerator] 生成指令数: {len(instructions)}")
    print(f"  示例: {instructions[:3]}")

    # 2. 拼接完整提示词（调用 data-generator 的 build_prompt）
    sys.path.insert(0, "/app/openclaw/skills/data-generator/scripts")
    try:
        from build_prompt import build_prompt
        prompt = build_prompt(args.correct_tool, instructions)
    except Exception as e:
        print(f"[BugDataGenerator] build_prompt 失败: {e}")
        print("[BugDataGenerator] 提示: 请确保 data-generator 技能已安装")
        # 回退：直接输出指令列表供人工处理
        with open(args.output.replace(".jsonl", "_instructions.txt"), "w", encoding="utf-8") as f:
            for instr in instructions:
                f.write(instr + "\n")
        print(f"[BugDataGenerator] 指令列表已保存到: {args.output.replace('.jsonl', '_instructions.txt')}")
        return

    # 3. 调用 LLM 生成完整 JSONL（简化版：直接构造）
    #    由于工具格式已知，直接生成而非依赖 LLM
    print(f"[BugDataGenerator] 提示词长度: {len(prompt)}")

    # 生成 system 模板数据
    import time, datetime
    def rand_time():
        y = random.choice([2026, 2027])
        return f"{y}-{random.randint(1,12):02d}-{random.randint(1,28):02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

    def rand_room():
        rooms = ["客厅","卧室","书房","厨房","全屋","餐厅","阳台","儿童房"]
        return random.choice(rooms)

    SCENES = ["舒适睡眠","回家模式","离家模式","快速净化","烛光晚餐","运动健身","下午茶模式","早餐模式","晚餐模式","看书模式","观影模式","会客模式"]
    DEVICE_NAMES = {
        "空调":["舒爽王(空调)","云逸空调(空调)","舒享家(空调)","清风侠(空调)","静心王(空调)"],
        "窗帘":["客厅窗帘(窗帘)","卧室窗帘(窗帘)","书房窗帘(窗帘)","智能窗帘(窗帘)"],
        "风扇":["静音风扇(风扇)","智能风扇(风扇)","塔扇(风扇)","落地扇(风扇)"],
        "灯":["客厅灯(灯)","卧室灯(灯)","台灯(灯)","吸顶灯(灯)","氛围灯(灯)"],
        "空气净化器":["空气净化器(空气净化器)","除醛净化器(净化器)","智能净化器(净化器)"],
        "扫地机":["扫地机(扫地机)","扫拖一体机(扫地机)","扫地机器人(扫地机)"],
    }

    def build_local_dev():
        dt = random.choice(DEVICE_TYPES)
        pool = DEVICE_NAMES.get(dt, [f"{dt}虚拟({dt})"])
        return random.choice(pool) if pool else f"{dt}虚拟({dt})"

    def build_dev_list(local_dev):
        dt = local_dev.rsplit("(",1)[-1].rstrip(")")
        room = rand_room()
        dl = {room: [local_dev]}
        # 添加同房间其他设备
        for d2, names in DEVICE_NAMES.items():
            if d2 != dt and len(dl[room]) < 8:
                dl[room].append(random.choice(names))
        return dl

    def make_scenes():
        return [{"scene_id": random.randint(65000,66000),
                 "scene_name": random.choice(SCENES),
                 "room_name": rand_room()} for _ in range(random.randint(2,4))]

    VOICES = ["好的~","好的呀~","好的呢~","嗯嗯~"]
    REPLIES_DELAY = ["{d}已经设置好了，{t}准时执行~","好的，{d}将在{t}自动执行~"]
    REPLIES_DEV  = ["好的，{d}马上执行~","好的~马上为您{d}~"]

    results = []
    for instr in instructions:
        local_dev = build_local_dev()
        dev_type = local_dev.rsplit("(",1)[-1].rstrip(")")
        dev_name = local_dev.rsplit("(",1)[0]
        dl = build_dev_list(local_dev)

        action = "打开" if any(w in instr for w in ["打开","开","启动"]) and "关闭" not in instr else "关闭"

        # 解析时间
        import re
        time_desc = ""
        timing_val, timing_unit = None, None
        m = re.search(r"(\d+)\s*秒", instr)
        if m:
            timing_val, timing_unit = int(m.group(1)), "秒"
            time_desc = m.group(0)
        m = re.search(r"(\d+)\s*分", instr)
        if m:
            timing_val, timing_unit = int(m.group(1)), "分钟"
            time_desc = m.group(0)
        m = re.search(r"(\d+)\s*小", instr)
        if m:
            timing_val, timing_unit = int(m.group(1))*60, "分钟"
            time_desc = m.group(0)

        # 构造 tool_call
        if args.correct_tool == "scene_generator":
            if timing_val:
                query_obj = {"action": action, "device": dev_name, "timing": {"value": timing_val, "unit": timing_unit}}
                tool_call = f\'<tool_call>{{"tool_name":"scene_generator","query":"{json.dumps(query_obj,ensure_ascii=False)}"}}</tool_call>\'
            else:
                tc = {"tool_name":"scene_generator","command":f"{action}{dev_name}","name":f"{action}{dev_name}场景","repeat_type":"单次","datetime":"","custom_days":"","condition":""}
                tool_call = f\'<tool_call>{json.dumps(tc,ensure_ascii=False)}</tool_call>\'
            reply = random.choice(REPLIES_DELAY).replace("{d}", dev_type).replace("{t}", time_desc or instr)
        else:
            query_str = f"{action}{dev_name}"
            tool_call = f\'<tool_call>{{"tool_name":"{args.correct_tool}","query":"{query_str}"}}</tool_call>\'
            reply = random.choice(REPLIES_DEV).replace("{d}", dev_type)

        results.append({
            "conversations": [
                {"from": "human", "value": instr},
                {"from": "assistant", "value": random.choice(VOICES) + tool_call},
                {"from": "observation", "value": "<tool_response>操作成功。</tool_response>"},
                {"from": "assistant", "value": reply}
            ],
            "system": (
                f"<本地设备>{local_dev}</本地设备>,"
                f"<当前时间>{rand_time()}</当前时间>,"
                f"<用户场景列表>{json.dumps(make_scenes(),ensure_ascii=False)}</用户场景列表>,"
                f"<用户设备列表>{json.dumps(dl,ensure_ascii=False)}</用户设备列表>"
            )
        })

    with open(args.output, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"[BugDataGenerator] ✅ 完成! 输出: {args.output} ({len(results)}条)")

if __name__ == "__main__":
    main()
