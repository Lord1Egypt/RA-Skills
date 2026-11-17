#!/usr/bin/env python3
"""
fetch_ceb.py — 中国招标投标公共服务平台（cebpubservice / bulletin）+ 省级公共资源
交易平台 数据解析管线（stdlib only）

架构定位（重要）
================
与 fetch_ccgp.py 一致：本脚本**只做解析与落 JSON**，不逆向后端接口、不擅自联网。

  背景：bulletin.cebpubservice.com 首页是 JS 门户，列表由后端接口
  （…/ctpsp_iiss/…/getSearch.do）驱动，无法像 ccgp 那样静态 GET listing。
  因此 ceb 侧的正确取数方式是：

  ✅ 主路径（推荐）：agent 用 WebFetch / WebSearch 找到详情页 URL 并抓取原始
     HTML 落盘 → 本脚本用 `--html-file` / `--html-dir` 解析成记录。
     每个详情页 HTML = 一条记录。

  ✅ 多源汇入：`--merge existing.json` 把解析出的 ceb 记录追加进已有 records
     （如 ccgp 的 records.json），再 `--run` 交给引擎去重+分析，实现
     「ccgp + ceb 多源数据自动流入同一分析」。

解析器覆盖 cebpubservice 标准发布格式与常见省级平台字段（招标人/招标代理机构/
项目名称/招标控制价/中标人/中标金额/公告时间等），兼容「表格 td」与「标签：值」
两种形态。**上线前建议用 1~2 个目标平台的真实详情页二次校准正则**（见 SELFTEST.md）。

用法：
  # 解析 agent 已落盘的 ceb 详情页（可多个）
  python fetch_ceb.py --html-file ceb1.html --html-file ceb2.html --out ceb_records.json
  python fetch_ceb.py --html-dir ./ceb_html/ --out ceb_records.json

  # 给某个详情页显式指定 source_url（便于回溯/去重）
  python fetch_ceb.py --html-file ceb1.html --source-url https://bulletin.cebpubservice.com/xx/ABC.htm --out ceb_records.json

  # 多源汇入：解析 ceb 后合并进 ccgp records，再跑引擎（自动去重）
  python fetch_ceb.py --html-dir ./ceb_html/ --merge records.json --profile profile.json --out all_records.json --run
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------- text helpers (内联，保持脚本独立可分发) ----------

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s or '')


def clean(s):
    return re.sub(r'\s+', ' ', strip_tags(s)).strip()


def read_text(path):
    return Path(path).read_text(encoding='utf-8', errors='ignore')


def normalize_amount(text):
    """'1101.5 万元' → 11015000 ; '950000.00元' → 950000 ; '￥1,200万' → 12000000"""
    if not text:
        return None
    m = re.search(r'[\d,]+\.?\d*', text)
    if not m:
        return None
    try:
        val = float(m.group().replace(',', ''))
    except ValueError:
        return None
    if val <= 0:
        return None
    if '万' in text:
        val *= 10000
    return int(round(val))


# 省份/直辖市/自治区（用于地域推断）
PROVINCES = ['北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江',
             '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南',
             '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾',
             '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门']

# 常见地级市/计划单列市 -> 省份（真实公告常只写城市名，如「深圳海关」）
CITY_PROVINCE = {
    '深圳': '广东', '广州': '广东', '珠海': '广东', '东莞': '广东', '佛山': '广东',
    '杭州': '浙江', '宁波': '浙江', '温州': '浙江', '南京': '江苏', '苏州': '江苏',
    '无锡': '江苏', '青岛': '山东', '济南': '山东', '烟台': '山东', '武汉': '湖北',
    '长沙': '湖南', '成都': '四川', '西安': '陕西', '郑州': '河南', '合肥': '安徽',
    '福州': '福建', '厦门': '福建', '南宁': '广西', '昆明': '云南', '贵阳': '贵州',
    '遵义': '贵州', '六盘水': '贵州', '南昌': '江西', '太原': '山西', '石家庄': '河北',
    '哈尔滨': '黑龙江', '长春': '吉林', '沈阳': '辽宁', '大连': '辽宁', '兰州': '甘肃',
    '银川': '宁夏', '西宁': '青海', '乌鲁木齐': '新疆', '拉萨': '西藏',
    '呼和浩特': '内蒙古', '海口': '海南', '三亚': '海南', '阜阳': '安徽', '潍坊': '山东',
}


def infer_region(*texts):
    for t in texts:
        if not t:
            continue
        for p in PROVINCES:
            if p in t:
                return p
    # 省名未出现时，用城市名回推所属省份
    for t in texts:
        if not t:
            continue
        for city, prov in CITY_PROVINCE.items():
            if city in t:
                return prov
    return None


def norm_date(text):
    """'2026-06-03' / '2026年06月03日' / '2026.06.03' / '2026/6/3' → '2026-06-03'"""
    if not text:
        return None
    m = re.search(r'(\d{4})[年\-./](\d{1,2})[月\-./](\d{1,2})', text)
    if not m:
        return None
    y, mo, d = m.groups()
    return f'{int(y):04d}-{int(mo):02d}-{int(d):02d}'


# ---------- 公告类型判定 ----------

def map_ceb_type(*texts):
    blob = ' '.join(t for t in texts if t)
    if '废标' in blob or '流标' in blob or '终止' in blob:
        return '废标'
    if '更正' in blob or '变更' in blob or '澄清' in blob or '补遗' in blob:
        return '变更'
    if '中标' in blob or '成交' in blob or '中选' in blob:
        return '中标'   # 含「中标候选人公示 / 中标结果公示」
    if ('招标' in blob or '采购公告' in blob or '资格预审' in blob or '谈判' in blob
            or '磋商' in blob or '询价' in blob or '竞争性' in blob):
        return '招标'
    return '其他'


# ---------- 字段提取（兼容「标签：值」与「表格 td」两种形态） ----------

def _label_value(html, keyword):
    """形态一：同段/同标签内『标签：值』。返回值文本或 None。"""
    m = re.search(keyword + r'\s*(?:[（(][^）)]{0,12}[）)])?\s*[：:]\s*([^<\n]{2,80})', html)
    if m:
        v = clean(m.group(1))
        # 去掉尾随的下一字段名（如「招标人：XX 招标代理机构：」）
        v = re.split(r'\s{2,}', v)[0].strip()
        if v and v not in ('/', '-', '—', '无', '略'):
            return v
    return None


def _td_value(html, keyword):
    """形态二：表格 <td>标签</td><td>值</td>；紧邻仍是表头则再跳一格。"""
    heads = {'项目名称', '工程名称', '招标项目名称', '招标人', '采购人', '建设单位',
             '招标单位', '招标代理机构', '代理机构', '采购代理机构', '招标控制价',
             '预算金额', '最高限价', '概算', '中标人', '成交供应商', '中标供应商',
             '中标金额', '中标价', '成交金额', '公告时间', '发布时间', '公示时间',
             '项目编号', '招标编号', '行政区域', '所在地区'}
    tds = re.findall(r'<td[^>]*>(.*?)</td>', html, re.S)
    for i, t in enumerate(tds):
        c = clean(t)
        if keyword in c and i + 1 < len(tds):
            nxt = clean(tds[i + 1])
            if nxt in heads and i + 2 < len(tds):
                return clean(tds[i + 2])
            if nxt and nxt not in ('/', '-', '—', '无'):
                return nxt
    return None


def _section_value(html, section_kw, name_kws=('名称', '单位名称', '全称')):
    """形态三：两级结构『采购人信息 …… 名 称：XX』。
    真实公告常把主体名放在小节标题下的『名称：』里，而非『采购人：』。
    """
    txt = strip_tags(html)
    i = txt.find(section_kw)
    if i < 0:
        return None
    start = i + len(section_kw)
    window = txt[start:start + 220]
    for nk in name_kws:
        # 允许标签内部有空格：『名 称：』
        pat = r'\s*'.join(list(nk)) + r'\s*[：:]\s*([^\n]{2,60})'
        m = re.search(pat, window)
        if m:
            v = clean(m.group(1))
            v = re.split(r'\s{2,}', v)[0].strip()
            if v and v not in ('/', '-', '—', '无'):
                return v
    return None


def field(html, keywords):
    """按关键词优先级依次尝试两种形态，返回首个命中的清洗值。"""
    for kw in keywords:
        v = _label_value(html, kw)
        if v:
            return v
    for kw in keywords:
        v = _td_value(html, kw)
        if v:
            return v
    return None


def amount_field(html, keywords):
    v = field(html, keywords)
    return normalize_amount(v) if v else None


def _title(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.S)
    if m:
        t = clean(m.group(1))
        # 去站点后缀
        t = re.split(r'[-_|]\s*(中国招标投标|全国|公共资源|招标投标公共服务)', t)[0].strip()
        if len(t) >= 6:
            return t
    for tag in ('h1', 'h2', 'h3'):
        m = re.search(r'<' + tag + r'[^>]*>(.*?)</' + tag + r'>', html, re.S)
        if m:
            t = clean(m.group(1))
            if len(t) >= 6:
                return t
    return None


# ---------- 详情页 → 记录 ----------

def parse_ceb_detail(html, source_url=None):
    project_name = field(html, ['招标项目名称', '项目名称', '工程名称'])
    title = _title(html) or project_name or '(未识别标题)'
    buyer = (field(html, ['招标人', '采购人', '建设单位', '招标单位'])
             or _section_value(html, '采购人信息')
             or _section_value(html, '招标人信息'))
    agency = (field(html, ['招标代理机构', '采购代理机构', '代理机构'])
              or _section_value(html, '采购代理机构信息')
              or _section_value(html, '招标代理机构信息')
              or _section_value(html, '代理机构信息'))
    budget = amount_field(html, ['招标控制价', '预算金额', '最高限价', '概算金额', '概算'])
    win_company = field(html, ['中标人', '成交供应商', '中标供应商', '中标候选人'])
    win_amount = amount_field(html, ['中标金额', '中标价', '成交金额'])
    # 发布日期三级回退：显式发布字段 -> 文末落款日期 -> 排除截止语境的首个日期
    pub = norm_date(
        field(html, ['公告发布时间', '发布日期', '公告时间', '发布时间',
                     '公示时间', '公示日期'])
        or _sign_date(html)
        or _fallback_date(html))
    region = (field(html, ['行政区域', '所在地区', '项目所在地'])
              or infer_region(buyer, project_name, title))
    ann_type = map_ceb_type(title, project_name, html[:400])
    proj_no = field(html, ['招标编号', '项目编号'])

    return {
        'title': title,
        'type': ann_type,
        'project_name': project_name or title,
        'budget_amount': budget,
        'win_amount': win_amount,
        'win_company': win_company,
        'buyer': buyer,
        'agency': agency,
        'region': region,
        'publish_date': pub,
        'source_url': source_url,
        'source_platform': '中国招标投标公共服务平台',
        'project_type': None,
        'content_summary': proj_no or project_name or title,
    }


# 表示「截止/开标」而非「发布」的语境词
_DEADLINE_CUES = ('截止', '开标', '递交', '提交', '结束', '终止', '开启', '解密')


def _sign_date(html):
    """文末落款日期（代理机构/采购人签章处），最贴近真实发布日。"""
    txt = strip_tags(html).rstrip()
    tail = txt[-260:]
    ms = list(re.finditer(r'\d{4}[年\-./]\d{1,2}[月\-./]\d{1,2}', tail))
    return ms[-1].group(0) if ms else None


def _fallback_date(html):
    """全文首个「非截止语境」日期；全被排除时才退回首个日期。"""
    txt = strip_tags(html)
    first = None
    for m in re.finditer(r'\d{4}[年\-./]\d{1,2}[月\-./]\d{1,2}', txt):
        if first is None:
            first = m.group(0)
        lo = max(0, m.start() - 30)
        ctx = txt[lo:m.end() + 30]
        if any(c in ctx for c in _DEADLINE_CUES):
            continue
        return m.group(0)
    return first


# ---------- CLI ----------

# 本工具/引擎自己产出的 HTML 报告标记，避免把产物当输入再解析一遍
_GENERATOR_TAG = 'bid-opportunity-advisor'


def _is_own_output(path):
    """带 generator 标记的文件是我们自己生成的报告，不是招标公告。"""
    try:
        head = path.open(encoding='utf-8', errors='ignore').read(1200)
    except OSError:
        return False
    return _GENERATOR_TAG in head


def _iter_html_files(args):
    files = []
    for f in (args.html_file or []):
        files.append(Path(f))
    if args.html_dir:
        out_p = Path(args.out).resolve() if getattr(args, 'out', None) else None
        for p in sorted(Path(args.html_dir).glob('*.htm*')):
            if out_p and p.resolve() == out_p:
                continue
            if _is_own_output(p):
                print(f'  跳过（本工具生成的报告）: {p.name}')
                continue
            files.append(p)
    return files


def main():
    ap = argparse.ArgumentParser(description='解析 ceb/省级平台详情页 HTML → records JSON')
    ap.add_argument('--html-file', action='append', help='详情页 HTML 文件（可重复）')
    ap.add_argument('--html-dir', help='含多个详情页 HTML 的目录（*.htm/*.html）')
    ap.add_argument('--source-url', help='当仅 1 个 --html-file 时，为其指定原始 URL')
    ap.add_argument('--merge', help='把解析结果追加进该已有 records.json（多源汇入）')
    ap.add_argument('--profile', help='公司画像 JSON（配合 --run）')
    ap.add_argument('--out', default='ceb_records.json')
    ap.add_argument('--run', action='store_true', help='落 JSON 后调用 opportunity_engine.py')
    args = ap.parse_args()

    files = _iter_html_files(args)
    if not files:
        print('Error: 需 --html-file 或 --html-dir 指定待解析的详情页 HTML', file=sys.stderr)
        sys.exit(1)

    records = []
    for i, fp in enumerate(files):
        if not fp.exists():
            print(f'  跳过（不存在）: {fp}', file=sys.stderr)
            continue
        html = read_text(fp)
        src = args.source_url if (args.source_url and len(files) == 1) else None
        rec = parse_ceb_detail(html, source_url=src)
        records.append(rec)
        print(f'  解析 {fp.name} -> {rec["type"]} | {rec["title"][:30]} | buyer={rec["buyer"]} | budget={rec["budget_amount"]} | win={rec["win_company"]}')

    if args.merge:
        mp = Path(args.merge)
        base = json.loads(mp.read_text(encoding='utf-8')) if mp.exists() else []
        combined = base + records
        print(f'\n多源汇入：已有 {len(base)} 条 + ceb {len(records)} 条 = {len(combined)} 条')
        records = combined

    out = Path(args.out)
    out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n已写 {len(records)} 条 -> {out}')

    if args.run:
        import subprocess
        engine = Path(__file__).resolve().parent / 'opportunity_engine.py'
        cmd = [sys.executable, str(engine), str(out)]
        if args.profile:
            cmd += ['--profile', args.profile]
        print('\n=== 调用机会引擎 ===')
        subprocess.run(cmd, check=False)


if __name__ == '__main__':
    main()
