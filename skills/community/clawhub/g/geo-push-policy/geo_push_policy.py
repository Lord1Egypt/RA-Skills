#!/usr/bin/env python3
"""
geo-push-policy - 推送策略管理

负责事件冷却期、观察池、频率限制等推送策略管理。
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Callable
from datetime import datetime

# =============================================================================
# 配置区
# =============================================================================

VERSION = "1.0.0"

# 冷却时间（分钟）
COOLDOWN_HIGH = 90
COOLDOWN_MEDIUM = 180

# 推送阈值
PUSH_THRESHOLD_HIGH = 70
PUSH_THRESHOLD_WATCH = 50

# 限制配置
MAX_EVENT_CACHE_SIZE = 50
MAX_WATCH_POOL_SIZE = 20
MAX_DEAD_LETTER_SIZE = 10
MAX_PUSH_COUNT = 3

# =============================================================================
# 数据结构
# =============================================================================

@dataclass
class AppState:
    """应用状态"""
    last_run_time: str = ""
    last_push_time: str = ""
    event_cache: Dict[str, Dict] = field(default_factory=dict)
    watch_pool: List[Dict] = field(default_factory=list)
    delivery: Dict = field(default_factory=dict)
    dead_letter_queue: List[Dict] = field(default_factory=list)
    last_error: str = ""
    
    def save(self, path: str):
        """保存状态到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(asdict(self), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存状态失败：{e}")
    
    @classmethod
    def load(cls, path: str) -> 'AppState':
        """从文件加载状态"""
        if not os.path.exists(path):
            return cls()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(**data)
        except Exception as e:
            print(f"⚠️  加载状态文件失败：{e}，使用空状态")
            return cls()

@dataclass
class PushPolicy:
    """推送策略配置"""
    cooldown_high: int = COOLDOWN_HIGH
    cooldown_medium: int = COOLDOWN_MEDIUM
    max_push_count: int = MAX_PUSH_COUNT
    threshold_high: int = PUSH_THRESHOLD_HIGH
    threshold_watch: int = PUSH_THRESHOLD_WATCH

# =============================================================================
# 推送决策
# =============================================================================

def should_push_event(event_dict: Dict, state: AppState, policy: Optional[PushPolicy] = None) -> Tuple[bool, str]:
    """
    判断事件是否应该推送
    
    考虑因素：
    - 评分是否达到阈值
    - 是否在冷却期内
    - 是否发生级别升级
    - 是否达到最大推送次数
    
    返回：(是否推送，原因)
    """
    if policy is None:
        policy = PushPolicy()
    
    score = event_dict.get('score', {})
    total_score = score.get('total', 0) if isinstance(score, dict) else 0
    event_id = event_dict.get('event_id', '')
    
    # 检查是否在 event_cache 中已有
    if event_id in state.event_cache:
        cached = state.event_cache[event_id]
        push_count = cached.get('push_count', 0)
        last_seen = cached.get('last_seen', '')
        severity = cached.get('severity', 'low')
        
        # 计算冷却时间
        cooldown = policy.cooldown_high if severity == 'high' else policy.cooldown_medium
        
        if last_seen:
            try:
                # 解析时间
                last_time_str = last_seen.replace('Z', '+00:00').replace('+08:00', '+08:00')
                if '+' not in last_time_str and 'Z' not in last_time_str:
                    last_time_str += '+08:00'
                last_time = datetime.fromisoformat(last_time_str)
                elapsed_minutes = (datetime.now(last_time.tzinfo) - last_time).total_seconds() / 60
                
                if elapsed_minutes < cooldown:
                    # 在冷却期内，检查是否升级
                    if total_score >= policy.threshold_high and push_count > 0:
                        return True, f"事件升级（冷却期内，评分{total_score}）"
                    return False, f"冷却期内（{elapsed_minutes:.0f}/{cooldown} 分钟）"
            except Exception as e:
                print(f"⚠️  解析时间失败：{e}")
        
        # 检查推送次数
        if push_count >= policy.max_push_count:
            return False, "已达到最大推送次数"
    
    # 新事件或可推送
    if total_score >= policy.threshold_high:
        return True, f"高优先级（评分{total_score}）"
    elif total_score >= policy.threshold_watch:
        return False, f"观察池（评分{total_score}）"
    else:
        return False, f"评分不足（{total_score}）"

def check_event_upgrade(event_dict: Dict, state: AppState) -> bool:
    """
    检查事件是否发生级别升级
    
    升级条件：
    - 评分从<70 上升到≥70
    - 新增权威来源
    - 市场联动扩大
    """
    event_id = event_dict.get('event_id', '')
    if event_id not in state.event_cache:
        return False
    
    cached = state.event_cache[event_id]
    old_severity = cached.get('severity', 'low')
    new_score = event_dict.get('score', {}).get('total', 0)
    
    # 评分升级
    if old_severity != 'high' and new_score >= PUSH_THRESHOLD_HIGH:
        return True
    
    return False

# =============================================================================
# 状态更新
# =============================================================================

def update_event_cache(state: AppState, events: List[Dict], push_events: List[Dict]):
    """
    更新事件缓存
    
    Args:
        state: 应用状态
        events: 所有事件列表
        push_events: 本次推送的事件列表
    """
    now = datetime.now().isoformat()
    push_event_ids = {e.get('event_id') for e in push_events}
    
    for event in events:
        event_id = event.get('event_id', '')
        event_data = dict(event)
        event_data['last_seen'] = now
        
        # 检查是否已有缓存
        cached = state.event_cache.get(event_id)
        if cached:
            # 保留旧数据
            event_data['push_count'] = cached.get('push_count', 0)
            event_data['first_seen'] = cached.get('first_seen', event_data.get('first_seen', now))
            
            # 如果本次推送，增加计数
            if event_id in push_event_ids:
                event_data['push_count'] += 1
                score = event.get('score', {}).get('total', 0)
                if score >= PUSH_THRESHOLD_HIGH:
                    event_data['severity'] = 'high'
                elif score >= PUSH_THRESHOLD_WATCH:
                    event_data['severity'] = 'medium'
        else:
            # 新事件
            if event_id in push_event_ids:
                event_data['push_count'] = 1
                score = event.get('score', {}).get('total', 0)
                if score >= PUSH_THRESHOLD_HIGH:
                    event_data['severity'] = 'high'
                elif score >= PUSH_THRESHOLD_WATCH:
                    event_data['severity'] = 'medium'
            else:
                event_data['push_count'] = 0
        
        state.event_cache[event_id] = event_data
    
    # 限制缓存大小
    if len(state.event_cache) > MAX_EVENT_CACHE_SIZE:
        sorted_events = sorted(
            state.event_cache.items(),
            key=lambda x: x[1].get('last_seen', ''),
            reverse=True
        )
        state.event_cache = dict(sorted_events[:MAX_EVENT_CACHE_SIZE])
    
    print(f"💾 事件缓存：{len(state.event_cache)}个事件")

def update_watch_pool(state: AppState, events: List[Dict], push_events: List[Dict]):
    """
    更新观察池
    
    Args:
        state: 应用状态
        events: 所有事件列表
        push_events: 本次推送的事件列表
    """
    now = datetime.now().isoformat()
    push_event_ids = {e.get('event_id') for e in push_events}
    
    for event in events:
        event_id = event.get('event_id', '')
        score = event.get('score', {}).get('total', 0)
        
        # 评分在 50-69 且未推送的事件加入观察池
        if event_id not in push_event_ids and PUSH_THRESHOLD_WATCH <= score < PUSH_THRESHOLD_HIGH:
            # 检查是否已在观察池中
            exists = any(w.get('event_id') == event_id for w in state.watch_pool)
            if not exists:
                state.watch_pool.append({
                    'event_id': event_id,
                    'title': event.get('title', ''),
                    'score': score,
                    'added_at': now,
                })
    
    # 限制观察池大小
    if len(state.watch_pool) > MAX_WATCH_POOL_SIZE:
        state.watch_pool = state.watch_pool[-MAX_WATCH_POOL_SIZE:]
    
    if state.watch_pool:
        print(f"👁️ 观察池：{len(state.watch_pool)}个事件")

def check_watch_pool_upgrade(state: AppState) -> List[Dict]:
    """
    检查观察池中是否有事件升级
    
    返回：需要推送的升级事件列表
    """
    upgrade_events = []
    
    for watch_item in state.watch_pool:
        event_id = watch_item.get('event_id', '')
        if event_id in state.event_cache:
            cached = state.event_cache[event_id]
            score = cached.get('score', {}).get('total', 0)
            
            # 评分上升到高优先级
            if score >= PUSH_THRESHOLD_HIGH:
                upgrade_events.append(cached)
    
    return upgrade_events

# =============================================================================
# 死信队列
# =============================================================================

def add_to_dead_letter_queue(state: AppState, message: str, events: List[Dict], error: str):
    """
    添加消息到死信队列
    
    Args:
        state: 应用状态
        message: 推送消息内容
        events: 相关事件列表
        error: 错误信息
    """
    state.dead_letter_queue.append({
        'message': message,
        'events': events,
        'failed_at': datetime.now().isoformat(),
        'error': error,
    })
    
    # 限制队列大小
    if len(state.dead_letter_queue) > MAX_DEAD_LETTER_SIZE:
        state.dead_letter_queue = state.dead_letter_queue[-MAX_DEAD_LETTER_SIZE:]
    
    print(f"📬 加入死信队列：{len(state.dead_letter_queue)} 条")

def process_dead_letter_queue(state: AppState, send_func: Callable[[str], bool]) -> bool:
    """
    处理死信队列（补投未送达的消息）
    
    Args:
        state: 应用状态
        send_func: 发送函数，接收消息字符串，返回是否成功
    
    返回：是否成功补投
    """
    if not state.dead_letter_queue:
        return False
    
    print(f"📬 处理死信队列：{len(state.dead_letter_queue)} 条")
    
    # 尝试补投最近一条
    dead_letter = state.dead_letter_queue[-1]
    message = dead_letter.get('message', '')
    
    if message:
        success = send_func(message)
        if success:
            state.dead_letter_queue.pop()
            print("✅ 死信补投成功")
            return True
        else:
            print("❌ 死信补投失败，保留在队列中")
    
    return False

# =============================================================================
# 频率限制保护
# =============================================================================

class RateLimiter:
    """频率限制器"""
    
    def __init__(self, max_calls: int = 1, period_seconds: int = 60):
        """
        初始化频率限制器
        
        Args:
            max_calls: 允许的最大调用次数
            period_seconds: 时间窗口（秒）
        """
        self.max_calls = max_calls
        self.period_seconds = period_seconds
        self.calls: List[float] = []
    
    def can_call(self) -> bool:
        """检查是否可以调用"""
        now = datetime.now().timestamp()
        
        # 移除过期调用记录
        self.calls = [t for t in self.calls if now - t < self.period_seconds]
        
        return len(self.calls) < self.max_calls
    
    def record_call(self):
        """记录一次调用"""
        self.calls.append(datetime.now().timestamp())
    
    def wait_time(self) -> float:
        """返回需要等待的时间（秒）"""
        if not self.calls:
            return 0
        
        now = datetime.now().timestamp()
        oldest = min(self.calls)
        
        return max(0, self.period_seconds - (now - oldest))

# =============================================================================
# 工具函数
# =============================================================================

def get_event_stage(event_dict: Dict, state: AppState) -> str:
    """
    获取事件阶段
    
    返回：new|escalating|ongoing|resolved
    """
    event_id = event_dict.get('event_id', '')
    
    if event_id not in state.event_cache:
        return 'new'
    
    cached = state.event_cache[event_id]
    push_count = cached.get('push_count', 0)
    stage = cached.get('stage', 'new')
    
    if push_count == 0:
        return 'new'
    elif push_count == 1:
        return 'escalating'
    elif push_count < MAX_PUSH_COUNT:
        return 'ongoing'
    else:
        return 'resolved'

def format_cooldown_message(event_dict: Dict, state: AppState) -> str:
    """
    格式化冷却期提示信息
    
    返回：冷却期提示字符串
    """
    event_id = event_dict.get('event_id', '')
    
    if event_id not in state.event_cache:
        return ""
    
    cached = state.event_cache[event_id]
    last_seen = cached.get('last_seen', '')
    severity = cached.get('severity', 'low')
    
    if not last_seen:
        return ""
    
    try:
        last_time_str = last_seen.replace('Z', '+00:00')
        if '+' not in last_time_str and 'Z' not in last_time_str:
            last_time_str += '+08:00'
        last_time = datetime.fromisoformat(last_time_str)
        elapsed_minutes = (datetime.now(last_time.tzinfo) - last_time).total_seconds() / 60
        
        cooldown = COOLDOWN_HIGH if severity == 'high' else COOLDOWN_MEDIUM
        remaining = max(0, cooldown - elapsed_minutes)
        
        if remaining > 0:
            return f"冷却期中，剩余{remaining:.0f}分钟"
    except:
        pass
    
    return ""
