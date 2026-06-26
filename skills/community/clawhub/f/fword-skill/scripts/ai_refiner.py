"""AI-powered refinement of raw LaTeX output.

Supports multiple LLM providers:
  - Anthropic (Claude) — native SDK
  - OpenAI, Qwen/Bailian, Kimi, MiniMax, DeepSeek, Zhipu — via OpenAI-compatible API
"""

import os
import sys
import textwrap

PROVIDERS = {
    "anthropic": {
        "base_url": None,
        "default_model": "claude-sonnet-4-20250514",
        "env_key": "ANTHROPIC_API_KEY",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o",
        "env_key": "OPENAI_API_KEY",
    },
    "qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
        "env_key": "DASHSCOPE_API_KEY",
    },
    "kimi": {
        "base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-8k",
        "env_key": "MOONSHOT_API_KEY",
    },
    "minimax": {
        "base_url": "https://api.minimax.chat/v1",
        "default_model": "MiniMax-Text-01",
        "env_key": "MINIMAX_API_KEY",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
        "env_key": "DEEPSEEK_API_KEY",
    },
    "zhipu": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4-plus",
        "env_key": "ZHIPU_API_KEY",
    },
}

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a LaTeX expert. Your job is to refine raw LaTeX that was auto-converted
    from a Word document by Pandoc. The input LaTeX is functional but has issues:

    Common problems to fix:
    1. Broken or malformed math equations (OMML artifacts, wrong delimiters)
    2. Ugly table formatting (missing column specs, wrong alignment)
    3. Incorrect or missing figure/image references
    4. Redundant or conflicting packages in the preamble
    5. Poor document structure (wrong sectioning levels, missing labels)
    6. Raw formatting commands that should be semantic
    7. Encoding issues and special character escaping

    Rules:
    - Output ONLY the refined LaTeX. No explanations, no markdown code fences.
    - Preserve ALL content — do not remove or summarize any text.
    - Fix formatting and structure, but keep the document's meaning identical.
    - Use standard LaTeX packages (amsmath, graphicx, hyperref, booktabs, etc.)
    - Make tables use booktabs style when possible.
    - Ensure all math is properly delimited with $ $, \\[ \\], or equation environments.
    - Keep it compilable — the output must work with pdflatex or xelatex.
""")


def _chunk_latex(latex: str, chunk_size: int = 200) -> list[str]:
    """Split LaTeX into chunks, trying to break at section boundaries."""
    lines = latex.split("\n")
    if len(lines) <= chunk_size:
        return [latex]

    chunks = []
    current: list[str] = []
    for line in lines:
        current.append(line)
        if len(current) >= chunk_size and (
            line.startswith("\\section")
            or line.startswith("\\subsection")
            or line.startswith("\\chapter")
            or line.strip() == ""
        ):
            chunks.append("\n".join(current))
            current = []
    if current:
        chunks.append("\n".join(current))
    return chunks


def _call_anthropic(api_key: str, model: str, system: str, prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=8192,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _call_openai_compatible(api_key: str, base_url: str, model: str, system: str, prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        max_tokens=8192,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def refine_latex(
    raw_latex: str,
    metadata: dict | None = None,
    provider: str = "anthropic",
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
) -> str:
    """Use AI to refine raw pandoc LaTeX into clean output.

    Supports: anthropic, openai, qwen, kimi, minimax, deepseek, zhipu.
    """
    metadata = metadata or {}
    preset = PROVIDERS.get(provider, {})
    env_key = preset.get("env_key", "API_KEY")
    model = model or preset.get("default_model", "")
    base_url = base_url or preset.get("base_url")

    api_key = api_key or os.environ.get(env_key)
    if not api_key:
        print(f"WARNING: No {env_key} set. Skipping AI refinement.", file=sys.stderr)
        return raw_latex

    chunks = _chunk_latex(raw_latex)
    refined_parts = []

    for i, chunk in enumerate(chunks):
        meta_str = ""
        if metadata.get("title"):
            meta_str += f"Document title: {metadata['title']}\n"
        if metadata.get("author"):
            meta_str += f"Author: {metadata['author']}\n"

        if i == 0:
            prompt = (
                f"{meta_str}\nHere is the raw Pandoc-converted LaTeX. "
                "Please refine it into clean, compilable LaTeX:\n\n"
                f"{chunk}"
            )
        else:
            prompt = (
                f"This is chunk {i + 1} of a multi-part document. "
                "Continue refining. Do NOT include \\documentclass or preamble — "
                "only output the body content.\n\n"
                f"{chunk}"
            )

        if len(chunks) > 1:
            print(f"  Refining chunk {i + 1}/{len(chunks)}...", file=sys.stderr)

        if provider == "anthropic":
            text = _call_anthropic(api_key, model, SYSTEM_PROMPT, prompt)
        else:
            text = _call_openai_compatible(api_key, base_url, model, SYSTEM_PROMPT, prompt)

        refined_parts.append(text)

    return "\n\n".join(refined_parts)
