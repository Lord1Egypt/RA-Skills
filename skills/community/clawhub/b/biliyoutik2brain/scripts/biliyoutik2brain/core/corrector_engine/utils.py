"""
BiliYouTik2Brain — Corrector Engine 共享工具函数

职责：被各层复用的纯函数（JSON提取、LLM调用封装、优先级排序）。
不包含任何业务逻辑。
"""

import os, sys, re, json, time
from typing import Dict, Optional, List, Tuple

_DEBUG = os.environ.get("BILI_DEBUG", "").lower() in ("1", "true", "yes")


# ═══════════════════════════════════════════════════════════════
# 安全浮点数解析
# ═══════════════════════════════════════════════════════════════

def safe_float(value, default=0.0) -> float:
    """将LLM返回的各种confidence格式转为float"""
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return default
    s = value.strip().lower()
    s = s.lstrip("<>")
    s = s.split("/")[0].split(",")[0].split("-")[0].strip()
    try:
        return float(s)
    except (ValueError, TypeError):
        return default


# ═══════════════════════════════════════════════════════════════
# JSON提取工具
# ═══════════════════════════════════════════════════════════════

def extract_json(text: str) -> Optional[dict]:
    """从LLM响应中提取JSON对象，容错处理"""
    if not text:
        return None
    
    text = text.strip()
    
    # 情况1: 完整JSON对象
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    
    # 情况2: 被markdown代码块包裹
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start) if "```" in text[start:] else len(text)
        candidate = text[start:end].strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            text = candidate
    elif "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start) if "```" in text[start:] else len(text)
        candidate = text[start:end].strip()
        if candidate.startswith("{"):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                text = candidate
    
    # 情况3: 从花括号开始截取
    brace_start = text.find("{")
    if brace_start >= 0:
        # 尝试逐位置找到匹配的闭合花括号
        depth = 0
        for i in range(brace_start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[brace_start:i+1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        pass
    
    # 情况4: 值内引号自修复
    try:
        return _extract_json_with_quote_fix(text)
    except Exception:
        pass
    
    return None


def _extract_json_with_quote_fix(text: str) -> Optional[dict]:
    """用上下文感知方式修复值内引号并解析JSON"""
    if not text:
        return None
    
    # 找到第一个{和最后一个}
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < 0 or end <= start:
        return None
    
    raw = text[start:end+1]
    
    # 尝试5种修复策略
    strategies = [
        lambda s: s,                                         # 原样
        lambda s: _fix_inner_quotes(s),                       # 值内引号替换
        lambda s: _fix_inner_quotes(_fix_unquoted_values(s)), # 引号+非引号值
        lambda s: re.sub(r"'([^']*?)'", r'"\1"', s),          # 单引号转双引号
        lambda s: _fix_inner_quotes(re.sub(r"'([^']*?)'", r'"\1"', s)),  # 全量组合
    ]
    
    for strategy in strategies:
        try:
            result = json.loads(strategy(raw))
            if isinstance(result, dict):
                return result
        except (json.JSONDecodeError, ValueError, TypeError):
            continue
    
    return None


def _fix_inner_quotes(s: str) -> str:
    """修复JSON值内部的引号问题：把值内的"替换为'"""
    result = []
    i = 0
    in_string = False
    string_start = -1
    
    while i < len(s):
        ch = s[i]
        if ch == '"' and (i == 0 or s[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_start = i
                result.append(ch)
            else:
                # 检查这个引号是否属于值内部
                # 向前看：值结束后的字符应该是, ] } 之一
                rest = s[i+1:].strip()
                if rest and not rest[0] in ',:]}\n':
                    # 值内引号，替换为单引号
                    result.append("'")
                else:
                    in_string = False
                    result.append(ch)
        else:
            result.append(ch)
        i += 1
    
    return ''.join(result)


def _fix_unquoted_values(s: str) -> str:
    """修复未被引号包裹的值"""
    # 匹配 key: value 模式，其中value不是字符串
    return re.sub(
        r'(:\s*)"?([^",}\]]+?)"?(?=[,}])',
        lambda m: m.group(1) + m.group(2) if m.group(2).strip().startswith('"') else m.group(1) + m.group(2),
        s
    )


def extract_json_array(text: str) -> Optional[list]:
    """从LLM响应中提取JSON数组，容错处理"""
    if not text:
        return None
    
    text = text.strip()
    
    # 完整数组
    if text.startswith("[") and text.endswith("]"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    
    # 被代码块包裹
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start) if "```" in text[start:] else len(text)
        candidate = text[start:end].strip()
        if candidate.startswith("["):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass
    
    # 范围截取
    start = text.find("[")
    end = text.rfind("]")
    if start >= 0 and end > start:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
    
    return None


# ═══════════════════════════════════════════════════════════════
# LLM调用（统一出口）
# ═══════════════════════════════════════════════════════════════

def call_llm(messages: List[Dict], timeout: int = 120) -> Optional[str]:
    """统一LLM调用出口。复用当前运行环境的DeepSeek配置。"""
    from ..secrets import get_llm_config
    import requests as _requests
    
    key, base, model = get_llm_config()
    if not key or not base:
        print("  ⚠️ [LLM] 无API配置，跳过")
        return None
    
    url = f"{base.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 8192,
        "temperature": 0.1,
    }
    
    try:
        r = _requests.post(url, headers=headers, json=payload, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not content:
                print(f"  ⚠️ [LLM] content为空 (推理模型: reasoning消耗全部token)")
            return content
        else:
            print(f"  ⚠️ [LLM] HTTP {r.status_code}: {r.text[:200]}")
            return None
    except Exception as e:
        print(f"  ⚠️ [LLM] 请求异常: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
# 优先级排序
# ═══════════════════════════════════════════════════════════════

def compute_priority(word: str) -> int:
    """计算词修正优先级（交易术语>常用词>人名地名）"""
    priority = 0
    from ..corrector_dictionary import TRADING_TERMS
    
    # +3: 交易术语
    if any(term and word and (term in word or word in term) for term in TRADING_TERMS):
        priority += 3
    # +2: 专有名词/复杂词
    if len(word) >= 4:
        priority += 2
    # +1: 多音节词
    if len(word) >= 3:
        priority += 1
    # +2: 含英文/数字
    if re.search(r'[a-zA-Z0-9]', word):
        priority += 2
    
    return priority


def is_noise_word(word: str) -> bool:
    """判断是否噪声词（单个字母/标点/常见助词/语气词）"""
    if len(word) <= 1:
        return True
    if word.strip() in "的了吗啊呢吧哦嗯哎":
        return True
    return False


def sort_low_conf_words(words: List[Tuple[str, float]]) -> List[Tuple[str, float, int]]:
    """按置信度升序+优先级降序排序"""
    scored = []
    for w, c in words:
        p = compute_priority(w)
        if not is_noise_word(w):
            scored.append((w, c, p))
    scored.sort(key=lambda x: (x[1], -x[2]))
    return scored
