#!/usr/bin/env python3
"""
八字命理分析脚本 v2 — 覆盖 lunar_python EightChar/Yun 全部能力
用法:
  bazi_analysis.py --date 1990-05-15 --time 10:30 --gender 男 [选项]
  bazi_analysis.py --date 1990-四-廿一 --lunar --gender 女 ...

选项:
  --date   必填。公历 YYYY-MM-DD；--lunar 时为农历 年-月-日，闰月用负数(-5=闰五月)
  --time   时辰 HH:MM 或 0-23；缺省=不知道时辰，只排三柱（不虚构时柱）
  --gender 男|女  必填，影响大运顺逆
  --lunar  输入为农历
  --leap   农历闰月（等价于月份取负）
  --sect   晚子时口径: 1=曰分早晚子时(默认, 23点后日柱按次日) 2=子时不换日
  --focus  综合|子女|婚姻|事业|财运|格局  (默认综合)
  --years  流年展望年数 (默认5, 从当年起)
  --json   输出机器可读 JSON（供 agent 解读），默认人类可读文本
依赖: ~/.venvs/bazi/bin/python (pip install lunar_python)
"""
import argparse, json, sys, datetime

try:
    from lunar_python import Lunar, Solar
except ImportError:
    sys.exit("缺少 lunar_python —— 运行: python3 -m venv ~/.venvs/bazi && ~/.venvs/bazi/bin/pip install lunar_python")

# ============ 基础数据 ============
GAN_WX = {'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
GAN_YY = {'甲':'阳','乙':'阴','丙':'阳','丁':'阴','戊':'阳','己':'阴','庚':'阳','辛':'阴','壬':'阳','癸':'阴'}
SHENG = {'木':'火','火':'土','土':'金','金':'水','水':'木'}
KE    = {'木':'土','土':'水','水':'火','火':'金','金':'木'}
LIU_HE = {'子':'丑','丑':'子','寅':'亥','亥':'寅','卯':'戌','戌':'卯','辰':'酉','酉':'辰','巳':'申','申':'巳','午':'未','未':'午'}
CHONG  = {'子':'午','午':'子','丑':'未','未':'丑','寅':'申','申':'寅','卯':'酉','酉':'卯','辰':'戌','戌':'辰','巳':'亥','亥':'巳'}
SAN_HE = {'申':'水','子':'水','辰':'水','寅':'火','午':'火','戌':'火','巳':'金','酉':'金','丑':'金','亥':'木','卯':'木','未':'木'}
# 十神判定：以日干为我
def shi_shen(day_gan, other_gan):
    dw, ow = GAN_WX[day_gan], GAN_WX[other_gan]
    same_yy = GAN_YY[day_gan] == GAN_YY[other_gan]
    if dw == ow:            return '比肩' if same_yy else '劫财'
    if SHENG[dw] == ow:     return '食神' if same_yy else '伤官'
    if KE[dw] == ow:        return '偏财' if same_yy else '正财'
    if KE[ow] == dw:        return '七杀' if same_yy else '正官'
    if SHENG[ow] == dw:     return '偏印' if same_yy else '正印'
    return '?'

SHI_SHEN_MEANING = {
    '比肩':'同辈、兄弟、竞争、合作','劫财':'破耗、争夺、冲动、姐妹',
    '食神':'才华、享受、口福、晚辈(男)','伤官':'创意、叛逆、表达、晚辈(男)',
    '偏财':'意外之财、投机、父亲','正财':'稳定收入、务实、妻子(男)/父亲(女)',
    '七杀':'压力、竞争、魄力、儿子(男)/情人(女)','正官':'权力、地位、约束、丈夫(女)/事业(男)',
    '偏印':'偏门学识、灵感、继母','正印':'学识、保护、贵人、母亲'}
# 子女星（传统口径：男以官杀为子女，女以食伤为子女；时柱为子女宫）
CHILD_STAR = {'男': ['正官','七杀'], '女': ['食神','伤官']}
MARRIAGE_STAR = {'男': ['正财'], '女': ['正官']}
CAREER_STAR  = ['正官','七杀','正印']
WEALTH_STAR  = ['正财','偏财']

YONG_HINT = {'木':'宜东方、绿色、文教','火':'宜南方、红色、传媒','土':'宜中央、黄色、地产',
             '金':'宜西方、白色、金融','水':'宜北方、黑色、贸易'}

# ============ 排盘 ============
def build(date_str, gender, time_str=None, is_lunar=False, leap=False, sect='1'):
    parts = [p for p in date_str.replace('／','/').replace('.','-').split('-') if p.strip()]
    if len(parts) != 3:
        sys.exit(f"日期格式应为 年-月-日，收到: {date_str}")
    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        sys.exit("农历中文月日(如 四-廿一)请用 --date 1990-4-21 数字形式，lunar_python 仅支持数字")
    if leap and m > 0: m = -m
    has_time = time_str is not None
    if is_lunar:
        solar0 = Lunar.fromYmd(y, m, d).getSolar()
        sy, sm, sd = solar0.getYear(), solar0.getMonth(), solar0.getDay()
    else:
        sy, sm, sd = y, m, d
    if has_time:
        ts = time_str.strip()
        if ':' in ts:
            hh, mm = ts.split(':')[:2]; hh, mm = int(hh), int(mm)
        else:
            hh, mm = int(ts), 0
        if not (0 <= hh <= 23 and 0 <= mm <= 59):
            sys.exit("时间应为 HH:MM 或 0-23")
    else:
        hh, mm = 12, 0  # 正午占位，仅取年月日柱；时柱在结果中被屏蔽
    solar = Solar.fromYmdHms(sy, sm, sd, hh, mm, 0)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()
    ec.setSect(int(sect))
    return ec, lunar, solar, has_time

def pillar_map(ec):
    r = {}
    for name, (g,z,n,ds,xk,hg,ssg,ssz,wx,xun) in {
        '年': (ec.getYearGan, ec.getYearZhi, ec.getYearNaYin, ec.getYearDiShi, ec.getYearXunKong, ec.getYearHideGan, ec.getYearShiShenGan, ec.getYearShiShenZhi, ec.getYearWuXing, ec.getYearXun),
        '月': (ec.getMonthGan, ec.getMonthZhi, ec.getMonthNaYin, ec.getMonthDiShi, ec.getMonthXunKong, ec.getMonthHideGan, ec.getMonthShiShenGan, ec.getMonthShiShenZhi, ec.getMonthWuXing, ec.getMonthXun),
        '日': (ec.getDayGan, ec.getDayZhi, ec.getDayNaYin, ec.getDayDiShi, ec.getDayXunKong, ec.getDayHideGan, ec.getDayShiShenGan, ec.getDayShiShenZhi, ec.getDayWuXing, ec.getDayXun),
        '时': (ec.getTimeGan, ec.getTimeZhi, ec.getTimeNaYin, ec.getTimeDiShi, ec.getTimeXunKong, ec.getTimeHideGan, ec.getTimeShiShenGan, ec.getTimeShiShenZhi, ec.getTimeWuXing, ec.getTimeXun),
    }.items():
        r[name] = {'gan': g(), 'zhi': z(), 'nayin': n(), 'dishi': ds(), 'xunkong': xk(),
                   'hide_gan': hg(), 'shishen_gan': ssg(), 'shishen_zhi': ssz(), 'wuxing': wx(), 'xun': xun()}
    return r

def strength(ec, has_time):
    """日主强弱启发式：月令得令 + 四柱干支(含藏干)生扶计数，透明可复核"""
    day = ec.getDayGan(); dw = GAN_WX[day]
    score, detail = 0, []
    mz = ec.getMonthZhi()
    # 藏干五行
    pools = {'年': ec.getYearHideGan(), '月': ec.getMonthHideGan(), '日': ec.getDayHideGan()}
    if has_time: pools['时'] = ec.getTimeHideGan()
    cnt = {'比劫':0,'印':0,'食伤':0,'财':0,'官杀':0}
    for pillar, gans in pools.items():
        for g in gans:
            ss = shi_shen(day, g)
            k = {'比肩':'比劫','劫财':'比劫','正印':'印','偏印':'印','食神':'食伤','伤官':'食伤',
                 '正财':'财','偏财':'财','正官':'官杀','七杀':'官杀'}[ss]
            cnt[k] += 1
    # 月令：日干五行与月支藏干本气
    benqi = ec.getMonthHideGan()[0] if ec.getMonthHideGan() else ''
    if GAN_WX.get(benqi) == dw: score += 3; detail.append(f'月令{benqi}本气比和+3')
    elif SHENG.get(GAN_WX.get(benqi)) == dw: score += 2; detail.append(f'月令{benqi}生我+2')
    support = cnt['比劫'] + cnt['印']; drain = cnt['食伤'] + cnt['财'] + cnt['官杀']
    score += support - drain
    detail.append(f'藏干比劫{cnt["比劫"]}+印{cnt["印"]} vs 食伤{cnt["食伤"]}+财{cnt["财"]}+官杀{cnt["官杀"]}')
    body = '偏旺' if score >= 2 else ('偏弱' if score <= -2 else '中和')
    # 简易喜用神：旺者宜克泄(官杀/食伤/财)，弱者宜生扶(印/比劫)
    if body == '偏旺': fav = ['官杀','食伤','财']
    elif body == '偏弱': fav = ['印','比劫']
    else: fav = ['印','官杀']
    bei_ke = [k for k, v in KE.items() if v == dw][0]
    wx_map = {'比劫': dw, '印': [k for k, v in SHENG.items() if v == dw][0],
              '食伤': SHENG[dw], '财': KE[dw], '官杀': bei_ke}
    fav_wx = sorted({wx_map[k] for k in fav})
    return {'日主': f'{day}{ec.getDayZhi()}({dw})', '强弱': body, '得分': score,
            '依据': detail, '五行计数': cnt, '喜用五行': fav_wx,
            '喜用提示': '；'.join(f'{w}行→{YONG_HINT[w]}' for w in fav_wx)}

def yun_info(ec, gender, has_time):
    g = 1 if gender == '男' else 0
    yun = ec.getYun(g)
    out = {'forward': yun.isForward(),
           '起运': f"{yun.getStartYear()}年{yun.getStartMonth()}月{yun.getStartDay()}日",
           '大运': []}
    for dy in yun.getDaYun():
        item = {'index': dy.getIndex(), 'ganZhi': dy.getGanZhi(),
                'startYear': dy.getStartYear(), 'endYear': dy.getEndYear(),
                'startAge': dy.getStartAge(), 'endAge': dy.getEndAge(), 'xunKong': dy.getXunKong()}
        if dy.getIndex() > 0 and dy.getGanZhi() != '':
            item['liuNian'] = [{'year': ln.getYear(), 'ganZhi': ln.getGanZhi(), 'age': ln.getAge()}
                               for ln in dy.getLiuNian()]
        out['大运'].append(item)
    return out

def relations(pillars_zhi, target_zhi):
    """目标地支与命局四支的合冲关系"""
    rels = []
    for i, z in enumerate(pillars_zhi):
        if z in CHONG and CHONG[z] == target_zhi: rels.append(f'冲{["年","月","日","时"][i]}支{z}')
        if z in LIU_HE and LIU_HE[z] == target_zhi: rels.append(f'合{["年","月","日","时"][i]}支{z}')
    return rels

def focus_stars(ec, gender, has_time, focus):
    day = ec.getDayGan()
    stars = []
    pools = [('年', ec.getYearGan(), ec.getYearHideGan()), ('月', ec.getMonthGan(), ec.getMonthHideGan()),
             ('日', None, ec.getDayHideGan()), ('时', ec.getTimeGan(), ec.getTimeHideGan())]
    if not has_time: pools = pools[:3]
    target_map = {
        '子女': (CHILD_STAR[gender], '子女星'), '婚姻': (MARRIAGE_STAR[gender], '婚姻星'),
        '事业': (CAREER_STAR, '事业星(官印)'), '财运': (WEALTH_STAR, '财星'),
        '综合': (list(SHI_SHEN_MEANING.keys()), '全部十神'), '格局': (list(SHI_SHEN_MEANING.keys()), '全部十神')}
    names, label = target_map[focus]
    for pos, tg, hides in pools:
        seen = set()
        for g in ([tg] if tg else []) + list(hides):
            if not g: continue
            ss = shi_shen(day, g)
            if ss in names and (pos, ss) not in seen:
                seen.add((pos, ss))
                stars.append({'pos': pos, 'shishen': ss, 'gan': g,
                              'meaning': SHI_SHEN_MEANING[ss],
                              'is_child': focus in ('综合','子女') and ss in CHILD_STAR[gender],
                              'is_marriage': focus in ('综合','婚姻') and ss in MARRIAGE_STAR[gender]})
    return label, stars

def liunian_view(yun, years, pillars_zhi):
    now = datetime.date.today().year
    flat = {}
    for dy in yun['大运']:
        for ln in dy.get('liuNian', []):
            flat[ln['year']] = ln
    view = []
    for yr in range(now, now + years):
        ln = flat.get(yr)
        if not ln: continue
        gz = ln['ganZhi']; zg = gz[1]
        rels = relations(pillars_zhi, zg)
        dy_idx = next((d['index'] for d in yun['大运'] if d['startYear'] <= yr <= d['endYear']), None)
        view.append({'year': yr, 'ganZhi': gz, 'age': ln['age'], '大运序': dy_idx,
                     '关系': rels or ['无明显刑冲合']})
    return view

def main():
    ap = argparse.ArgumentParser(description='八字排盘 v2（lunar_python 全能力）')
    ap.add_argument('--date', required=True, help='年-月-日')
    ap.add_argument('--time', default=None, help='HH:MM 或 0-23；缺省=三柱模式')
    ap.add_argument('--gender', required=True, choices=['男','女'])
    ap.add_argument('--lunar', action='store_true', help='输入为农历')
    ap.add_argument('--leap', action='store_true', help='农历闰月')
    ap.add_argument('--sect', default='1', choices=['1','2'], help='晚子时口径')
    ap.add_argument('--focus', default='综合', choices=['综合','子女','婚姻','事业','财运','格局'])
    ap.add_argument('--years', type=int, default=5)
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()

    ec, lunar, solar, has_time = build(a.date, a.gender, a.time, a.lunar, a.leap, a.sect)
    P = pillar_map(ec)
    zhis = [P[k]['zhi'] for k in ['年','月','日']] + ([P['时']['zhi']] if has_time else [])
    strength_r = strength(ec, has_time)
    yun = yun_info(ec, a.gender, has_time)
    label, stars = focus_stars(ec, a.gender, has_time, a.focus)
    lnview = liunian_view(yun, a.years, zhis)

    result = {
        '输入': {'日期': f'{solar.getYear()}-{solar.getMonth()}-{solar.getDay()}(公历)',
                 '农历': lunar.toString(), '时辰': a.time or '未知(三柱模式)', '性别': a.gender},
        '四柱': {k: P[k] for k in ['年','月','日','时'] if has_time or k != '时'},
        '日主': {'天干': ec.getDayGan(), '十神(干)': ec.getDayShiShenGan(),
                 '命宫': ec.getMingGong(), '命宫纳音': ec.getMingGongNaYin(),
                 '身宫': ec.getShenGong(), '胎元': ec.getTaiYuan(), '胎息': ec.getTaiXi()},
        '强弱': strength_r, '专项': {'标签': label, '星曜': stars},
        '大运': yun, '流年': lnview,
        '提示': [] if has_time else ['未提供出生时辰：时柱(子女宫)与各支十神不可推，三柱结论置信度较低']}

    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return
    R = result
    print('=' * 58)
    print(f"  公历 {R['输入']['日期']} {R['输入']['时辰']}  性别{a.gender}")
    print(f"  农历 {R['输入']['农历']}")
    print('=' * 58)
    for k in ['年','月','日','时']:
        if k not in R['四柱']:
            print(f"  {k}柱: ——（未知时辰，三柱模式）"); continue
        p = R['四柱'][k]
        print(f"  {k}柱: {p['gan']}{p['zhi']}  纳音{p['nayin']}  地势{p['dishi']}  空亡{p['xunkong']}")
        print(f"       十神(干){p['shishen_gan']}  藏干{'/'.join(p['hide_gan'])}  支十神{'/'.join(p['shishen_zhi'])}")
    print(f"\n  日主 {R['日主']['天干']} | 命宫{R['日主']['命宫']}({R['日主']['命宫纳音']}) 身宫{R['日主']['身宫']} 胎元{R['日主']['胎元']} 胎息{R['日主']['胎息']}")
    s = R['强弱']
    print(f"\n【日主强弱·启发式】{s['日主']} → {s['强弱']}（得分{s['得分']}）")
    for d in s['依据']: print(f"  · {d}")
    print(f"  喜用五行: {'、'.join(s['喜用五行'])} → {s['喜用提示']}")
    print(f"\n【{R['专项']['标签']}】")
    for st in R['专项']['星曜']:
        tag = '★' if (st['is_child'] and a.focus in ('综合','子女')) or (st['is_marriage'] and a.focus in ('综合','婚姻')) else ' '
        print(f"  {tag}{st['pos']}柱 {st['shishen']}({st['gan']}) — {st['meaning']}")
    y = R['大运']
    print(f"\n【大运】{'顺行' if y['forward'] else '逆行'}，起运 {y['起运']}")
    for d in y['大运']:
        if d['ganZhi']:
            print(f"  {d['startAge']}-{d['endAge']}岁 {d['startYear']}-{d['endYear']}: {d['ganZhi']} (空亡{d['xunKong']})")
    print(f"\n【近年流年】")
    for v in R['流年']:
        print(f"  {v['year']} {v['ganZhi']}({v['age']}岁,大运{v['大运序']}) — {'、'.join(v['关系'])}")
    for t in R['提示']: print(f"\n⚠ {t}")
    print('\n※ 八字为传统文化模型，强弱/喜用为可复核的启发式估算，仅供娱乐参考。')

if __name__ == '__main__':
    main()
