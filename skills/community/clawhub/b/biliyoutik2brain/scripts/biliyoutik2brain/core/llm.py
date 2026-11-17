"""
LLM 抽象层 (v3.0)

统一接口，多后端支持。中文友好 prompt 模板。
两个核心能力：correct(转录修正) + analyze(结构化分析)

支持的模型后端:
  - deepseek:   DeepSeek V4 (推荐, ¥0.001/1K tokens)
  - openai:     OpenAI 兼容 API (任意供应商)
  - ollama:     本地免费模型 (qwen2.5/llama3 等)
  - vllm:       本地 GPU 推理服务
"""

import os, json, time, hashlib
from typing import Dict, List, Optional, Iterator
from dataclasses import dataclass, field
from enum import Enum

# ═══════════════════════════════════════════════════════════════
#  缓存 (v3.1)
# ═══════════════════════════════════════════════════════════════

_CACHE_DIR = os.path.expanduser("~/.biliyoutik2brain")
_CACHE_FILE = os.path.join(_CACHE_DIR, "llm_cache.json")
os.makedirs(_CACHE_DIR, exist_ok=True)

def _cache_key(bvid: str, operation: str) -> str:
    return f"{bvid}|{operation}"

def _cache_get(key: str) -> Optional[Dict]:
    try:
        if os.path.exists(_CACHE_FILE):
            with open(_CACHE_FILE) as f:
                return json.load(f).get(key)
    except Exception:
        pass
    return None

def _cache_set(key: str, value: Dict):
    try:
        db = {}
        if os.path.exists(_CACHE_FILE):
            with open(_CACHE_FILE) as f:
                db = json.load(f)
        db[key] = value
        if len(db) > 500:
            db = dict(list(db.items())[-500:])
        with open(_CACHE_FILE, "w") as f:
            json.dump(db, f, ensure_ascii=False)
    except Exception:
        pass


@dataclass
class LLMConfig:
    """LLM 配置"""
    backend: str = "deepseek"
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    max_tokens: int = 4096
    temperature: float = 0.3
    timeout: int = 60
    max_retries: int = 2


@dataclass
class CorrectResult:
    """转录修正结果"""
    corrected_text: str
    corrections: List[Dict] = field(default_factory=list)
    confidence: float = 0.0
    tokens_used: int = 0
    elapsed_ms: int = 0
    backend: str = ""
    model: str = ""


@dataclass
class AnalysisResult:
    """结构化分析结果"""
    summary: str = ""
    keywords: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    chapters: List[Dict] = field(default_factory=list)
    raw_json: Dict = field(default_factory=dict)
    tokens_used: int = 0
    elapsed_ms: int = 0
    backend: str = ""
    model: str = ""


# ═══════════════════════════════════════════════════════════════
#  后端配置
# ═══════════════════════════════════════════════════════════════

def _load_workbuddy_api_key() -> str:
    """从 WorkBuddy 配置读取 API key（优先于环境变量）"""
    import json
    models_path = os.path.expanduser("~/.workbuddy/models.json")
    if os.path.exists(models_path):
        try:
            with open(models_path) as f:
                models = json.load(f)
            for m in models:
                if m.get("vendor", "").lower() == "deepseek":
                    return m.get("apiKey", "")
        except Exception:
            pass
    return ""


_BACKEND_CONFIGS = {
    "deepseek": LLMConfig(
        backend="deepseek",
        base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        api_key=_load_workbuddy_api_key() or os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("LLM_API_KEY", ""),
        model=os.environ.get("DEEPSEEK_MODEL") or os.environ.get("LLM_MODEL", "deepseek-chat"),
        max_tokens=4096,
    ),
    "openai": LLMConfig(
        backend="openai",
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        max_tokens=4096,
    ),
    "ollama": LLMConfig(
        backend="ollama",
        base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
        api_key="",  # Ollama 不需要 API key
        model=os.environ.get("OLLAMA_MODEL", "qwen2.5:7b"),
        max_tokens=2048,
    ),
    "vllm": LLMConfig(
        backend="vllm",
        base_url=os.environ.get("VLLM_BASE_URL", "http://localhost:8000/v1"),
        api_key=os.environ.get("VLLM_API_KEY", "not-needed"),
        model=os.environ.get("VLLM_MODEL", ""),
        max_tokens=4096,
    ),
}


def _get_config(backend: str = "auto") -> LLMConfig:
    """获取 LLM 配置（自动选择 + 环境变量覆盖）"""
    if backend == "auto":
        # 按优先级选择
        for name in ["deepseek", "openai", "ollama", "vllm"]:
            cfg = _BACKEND_CONFIGS[name]
            if name in ("ollama", "vllm"):
                if _check_backend_available(name):
                    return cfg
            elif cfg.api_key:
                return cfg
        for name in ["deepseek", "openai"]:
            return _BACKEND_CONFIGS[name]  # 乐观假设

    cfg = _BACKEND_CONFIGS.get(backend, _BACKEND_CONFIGS["deepseek"])
    # 允许环境变量覆盖 key/model
    env_key = f"{backend.upper()}_API_KEY"
    env_model = f"{backend.upper()}_MODEL"
    if os.environ.get(env_key):
        cfg.api_key = os.environ[env_key]
    if os.environ.get(env_model):
        cfg.model = os.environ[env_model]
    return cfg


def _check_backend_available(backend: str) -> bool:
    """检测后端是否可用"""
    if backend == "ollama":
        try:
            import subprocess
            r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=3)
            return r.returncode == 0
        except Exception:
            return False
    if backend == "vllm":
        try:
            import urllib.request
            url = _BACKEND_CONFIGS["vllm"].base_url.rstrip("/v1") + "/health"
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req, timeout=3)
            return resp.status == 200
        except Exception:
            return False
    return True


# ═══════════════════════════════════════════════════════════════
#  API 调用
# ═══════════════════════════════════════════════════════════════

def _call_openai_compatible(
    messages: List[Dict],
    config: LLMConfig,
    max_tokens: int = 4096,
    temperature: float = 0.3,
    stream: bool = False,
) -> Dict:
    """OpenAI 兼容 API 调用 (DeepSeek, OpenAI, vLLM 通用)"""
    import urllib.request, urllib.error

    url = config.base_url.rstrip("/") + "/chat/completions"
    model = config.model
    api_key = config.api_key

    if not api_key and config.backend not in ("vllm",):
        raise RuntimeError(f"{config.backend} API key 未设置")

    body = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
    }

    data = json.dumps(body).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    for attempt in range(config.max_retries + 1):
        try:
            resp = urllib.request.urlopen(req, timeout=config.timeout)
            result = json.loads(resp.read().decode("utf-8"))
            return result
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")[:300]
            if attempt < config.max_retries:
                wait = 2 ** attempt
                print(f"  [LLM] {config.backend} 请求失败 ({e.code}), {wait}s后重试...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"{config.backend} API 错误 ({e.code}): {error_body}") from e
        except Exception as e:
            if attempt < config.max_retries:
                wait = 2 ** attempt
                print(f"  [LLM] 网络错误, {wait}s后重试...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"{config.backend} 网络错误: {e}") from e


def _call_ollama(
    messages: List[Dict],
    config: LLMConfig,
    max_tokens: int = 2048,
    temperature: float = 0.3,
) -> Dict:
    """Ollama API 调用"""
    import urllib.request, urllib.error

    url = config.base_url.rstrip("/") + "/api/chat"
    model = config.model

    body = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": temperature,
        },
    }

    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    for attempt in range(config.max_retries + 1):
        try:
            resp = urllib.request.urlopen(req, timeout=config.timeout)
            return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < config.max_retries:
                time.sleep(2 ** attempt)
            else:
                raise RuntimeError(f"Ollama 调用失败: {e}") from e


# ═══════════════════════════════════════════════════════════════
#  Prompt 模板 (中文友好)
# ═══════════════════════════════════════════════════════════════

def _build_correction_prompt(
    text: str,
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
    speaker_context: str = "",
    low_conf_spans: List[str] = None,
    correction_hints: str = "",
) -> List[Dict]:
    """构建转录修正 prompt（中文优化）

    只在给定低置信区间内做修正，高置信部分直接保留。
    """
    system = """你是一位中文视频转录修正专家。任务是根据上下文修正转录错误，同时严格保持原文的语义。

核心原则：
1. 只修正明显的转录错误（同音词、术语误识别、数字错误）
2. 不要改变说话风格和语气
3. 不要添加、删减原文的实质内容（标点和分段不算实质内容）
4. 不要删除任何有效的句子
5. 金融术语修正优先级最高（如"运线→孕线"、"军线→均线"）
6. 排版整理（必做）：口语转录通常缺少标点和段落，请为全文补全标点符号（。？！，、；：以及引号），并按语义把内容切分为自然段落，段落之间用一个空行分隔。这是对口语转写的必要整理，不属于"添加原文没有的内容"。不要把每句话单独成行，要让连贯的句子组成完整段落。"""

    user_parts = []

    if video_title:
        user_parts.append(f"视频标题：{video_title}")
    if uploader:
        user_parts.append(f"说话人：{uploader}")
    if domain:
        user_parts.append(f"领域：{domain}")

    if speaker_context:
        user_parts.append(f"\n{speaker_context}")

    if correction_hints:
        user_parts.append(f"\n修正提示：\n{correction_hints}")

    if low_conf_spans:
        span_list = "\n".join(f"  · {s}" for s in low_conf_spans[:10])
        user_parts.append(f"\n以下是转录中置信度较低的片段（请重点检查修正）：\n{span_list}")
        user_parts.append("\n请重点修正上述低置信片段中的错误，其余文字保持原意不变（但仍需按系统要求补全标点、整理段落）。")

    user_parts.append(f"\n---\n{text}\n---")
    user_parts.append("\n请直接输出修正后的完整文本：补全标点、划分自然段落（段间空行），不要输出任何解释或标题。")

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n".join(user_parts)},
    ]


def _build_analysis_prompt(
    text: str,
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
) -> List[Dict]:
    """构建结构化分析 prompt"""
    system = """你是一位视频内容分析师。请分析以下视频转录文本，输出结构化JSON。

要求：
1. summary: 1-3句话概括核心内容
2. keywords: 5-10个关键术语
3. topics: 3-5个讨论的主题
4. chapters: 按时间线分段，每段包含 title 和 key_points

只输出JSON，不要有其他文字。"""

    user = f"""视频标题：{video_title}
说话人：{uploader or '未知'}
领域：{domain or 'general'}

文本：
{text[:3000]}

请输出JSON（必须包含 summary, keywords, topics, chapters 四个字段）："""

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


# ═══════════════════════════════════════════════════════════════
#  核心 API
# ═══════════════════════════════════════════════════════════════

def correct(
    text: str,
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
    speaker_context: str = "",
    low_conf_spans: List[str] = None,
    correction_hints: str = "",
    backend: str = "auto",
    bvid: str = "",          # v3.1: 缓存key
) -> CorrectResult:
    """转录文本修正

    v3.1: 按bvid缓存，同视频不重复调LLM
    """
    if not text or len(text) < 10:
        return CorrectResult(corrected_text=text, backend=backend)

    # ── v3.1: 缓存 (按bvid+chunk_hash) ──
    if bvid:
        chunk_hash = hashlib.md5(text[:200].encode()).hexdigest()[:8]
        cache_key = _cache_key(bvid, f"correct_{chunk_hash}")
        cached = _cache_get(cache_key)
        if cached:
            print(f"  [LLM/缓存] ✅ 命中! 跳过API")
            return CorrectResult(
                corrected_text=cached.get("text", text),
                backend=cached.get("backend", "cache"),
                model=cached.get("model", ""),
                tokens_used=0,
            )

    config = _get_config(backend)
    t0 = time.time()

    messages = _build_correction_prompt(
        text=text,
        video_title=video_title,
        uploader=uploader,
        domain=domain,
        speaker_context=speaker_context,
        low_conf_spans=low_conf_spans,
        correction_hints=correction_hints,
    )

    try:
        if config.backend == "ollama":
            resp = _call_ollama(messages, config)
            corrected = resp.get("message", {}).get("content", text)
            tokens = resp.get("eval_count", 0)
        else:
            resp = _call_openai_compatible(messages, config, max_tokens=4096)
            choice = resp.get("choices", [{}])[0]
            corrected = choice.get("message", {}).get("content", text)
            tokens = resp.get("usage", {}).get("total_tokens", 0)

        elapsed = int((time.time() - t0) * 1000)

        # 简单校验：修正后的文本不应该比原文短太多
        if len(corrected) < len(text) * 0.3:
            print(f"  [LLM] ⚠️ 修正结果过短({len(corrected)}字), 使用原文")
            corrected = text

        print(f"  [LLM] {config.backend}/{config.model} 修正完成 "
              f"({elapsed}ms, {tokens}tokens, {len(text)}→{len(corrected)}字)")

        # ── v3.1: 写缓存 ──
        if bvid:
            chunk_hash = hashlib.md5(text[:200].encode()).hexdigest()[:8]
            _cache_set(_cache_key(bvid, f"correct_{chunk_hash}"), {
                "text": corrected, "backend": config.backend, "model": config.model,
                "timestamp": time.time(),
            })

        return CorrectResult(
            corrected_text=corrected,
            confidence=0.7,
            tokens_used=tokens,
            elapsed_ms=elapsed,
            backend=config.backend,
            model=config.model,
        )

    except Exception as e:
        print(f"  [LLM] {config.backend} 修正失败: {e}")
        return CorrectResult(
            corrected_text=text,
            confidence=0.0,
            backend=config.backend,
            model=config.model,
        )


def analyze(
    text: str,
    video_title: str = "",
    uploader: str = "",
    domain: str = "",
    backend: str = "auto",
) -> AnalysisResult:
    """结构化分析"""

    if not text or len(text) < 20:
        return AnalysisResult(backend=backend)

    config = _get_config(backend)
    t0 = time.time()

    messages = _build_analysis_prompt(
        text=text,
        video_title=video_title,
        uploader=uploader,
        domain=domain,
    )

    try:
        if config.backend == "ollama":
            resp = _call_ollama(messages, config, max_tokens=1024)
            content = resp.get("message", {}).get("content", "{}")
            tokens = resp.get("eval_count", 0)
        else:
            resp = _call_openai_compatible(messages, config, max_tokens=2048, temperature=0.5)
            choice = resp.get("choices", [{}])[0]
            content = choice.get("message", {}).get("content", "{}")
            tokens = resp.get("usage", {}).get("total_tokens", 0)

        elapsed = int((time.time() - t0) * 1000)

        # 解析 JSON
        raw_json = {}
        try:
            # 清理可能的 markdown 代码块包装
            content = content.strip()
            if content.startswith("```"):
                content = content[content.find("\n")+1:]
                if content.endswith("```"):
                    content = content[:-3]
            raw_json = json.loads(content)
        except json.JSONDecodeError:
            print(f"  [LLM] JSON 解析失败，使用原始文本")
            raw_json = {"summary": content[:200], "keywords": [], "topics": [], "chapters": []}

        chapters = raw_json.get("chapters", [])
        if isinstance(chapters, list):
            chapters = [
                {"title": c.get("title", ""), "key_points": c.get("key_points", [])}
                for c in chapters[:10]
            ]

        print(f"  [LLM] {config.backend}/{config.model} 分析完成 "
              f"({elapsed}ms, {tokens}tokens, {len(raw_json.get('keywords',[]))}关键词)")

        return AnalysisResult(
            summary=raw_json.get("summary", ""),
            keywords=raw_json.get("keywords", []),
            topics=raw_json.get("topics", []),
            chapters=chapters,
            raw_json=raw_json,
            tokens_used=tokens,
            elapsed_ms=elapsed,
            backend=config.backend,
            model=config.model,
        )

    except Exception as e:
        print(f"  [LLM] {config.backend} 分析失败: {e}")
        return AnalysisResult(
            summary=text[:200],
            backend=config.backend,
            model=config.model,
        )


def check_available() -> List[str]:
    """检查当前环境可用的 LLM 后端"""
    available = []
    for name in _BACKEND_CONFIGS:
        if name in ("ollama", "vllm"):
            if _check_backend_available(name):
                available.append(name)
        elif _BACKEND_CONFIGS[name].api_key:
            available.append(name)
    if not available:
        available.append("deepseek")  # 乐观假设
    return available
