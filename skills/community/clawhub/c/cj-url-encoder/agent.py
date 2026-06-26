from urllib.parse import quote, unquote
from typing import Dict, Any, Optional

def process_url_text(text: str, action: str = "encode") -> Dict[str, Any]:
    """
    对文本进行 URL 编码或解码。
    
    Args:
        text: 需要处理的字符串。
        action: 'encode' 或 'decode'。
        
    Returns:
        包含结果状态和内容的字典。
    """
    try:
        if action == "encode":
            # quote 默认会保留安全字符，safe='' 可以编码所有非字母数字字符，但通常默认行为更符合 URL 规范
            # 这里使用默认 safe 参数，保留 URL 常用分隔符如 : / ? # [ ] @ ! $ & ' ( ) * + , ; =
            # 如果用户想编码整个字符串包括分隔符，可以调整 safe 参数，但通常不需要。
            # 为了更严格的编码（例如用于 query parameter value），我们可以设置 safe=''
            # 这里为了通用性，我们采用较安全的默认策略，或者针对中文空格进行强编码。
            # 修正：为了处理中文链接中的空格和特殊字，通常我们需要编码除了 ~.-_ 之外的所有非 ASCII 字符。
            # urllib.parse.quote 默认 safe='/'，我们可以根据需要调整。
            # 最佳实践：编码时通常希望空格变 %20，中文变 hex。
            result = quote(text, safe='') # safe='' 表示除了字母数字外全部编码，最稳妥
            return {
                "success": True,
                "action": "encoded",
                "original": text,
                "result": result,
                "message": "编码成功。所有非字母数字字符均已转换。"
            }
            
        elif action == "decode":
            # unquote 会自动处理 %xx 格式
            result = unquote(text)
            return {
                "success": True,
                "action": "decoded",
                "original": text,
                "result": result,
                "message": "解码成功。"
            }
        else:
            return {
                "success": False,
                "error": "未知的操作类型，必须是 'encode' 或 'decode'。"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"处理失败: {str(e)}",
            "hint": "如果是解码失败，请检查字符串是否包含无效的 % 序列。"
        }

# 辅助函数：自动判断动作（可选，也可以让 LLM 决定）
def auto_process(text: str) -> Dict[str, Any]:
    """
    自动判断是编码还是解码。
    如果包含大量 % 且符合 hex 格式，尝试解码；否则编码。
    """
    import re
    # 简单的启发式判断：如果字符串中 % 后跟两个十六进制字符的比例很高，认为是编码过的
    hex_pattern = re.compile(r'%[0-9A-Fa-f]{2}')
    matches = hex_pattern.findall(text)
    
    # 如果超过 30% 的内容看起来像编码，或者用户明确说了“解码”（这步通常在 prompt 层处理，这里做兜底）
    # 这里简单处理：如果包含明显的中文或非 ASCII 字符，倾向于编码；如果全是 %xx 形式，倾向于解码
    has_non_ascii = any(ord(c) > 127 for c in text)
    
    if not has_non_ascii and len(matches) > len(text) * 0.3:
        return process_url_text(text, "decode")
    else:
        # 默认行为：如果不确定，且没有明显编码特征，执行编码（因为解码非编码字符串通常只是原样返回或报错，风险较小，但编码更有用）
        # 实际上，LLM 会在 SKILL.md 中根据用户指令决定调用哪个 action，这个函数主要供直接调用
        return process_url_text(text, "encode")