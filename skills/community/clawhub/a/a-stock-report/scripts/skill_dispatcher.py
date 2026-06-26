#!/usr/bin/env python3
"""
A-stock-report skill dispatcher
从 SKILL.md 动态读取各任务的 prompt 模板，注入真实日期变量，写入约定路径。

设计：
- cron job 调用本脚本，将生成的 prompt 写入 /tmp/dispatcher_prompt_<task>.txt
- 同一 cron session 内，LLM 读取该文件，加载 A-stock-report skill，执行任务
- SKILL.md 中的 "Cron 任务配置" 区块只保留简短通用模板（见 SKILL.md 末尾附录）

用法（cron 直接触发）：
  python3 skill_dispatcher.py --task morning
  python3 skill_dispatcher.py --task evening
  python3 skill_dispatcher.py --task weekend

注意：盘中预警已迁移为独立脚本模式（见 cron_jobs/cron_mirror.json#intraday），不再支持 --task intraday。

用法（带输出重定向）：
  python3 skill_dispatcher.py --task morning --output /tmp/my_prompt.txt
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timedelta

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")
TEMPLATES_DIR = os.path.join(SKILL_DIR, "templates")  # v3.0 模板外置目录

# v3.4 数据驱动 - weekend 任务专用
WEEKEND_REPORTS_DIR = '/workspace/projects/A股报告系统/reports'
WEEKEND_DATA_OUTPUT = '/tmp/_weekend_5d.json'

# 7 字段解析正则 + 数据来源
#   close = 收盘小结_YYYYMMDD.md
#   evening = 晚报_YYYYMMDD.md
WEEKEND_FIELD_PATTERNS = {
    '综合评分':  (r'综合评分[：:]\s*(\d+)\s*/\s*100',         'close'),
    'IF基差':    (r'基差([+\-\d.]+)点[（(]([\u4e00-\u9fa5]+)[）)]', 'close'),  # 修 2026/06/16: 字符类 [+\-\d.]+ 接受 +/- 号 (原 [-\d.]+ 不接受 + 号, 导致升水 06/09 +06/15 IF基差漏抽)
    '两融(亿)':  (r'两融余额[（(](\d{8})[）)][：:]?\s*([\d,]+)亿',  'evening'),
    '两融占比%': (r'两融余额/A股流通市值[（(](\d{8})[）)]\s*=\s*([\d.]+)%', 'evening'),
    'PE':        (r'沪深300PE\s*=\s*([\d.]+)',                  'evening'),
    'PE分位%':   (r'近5年分位点=([\d.]+)%',                      'evening'),
    'ERP%':      (r'股市风险溢价[（(]\d+年\d+月\d+日[）)]\s*=\s*([\d.]+)%', 'evening'),
}

# SKILL.md 中各任务的 marker（用于定位 JSON 块）
TASK_MARKERS = {
    "morning":   "### 1. 晨报",
    "evening":   "### 3. 晚报",
    "weekend":   "### 5. 财经周末版",
}
TASK_ORDER = ["morning", "evening", "weekend"]


def load_template_from_file(task: str):
    """
    v3.0 优先：尝试从 templates/<task>.json 读取 prompt。
    返回 (prompt, source_tag) 或 (None, None) 表示未找到。
    """
    path = os.path.join(TEMPLATES_DIR, f"{task}.json")
    if not os.path.isfile(path):
        return None, None
    try:
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        if "prompt" not in obj:
            print(f"⚠️ templates/{task}.json 缺少 prompt 字段，回退 SKILL.md")
            return None, None
        return obj["prompt"], f"templates/{task}.json"
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️ templates/{task}.json 读取失败 ({e})，回退 SKILL.md")
        return None, None


def skill_md_has_template(task: str) -> bool:
    """v3.0 探测：SKILL.md 中此任务的 json 块是否还在（用于决定 fallback 行为）"""
    try:
        skill_md = read_skill_md()
    except OSError:
        return False
    marker = TASK_MARKERS.get(task)
    if not marker:
        return False
    idx = skill_md.find(marker)
    if idx == -1:
        return False
    task_idx = TASK_ORDER.index(task)
    next_task = TASK_ORDER[task_idx + 1] if task_idx + 1 < len(TASK_ORDER) else None
    next_marker = TASK_MARKERS.get(next_task)
    next_idx = skill_md.find(next_marker, idx + 1) if next_marker else len(skill_md)
    block = skill_md[idx:next_idx]
    return re.search(r"```json\s*\{.*?\}\s*```", block, re.DOTALL) is not None


def raise_template_missing_error(task: str):
    """v3.0 方案 B：templates/ 缺失 + SKILL.md 也无 json 块时，抛清晰错误 + 修复指引"""
    path = os.path.join(TEMPLATES_DIR, f"{task}.json")
    raise FileNotFoundError(
        f"\n❌ 模板缺失：{path}\n"
        f"\n"
        f"该 task 的 prompt 模板未找到。可能原因：\n"
        f"  1. templates/{task}.json 文件丢失（最常见 —— 误删/同步失败）\n"
        f"  2. dispatcher 跑在错误的 skill 目录（SKILL_DIR={SKILL_DIR}）\n"
        f"  3. v3.0 迁移未完成 —— 该 task 还没建 templates/{task}.json\n"
        f"\n"
        f"修复方法：\n"
        f"  · 从备份恢复：cp /tmp/astock_v3.0_phase2/templates/{task}.json {path}\n"
        f"  · 重新生成：用 SKILL.md 里对应段落的 ```json 块（如果还在）抠出 prompt 字段写入该文件\n"
        f"  · 紧急绕过：把 prompt 临时粘到 SKILL.md 该 task 段落下作为 ```json 块（dispatcher 会自动回退）\n"
    )


def read_skill_md():
    with open(SKILL_MD, "r", encoding="utf-8") as f:
        return f.read()


def extract_prompt_template(skill_md: str, task: str) -> str:
    """从 SKILL.md 的 JSON 代码块中提取对应任务的 prompt 字段"""
    marker = TASK_MARKERS.get(task)
    if not marker:
        raise ValueError(f"未知任务类型: {task}")

    # 定位任务区块起点
    idx = skill_md.find(marker)
    if idx == -1:
        raise ValueError(f"SKILL.md 中未找到任务标记: {marker}")

    # 找到下一个任务的 marker 限定块范围（避免跨章节）
    task_idx = TASK_ORDER.index(task)
    next_task = TASK_ORDER[task_idx + 1] if task_idx + 1 < len(TASK_ORDER) else None
    next_marker = TASK_MARKERS.get(next_task)
    next_idx = skill_md.find(next_marker, idx + 1) if next_marker else len(skill_md)
    block = skill_md[idx:next_idx]

    # 在块中找第一个 ```json ... ``` 块（容错：json 必是 {...} 对象，最少空白匹配）
    m = re.search(r'```json\s*(\{.*?\})\s*```', block, re.DOTALL)
    if not m:
        raise ValueError(f"SKILL.md {task} 区块中未找到 ```json 代码块")

    json_text = m.group(1).strip()
    try:
        obj = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"SKILL.md 中 {task} JSON 解析失败: {e}")

    if "prompt" not in obj:
        raise ValueError(f"{task} JSON 中无 prompt 字段")

    return obj["prompt"]


def get_prev_trade_date(n=1):
    """返回上一交易日的日期字符串 YYYY-MM-DD（工作日回溯）"""
    today = datetime.now()
    days = n
    date = today
    while days > 0:
        date -= timedelta(days=1)
        if date.weekday() < 5:
            days -= 1
    return date.strftime("%Y-%m-%d")


def get_today_str():
    now = datetime.now()
    weekday = ["一","二","三","四","五","六","日"][now.weekday()]
    return f"{now.year}年{now.month}月{now.day}日（周{weekday}）"


def get_yesterday_str():
    """返回前一交易日的格式化字符串"""
    return get_prev_trade_date(1)


def get_prev_n_trade_dates(n, end_date=None):
    """返回过去 n 个工作日（周一到周五）的日期字符串列表（按周一→周五顺序）

    D1 决策: 不识别 A 股节假日、简单工作日回溯
    6/14 周日跑 → 返回 ['20260608','20260609','20260610','20260611','20260612']
    """
    if end_date is None:
        end_date = datetime.now()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y%m%d')

    dates = []
    d = end_date
    while len(dates) < n:
        d = d - timedelta(days=1)
        if d.weekday() < 5:  # 周一到周五
            dates.append(d.strftime('%Y%m%d'))
    return list(reversed(dates))


def parse_field(content, field_name):
    """从 md 文本中抽取 1 个字段值；找不到返回 None"""
    pattern, source = WEEKEND_FIELD_PATTERNS[field_name]
    m = re.search(pattern, content)
    if not m:
        return None
    if field_name in ('两融(亿)', '两融占比%'):
        return {'date': m.group(1), 'value': m.group(2).replace(',', '')}
    if field_name == 'IF基差':
        return {'value': m.group(1), 'tag': m.group(2)}
    return m.group(1)


def extract_5d_data(reports_dir, dates):
    """读取 5 天收盘小结 + 晚报、抽 7 字段
    返回 {date: {field: value or None}}"""
    data = {}
    for d in dates:
        close_path = f"{reports_dir}/收盘小结_{d}.md"
        even_path = f"{reports_dir}/晚报_{d}.md"
        close_content = ''
        even_content = ''
        try:
            with open(close_path, encoding='utf-8') as f:
                close_content = f.read()
        except FileNotFoundError:
            pass
        try:
            with open(even_path, encoding='utf-8') as f:
                even_content = f.read()
        except FileNotFoundError:
            pass

        day_data = {}
        for field, (pat, source) in WEEKEND_FIELD_PATTERNS.items():
            content = close_content if source == 'close' else even_content
            if not content:
                day_data[field] = None
            else:
                day_data[field] = parse_field(content, field)
        data[d] = day_data
    return data


def build_weekend_data_block(data, dates):
    """生成 LLM 友好的"原始数据块"文本 + 写 /tmp/_weekend_5d.json

    D2 决策: 缺数据标 ❌ 继续、不硬填不阻断
    """
    # 写 json (结构化数据, LLM 也能用)
    with open(WEEKEND_DATA_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 统计
    total_days = len(dates)
    days_complete = sum(1 for d in dates if all(data[d].values()))
    total_fields = total_days * len(WEEKEND_FIELD_PATTERNS)
    fields_ok = sum(1 for d in dates for f in WEEKEND_FIELD_PATTERNS if data[d][f] is not None)
    missing = [(d, f) for d in dates for f in WEEKEND_FIELD_PATTERNS if data[d][f] is None]

    lines = []
    lines.append('--- 5d 原始数据（v3.4 数据驱动）---')
    lines.append(f'✅ 交易日文件: {days_complete}/{total_days} 完整')
    lines.append(f'✅ 字段解析:   {fields_ok}/{total_fields} 成功')
    if missing:
        miss_str = '、'.join([f'{d}/{f}' for d, f in missing])
        lines.append(f'❌ 缺失字段:   {miss_str}')
    lines.append('')
    lines.append(f'{"日期":10s}  {"综合评分":6s}  {"IF基差":18s}  {"两融(亿)":8s}  {"占比%":5s}  {"PE":5s}  {"PE分位%":6s}  {"ERP%":5s}')

    for d in dates:
        d_data = data[d]
        score = d_data['综合评分'] or '❌'
        if_data = d_data['IF基差']
        if if_data:
            if_str = f'{if_data["value"]}({if_data["tag"]})'
        else:
            if_str = '❌'
        margin = d_data['两融(亿)']
        margin_str = margin['value'] if margin else '❌'
        mpct = d_data['两融占比%']
        mpct_str = mpct['value'] if mpct else '❌'
        pe = d_data['PE'] or '❌'
        pepct = d_data['PE分位%'] or '❌'
        erp = d_data['ERP%'] or '❌'
        lines.append(f'{d}  {score:6s}  {if_str:18s}  {margin_str:8s}  {mpct_str:5s}  {pe:5s}  {pepct:6s}  {erp:5s}')

    lines.append('')
    lines.append('📌 数据来源映射：')
    lines.append('  · 综合评分、IF基差         → 收盘小结_YYYYMMDD.md')
    lines.append('  · 两融(亿)/两融占比%/PE/PE分位%/ERP% → 晚报_YYYYMMDD.md')
    lines.append('  · 两融数据为 T-1（晚报里 YYYYMMDD 字段是昨日日期）')
    lines.append('  · 缺失字段: LLM 标 ❌、不硬填、不跳不补')

    return '\n'.join(lines)


def format_prompt(prompt_template: str) -> str:
    """向 prompt 模板注入当前日期变量"""
    today_str = get_today_str()
    yesterday_str = get_yesterday_str()

    prompt = prompt_template
    prompt = prompt.replace("[今日实际日期]", today_str)
    prompt = prompt.replace("[今日日期]", today_str)
    prompt = prompt.replace("[前一日日期]", yesterday_str)
    prompt = re.sub(r"\[YYYY年MM月DD日\]", today_str, prompt)

    return prompt


def main():
    parser = argparse.ArgumentParser(description="A-stock-report dispatcher")
    parser.add_argument(
        "--task",
        choices=["morning", "evening", "weekend"],
        required=True,
        help="任务类型",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="输出文件路径（默认: /tmp/dispatcher_prompt_<task>.txt）",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="仅打印 prompt 到 stdout，不写入文件",
    )
    args = parser.parse_args()

    output_path = args.output
    if not output_path:
        output_path = f"/tmp/dispatcher_prompt_{args.task}.txt"

    print(f"=== A-stock-report dispatcher | task={args.task} ===")

    # v3.0 双轨制：先试 templates/<task>.json，回退到 SKILL.md（如果 SKILL.md 也有 json 块）
    template, source = load_template_from_file(args.task)
    if template is not None:
        print(f"📂 模板来源: {source}（v3.0 外置模板）")
    elif skill_md_has_template(args.task):
        # 老路径兜底：SKILL.md 还在用 v2.x 内嵌模板
        skill_md = read_skill_md()
        template = extract_prompt_template(skill_md, args.task)
        source = "SKILL.md（v2.x 内嵌模板，fallback）"
        print(f"📂 模板来源: {source}")
    else:
        # v3.0 已完成（SKILL.md 不再含内嵌模板）但 templates/ 缺失 —— 报清晰错误
        raise_template_missing_error(args.task)
    prompt = format_prompt(template)

    # v3.4 数据驱动: weekend 任务自动抽取 5d 数据
    if args.task == 'weekend':
        try:
            dates = get_prev_n_trade_dates(5)
            data = extract_5d_data(WEEKEND_REPORTS_DIR, dates)
            data_block = build_weekend_data_block(data, dates)
            prompt = prompt.replace('{{WEEKEND_5D_DATA}}', data_block)
            print(f"📊 v3.4 数据驱动: 5d 数据已抽取 ({len(dates)} 天, 写 {WEEKEND_DATA_OUTPUT})")
        except Exception as e:
            # 异常时不阻塞, LLM 看到的是空数据块
            print(f"⚠️ v3.4 数据驱动失败: {e}")
            prompt = prompt.replace('{{WEEKEND_5D_DATA}}', '⚠️ 数据驱动抽取失败、请 LLM 自行 read_file 历史报告')
    else:
        prompt = prompt.replace('{{WEEKEND_5D_DATA}}', '')

    print(f"Prompt 已生成，{len(prompt)} 字符")

    if args.print_only:
        print(prompt)
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Prompt 已写入 {output_path}")


if __name__ == "__main__":
    main()
