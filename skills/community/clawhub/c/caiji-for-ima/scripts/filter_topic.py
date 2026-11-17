# -*- coding: utf-8 -*-
"""方法论素材筛选：理论/模型/方法/模板/工具/范式/综述等。复用去重+URL编码+分批。"""
import json, re, sys, difflib
from pathlib import Path
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')
BASE = Path.cwd()

DOMAIN = ['科研', '论文', '学术', '研究', '课题', '写作', '发表', '期刊', '文献', '读博', '博士',
          '研究生', '硕士', '基金', '申报', '选题', '综述', '投稿', '审稿', '引用', '核心', 'cssci',
          'sci', 'ssci', '项目', '学科', '教学', '教师', '高校', '大学', '方法', '数据', '实证',
          '问卷', '访谈', '质性', '量化', '统计', '实验', '开题', '答辩', '文献计量', 'meta', 'c刊', '专著']
METH = ['理论', '模型', '方法', '模板', '工具', '框架', '范式', '综述', '设计', '流程', '规范',
        '格式', '量表', '问卷', '编码', '信度', '效度', '抽样', '元分析', '扎根', '案例研究',
        '内容分析', '混合研究', 'SOP', '结构', '选题', '写作', '引用', '文献综述', '研究设计',
        '实证', '质性', '量化', '路径', '机制', '维度', '变量', '假设', '访谈提纲', '编码方案',
        '分析框架', '方法论', '模版', '常用', '经典']
JUNK = ['减肥', '瑜伽', '健身', '护肤', '美食', '旅游', '母婴', '理财', '股票', '楼市', '穿搭',
        '星座', '情感', '相亲', '恋爱', '副业', '微商', '带货', '高考志愿', '四六级', '竞赛',
        '秋招', '薪资', '抗癌', '养生', '中医', '西医', '降压', '血压', '糖尿病', '抗衰', '美白']
AD = ['学习班', '培训班', '研修班', '招生', '报名', '开班', '训练营', '辅导班', '速成', '代写',
      '包过', '包发', '套餐', '优惠', '限时', '扫码', '加微信', '领取资料', '讲座通知', '会议通知',
      '论坛通知', '线上直播', '直播课', '免费直播', '征文通知', '征稿启事', '培训课程', '招生简章',
      '面授', '收费标准', '加盟', '代理', '招商', '带货', '直销']
# 与科研方法论无关的中小学/育儿类
K12 = ['中小学', '中学', '小学', '幼儿园', '家长', '育儿', '亲子', '班主任', '义务教育', '中考', '高考']


def norm(t):
    t = re.sub(r'[【】\[\]（）()《》""\'\'、，,。.！!？?：:；;~～\-—_|/\\\s]+', '', t)
    return t.lower().strip()


def score(a):
    title = a.get('title', '')
    text = title + ' ' + a.get('summary', '')
    if any(j in title for j in JUNK):
        return -1
    if any(ad in title for ad in AD):
        return -1
    if any(k in title for k in K12):
        return -1
    if '通知' in title and len(title) > 25:
        return -1
    dt = sum(1 for w in DOMAIN if w in title)
    if dt < 1:
        return -1  # 必须命中领域词
    mt = sum(1 for w in METH if w in title)
    if mt < 1:
        return -1  # 必须命中方法论词，保证主题纯度
    m = sum(1 for w in METH if w in text)
    return dt * 3 + mt * 5 + min(m, 6) + min(len(text) // 40, 4)


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else 'out2'
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    arts = json.load(open(BASE / tag / 'all_articles.json', encoding='utf-8'))
    print('候选总数:', len(arts))

    exist = []
    tp = BASE / 'existing' / 'titles.txt'
    if tp.exists():
        exist = [norm(x) for x in tp.read_text(encoding='utf-8').split('\n') if x.strip()]
    print('已有标题池(01素材区):', len(exist))

    scored = []
    for a in arts:
        s = score(a)
        if s > 0:
            a['_score'] = s
            scored.append(a)
    scored.sort(key=lambda x: -x['_score'])
    print('主题命中:', len(scored))

    # 排除已导入01素材区的URL（避免跨文件夹重复同一篇）
    imported = set()
    for f in ['batches_out.json', 'batches_extra.json']:
        fp = BASE / f
        if fp.exists():
            for b in json.load(open(fp, encoding='utf-8')):
                imported.update(b['urls'])

    seen_url, seen_title, uniq = set(), [], []
    for a in scored:
        nt = norm(a['title'])
        if a['url'] in seen_url:
            continue
        dup = False
        for t in seen_title:
            if difflib.SequenceMatcher(None, nt, t).ratio() > 0.72:
                dup = True
                break
        if dup:
            continue
        seen_url.add(a['url'])
        seen_title.append(nt)
        uniq.append(a)
    print('内部去重后:', len(uniq))
    uniq = [a for a in uniq if a['url'] not in imported]
    print('排除已导入01后:', len(uniq))

    kept, dropped = [], []
    for a in uniq:
        nt = norm(a['title'])
        hit = None
        for et in exist:
            if not et:
                continue
            r = difflib.SequenceMatcher(None, nt, et).ratio()
            if r > 0.72:
                hit = (et, round(r, 2)); break
            if len(nt) > 8 and nt in et:
                hit = (et, 1.0); break
        if hit:
            dropped.append((a['title'], hit[0], hit[1]))
        else:
            kept.append(a)
    print('与已有素材去重后:', len(kept), ' 剔除:', len(dropped))

    if limit:
        kept = kept[:limit]

    with open(BASE / f'kept_{tag}.json', 'w', encoding='utf-8') as f:
        json.dump(kept, f, ensure_ascii=False, indent=2)
    with open(BASE / f'dropped_{tag}.txt', 'w', encoding='utf-8') as f:
        for t, e, r in dropped:
            f.write(f'{t}\t||\t{e}\t||\t{r}\n')

    def fix(u):
        return quote(u, safe=":/?&=%~#+,-_.!*'();@$=,")

    batches = [kept[i:i + 10] for i in range(0, len(kept), 10)]
    tasks = [{'batch': i + 1, 'urls': [fix(a['url']) for a in b], 'titles': [a['title'] for a in b]}
             for i, b in enumerate(batches)]
    with open(BASE / f'batches_{tag}.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    print('批次数:', len(tasks), ' 总URL:', sum(len(b['urls']) for b in tasks))
    print('\n前40条入选样例:')
    for a in kept[:40]:
        print(f"  [{a['_score']}] {a['title'][:52]} | {a['source']} | {a['date']}")


main()
