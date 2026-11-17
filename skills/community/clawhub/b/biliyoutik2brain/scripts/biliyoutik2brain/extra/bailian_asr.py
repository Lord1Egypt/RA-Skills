"""
百炼ASR API封装 — 双模型交叉验证的第二转录引擎

使用阿里云百炼/Model Studio qwen-audio-turbo-latest 语音识别服务。
与 whisper/faster-whisper 形成独立ASR源，用于交叉验证。

已验证: qwen-audio-turbo-latest 通过 DashScope 多模态生成端点可用
Endpoint: POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
"""

import os
import json
import time
import base64
import re
import requests
from typing import Optional, Tuple, List

from biliyoutik2brain.core.secrets import get_dashscope_key
from biliyoutik2brain.core.secrets import DASHSCOPE_MULTIMODAL_URL as _DASHSCOPE_URL

# ── 配置（从统一机密管理器获取） ──
DASHSCOPE_API_KEY = get_dashscope_key() or ""
MULTIMODAL_URL = _DASHSCOPE_URL


def transcribe_audio_segment(
    audio_path: str,
    language: str = "zh",
    model: str = "qwen-audio-turbo-latest",
    timeout: int = 120,
) -> Tuple[str, List[Tuple[str, float]]]:
    """用百炼ASR转写一段音频文件
    
    Args:
        audio_path: 音频文件路径 (wav/mp3)
        language: 语言 (zh/en, 暂只支持zh)
        model: 百炼音频模型 (仅 qwen-audio-turbo-latest 测试通过)
        timeout: 等待超时秒数
    
    Returns:
        (text, low_conf_words) — 文本 (无低置信词信息, 返回空列表)
    """
    if not os.path.isfile(audio_path):
        print(f"  [百炼ASR] 文件不存在: {audio_path}")
        return "", []
    
    # 读取音频文件 → base64
    try:
        with open(audio_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"  [百炼ASR] 读取失败: {e}")
        return "", []
    
    # 确定MIME类型
    mime = "audio/wav"
    ext = os.path.splitext(audio_path)[1].lower()
    if ext == ".mp3":
        mime = "audio/mp3"
    elif ext == ".m4a":
        mime = "audio/mp4"
    elif ext == ".ogg":
        mime = "audio/ogg"
    
    # 构建请求体 — 用多模态生成 API
    body = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"audio": f"data:{mime};base64,{audio_b64}"},
                        {"text": "请完整识别这段音频的内容，输出逐字文本，不要添加额外说明。"}
                    ]
                }
            ]
        }
    }
    
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        resp = requests.post(MULTIMODAL_URL, headers=headers, json=body, timeout=timeout)
    except requests.Timeout:
        print(f"  [百炼ASR] 超时({timeout}s)")
        return "", []
    except Exception as e:
        print(f"  [百炼ASR] 请求异常: {e}")
        return "", []
    
    if resp.status_code != 200:
        print(f"  [百炼ASR] 失败({resp.status_code}): {resp.text[:200]}")
        return "", []
    
    try:
        data = resp.json()
        choices = data.get("output", {}).get("choices", [])
        if not choices:
            print(f"  [百炼ASR] 响应无choices: {json.dumps(data)[:200]}")
            return "", []
        
        content = choices[0].get("message", {}).get("content", [])
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict):
                    text_parts.append(part.get("text", ""))
                else:
                    text_parts.append(str(part))
            full_text = " ".join(text_parts)
        else:
            full_text = str(content)
        
        return full_text.strip(), []
    except Exception as e:
        print(f"  [百炼ASR] 解析失败: {e}")
        return "", []


def cross_validate(
    whisper_text: str,
    bailian_text: str,
    ocr_persistent: str = "",
) -> List[dict]:
    """双模型交叉验证
    
    比较 whisper 和 百炼 的结果，输出差异分析。
    使用字符级和二/三字词级双重比较（中文无空格分词).
    
    Returns:
        [{"type": "bailian_only"|"whisper_only"|"overall", ...}]
    """
    if not bailian_text.strip():
        return [{"error": "百炼ASR无结果"}]
    if not whisper_text.strip():
        return [{"error": "whisper无结果"}]
    
    results = []
    
    # 预处理：去标点 + 归一空格
    def _clean(t):
        t = re.sub(r'[^\u4e00-\u9fff\w]', '', t)  # 去标点
        return t.strip()
    
    w_clean = _clean(whisper_text)
    b_clean = _clean(bailian_text)
    
    # 字符级比较（中文）
    w_chars = set(w_clean)
    b_chars = set(b_clean)
    w_only_chars = w_chars - b_chars
    b_only_chars = b_chars - w_chars
    
    # 双字词比较
    def _bigrams(s):
        return set(s[i:i+2] for i in range(len(s)-1))
    w_bigrams = _bigrams(w_clean)
    b_bigrams = _bigrams(b_clean)
    w_only_bigram = w_bigrams - b_bigrams
    b_only_bigram = b_bigrams - w_bigrams
    
    # 三字词比较
    def _trigrams(s):
        return set(s[i:i+3] for i in range(len(s)-2))
    w_trigrams = _trigrams(w_clean)
    b_trigrams = _trigrams(b_clean)
    
    if w_only_chars or b_only_chars:
        results.append({
            "type": "char_diff",
            "whisper_only": list(w_only_chars)[:15],
            "bailian_only": list(b_only_chars)[:15],
        })
    
    if w_only_bigram or b_only_bigram:
        results.append({
            "type": "bigram_diff",
            "whisper_only": list(w_only_bigram)[:15],
            "bailian_only": list(b_only_bigram)[:15],
        })
    
    # 总体一致率（字符级）
    total_chars = len(w_chars | b_chars)
    agree_chars = len(w_chars & b_chars)
    
    if total_chars > 0:
        results.append({
            "type": "overall",
            "whisper_len": len(w_clean),
            "bailian_len": len(b_clean),
            "agree_chars": agree_chars,
            "total_unique_chars": total_chars,
            "char_agreement_rate": round(agree_chars / total_chars * 100, 1),
            "whisper_bi": len(w_bigrams),
            "bailian_bi": len(b_bigrams),
            "bigram_agreement": round(len(w_bigrams & b_bigrams) / max(1, len(w_bigrams | b_bigrams)) * 100, 1),
            "trigram_agreement": round(len(w_trigrams & b_trigrams) / max(1, len(w_trigrams | b_trigrams)) * 100, 1),
        })
    
    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text, low_conf = transcribe_audio_segment(sys.argv[1])
        print(f"文本: {text[:300]}...")
        print(f"(共{len(text)}字)")
