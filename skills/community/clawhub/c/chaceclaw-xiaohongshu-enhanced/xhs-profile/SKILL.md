---
name: xhs-profile
description: 小红书博主主页分析。粉丝数据、内容分析、合作价值评估、批量对比。
emoji: 👤
version: "1.0.0"
triggers:
  - 博主
  - 主页
  - 粉丝
  - 分析博主
  - profile
---

# 👤 xhs-profile

> 小红书博主主页分析完整指南

## 何时触发

- "看看这个博主"
- "分析一下这个账号"
- "博主主页"
- "粉丝数据"
- `/xhs-profile`

---

## 前置必检

```python
status = await mcp.check_login_status()
assert status["logged_in"], "❌ 未登录"
```

---

## 获取博主主页

### 标准查询

```python
# 获取博主资料
profile = await mcp.get_user_profile(user_id="xxxxxxxx")

# 返回格式
{
    "user_id": "xxxxxxxx",
    "nickname": "博主昵称",
    "avatar": "https://...",
    "gender": "f",  # f=女, m=男
    "ip_location": "广东",
    "bio": "个人简介文字",
    "followers": 12500,        # 粉丝数
    "following": 328,          # 关注数
    "likes_received": 89000,   # 获赞数
    "notes_count": 45,         # 笔记总数
    "is_verified": false,      # 是否认证
    "verified_type": "",       # 认证类型
    "level": 6,                # 薯等级
    "created_at": "2023-01-15"
}
```

### 获取博主笔记列表

```python
# 获取博主所有笔记
notes = await mcp.get_user_notes(
    user_id="xxxxxxxx",
    page=1,
    page_size=20,
    sort="time"  # time=最新, likes=最热
)

# 返回格式
{
    "items": [
        {
            "note_id": "64xxxxxxx",
            "title": "标题",
            "type": "normal",  # normal=图文, video=视频
            "likes": 1234,
            "collects": 567,
            "comments": 89,
            "published_at": "2026-04-20T...",
            "image_urls": ["..."],
            "topics": ["#话题#"]
        }
    ],
    "total": 45,
    "has_more": true
}
```

---

## 博主数据分析

### 基础指标计算

```python
def analyze_profile(profile, notes):
    """全面分析博主数据"""
    
    total_notes = len(notes)
    if total_notes == 0:
        return {"error": "无笔记数据"}
    
    # 基础统计
    total_likes = sum(n['likes'] for n in notes)
    total_collects = sum(n['collects'] for n in notes)
    total_comments = sum(n['comments'] for n in notes)
    
    stats = {
        # 粉丝效率
        "followers_per_note": round(profile['followers'] / total_notes, 1),
        # 平均互动
        "avg_likes_per_note": round(total_likes / total_notes, 1),
        "avg_collects_per_note": round(total_collects / total_notes, 1),
        "avg_comments_per_note": round(total_comments / total_notes, 1),
        # 爆款率（点赞>1000的笔记比例）
        "viral_rate": round(len([n for n in notes if n['likes'] > 1000]) / total_notes * 100, 1),
        # 粉丝质量（获赞/粉丝比）
        "fan_quality": round(profile['likes_received'] / max(profile['followers'], 1), 1),
    }
    
    # 互动率
    # 互动率 = (点赞+收藏+评论) / 浏览量（浏览量估算：点赞*20）
    estimated_views = sum(n['likes'] * 20 for n in notes)
    total_interactions = total_likes + total_collects + total_comments
    stats['engagement_rate'] = round(total_interactions / max(estimated_views, 1) * 100, 2)
    
    return stats
```

### 博主质量分级

```python
def rate_influencer(profile, notes):
    """博主价值评级"""
    
    followers = profile['followers']
    stats = analyze_profile(profile, notes)
    
    # 评级标准
    if followers >= 100000 and stats['engagement_rate'] >= 5:
        return "⭐⭐⭐⭐⭐ S级（头部博主）"
    elif followers >= 50000 and stats['engagement_rate'] >= 3:
        return "⭐⭐⭐⭐ A级（腰部博主）"
    elif followers >= 10000 and stats['engagement_rate'] >= 2:
        return "⭐⭐⭐ B级（成长期博主）"
    elif followers >= 1000:
        return "⭐⭐ C级（初级博主）"
    else:
        return "⭐ D级（素人账号）"
```

### 发布规律分析

```python
from collections import Counter
from datetime import datetime

def analyze_posting_pattern(notes):
    """分析博主发布规律"""
    
    # 提取发布时间
    hours = []
    weekdays = []
    
    for note in notes:
        dt = datetime.fromisoformat(note['published_at'].replace('Z', '+08:00'))
        hours.append(dt.hour)
        weekdays.append(dt.strftime('%A'))
    
    # 最常发布时段
    peak_hour = Counter(hours).most_common(1)[0]
    peak_weekday = Counter(weekdays).most_common(1)[0]
    
    # 内容类型分布
    video_count = len([n for n in notes if n['type'] == 'video'])
    normal_count = len([n for n in notes if n['type'] == 'normal'])
    
    return {
        "peak_post_hour": f"{peak_hour[0]}:00",  # 最常发笔记的时间
        "peak_post_weekday": peak_weekday[0],     # 最常发笔记的星期
        "video_ratio": round(video_count / len(notes) * 100, 1),
        "avg_notes_per_week": round(len(notes) / 4, 1) if len(notes) >= 4 else "数据不足",
        "most_active_hour_range": f"{peak_hour[0]-1}:00~{peak_hour[0]+2}:00"
    }
```

---

## 批量博主对比

```python
async def compare_influencers(mcp, user_ids):
    """批量对比多个博主"""
    
    results = []
    
    for user_id in user_ids:
        try:
            # 获取资料和笔记
            profile = await mcp.get_user_profile(user_id)
            notes = await mcp.get_user_notes(user_id, sort="popularity_desc", page_size=20)
            
            # 计算数据
            stats = analyze_profile(profile, notes['items'][:10])  # 取前10篇分析
            rating = rate_influencer(profile, notes['items'])
            
            results.append({
                "user_id": user_id,
                "nickname": profile['nickname'],
                "followers": profile['followers'],
                "avg_likes": stats.get('avg_likes_per_note', 0),
                "engagement_rate": stats.get('engagement_rate', 0),
                "viral_rate": stats.get('viral_rate', 0),
                "rating": rating
            })
            
            await asyncio.sleep(2)  # 限流
            
        except Exception as e:
            print(f"获取 {user_id} 失败: {e}")
            continue
    
    # 按粉丝数排序
    results.sort(key=lambda x: x['followers'], reverse=True)
    
    # 打印对比表
    print(f"{'博主':<12} {'粉丝':>8} {'均赞':>8} {'互动率':>8} {'爆款率':>8} {'评级':<15}")
    print("-" * 65)
    for r in results:
        print(f"{r['nickname']:<12} {r['followers']:>8,} {r['avg_likes']:>8.0f} "
              f"{r['engagement_rate']:>7.1f}% {r['viral_rate']:>7.1f}% {r['rating']:<15}")
    
    return results
```

---

## 博主合作价值评估

```python
def evaluate_collab_value(profile, notes):
    """评估博主合作价值"""
    
    stats = analyze_profile(profile, notes[:10])
    
    # 评估维度
    factors = {
        "粉丝质量": "⭐⭐⭐⭐⭐" if stats['fan_quality'] > 5 else
                   "⭐⭐⭐⭐" if stats['fan_quality'] > 3 else
                   "⭐⭐⭐" if stats['fan_quality'] > 1 else "⭐⭐",
        "互动率": "⭐⭐⭐⭐⭐" if stats['engagement_rate'] > 8 else
                  "⭐⭐⭐⭐" if stats['engagement_rate'] > 5 else
                  "⭐⭐⭐" if stats['engagement_rate'] > 2 else "⭐⭐",
        "爆款率": "⭐⭐⭐⭐⭐" if stats['viral_rate'] > 30 else
                  "⭐⭐⭐⭐" if stats['viral_rate'] > 20 else
                  "⭐⭐⭐" if stats['viral_rate'] > 10 else "⭐⭐",
        "内容垂直度": "⭐⭐⭐⭐⭐" if len(set(n.get('topics', []) for n in notes[:5])) <= 3 else "⭐⭐⭐",
    }
    
    # 合作建议
    if stats['engagement_rate'] > 5 and profile['followers'] >= 10000:
        advice = "✅ 高价值合作博主，建议深度合作"
    elif stats['engagement_rate'] > 2:
        advice = "✅ 中等价值，可考虑小规模合作"
    else:
        advice = "⚠️ 性价比一般，建议观望或放弃"
    
    return {
        "nickname": profile['nickname'],
        "factors": factors,
        "advice": advice,
        "estimated_cpc": stats['avg_likes_per_note'] * 0.1  # 粗估报价参考
    }
```

---

## 博主黑名单检测

```python
SUSPICIOUS_PATTERNS = [
    "小号", "助理", "合作", "广告", "代发",
    "涨粉", "点赞", "刷", "互", "群"
]

def is_suspicious(profile, notes):
    """检测可疑博主"""
    
    reasons = []
    
    # 昵称/简介含可疑词
    bio = (profile.get('bio') or "").lower()
    nickname = profile.get('nickname', "").lower()
    combined = bio + nickname
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in combined:
            reasons.append(f"昵称/简介含可疑词: {pattern}")
    
    # 粉丝/获赞比异常（刷量嫌疑）
    if profile['followers'] > 0:
        ratio = profile['likes_received'] / profile['followers']
        if ratio < 0.5 and profile['followers'] > 1000:
            reasons.append(f"获赞/粉丝比异常低: {ratio:.2f}")
    
    # 笔记全部极短（机器批量发）
    avg_len = sum(len(n.get('content', '')) for n in notes) / max(len(notes), 1)
    if avg_len < 20 and len(notes) > 5:
        reasons.append("笔记内容极短，可能是机器批量发")
    
    # 同一时间段集中发布
    from collections import Counter
    hours = [datetime.fromisoformat(n['published_at'].replace('Z', '+08:00')).hour 
             for n in notes]
    if len(hours) >= 5:
        most_common_hour = Counter(hours).most_common(1)[0]
        if most_common_hour[1] / len(hours) > 0.5:
            reasons.append(f"集中发布时间，可能刷量")
    
    return {
        "suspicious": len(reasons) > 0,
        "reasons": reasons
    }
```

---

*Version: 1.0.0 | Updated: 2026-04-23*