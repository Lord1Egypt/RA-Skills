#!/usr/bin/env python3
"""
geo-push-ops - 推送操作

负责飞书消息的构建、发送、重试和投递诊断。
"""

import json
import time
import requests
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

# =============================================================================
# 配置区
# =============================================================================

VERSION = "1.0.0"

# 飞书配置
FEISHU_RETRY_DELAY = 5      # 重试延迟（秒）
FEISHU_MAX_RETRIES = 3      # 最大重试次数
FEISHU_FREQUENCY_LIMIT_CODE = 11232  # 频率限制业务码

# =============================================================================
# 数据结构
# =============================================================================

@dataclass
class FeishuConfig:
    """飞书配置"""
    webhook: str = ""
    retry_delay: int = FEISHU_RETRY_DELAY
    max_retries: int = FEISHU_MAX_RETRIES

@dataclass
class MarketImpact:
    """市场影响数据（简化版）"""
    oil_pct: float = 0.0
    gold_pct: float = 0.0
    
    def is_high_priority(self) -> bool:
        return abs(self.oil_pct) >= 3.0 or abs(self.gold_pct) >= 2.0
    
    def is_watch_level(self) -> bool:
        return abs(self.oil_pct) >= 1.2 or abs(self.gold_pct) >= 0.8

@dataclass
class LLMAnalysis:
    """LLM 分析结果"""
    event_type: str = ""
    urgency: str = "低"
    novelty: str = "中"
    market_bias: str = "中性"
    reasoning: List[str] = field(default_factory=list)
    should_push: bool = False

@dataclass
class Event:
    """事件对象（简化版）"""
    event_id: str
    title: str
    event_type: str
    severity: str
    score: Dict
    llm_analysis: Optional[LLMAnalysis] = None
    market_impact: Optional[MarketImpact] = None
    sources: List[str] = field(default_factory=list)
    related_stocks: List[Dict] = field(default_factory=list)
    impact_path: str = ""
    stage: str = "new"

@dataclass
class DeliveryResult:
    """投递结果"""
    target: str = "feishu"
    attempts: int = 0
    http_status: int = 0
    biz_code: int = 0
    biz_msg: str = ""
    delivered: bool = False
    error: str = ""
    duration_ms: int = 0

# =============================================================================
# 消息模板
# =============================================================================

def build_feishu_message(events: List[Event], market: MarketImpact, llm_enabled: bool = False) -> str:
    """
    构建飞书消息（分层模板）
    
    Args:
        events: 事件列表
        market: 市场影响数据
        llm_enabled: 是否启用 LLM 分析
    
    Returns:
        消息文本
    """
    now = datetime.now().strftime("%H:%M")
    
    # 判断是否为高优先级警报
    is_high_priority = any(
        getattr(e, 'severity', 'low') == 'high' or 
        (isinstance(e.score, dict) and e.score.get('total', 0) >= 70)
        for e in events
    )
    
    if is_high_priority:
        return _build_high_priority_message(events, market, now, llm_enabled)
    else:
        return _build_observation_message(events, market, now, llm_enabled)

def _build_high_priority_message(events: List[Event], market: MarketImpact, now: str, llm_enabled: bool) -> str:
    """构建高优先级警报消息"""
    lines = [f"🚨 宏观地缘高优先级 | {now}"]
    lines.append("")
    
    for event in events[:3]:  # 最多显示 3 个
        lines.append(f"【事件】")
        lines.append(f"{event.title}")
        lines.append("")
        
        # 判断偏向
        bias = "中性"
        if event.llm_analysis:
            bias = event.llm_analysis.market_bias
        elif event.market_impact:
            if event.market_impact.oil_pct > 0:
                bias = "利多原油、油运、黄金"
            elif event.market_impact.oil_pct < 0:
                bias = "利空原油、利多航空"
        
        lines.append(f"【判断】")
        lines.append(f"偏{bias}")
        lines.append("")
        
        # 映射
        if event.related_stocks:
            sectors = set(s.get('sector', '') for s in event.related_stocks if s.get('sector'))
            if sectors:
                lines.append(f"【映射】")
                lines.append(f"{' / '.join(sectors)}")
                lines.append("")
        
        lines.append(f"【说明】")
        stage = getattr(event, 'stage', 'new')
        if stage == 'new':
            lines.append("当前为突发阶段，若后续出现官方确认或进一步升级，影响可能继续扩大。")
        elif stage == 'escalating':
            lines.append("事件正在升级，请密切关注后续发展。")
        else:
            lines.append("事件持续发酵中。")
        
        lines.append("")
        lines.append("---")
        lines.append("")
    
    lines.append("")
    lines.append(f"📡 数据源：财联社")
    if llm_enabled:
        lines.append("🧠 AI 语义分析：已启用")
    else:
        lines.append("🧠 AI 语义分析：未启用（降级模式）")
    
    return "\n".join(lines)

def _build_observation_message(events: List[Event], market: MarketImpact, now: str, llm_enabled: bool) -> str:
    """构建观察推送消息"""
    lines = [f"🦾 宏观地缘观察 | {now}"]
    lines.append("")
    lines.append("📰 最新动态")
    
    for event in events[:5]:
        severity = getattr(event, 'severity', 'low')
        icon = "🔥" if severity == 'high' else "⚠️" if severity == 'medium' else "○"
        lines.append(f"{icon} {event.title}")
    
    lines.append("")
    
    if market.is_watch_level():
        lines.append("📊 市场异动")
        if abs(market.oil_pct) >= 1.2:
            sign = "📈" if market.oil_pct > 0 else "📉"
            lines.append(f"{sign} 原油：{market.oil_pct:+.1f}%")
        if abs(market.gold_pct) >= 0.8:
            sign = "📈" if market.gold_pct > 0 else "📉"
            lines.append(f"{sign} 黄金：{market.gold_pct:+.1f}%")
        lines.append("")
    
    lines.append("---")
    lines.append("💡 当前为观察阶段，如有重大升级将单独推送")
    
    lines.append("")
    lines.append(f"📡 数据源：财联社")
    if llm_enabled:
        lines.append("🧠 AI 语义分析：已启用")
    else:
        lines.append("🧠 AI 语义分析：未启用（降级模式）")
    
    return "\n".join(lines)

def build_market_only_message(market: MarketImpact) -> str:
    """
    构建仅市场异动消息
    
    Args:
        market: 市场影响数据
    
    Returns:
        消息文本
    """
    now = datetime.now().strftime("%H:%M")
    lines = [f"📊 市场异动警报 | {now}"]
    lines.append("")
    
    if abs(market.oil_pct) >= 1.2:
        sign = "📈" if market.oil_pct > 0 else "📉"
        lines.append(f"{sign} 原油：{market.oil_pct:+.1f}%")
    
    if abs(market.gold_pct) >= 0.8:
        sign = "📈" if market.gold_pct > 0 else "📉"
        lines.append(f"{sign} 黄金：{market.gold_pct:+.1f}%")
    
    lines.append("")
    lines.append("⚠️ 商品价格出现显著波动，请密切关注相关地缘动态")
    
    return "\n".join(lines)

# =============================================================================
# 飞书发送
# =============================================================================

def send_to_feishu(message: str, config: Optional[FeishuConfig] = None) -> DeliveryResult:
    """
    发送飞书消息（带诊断和重试）
    
    Args:
        message: 消息文本
        config: 飞书配置（可选，使用默认 webhook）
    
    Returns:
        DeliveryResult 投递结果
    """
    if config is None:
        config = FeishuConfig(
            webhook="https://open.feishu.cn/open-apis/bot/v2/hook/cb9b2f26-c8be-483b-afca-2e4a59061e76"
        )
    
    result = DeliveryResult()
    payload = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    headers = {"Content-Type": "application/json"}
    
    for attempt in range(1, config.max_retries + 1):
        result.attempts = attempt
        start_time = time.time()
        
        try:
            resp = requests.post(config.webhook, json=payload, headers=headers, timeout=10)
            result.http_status = resp.status_code
            result.duration_ms = int((time.time() - start_time) * 1000)
            
            # 解析响应
            try:
                resp_data = resp.json()
                result.biz_code = resp_data.get('code', resp_data.get('StatusCode', 0))
                result.biz_msg = resp_data.get('msg', resp_data.get('statusMsg', ''))
            except:
                result.biz_msg = resp.text[:100]
            
            # 判断是否成功
            if resp.status_code == 200 and result.biz_code == 0:
                result.delivered = True
                print(f"✅ 飞书推送成功（尝试 {attempt} 次，耗时 {result.duration_ms}ms）")
                return result
            
            # 检查是否频率限制
            if result.biz_code == FEISHU_FREQUENCY_LIMIT_CODE or 'frequency' in result.biz_msg.lower():
                wait_time = config.retry_delay * attempt  # 递增延迟
                print(f"⚠️  飞书频率限制，等待 {wait_time}秒后重试...")
                time.sleep(wait_time)
                continue
            
            # 其他错误
            print(f"⚠️  飞书推送失败（HTTP {result.http_status}, 业务码 {result.biz_code}）: {result.biz_msg}")
            
            # 非频率限制错误不重试
            if attempt < config.max_retries:
                time.sleep(config.retry_delay)
                
        except requests.exceptions.RequestException as e:
            result.error = str(e)
            print(f"❌ 飞书推送异常（尝试 {attempt} 次）: {e}")
            if attempt < config.max_retries:
                time.sleep(config.retry_delay)
        except Exception as e:
            result.error = str(e)
            print(f"❌ 飞书推送异常（尝试 {attempt} 次）: {e}")
            break
    
    return result

def send_to_feishu_with_retry(message: str, webhook: str, max_retries: int = 3, retry_delay: int = 5) -> DeliveryResult:
    """
    发送飞书消息（简化版 API）
    
    Args:
        message: 消息文本
        webhook: Webhook URL
        max_retries: 最大重试次数
        retry_delay: 重试延迟（秒）
    
    Returns:
        DeliveryResult 投递结果
    """
    config = FeishuConfig(
        webhook=webhook,
        retry_delay=retry_delay,
        max_retries=max_retries,
    )
    return send_to_feishu(message, config)

# =============================================================================
# 投递诊断
# =============================================================================

def diagnose_delivery_result(result: DeliveryResult) -> Dict:
    """
    诊断投递结果
    
    返回：{
        'success': bool,
        'error_type': str,
        'suggestion': str,
    }
    """
    diagnosis = {
        'success': result.delivered,
        'error_type': 'none',
        'suggestion': '',
    }
    
    if result.delivered:
        diagnosis['suggestion'] = '推送成功，无需处理'
        return diagnosis
    
    # HTTP 错误
    if result.http_status == 0:
        diagnosis['error_type'] = 'network_error'
        diagnosis['suggestion'] = '检查网络连接或 webhook URL'
        return diagnosis
    
    if result.http_status != 200:
        diagnosis['error_type'] = 'http_error'
        diagnosis['suggestion'] = f'HTTP {result.http_status}，检查 webhook 配置'
        return diagnosis
    
    # 业务错误
    if result.biz_code == FEISHU_FREQUENCY_LIMIT_CODE:
        diagnosis['error_type'] = 'rate_limit'
        diagnosis['suggestion'] = '触发频率限制，降低推送频率或增加重试延迟'
        return diagnosis
    
    if result.biz_code == 99991504:
        diagnosis['error_type'] = 'invalid_webhook'
        diagnosis['suggestion'] = 'Webhook URL 无效，检查机器人配置'
        return diagnosis
    
    diagnosis['error_type'] = 'unknown'
    diagnosis['suggestion'] = f'未知错误：{result.biz_msg}'
    return diagnosis

def format_delivery_log(result: DeliveryResult) -> str:
    """
    格式化投递日志
    
    返回：日志字符串
    """
    status = "✅ 成功" if result.delivered else "❌ 失败"
    lines = [
        f"📤 投递结果：{status}",
        f"   目标：{result.target}",
        f"   尝试：{result.attempts} 次",
        f"   HTTP: {result.http_status}",
        f"   业务码：{result.biz_code}",
        f"   耗时：{result.duration_ms}ms",
    ]
    
    if result.error:
        lines.append(f"   错误：{result.error}")
    if result.biz_msg:
        lines.append(f"   消息：{result.biz_msg}")
    
    return "\n".join(lines)

# =============================================================================
# 工具函数
# =============================================================================

def validate_webhook(webhook: str) -> bool:
    """
    验证飞书 webhook URL 格式
    
    返回：是否有效
    """
    if not webhook:
        return False
    
    # 基本格式检查
    if not webhook.startswith('https://open.feishu.cn/open-apis/bot/v2/hook/'):
        return False
    
    # 长度检查（应该有足够的随机字符）
    if len(webhook) < 80:
        return False
    
    return True

def truncate_message(message: str, max_length: int = 10000) -> str:
    """
    截断消息（飞书有长度限制）
    
    返回：截断后的消息
    """
    if len(message) <= max_length:
        return message
    
    # 保留完整的前面部分
    truncated = message[:max_length - 100]
    truncated += f"\n\n...（内容过长，已截断）"
    
    return truncated

def count_events_in_message(message: str) -> int:
    """
    统计消息中的事件数量
    
    返回：事件数量
    """
    # 简单统计：计算"【事件】"的出现次数
    return message.count("【事件】")
