#!/usr/bin/env python3
import json, os, sys
from datetime import datetime

def build_recs(recs):
    lines = []
    star = chr(9733)
    for i, r in enumerate(recs, 1):
        lines.append("### {0}. 【{1}】 适合指数：{2}".format(
            i, r.get('title','方向'+str(i)), star * r.get('score', 3)))
        for k, v in [('推荐理由', r.get('reason','')),
                      ('AI评级', r.get('ai_rating','')),
                      ('薪资参考', r.get('salary','')),
                      ('入门路径', r.get('path','')),
                      ('3年预期', r.get('expectation','')),
                      ('潜在风险', r.get('risk',''))]:
            if v: lines.append("- **{0}**：{1}".format(k, v))
        lines.append('')
    return '\n'.join(lines)

def generate_report(data):
    today = datetime.now().strftime('%Y-%m-%d')
    ai = data.get('ai_guide', {})
    acts = data.get('actions', {})
    recs_md = build_recs(data.get('recommendations', []))
    md = [
        '# 个性化职业规划报告',
        '',
        '> 生成日期：' + today,
        '',
        '---',
        '',
        '## 基础档案',
        '',
        '- 昵称：' + data.get('nickname','未提供'),
        '- 当前阶段：' + data.get('stage','未提供'),
        '- 霍兰德代码：' + data.get('holland','未测评'),
        '- MBTI类型：' + data.get('mbti','未测评'),
        '- 职业锚：' + data.get('anchor','未测评'),
        '- 核心价值观：' + data.get('values','未明确'),
        '- 城市：' + data.get('city','未提供'),
        '',
        '---',
        '',
        '## 职业方向推荐',
        '',
        recs_md,
        '',
        '## AI时代生存指南',
        '',
        '- 核心技能：' + ai.get('skills','详见推荐职业'),
        '- 必学AI工具：' + ai.get('tools','暂无'),
        '- 建议认证：' + ai.get('cert','暂无'),
        '',
        '## 下一步行动清单',
        '',
        '- 今天：' + acts.get('today','暂无'),
        '- 1个月内：' + acts.get('1month','暂无'),
        '- 3个月内：' + acts.get('3months','暂无'),
        '- 1年内：' + acts.get('1year','暂无'),
        '',
        '---',
        '',
        '由 AI时代职业规划师 v1.4 生成'
    ]
    return '\n'.join(md)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='{}')
    p.add_argument('--output-dir', default='.')
    args = p.parse_args()
    data = json.loads(args.data)
    md = generate_report(data)
    ds = datetime.now().strftime('%Y%m%d')
    path = os.path.join(args.output_dir, '职业规划报告_' + ds + '.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(md)
    print('Markdown: ' + path)
