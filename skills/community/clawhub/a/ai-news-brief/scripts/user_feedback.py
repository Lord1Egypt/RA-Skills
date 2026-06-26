#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户反馈处理模块
功能：
1. 解析用户反馈（喜欢/不喜欢某些内容）
2. 调整关键词权重
3. 验证内容可信度
"""

import json
import os
import re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "user_config")
USER_CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "user_config.json")
DEFAULT_USER_CONFIG_FILE = os.path.join(SCRIPT_DIR, "user_config.json.default")


def load_user_config():
    """加载用户配置（优先用户配置目录）"""
    # 优先读取用户配置目录
    if os.path.exists(USER_CONFIG_FILE):
        try:
            with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 读取用户配置失败: {e}")
    
    # 读取默认配置
    if os.path.exists(DEFAULT_USER_CONFIG_FILE):
        try:
            with open(DEFAULT_USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                print("[INFO] 使用默认用户配置，请复制到 user_config 目录进行自定义")
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] 无法加载默认配置: {e}")
    
    return {
        "user_preferences": {
            "liked_keywords": [],
            "disliked_keywords": [],
            "liked_sources": [],
            "disliked_sources": [],
            "custom_keywords": [],
            "excluded_keywords": []
        }
    }


def save_user_config(config):
    """保存用户配置"""
    try:
        with open(USER_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] 保存配置失败: {e}")
        return False


def parse_feedback(feedback_text):
    """
    解析用户反馈文本
    返回: {action: 'like'/'dislike', type: 'keyword'/'source', value: 'xxx'}
    """
    feedback = feedback_text.lower().strip()
    
    # 解析喜欢
    like_patterns = [
        r"(喜欢|想要|想看|关注|感兴趣|只看|只要)(.+)",
        r"(.+)(相关|的|资讯|新闻)",
    ]
    
    # 解析不喜欢
    dislike_patterns = [
        r"(不喜欢|不要|不想看|不想要|过滤|排除)(.+)",
        r"别(要|要|的)(.+)",
    ]
    
    # 检查是否是排除来源
    for source in ["36kr", "量子位", "虎嗅", "爱范儿", "网易", "新浪", "腾讯", "凤凰"]:
        if source in feedback:
            return {"action": "dislike", "type": "source", "value": source}
    
    # 检查关键词
    keywords = [
        "gpu", "显卡", "nvidia", "amd", "intel", "cuda",
        "ai", "人工智能", "大模型", "gpt", "llm", "chatgpt",
        "自动驾驶", "智驾", "特斯拉", "fsd",
        "华为", "昇腾", "阿里", "百度", "字节", "腾讯",
        "openai", "claude", "gemini", "deepseek",
        "视频生成", "图像生成", "sora", "多模态",
        "芯片", "算力", "半导体", "处理器"
    ]
    
    for kw in keywords:
        if kw in feedback:
            if any(x in feedback for x in ["不要", "不喜欢", "不想要", "过滤", "排除", "别"]):
                return {"action": "dislike", "type": "keyword", "value": kw}
            else:
                return {"action": "like", "type": "keyword", "value": kw}
    
    return None


def process_feedback(feedback_text):
    """处理用户反馈，更新配置"""
    config = load_user_config()
    prefs = config.get("user_preferences", {})
    
    parsed = parse_feedback(feedback_text)
    if not parsed:
        return False, "无法解析反馈内容"
    
    action = parsed["action"]  # like / dislike
    ptype = parsed["type"]     # keyword / source
    value = parsed["value"]
    
    if ptype == "keyword":
        liked = prefs.get("liked_keywords", [])
        disliked = prefs.get("disliked_keywords", [])
        
        if action == "like":
            if value not in liked:
                liked.append(value)
            if value in disliked:
                disliked.remove(value)
            prefs["liked_keywords"] = liked
            prefs["disliked_keywords"] = disliked
            msg = f"已添加关键词: {value}"
        else:
            if value not in disliked:
                disliked.append(value)
            if value in liked:
                liked.remove(value)
            prefs["liked_keywords"] = liked
            prefs["disliked_keywords"] = disliked
            msg = f"已排除关键词: {value}"
    
    elif ptype == "source":
        liked = prefs.get("liked_sources", [])
        disliked = prefs.get("disliked_sources", [])
        
        if action == "like":
            if value not in liked:
                liked.append(value)
            if value in disliked:
                disliked.remove(value)
            prefs["liked_sources"] = liked
            prefs["disliked_sources"] = disliked
            msg = f"已添加来源偏好: {value}"
        else:
            if value not in disliked:
                disliked.append(value)
            if value in liked:
                liked.remove(value)
            prefs["liked_sources"] = liked
            prefs["disliked_sources"] = disliked
            msg = f"已屏蔽来源: {value}"
    
    config["user_preferences"] = prefs
    config["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    save_user_config(config)
    return True, msg


def get_user_keywords():
    """获取用户偏好的关键词"""
    config = load_user_config()
    prefs = config.get("user_preferences", {})
    default_kw = config.get("default_keywords", {})
    
    # 合并所有默认关键词
    all_keywords = []
    for category, kws in default_kw.items():
        all_keywords.extend(kws)
    
    # 添加用户自定义关键词
    custom = prefs.get("custom_keywords", [])
    liked = prefs.get("liked_keywords", [])
    
    # 添加喜欢的，移除不喜欢的
    final_keywords = list(set(all_keywords + custom + liked))
    
    # 移除排除的
    excluded = prefs.get("disliked_keywords", [])
    final_keywords = [k for k in final_keywords if k not in excluded]
    
    return final_keywords


def get_user_sources():
    """获取用户偏好的来源"""
    config = load_user_config()
    prefs = config.get("user_preferences", {})
    
    liked = prefs.get("liked_sources", [])
    disliked = prefs.get("disliked_sources", [])
    
    return {"liked": liked, "disliked": disliked}


def verify_content_credibility(source_name, title, content):
    """
    验证内容可信度
    返回: {score: 0-100, level: 'A'/'B'/'C'/'D', reasons: []}
    """
    config = load_user_config()
    source_cred = config.get("source_credibility", {})
    rules = config.get("verification_rules", {})
    
    score = 50  # 基础分
    reasons = []
    
    # 1. 来源可信度
    source_info = source_cred.get(source_name, {})
    level = source_info.get("level", "C")
    level_scores = {"A": 90, "B": 70, "C": 50, "D": 30}
    source_score = level_scores.get(level, 50)
    
    if source_score >= 70:
        reasons.append(f"来源可信({source_info.get('name', source_name)})")
    else:
        reasons.append(f"来源可信度较低")
    
    # 2. 内容长度
    if len(content) > 200:
        score += 10
        reasons.append("内容详细")
    elif len(content) < 50:
        score -= 10
        reasons.append("内容过短")
    
    # 3. 敏感词检测
    suspicious = rules.get("suspicious_keywords", [])
    found_suspicious = [w for w in suspicious if w in title or w in content[:200]]
    if found_suspicious:
        score -= 15
        reasons.append(f"含敏感词: {', '.join(found_suspicious)}")
    
    # 4. 是否有原始链接
    has_source_link = "来源:" in content or "原文:" in content or "链接:" in content
    if has_source_link:
        score += 5
    
    # 5. 是否有时效性
    import re
    date_patterns = [
        r"\d{4}年\d{1,2}月\d{1,2}日",
        r"\d{4}-\d{2}-\d{2}",
        r"昨天|今天|刚刚|日前"
    ]
    has_date = any(re.search(p, title + content[:500]) for p in date_patterns)
    if has_date:
        score += 5
        reasons.append("有时效性标注")
    
    # 限制分数范围
    score = max(0, min(100, score))
    
    # 确定等级
    if score >= 90:
        level = "A"
    elif score >= 70:
        level = "B"
    elif score >= 50:
        level = "C"
    else:
        level = "D"
    
    return {
        "score": score,
        "level": level,
        "reasons": reasons,
        "source_info": source_info
    }


def filter_by_credibility(articles, min_level="D", min_score=0):
    """
    根据可信度过滤文章
    min_level: 最低可信度等级
    min_score: 最低可信度分数
    """
    config = load_user_config()
    source_cred = config.get("source_credibility", {})
    rules = config.get("verification_rules", {})
    
    level_order = {"A": 4, "B": 3, "C": 2, "D": 1}
    min_level_num = level_order.get(min_level, 1)
    
    filtered = []
    
    for article in articles:
        source = article.get("source", "")
        title = article.get("title", "")
        content = article.get("summary", "") + article.get("content", "")
        
        # 验证可信度
        result = verify_content_credibility(source, title, content)
        
        # 检查是否满足阈值
        level_num = level_order.get(result["level"], 1)
        
        if level_num >= min_level_num and result["score"] >= min_score:
            article["credibility"] = {
                "score": result["score"],
                "level": result["level"],
                "reasons": result["reasons"]
            }
            filtered.append(article)
    
    return filtered


def main():
    """测试反馈处理"""
    print("=" * 50)
    print("用户反馈处理测试")
    print("=" * 50)
    
    # 测试解析
    test_feedbacks = [
        "我喜欢GPU和显卡相关的新闻",
        "不喜欢自动驾驶的内容",
        "想要华为和昇腾的消息",
        "不要抖音字节的资讯"
    ]
    
    for fb in test_feedbacks:
        result = parse_feedback(fb)
        print(f"反馈: {fb}")
        print(f"解析: {result}")
        print()
    
    # 测试处理
    print("\n处理反馈:")
    for fb in test_feedbacks:
        success, msg = process_feedback(fb)
        print(f"  {fb} -> {msg}")
    
    # 显示当前关键词
    print(f"\n当前用户关键词数量: {len(get_user_keywords())}")
    
    # 测试可信度验证
    print("\n内容可信度验证:")
    test_articles = [
        {"source": "36kr", "title": "测试文章", "summary": "这是一篇测试文章内容"},
        {"source": "HackerNews", "title": "突发消息", "summary": "刚刚发生的"},
    ]
    
    for art in test_articles:
        result = verify_content_credibility(
            art["source"], 
            art["title"], 
            art["summary"]
        )
        print(f"  [{art['source']}] 分数: {result['score']}, 等级: {result['level']}")
        print(f"    原因: {', '.join(result['reasons'])}")


if __name__ == "__main__":
    main()