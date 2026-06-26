#!/usr/bin/env python3
"""
interceptor.py - 判断当前操作是否需要拦截
v2.0.0: auto_learn闭环 + 动态收件人判断

亲密信号 → 自动更新信任
降级信号 → 自动降低信任
"""

import json
import sys
import os
import re
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
TRUST_DB = os.path.join(SKILL_DIR, 'assets', 'trust_db.json')
TRUST_TRACKER = os.path.join(SCRIPT_DIR, 'trust_tracker.py')

# ============ 亲密信号检测 ============

INTIMATE_PATTERNS = [
    r'哈+', r'嗯嗯', r'ok', r'好的', r'行', r'收到',
    r'[wW]{1,}', r'\.\.\.', r'没啥', r'随便',
    r'感觉', r'其实', r'可能吧', r'算了'
]

SHORT_REPLY_THRESHOLD = 30

def detect_intimate_signals(message):
    """
    检测消息中的亲密信号
    返回: (是否亲密, 理由)
    """
    if not message:
        return False, "空消息"

    # 1. 检查语气词
    for pattern in INTIMATE_PATTERNS:
        if re.search(pattern, message):
            return True, f"语气词匹配:{pattern}"

    # 2. 检查短回复
    if len(message.strip()) < SHORT_REPLY_THRESHOLD:
        return True, f"短回复:{len(message)}字"

    return False, "无非亲密信号"

def detect_downgrade_signals(message):
    """
    检测降级信号（亲密→需确认）
    返回: (是否降级, 理由)
    """
    if not message:
        return False, "空消息"

    DOWNGRADE_PATTERNS = [
        r'等等', r'先别', r'确认', r'等等哈', r'不对',
        r'慢点', r'先问', r'等等等等', r'我看看', r'等一下'
    ]

    for pattern in DOWNGRADE_PATTERNS:
        if re.search(pattern, message):
            return True, f"降级信号:{pattern}"

    return False, "无降级信号"

# ============ 信任更新（auto_learn闭环）============

def auto_update_trust(recipient, operation_type):
    """
    自动更新信任（当亲密信号出现时调用）
    调用trust_tracker.py update
    """
    try:
        import subprocess
        result = subprocess.run(
            ['python3', TRUST_TRACKER, 'update', recipient, operation_type],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"自动更新失败: {e}"

def auto_downgrade_trust(recipient, operation_type):
    """
    自动降低信任（当降级信号出现时调用）
    重置该收件人的信任计数
    """
    try:
        import subprocess
        result = subprocess.run(
            ['python3', TRUST_TRACKER, 'reset', recipient],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"自动降级失败: {e}"

# ============ 动态收件人判断 ============

def is_high_risk_recipient_dynamic(recipient, context_message=None):
    """
    动态判断收件人是否高风险
    替代原来的硬编码关键词判断

    规则：
    - 'local'/'system' → 中性（本地操作）
    - 收件人包含特定关键词 → 仍为高风险
    - 收件人ID以特定前缀开头 → 高风险
    """
    # 中性上下文
    if recipient in ('local', 'system'):
        return False, 'neutral'

    # 从上下文消息推断
    if context_message:
        intimate, _ = detect_intimate_signals(context_message)
        downgrade, _ = detect_downgrade_signals(context_message)

        if downgrade:
            # 有降级信号 → 提高风险等级
            return True, '降级信号'
        if intimate:
            # 有亲密信号 → 降低风险等级
            return False, '亲密信号'

    # 保留必要的高风险标识（群聊、外部联系人）
    HIGH_RISK_RECIPIENTS = [
        'group:', 'chat:', '所有人', '@all', '@everyone',
        'external', '陌生'
    ]
    recipient_lower = recipient.lower()
    for pattern in HIGH_RISK_RECIPIENTS:
        if pattern in recipient_lower:
            return True, f'高风险标识:{pattern}'

    return False, '普通收件人'

# ============ 原有逻辑（保留兼容）============

HIGH_RISK_KEYWORDS = ['老板', 'boss', 'group', '群聊', '所有人', 'all']

def load_trust_db():
    if os.path.exists(TRUST_DB):
        with open(TRUST_DB, 'r') as f:
            return json.load(f)
    return {"contacts": {}}

def get_operation_risk(operation_type, args):
    risks = {
        'delete': 'medium',
        'send': 'high',
        'permission': 'high',
        'exec': 'high',
    }
    base_risk = risks.get(operation_type, 'medium')
    if operation_type == 'delete' and args:
        if '/tmp' in args[0]:
            return 'low'
    return base_risk

def get_recipient_risk(recipient, context_message=None):
    """
    判断收件人风险等级
    v2.0: 优先使用动态判断
    """
    # 动态判断（v2.0新增）
    is_high, reason = is_high_risk_recipient_dynamic(recipient, context_message)
    if is_high:
        return 'high'

    # 中性
    if recipient in ('local', 'system'):
        return 'neutral'

    # 低信任（3次确认）
    trust_db = load_trust_db()
    if 'contacts' in trust_db and recipient in trust_db['contacts']:
        total_confirms = sum(
            v.get('count', 0)
            for v in trust_db['contacts'][recipient].values()
        )
        if total_confirms >= 3:
            return 'low'

    return 'medium'

def check_trust_count(recipient, operation_type):
    trust_db = load_trust_db()
    if 'contacts' not in trust_db:
        return 0
    if recipient not in trust_db['contacts']:
        return 0

    op_data = trust_db['contacts'][recipient].get(operation_type, {})
    count = op_data.get('count', 0)
    last_confirm = op_data.get('lastConfirm')
    if last_confirm:
        try:
            last_time = datetime.fromisoformat(last_confirm)
            if datetime.now() - last_time > timedelta(days=7):
                return 0
        except:
            pass
    return count

def should_intercept(operation_type, recipient, args=None, context_message=None):
    """
    判断是否应该拦截
    v2.0: 增加context_message参数用于动态判断
    """
    if args is None:
        args = []
    if context_message is None:
        context_message = ""

    # auto_learn: 检测信号并自动更新/降级
    intimate, _ = detect_intimate_signals(context_message)
    downgrade, _ = detect_downgrade_signals(context_message)

    if intimate:
        auto_update_trust(recipient, operation_type)
    elif downgrade:
        auto_downgrade_trust(recipient, operation_type)

    op_risk = get_operation_risk(operation_type, args)
    rec_risk = get_recipient_risk(recipient, context_message)

    # 中性上下文
    if rec_risk == 'neutral':
        if op_risk == 'low':
            return False, "本地中性操作，操作风险低，自动放行"
        return True, f"本地操作，操作风险[{op_risk}]，需要确认"

    # 高风险收件人
    if rec_risk == 'high':
        return True, f"高风险收件人[{recipient}]，操作[{operation_type}]需要确认"

    # 中风险收件人
    if rec_risk == 'medium':
        return True, f"中风险收件人[{recipient}]，操作[{operation_type}]需要确认"

    # 低风险收件人
    if op_risk == 'low':
        return False, "低风险操作，自动放行"

    trust_count = check_trust_count(recipient, operation_type)
    if trust_count >= 3:
        return False, f"信任次数[{trust_count}]>=3，自动放行"
    else:
        return True, f"信任次数[{trust_count}]<3，操作[{operation_type}]需要确认"

def main():
    if len(sys.argv) < 3:
        print("用法: interceptor.py <操作类型> <收件人> [参数...]")
        sys.exit(1)

    operation_type = sys.argv[1]
    recipient = sys.argv[2]
    args = sys.argv[3:]

    # 从环境变量读取上下文消息（用于auto_learn）
    context_message = os.environ.get('INTERCEPTOR_CONTEXT', '')

    intercept, reason = should_intercept(operation_type, recipient, args, context_message)

    result = {
        "intercept": intercept,
        "reason": reason,
        "operation": operation_type,
        "recipient": recipient,
        "version": "2.0.0"
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not intercept else 1)

if __name__ == '__main__':
    main()
