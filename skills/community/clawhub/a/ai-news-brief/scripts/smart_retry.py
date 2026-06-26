#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能重试机制 + 失败记录
功能：
1. 每个获取方式最多重试2次
2. 失败后自动降低该方式优先级
3. 记录失败到配置文件
"""

import sys
import io
import os
import json
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "user_config")
CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "sites_config.json")
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "sites_config.json.default")
FAILURE_LOG_FILE = os.path.join(SCRIPT_DIR, "failure_log.json")

# 重试配置
MAX_RETRIES = 2  # 最多重试2次
FAILURE_THRESHOLD = 3  # 失败3次后降低优先级


def load_failure_log():
    """加载失败记录"""
    try:
        with open(FAILURE_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"failures": {}, "last_reset": datetime.now().strftime("%Y-%m-%d")}


def save_failure_log(log):
    """保存失败记录"""
    with open(FAILURE_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def record_failure(site_key, method, error_msg):
    """记录失败事件"""
    log = load_failure_log()
    
    if site_key not in log['failures']:
        log['failures'][site_key] = {}
    if method not in log['failures'][site_key]:
        log['failures'][site_key][method] = {"count": 0, "last_error": "", "last_time": ""}
    
    log['failures'][site_key][method]["count"] += 1
    log['failures'][site_key][method]["last_error"] = error_msg[:100]
    log['failures'][site_key][method]["last_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    save_failure_log(log)
    print(f"  ⚠️ 记录失败: {site_key}/{method} (累计{log['failures'][site_key][method]['count']}次)")


def get_failure_count(site_key, method):
    """获取失败次数"""
    log = load_failure_log()
    return log.get('failures', {}).get(site_key, {}).get(method, {}).get("count", 0)


def smart_fetch_with_retry(fetch_func, url, source_name, methods_priority):
    """
    智能重试获取
    - 按优先级顺序尝试每个方式
    - 每个方式最多重试 MAX_RETRIES 次
    - 失败后自动记录并切换到下一种方式
    """
    results = []
    last_error = ""
    
    for method in methods_priority:
        # 检查该方式的失败次数
        failure_count = get_failure_count(source_name, method)
        
        if failure_count >= FAILURE_THRESHOLD:
            print(f"  ⏭️ 跳过 {method} (失败{failure_count}次，已降权)")
            continue
        
        print(f"  尝试 {method} 方式 (失败{failure_count}次)...")
        
        for retry in range(MAX_RETRIES):
            try:
                if retry > 0:
                    print(f"    第{retry+1}次重试...")
                
                # 执行获取
                if method == 'rss':
                    results = fetch_func['rss'](url, source_name)
                elif method == 'http':
                    results = fetch_func['http'](url, source_name)
                elif method == 'chrome':
                    results = fetch_func['chrome'](url, source_name)
                
                if results and len(results) > 0:
                    print(f"  ✅ {method} 成功! 获取{len(results)}条")
                    return results, method, "success"
                
                last_error = "无结果"
                
            except Exception as e:
                last_error = str(e)[:50]
                print(f"    ❌ {method} 失败: {last_error}")
        
        # 记录失败
        record_failure(source_name, method, last_error)
    
    return [], "", "all_failed"


def update_site_priority_on_failure(site_key, method):
    """
    当某个方式连续失败后，自动降低其优先级
    """
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except:
        return
    
    if site_key not in config.get('sites', {}):
        return
    
    site = config['sites'][site_key]
    priority = site.get('priority', [])
    
    if method in priority:
        # 将失败的方式移到最后
        priority.remove(method)
        priority.append(method)
        config['sites'][site_key]['priority'] = priority
        config['sites'][site_key]['status'][method] = 'failed'
        
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"  📝 已更新 {site_key} 的优先级: {priority}")
        except:
            pass


def reset_failure_log():
    """重置失败记录（每天首次运行时调用）"""
    log = load_failure_log()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if log.get('last_reset') != today:
        log = {"failures": {}, "last_reset": today}
        save_failure_log(log)
        print("  🔄 失败记录已重置")


def get_optimized_priority(site_key, config):
    """
    获取优化后的优先级
    - 综合考虑配置的优先级和失败记录
    """
    if site_key not in config.get('sites', {}):
        return ['chrome']  # 默认
    
    site = config['sites'][site_key]
    base_priority = site.get('priority', ['rss', 'http', 'chrome'])
    
    # 根据失败次数调整优先级
    log = load_failure_log()
    adjusted_priority = []
    
    for method in base_priority:
        failure_count = log.get('failures', {}).get(site_key, {}).get(method, {}).get("count", 0)
        
        if failure_count >= FAILURE_THRESHOLD:
            # 失败太多，暂不考虑
            continue
        
        # 失败1-2次的排在后面
        if failure_count > 0:
            adjusted_priority.append(method)
        else:
            # 没失败的优先
            adjusted_priority.insert(0, method)
    
    # 如果都被降权了，使用全部
    if not adjusted_priority:
        adjusted_priority = base_priority
    
    return adjusted_priority


# ========== 改进的去重算法 ==========

def calculate_similarity(title1, title2):
    """
    计算两个标题的相似度
    返回 0-1 之间的分数，1表示完全相同
    支持中英文
    """
    if not title1 or not title2:
        return 0
    
    # 转为小写
    t1 = title1.lower()
    t2 = title2.lower()
    
    # 完全相同
    if t1 == t2:
        return 1.0
    
    # 包含关系
    if t1 in t2 or t2 in t1:
        return 0.8
    
    # 对于中文，按字符分割
    # 对于英文，按空格分割
    def tokenize(text):
        # 提取所有2-4个字的词组（中文）
        tokens = set()
        
        # 连续中文字符
        import re
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        tokens.update(chinese_words)
        
        # 连续英文字符
        english_words = re.findall(r'[a-zA-Z]{3,}', text)
        tokens.update(english_words)
        
        # 数字
        numbers = re.findall(r'\d+', text)
        tokens.update(numbers)
        
        return tokens
    
    tokens1 = tokenize(t1)
    tokens2 = tokenize(t2)
    
    if not tokens1 or not tokens2:
        return 0
    
    # Jaccard相似度
    common = tokens1 & tokens2
    union = tokens1 | tokens2
    
    if len(union) == 0:
        return 0
    
    similarity = len(common) / len(union)
    
    return similarity


def smart_deduplicate(articles, similarity_threshold=0.6):
    """
    智能去重
    - 使用标题相似度检测
    - 保留可信度更高的文章
    """
    if not articles:
        return []
    
    # 按可信度排序
    level_order = {"A": 4, "B": 3, "C": 2, "D": 1}
    articles.sort(key=lambda x: (
        level_order.get(x.get('credibility', {}).get('level', 'D'), 0),
        x.get('hot_score', 0)
    ), reverse=True)
    
    unique = []
    removed_count = 0
    
    for article in articles:
        is_duplicate = False
        
        for existing in unique:
            similarity = calculate_similarity(
                article.get('title', ''),
                existing.get('title', '')
            )
            
            if similarity >= similarity_threshold:
                is_duplicate = True
                removed_count += 1
                break
        
        if not is_duplicate:
            unique.append(article)
    
    if removed_count > 0:
        print(f"  🧹 智能去重: 移除{removed_count}条重复文章")
    
    return unique


# ========== 测试 ==========

def test_similarity():
    """测试相似度算法"""
    test_cases = [
        ("OpenAI发布新模型GPT-5", "OpenAI发布GPT-5新模型", 0.8),
        ("NVIDIA发布RTX 5090显卡", "AMD发布RX 9070显卡", 0.2),
        ("AI大模型周调用量超万亿", "中国AI大模型周调用量全球第一", 0.5),
    ]
    
    print("=" * 50)
    print("相似度算法测试")
    print("=" * 50)
    
    for t1, t2, expected in test_cases:
        sim = calculate_similarity(t1, t2)
        status = "✅" if sim >= expected else "❌"
        print(f"{status} \"{t1[:20]}...\" vs \"{t2[:20]}...\" = {sim:.2f} (期望≥{expected})")


if __name__ == "__main__":
    test_similarity()
    
    print("\n" + "=" * 50)
    print("重试机制测试")
    print("=" * 50)
    
    reset_failure_log()
    print(f"当前失败记录: {load_failure_log()['failures']}")