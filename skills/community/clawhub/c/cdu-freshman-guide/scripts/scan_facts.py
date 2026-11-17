#!/usr/bin/env python3
"""定向检索脱敏数据中的高价值事实（排除广告/代课噪音）。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / 'data' / 'raw_desensitized'

# 定向事实 → 检索正则（命中即打印，最多 N 条）
QUERIES = {
    '宿舍功率/限电': [r'功率', r'限电', r'800w', r'800W', r'跳闸', r'电费'],
    '选床位/选舍友': [r'选床位', r'选舍友', r'床位', r'室友.*选|选.*室友', r'小程序.*寝室'],
    '报到流程': [r'报到', r'报到流程', r'报到证', r'入学流程'],
    '转专业流程': [r'转专业.*(流程|条件|要求|申请|成功|难)', r'(流程|条件|要求|申请).*转专业'],
    '空调': [r'空调.*(租|费|钱|装|遥控|押金)', r'(租|装).*空调'],
    '热水/洗澡': [r'热水.*(时间|几点|供应|停)', r'洗澡.*(时间|几点|钱|费)', r'浴室'],
    '军训': [r'军训.*(时间|几天|什么时候|鞋|衣服|防晒|免训)', r'(什么时候|几天).*军训'],
    '医保': [r'医保.*(怎么|报销|买|交|多少钱|在哪)', r'(怎么|如何).*医保'],
    '校园卡/一卡通': [r'一卡通.*(充值|补办|挂失|在哪|怎么)', r'校园卡.*(充值|补办|挂失|在哪|怎么)'],
    '宽带/校园网': [r'宽带.*(办|装|钱|月|套餐)', r'校园网.*(怎么|钱|月|套餐|连)'],
    '学生证': [r'学生证.*(照片|贴|办|补)', r'(照片|办|补).*学生证'],
    '体检': [r'体检.*(什么时候|在哪|项目|钱)', r'(什么时候|在哪).*体检'],
    '床上用品': [r'被子.*(带|买|学校|发)', r'床上用品.*(带|买)', r'床垫.*(带|买)'],
    '上课作息': [r'几点上课', r'上课时间', r'作息时间', r'早八', r'晚自习'],
    '食堂': [r'食堂.*(好吃|推荐|几楼|几点)', r'(好吃|推荐).*食堂'],
    '图书馆': [r'图书馆.*(开放|几点|借书|预约)', r'(开放|几点).*图书馆'],
    '快递': [r'快递.*(在哪|地址|驿站|怎么填)', r'(在哪|地址).*快递'],
    '成绩/绩点': [r'绩点.*(怎么|多少|算)', r'挂科.*(影响|后果|重修)', r'补考.*(时间|怎么)'],
    '毕业学分': [r'毕业.*(学分|要求)', r'学分.*(要求|多少|怎么)'],
    '实习/社会实践': [r'社会实践.*(怎么|要求|学分)', r'实习.*(怎么|要求|大几)'],
    '考研/保研': [r'保研.*(条件|名额|怎么)', r'考研.*(准备|什么时候|大几)'],
    '社团': [r'社团.*(怎么|加入|招新|什么时候)', r'(怎么|如何).*社团'],
    '兼职': [r'兼职.*(怎么|哪里|找)', r'勤工俭学'],
    '防骗': [r'诈骗|骗子|反诈|被骗|防骗'],
    '宿舍查寝': [r'查寝.*(几点|怎么|查什么)', r'(几点|怎么).*查寝'],
    '请假': [r'请假.*(流程|怎么|多久)', r'(怎么|如何).*请假'],
    '学费': [r'学费.*(多少|怎么交|什么时候)', r'(多少|怎么交).*学费'],
    '银行卡': [r'银行卡.*(哪个|什么银行|办)', r'(哪个|什么银行).*银行卡'],
}

AD_NOISE = re.compile(r'代课|代取|代写|代做|代抢|代刷|代考|代签|办卡|卖被子|驾校|校园墙|跳蚤|代跑|代测|代看|代听|代买|代充|挂证|论文|毕设|题库|有偿|私我|加我|滴滴|老登|学长学姐.*(办|卖|出)|出.*(鞋|衣服|外套|书)|免费送|售后|拼车|拼单')


def iter_messages():
    for f in sorted(RAW.glob('group_*.json')):
        if f.name == 'desensitize_report.json':
            continue
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
        except Exception:
            continue
        gname = data.get('chatInfo', {}).get('name', f.stem)
        for m in data.get('messages', []):
            if m.get('recalled') or m.get('system'):
                continue
            text = (m.get('content') or {}).get('text', '') or ''
            if not text or len(text) < 8:
                continue
            yield gname, m.get('time', ''), text


def main() -> int:
    for topic, pats in QUERIES.items():
        regex = re.compile('|'.join(pats))
        print(f'\n===== {topic} =====')
        seen = set()
        count = 0
        for gname, time, text in iter_messages():
            if not regex.search(text):
                continue
            if AD_NOISE.search(text):
                continue
            key = text[:40]
            if key in seen:
                continue
            seen.add(key)
            print(f'  [{gname} {time}] {text[:120]}')
            count += 1
            if count >= 5:
                break
        if count == 0:
            print('  （无有效内容）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
