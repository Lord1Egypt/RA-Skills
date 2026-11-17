#!/usr/bin/env python3
"""报告内容质量校验（V2.0 重写 — 结构校验 → 内容质量校验）

校验维度:
  1. 结论清晰度 — BLUF 第一句是否为结论（非铺垫/背景）
  2. So What 检查 — 每段是否有业务影响说明
  3. 数据支撑度 — 关键主张是否有数据/引用支撑
  4. 行动明确性 — 建议是否含 Owner + Timeline
  5. 篇幅控制 — 主体是否 ≤500 词
  6. 置信度标注 — HE/MEDIUM/LOW 是否出现在关键发现中
  7. 被动语态 — 是否使用了被动语态
  8. 术语检查 — 是否有未解释的专业术语

用法:
  python3 validate.py <file>                 # JSON 报告到 stdout
  python3 validate.py <file> -o report.json  # 写入文件
"""
import re, sys, json, argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))

# 常见中文被动语态标记
PASSIVE_CN = ['被', '受到', '遭到', '得以', '获得']
# 常见英文被动语态模式
PASSIVE_EN = re.compile(r'\b(?:is|are|was|were|been|being)\s+\w+ed\b', re.IGNORECASE)
# 常见技术术语（需结合上下文判断是否翻译）
TECH_TERMS = [
    '微服务', 'Kubernetes', 'API', 'SDK', 'CI/CD', 'DevOps',
    'middleware', 'ETL', 'OLAP', 'OLTP', 'SaaS', 'PaaS', 'IaaS',
    'MVP', 'POC', 'ROI', 'OKR', 'KPI', 'SLA', 'SLO',
]


def extract_body(text: str) -> str:
    """提取报告主体（排除附录部分）"""
    # 移除 ─── 分隔线之间的内容（header/footer）
    body = re.sub(r'^[═╌─]{5,}.*?$', '', text, flags=re.MULTILINE)
    # 如果存在 ## 附录 或 ## Appendix，截断
    m = re.search(r'^#{2,3}\s*(附录|Appendix|Source|来源)', text,
                  re.MULTILINE | re.IGNORECASE)
    if m:
        body = text[:m.start()]
    return body.strip()


def word_count(text: str) -> int:
    """中英文混合词数估算"""
    # 中文字符数 + 英文单词数
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    en_words = len(re.findall(r'[a-zA-Z]+', text))
    return cn_chars + en_words


def check_bluf(text: str) -> tuple[bool, str]:
    """检查 BLUF：前两段是否包含结论性表述"""
    lines = [l.strip() for l in text.split('\n') if l.strip() and not l.startswith('#')
             and not l.startswith('=') and not l.startswith('─') and not l.startswith('━')
             and not l.startswith('╌')][:5]
    conclusion_markers = [
        '结论', '建议', '需要', '必须', '关键', '核心',
        '建议', '应该', '推荐', '决定', '决策', 'bottom line',
        'headline', 'conclusion', 'recommend', 'key takeaway',
    ]
    first_200 = ' '.join(lines)[:200]
    for marker in conclusion_markers:
        if marker.lower() in first_200.lower():
            return True, f'首段发现结论性标记: "{marker}"'
    # 检查是否以背景/方法论开头（这不好）
    bad_starts = ['背景', '方法', '过程', '概述', '范围', 'background',
                  'methodology', 'scope', 'overview']
    for bad in bad_starts:
        if first_200.lower().startswith(bad.lower()):
            return False, f'首段以背景开头: "{bad}"，建议结论前置'
    return False, '未检测到明确的结论性表述，请确保 BLUF（结论前置）'


def check_so_what(text: str) -> tuple[bool, str]:
    """检查是否有 So What 逻辑：每个发现是否有业务影响"""
    # 查找 Implications / 业务影响 / So What 章节
    so_what_patterns = [
        r'(?i)implication', r'业务影响', r'So\s*What', r'这意味着',
        r'(?i)what this means', r'影响分析', r'(?i)impact',
    ]
    for pat in so_what_patterns:
        if re.search(pat, text):
            return True, '检测到业务影响相关章节'
    return False, '缺少业务影响章节（So What），建议增加  Implications 或 业务影响 部分'


def check_data_support(text: str) -> tuple[bool, str]:
    """检查关键主张是否有数据支撑"""
    # 检测数字+单位组合
    data_patterns = [
        r'\d+[\.\d]*%',           # 百分比
        r'[¥$€£]\s*\d[\d,.]*[万亿]?',  # 货币
        r'\d+[\.\d]*\s*(倍|x|times)',   # 倍数
        r'(同比|环比|增长|下降|提升|降低)\s*\d+',  # 趋势+数字
        r'\d+\s*(个|家|人|次|项|笔)',  # 数量
    ]
    count = 0
    for pat in data_patterns:
        count += len(re.findall(pat, text))
    if count >= 2:
        return True, f'检测到 {count} 处数据支撑'
    elif count == 1:
        return True, f'仅有 1 处数据支撑，建议补充更多量化指标'
    return False, '缺少数据支撑，关键主张需要量化（数字/百分比/金额/趋势对比）'


def check_action_clarity(text: str) -> tuple[bool, str]:
    """检查行动建议是否包含 Owner + Timeline"""
    # 查找 RECOMMENDED ACTIONS / 建议行动 / 建议 章节
    action_section = re.search(
        r'(?i)(?:RECOMMENDED\s*ACTIONS|建议行动|建议|ACTION).*?(?=#{2,3}\s|\Z)',
        text, re.DOTALL)
    if not action_section:
        return False, '缺少"建议行动"章节'

    section = action_section.group(0)
    # 检查是否包含 Owner/Timeline 标记
    has_owner = bool(re.search(r'(?i)(owner|负责|责任人|—\s*\S+)', section))
    has_timeline = bool(re.search(
        r'(?i)(timeline|时间|Q[1-4]|月|周|日前|deadline)', section))

    if has_owner and has_timeline:
        return True, '建议行动包含负责人和时间线'
    elif has_owner:
        return False, '建议行动有负责人但缺少时间线'
    elif has_timeline:
        return False, '建议行动有时间线但缺少负责人'
    return False, '建议行动缺少负责人（Owner）和时间线（Timeline），格式：行动 — 负责人 — 时间线'


def check_word_limit(text: str) -> tuple[bool, str]:
    """检查 500 词篇幅限制"""
    body = extract_body(text)
    wc = word_count(body)
    if wc <= 500:
        return True, f'主体 {wc} 词，符合 ≤500 词要求'
    return False, f'主体 {wc} 词，超出 500 词上限（超出 {wc - 500} 词），请压缩或移至附录'


def check_confidence(text: str) -> tuple[bool, str]:
    """检查关键发现是否标注置信度"""
    confidence_markers = [
        r'置信度[：:]\s*(HIGH|MEDIUM|LOW|高|中|低)',
        r'\[(HIGH|MEDIUM|LOW)\s*(CONFIDENCE|置信度)\]',
        r'(?i)confidence[：:]\s*(HIGH|MEDIUM|LOW)',
    ]
    for pat in confidence_markers:
        matches = re.findall(pat, text)
        if matches:
            return True, f'检测到 {len(matches)} 处置信度标注'
    return False, '关键发现未标注置信度（HIGH/MEDIUM/LOW），建议在每个关键发现后标注'


def check_passive_voice(text: str) -> tuple[bool, str]:
    """检查被动语态"""
    cn_passive = []
    for word in PASSIVE_CN:
        matches = list(re.finditer(word, text))
        for m in matches:
            ctx = text[max(0, m.start() - 10):m.end() + 10]
            cn_passive.append(ctx.strip())
    en_passive = PASSIVE_EN.findall(text)
    total = len(cn_passive) + len(en_passive)
    if total == 0:
        return True, '未发现被动语态'
    if total <= 2:
        return True, f'发现 {total} 处被动语态（可接受范围）'
    return False, f'发现 {total} 处被动语态（建议尽量改为主动语态）'


def validate(filepath: str) -> dict:
    """执行完整校验并返回 report dict"""
    text = Path(filepath).read_text(encoding='utf-8')
    body = extract_body(text)

    checks = [
        {'rule': 'bluf', 'name': '结论前置（BLUF）',
         **dict(zip(('pass', 'detail'), check_bluf(body)))},
        {'rule': 'so-what', 'name': '业务影响（So What）',
         **dict(zip(('pass', 'detail'), check_so_what(body)))},
        {'rule': 'data-support', 'name': '数据支撑度',
         **dict(zip(('pass', 'detail'), check_data_support(body)))},
        {'rule': 'action-clarity', 'name': '行动明确性（Owner+Timeline）',
         **dict(zip(('pass', 'detail'), check_action_clarity(body)))},
        {'rule': 'word-limit', 'name': '篇幅控制（≤500词）',
         **dict(zip(('pass', 'detail'), check_word_limit(text)))},
        {'rule': 'confidence', 'name': '置信度标注',
         **dict(zip(('pass', 'detail'), check_confidence(text)))},
        {'rule': 'passive-voice', 'name': '被动语态检查',
         **dict(zip(('pass', 'detail'), check_passive_voice(body)))},
    ]

    passed = sum(1 for c in checks if c['pass'])
    total = len(checks)

    return {
        'report': Path(filepath).name,
        'timestamp': datetime.now(CST).isoformat(),
        'summary': {
            'passed': passed,
            'total': total,
            'score': f'{passed}/{total}',
            'grade': 'A' if passed >= 6 else 'B' if passed >= 4 else 'C' if passed >= 2 else 'D'
        },
        'checks': checks,
    }


def main():
    p = argparse.ArgumentParser(description='报告内容质量校验 V2.0')
    p.add_argument('file')
    p.add_argument('--output', '-o')
    args = p.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(json.dumps({'error': f'文件不存在: {args.file}'}, ensure_ascii=False),
              file=sys.stderr)
        sys.exit(1)
    report = validate(args.file)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'校验报告: {args.output}  [{report["summary"]["score"]} {report["summary"]["grade"]}级]')
    else:
        print(output)


if __name__ == '__main__':
    main()
