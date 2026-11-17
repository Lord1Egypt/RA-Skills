# -*- coding: utf-8 -*-
"""
股指期货 · 净增对比（直接计算法 v1）
=====================================
维度: ① 中信期货(代客)（席位码0018）   ② 全市场前20名会员合并
数据: 中金所官网 cffex.com.cn 会员持仓排名(前20名)

【计算方法 —— 用户指定，显式固化】
  净增对比：直接采用中金所官方“比上交易日增减”字段（XML 中 varvolume）数值，按各品种求和：
    多单净增 = Σ_各品种 (当日该品种 持买单量 的“比上交易日增减”)
    空单净增 = Σ_各品种 (当日该品种 持卖单量 的“比上交易日增减”)
    净多空   = 多单净增 − 空单净增
  （即：读取官方自带的增减条目直接相加，不再用“当日−前日”自行相减；
    该字段已含合约上市/退市、会员进出前20等边界，比自行相减更准，尤其适用于全市场前20合并维度）
  绝对持仓：仍用 volume 字段（当日持仓量）直接求和。

【用法 / 可执行命令】
  本脚本随 skill 一起存放，路径为 <skill目录>/if_netchange.py（与 SKILL.md 同级）。
  缓存目录自动建于脚本同级的 cache/ 下，与运行位置、工区无关，可随处拷贝使用。

  # 自动：优先取"今日"数据(若已发布)，对比前一交易日；否则回退到最近交易日
  python3 <skill目录>/if_netchange.py
  # （本机可用 WorkBuddy 托管 Python：python3 <skill目录>/if_netchange.py）

  # 手动指定 当前日 与 对比前日（格式 YYYYMMDD）
  python3 <skill目录>/if_netchange.py 20260810 20260807

  # 仅生成 HTML、不打印控制台表
  python3 <skill目录>/if_netchange.py --quiet

【输出】
  控制台：两张净增对比表（中信 / 全市场前20）
  文件  ：股指期货持仓统计_YYYYMMDD.html（写入当前工作目录，含绝对持仓 + 净增对比 + 方法说明）
  纯标准库，无需 pip 安装任何第三方包。
"""
import xml.etree.ElementTree as ET
import urllib.request, ssl, os, sys, random, datetime

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(SKILL_DIR, 'cache')                   # 缓存目录跟随脚本自身（可移植，不依赖工区路径）
os.makedirs(HIST, exist_ok=True)
CITIC = '0018'                                            # 中信期货席位（中信证券体系）
PRODUCTS = [('IF', '沪深300'), ('IH', '上证50'), ('IC', '中证500'), ('IM', '中证1000')]
HOLIDAYS = set()                                          # 如需排除调休节假日，在此添加 'YYYY-MM-DD'

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


# ---------- 中金所下载 ----------
def cffex_url(date8, product):
    return f"http://www.cffex.com.cn/sj/ccpm/{date8[:6]}/{date8[6:]}/{product}.xml?id={random.randint(1,99)}"


def download(product, date8, save_path):
    try:
        req = urllib.request.Request(cffex_url(date8, product), headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": "http://www.cffex.com.cn/cn/ccpm.html"})
        data = urllib.request.urlopen(req, timeout=30, context=CTX).read()
        if b'<positionRank' not in data[:600]:
            raise ValueError("返回非持仓XML（可能404/空）")
        with open(save_path, 'wb') as f:
            f.write(data)
        print(f"  下载成功 {product} {date8} ({len(data)} bytes)")
        return True
    except Exception as e:
        if os.path.exists(save_path):
            print(f"  下载失败 {product} {date8} ({e})，使用本地缓存")
            return True
        print(f"  下载失败且无缓存 {product} {date8}: {e}")
        return False


def data_available(date8):
    """探测某日 4 品种持仓 XML 是否均已发布。"""
    for code, _ in PRODUCTS:
        try:
            req = urllib.request.Request(cffex_url(date8, code), headers={
                "User-Agent": "Mozilla/5.0", "Referer": "http://www.cffex.com.cn/cn/ccpm.html"})
            d = urllib.request.urlopen(req, timeout=15, context=CTX).read()
            if b'<positionRank' not in d[:600]:
                return False
        except Exception:
            return False
    return True


def last_trading_day_before(d):
    while True:
        d -= datetime.timedelta(days=1)
        if d.weekday() >= 5:
            continue
        if d.strftime('%Y-%m-%d') in HOLIDAYS:
            continue
        return d


def ymd(d):
    return d.strftime('%Y%m%d')


# ---------- 解析（dt1=持买单量(多单), dt2=持卖单量(空单); dt0=套利分项, 不计入多空净持仓）----------
def parse(fn, mode):
    root = ET.parse(fn).getroot()
    b = s = 0
    for d in root.findall('data'):
        sn = d.find('shortname').text or ''
        if mode == 'citic' and '中信期货(代客)' not in sn:
            continue
        dt = d.find('datatypeid').text
        v = int(d.find('volume').text)
        if dt == '1':        # 1 = 持买单量（多单）
            b += v
        elif dt == '2':      # 2 = 持卖单量（空单）
            s += v
        # 0 = 套利，不计入多/空净持仓
    return (b, s)


def snapshot(day, mode):
    return {c: parse(os.path.join(HIST, f'{c}_{day}.xml'), mode) for c, _ in PRODUCTS}


# ---------- 解析：官方“比上交易日增减”字段（varvolume），用于净增对比 ----------
def var_snapshot(fn, mode):
    """读取当前日文件中的 varvolume（比上交易日增减）字段，按 dt1/dt2 求和。
    varvolume 已是中金所官方公布的当日相对其上交易日的增减，直接求和即得净增。
    （dt1=持买单量/多单，dt2=持卖单量/空单，dt0=套利不参与多空净增减）"""
    root = ET.parse(fn).getroot()
    b = s = 0
    for d in root.findall('data'):
        sn = d.find('shortname').text or ''
        if mode == 'citic' and '中信期货(代客)' not in sn:
            continue
        dt = d.find('datatypeid').text
        try:
            v = int(d.find('varvolume').text or 0)
        except (TypeError, ValueError):
            v = 0
        if dt == '1':        # 1 = 持买单量（多单）
            b += v
        elif dt == '2':      # 2 = 持卖单量（空单）
            s += v
        # 0 = 套利，不计入多/空净增减
    return (b, s)


# ---------- 净增对比：官方“比上交易日增减”字段直接求和 ----------
def net_change_var(cit_var, all_var):
    """用户指定算法：各品种“比上交易日增减”(varvolume) 直接相加。
    cit_var / all_var: dict product -> (buy_var_sum, sell_var_sum)
    返回 (中信行, 中信合计, 全市场行, 全市场合计)。"""
    def make(var_map):
        rows = []; tb = ts = 0
        for c, name in PRODUCTS:
            b, s = var_map[c]; net = b - s
            rows.append((name, b, s, net))
            tb += b; ts += s
        return rows, (tb, ts, tb - ts)
    cit_rows, cit_tot = make(cit_var)
    all_rows, all_tot = make(all_var)
    return cit_rows, cit_tot, all_rows, all_tot


# ---------- HTML 构建 ----------
def table_abs(title, snap):
    rows = ''; tb = ts = 0
    for code, name in PRODUCTS:
        b, s = snap[code]; net = b - s; tb += b; ts += s
        rows += f'<tr><td class="lbl">{name}</td><td>{b:,}</td><td>{s:,}</td>' \
                f'<td class="{"net-pos" if net >= 0 else "net-neg"}">{net:+,}</td></tr>'
    nt = tb - ts
    rows += f'<tr class="total"><td>合计</td><td>{tb:,}</td><td>{ts:,}</td>' \
            f'<td class="{"net-pos" if nt >= 0 else "net-neg"}">{nt:+,}</td></tr>'
    return f'<h3>{title}</h3><table><thead><tr><th>合约类型</th><th>多单(持买)</th>' \
           f'<th>空单(持卖)</th><th>净多空</th></tr></thead><tbody>{rows}</tbody></table>'


def table_diff(title, rows, tot):
    body = ''
    for name, db, ds, net in rows:
        body += f'<tr><td class="lbl">{name}</td>' \
                f'<td class="{"up" if db > 0 else ("down" if db < 0 else "")}">{db:+,}</td>' \
                f'<td class="{"up" if ds > 0 else ("down" if ds < 0 else "")}">{ds:+,}</td>' \
                f'<td class="{"net-pos" if net >= 0 else "net-neg"}">{net:+,}</td></tr>'
    tb, ts, nt = tot
    body += f'<tr class="total"><td>合计</td><td>{tb:+,}</td><td>{ts:+,}</td>' \
            f'<td class="{"net-pos" if nt >= 0 else "net-neg"}">{nt:+,}</td></tr>'
    return f'<h3>{title}</h3><table><thead><tr><th>合约类型</th><th>多单净增</th>' \
           f'<th>空单净增</th><th>净多空</th></tr></thead><tbody>{body}</tbody></table>'


def build_html(cur8, prev8, cit_cur, all_cur, cit_var, all_var):
    cit_rows, cit_tot, all_rows, all_tot = net_change_var(cit_var, all_var)

    def net(s): return sum(s[c][0] - s[c][1] for c, _ in PRODUCTS)
    cit_net, all_net = net(cit_cur), net(all_cur)          # 绝对净持仓（volume）
    cit_chg, all_chg = cit_tot[2], all_tot[2]              # 净增（varvolume 直接求和）
    bias = "偏多" if all_chg > 0 else ("偏空" if all_chg < 0 else "中性")
    biggest = max(PRODUCTS, key=lambda cp: abs(all_var[cp[0]][0] - all_var[cp[0]][1]))
    note = (f"<b>核心解读（数据驱动）：</b><br>"
            f"1. 整体{bias}：中信期货(代客)净持仓 <b>{cit_net:+,}</b> 手，净增 <b>{cit_chg:+,}</b> 手；"
            f"全市场前20名会员净持仓 <b>{all_net:+,}</b> 手，净增 <b>{all_chg:+,}</b> 手。<br>"
            f"2. 全市场维度净增绝对值最大的品种为 <b>{dict(PRODUCTS)[biggest[0]]}（{biggest[0]}）</b>，"
            f"多单净增 {all_var[biggest[0]][0]:+,}、"
            f"空单净增 {all_var[biggest[0]][1]:+,}。<br>"
            f"3. 中信席位在大盘（IF/IH）净增 <b>{sum(cit_var[c][0]-cit_var[c][1] for c,_ in PRODUCTS if c in ('IF','IH')):+,}</b> 手，"
            f"在小盘（IC/IM）净增 <b>{sum(cit_var[c][0]-cit_var[c][1] for c,_ in PRODUCTS if c in ('IC','IM')):+,}</b> 手。")

    method = ("<p class='method'><b>计算方法与口径（已按用户确认修正）：</b>"
              "① 多单 = 持买单量（datatypeid=1），空单 = 持卖单量（datatypeid=2），套利（datatypeid=0）不计入多空净持仓；"
              "② 绝对持仓用 volume（当日持仓量）字段直接求和；"
              "③ 净增对比用中金所官方“比上交易日增减”字段（varvolume）直接求和：多单净增 = Σ各品种(持买单量的比上交易日增减)，"
              "空单净增 = Σ各品种(持卖单量的比上交易日增减)，净多空 = 多单净增 − 空单净增。"
              "varvolume 已由交易所计入合约上市/退市、会员进出前20名等边界，比“当日−前日”自行相减更准（尤其全市场前20合并维度）。"
              "④ 中信维度仅取“中信期货(代客)”席位（shortname 精确匹配，自动排除自营及其他会员）。</p>")

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>股指期货持仓统计 {cur8}</title>
<style>
body{{font-family:-apple-system,"Microsoft YaHei",sans-serif;background:#f5f7fa;color:#1f2d3d;margin:0;padding:24px;}}
.card{{background:#fff;border-radius:12px;padding:24px;margin:0 auto 24px;max-width:880px;box-shadow:0 2px 12px rgba(0,0,0,.06);}}
h1{{font-size:22px;margin:0 0 4px;color:#0d47a1;}}
.sub{{color:#607d8b;font-size:13px;margin-bottom:20px;}}
h2{{font-size:17px;color:#1565c0;border-left:4px solid #1565c0;padding-left:10px;margin:28px 0 12px;}}
h3{{font-size:15px;margin:18px 0 8px;color:#37474f;}}
table{{width:100%;border-collapse:collapse;font-size:14px;margin-bottom:8px;}}
th,td{{padding:10px 8px;text-align:right;border-bottom:1px solid #eceff1;}}
th{{background:#e3f2fd;color:#0d47a1;font-weight:600;}}
td.lbl,th:first-child{{text-align:left;}}
tr.total td{{font-weight:700;background:#f1f8e9;border-top:2px solid #c5e1a5;}}
.net-pos{{color:#c62828;font-weight:600;}}
.net-neg{{color:#2e7d32;font-weight:600;}}
.up{{color:#c62828;}}
.down{{color:#2e7d32;}}
.method{{font-size:12px;color:#455a64;background:#eef6ff;padding:12px;border-radius:8px;margin:6px 0 14px;line-height:1.7;}}
.note{{font-size:13px;color:#37474f;line-height:1.8;margin-top:18px;background:#fafafa;padding:14px;border-radius:8px;}}
.disc{{font-size:11px;color:#90a4ae;margin-top:20px;border-top:1px dashed #cfd8dc;padding-top:12px;}}
</style></head>
<body>
<div class="card">
<h1>中国金融期货交易所 · 股指期货持仓统计</h1>
<div class="sub">统计基准日：{cur8}｜ 对比前一交易日：{prev8}<br>
数据来源：中金所官网 cffex.com.cn 会员持仓排名（前20名会员）｜ 维度一：中信期货(代客)（席位码0018）；维度二：全市场前20名会员合并</div>

<h2>一、当日绝对持仓（{cur8}）</h2>
{table_abs('① 中信期货(代客)（席位码0018）', cit_cur)}
{table_abs('② 全市场前20名会员合并', all_cur)}

<h2>二、净增对比（{cur8} vs {prev8}）</h2>
{method}
{table_diff('① 中信期货(代客)（席位码0018）', cit_rows, cit_tot)}
{table_diff('② 全市场前20名会员合并', all_rows, all_tot)}

<div class="note">{note}</div>
<div class="disc">
说明：① "全市场前20名会员合并"为中金所公开的前20名会员持仓加总（官网仅披露前20名），非严格全市场；② 数据为盘后滞后指标、含大量套保盘，仅作风格参考；③ 中信维度取"中信期货(代客)"经纪业务持仓，不代表自营方向；④ 套利持仓(datatypeid=0)不计入多空净持仓。<br>
免责声明：以上内容基于中金所公开数据自动生成，仅供参考，不构成投资建议。市场有风险，投资需谨慎。
</div>
</div>
</body></html>"""


# ---------- 主流程 ----------
def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    quiet = '--quiet' in sys.argv[1:]

    if len(args) >= 2:
        cur8, prev8 = args[0], args[1]
    else:
        today = datetime.date.today()
        if today.weekday() >= 5 or today.strftime('%Y-%m-%d') in HOLIDAYS:
            print(f"[跳过] 今日 {today} 非交易日，不执行统计。")
            sys.exit(10)
        target = today
        if not data_available(ymd(target)):
            target = last_trading_day_before(today)
            if not data_available(ymd(target)):
                target = last_trading_day_before(target)
        prior = last_trading_day_before(target)
        cur8, prev8 = ymd(target), ymd(prior)

    print(f"当前日={cur8}  对比前日={prev8}")

    ok = True
    for code, _ in PRODUCTS:
        for day in (cur8, prev8):
            if not download(code, day, os.path.join(HIST, f'{code}_{day}.xml')):
                ok = False
    if not ok:
        print("[错误] 关键数据缺失，终止。")
        sys.exit(20)

    cit_cur = snapshot(cur8, 'citic')
    all_cur = snapshot(cur8, 'all')
    cit_var = {c: var_snapshot(os.path.join(HIST, f'{c}_{cur8}.xml'), 'citic') for c, _ in PRODUCTS}
    all_var = {c: var_snapshot(os.path.join(HIST, f'{c}_{cur8}.xml'), 'all') for c, _ in PRODUCTS}
    cit_rows, cit_tot, all_rows, all_tot = net_change_var(cit_var, all_var)

    if not quiet:
        def ptable(label, rows, tot):
            print(f"\n=== {label} ===")
            print(f"{'合约':8}{'多单净增':>12}{'空单净增':>12}{'净多空':>12}")
            for n, db, ds, nt in rows:
                print(f"{n:8}{db:>+12,}{ds:>+12,}{nt:>+12,}")
            print(f"{'合计':8}{tot[0]:>+12,}{tot[1]:>+12,}{tot[2]:>+12,}")
        ptable('① 中信期货席位(0018)', cit_rows, cit_tot)
        ptable('② 全市场前20会员合并', all_rows, all_tot)

    html = build_html(cur8, prev8, cit_cur, all_cur, cit_var, all_var)
    fn = f'股指期货持仓统计_{cur8}.html'
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n[完成] 报告已生成：{fn}  ({len(html)} bytes)")


if __name__ == '__main__':
    main()
