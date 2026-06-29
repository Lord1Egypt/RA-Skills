"""
compress.py — 零 LLM 合成压缩
将原始观察数据结构化，不经 LLM 直接索引。
由 observe hook 或 heartbeat 调用。

用法: python scripts/compress.py --input <json-file> [--output <json-file>]
      python scripts/compress.py --process-queue   (处理观察队列)
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

# 观察类型（规则驱动）
OBSERVATION_TYPES = {
    "file_read", "file_write", "file_edit", "command_run",
    "search", "web_fetch", "conversation", "error",
    "decision", "discovery", "subagent", "task", "other"
}

# 技术关键词表（可扩展）
TECH_KEYWORDS = {
    "python", "javascript", "typescript", "rust", "go", "node",
    "react", "vue", "angular", "django", "flask", "fastapi",
    "sql", "postgresql", "mysql", "sqlite", "redis", "mongodb",
    "docker", "kubernetes", "nginx", "git", "api", "rest",
    "graphql", "websocket", "oauth", "jwt", "auth", "middleware",
    "vector", "embedding", "qdrant", "llm", "openai", "claude",
    "embedding", "token", "prompt", "model", "training",
    "pytest", "jest", "unittest", "ci/cd", "github", "action",
    "Lambda", "cache", "webhook", "session", "async",
}

# 重要性评分规则
IMPORTANCE_RULES = [
    # (匹配条件, 重要性)
    (lambda t, o: t == "file_read", 2),
    (lambda t, o: t == "file_edit", 5),
    (lambda t, o: t == "file_write" and len(o or "") > 200, 6),
    (lambda t, o: t == "command_run", 4),
    (lambda t, o: t == "error", 7),
    (lambda t, o: t == "decision", 8),
    (lambda t, o: t == "discovery", 8),
    (lambda t, o: "error" in (o or "").lower() or "failed" in (o or "").lower(), 6),
    (lambda t, o: "api" in (o or "").lower() and "key" in (o or "").lower(), 8),
    (lambda t, o: "配置" in (o or "") or "config" in (o or "").lower(), 5),
    (lambda t, o: True, 3),  # default
]


def derive_type(hook_type: str, tool_name: str = "",
                tool_input: str = "", tool_output: str = "",
                user_prompt: str = "") -> str:
    """规则驱动类型推导，0 token"""
    t = tool_name.lower() if tool_name else ""
    inp = tool_input.lower() if tool_input else ""
    out = tool_output.lower() if tool_output else ""
    prompt = user_prompt.lower() if user_prompt else ""

    if hook_type == "subagent_start" or hook_type == "subagent_stop":
        return "subagent"
    if t in ("read",):
        return "file_read"
    if t in ("write", "create"):
        return "file_write"
    if t in ("edit", "patch"):
        return "file_edit"
    if t in ("exec", "run", "command"):
        return "command_run"
    if t in ("web_search", "search"):
        return "search"
    if t in ("web_fetch", "fetch"):
        return "web_fetch"
    # 输出包含错误
    if any(w in out for w in ["error", "failed", "exception", "traceback", "fatal"]):
        return "error"
    if hook_type in ("task_completed",):
        return "task"
    # 决策/发现优先于 conversation
    if any(w in prompt for w in ["决定", "选", "不用", "放弃", "换成"]):
        return "decision"
    if any(w in prompt for w in ["发现", "原来", "实际上", "其实是"]):
        return "discovery"
    if hook_type in ("prompt_submit",) and not t:
        return "conversation"
    return "other"


def extract_concepts(inp: str, out: str, prompt: str) -> list:
    """从输入输出中提取技术概念"""
    combined = f"{inp} {out} {prompt}".lower()
    found = set()
    for kw in TECH_KEYWORDS:
        if kw in combined:
            found.add(kw)
    # 提取文件名中的扩展名和技术后缀
    file_exts = re.findall(r'\.(\w+)(?:\s|$|/)', combined)
    for ext in file_exts:
        if ext in ("py", "js", "ts", "rs", "go", "java", "sql", "yaml", "yml",
                    "json", "md", "html", "css", "sh", "bat", "ps1", "tf",
                    "dockerfile", "toml", "ini", "cfg", "conf"):
            found.add(f".{ext}")
    return sorted(found)


def extract_file_paths(inp: str, out: str) -> list:
    """提取文件路径"""
    combined = f"{inp} {out}"
    # Windows 路径
    paths = re.findall(r'[A-Za-z]:\\[^\s\'\"<>|]+', combined)
    # Unix 路径
    paths += re.findall(r'(?:/[\w\.-]+)+', combined)
    # 相对路径
    paths += re.findall(r'(?:\.\.?/[\w\.-]+)+', combined)
    return list(set(p.replace("\\", "/") for p in paths))


def score_importance(obs_type: str, tool_output: str) -> int:
    """基于规则的重要性评分"""
    for condition, score in IMPORTANCE_RULES:
        if condition(obs_type, tool_output):
            return score
    return 3


def summarize_narrative(tool_output: str, obs_type: str) -> str:
    """从 tool output 截取叙事（0 token）"""
    if not tool_output or not tool_output.strip():
        # 没有输出时用类型描述兜底
        type_desc = {
            "file_read": "读取了文件",
            "file_write": "写入了文件",
            "file_edit": "编辑了文件",
            "command_run": "执行了命令",
            "error": "发生了错误",
            "web_search": "执行了网页搜索",
            "web_fetch": "抓取了网页内容",
            "memory_search": "搜索了记忆库",
            "memory_get": "获取了记忆内容",
            "agent_call": "调用了子Agent",
            "tool_call": "调用了工具",
            "config_change": "修改了配置",
        }
        return type_desc.get(obs_type, f"执行了{obs_type}操作")

    # 截取前 200 字符作为叙事
    clean = tool_output.strip()[:200]
    if len(tool_output) > 200:
        clean += "..."
    return clean


def extract_facts(tool_output: str, obs_type: str) -> list:
    """从输出中提取关键事实"""
    facts = []
    if not tool_output:
        return facts
    lines = tool_output.strip().split("\n")
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 10 and len(line) < 200:
            # 过滤掉噪音行
            if not line.startswith(("#", "//", "--", "*", "```")):
                facts.append(line.strip("- "))
    return facts[:3]


def derive_title(obs_type: str, tool_name: str, inp: str, prompt: str) -> str:
    """规则驱动标题提取"""
    if obs_type == "file_read":
        match = re.search(r'[\w\\/-]+\.[\w]+', inp)
        return f"读取文件: {match.group()}" if match else "读取文件"
    elif obs_type == "file_edit":
        match = re.search(r'[\w\\/-]+\.[\w]+', inp)
        return f"编辑文件: {match.group()}" if match else "编辑文件"
    elif obs_type == "file_write":
        match = re.search(r'[\w\\/-]+\.[\w]+', inp)
        return f"写入文件: {match.group()}" if match else "写入文件"
    elif obs_type == "command_run":
        cmd = inp.strip()[:60] if inp else ""
        return f"执行: {cmd}" if cmd else "执行命令"
    elif obs_type == "error":
        err = tool_output.strip()[:60] if tool_output else ""
        return f"错误: {err}" if err else "发生错误"
    elif obs_type == "decision":
        return f"决策: {prompt[:60]}" if prompt else "做出决策"
    elif obs_type == "discovery":
        return f"发现: {prompt[:60]}" if prompt else "发现"
    elif obs_type == "search":
        return f"搜索: {tool_name}"
    elif obs_type == "subagent":
        return "子任务"
    else:
        return prompt[:60] if prompt else tool_name or "操作"


def compress(raw: dict) -> dict:
    """将原始观察压缩为结构化数据（纯规则，0 LLM token）"""
    hook = raw.get("hookType", "")
    tool = raw.get("toolName", "")
    inp = json.dumps(raw.get("toolInput", ""), ensure_ascii=False) if isinstance(raw.get("toolInput"), (dict, list)) else str(raw.get("toolInput", ""))
    out = str(raw.get("toolOutput", ""))
    prompt = str(raw.get("userPrompt", ""))

    obs_type = derive_type(hook, tool, inp, out, prompt)
    title = derive_title(obs_type, tool, inp, prompt)
    concepts = extract_concepts(inp, out, prompt)
    files = extract_file_paths(inp, out)
    importance = score_importance(obs_type, out)
    narrative = summarize_narrative(out, obs_type)
    facts = extract_facts(out, obs_type)

    return {
        "type": obs_type,
        "title": title,
        "narrative": narrative,
        "concepts": concepts,
        "files": files,
        "importance": importance,
        "facts": facts,
        "source": "compress.py",
        "compressedAt": datetime.now(timezone.utc).isoformat(),
    }


def quality_gate(compressed: dict) -> bool:
    """检查压缩结果质量。返回 False 表示应拒绝写入 Qdrant。"""
    title = compressed.get("title", "")
    narrative = compressed.get("narrative", "")
    # 空壳标记：旧 parser 产出的垃圾
    if title == "操作" or len(title.strip()) < 5:
        return False
    # 内容太短，无意义
    if len(narrative.strip()) < 10:
        return False
    return True


def process_queue():
    """处理观察队列中的文件"""
    queue_file = Path.home() / ".openclaw" / "observe_queue.jsonl"
    if not queue_file.exists():
        return []

    results = []
    processed = []
    with open(queue_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
                compressed = compress(raw)
                results.append(compressed)
                processed.append(raw)
            except json.JSONDecodeError:
                continue

    # 清空队列并备份
    if processed:
        backup = queue_file.with_suffix(".bak")
        queue_file.replace(backup)
        # 重建空队列
        queue_file.write_text("", encoding="utf-8")

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="输入的 JSON 文件路径")
    parser.add_argument("--output", help="输出的 JSON 文件路径（ut）")
    parser.add_argument("--process-queue", action="store_true", help="处理观察队列")
    opts = parser.parse_args()

    results = []

    if opts.process_queue:
        results = process_queue()
        print(f"处理了 {len(results)} 条观察")

    elif opts.input:
        with open(opts.input, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        if isinstance(data, list):
            results = [compress(item) for item in data]
        else:
            results = [compress(data)]

        print(f"压缩了 {len(results)} 条观察")

    else:
        # 从 stdin 读取（兼容 GBK 环境，优先用 utf-8）
        try:
            input_str = sys.stdin.buffer.read().decode('utf-8')
        except Exception:
            input_str = sys.stdin.read()
        if input_str.strip():
            data = json.loads(input_str)
            if isinstance(data, list):
                results = [compress(item) for item in data]
            else:
                results = [compress(data)]

    if opts.output:
        with open(opts.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    elif results:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
