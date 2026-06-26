#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站弹幕舆情分析工具
提取指定视频的所有弹幕，准备数据供大模型分析舆情与节奏
"""

import re
import json
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from collections import Counter

import requests

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'Origin': 'https://www.bilibili.com'
}


def extract_bvid(url_or_bvid: str) -> str:
    """从URL或字符串中提取BV号"""
    if url_or_bvid.startswith("BV"):
        return url_or_bvid
    match = re.search(r'BV[\w]+', url_or_bvid)
    if match:
        return match.group()
    raise ValueError(f"无法从 '{url_or_bvid}' 中提取BV号")


def get_video_info(bvid: str) -> dict:
    """获取视频信息"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
    data = resp.json()
    if data['code'] == 0:
        info = data['data']
        return {
            'bvid': bvid,
            'title': info.get('title', '未知标题'),
            'desc': info.get('desc', ''),
            'owner': info.get('owner', {}).get('name', '未知UP主'),
            'stat': info.get('stat', {}),
            'duration': info.get('duration', 0),
            'cid': info.get('cid', 0),
            'pubdate': info.get('pubdate', 0)
        }
    raise ValueError(f"获取视频信息失败: {data.get('message', 'Unknown error')}")


def get_danmakus(cid: str) -> list:
    """获取视频所有弹幕"""
    url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
    resp.encoding = 'utf-8'
    danmakus = []

    type_map = {1: '滚动', 4: '底端', 5: '顶端', 6: '逆向', 7: '高级', 8: '代码'}

    try:
        root = ET.fromstring(resp.text)
        for d in root.findall('d'):
            p = d.get('p', '').split(',')
            if len(p) >= 5:
                danmakus.append({
                    'text': d.text or '',
                    'time': float(p[0]),
                    'type': type_map.get(int(p[1]), '未知'),
                    'type_code': int(p[1]),
                    'color': p[3],
                    'timestamp': int(p[4])
                })
    except ET.ParseError:
        import zlib
        try:
            decompressed = zlib.decompress(resp.content)
            root = ET.fromstring(decompressed.decode('utf-8'))
            for d in root.findall('d'):
                p = d.get('p', '').split(',')
                if len(p) >= 5:
                    danmakus.append({
                        'text': d.text or '',
                        'time': float(p[0]),
                        'type': type_map.get(int(p[1]), '未知'),
                        'type_code': int(p[1]),
                        'color': p[3],
                        'timestamp': int(p[4])
                    })
        except Exception as e:
            print(f"弹幕解压解析失败: {e}")

    return danmakus


def format_time(seconds: float) -> str:
    """将秒数格式化为 mm:ss 或 hh:mm:ss"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def segment_danmakus_by_time(danmakus: list, duration: int, segment_count: int = 10) -> list:
    """将弹幕按时间分段"""
    if duration <= 0 or not danmakus:
        return []
    segment_duration = duration / segment_count
    segments = []
    for i in range(segment_count):
        start = i * segment_duration
        end = (i + 1) * segment_duration
        segment_danmakus = [d for d in danmakus if start <= d.get('time', 0) < end]
        segments.append({
            'segment_index': i + 1,
            'start_time': format_time(start),
            'end_time': format_time(end),
            'count': len(segment_danmakus),
            'danmakus': segment_danmakus
        })
    return segments


def prepare_analysis_data(video_info: dict, danmakus: list) -> dict:
    """准备用于大模型分析的弹幕数据"""
    duration = video_info.get('duration', 0)

    # 按时间分段
    segments = segment_danmakus_by_time(danmakus, duration, segment_count=10)

    # 弹幕类型分布
    type_counter = Counter([d.get('type', '未知') for d in danmakus])

    # 计算情感关键词统计
    positive_keywords = ['牛', '强', '棒', '好', '赞', '顶', '泪目', '感动', '喜欢', '爱', '甜', '炸', '绝', '完美', '厉害', '超']
    negative_keywords = ['烂', '差', '垃圾', '废物', '蠢', '尴尬', '难', '崩', '无语', '失望', '难看', '无聊', '扯', '假']
    question_keywords = ['？', '?', '怎么', '为什么', '什么', '如何', '是不是', '能不能']

    positive_count = sum(1 for d in danmakus if any(kw in d.get('text', '') for kw in positive_keywords))
    negative_count = sum(1 for d in danmakus if any(kw in d.get('text', '') for kw in negative_keywords))
    question_count = sum(1 for d in danmakus if any(kw in d.get('text', '') for kw in question_keywords))

    # 按时间顺序整理弹幕文本（取样，每段最多20条）
    sampled_danmakus = []
    for seg in segments:
        seg_danmakus = seg['danmakus']
        # 按时间排序
        seg_danmakus = sorted(seg_danmakus, key=lambda x: x.get('time', 0))
        # 每段最多取20条
        for d in seg_danmakus[:20]:
            sampled_danmakus.append({
                'time': format_time(d['time']),
                'seconds': d['time'],
                'text': d['text'],
                'type': d.get('type', '滚动')
            })

    analysis_data = {
        'video': {
            'bvid': video_info['bvid'],
            'title': video_info['title'],
            'owner': video_info['owner'],
            'duration': duration,
            'duration_str': format_time(duration) if duration else '未知',
            'pubdate': datetime.fromtimestamp(video_info.get('pubdate', 0)).strftime('%Y-%m-%d') if video_info.get('pubdate', 0) else '未知'
        },
        'statistics': {
            'total_count': len(danmakus),
            'type_distribution': dict(type_counter),
            'positive_keyword_count': positive_count,
            'negative_keyword_count': negative_count,
            'question_keyword_count': question_count,
            'positive_rate': round(positive_count / len(danmakus) * 100, 2) if danmakus else 0,
            'negative_rate': round(negative_count / len(danmakus) * 100, 2) if danmakus else 0,
            'question_rate': round(question_count / len(danmakus) * 100, 2) if danmakus else 0
        },
        'time_segments': [
            {
                'segment': f"{seg['start_time']}-{seg['end_time']}",
                'count': seg['count'],
                'samples': [
                    {'time': d['time'], 'text': d['text']}
                    for d in sorted(seg['danmakus'], key=lambda x: x.get('time', 0))[:10]
                ]
            }
            for seg in segments
        ],
        'all_danmakus_text': [d['text'] for d in sampled_danmakus],
        'sampled_danmakus': sampled_danmakus
    }

    return analysis_data


def generate_analysis_prompt(analysis_data: dict) -> str:
    """生成用于大模型分析的提示词"""
    video = analysis_data['video']
    stats = analysis_data['statistics']

    prompt = f"""# B站视频弹幕舆情与节奏分析

## 视频信息
- **标题**: {video['title']}
- **BV号**: {video['bvid']}
- **UP主**: {video['owner']}
- **时长**: {video['duration_str']}
- **弹幕总数**: {stats['total_count']} 条

## 弹幕统计概览
- **弹幕类型分布**: {stats['type_distribution']}
- **正面关键词占比**: {stats['positive_rate']}%
- **负面关键词占比**: {stats['negative_rate']}%
- **疑问句占比**: {stats['question_rate']}%

## 弹幕时间分布与内容（分段展示）

"""

    for seg in analysis_data['time_segments']:
        prompt += f"### 时段 {seg['segment']} (共 {seg['count']} 条弹幕)\n"
        if seg['samples']:
            for sample in seg['samples']:
                prompt += f"- [{sample['time']}] {sample['text']}\n"
        else:
            prompt += "- (此时间段无弹幕)\n"
        prompt += "\n"

    prompt += """## 分析要求

请基于以上弹幕数据，从以下维度进行深度分析：

### 1. 舆情分析
- **整体情感倾向**: 观众对这个视频的整体情感是正面、负面还是中性？
- **情感演变轨迹**: 在视频的不同时间段，弹幕情感是否有明显变化？
- **情感峰值时段**: 哪些时间点的弹幕情感最强烈（正面或负面）？

### 2. 节奏分析
- **高能预警点**: 根据弹幕密度和内容，哪些时间点是观众认为的"高能"时刻？
- **讨论热度分布**: 视频的哪些部分引发了最多的弹幕互动？
- **弹幕密度变化**: 弹幕数量随时间如何分布？是否有明显的聚集区域？

### 3. 内容特征
- **主要话题**: 弹幕中讨论的主要话题是什么？
- **梗与玩梗**: 视频中出现了哪些经典梗或流行语？
- **用户互动类型**: 观众是以什么方式在互动（科普、吐槽、情感共鸣、玩梗等）？

### 4. 舆情风险点
- **潜在负面点**: 是否有引发观众不满或争议的内容？
- **风险预警**: 哪些弹幕可能预示着舆情风险？

### 5. 总结
- 用3-5句话总结这个视频的弹幕舆情特征
"""

    return prompt


def generate_markdown_report(analysis_data: dict) -> str:
    """生成Markdown格式的完整分析报告"""
    video = analysis_data['video']
    stats = analysis_data['statistics']
    segments = analysis_data['time_segments']

    # 找出峰值时段
    peak_segments = sorted(segments, key=lambda x: x['count'], reverse=True)[:3]

    # 计算情感比
    positive_rate = stats['positive_rate']
    negative_rate = stats['negative_rate']
    if positive_rate > negative_rate * 1.5:
        overall_sentiment = "正面"
    elif negative_rate > positive_rate * 1.5:
        overall_sentiment = "负面"
    else:
        overall_sentiment = "中性"

    # 统计弹幕密度条形图
    max_count = max(seg['count'] for seg in segments) if segments else 1

    report = f"""# B站视频弹幕舆情与节奏分析报告

## 视频信息

| 项目 | 内容 |
|------|------|
| **标题** | {video['title']} |
| **BV号** | `{video['bvid']}` |
| **UP主** | {video['owner']} |
| **时长** | {video['duration_str']} |
| **弹幕总数** | **{stats['total_count']} 条** |
| **分析时间** | {datetime.now().strftime('%Y-%m-%d %H:%M')} |

---

## 弹幕统计概览

| 指标 | 数值 |
|------|------|
| 弹幕类型分布 | {', '.join([f"`{k}`:{v}" for k,v in stats['type_distribution'].items()])} |
| **正面关键词占比** | {stats['positive_rate']}% |
| **负面关键词占比** | {stats['negative_rate']}% |
| **疑问句占比** | {stats['question_rate']}% |
| 正面/负面比 | {round(positive_rate / negative_rate, 2) if negative_rate > 0 else '∞'} |

**整体情感倾向**: {overall_sentiment}

---

## 弹幕时间分布

### 密度分布图

| 时段 | 弹幕数 | 密度 |
|:-----|-------:|:-----|
"""

    for seg in segments:
        bar_len = int(seg['count'] / max_count * 10)
        bar = '#' * bar_len + '-' * (10 - bar_len)
        report += f"| {seg['segment']} | {seg['count']:4d} | {bar} |\n"

    report += f"""
### 高密度时段 TOP3

| 排名 | 时段 | 弹幕数 |
|:----:|:-----|-------:|
| 第1名 | {peak_segments[0]['segment']} | {peak_segments[0]['count']} 条 |
| 第2名 | {peak_segments[1]['segment']} | {peak_segments[1]['count']} 条 |
| 第3名 | {peak_segments[2]['segment']} | {peak_segments[2]['count']} 条 |

---

## 分时段弹幕详情

"""

    for seg in segments:
        report += f"### {seg['segment']} (共 {seg['count']} 条弹幕)\n\n"
        if seg['samples']:
            for sample in seg['samples'][:10]:
                time_formatted = format_time(sample['time'])
                report += f"- `[{time_formatted}]` {sample['text']}\n"
        else:
            report += "- (此时间段无弹幕)\n"
        report += "\n"

    report += f"""---

## 舆情分析

### 1. 整体情感倾向

基于关键词统计：
- **正面关键词**（牛、强、棒、好、赞、泪目、感动等）: {stats['positive_keyword_count']} 次
- **负面关键词**（烂、差、垃圾、无语、失望等）: {stats['negative_keyword_count']} 次
- **疑问句**（怎么、为什么、什么等）: {stats['question_keyword_count']} 次

**结论**: 观众对该视频的整体情感倾向为 **{overall_sentiment}**，正面评价占比 {positive_rate}%，负面评价占比 {negative_rate}%，正面是负面的 {round(positive_rate / negative_rate, 2) if negative_rate > 0 else '∞'} 倍。

### 2. 情感峰值时段

弹幕密度最高的时段为 **{peak_segments[0]['segment']}**（{peak_segments[0]['count']} 条），该时段弹幕以 {overall_sentiment}向评论为主。

"""

    report += f"""### 3. 高能预警点

根据弹幕密度和内容分析，以下时间点为"高能时刻"：

| 时间点 | 弹幕数 | 特征 |
|:-------|-------:|:-----|
"""

    for i, seg in enumerate(peak_segments[:3], 1):
        report += f"| {seg['segment']} | {seg['count']} | 高密度弹幕区 |\n"

    # 获取开场和结尾的时间段名称
    opening_segment = segments[2]['segment'] if len(segments) > 2 else segments[-1]['segment']
    closing_segment = segments[-1]['segment']

    report += f"""
---

## 节奏分析

### 弹幕密度变化特征

- **开场阶段** (00:00-{opening_segment.split('-')[1] if len(segments) > 2 else '...' }): {sum(seg['count'] for seg in segments[:3])} 条弹幕，平均 {sum(seg['count'] for seg in segments[:3])//3} 条/分钟
- **中间阶段**: {sum(seg['count'] for seg in segments[3:7]) if len(segments) > 7 else 0} 条弹幕
- **高潮阶段** ({closing_segment}): {segments[-1]['count']} 条弹幕

"""

    report += """---

## 主要发现

### 弹幕内容特征

1. **情感表达**: 弹幕以情感共鸣型内容为主，观众积极参与互动
2. **内容质量**: 高密度弹幕时段通常对应视频的关键内容点
3. **互动形式**: 弹幕形式多样，包括科普补充、玩梗、感慨等多种类型

---

## 风险提示

"""

    if negative_rate > 10:
        report += f"""**注意**: 该视频负面弹幕占比 ({negative_rate}%) 相对较高，建议关注舆情动态。
"""
    else:
        report += """**整体舆情**: 弹幕内容积极正面，未发现明显舆情风险点。
"""

    report += f"""
---

## 总结

本视频共获得 **{stats['total_count']} 条弹幕**，弹幕密度呈现**双峰结构**特征：
- 第一个高峰出现在 **{peak_segments[0]['segment']}** 时段（{peak_segments[0]['count']} 条）
- 第二个高峰出现在 **{peak_segments[1]['segment']}** 时段（{peak_segments[1]['count']} 条）

整体舆情 **{overall_sentiment}**，正面关键词占比 {positive_rate}%，负面占比 {negative_rate}%。
"""

    return report


def export_analysis_data(analysis_data: dict, output_dir: Path) -> tuple:
    """导出分析数据到JSON文件"""
    json_path = output_dir / f"{analysis_data['video']['bvid']}_弹幕分析数据.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2)

    prompt_path = output_dir / f"{analysis_data['video']['bvid']}_分析提示词.txt"
    prompt = generate_analysis_prompt(analysis_data)
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(prompt)

    # 生成Markdown报告
    md_report = generate_markdown_report(analysis_data)
    md_path = output_dir / f"{analysis_data['video']['bvid']}_弹幕舆情分析报告.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_report)

    return json_path, prompt_path, md_path


def main():
    parser = argparse.ArgumentParser(description='B站弹幕舆情分析工具')
    parser.add_argument('url', help='B站视频链接或BV号')
    parser.add_argument('-o', '--output', help='输出目录 (默认: 当前目录)', default='.')
    args = parser.parse_args()

    try:
        bvid = extract_bvid(args.url)
        print(f"正在分析弹幕: {bvid}")

        print("正在获取视频信息...")
        video_info = get_video_info(bvid)
        title = video_info['title']
        cid = video_info.get('cid', 0)

        if not cid:
            raise ValueError("无法获取视频CID，请检查视频链接是否有效")

        print(f"正在获取弹幕 (视频: {title})...")
        danmakus = get_danmakus(str(cid))
        print(f"获取到 {len(danmakus)} 条弹幕")

        print("正在整理分析数据...")
        analysis_data = prepare_analysis_data(video_info, danmakus)

        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        print("正在导出分析数据...")
        json_path, prompt_path, md_path = export_analysis_data(analysis_data, output_dir)

        # 生成Markdown报告
        md_report = generate_markdown_report(analysis_data)

        print("\n" + "=" * 60)
        print("分析完成!")
        print("=" * 60)
        print(f"视频: {title}")
        print(f"弹幕数: {len(danmakus)} 条")
        print(f"\n输出文件:")
        print(f"  [JSON] {json_path}")
        print(f"  [TXT]  {prompt_path}")
        print(f"  [MD]   {md_path}")

        # 生成Markdown报告
        md_report = generate_markdown_report(analysis_data)

        print("\n" + "=" * 60)
        print("[Markdown报告预览]")
        print("=" * 60)
        print(md_report)

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())