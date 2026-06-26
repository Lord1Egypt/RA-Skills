"""buyer_id_list 入参解析工具（3 个客户深入分析能力共用）

支持的入参格式（强容错）：
- 标准 JSON 字符串数组：'["abc","def"]'  /  '["abc", "def"]'
- 标准 JSON 整数数组（兼容历史）：'[123,456]'  /  '[123, 456]'
- 逗号分隔字符串：'abc,def'  /  '123, 456'
- 空格分隔字符串：'abc def'
- 单个 ID：'abc'  /  '"abc"'  /  '123'
- 混合格式：'[abc, "def", 789]'

返回：(buyer_id_list, error_msg)
- 成功 → (list[str], None)
- 失败 → (None, str)  调用方据此 print_output(False, error_msg)

注意：后端 buyerIdList 入参类型为 Array<String>，加密格式 ID 直接透传即可。
"""

import json
import re
from typing import List, Optional, Tuple


def parse_buyer_id_list(raw: str) -> Tuple[Optional[List[str]], Optional[str]]:
    """把任意格式的 buyer-id-list 入参解析为字符串数组。

    严格保证：返回的列表元素全部是 Python str 类型，符合后端 Array<String> 契约。
    支持加密格式 ID（非数字字符串）直接透传。
    """
    if raw is None:
        return None, None

    s = raw.strip()
    if not s:
        return None, None

    # 第一阶段：尝试 JSON 解析（数组 / 单值）
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return _coerce_str_list(parsed)
        if isinstance(parsed, (int, str)):
            return _coerce_str_list([parsed])
    except (ValueError, TypeError):
        pass

    # 第二阶段：去掉外层方括号后按 , / 空格 切分
    inner = s
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    # 去掉所有引号
    inner = inner.replace('"', "").replace("'", "")
    # 按逗号 / 中文逗号 / 空格切分
    tokens = [t.strip() for t in re.split(r"[,，\s]+", inner) if t.strip()]
    if not tokens:
        return None, "❌ 客户 ID 列表为空"

    return _coerce_str_list(tokens)


def _coerce_str_list(items: list) -> Tuple[Optional[List[str]], Optional[str]]:
    """把 list 元素全部转为 str，过滤空值。"""
    result = []
    for x in items:
        if x is None:
            continue
        if isinstance(x, str):
            v = x.strip()
            if v:
                result.append(v)
        else:
            # int / float 等基础类型直接转字符串（兼容历史整数 ID）
            result.append(str(x))
    if not result:
        return None, "❌ 客户 ID 列表为空"
    return result, None
