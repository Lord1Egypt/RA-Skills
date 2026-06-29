#!/usr/bin/env python3
"""
process_inbox.py — 收件箱自动分类归档

流程：
  1. 文件名关键词匹配（确定性的，100% 正确）
  2. LLM 兜底 — 走 Gateway 本地 API（文件名不明确的）
  3. 搬完后自动触发 sync 同步到向量库

用法: python scripts/process_inbox.py
      python scripts/process_inbox.py --dry-run  只预览不执行
"""
import _suppress_windows

import os, sys, shutil, time, subprocess, json
from pathlib import Path
from datetime import datetime

from shared_config import VAULT_DIR as VAULT
INBOX = VAULT / "06-收件箱"

# 文件名关键词 → 目标目录映射（确定性规则，不改就不出错）
KEYWORD_RULES = [
    # 04-教训：用户偏好/纠正/决策/经验
    (["用户偏好", "用户纠正", "用户明确", "用户关注",
      "User correction", "User preference",
      "纠正：", "教训", "经验", "避坑",
      "有待解决",
      # 注意："决策" 可能匹配技术决策，所以放后面更精确的
      "决策：子会话", "Decision：",
      # 用户决策（非技术决策）
      "用户决策："],
     "04-教训"),

    # 02-知识：技术/配置/工具
    (["技术修复", "技术决策", "技术环境", "技术错误", "技术债务", "技术债",
      "Config", "配置：", "Search-", "Search:",
      "API", "教程", "工具",
      "学习", "论文", "知识点",
      "triton", "torch.compile", "ComfyUI",
      "DeepSeek", "会话成本", "成本策略"],
     "02-知识"),

    # 07-项目：项目/架构/方案
    (["项目", "架构", "方案", "设计", "赛狐", "Sellfox",
      "评估", "管线", "管道", "系统",
      "正在准备", "演示素材", "干活",
      "分析器", "analyzer"],
     "07-项目"),

    # 01-日记：日记/记录
    (["日记", "日志", "记录", "Heartbeat", "scheduled task"],
     "01-日记"),

    # 其他决策（放最后，更精确的决策关键词已在前面匹配后）
    (["决策："], "04-教训"),
]


def classify_by_filename(name):
    """文件名关键词匹配，命中即返回目标目录名。"""
    for keywords, target in KEYWORD_RULES:
        for kw in keywords:
            if kw in name:
                return target
    return None


def classify_by_llm_batch(items):
    """批量 LLM 分类 — N 个文件合并为 1 次 API 调用。
    
    items: list of (name, text)
    Returns: list of target_dir strings, parallel to items
    """
    if not items:
        return []
    
    from gateway_client import chat
    
    parts = []
    for i, (name, text) in enumerate(items):
        parts.append(
            f"File {i}: {name}\n"
            f"Content: {text[:300]}"
        )
    
    prompt = (
        "Classify each file below into one vault directory. "
        "Output exactly one word per file, one per line, in order:\n"
        "diary - daily records/events/conversation summaries\n"
        "knowledge - config/API/tutorials/tools/technical docs\n"
        "lessons - lessons learned/user preferences/decisions/error summaries\n"
        "projects - project docs/architecture/task records\n\n"
        + "\n\n".join(parts)
        + f"\n\nOutput {len(items)} words, one per line, in the same order:"
    )
    
    try:
        result = chat(
            messages=prompt,
            model="xiaomi/mimo-v2.5-pro",
            temperature=0,
            max_tokens=20 * len(items),
            timeout=30 + 5 * len(items),
        )
        if not result:
            return ["02-知识"] * len(items)
        
        mapping = {
            "diary": "01-日记", "knowledge": "02-知识",
            "lessons": "04-教训", "projects": "07-项目",
        }
        results = []
        for line in result["content"].strip().lower().split("\n"):
            line = line.strip()
            for key, val in mapping.items():
                if key in line:
                    results.append(val)
                    break
            else:
                results.append("02-知识")
        
        while len(results) < len(items):
            results.append("02-知识")
        return results[:len(items)]
    except Exception:
        return ["02-知识"] * len(items)


def process(dry_run=True):
    if not INBOX.exists():
        print("收件箱目录不存在")
        return

    files = sorted(INBOX.iterdir())
    if not files:
        print("收件箱为空")
        return

    print(f"收件箱: {len(files)} 个文件\n")

    stats = {"moved": 0, "llm": 0, "skipped": 0, "errors": 0}

    # 第一遍：收集需要 LLM 分类的文件
    keyword_targets = {}  # path → target
    llm_queue = []        # (path, name, text)
    for f in files:
        if not f.is_file() or f.suffix not in (".md", ".txt", ".json"):
            continue
        name = f.name
        target = classify_by_filename(name)
        if target:
            keyword_targets[f] = target
        else:
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except:
                text = ""
            llm_queue.append((f, name, text))
    
    # 批量 LLM 分类（1 次 API 调用）
    llm_results = {}
    if llm_queue:
        print(f"  → Batch classifying {len(llm_queue)} files via LLM (1 API call)...")
        items = [(name, text) for _, name, text in llm_queue]
        targets = classify_by_llm_batch(items)
        for (fp, name, _), target in zip(llm_queue, targets):
            llm_results[fp] = target
    
    # 第二遍：执行移动
    for f in files:
        if not f.is_file() or f.suffix not in (".md", ".txt", ".json"):
            continue
        name = f.name
        
        if f in keyword_targets:
            target = keyword_targets[f]
            source = "关键词"
        elif f in llm_results:
            target = llm_results[f]
            source = "LLM"
        else:
            continue

        # 目标目录
        dest_dir = VAULT / target
        dest_dir.mkdir(parents=True, exist_ok=True)

        # 检查目标是否已有同名文件
        dest_file = dest_dir / name
        if dest_file.exists():
            stamp = datetime.now().strftime("%H%M%S")
            dest_file = dest_dir / f"{stamp}-{name}"

        if dry_run:
            flag = "[DRY]" if source == "关键词" else "[LLM]"
            print(f"  {flag} {name[:50]:50s} → {target}")
            stats["moved"] += 1
            continue

        try:
            shutil.move(str(f), str(dest_file))
            print(f"  [{'✓' if source == '关键词' else 'L'}] {name[:50]:50s} → {target}")
            stats["moved"] += 1
            if source == "LLM":
                stats["llm"] += 1
        except Exception as e:
            print(f"  [✗] {name[:50]:50s} → 失败: {e}")
            stats["errors"] += 1

    print(f"\n结果: {stats['moved']} 移动 ({stats['llm']} LLM), "
          f"{stats['errors']} 失败, {stats['skipped']} 跳过")

    if not dry_run and stats["moved"] > 0:
        print("\n触发向量同步...")
        subprocess.run(["python", str(Path(__file__).parent / "vault_to_qdrant.py")],
                       capture_output=True, timeout=120)
        print("同步完成")

    return stats


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    process(dry_run=dry)


