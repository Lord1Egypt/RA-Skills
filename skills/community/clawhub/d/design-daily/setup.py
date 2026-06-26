#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py
Design Brief Skill 一键配置向导
运行后自动生成 .env 和 config.yaml
"""

import os
import sys
import re
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent

# ANSI 颜色
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# 岗位列表（分组展示）
ROLE_GROUPS = {
    "设计执行层": [
        "UI设计师",
        "UX设计师",
        "视觉设计师",
        "交互设计师",
        "服务设计师",
        "设计系统工程师",
        "动效设计师",
        "内容设计师",
        "可访问性设计师",
    ],
    "策略研究层": [
        "用户研究员",
        "增长设计师",
        "产品设计师",
    ],
    "新兴/前沿工种": [
        "AI产品设计师",
        "设计工程师",
        "零界面设计师",
        "空间计算设计师",
    ],
    "其他": [
        "产品经理",
    ],
}

ALL_ROLES = [r for roles in ROLE_GROUPS.values() for r in roles]

ROLES_TABLE = """
  ┌─────────────────┬──────────────────────────────────────────────────────────┐
  │ 分组            │ 岗位                                                     │
  ├─────────────────┼──────────────────────────────────────────────────────────┤
  │ 设计执行层      │ UI设计师 / UX设计师 / 视觉设计师 / 交互设计师           │
  │                 │ 服务设计师 / 设计系统工程师 / 动效设计师                │
  │                 │ 内容设计师 / 可访问性设计师                             │
  ├─────────────────┼──────────────────────────────────────────────────────────┤
  │ 策略研究层      │ 用户研究员 / 增长设计师 / 产品设计师                    │
  ├─────────────────┼──────────────────────────────────────────────────────────┤
  │ 新兴/前沿工种   │ AI产品设计师 / 设计工程师 / 零界面设计师 / 空间计算设计师│
  ├─────────────────┼──────────────────────────────────────────────────────────┤
  │ 其他            │ 产品经理                                                 │
  └─────────────────┴──────────────────────────────────────────────────────────┘
"""


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════╗
║         Design_Daily 配置向导            ║
║    每天自动生成你的专属设计行业日报       ║
╚══════════════════════════════════════════╝{RESET}
""")


def step(n: int, title: str):
    print(f"\n{BOLD}{CYAN}── 第{n}步：{title} ──{RESET}")


def ok(msg: str):
    print(f"{GREEN}✅ {msg}{RESET}")


def warn(msg: str):
    print(f"{YELLOW}⚠️  {msg}{RESET}")


def err(msg: str):
    print(f"{RED}❌ {msg}{RESET}")


def ask(prompt: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    try:
        val = input(f"{BOLD}{prompt}{hint}: {RESET}").strip()
    except UnicodeDecodeError:
        warn("输入包含无法识别的字符，已使用默认值")
        return default
    except EOFError:
        return default
    return val if val else default


def safe_input(prompt: str) -> str:
    """用于序号/时间等纯 ASCII 输入场景，彻底规避编码问题"""
    try:
        import sys
        sys.stdout.write(prompt)
        sys.stdout.flush()
        line = sys.stdin.buffer.readline()
        return line.decode("utf-8", errors="replace").strip()
    except Exception:
        return ""


def ask_roles() -> list[str]:
    """展示分组岗位列表，让用户输入序号选择"""
    # 展示带序号的完整列表
    print(f"\n{BOLD}所有可选岗位：{RESET}")
    idx = 1
    role_idx_map = {}  # 序号 → 岗位名
    for group, roles in ROLE_GROUPS.items():
        print(f"\n  {CYAN}【{group}】{RESET}")
        for role in roles:
            print(f"    {idx:2d}. {role}")
            role_idx_map[idx] = role
            idx += 1

    print(f"""
{YELLOW}💡 选择建议：
   选 1~2 个 → 内容更聚焦，每条都和你强相关
   选 3~5 个 → 兼顾多个方向，适合 lead 或跨角色
   全选     → 信息面最广，但每条针对性会降低{RESET}
""")

    while True:
        raw = input(f"{BOLD}请输入序号（用逗号分隔，如 1,2 或 1,4,13）: {RESET}").strip()
        if not raw:
            warn("至少选择 1 个岗位")
            continue

        parts   = [p.strip() for p in raw.replace("，", ",").split(",")]
        selected = []
        valid    = True

        for p in parts:
            if p.isdigit() and 1 <= int(p) <= len(ALL_ROLES):
                role = role_idx_map[int(p)]
                if role not in selected:
                    selected.append(role)
            else:
                warn(f"无效序号：{p}，请重新输入")
                valid = False
                break

        if not valid:
            continue
        if not selected:
            warn("至少选择 1 个岗位")
            continue

        # 确认
        print(f"\n{GREEN}已选择（{len(selected)} 个）：{' · '.join(selected)}{RESET}")
        confirm = ask("确认？[Y/n]", "Y")
        if confirm.upper() != "N":
            return selected


def ask_items_per_day() -> int:
    step(3, "每日推送条数")
    print(f"""
{YELLOW}每天为你精选几条内容？
  3 条  → 精简版，2 分钟读完
  5 条  → 标准版，5 分钟左右（推荐）
  8 条  → 扩展版，适合设计 lead / 跨团队协作
  10 条 → 全量版，适合设计总监 / 设计管理者，知识面最广{RESET}
""")
    while True:
        val = ask("请输入数字 (3-10)", default="5")
        if val.isdigit() and 3 <= int(val) <= 10:
            ok(f"已设置每日 {val} 条")
            return int(val)
        warn("请输入 3 到 10 之间的数字")




# ── API Key 验证 ──────────────────────────────────────────────────────────────

def verify_serper_key(key: str) -> bool:
    try:
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": key, "Content-Type": "application/json"},
            json={"q": "design news", "num": 1},
            timeout=8,
        )
        return resp.status_code == 200
    except Exception:
        return False


def verify_deepseek_key(key: str) -> bool:
    try:
        resp = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model"   : "deepseek-chat",
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 5,
            },
            timeout=8,
        )
        return resp.status_code == 200
    except Exception:
        return False


def setup_api_keys() -> tuple[str, str]:
    step(1, "配置 API Keys")
    print(f"""
{YELLOW}需要两个免费/低价 API Key：

  1. Serper API Key（搜索设计行业内容用）
     • 免费额度：2500次/月
     • 获取地址：{BOLD}https://serper.dev/{RESET}{YELLOW}
     • 注册后在 Dashboard → API Key 复制

  2. DeepSeek API Key（AI 提炼日报内容用）
     • 费用：约 ¥0.015/次
     • 获取地址：{BOLD}https://platform.deepseek.com{RESET}{YELLOW}
     • 注册后在 API Keys → 创建新密钥{RESET}
""")

    # Serper Key
    while True:
        serper_key = ask("请粘贴你的 Serper API Key")
        if not serper_key:
            warn("Serper API Key 不能为空")
            continue
        print("  验证中...", end="", flush=True)
        if verify_serper_key(serper_key):
            print(f"\r{GREEN}✅ Serper API Key 验证通过{RESET}          ")
            break
        else:
            print(f"\r{RED}❌ Serper API Key 无效，请检查后重新输入{RESET}")

    # DeepSeek Key
    while True:
        deepseek_key = ask("请粘贴你的 DeepSeek API Key")
        if not deepseek_key:
            warn("DeepSeek API Key 不能为空")
            continue
        print("  验证中...", end="", flush=True)
        if verify_deepseek_key(deepseek_key):
            print(f"\r{GREEN}✅ DeepSeek API Key 验证通过{RESET}         ")
            break
        else:
            print(f"\r{RED}❌ DeepSeek API Key 无效，请检查后重新输入{RESET}")

    return serper_key, deepseek_key


def setup_roles() -> list[str]:
    step(2, "选择你的岗位")
    print(f"""
{YELLOW}根据你的岗位，日报会把「设计师视角」写得更有针对性。
选得越少，内容越聚焦；选得越多，信息面越广。{RESET}
{CYAN}{ROLES_TABLE}{RESET}""")
    return ask_roles()


# ── 写入文件 ──────────────────────────────────────────────────────────────────

def write_env(serper_key: str, deepseek_key: str):
    env_path = BASE_DIR / ".env"
    env_path.write_text(
        f"SERPER_API_KEY={serper_key}\n"
        f"DEEPSEEK_API_KEY={deepseek_key}\n",
        encoding="utf-8",
    )
    ok(f".env 已写入：{env_path}")


def write_config(roles: list[str], items_per_day: int, brief_title: str,
                 time_range: str, favorite_designers: list):
    all_commented = []
    for group, group_roles in ROLE_GROUPS.items():
        all_commented.append(f"  # ——【{group}】——")
        for r in group_roles:
            prefix = "  - " if r in roles else "  # - "
            all_commented.append(f"{prefix}{r}")
    commented_block = "\n".join(all_commented)

    # 生成 favorite_designers YAML 块
    if favorite_designers:
        fav_lines = ["favorite_designers:"]
        for d in favorite_designers:
            fav_lines.append(f"  - name: \"{d.get('name', '')}\"")
            if d.get("url"):
                fav_lines.append(f"    url: \"{d['url']}\"")
            if d.get("focus"):
                fav_lines.append(f"    focus: \"{d['focus']}\"")
        fav_block = "\n".join(fav_lines)
    else:
        fav_block = "favorite_designers: []"

    config_content = f"""# =====================================================
# Design Brief · 设计日报 配置文件（由 setup.py 生成）
# 如需修改，直接编辑本文件后重新运行 run.py
# =====================================================

# ── 你的岗位（取消注释 # 号即可启用）────────────────
#
# 💡 选 1~2 个 → 内容更聚焦
#    选 3~5 个 → 兼顾多个方向
#    全选     → 信息面最广，针对性略低
#
roles:
{commented_block}

# ── 每日条数（1~5）──────────────────────────────────
items_per_day: {items_per_day}

# ── 信息时间范围（24h/2d/3d/1w/2w/1m）───────────────
time_range: "{time_range}"

# ── 日报标题────────────────────────────────────────
brief_title: "{brief_title}"

# ── 关注的设计师（选填，1~2 个）─────────────────────
# name：名字/艺名（中英文都行）
# url ：主页链接（任意一个即可）
# focus：你关注他/她的哪个方向
{fav_block}
"""
    cfg_path = BASE_DIR / "config.yaml"
    cfg_path.write_text(config_content, encoding="utf-8")
    ok(f"config.yaml 已写入：{cfg_path}")


def ask_favorite_designers() -> list:
    step(5, "关注的设计师（选填）")
    print(f"""
{YELLOW}可以填写 1~2 位你感兴趣的设计师，日报会优先抓取他们的最新动态。

适合填：
  · 你一直在关注的某位设计师/博主
  · 最近在设计圈突然火起来的人
  · 你对象 / 同事推荐的某个厉害的人

支持：中文艺名、真名、英文名、主页链接（任意一种）
直接回车跳过此步骤。{RESET}
""")
    designers = []
    for i in range(1, 3):
        name_or_url = ask(f"设计师 {i}（名字或主页链接，回车跳过）", default="").strip()
        if not name_or_url:
            break

        designer = {}
        # 判断是 URL 还是名字
        if name_or_url.startswith("http"):
            designer["url"] = name_or_url
            name = ask(f"  → 他/她叫什么名字？（可不填）", default="").strip()
            if name:
                designer["name"] = name
        else:
            designer["name"] = name_or_url
            url = ask(f"  → 有主页链接吗？（可不填）", default="").strip()
            if url.startswith("http"):
                designer["url"] = url

        focus = ask(f"  → 你关注他/她的哪个方向？（如：品牌设计、动效、可以不填）", default="").strip()
        if focus:
            designer["focus"] = focus

        label = designer.get("name") or designer.get("url", "")
        ok(f"已添加：{label}" + (f"（{focus}）" if focus else ""))
        designers.append(designer)

    if not designers:
        print(f"{YELLOW}跳过，未添加关注设计师{RESET}")
    return designers


def print_crontab(push_time: str):
    hour, minute = push_time.split(":")
    cron_line = (
        f"{minute} {hour} * * * "
        f"cd {BASE_DIR.resolve()} && "
        f"python run.py >> {BASE_DIR.resolve()}/logs/cron.log 2>&1"
    )
    print(f"""
{CYAN}── 定时运行设置（可选）──{RESET}
如需每天 {push_time} 自动运行，执行：

  {BOLD}crontab -e{RESET}

添加这一行：
  {YELLOW}{cron_line}{RESET}
""")


def ask_time_range() -> str:
    step(4, "信息时间范围")
    print(f"""
{YELLOW}搜索多长时间内的内容？

设计行业更新不像新闻那么频繁，时间范围可以放宽一些。

  1. 过去 24 小时  → 关注 Figma 等工具的高频更新
  2. 过去 2 天     → 稍宽松，不会遗漏昨天的内容
  3. 过去 3 天     → 周中刷，周末补漏
  4. 过去 1 周     → 推荐默认，设计行业的主流更新频率
  5. 过去 2 周     → 捕捉慢热话题、知名设计师长文
  6. 过去 1 个月   → 视野最广，适合找「引发讨论的大事件」{RESET}
""")
    options = [
        ("24h", "过去 24 小时"),
        ("2d",  "过去 2 天"),
        ("3d",  "过去 3 天"),
        ("1w",  "过去 1 周（推荐）"),
        ("2w",  "过去 2 周"),
        ("1m",  "过去 1 个月"),
    ]
    while True:
        val = ask("请输入序号 (1-6)", default="4")
        if val.isdigit() and 1 <= int(val) <= 6:
            key, label = options[int(val) - 1]
            ok(f"时间范围：{label}")
            return key
        warn("请输入 1 到 6 之间的数字")


def ask_push_time() -> str:
    step(6, "设置定时运行时间（可选）")
    print(f"""
{YELLOW}每天几点自动运行？（仅用于生成 crontab 命令，不会自动写入）
  常用时间：08:00 上班前 / 09:00 到公司 / 12:00 午休{RESET}
""")
    while True:
        val = ask("请输入时间（格式 HH:MM）", default="09:00")
        if re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", val):
            ok(f"定时时间：{val}")
            return val
        warn("格式不正确，请输入如 09:00 / 08:30 这样的格式")


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    banner()
    print(f"{YELLOW}本向导将帮你完成所有配置，大约需要 3 分钟。{RESET}")
    input(f"\n按 {BOLD}Enter{RESET} 开始配置...")

    serper_key, deepseek_key = setup_api_keys()

    try:
        roles = setup_roles()
    except Exception as e:
        warn(f"第2步（岗位选择）出错：{e}，已使用默认值 [UI设计师, UX设计师]")
        roles = ["UI设计师", "UX设计师"]

    try:
        items_per_day = ask_items_per_day()
    except Exception as e:
        warn(f"第3步（每日条数）出错：{e}，已使用默认值 3")
        items_per_day = 3

    brief_title = "Design Daily"

    try:
        time_range = ask_time_range()
    except Exception as e:
        warn(f"第4步（时间范围）出错：{e}，已使用默认值 1w（过去1周）")
        time_range = "1w"

    try:
        favorite_designers = ask_favorite_designers()
    except Exception as e:
        warn(f"第5步（关注设计师）出错：{e}，此项已跳过，可后续在 config.yaml 中手动补充")
        favorite_designers = []

    try:
        push_time = ask_push_time()
    except Exception as e:
        warn(f"第6步（定时时间）出错：{e}，已使用默认值 09:00")
        push_time = "09:00"

    # 写入文件
    print(f"\n{CYAN}{BOLD}── 正在保存配置... ──{RESET}")
    write_env(serper_key, deepseek_key)
    write_config(roles, items_per_day, brief_title, time_range, favorite_designers)

    # 汇总
    time_label = {
        "24h": "过去 24 小时", "2d": "过去 2 天", "3d": "过去 3 天",
        "1w" : "过去 1 周",   "2w": "过去 2 周", "1m": "过去 1 个月",
    }.get(time_range, time_range)
    role_count = len(roles)
    if role_count <= 2:
        focus = "聚焦模式"
    elif role_count <= 5:
        focus = "均衡模式"
    else:
        focus = "广覆盖模式"

    print(f"""
{GREEN}{BOLD}╔══════════════════════════════════════════╗
║             🎉 配置完成！                ║
╚══════════════════════════════════════════╝{RESET}

{BOLD}你的配置：{RESET}
  📋 日报标题：{brief_title}
  👤 岗位（{role_count}个，{focus}）：{' · '.join(roles)}
  📌 每日条数：{items_per_day} 条
  ⏱️  时间范围：{time_label}
  ⭐ 关注设计师：{", ".join([d.get("name") or d.get("url","") for d in favorite_designers]) if favorite_designers else "未设置"}
  ⏰ 定时时间：{push_time}

{BOLD}立即运行：{RESET}
  {YELLOW}python run.py{RESET}

{BOLD}预览模式（不保存文件）：{RESET}
  {YELLOW}python run.py --preview{RESET}
""")

    print_crontab(push_time)

    # 询问是否立即试跑
    run_now = ask("是否立即运行一次看看效果？[Y/n]", "Y")
    if run_now.upper() != "N":
        print(f"\n{CYAN}正在运行，请稍候...{RESET}\n")
        os.environ["SERPER_API_KEY"]   = serper_key
        os.environ["DEEPSEEK_API_KEY"] = deepseek_key
        os.chdir(BASE_DIR)
        os.system(f"{sys.executable} {BASE_DIR / 'run.py'}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}已取消配置。{RESET}")
        sys.exit(0)
