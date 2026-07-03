"""
外卖评价智能分析引擎
- 情感分析（基于SnowNLP + 关键词增强）
- 趋势检测（评分趋势、差评趋势）
- 异常检测（口味变差、配送超时、服务问题）
- 关键词提取
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import re
import json
import os

# 餐饮领域情感词典
FOOD_SENTIMENT_DICT = {
    # 口味相关 - 正面
    "好吃": 1.0, "美味": 1.0, "好吃极了": 1.5, "味道不错": 0.8,
    "口感好": 0.8, "入味": 0.7, "鲜美": 0.9, "香": 0.5,
    "正宗": 0.7, "地道": 0.7, "够味": 0.6, "回味": 0.6,
    "下饭": 0.6, "开胃": 0.5, "分量足": 0.5, "量足": 0.5,
    "新鲜": 0.7, "现做": 0.6, "热乎": 0.6, "烫": 0.4,
    # 口味相关 - 负面
    "难吃": -1.0, "不好吃": -0.8, "味道差": -1.0, "没味道": -0.8,
    "太咸": -0.7, "太淡": -0.6, "太甜": -0.5, "太辣": -0.4,
    "油腻": -0.7, "腥": -0.8, "不新鲜": -0.9, "变质": -1.5,
    "馊": -1.5, "凉了": -0.7, "冷的": -0.7, "温的": -0.5,
    "量少": -0.6, "分量少": -0.6, "不值": -0.7,
    # 配送相关 - 负面
    "超时": -0.9, "迟到": -0.8, "送得慢": -0.8, "配送慢": -0.8,
    "等太久": -0.8, "等了好久": -0.8, "快递慢": -0.7,
    "洒了": -1.0, "漏了": -1.0, "破损": -1.0, "摔坏": -1.0,
    "包装差": -0.7, "包装不好": -0.7, "包装破损": -0.9,
    "少送": -1.0, "漏送": -1.0, "送错": -1.0, "少东西": -1.0,
    # 配送相关 - 正面
    "送得快": 0.6, "配送快": 0.6, "准时": 0.5, "提前": 0.4,
    "包装好": 0.5, "包装严实": 0.6, "保温好": 0.5,
    # 服务相关 - 正面
    "态度好": 0.7, "服务好": 0.7, "热情": 0.6, "周到": 0.6,
    "细心": 0.6, "耐心": 0.5, "回复快": 0.5,
    # 服务相关 - 负面
    "态度差": -0.9, "服务差": -0.9, "态度恶劣": -1.2,
    "不理人": -0.8, "回复慢": -0.5, "敷衍": -0.7,
    # 价格相关
    "性价比高": 0.7, "实惠": 0.6, "便宜": 0.3, "划算": 0.6,
    "贵": -0.4, "太贵": -0.7, "不值这个价": -0.9, "坑": -1.0,
    # 综合
    "推荐": 0.7, "会回购": 0.8, "还会来": 0.7, "再来": 0.6,
    "失望": -0.8, "不会再买": -1.0, "后悔": -1.0, "踩雷": -1.0,
}

# 维度关键词分类
DIMENSION_KEYWORDS = {
    "口味": ["好吃", "难吃", "味道", "口感", "咸", "淡", "甜", "辣", "酸",
             "油腻", "腥", "新鲜", "变质", "馊", "正宗", "地道", "香",
             "入味", "下饭", "开胃", "分量", "量足", "量少", "现做", "热乎", "烫", "凉"],
    "配送": ["配送", "外卖", "送餐", "快递", "超时", "迟到", "送达",
             "等太久", "包装", "洒", "漏", "破损", "摔", "少送", "漏送", "送错"],
    "服务": ["态度", "服务", "热情", "周到", "细心", "耐心", "回复",
             "不理", "敷衍", "售后", "处理", "解决"],
    "价格": ["价格", "性价比", "实惠", "便宜", "划算", "贵", "不值", "坑"],
}


def analyze_sentiment(text: str) -> dict:
    """基于词典的情感分析"""
    if not text or pd.isna(text):
        return {"score": 0, "label": "neutral", "intensity": 0}

    text = str(text).strip()
    score = 0
    match_count = 0
    dimension_scores = {dim: 0 for dim in DIMENSION_KEYWORDS}

    for word, weight in FOOD_SENTIMENT_DICT.items():
        if word in text:
            score += weight
            match_count += 1

            # 统计各维度得分
            for dim, keywords in DIMENSION_KEYWORDS.items():
                if word in keywords:
                    dimension_scores[dim] += weight
                    break

    # 归一化
    if match_count > 0:
        score = score / np.sqrt(match_count + 1)  # 防止短文本高分
    score = max(-2.0, min(2.0, score))

    # 确定标签
    if score > 0.3:
        label = "positive"
    elif score < -0.3:
        label = "negative"
    else:
        label = "neutral"

    # 情感强度
    intensity = min(1.0, abs(score) / 2.0)

    return {
        "score": round(score, 3),
        "label": label,
        "intensity": round(intensity, 3),
        "dimension_scores": dimension_scores,
        "matched_words": match_count,
    }


def extract_keywords(texts: list, top_n: int = 30) -> list:
    """提取高频关键词（简单TF方式，不依赖jieba）"""
    # 过滤停用词
    stopwords = {
        "的", "了", "是", "我", "在", "有", "和", "就", "不", "人", "都", "一",
        "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着",
        "没有", "看", "好", "自己", "这", "他", "她", "它", "们", "那", "些",
        "什么", "怎么", "这个", "那个", "还是", "但是", "因为", "所以",
        "可以", "觉得", "比较", "非常", "真的", "还", "太", "挺", "蛮",
        "给", "让", "把", "被", "从", "对", "跟", "与", "或",
        "又", "再", "才", "刚", "已经", "正在", "将", "要",
        "能", "会", "想", "可能", "应该", "必须",
        "来", "去", "出", "进", "过", "回",
        "买", "点", "份", "次", "个", "元", "块",
        "今天", "昨天", "明天", "现在", "之前", "以后",
        "嗯", "啊", "吧", "呢", "吗", "哦", "哈",
    }

    # 简单的2-4字词提取
    word_counter = Counter()
    for text in texts:
        if not text or pd.isna(text):
            continue
        text = str(text).strip()
        # 提取中文词组（2-4字）
        chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
        for segment in chinese_chars:
            if 2 <= len(segment) <= 4 and segment not in stopwords:
                word_counter[segment] += 1
            elif len(segment) > 4:
                # 滑动窗口提取2-3字词
                for i in range(len(segment) - 1):
                    for wlen in [2, 3]:
                        if i + wlen <= len(segment):
                            word = segment[i:i+wlen]
                            if word not in stopwords:
                                word_counter[word] += 1

    return word_counter.most_common(top_n)


def analyze_reviews(df: pd.DataFrame) -> dict:
    """综合分析评价数据"""
    result = {
        "summary": {},
        "sentiment": {},
        "dimensions": {},
        "trends": {},
        "anomalies": [],
        "keywords": [],
        "alerts": [],
    }

    if df.empty:
        result["summary"] = {"total": 0, "message": "无评价数据"}
        return result

    # === 基本统计 ===
    total = len(df)
    result["summary"]["total"] = total

    if 'rating' in df.columns:
        ratings = df['rating'].dropna()
        if len(ratings) > 0:
            result["summary"]["avg_rating"] = round(ratings.mean(), 2)
            result["summary"]["min_rating"] = round(ratings.min(), 1)
            result["summary"]["max_rating"] = round(ratings.max(), 1)
            result["summary"]["rating_distribution"] = {
                "5星": int((ratings >= 4.5).sum()),
                "4星": int(((ratings >= 3.5) & (ratings < 4.5)).sum()),
                "3星": int(((ratings >= 2.5) & (ratings < 3.5)).sum()),
                "2星": int(((ratings >= 1.5) & (ratings < 2.5)).sum()),
                "1星": int((ratings < 1.5).sum()),
            }

    if 'platform' in df.columns:
        result["summary"]["platforms"] = df['platform'].value_counts().to_dict()

    if 'review_time' in df.columns:
        times = df['review_time'].dropna()
        if len(times) > 0:
            result["summary"]["time_range"] = {
                "start": times.min().strftime("%Y-%m-%d"),
                "end": times.max().strftime("%Y-%m-%d"),
            }

    # === 情感分析 ===
    if 'content' in df.columns:
        sentiments = []
        all_dimension_scores = {dim: [] for dim in DIMENSION_KEYWORDS}

        for text in df['content']:
            sent = analyze_sentiment(text)
            sentiments.append(sent)
            for dim in DIMENSION_KEYWORDS:
                all_dimension_scores[dim].append(sent["dimension_scores"][dim])

        df['sentiment_label'] = [s['label'] for s in sentiments]
        df['sentiment_score'] = [s['score'] for s in sentiments]
        df['sentiment_intensity'] = [s['intensity'] for s in sentiments]

        labels = df['sentiment_label'].value_counts()
        result["sentiment"] = {
            "positive": int(labels.get("positive", 0)),
            "neutral": int(labels.get("neutral", 0)),
            "negative": int(labels.get("negative", 0)),
            "negative_ratio": round(
                labels.get("negative", 0) / total * 100, 1
            ) if total > 0 else 0,
            "avg_sentiment_score": round(
                df['sentiment_score'].mean(), 3
            ),
        }

        # === 维度分析 ===
        for dim in DIMENSION_KEYWORDS:
            scores = all_dimension_scores[dim]
            negative_count = sum(1 for s in scores if s < -0.2)
            positive_count = sum(1 for s in scores if s > 0.2)
            total_mentions = sum(1 for s in scores if abs(s) > 0.01)

            result["dimensions"][dim] = {
                "total_mentions": total_mentions,
                "mention_ratio": round(total_mentions / total * 100, 1) if total > 0 else 0,
                "positive_ratio": round(
                    positive_count / max(total_mentions, 1) * 100, 1
                ),
                "negative_ratio": round(
                    negative_count / max(total_mentions, 1) * 100, 1
                ),
                "avg_score": round(np.mean(scores), 3) if scores else 0,
            }

        # === 关键词提取 ===
        result["keywords"] = extract_keywords(df['content'].tolist(), top_n=50)

        # === 差评列表 ===
        negative_reviews = df[df['sentiment_label'] == 'negative'].head(20)
        result["negative_reviews"] = []
        for _, row in negative_reviews.iterrows():
            result["negative_reviews"].append({
                "content": str(row['content'])[:200],
                "score": round(row.get('sentiment_score', 0), 2),
                "time": str(row.get('review_time', '')),
                "rating": row.get('rating', None),
            })

    # === 趋势分析 ===
    if 'review_time' in df.columns and 'sentiment_label' in df.columns:
        df_time = df.copy()
        df_time['date'] = pd.to_datetime(df_time['review_time']).dt.date

        daily = df_time.groupby('date').agg(
            total=('sentiment_label', 'count'),
            avg_rating=('rating', 'mean') if 'rating' in df.columns else ('sentiment_score', 'mean'),
            negative_count=('sentiment_label', lambda x: (x == 'negative').sum()),
            negative_ratio=('sentiment_label', lambda x: (x == 'negative').sum() / len(x) * 100),
        ).reset_index()

        daily['date_str'] = daily['date'].astype(str)
        result["trends"]["daily"] = daily.to_dict('records')

        # 最近7天趋势
        if len(daily) >= 3:
            recent = daily.tail(7)
            result["trends"]["recent_7days"] = {
                "avg_rating": round(recent['avg_rating'].mean(), 2),
                "avg_negative_ratio": round(recent['negative_ratio'].mean(), 1),
                "trend": "上升" if recent['negative_ratio'].iloc[-1] > recent['negative_ratio'].iloc[0]
                else "下降" if recent['negative_ratio'].iloc[-1] < recent['negative_ratio'].iloc[0]
                else "平稳",
            }

    # === 异常检测 ===
    result["anomalies"] = detect_anomalies(df)

    return result


def detect_anomalies(df: pd.DataFrame) -> list:
    """检测异常"""
    anomalies = []
    total = len(df)
    if total == 0:
        return anomalies

    # 1. 口味异常检测
    if 'sentiment_score' in df.columns and 'content' in df.columns:
        # 检查口味相关的负面评价
        taste_negative = df[
            df['content'].str.contains(
                '难吃|不好吃|味道差|没味道|太咸|太淡|太甜|油腻|腥|不新鲜|变质|馊',
                na=False
            ) & (df['sentiment_label'] == 'negative')
        ]
        taste_ratio = len(taste_negative) / total * 100
        if taste_ratio > 30:
            anomalies.append({
                "type": "口味异常",
                "severity": "high" if taste_ratio > 50 else "medium",
                "message": f"口味负面评价占比 {taste_ratio:.1f}%，超过30%告警线",
                "details": f"共{len(taste_negative)}条口味负面评价",
                "sample_reviews": taste_negative['content'].head(3).tolist() if len(taste_negative) > 0 else [],
            })
        elif taste_ratio > 15:
            anomalies.append({
                "type": "口味关注",
                "severity": "low",
                "message": f"口味负面评价占比 {taste_ratio:.1f}%，需关注",
                "details": f"共{len(taste_negative)}条口味负面评价",
            })

    # 2. 配送异常检测
    if 'content' in df.columns:
        delivery_negative = df[
            df['content'].str.contains(
                '超时|迟到|送得慢|配送慢|等太久|洒了|漏了|破损|少送|漏送|送错',
                na=False
            )
        ]
        delivery_ratio = len(delivery_negative) / total * 100
        if delivery_ratio > 15:
            anomalies.append({
                "type": "配送异常",
                "severity": "high" if delivery_ratio > 25 else "medium",
                "message": f"配送问题提及率 {delivery_ratio:.1f}%，超过15%告警线",
                "details": f"共{len(delivery_negative)}条配送相关负面评价",
                "sample_reviews": delivery_negative['content'].head(3).tolist() if len(delivery_negative) > 0 else [],
            })

    # 3. 服务异常检测
    if 'content' in df.columns:
        service_negative = df[
            df['content'].str.contains(
                '态度差|服务差|态度恶劣|不理人|敷衍',
                na=False
            )
        ]
        service_ratio = len(service_negative) / total * 100
        if service_ratio > 20:
            anomalies.append({
                "type": "服务异常",
                "severity": "high" if service_ratio > 35 else "medium",
                "message": f"服务负面评价占比 {service_ratio:.1f}%，超过20%告警线",
                "details": f"共{len(service_negative)}条服务负面评价",
                "sample_reviews": service_negative['content'].head(3).tolist() if len(service_negative) > 0 else [],
            })

    # 4. 评分异常检测
    if 'rating' in df.columns and 'review_time' in df.columns:
        ratings = df['rating'].dropna()
        if len(ratings) > 0:
            avg_rating = ratings.mean()
            if avg_rating < 3.5:
                anomalies.append({
                    "type": "评分异常",
                    "severity": "high" if avg_rating < 3.0 else "medium",
                    "message": f"平均评分仅 {avg_rating:.1f}，低于4.0告警线",
                    "details": f"最低评分: {ratings.min():.1f}, 最高评分: {ratings.max():.1f}",
                })

            # 低分占比
            low_ratio = (ratings < 3.0).sum() / len(ratings) * 100
            if low_ratio > 30:
                anomalies.append({
                    "type": "差评突增",
                    "severity": "high" if low_ratio > 50 else "medium",
                    "message": f"低分评价(1-2星)占比 {low_ratio:.1f}%，超过30%告警线",
                    "details": f"共{(ratings < 3.0).sum()}条低分评价",
                })

    # 5. 差评率趋势异常
    if 'review_time' in df.columns and 'sentiment_label' in df.columns:
        df_time = df.copy()
        df_time['date'] = pd.to_datetime(df_time['review_time']).dt.date
        daily = df_time.groupby('date').agg(
            total=('sentiment_label', 'count'),
            neg=('sentiment_label', lambda x: (x == 'negative').sum()),
        )
        daily['neg_ratio'] = daily['neg'] / daily['total'] * 100

        if len(daily) >= 3:
            recent_avg = daily['neg_ratio'].tail(3).mean()
            earlier_avg = daily['neg_ratio'].head(max(len(daily) - 3, 1)).mean()
            if earlier_avg > 0 and recent_avg > earlier_avg * 2:
                anomalies.append({
                    "type": "差评率飙升",
                    "severity": "high" if recent_avg > earlier_avg * 3 else "medium",
                    "message": f"近期差评率 {recent_avg:.1f}% 是前期 {earlier_avg:.1f}% 的 {recent_avg/earlier_avg:.1f}倍",
                    "details": "建议立即排查菜品质量和服务问题",
                })

    return anomalies


def compare_periods(current_df: pd.DataFrame, previous_df: pd.DataFrame) -> dict:
    """对比两个时间段的评价变化"""
    comparison = {
        "current_period": {},
        "previous_period": {},
        "changes": {},
    }

    for label, df in [("current_period", current_df), ("previous_period", previous_df)]:
        if df.empty:
            continue
        analysis = analyze_reviews(df)
        comparison[label] = {
            "total": analysis["summary"].get("total", 0),
            "sentiment": analysis.get("sentiment", {}),
            "dimensions": analysis.get("dimensions", {}),
        }

    # 计算变化
    cur = comparison.get("current_period", {})
    prev = comparison.get("previous_period", {})

    if cur and prev:
        cur_sent = cur.get("sentiment", {})
        prev_sent = prev.get("sentiment", {})

        comparison["changes"] = {
            "total_change": cur.get("total", 0) - prev.get("total", 0),
            "negative_ratio_change": round(
                cur_sent.get("negative_ratio", 0) - prev_sent.get("negative_ratio", 0), 1
            ),
            "sentiment_score_change": round(
                cur_sent.get("avg_sentiment_score", 0) - prev_sent.get("avg_sentiment_score", 0), 3
            ),
        }

        # 维度变化
        cur_dims = cur.get("dimensions", {})
        prev_dims = prev.get("dimensions", {})
        comparison["changes"]["dimensions"] = {}
        for dim in cur_dims:
            if dim in prev_dims:
                comparison["changes"]["dimensions"][dim] = {
                    "negative_ratio_change": round(
                        cur_dims[dim].get("negative_ratio", 0) - prev_dims[dim].get("negative_ratio", 0), 1
                    ),
                }

    return comparison
