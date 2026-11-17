#!/usr/bin/env python3
"""
被动画像记录器
从对话中提取用户事实，多层置信度+衰减机制。

存储位置：memory/user_observations.json

Usage:
    python profile_observer.py --extract --text="对话内容"
    python profile_observer.py --list
    python profile_observer.py --decay  # 运行衰减
"""
import argparse
import json
import math
import os
import sys
from datetime import datetime


OBSERVATIONS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    '..', '..', 'memory', 'user_observations.json'
)

# 置信度层级
CONFIDENCE_LEVELS = {
    'explicit': 1.0,      # 用户明确陈述
    'strong_hint': 0.8,   # 强暗示（多次一致行为）
    'hint': 0.5,           # 弱暗示（单次行为）
    'inferred': 0.3,       # 推断（从其他事实推导）
}

# 衰减参数
DECAY_HALF_LIFE_DAYS = 90  # 半衰期90天
MIN_CONFIDENCE = 0.1       # 最低保留阈值


def load_observations():
    if os.path.exists(OBSERVATIONS_FILE):
        with open(OBSERVATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'observations': [], 'last_decay': datetime.now().isoformat()}


def save_observations(data):
    os.makedirs(os.path.dirname(OBSERVATIONS_FILE), exist_ok=True)
    with open(OBSERVATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_observation(category, fact, confidence='hint', source_text='', tags=None):
    """添加新的观察记录"""
    data = load_observations()
    
    # 检查是否已有相同事实
    for obs in data['observations']:
        if obs['fact'] == fact and obs['category'] == category:
            # 提升置信度
            old_conf = CONFIDENCE_LEVELS.get(obs['confidence'], 0.3)
            new_conf = min(1.0, old_conf + 0.2)
            obs['confidence'] = max(
                [k for k, v in CONFIDENCE_LEVELS.items() if v <= new_conf],
                key=lambda k: CONFIDENCE_LEVELS[k]
            )
            obs['last_seen'] = datetime.now().isoformat()
            obs['mention_count'] = obs.get('mention_count', 1) + 1
            save_observations(data)
            return {'status': 'updated', 'observation': obs}
    
    # 新增观察
    obs = {
        'category': category,
        'fact': fact,
        'confidence': confidence,
        'confidence_score': CONFIDENCE_LEVELS.get(confidence, 0.5),
        'source_text': source_text[:200],
        'tags': tags or [],
        'created': datetime.now().isoformat(),
        'last_seen': datetime.now().isoformat(),
        'mention_count': 1,
    }
    data['observations'].append(obs)
    save_observations(data)
    return {'status': 'created', 'observation': obs}


def apply_decay():
    """应用时间衰减"""
    data = load_observations()
    now = datetime.now()
    survived = []
    decayed_count = 0
    
    for obs in data['observations']:
        last_seen = datetime.fromisoformat(obs['last_seen'])
        days_elapsed = (now - last_seen).days
        
        # 计算衰减后的置信度
        original_score = obs.get('confidence_score', 0.5)
        decay_factor = math.pow(0.5, days_elapsed / DECAY_HALF_LIFE_DAYS)
        new_score = original_score * decay_factor
        
        if new_score >= MIN_CONFIDENCE:
            obs['confidence_score'] = round(new_score, 3)
            obs['decay_factor'] = round(decay_factor, 3)
            survived.append(obs)
        else:
            decayed_count += 1
    
    data['observations'] = survived
    data['last_decay'] = now.isoformat()
    save_observations(data)
    
    return {
        'status': 'decayed',
        'removed': decayed_count,
        'remaining': len(survived),
    }


def list_observations(category=None, min_confidence=0.0):
    """列出观察记录"""
    data = load_observations()
    obs = data['observations']
    
    if category:
        obs = [o for o in obs if o['category'] == category]
    if min_confidence > 0:
        obs = [o for o in obs if o.get('confidence_score', 0) >= min_confidence]
    
    # 按置信度排序
    obs.sort(key=lambda x: x.get('confidence_score', 0), reverse=True)
    
    return {
        'total': len(obs),
        'observations': obs,
    }


def main():
    parser = argparse.ArgumentParser(description='被动画像记录器')
    parser.add_argument('--extract', action='store_true', help='从文本提取观察')
    parser.add_argument('--text', help='对话文本')
    parser.add_argument('--category', help='观察类别')
    parser.add_argument('--fact', help='事实描述')
    parser.add_argument('--confidence', default='hint', choices=list(CONFIDENCE_LEVELS.keys()))
    parser.add_argument('--list', action='store_true', help='列出观察记录')
    parser.add_argument('--decay', action='store_true', help='运行衰减')
    parser.add_argument('--min-confidence', type=float, default=0.0)
    
    args = parser.parse_args()
    
    if args.extract and args.text:
        # 简单提取（实际使用时由 agent 调用，传入结构化的事实）
        result = add_observation(
            category=args.category or 'general',
            fact=args.text,
            confidence=args.confidence,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.fact:
        result = add_observation(
            category=args.category or 'general',
            fact=args.fact,
            confidence=args.confidence,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.list:
        result = list_observations(args.category, args.min_confidence)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.decay:
        result = apply_decay()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
