"""
Diary Force - 日记催命鬼（智能提取版）

核心逻辑：
- 用户说一段话 → 我提取其中的各个部分
- 检测到哪个部分就说哪个，不按顺序
- 缺失的部分进行追问
- 用户说"记录完成" → 写入文件 → 内化
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path

# 配置
DIARY_PATH = Path("E:/My-life/daily")
MEMORY_PATH = Path("D:/ObsidianVault/ChuQuan/memory")

# 收集的内容
diary_sections = {
    "overview": "",      # 今日概况（计划、完成、意外、状态）
    "completed": [],     # 今日完成（列表）
    "todos": [],        # 待办延续（列表）
    "thoughts": "",     # 今日思考（问题+答案）
    "insights": "",     # 认知收获
    "wins": "",         # 做得好的地方
    "improvements": "", # 可以改进的地方
    "connections": "",  # 人际连接
    "progress": {},     # 进度追踪 {目标: 进展}
    "mood": "",         # 心情描述
    "energy": 0,        # 能量值 1-10
    "quote": "",        # 今日金句
    "inspiration": "",  # 灵感与想法
    "tomorrow": [],     # 明日展望（列表）
    "free_write": "",   # 自由书写
}

# 检测关键词
SECTION_KEYWORDS = {
    "overview": ["今天", "整体", "感觉", "计划", "发生", "特别", "怎么样", "感觉如何", "早上", "上午", "下午", "晚上"],
    "completed": ["完成", "做了", "实现了", "搞定了", "成功了", "做好", "搞定", "结束", "完成了", "做了"],
    "todos": ["待办", "没完成", "延续", "还没", "待完成", "pending", "接下来"],
    "thoughts": ["思考", "问题", "感悟", "想法", "认知", "反思", "觉得", "认为", "理解"],
    "wins": ["做得好", "成功", "突破", "进步", "好样的", "不错", "值得肯定"],
    "improvements": ["改进", "问题", "不足", "可以更好", "需要改", "遗憾", "可惜"],
    "connections": ["交流", "对话", "感谢", "人", "聊天", "沟通", "谁", "和人"],
    "progress": ["毕业论文", "论文", "目标", "进展", "进度", "状态", "微运动", "习惯"],
    "mood": ["心情", "情绪", "状态", "感受", "感觉", "开心", "难过", "郁闷", "兴奋"],
    "energy": ["能量", "精力", "疲惫", "累", "困", "精神"],
    "quote": ["金句", "名言", "句话说", "一句话", "说的好"],
    "inspiration": ["灵感", "创意", "想法", "念头", "idea", "新的"],
    "tomorrow": ["明天", "明日", "期待", "希望", "接下来", "未来"],
}


def extract_sections(text: str) -> dict:
    """从文本中智能提取各个部分"""
    text = text.strip()
    extracted = {}
    
    # 1. 检测整体内容分配到各个部分
    # 如果是纯叙述（没有明显标签），尝试理解内容并分配
    
    # 检测完成事项 (可能以 • 或 - 开头)
    completed_items = re.findall(r'[•\-\*]\s*(.+)', text)
    if completed_items:
        diary_sections["completed"].extend(completed_items)
        extracted["completed"] = True
    
    # 检测待办事项
    todo_items = re.findall(r'[•\-\*]\s*(.+)', text)
    # 过滤掉已完成的
    if todo_items:
        for item in todo_items:
            if any(kw in item for kw in ["待", "没", "未", "接下来"]):
                diary_sections["todos"].append(item)
        if diary_sections["todos"]:
            extracted["todos"] = True
    
    # 检测能量值
    energy_match = re.search(r'(\d)[/／]10|能量[：:]\s*(\d)', text)
    if energy_match:
        energy = energy_match.group(1) or energy_match.group(2)
        diary_sections["energy"] = int(energy)
        extracted["energy"] = True
    
    # 检测心情
    mood_words = ["开心", "高兴", "难过", "郁闷", "焦虑", "平静", "充实", "疲惫", "兴奋"]
    for mood in mood_words:
        if mood in text:
            diary_sections["mood"] = mood
            extracted["mood"] = True
            break
    
    # 检测进度（目标+进展）
    progress_targets = ["毕业论文", "论文", "微运动", "数字孪生", "lorra"]
    for target in progress_targets:
        if target in text:
            # 提取进展描述
            match = re.search(rf'{target}[^。]*[。]?', text)
            if match:
                diary_sections["progress"][target] = match.group(0)
                extracted["progress"] = True
    
    # 检测金句（引号中的内容）
    quotes = re.findall(r'[""''](.+?)[""'']', text)
    if quotes:
        diary_sections["quote"] = quotes[0]
        extracted["quote"] = True
    
    # 检测思考/感悟（关键词触发）
    if any(kw in text for kw in ["思考", "问题", "感悟", "反思", "意识到", "发现"]):
        diary_sections["thoughts"] = text
        extracted["thoughts"] = True
    
    # 检测做得好/改进
    if any(kw in text for kw in ["做得好", "不错", "成功", "突破"]):
        diary_sections["wins"] = text
        extracted["wins"] = True
    
    if any(kw in text for kw in ["改进", "不足", "问题", "遗憾"]):
        diary_sections["improvements"] = text
        extracted["improvements"] = True
    
    # 检测人际
    if any(kw in text for kw in ["交流", "感谢", "聊天", "对话", "人"]):
        diary_sections["connections"] = text
        extracted["connections"] = True
    
    # 检测灵感
    if any(kw in text for kw in ["灵感", "想法", "创意", "念头"]):
        diary_sections["inspiration"] = text
        extracted["inspiration"] = True
    
    # 检测明天
    if any(kw in text for kw in ["明天", "明日", "期待", "希望"]):
        diary_sections["tomorrow"].append(text)
        extracted["tomorrow"] = True
    
    # 如果没有明显分类，归入 overview 或 free_write
    if not extracted:
        if len(text) < 100:
            diary_sections["overview"] = text
        else:
            diary_sections["free_write"] = text
    
    return extracted


def check_missing_sections() -> list:
    """检查缺失的部分"""
    missing = []
    
    if not diary_sections["overview"]:
        missing.append("今日概况")
    if not diary_sections["completed"]:
        missing.append("今日完成")
    if not diary_sections["thoughts"]:
        missing.append("今日思考")
    if not diary_sections["progress"]:
        missing.append("进度追踪")
    if not diary_sections["mood"]:
        missing.append("心情能量")
    if not diary_sections["tomorrow"]:
        missing.append("明日展望")
    
    return missing


def generate_diary() -> str:
    """生成完整日记"""
    date = datetime.now().strftime("%Y-%m-%d")
    date_tag = date.replace("-", "/")
    
    # 构建日记内容
    lines = [
        "---",
        f'title: "{date} 每日复盘"',
        f'date: "{date}"',
        f"tags: [daily/reflect, daily/{date_tag}]",
        'mood: ""',
        'energy: ""',
        'weather: ""',
        'focus_area: ""',
        "---",
        "",
        f"# {date} 每日复盘",
        "",
        "## 📊 今日概况",
        "",
        "> [!todo] 今日检查清单",
    ]
    
    # 填充 overview
    if diary_sections["overview"]:
        lines.append(f"> - [x] 今日概况: {diary_sections['overview'][:100]}")
    else:
        lines.append("> - [ ] 今日概况")
    
    lines.extend([
        "> - [ ] 核心任务推进了？",
        "> - [ ] 有意外收获或挑战？",
        "> - [ ] 身体和精神状态如何？",
        "",
        "### 🎯 今日完成",
        "",
        "| 任务 | 状态 | 备注 |",
        "|------|------|------|",
    ])
    
    # 完成事项
    if diary_sections["completed"]:
        for item in diary_sections["completed"]:
            lines.append(f"| {item} | ✅ | |")
    else:
        lines.append("| | | |")
    
    lines.extend([
        "",
        "### ⏳ 待办延续",
        "",
        "| 任务 | 优先级 | 原因 |",
        "|------|--------|------|",
    ])
    
    if diary_sections["todos"]:
        for item in diary_sections["todos"]:
            lines.append(f"| {item} | 中 | |")
    else:
        lines.append("| | | |")
    
    lines.extend([
        "",
        "## 💭 今日思考",
        "",
        "> [!question] 核心问题",
    ])
    
    if diary_sections["thoughts"]:
        lines.append(f"> 今天最值得思考的一个问题是：{diary_sections['thoughts'][:200]}")
    else:
        lines.append("> 今天最值得思考的一个问题是：")
    
    lines.extend([
        "",
        "**答案/感悟：**",
        "",
        "> [!info] 认知收获",
    ])
    
    if diary_sections["insights"]:
        lines.append(f"- {diary_sections['insights']}")
    else:
        lines.append("- ")
    
    lines.extend([
        "",
        "> [!success] 做得好的地方",
    ])
    
    if diary_sections["wins"]:
        lines.append(f"- {diary_sections['wins']}")
    else:
        lines.append("- ")
    
    lines.extend([
        "",
        "> [!warning] 可以改进的地方",
    ])
    
    if diary_sections["improvements"]:
        lines.append(f"- {diary_sections['improvements']}")
    else:
        lines.append("- ")
    
    lines.extend([
        "",
        "## 🤝 人际连接",
        "",
        f"- **交流的人：** {diary_sections['connections'] or '无'}",
        "- **有价值的对话：**",
        "- **感谢的人/事：**",
        "",
        "## 📈 进度追踪",
        "",
        "### 长期目标回顾",
        "",
        "| 目标 | 今日进展 | 状态 |",
        "|------|----------|------|",
    ])
    
    # 进度
    progress_map = {
        "毕业论文": "论文目标函数",
        "微运动": "微运动习惯",
        "数字孪生": "记忆架构",
        "lorra": "主动性提升"
    }
    
    for target, label in progress_map.items():
        if target in diary_sections["progress"]:
            lines.append(f"| {label} | {diary_sections['progress'][target][:50]} | 🔄 |")
        else:
            lines.append(f"| {label} | - | 🔄 |")
    
    lines.extend([
        "",
        "### 习惯打卡",
        "",
        "- [ ] 早起",
        "- [ ] 运动",
        "- [ ] 阅读",
        "- [ ] 冥想/反思",
        "- [ ] 早睡",
        "",
        "## 🎭 心情与能量",
        "",
        "### 情绪曲线",
        "",
        "```",
        "早晨:",
        "上午:",
        "下午:",
        "晚上:",
        "```",
        "",
        "### 能量值 (1-10)",
        "",
        f"能量: {diary_sections['energy']}/10",
        "",
        "### 今日金句",
        "",
        f'> "{diary_sections["quote"]}"' if diary_sections["quote"] else "> \"\"",
        "",
        "## 💡 灵感与想法",
        "",
        "> [!tip] 新的想法",
        "",
        diary_sections["inspiration"] or "- ",
        "",
        "> [!abstract] 创意种子",
        "",
        "- ",
        "",
        "## 🔮 明日展望",
        "",
        "### 🎯 明日最重要的 3 件事",
        "",
    ])
    
    if diary_sections["tomorrow"]:
        for i, item in enumerate(diary_sections["tomorrow"][:3], 1):
            lines.append(f"{i}. {item}")
    else:
        lines.extend(["1. ", "2. ", "3. "])
    
    lines.extend([
        "",
        "### ⚠️ 潜在挑战",
        "",
        "- ",
        "",
        "### 🎁 期待的事情",
        "",
        "- ",
        "",
        "## 📝 自由书写",
        "",
        diary_sections["free_write"] or "",
        "",
        "---",
        "",
        f"**记录时间：** {date}",
        f"**用时：** 约 {len(''.join(diary_sections.values())) // 500} 分钟",
    ])
    
    return "\n".join(lines)


def summarize_and_ask(user_input: str) -> str:
    """总结用户输入，检测提取了什么，还缺什么"""
    extracted = extract_sections(user_input)
    missing = check_missing_sections()
    
    # 总结提取的内容
    summary_parts = []
    if "completed" in extracted:
        summary_parts.append("✅ 已记录完成事项")
    if "todos" in extracted:
        summary_parts.append("📋 已记录待办")
    if "thoughts" in extracted:
        summary_parts.append("💭 已记录思考")
    if "wins" in extracted:
        summary_parts.append("🎉 已记录做得好的地方")
    if "improvements" in extracted:
        summary_parts.append("💡 已记录可以改进的地方")
    if "progress" in extracted:
        summary_parts.append("📈 已记录进度")
    if "energy" in extracted:
        summary_parts.append(f"⚡ 能量值: {diary_sections['energy']}/10")
    if "mood" in extracted:
        summary_parts.append(f"😄 心情: {diary_sections['mood']}")
    if "tomorrow" in extracted:
        summary_parts.append("🔮 已记录明日展望")
    
    summary = " | ".join(summary_parts) if summary_parts else "📝 已记录"
    
    # 追问缺失的部分
    ask_part = ""
    if missing:
        # 随机选一个缺失的部分追问
        next_ask = missing[0]
        prompts = {
            "今日概况": "今天的整体感觉怎么样？还有什么要补充的吗？",
            "今日完成": "今天还完成了哪些具体的事？",
            "今日思考": "今天有什么值得思考的问题或感悟吗？",
            "进度追踪": "毕业论文/微运动/其他目标进展如何？",
            "心情能量": "心情怎么样？能量值多少（1-10）？",
            "明日展望": "明天最想做什么？有什么期待？"
        }
        ask_part = f"\n\n💬 {prompts.get(next_ask, '还有要补充的吗？')}"
    
    return f"**{summary}**{ask_part}"


def finalize_diary() -> str:
    """完成日记写作并内化"""
    content = generate_diary()
    
    # 🔥 熬夜判断：0-5点写日记，询问日期
    current_hour = datetime.now().hour
    if 0 <= current_hour < 5:
        # 熬夜到凌晨，默认用昨天的日期
        yesterday = (datetime.now() - __import__('datetime').timedelta(days=1)).strftime("%Y-%m-%d")
        today = datetime.now().strftime("%Y-%m-%d")
        return f"""
🌙 检测到你在熬夜时间（{current_hour}点）写日记

请问今天是 **{yesterday}** 还是 **{today}** ？

回复日期我将完成日记写入～
"""
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    # 写入文件
    diary_file = DIARY_PATH / f"{date}.md"
    diary_file.write_text(content, encoding='utf-8')
    
    # 内化到 memory/
    memory_file = MEMORY_PATH / f"{date}.md"
    memory_file.write_text(content, encoding='utf-8')
    
    # Git push
    os.chdir(MEMORY_PATH.parent)
    os.system('git add . && git commit -m "memory: sync {}" && git push'.format(date))
    
    return f"""
✅ **日记已完成！**

- 📝 已写入: {diary_file}
- 💾 已内化到: memory/{date}.md  
- 🚀 Git push 完成

🌙 晚安，好梦～
"""



def finalize_diary_with_date(date: str) -> str:
    content = generate_diary()
    
    # 验证日期格式
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "❌ 日期格式错误，请使用 YYYY-MM-DD 格式"
    
    # 写入文件
    diary_file = DIARY_PATH / f"{date}.md"
    diary_file.write_text(content, encoding='utf-8')

    # 内化到 memory/
    memory_file = MEMORY_PATH / f"{date}.md"
    memory_file.write_text(content, encoding='utf-8')

    # Git push
    os.chdir(MEMORY_PATH.parent)
    os.system(f'git add . && git commit -m "memory: sync {date}" && git push')

    msg = f"""
✅日记已完成！
- 📝 已写入: {diary_file}
- 💾 已内化到: memory/{date}.md  
- 🚀 Git push 完成
"""
    return msg



def reset_sections():
    """重置所有部分"""
    global diary_sections
    diary_sections = {
        "overview": "",
        "completed": [],
        "todos": [],
        "thoughts": "",
        "insights": "",
        "wins": "",
        "improvements": "",
        "connections": "",
        "progress": {},
        "mood": "",
        "energy": 0,
        "quote": "",
        "inspiration": "",
        "tomorrow": [],
        "free_write": "",
    }


# CLI 接口
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            reset_sections()
            print("""
📅 **Diary Force 启动！**

你来说，我来记。
不用按顺序，想说什么说什么。

说到一定程度后，说**"记录完成"**我就生成最终日记～

---
开始吧：
""")
        elif sys.argv[1] == "done":
            # 支持指定日期: python diary_force.py done 2026-02-27
            date = sys.argv[2] if len(sys.argv) > 2 else None
            if date:
                print(finalize_diary_with_date(date))
            else:
                print(finalize_diary())
        elif sys.argv[1] == "reset":
            reset_sections()
            print("✅ 已重置")
        else:
            # 处理用户输入
            user_text = " ".join(sys.argv[1:])
            print(summarize_and_ask(user_text))
    else:
        print("用法:")
        print("  python diary_force.py start       # 开始新日记")
        print("  python diary_force.py done        # 完成并内化")
        print("  python diary_force.py reset       # 重置")
        print("  python diary_force.py <文本>      # 处理用户输入")
