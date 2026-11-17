#!/usr/bin/env python3
"""扫描脱敏后的群聊数据，找出知识库尚未覆盖的高价值主题。

用法:
  python scripts/scan_kb_gaps.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / 'data' / 'raw_desensitized'

# 目标主题 → 关键词（命中任一即输出该条消息）
TOPICS = {
    '报到/开学流程': ['报到', '开学流程', '入学', '迎新', '报名点', '报到流程'],
    '选课系统/教务系统': ['教务系统', '选课系统', '抢课', '选课时间', '退课', '改选'],
    '转专业': ['转专业', '转系'],
    '一卡通/校园卡': ['一卡通', '校园卡', '饭卡', '水卡', '洗澡卡'],
    '空调/热水': ['空调', '热水', '洗澡', '浴室', '淋浴'],
    '社团招新': ['社团招新', '百团', '招新', '社团'],
    '新生体检': ['体检', '复检'],
    '床上用品': ['床上用品', '被褥', '床垫', '蚊帐', '被子'],
    '宽带办理': ['宽带', '办网', '装网', '路由器'],
    '快递': ['快递', '驿站', '取件'],
    '军训': ['军训', '军姿', '迷彩'],
    '宿舍分配': ['宿舍分配', '分宿舍', '几人间', '宿舍号', '床位'],
    '英语分级/摸底': ['英语分级', '摸底', '分班考', '英语测试'],
    '体育课': ['体育课', '选体育', '体测', '跑步打卡'],
    '图书馆': ['图书馆', '借书', '自习', '占座'],
    '校园交通': ['校车', '公交', '地铁', '摆渡车', '共享单车'],
    '食堂': ['食堂', '餐厅', '吃饭', '美食'],
    '打印/复印': ['打印', '复印', '文印'],
    '银行卡/学费': ['学费', '缴费', '银行卡', '交费'],
    '医保/社保': ['医保', '社保', '报销'],
    '学生证': ['学生证', '学生卡'],
    '入党/团': ['入党', '积极分子', '团员', '团组织'],
    '兼职/勤工俭学': ['兼职', '勤工', '家教', '打工'],
    '考试/绩点': ['绩点', 'GPA', '挂科', '补考', '期末'],
    '开学必备物品': ['必备', '清单', '要带', '带什么'],
    '宿舍电器/功率': ['功率', '电费', '跳闸', '限电'],
    '上课时间/作息': ['上课时间', '作息', '课表', '几点上课'],
    '校园卡充值': ['充值', '圈存', '缴费'],
    '成绩查询': ['成绩查询', '查成绩', '成绩单'],
    '毕业要求/学分': ['学分', '毕业要求', '培养方案', '必修'],
    '实习': ['实习', '暑期实践', '社会实践'],
    '考研': ['考研', '保研', '研究生'],
    '就业/招聘': ['招聘', '校招', '双选会', '就业'],
    '宿舍报修': ['报修', '维修', '坏了'],
    '门禁/晚归': ['门禁', '晚归', '夜不归宿', '查寝'],
    '请假': ['请假', '销假', '续假'],
    '快递代收/代取': ['代取', '代收'],
    '二手交易': ['出', '收', '转让', '闲置', '二手'],
    '拼车/拼单': ['拼车', '拼单', '拼'],
    '校园活动': ['活动', '讲座', '比赛', '晚会'],
    '心理/咨询': ['心理', '咨询', '辅导'],
    '安全/防骗': ['诈骗', '防骗', '反诈', '骗子'],
    '宿舍关系/室友': ['室友', '舍友', '矛盾'],
    '外卖': ['外卖', '配送'],
    '洗衣机': ['洗衣机', '洗衣'],
    '超市/购物': ['超市', '便利店', '购物'],
    '药店/看病': ['药店', '看病', '校医院', '挂号'],
    '手机卡/运营商': ['移动', '联通', '电信', '手机卡', '流量'],
}

# 排除的群（空群/无内容）
SKIP_GROUPS = {
    '教务系统选课咨询群', '校园媒体联合会', '文新学院第62期青马培训',
    '2024成都大学新生交流群',
}

# 排除的发送者昵称模式（广告/机器人）
AD_PATTERNS = [re.compile(p) for p in (r'^\[同学\]$',)]


def iter_messages():
    for f in sorted(RAW.glob('group_*.json')):
        if f.name == 'desensitize_report.json':
            continue
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
        except Exception:
            continue
        gname = data.get('chatInfo', {}).get('name', f.stem)
        if gname in SKIP_GROUPS:
            continue
        for m in data.get('messages', []):
            if m.get('recalled') or m.get('system'):
                continue
            text = (m.get('content') or {}).get('text', '') or ''
            if not text:
                continue
            yield gname, m.get('time', ''), text


def main() -> int:
    hits: dict[str, list[tuple[str, str, str]]] = {t: [] for t in TOPICS}
    for gname, time, text in iter_messages():
        for topic, kws in TOPICS.items():
            if any(kw in text for kw in kws):
                hits[topic].append((gname, time, text))

    print(f'{"主题":<14} {"命中数":>6}  示例')
    print('-' * 90)
    for topic, items in hits.items():
        if not items:
            continue
        # 去重示例（同一群同一主题只取前 3 条）
        seen = set()
        samples = []
        for gname, time, text in items:
            key = (gname, text[:30])
            if key in seen:
                continue
            seen.add(key)
            samples.append((gname, time, text))
            if len(samples) >= 3:
                break
        print(f'{topic:<14} {len(items):>6}  |  ' + ' || '.join(
            f'[{g}] {t} {s[:40]}' for g, t, s in samples))
    return 0


if __name__ == '__main__':
    sys.exit(main())
