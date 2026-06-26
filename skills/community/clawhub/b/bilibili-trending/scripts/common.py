"""
Bilibili-trending 共享工具模块

提供路径配置、数据持久化、关键词提取、AI 分析 prompt 生成、子 Agent 调用等通用功能。
"""

import json
import os
import re
import time
import random
from datetime import datetime
from collections import Counter

import requests

from config import RANK_CONFIG

# ========== 路径配置 ==========
_script_dir = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(_script_dir)
WORKSPACE = os.environ.get(
    "BILIBILI_WORKSPACE",
    os.path.dirname(os.path.dirname(SKILL_DIR))
)
JSON_DIR = os.path.join(WORKSPACE, "json")
ANALYSIS_DIR = os.path.join(WORKSPACE, "memory", "bilibili-analysis")
TREND_FILE = os.path.join(ANALYSIS_DIR, "trend.json")

os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# ========== 数据持久化 ==========

def load_trend():
    """加载趋势数据，不存在或格式不兼容时返回空结构"""
    defaults = {"records": [], "keywords": {}, "zones": {}, "rank_stats": {}}
    if os.path.exists(TREND_FILE):
        with open(TREND_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, default in defaults.items():
            if key not in data:
                data[key] = default
        return data
    return defaults


def save_trend(rank_type, top_zone, keywords, avg_interaction):
    """追加一条趋势记录，自动裁剪最近 60 条"""
    trend = load_trend()

    now = datetime.now()
    trend["records"].append({
        "time": now.strftime("%Y-%m-%d-%H%M%S"),
        "date": now.strftime("%Y-%m-%d"),
        "rank_type": rank_type,
        "top_zone": top_zone,
        "avg_interaction": avg_interaction,
        "keywords": keywords,
    })

    for kw in keywords:
        trend["keywords"][kw] = trend["keywords"].get(kw, 0) + 1
    if top_zone:
        trend["zones"][top_zone] = trend["zones"].get(top_zone, 0) + 1
    if rank_type not in trend["rank_stats"]:
        trend["rank_stats"][rank_type] = 0
    trend["rank_stats"][rank_type] += 1

    trend["records"] = trend["records"][-60:]

    with open(TREND_FILE, "w", encoding="utf-8") as f:
        json.dump(trend, f, ensure_ascii=False, indent=2)


def save_report(rank_type, content):
    """保存分析报告为 Markdown 文件，返回文件路径"""
    rank_name = RANK_CONFIG[rank_type]["name"]
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{rank_name}_{timestamp}.md"
    filepath = os.path.join(ANALYSIS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def save_summary_report(prefix, content):
    """保存周/月总结报告"""
    filepath = os.path.join(ANALYSIS_DIR, f"{prefix}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


# ========== 数据分析 ==========

def extract_keywords(videos):
    """从视频标题中提取 2-4 字中文关键词，返回 Top 10 列表"""
    all_words = []
    for v in videos:
        words = re.findall(r'[一-龥]{2,4}', v.get('title', ''))
        all_words.extend(words)
    kw_counter = Counter(all_words)
    return [kw for kw, _ in kw_counter.most_common(10)]


def extract_up_stats(videos):
    """统计重复上榜的 UP 主，返回 [(name, count), ...]"""
    owners = [v.get('owner', '') for v in videos if v.get('owner')]
    owner_counter = Counter(owners)
    return [(name, cnt) for name, cnt in owner_counter.most_common(5) if cnt > 1]


def compute_video_stats(videos, summary):
    """计算播放量分布、互动率等统计指标"""
    total_views = summary.get('total_views', 0)
    avg_ir = summary.get('avg_interaction_rate', 0)

    views = [v.get('view', 0) for v in videos]
    top10_views = sum(views[:10])
    top10_ratio = round(top10_views / max(total_views, 1) * 100, 1) if total_views else 0

    irs = [v.get('interaction_rate', 0) for v in videos]
    high_ir_count = sum(1 for ir in irs if ir > avg_ir * 1.5)

    return {
        "total_videos": len(videos),
        "total_views": total_views,
        "avg_interaction_rate": avg_ir,
        "top10_views_ratio": top10_ratio,
        "high_interaction_count": high_ir_count,
    }


# ========== Prompt 生成 ==========

def generate_analysis_prompt(rank_type, videos, summary):
    """生成发给子 Agent 的分析 prompt，返回 (prompt_text, top_keywords)"""
    rank_name = RANK_CONFIG[rank_type]["name"]
    stats = compute_video_stats(videos, summary)
    top_keywords = extract_keywords(videos)
    top_owners = extract_up_stats(videos)

    full_data = {
        "rank_type": rank_type,
        "rank_name": rank_name,
        "top_zone": summary.get('top_zone', ''),
        "zone_distribution": summary.get('zone_distribution', {}),
        "top_keywords": top_keywords,
        "top_owners": top_owners,
        "videos": videos,
        **stats,
    }

    prompt = f"""请深度分析 Bilibili {rank_name} 榜单数据（共{stats['total_videos']}条视频）。

## 数据概览
- 总视频数: {stats['total_videos']}
- 总播放: {stats['total_views']:,}
- 平均互动率: {stats['avg_interaction_rate']:.3f}%
- 分区数: {len(summary.get('zone_distribution', {}))}
- TOP10播放占比: {stats['top10_views_ratio']}%
- 高互动视频数: {stats['high_interaction_count']}条

## 热门分区分布
{json.dumps(summary.get('zone_distribution', {}), ensure_ascii=False)}

## 高频关键词 TOP10
{json.dumps(top_keywords, ensure_ascii=False)}

## 头部UP主（重复上榜）
{json.dumps(top_owners, ensure_ascii=False)}

## 完整视频数据
{json.dumps(full_data, ensure_ascii=False, indent=2)}

请输出 Markdown 分析报告，包含：
1. **播放量分布**：头部效应是否明显，TOP10占比，高播放视频特征
2. **互动率分析**：高互动视频的共同特征（标题/分区/UP主）
3. **热门分区**：哪些分区最活跃，竞争程度
4. **UP主生态**：是否有重复上榜的头部UP主，分析其内容风格
5. **标题规律**：高频词、热门题材、标题起名技巧
6. **下期预测**：什么类型/分区/题材可能下期上位

请用中文输出，直接输出报告内容。"""

    return prompt, top_keywords


# ========== 子 Agent 调用 ==========

def spawn_analysis_agent(prompt, label="bili-analysis"):
    """调用 OpenClaw 子 Agent 进行分析，不可用时返回 False"""
    try:
        from sessions_spawn import sessions_spawn
        response = sessions_spawn(
            label=label,
            runtime="subagent",
            task=prompt,
            timeoutSeconds=120
        )
        return response.get('status') == 'accepted'
    except ImportError:
        return False
    except Exception:
        return False


# ========== API 请求工具 ==========

def api_get(url, params=None, max_retries=3):
    """带重试的 GET 请求，自动处理限流和网络错误"""
    headers = {"User-Agent": "Mozilla/5.0"}
    last_error = None

    for attempt in range(max_retries):
        try:
            time.sleep(random.uniform(1, 3))
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()

            if data.get("code") == -352:
                wait = 30 * (attempt + 1)
                print(f"  API 限流，等待 {wait}s 后重试...")
                time.sleep(wait)
                last_error = Exception(f"API 限流 (-352)，已等待 {wait}s")
                continue

            if data.get("code") != 0:
                raise Exception(f"API 错误 (code={data.get('code')}): {data.get('message')}")

            return data

        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  请求失败 ({e})，{wait}s 后重试...")
                time.sleep(wait)

    raise Exception(f"API 请求失败（已重试 {max_retries} 次）: {last_error}")


# ========== JSON 数据存取 ==========

def get_json_path(rank_type="all"):
    return os.path.join(JSON_DIR, f"output_{rank_type}.json")


def load_json_data(rank_type="all"):
    json_path = get_json_path(rank_type)
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"数据文件不存在: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_data(rank_type, rank_name, videos, summary):
    output_path = get_json_path(rank_type)
    result = {
        "result": "success",
        "data": {
            "rank_type": rank_type,
            "rank_name": rank_name,
            "videos": videos,
            "summary": summary,
        }
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return output_path


# ========== 数据抓取与处理 ==========

def fetch_ranking_v2(rid):
    """抓取普通视频排行榜"""
    return api_get(
        "https://api.bilibili.com/x/web-interface/ranking/v2",
        params={"rid": rid, "type": "all", "pn": 1, "ps": 30},
    )


def fetch_pgc_ranking(season_type):
    """抓取 PGC 内容排行榜"""
    return api_get(
        "https://api.bilibili.com/pgc/season/rank/list",
        params={"season_type": season_type},
    )


def process_ranking_v2(raw_data):
    """处理普通视频数据，保留 owner 信息用于 UP 主分析"""
    video_list = raw_data["data"]["list"]
    processed = []

    for idx, v in enumerate(video_list):
        view = v["stat"]["view"]
        danmaku = v["stat"]["danmaku"]
        reply = v["stat"]["reply"]
        like = v["stat"]["like"]
        owner_info = v.get("owner", {})

        processed.append({
            "rank": idx + 1,
            "title": v.get("title", "").strip(),
            "tname": v.get("tname"),
            "view": view,
            "danmaku": danmaku,
            "reply": reply,
            "like": like,
            "interaction_rate": round((danmaku + reply) / max(view, 1) * 100, 3),
            "owner": owner_info.get("name", ""),
            "owner_mid": owner_info.get("mid", 0),
        })

    total_views = sum(v["stat"]["view"] for v in video_list)
    zone_dist = {}
    for v in video_list:
        tname = v.get("tname")
        zone_dist[tname] = zone_dist.get(tname, 0) + 1

    return processed, {
        "total_videos": len(processed),
        "total_views": total_views,
        "avg_interaction_rate": round(sum(p["interaction_rate"] for p in processed) / len(processed), 3),
        "top_zone": max(zone_dist.items(), key=lambda x: x[1])[0] if zone_dist else "",
        "zone_distribution": zone_dist,
    }


def process_pgc_ranking_data(raw_data):
    """处理 PGC 数据"""
    video_list = raw_data["data"]["list"]
    processed = []
    total_views = 0

    for idx, v in enumerate(video_list):
        view = v.get("stat", {}).get("view", 0)
        total_views += view
        processed.append({
            "rank": idx + 1,
            "title": v.get("title", "").strip(),
            "area": v.get("area", ""),
            "view": view,
            "score": v.get("score", 0),
            "owner": v.get("new_ep", {}).get("title", "") or v.get("publish", {}).get("title", ""),
        })

    area_dist = {}
    for v in video_list:
        area = v.get("area", "未知")
        area_dist[area] = area_dist.get(area, 0) + 1

    return processed, {
        "total_videos": len(processed),
        "total_views": total_views,
        "avg_interaction_rate": 0,
        "top_zone": max(area_dist.items(), key=lambda x: x[1])[0] if area_dist else "",
        "zone_distribution": area_dist,
    }


def fetch_and_process(rank_type):
    """统一抓取入口：根据榜单类型抓取并处理数据"""
    config = RANK_CONFIG[rank_type]
    if config["api_type"] == "ranking":
        raw_data = fetch_ranking_v2(config["rid"])
        return process_ranking_v2(raw_data)
    else:
        raw_data = fetch_pgc_ranking(config["season_type"])
        return process_pgc_ranking_data(raw_data)


def fetch_all_ranks(rank_types, delay=5):
    """批量抓取多个榜单，榜单间自动延迟避免限流。返回 {rank_type: (videos, summary)}"""
    results = {}
    for i, rank_type in enumerate(rank_types):
        if i > 0:
            time.sleep(delay)
        try:
            videos, summary = fetch_and_process(rank_type)
            results[rank_type] = (videos, summary)
            rank_name = RANK_CONFIG[rank_type]["name"]
            print(f"  [{rank_name}] {len(videos)} 条, 总播放 {summary['total_views']:,}")
        except Exception as e:
            print(f"  [{RANK_CONFIG[rank_type]['name']}] 抓取失败: {e}")
            continue
    return results
