#!/usr/bin/env python3
"""内容密度分析 — 检测报告的"干货率"

分析维度:
  1. 数据密度 — 数字/百分比/金额在全文中的占比
  2. 段落长度分布 — 识别过长的叙述段落
  3. 空洞检测 — 识别"废话"段落（缺乏具体信息）
  4. 可操作词汇密度 — 动词导向 vs 形容词导向

用法:
  python3 density.py <file>                 # 分析报告到 stdout
  python3 density.py <file> --json         # JSON 格式输出
"""
import re, sys, json, argparse
from pathlib import Path


def data_density(text: str) -> dict:
    """计算数据出现的密度"""
    patterns = {
        '百分比': r'\d+[\.\d]*%',
        '金额': r'[¥$€£]\s*\d[\d,.]*[万亿]?',
        '倍数': r'\d+[\.\d]*\s*(倍|x|times)',
        '数量': r'\d+\s*(个|家|人|次|项|笔|万|亿)',
        '年份': r'(20\d{2}|FY\d{2})',
        '增长词': r'(同比|环比|增长|下降|提升|降低|上涨|下滑)\s*\d+',
    }
    result = {}
    total = 0
    for name, pat in patterns.items():
        count = len(re.findall(pat, text))
        result[name] = count
        total += count
    word_count = len(re.findall(r'[\u4e00-\u9fff]', text)) + len(re.findall(r'[a-zA-Z]+', text))
    result['总数'] = total
    result['密度'] = f'{total}/{word_count}词 = {total/max(word_count, 1)*100:.1f}%' \
        if word_count > 0 else '0'
    return result


def paragraph_analysis(text: str) -> dict:
    """分析段落长度分布"""
    # 按空行分割段落
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text)
                  if p.strip() and not p.strip().startswith('#')
                  and not p.strip().startswith('=') and not p.strip().startswith('─')
                  and not p.strip().startswith('━')]
    lengths = [len(p) for p in paragraphs]
    if not lengths:
        return {'段落数': 0, '平均长度': 0, '最长': 0, '过长段落': 0}

    long_threshold = 300  # 超过300字符的段落视为过长
    long_paragraphs = [l for l in lengths if l > long_threshold]

    return {
        '段落数': len(lengths),
        '平均长度': sum(lengths) // len(lengths),
        '最长': max(lengths),
        '过长段落': len(long_paragraphs),
        '长度分布': {
            '短(<100字)': len([l for l in lengths if l <= 100]),
            '中(100-300字)': len([l for l in lengths if 100 < l <= 300]),
            '长(>300字)': len(long_paragraphs),
        }
    }


def fluff_detection(text: str) -> dict:
    """检测空洞/废话段落"""
    fluff_patterns = [
        (r'(众所周知|众所周知|不言而喻)', '陈词滥调'),
        (r'(为了|旨在|目的是).{0,20}(提升|加强|优化|完善|改进)', '空洞目标陈述'),
        (r'(高度重视|充分认识|深刻理解|深入推进|全面贯彻)', '官僚套话'),
        (r'(在.{0,10}的.{0,10}下)', '嵌套句式'),
    ]
    findings = {}
    for pat, label in fluff_patterns:
        matches = re.findall(pat, text)
        if matches:
            findings[label] = len(matches)
    return findings if findings else {'无': 0}


def action_density(text: str) -> dict:
    """计算可操作词汇密度"""
    action_verbs = ['建议', '推荐', '需要', '必须', '应该', '决定', '审批',
                    '启动', '执行', '部署', '分配', '监控', 'review', 'approve',
                    'recommend', 'require', 'decide', 'launch', 'execute']
    descriptive = ['良好', '显著', '稳定', '持续', '积极', '重要', '关键',
                   '优秀', '不错', '很大', '非常', '较为', '一定的']

    action_count = sum(len(re.findall(re.escape(v), text)) for v in action_verbs)
    desc_count = sum(len(re.findall(re.escape(v), text)) for v in descriptive)

    return {
        '行动词': action_count,
        '描述词': desc_count,
        '行动/描述比': f'{action_count}:{desc_count}'
                       f' ({"✅ 行动导向" if action_count > desc_count else "⚠️ 描述过多"})'
    }


def estimate_reading_time(text: str) -> str:
    """估算阅读时间"""
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    reading_speed = 400  # 中文阅读速度：字/分钟
    minutes = cn_chars / reading_speed
    if minutes < 1:
        return f'<1 分钟（{cn_chars}字）'
    return f'{minutes:.0f} 分钟（{cn_chars}字）'


def analyze(filepath: str) -> dict:
    """执行完整密度分析"""
    text = Path(filepath).read_text(encoding='utf-8')
    return {
        'report': Path(filepath).name,
        'reading_time': estimate_reading_time(text),
        'data_density': data_density(text),
        'paragraph_analysis': paragraph_analysis(text),
        'fluff_detection': fluff_detection(text),
        'action_density': action_density(text),
        'verdict': _verdict(text),
    }


def _verdict(text: str) -> str:
    """综合判断"""
    data = data_density(text)
    para = paragraph_analysis(text)
    fluff = fluff_detection(text)
    action = action_density(text)

    issues = []
    if int(data.get('总数', 0)) < 3:
        issues.append('数据密度过低')
    if para.get('过长段落', 0) > 1:
        issues.append(f'{para["过长段落"]}个过长段落需要拆分')
    if fluff and sum(fluff.values()) > 2:
        issues.append('存在空洞/套话')
    if action.get('行动词', 0) < action.get('描述词', 0):
        issues.append('描述多于行动，建议增加具体建议')

    if not issues:
        return '✅ 报告密度良好，适合高管阅读'
    return f'⚠️ 需改进：{"; ".join(issues)}'


def main():
    p = argparse.ArgumentParser(description='内容密度分析')
    p.add_argument('file')
    p.add_argument('--json', action='store_true', help='JSON 格式输出')
    args = p.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f'错误：文件不存在 {args.file}', file=sys.stderr)
        sys.exit(1)

    result = analyze(args.file)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f'📊 内容密度分析: {result["report"]}')
        print(f'⏱  阅读时间: {result["reading_time"]}')
        print(f'📈 数据密度: {json.dumps(result["data_density"], ensure_ascii=False, indent=2)}')
        print(f'📝 段落分析: {json.dumps(result["paragraph_analysis"], ensure_ascii=False, indent=2)}')
        print(f'🗑  空洞检测: {json.dumps(result["fluff_detection"], ensure_ascii=False)}')
        print(f'🎯 行动密度: {json.dumps(result["action_density"], ensure_ascii=False)}')
        print(f'\n🏆 综合判断: {result["verdict"]}')


if __name__ == '__main__':
    main()
