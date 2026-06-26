#!/usr/bin/env python3
"""
consensus_analyze.py — 用 PAL MCP 多模型 Consensus 评估贝壳小区候选清单

用法：
    python3 consensus_analyze.py \
        --data-file /tmp/beike_discover/all_candidates.json \
        --requirements "三房120㎡以上, 预算1300万, 产权车位×2, 地铁1km, 2005年后, 有电梯" \
        --models "gemini-3-pro-preview,auto" \
        --output /tmp/report.md

依赖：
    - mcporter 已安装且配置了 pal server（~/.mcporter/mcporter.json）
    - pal-mcp-server 通过 uvx 启动

流程：
    1. 读取候选小区 JSON，构建结构化摘要
    2. 向模型1发送 prompt（偏价格/稳健视角）
    3. 向模型2发送同样 prompt（偏流动性/投资视角）
    4. 综合两个视角输出最终排名和推荐理由
    5. 保存 Markdown 报告
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from typing import Optional


# ──────────────────────────────────────────────────────────────────────────────
# mcporter 调用封装
# ──────────────────────────────────────────────────────────────────────────────

def call_pal_chat(prompt: str, model: str = 'auto',
                  workdir: str = '/tmp',
                  thinking_mode: str = 'medium',
                  continuation_id: Optional[str] = None) -> dict:
    """调用 PAL MCP chat 工具，返回响应内容和 continuation_id"""

    args_dict = {
        'prompt': prompt,
        'model': model,
        'working_directory_absolute_path': workdir,
        'thinking_mode': thinking_mode,
    }
    if continuation_id:
        args_dict['continuation_id'] = continuation_id

    args_json = json.dumps(args_dict)
    cmd = ['mcporter', 'call', 'pal.chat', '--args', args_json, '--output', 'json']

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout.strip()
        if not output:
            return {'error': result.stderr[:500], 'content': ''}

        # mcporter 可能输出多个 JSON 或带前缀
        # 尝试直接解析
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            # 找最后一个完整 JSON 对象
            matches = re.findall(r'\{[^{}]*"content"[^{}]*\}', output, re.DOTALL)
            data = json.loads(matches[-1]) if matches else {'content': output, 'error': None}

        return {
            'content': data.get('content', output),
            'continuation_id': data.get('continuation_offer', {}).get('continuation_id'),
            'model_used': data.get('metadata', {}).get('model_used', model),
        }
    except subprocess.TimeoutExpired:
        return {'error': 'timeout', 'content': ''}
    except Exception as e:
        return {'error': str(e), 'content': ''}


# ──────────────────────────────────────────────────────────────────────────────
# 数据摘要构建
# ──────────────────────────────────────────────────────────────────────────────

def build_summary(candidates: list, requirements: str) -> str:
    """将候选小区列表构建为结构化文本摘要"""
    lines = [
        f"# 上海二手房候选小区数据（贝壳找房，{datetime.now().strftime('%Y-%m-%d')} 抓取）",
        "",
        f"## 购房需求",
        requirements,
        "",
        f"## 候选小区清单（共 {len(candidates)} 个，按流动性排序）",
        "",
        "| 序号 | 小区名 | 板块 | 均价(万/㎡) | 建年 | 总户数 | 在售 | 90天成交 | 地铁 | 建筑 | 容积率 | 物业 |",
        "|------|--------|------|------------|------|-------|------|---------|------|------|--------|------|",
    ]

    for i, r in enumerate(candidates[:20], 1):  # 最多20个
        price = int(r.get('price', 0) or 0)
        est_130 = round(price * 130 / 10000) if price else '?'
        metro = r.get('metro', '')[:15] or '无'
        lines.append(
            f"| {i} | {r.get('name','')} | {r.get('board','')} | {price/10000:.1f} "
            f"| {r.get('year','')} | {r.get('total_units','')} "
            f"| {r.get('on_sale','')} | {r.get('sold_90d','')} "
            f"| {metro} | {r.get('building_type','')} "
            f"| {r.get('far','')} | {r.get('mgmt_company','')[:8]} |"
        )

    lines += [
        "",
        "## 字段说明",
        "- **90天成交**：近3个月成交套数，越高流动性越好",
        "- **均价**：贝壳2月参考均价，130㎡三房总价 = 均价 × 130 ÷ 10000（万元）",
        "- **建筑**：板楼优于塔楼（采光/通风更好）",
        "- **容积率**：< 2.0 为低密度，居住品质更好",
        "- **产权车位**：需现场核实，列表数据未包含",
        "",
        "## 评估要求",
        f"{requirements}",
    ]

    return '\n'.join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Consensus 评估流程
# ──────────────────────────────────────────────────────────────────────────────

PROMPT_TEMPLATE_MODEL1 = """你是一位**稳健型**房产顾问，偏重价格安全边际和长期持有价值。

请基于以下上海二手房小区数据，从稳健买家的角度进行评估。

{summary}

## 任务
1. **逐一点评**每个小区（3–5句话）：是否符合购房需求？主要优势和风险是什么？
2. 给出你的**TOP 5 推荐排名**，并说明理由（重点关注：价格安全、物业品质、建筑年代、低密度）
3. 列出**明确不推荐**的小区及原因

评估维度权重：价格匹配 35% + 建筑品质 25% + 地铁通勤 20% + 流动性 20%
"""

PROMPT_TEMPLATE_MODEL2 = """你是一位**流动性导向型**房产顾问，偏重未来转手能力和市场热度。

请基于以下上海二手房小区数据，从关注流动性的买家角度进行评估。

{summary}

## 任务
1. **逐一点评**每个小区（3–5句话）：市场热度如何？未来转手难度？
2. 给出你的**TOP 5 推荐排名**，并说明理由（重点关注：90天成交量、在售套数、地铁距离、关注人气）
3. 指出**流动性陷阱**：哪些小区看起来便宜但可能难以转手

评估维度权重：流动性 40% + 地铁通勤 25% + 价格匹配 20% + 建筑品质 15%
"""

PROMPT_SYNTHESIS = """你是一位综合评估专家。以下是两位顾问对同一批上海二手房小区的独立评估意见：

## 稳健型顾问（偏价格和品质）的意见：
{opinion1}

---

## 流动性顾问（偏市场热度和转手）的意见：
{opinion2}

---

## 购房需求
{requirements}

## 综合评估任务
1. 找出两位顾问**共同推荐**的小区（最可靠）
2. 分析两者**分歧点**及各自理由是否充分
3. 给出最终**综合推荐 TOP 5**，权衡两种视角
4. 给出一句话**执行建议**：接下来应该优先看哪 2-3 个小区？

请用 Markdown 表格和分节标题组织输出，便于阅读。
"""


def run_consensus(candidates: list, requirements: str, models: list,
                  workdir: str = '/tmp') -> dict:
    """执行完整的 consensus 评估流程"""

    model1 = models[0] if len(models) >= 1 else 'gemini-3-pro-preview'
    model2 = models[1] if len(models) >= 2 else 'auto'

    summary = build_summary(candidates, requirements)
    results = {}

    print(f"\n📤 向模型1 ({model1}) 发送稳健视角评估...")
    resp1 = call_pal_chat(
        prompt=PROMPT_TEMPLATE_MODEL1.format(summary=summary),
        model=model1,
        workdir=workdir,
        thinking_mode='high',
    )
    results['model1'] = {'model': model1, 'response': resp1}
    if resp1.get('content'):
        print(f"✅ 模型1 响应: {len(resp1['content'])} 字")
    else:
        print(f"⚠️  模型1 响应为空: {resp1.get('error')}")

    print(f"\n📤 向模型2 ({model2}) 发送流动性视角评估...")
    resp2 = call_pal_chat(
        prompt=PROMPT_TEMPLATE_MODEL2.format(summary=summary),
        model=model2,
        workdir=workdir,
        thinking_mode='high',
    )
    results['model2'] = {'model': model2, 'response': resp2}
    if resp2.get('content'):
        print(f"✅ 模型2 响应: {len(resp2['content'])} 字")
    else:
        print(f"⚠️  模型2 响应为空: {resp2.get('error')}")

    print("\n📤 进行综合 Synthesis 评估...")
    opinion1 = resp1.get('content', '（模型1无响应）')
    opinion2 = resp2.get('content', '（模型2无响应）')
    resp3 = call_pal_chat(
        prompt=PROMPT_SYNTHESIS.format(
            opinion1=opinion1,
            opinion2=opinion2,
            requirements=requirements,
        ),
        model='auto',
        workdir=workdir,
        thinking_mode='medium',
    )
    results['synthesis'] = {'model': 'auto', 'response': resp3}
    if resp3.get('content'):
        print(f"✅ Synthesis 响应: {len(resp3['content'])} 字")
    else:
        print(f"⚠️  Synthesis 响应为空: {resp3.get('error')}")

    return results


# ──────────────────────────────────────────────────────────────────────────────
# 报告生成
# ──────────────────────────────────────────────────────────────────────────────

def generate_report(candidates: list, requirements: str,
                    results: dict, output_path: str) -> str:
    """生成完整 Markdown 报告"""

    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    report = f"""# 贝壳找房小区 PAL MCP Consensus 评估报告

> 生成时间：{now}  
> 数据来源：贝壳找房（mcp-chrome 实时抓取）  
> 候选小区：{len(candidates)} 个

---

## 购房需求
{requirements}

---

## 候选小区概览

| # | 小区名 | 板块 | 均价 | 建年 | 在售 | 90天成交 | 地铁 |
|---|--------|------|------|------|------|---------|------|
"""
    for i, r in enumerate(candidates[:20], 1):
        price = int(r.get('price', 0) or 0)
        report += (
            f"| {i} | {r.get('name','')} | {r.get('board','')} "
            f"| {price/10000:.1f}万 | {r.get('year','')} "
            f"| {r.get('on_sale','')} | {r.get('sold_90d','')} "
            f"| {r.get('metro','')[:15] or '无'} |\n"
        )

    m1_name = results.get('model1', {}).get('model', '模型1')
    m2_name = results.get('model2', {}).get('model', '模型2')

    report += f"""
---

## 🏦 稳健视角（{m1_name}）

{results.get('model1', {}).get('response', {}).get('content', '无响应')}

---

## 📈 流动性视角（{m2_name}）

{results.get('model2', {}).get('response', {}).get('content', '无响应')}

---

## 🎯 综合 Consensus 推荐

{results.get('synthesis', {}).get('response', {}).get('content', '无响应')}

---

*本报告由 beike-xiaoqu-research skill v2 + PAL MCP 自动生成*
"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return report


# ──────────────────────────────────────────────────────────────────────────────
# 入口
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='PAL MCP Consensus 小区评估')
    parser.add_argument('--data-file', default=None,
                        help='候选小区 JSON 文件路径')
    parser.add_argument('--requirements',
                        default='三房120㎡以上，预算1300万以内，需产权车位，地铁1km以内，2005年后建成，有电梯',
                        help='购房需求描述')
    parser.add_argument('--models', default='gemini-3-pro-preview,auto',
                        help='逗号分隔的模型列表（最少2个）')
    parser.add_argument('--output', default='/tmp/consensus_report.md',
                        help='输出报告路径')
    parser.add_argument('--workdir', default='/tmp',
                        help='PAL MCP 工作目录')

    args = parser.parse_args()

    # 加载候选小区数据
    if args.data_file and os.path.exists(args.data_file):
        with open(args.data_file) as f:
            candidates = json.load(f)
        print(f"📂 加载 {len(candidates)} 个候选小区: {args.data_file}")
    else:
        print("❌ 未提供有效的 --data-file，请先运行 region_discover.sh")
        sys.exit(1)

    models = [m.strip() for m in args.models.split(',')]
    if len(models) < 2:
        models.append('auto')

    print(f"🤖 使用模型: {models}")
    print(f"📋 购房需求: {args.requirements}")

    # 执行 consensus
    results = run_consensus(
        candidates=candidates,
        requirements=args.requirements,
        models=models,
        workdir=args.workdir,
    )

    # 生成报告
    report = generate_report(
        candidates=candidates,
        requirements=args.requirements,
        results=results,
        output_path=args.output,
    )

    print(f"\n✅ 报告已保存: {args.output}")
    print(f"   大小: {len(report)} 字")
    print("\n--- 综合推荐摘要 ---")
    synthesis = results.get('synthesis', {}).get('response', {}).get('content', '')
    # 打印前500字
    print(synthesis[:500] + ('...' if len(synthesis) > 500 else ''))


if __name__ == '__main__':
    main()
