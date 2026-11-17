#!/usr/bin/env python3
"""Step 2: 离线精解析 cards_full.json → 结构化房源数据 final_records.json
（电话优先从房源 ID 提取，其次从卡片 HTML 全局电话库提取）
用法: python3 parse_final.py [--config path/to/config.json]
"""
import json, re, os, pathlib, sys

BASE = pathlib.Path(__file__).resolve().parent

def load_config():
    """查找 config.json：--config 参数 > 当前目录 > 脚本目录 > skill 根目录"""
    cfg_path = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--config":
        cfg_path = pathlib.Path(sys.argv[2])
    else:
        for cand in [pathlib.Path.cwd() / "config.json",
                     BASE / "config.json",
                     BASE.parent / "config.json"]:
            if cand.exists():
                cfg_path = cand
                break
    if cfg_path is None:
        sys.exit("未找到 config.json：请复制 config.example.json 为 config.json 后重试，或用 --config 指定路径")
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    cfg.setdefault("output_dir", str(cfg_path.parent / "output"))
    os.makedirs(cfg["output_dir"], exist_ok=True)
    return cfg

CFG = load_config()
OUT = CFG["output_dir"].rstrip("/") + "/"

cards = json.load(open(OUT + "cards_full.json"))
print(f"卡片数: {len(cards)}")

# 全局电话库：从所有卡片 HTML 提取
all_html = "\n".join(c['html'] for c in cards)
html_phones = set(re.findall(r'1[3-9]\d{9}', all_html))
print(f"HTML 全局唯一电话: {len(html_phones)}")

def phone_from_id(url):
    m = re.search(r'/fangyuan/(\d+)', url)
    if not m:
        return ''
    phones = re.findall(r'1[3-9]\d{9}', m.group(1))
    return phones[0] if phones else ''

def parse_card(c):
    text = c['text']
    href = c['href']
    html = c['html']
    t = re.sub(r'\s+', ' ', text)
    rec = {
        'url': href.split('?')[0],
        'full_url': href,
        'id': (re.search(r'/fangyuan/(\d+)', href) or [None, ''])[1] if re.search(r'/fangyuan/(\d+)', href) else '',
    }
    # 电话：ID 提取优先，其次卡片 HTML 内电话（排除 ID 里的）
    ph = phone_from_id(href)
    if not ph:
        ids = rec['id']
        for p in re.findall(r'1[3-9]\d{9}', html):
            if ids and p in ids:
                continue
            ph = p
            break
    rec['phone'] = ph

    segs = [s.strip() for s in re.split(r'[|｜]', t) if s.strip()]
    rec['title'] = segs[0] if segs else ''
    # 标签
    tags = re.findall(r'(安选|实拍真房|实拍|验真|视频看房|个人房源|经纪人房源|公寓|VR看房|近地铁|新上|降价|随时看房|拎包入住)', t)
    rec['tags'] = list(dict.fromkeys(tags))
    # 房型/面积/楼层
    m = re.search(r'(\d室\d厅(?:\d卫)?|\d室\d厅|\d室|\d居室|\d房\d厅).*?(\d+(?:\.\d+)?平米).*?((?:高|中|低)层\(共\d+层\)|(?:高|中|低)楼层)', t)
    if m:
        rec['model'], rec['area'], rec['floor'] = m.group(1), m.group(2), m.group(3)
    # 小区 + 区域
    m2 = re.search(r'([\u4e00-\u9fa5A-Za-z0-9·]+(?:苑|园|城|府|中心|国际|广场|小区|里|庭|湾|台|郡|汇|都|轩|阁|居|家|世界|公寓|名邸|华庭|山庄|堡|岸|院|区|路|街|村|镇|座|号|二期|三期|一期|组团|天地|公馆|花园|星座|领域|晶|大厦|综合楼))(?:\s+|)((?:两江新区|渝北|江北|南岸|沙坪坝|九龙坡|渝中|巴南|北碚|大渡口|江津|璧山|万州|涪陵)[\u4e00-\u9fa5A-Za-z0-9\-·]*)', t)
    if m2:
        rec['community'] = m2.group(1)
        rec['district'] = m2.group(2)
    else:
        # 兜底：any 中文词组后跟 区名-xxx
        m2b = re.search(r'([\u4e00-\u9fa5A-Za-z0-9]{2,12})\s+((?:两江新区|渝北|江北|南岸|沙坪坝|九龙坡|渝中|巴南|北碚|大渡口|江津|璧山)[\u4e00-\u9fa5A-Za-z0-9\-·]*)', t)
        if m2b:
            rec['community'] = m2b.group(1)
            rec['district'] = m2b.group(2)
    # 整租/合租
    rec['rent_type'] = '整租' if '整租' in t else ('合租' if '合租' in t else '')
    # 朝向
    m3 = re.search(r'朝(东|南|西|北|东南|东北|西南|西北)', t)
    rec['orientation'] = m3.group(0) if m3 else ''
    rec['elevator'] = '有电梯' if '有电梯' in t else ('无电梯' if '无电梯' in t else '')
    # 地铁
    m4 = re.search(r'(\d{1,2}号线[东南西北]?|\d{1,2}号线)', t)
    rec['metro'] = m4.group(1) if m4 else ''
    # 租金（支持区间）
    m5 = re.search(r'(\d+(?:\.\d+)?)\s*(?:-|—|~|到)\s*(\d+(?:\.\d+)?)\s*元/月|(\d+(?:\.\d+)?)\s*元/月', t)
    if m5:
        if m5.group(1) and m5.group(2):
            rec['rent_min'], rec['rent_max'] = float(m5.group(1)), float(m5.group(2))
        elif m5.group(3):
            rec['rent_min'] = rec['rent_max'] = float(m5.group(3))
    # 联系人
    m6 = re.search(r'([\u4e00-\u9fa5]{2,4})\s*[|｜]?\s*(\d[\d\- ]*元/月|\d+-\d+\s*元/月)', t)
    if m6:
        rec['contact'] = m6.group(1)
    else:
        m6b = re.search(r'[|｜]\s*([\u4e00-\u9fa5]{2,4})\s*[|｜]\s*\d', t)
        if m6b:
            rec['contact'] = m6b.group(1)
    # 付款/交付方式
    pay = re.findall(r'(押一付一|押一付二|押一付三|押一付半年|押二付一|半年付|年付|季付|月付|可月付|免中介|无中介)', t)
    rec['pay'] = list(dict.fromkeys(pay))
    return rec

records = [parse_card(c) for c in cards]
# 按 ID 去重
seen, uniq = set(), []
for r in records:
    if r['id'] and r['id'] not in seen:
        seen.add(r['id'])
        uniq.append(r)
print(f"最终记录: {len(uniq)}")

fields = ['title', 'model', 'area', 'community', 'district', 'rent_type',
          'orientation', 'contact', 'rent_min', 'phone', 'pay', 'metro', 'elevator']
for f in fields:
    print(f"  {f}: {sum(1 for r in uniq if r.get(f))}/{len(uniq)}")

with open(OUT + "final_records.json", "w") as f:
    json.dump(uniq, f, ensure_ascii=False, indent=1)
print("\n样例:")
for r in uniq[:3]:
    print({k: r[k] for k in ['title', 'community', 'district', 'model', 'area',
                             'rent_min', 'rent_max', 'contact', 'phone', 'pay', 'metro']})
