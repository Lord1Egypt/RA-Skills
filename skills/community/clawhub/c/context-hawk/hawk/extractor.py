"""
Memory extractor for hawk-bridge

Receives conversation text from TypeScript hook via stdin.
Outputs JSON array of extracted memories to stdout.

Supports multiple backends:
- keyword (default, zero API needed — rule-based extraction)
- openai (requires key)
- groq (free Llama-3, no key needed for free tier)
- ollama (local, completely free)
- openrouter (free models available)

Usage:
  echo "conversation" | python3.12 -m hawk_memory.extractor --provider keyword
  echo "conversation" | python3.12 -m hawk_memory.extractor --provider groq
"""

import sys
import json
import os
import argparse
from typing import TypedDict

# ─── Tunable extraction parameters ─────────────────────────────────────────────
# Override via environment variables

EXTRACTION_TEMPERATURE = float(os.environ.get('HAWK_EXTRACTION_TEMPERATURE', '0.1'))
"""
LLM temperature for memory extraction.
Range: 0.0–1.0. Default 0.1.
- 0.0 = deterministic, best for extraction (factual consistency)
- Lower is better for extraction where factual accuracy matters more than variety.
"""

EXTRACTION_MAX_TOKENS = int(os.environ.get('HAWK_EXTRACTION_MAX_TOKENS', '2000'))
"""
Max tokens for LLM extraction response.
Default 2000. Increase if extracting very long memories.
"""

IMPORTANCE_KEYWORD_DEFAULT = float(os.environ.get('HAWK_IMPORTANCE_KEYWORD', '0.7'))
"""
Default importance for keyword-mode extraction when a keyword match is found.
Range: 0.0–1.0. Default 0.7.
"""


class ExtractedMemory(TypedDict):
    text: str
    category: str
    importance: float
    abstract: str
    overview: str


EXTRACTION_PROMPT = """你是一个记忆提取引擎。从以下对话内容中提取值得长期记忆的信息。

分类标准：
- fact: 客观事实、知识、数据
- preference: 用户偏好、习惯、风格
- decision: 用户做出的决定、选择、承诺
- entity: 用户提到的实体（人/公司/产品/项目）
- other: 其他值得记住的内容

输出要求：
- 只输出真正重要的信息，单条不超过200字
- 忽略寒暄、问候、确认类内容
- importance 0.0-1.0，表示这条记忆的重要程度
- abstract: 一句话概括
- overview: 结构化摘要

对话内容：
{conversation}

输出格式（JSON数组，无markdown）：
{format_example}"""

FORMAT_EXAMPLE = json.dumps([
    {"text": "示例记忆", "category": "fact", "importance": 0.8, "abstract": "一句话", "overview": "结构化摘要"}
])


def get_llm_client(provider: str, api_key: str, base_url: str = "", model: str = ""):
    """Get LLM client based on provider"""
    if provider == 'openclaw':
        # Uses OpenClaw's configured provider (Minimax etc.)
        base_url = base_url or os.environ.get("MINIMAX_BASE_URL", "https://api.minimaxi.com/anthropic")
        api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        model = model or os.environ.get("MINIMAX_MODEL", "MiniMax-M2.7")
        try:
            from openai import OpenAI
            return OpenAI(api_key=api_key, base_url=base_url)
        except ImportError:
            import urllib.request
            class OpenAIClient:
                def __init__(self, key, base, m):
                    self.key = key; self.base = base; self.model = m
                def chat(self):
                    pass
            return OpenAIClient(api_key, base_url, model)
    elif provider == 'groq':
        # Groq free tier - no API key needed for free models
        try:
            from groq import Groq
            return Groq(api_key=api_key or "free")
        except ImportError:
            # Fallback to OpenAI-compatible client
            class GroqClient:
                def __init__(self, key):
                    self.key = key
                    self.base_url = "https://api.groq.com/openai/v1"
                def chat(self):
                    pass
            return GroqClient(api_key)
    elif provider == 'ollama':
        class OllamaClient:
            def __init__(self, base_url):
                self.base_url = base_url or "http://localhost:11434"
                self.model = "llama3"
            def chat(self):
                pass
        return OllamaClient()
    elif provider == 'openrouter':
        try:
            from openai import OpenAI
            return OpenAI(
                api_key=api_key or "free",
                base_url="https://openrouter.ai/api/v1"
            )
        except ImportError:
            class FallbackClient:
                def chat(self):
                    pass
            return FallbackClient()
    else:
        # OpenAI compatible
        from openai import OpenAI
        return OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY", ""))


def extract_memories(conversation_text: str, api_key: str = "", model: str = "", provider: str = "openai", base_url: str = "") -> list[ExtractedMemory]:
    """使用配置的 LLM 从对话中提取记忆"""
    api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("GROQ_API_KEY") or os.environ.get("MINIMAX_API_KEY") or ""

    prompt = EXTRACTION_PROMPT.format(
        conversation=conversation_text,
        format_example=FORMAT_EXAMPLE
    )

    if provider == 'keyword':
        return extract_with_keyword(conversation_text)
    elif provider == 'openclaw':
        return extract_with_openclaw(prompt, api_key, model or os.environ.get("MINIMAX_MODEL", "MiniMax-M2.7"), base_url)
    elif provider == 'groq':
        return extract_with_groq(prompt, api_key, model or "llama-3.3-70b-versatile")
    elif provider == 'ollama':
        return extract_with_ollama(prompt, model or "llama3")
    elif provider == 'openrouter':
        return extract_with_openrouter(prompt, api_key, model or "google/gemma-2-9b-it")
    else:
        return extract_with_openai(prompt, api_key, model or "gpt-4o-mini")


def extract_with_keyword(conversation_text: str) -> list[ExtractedMemory]:
    """
    Zero-dependency keyword-based extraction.
    No API key needed — works completely offline.
    Uses pattern matching to identify important statements.

    Keywords are configurable via HAWK_KEYWORD_* env vars (comma-separated).
    Defaults work for Chinese; set HAWK_KEYWORD_LANG=en for English.
    """
    # Configurable via env vars; comma-separated strings
    _kw_fact = os.environ.get('HAWK_KEYWORD_FACT', '是,叫,名字是,在,位于,等于')
    _kw_pref = os.environ.get('HAWK_KEYWORD_PREF', '喜欢,希望,想要,倾向,偏好,不要,拒绝')
    _kw_dec = os.environ.get('HAWK_KEYWORD_DEC', '决定,选择,要用,采用,做,开始,停止,不买')
    _kw_ent = os.environ.get('HAWK_KEYWORD_ENT', '周,老板,老周,悟空,唐僧,趣近,取经')
    _kw_skip = os.environ.get('HAWK_KEYWORD_SKIP', '好的,收到,嗯,哈哈,ok,OK,了解,没问题,✅,👍')

    CATEGORIES = {
        'fact': _kw_fact.split(','),
        'preference': _kw_pref.split(','),
        'decision': _kw_dec.split(','),
        'entity': _kw_ent.split(','),
    }
    SKIP_WORDS = _kw_skip.split(',')

    lines = conversation_text.strip().split('\n')
    results = []
    seen_texts = set()

    for line in lines:
        line = line.strip()
        if len(line) < 5:
            continue
        # Skip greetings and acknowledgements
        if any(line.startswith(w) or line in SKIP_WORDS for w in SKIP_WORDS):
            continue

        # Categorize
        category = 'other'
        importance = 0.5
        for cat, keywords in CATEGORIES.items():
            for kw in keywords:
                if kw in line:
                    category = cat
                    importance = IMPORTANCE_KEYWORD_DEFAULT
                    break

        # Skip low-value lines
        if importance < 0.5:
            continue

        # Deduplicate
        text_normalized = line.lower()
        if text_normalized in seen_texts:
            continue
        seen_texts.add(text_normalized)

        results.append({
            'text': line[:200],
            'category': category,
            'importance': importance,
            'abstract': line[:50],
            'overview': f"[{category}] {line[:100]}",
        })

    return results[:5]  # Limit to 5


def extract_with_openai(prompt: str, api_key: str, model: str) -> list[ExtractedMemory]:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个精确的记忆提取引擎。只输出JSON数组，不输出任何其他内容。"},
            {"role": "user", "content": prompt}
        ],
        temperature=EXTRACTION_TEMPERATURE,
        max_tokens=2000,
    )
    return parse_and_validate(response.choices[0].message.content)


def extract_with_groq(prompt: str, api_key: str, model: str) -> list[ExtractedMemory]:
    """Groq free tier - no API key required for free models"""
    try:
        from groq import Groq
    except ImportError:
        # Fallback to direct API call
        import urllib.request
        data = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个精确的记忆提取引擎。只输出JSON数组，不输出任何其他内容。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": EXTRACTION_TEMPERATURE,
            "max_tokens": 2000,
        }).encode()
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {api_key or 'free'}",
                "Content-Type": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            content = result["choices"][0]["message"]["content"]
            return parse_and_validate(content)

    client = Groq(api_key=api_key or "dummy")  # Groq free tier doesn't require key for some models
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个精确的记忆提取引擎。只输出JSON数组，不输出任何其他内容。"},
            {"role": "user", "content": prompt}
        ],
        temperature=EXTRACTION_TEMPERATURE,
        max_tokens=2000,
    )
    return parse_and_validate(response.choices[0].message.content)


def extract_with_ollama(prompt: str, model: str) -> list[ExtractedMemory]:
    """Ollama local LLM - completely free"""
    import urllib.request
    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个精确的记忆提取引引擎。只输出JSON数组，不输出任何其他内容。"},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
        content = result["message"]["content"]
        return parse_and_validate(content)


def extract_with_openrouter(prompt: str, api_key: str, model: str) -> list[ExtractedMemory]:
    """OpenRouter - has free models"""
    import urllib.request
    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一个精确的记忆提取引引擎。只输出JSON数组，不输出任何其他内容。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": EXTRACTION_TEMPERATURE,
        "max_tokens": 2000,
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key or 'free'}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://hawk-bridge",
            "X-Title": "hawk-bridge",
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
        content = result["choices"][0]["message"]["content"]
        return parse_and_validate(content)


def extract_with_openclaw(prompt: str, api_key: str, model: str, base_url: str) -> list[ExtractedMemory]:
    """OpenClaw's configured provider (Minimax etc.) — uses OpenAI-compatible endpoint"""
    try:
        from openai import OpenAI
    except ImportError:
        import urllib.request
        # Minimax uses anthropic endpoint for chat, not /chat/completions
        # Strip /anthropic suffix if present (Minimax-specific), then use standard /chat/completions
        base = base_url.rstrip('/').replace('/anthropic', '')
        chat_url = base + '/chat/completions'
        data = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个精确的记忆提取引擎。只输出JSON数组，不输出任何其他内容。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": EXTRACTION_TEMPERATURE,
            "max_tokens": 2000,
        }).encode()
        req = urllib.request.Request(
            chat_url,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            content = result["choices"][0]["message"]["content"]
            return parse_and_validate(content)

    # Strip /anthropic suffix if present (Minimax-specific), then use standard /chat/completions
    chat_base = base_url.rstrip('/').replace('/anthropic', '')
    client = OpenAI(api_key=api_key, base_url=chat_base)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个精确的记忆提取引擎。只输出JSON数组，不输出任何其他内容。"},
            {"role": "user", "content": prompt}
        ],
        temperature=EXTRACTION_TEMPERATURE,
        max_tokens=2000,
    )
    return parse_and_validate(response.choices[0].message.content)


def parse_and_validate(content: str) -> list[ExtractedMemory]:
    """Parse and validate extracted memories"""
    # Strip markdown code blocks
    text = content.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:])

    try:
        memories = json.loads(text)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON parse failed: {e}", "raw": content[:500]}), file=sys.stderr)
        sys.exit(1)

    valid_categories = {"fact", "preference", "decision", "entity", "other"}
    validated = []
    for m in memories:
        if not isinstance(m, dict) or "text" not in m:
            continue
        cat = m.get("category", "other")
        if cat not in valid_categories:
            cat = "other"
        validated.append({
            "text": m["text"][:500],
            "category": cat,
            "importance": min(1.0, max(0.0, float(m.get("importance", 0.5)))),
            "abstract": m.get("abstract", "")[:100],
            "overview": m.get("overview", "")[:300],
        })
    return validated


def main():
    parser = argparse.ArgumentParser(description="hawk-bridge memory extractor")
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY", "") or os.environ.get("MINIMAX_API_KEY", ""))
    parser.add_argument("--model", default=os.environ.get("LLM_MODEL", "") or os.environ.get("MINIMAX_MODEL", "MiniMax-M2.7"))
    parser.add_argument("--provider", default=os.environ.get("LLM_PROVIDER", "keyword"),
                        choices=["keyword", "openai", "groq", "ollama", "openrouter", "openclaw"])
    parser.add_argument("--base-url", default=os.environ.get("LLM_BASE_URL", "") or os.environ.get("MINIMAX_BASE_URL", ""))
    args = parser.parse_args()

    conversation = sys.stdin.read()
    if not conversation.strip():
        print("[]")
        return

    try:
        memories = extract_memories(conversation, args.api_key, args.model, args.provider, args.base_url)
        print(json.dumps(memories, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
