#!/usr/bin/env python3
"""
AutoDream Cycle - 自动记忆整理主脚本

实现四阶段流程：
1. Orientation: 读取当前记忆目录，建立记忆状态地图
2. Gather Signal: 窄搜索会话记录，提取高价值信号
3. Consolidation: 合并、去重、删除过时条目
4. Prune and Index: 更新 MEMORY.md 索引，保持≤200 行

用法:
    python3 autodream_cycle.py --workspace .
    python3 autodream_cycle.py --workspace . --force  # 强制运行，忽略触发条件
"""

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ============== 工具函数 ==============

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def now_ts() -> float:
    return datetime.now(timezone.utc).timestamp()


def normalize(text: str) -> str:
    """标准化文本：去除多余空白"""
    return re.sub(r"\s+", " ", str(text or "").strip())


def canonical(text: str) -> str:
    """规范化文本：用于去重比较"""
    s = normalize(text).lower()
    s = re.sub(r"[^a-z0-9\s:_-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def stable_id(text: str) -> str:
    """生成稳定的条目 ID"""
    return "ad_" + hashlib.sha256(canonical(text).encode("utf-8")).hexdigest()[:16]


def parse_relative_dates(text: str, reference_date: datetime) -> str:
    """
    将相对日期转换为绝对日期
    
    示例:
    - "昨天我们决定使用 Redis" → "2026-04-01 我们决定使用 Redis"
    - "上周修复了这个 bug" → "2026-03-26 修复了这个 bug"
    """
    today = reference_date.date()
    
    # 常见相对日期模式
    patterns = [
        (r'\b昨天\b', (today - timedelta(days=1)).isoformat()),
        (r'\b前天\b', (today - timedelta(days=2)).isoformat()),
        (r'\b今天\b', today.isoformat()),
        (r'\b明天\b', (today + timedelta(days=1)).isoformat()),
        (r'\b上周\b', (today - timedelta(days=7)).isoformat()),
        (r'\b本周\b', today.isoformat()),
        (r'\b下周\b', (today + timedelta(days=7)).isoformat()),
        (r'\b上个月\b', (today.replace(day=1) - timedelta(days=1)).strftime('%Y-%m')),
        (r'\b这个月\b', today.strftime('%Y-%m')),
        (r'\b前几天\b', (today - timedelta(days=3)).isoformat()),
        (r'\b最近\b', (today - timedelta(days=7)).isoformat()),
    ]
    
    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result


def detect_contradiction(entry1: Dict, entry2: Dict) -> bool:
    """
    检测两个条目是否矛盾
    
    矛盾场景：
    - 同一主题但决策相反（如"使用 Redis" vs "使用 Memcached"）
    - 同一文件但状态不同（如"文件存在" vs "文件已删除"）
    """
    text1 = canonical(entry1.get("text", ""))
    text2 = canonical(entry2.get("text", ""))
    
    # 对立词检测
    opposites = [
        ("使用", "弃用"),
        ("启用", "禁用"),
        ("开始", "停止"),
        ("添加", "删除"),
        ("创建", "销毁"),
        ("prefer", "avoid"),
        ("use", "remove"),
    ]
    
    for word1, word2 in opposites:
        if word1 in text1 and word2 in text2:
            return True
        if word2 in text1 and word1 in text2:
            return True
    
    return False


def is_stale(entry: Dict, workspace: Path) -> bool:
    """
    检测条目是否过时
    
    过时场景：
    - 引用已删除的文件
    - 包含过时的技术栈（被后续决策覆盖）
    """
    text = entry.get("text", "")
    
    # 检查是否引用不存在的文件
    file_pattern = r'[/\w.-]+\.(py|js|ts|md|json|yaml|yml|toml)'
    matches = re.findall(file_pattern, text)
    for file_path in matches:
        if file_path.startswith('/'):
            full_path = Path(file_path)
        else:
            full_path = workspace / file_path
        if not full_path.exists():
            # 文件不存在，可能是过时条目
            if any(kw in text.lower() for kw in ["存在", "exists", "位于", "located"]):
                return True
    
    return False


# ============== 阶段 1: Orientation ==============

def phase1_orientation(workspace: Path) -> Dict:
    """
    阶段 1: 读取当前记忆目录，建立记忆状态地图
    
    返回:
    {
        "memory_files": [...],
        "total_entries": int,
        "memory_md_lines": int,
        "topics": [...]
    }
    """
    print("📍 阶段 1: Orientation - 建立记忆状态地图")
    
    result = {
        "memory_files": [],
        "total_entries": 0,
        "memory_md_lines": 0,
        "topics": [],
        "timestamp": now_iso()
    }
    
    # 检查 MEMORY.md
    memory_md = workspace / "MEMORY.md"
    if memory_md.exists():
        content = memory_md.read_text(encoding="utf-8")
        result["memory_md_lines"] = len(content.splitlines())
        result["memory_files"].append(str(memory_md))
    
    # 检查 memory/ 目录
    memory_dir = workspace / "memory"
    if memory_dir.exists():
        # 日常记忆文件
        for f in sorted(memory_dir.glob("20*.md")):
            result["memory_files"].append(str(f))
            entries = extract_entries_from_file(f)
            result["total_entries"] += len(entries)
        
        # 主题记忆文件
        topics_dir = memory_dir / "topics"
        if topics_dir.exists():
            for f in topics_dir.glob("*.md"):
                result["memory_files"].append(str(f))
                result["topics"].append(f.stem)
                entries = extract_entries_from_file(f)
                result["total_entries"] += len(entries)
        
        # 共享记忆文件
        shared_dir = memory_dir / "shared"
        if shared_dir.exists():
            for f in shared_dir.glob("*.md"):
                result["memory_files"].append(str(f))
                entries = extract_entries_from_file(f)
                result["total_entries"] += len(entries)
    
    print(f"   找到 {len(result['memory_files'])} 个记忆文件，共 {result['total_entries']} 个条目")
    return result


def extract_entries_from_file(path: Path) -> List[Dict]:
    """从 Markdown 文件提取记忆条目"""
    entries = []
    in_code = False
    
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"   ⚠️ 无法读取 {path}: {e}")
        return entries
    
    for idx, raw in enumerate(content.splitlines(), start=1):
        line = raw.strip()
        
        # 跳过代码块
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        
        # 跳过标题和空行
        if not line or line.startswith("#"):
            continue
        
        # 提取列表项
        text = None
        if line.startswith(("- ", "* ")):
            text = line[2:].strip()
        elif re.match(r"^\d+\.\s+", line):
            text = re.sub(r"^\d+\.\s+", "", line).strip()
        elif ":" in line and len(line) <= 320:
            head = line.split(":", 1)[0].strip().lower()
            if head in {"rule", "lesson", "insight", "policy", "decision", "note", "action"}:
                text = line
        
        if text and len(text) >= 24:
            entries.append({
                "id": stable_id(text),
                "text": text,
                "source_file": str(path),
                "source_line": idx,
            })
    
    return entries


# ============== 阶段 2: Gather Signal ==============

def phase2_gather_signal(workspace: Path, orientation: Dict) -> Dict:
    """
    阶段 2: 窄搜索会话记录，提取高价值信号
    
    搜索模式：
    - 用户纠正："不对"、"错了"、"应该是"
    - 明确保存："记住这个"、"保存到记忆"
    - 重要决策："决定使用"、"选择"
    - 重复主题：跨多个会话出现的模式
    """
    print("📡 阶段 2: Gather Signal - 提取高价值信号")
    
    result = {
        "signals": [],
        "user_corrections": [],
        "explicit_saves": [],
        "decisions": [],
        "recurring_themes": [],
        "timestamp": now_iso()
    }
    
    # 搜索会话记录（JSONL 文件）
    sessions_dir = workspace / "sessions"
    if not sessions_dir.exists():
        print("   ⚠️ 未找到 sessions 目录，跳过会话分析")
        return result
    
    signals = []
    
    # 窄搜索模式
    patterns = {
        "user_corrections": [r"不对", r"错了", r"应该是", r"不是.*是", r"correct", r"actually"],
        "explicit_saves": [r"记住", r"保存.*记忆", r"remember", r"save.*memory"],
        "decisions": [r"决定.*使用", r"选择", r"decided to", r"opt for"],
    }
    
    for jsonl_file in sessions_dir.glob("*.jsonl"):
        try:
            content = jsonl_file.read_text(encoding="utf-8", errors="ignore")
            for line in content.splitlines():
                if not line.strip():
                    continue
                try:
                    session = json.loads(line)
                    messages = session.get("messages", [])
                    for msg in messages:
                        role = msg.get("role", "")
                        text = msg.get("content", "")
                        
                        # 检测信号
                        for signal_type, pattern_list in patterns.items():
                            for pattern in pattern_list:
                                if re.search(pattern, text, re.IGNORECASE):
                                    signals.append({
                                        "type": signal_type,
                                        "text": text[:200],
                                        "source": str(jsonl_file),
                                        "role": role,
                                    })
                                    result[signal_type].append({
                                        "text": text[:200],
                                        "source": str(jsonl_file),
                                    })
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            print(f"   ⚠️ 读取 {jsonl_file} 失败：{e}")
    
    # 去重
    seen = set()
    unique_signals = []
    for s in signals:
        key = canonical(s["text"])
        if key not in seen:
            seen.add(key)
            unique_signals.append(s)
    
    result["signals"] = unique_signals
    print(f"   提取 {len(unique_signals)} 个高价值信号")
    return result


# ============== 阶段 3: Consolidation ==============

def phase3_consolidation(workspace: Path, orientation: Dict, signals: Dict) -> Dict:
    """
    阶段 3: 合并、去重、删除过时条目
    
    操作：
    - 转换相对日期为绝对日期
    - 删除矛盾条目（保留最新的）
    - 删除过时条目（引用已删除文件）
    - 合并重复条目
    """
    print("🔄 阶段 3: Consolidation - 合并整理")
    
    result = {
        "original_count": 0,
        "final_count": 0,
        "pruned": [],
        "merged": [],
        "updated": [],
        "timestamp": now_iso()
    }
    
    # 收集所有条目
    all_entries = []
    memory_dir = workspace / "memory"
    
    if memory_dir.exists():
        for md_file in memory_dir.glob("*.md"):
            entries = extract_entries_from_file(md_file)
            all_entries.extend(entries)
        
        topics_dir = memory_dir / "topics"
        if topics_dir.exists():
            for md_file in topics_dir.glob("*.md"):
                entries = extract_entries_from_file(md_file)
                all_entries.extend(entries)
    
    result["original_count"] = len(all_entries)
    print(f"   原始条目数：{len(all_entries)}")
    
    # 去重和整理
    seen = {}
    pruned = []
    merged = []
    updated = []
    
    today = datetime.now(timezone.utc)
    
    for entry in all_entries:
        text = entry["text"]
        key = canonical(text)
        
        # 转换相对日期
        updated_text = parse_relative_dates(text, today)
        if updated_text != text:
            entry["text"] = updated_text
            updated.append({
                "original": text[:100],
                "updated": updated_text[:100],
            })
        
        # 检查是否过时
        if is_stale(entry, workspace):
            pruned.append(entry)
            continue
        
        # 检查重复
        if key in seen:
            # 合并重复条目（保留更详细的）
            existing = seen[key]
            if len(text) > len(existing["text"]):
                seen[key] = entry
            merged.append({
                "kept": seen[key]["text"][:100],
                "discarded": text[:100],
            })
            continue
        
        # 检查矛盾（简化版：只检测明显矛盾）
        is_contradictory = False
        for existing_key, existing_entry in seen.items():
            if detect_contradiction(entry, existing_entry):
                # 保留新的，删除旧的
                pruned.append(existing_entry)
                del seen[existing_key]
                is_contradictory = True
                break
        
        if not is_contradictory:
            seen[key] = entry
    
    result["pruned"] = pruned
    result["merged"] = merged
    result["updated"] = updated
    result["final_count"] = len(seen)
    
    print(f"   整理后：{len(seen)} 个条目")
    print(f"   - 删除过时：{len(pruned)}")
    print(f"   - 合并重复：{len(merged)}")
    print(f"   - 更新日期：{len(updated)}")
    
    # 保存整理后的条目
    return {
        **result,
        "entries": list(seen.values()),
    }


# ============== 阶段 4: Prune and Index ==============

def phase4_prune_and_index(workspace: Path, consolidation: Dict) -> Dict:
    """
    阶段 4: 更新 MEMORY.md 索引，保持≤200 行
    
    操作：
    - 删除不存在的主题文件引用
    - 添加新主题文件链接
    - 解决索引与实际内容的矛盾
    - 按相关性和时间排序
    """
    print("📇 阶段 4: Prune and Index - 更新索引")
    
    result = {
        "memory_md_lines_before": 0,
        "memory_md_lines_after": 0,
        "topics_added": [],
        "topics_removed": [],
        "timestamp": now_iso()
    }
    
    memory_md = workspace / "MEMORY.md"
    entries = consolidation.get("entries", [])
    
    # 读取现有 MEMORY.md
    if memory_md.exists():
        content = memory_md.read_text(encoding="utf-8")
        result["memory_md_lines_before"] = len(content.splitlines())
    
    # 生成新的 MEMORY.md
    lines = [
        "# MEMORY.md - 长期记忆索引",
        "",
        f"- 最后整理：{consolidation.get('timestamp', now_iso())}",
        f"- 条目总数：{consolidation.get('final_count', 0)}",
        "",
        "## 记忆条目",
        "",
    ]
    
    # 添加整理后的条目（限制 200 行）
    max_lines = 200
    current_lines = len(lines)
    
    for entry in entries[:max_lines - current_lines - 10]:  # 留余量
        text = entry.get("text", "")
        if len(text) > 120:
            text = text[:117] + "..."
        lines.append(f"- {text}")
    
    lines += [
        "",
        "## 元信息",
        "",
        f"- 整理时间：{consolidation.get('timestamp', now_iso())}",
        f"- 删除条目：{consolidation.get('pruned', []) and len(consolidation['pruned'])}",
        f"- 合并条目：{consolidation.get('merged', []) and len(consolidation['merged'])}",
        "",
        "*此文件由 AutoDream 自动整理*",
    ]
    
    # 写入 MEMORY.md
    memory_md.parent.mkdir(parents=True, exist_ok=True)
    memory_md.write_text("\n".join(lines), encoding="utf-8")
    
    result["memory_md_lines_after"] = len(lines)
    print(f"   MEMORY.md: {result['memory_md_lines_before']} → {result['memory_md_lines_after']} 行")
    
    return result


# ============== 状态管理 ==============

def load_state(workspace: Path) -> Dict:
    """加载 AutoDream 状态"""
    state_file = workspace / "memory" / "autodream" / "state.json"
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except:
        return {
            "last_run": None,
            "last_run_ts": 0,
            "session_count_since_last": 0,
        }


def save_state(workspace: Path, state: Dict):
    """保存 AutoDream 状态"""
    state_file = workspace / "memory" / "autodream" / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def count_sessions_since(workspace: Path, since_ts: float) -> int:
    """计算自指定时间以来的会话数"""
    sessions_dir = workspace / "sessions"
    if not sessions_dir.exists():
        return 0
    
    count = 0
    for f in sessions_dir.glob("*.json"):
        try:
            mtime = f.stat().st_mtime
            if mtime > since_ts:
                count += 1
        except:
            continue
    
    return count


def should_trigger(state: Dict, workspace: Path, config: Dict) -> Tuple[bool, str]:
    """
    判断是否应该触发 AutoDream
    
    触发条件：
    - 距上次运行 ≥ 24 小时 且
    - 自上次运行后 ≥ 5 次会话
    """
    if not state.get("last_run_ts"):
        return True, "首次运行"
    
    last_run_ts = state["last_run_ts"]
    now = datetime.now(timezone.utc).timestamp()
    
    hours_since = (now - last_run_ts) / 3600
    sessions_since = count_sessions_since(workspace, last_run_ts)
    
    interval_hours = config.get("interval_hours", 24)
    min_sessions = config.get("min_sessions", 5)
    
    if hours_since >= interval_hours and sessions_since >= min_sessions:
        return True, f"距上次运行 {hours_since:.1f} 小时，{sessions_since} 次会话"
    
    if hours_since < interval_hours:
        return False, f"间隔不足 {interval_hours} 小时（当前 {hours_since:.1f} 小时）"
    
    return False, f"会话数不足 {min_sessions} 次（当前 {sessions_since} 次）"


# ============== 主流程 ==============

def write_report(workspace: Path, consolidation: Dict, orientation: Dict, prune_result: Dict) -> str:
    """生成整理报告"""
    report_path = workspace / "memory" / "autodream" / "cycle_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    report = f"""# AutoDream 整理报告

**整理时间**: {consolidation.get('timestamp', now_iso())}

## 概览

| 指标 | 数值 |
|------|------|
| 原始条目数 | {consolidation.get('original_count', 0)} |
| 整理后条目数 | {consolidation.get('final_count', 0)} |
| 删除过时 | {len(consolidation.get('pruned', []))} |
| 合并重复 | {len(consolidation.get('merged', []))} |
| 更新日期 | {len(consolidation.get('updated', []))} |

## MEMORY.md 变化

- 整理前：{prune_result.get('memory_md_lines_before', 0)} 行
- 整理后：{prune_result.get('memory_md_lines_after', 0)} 行

## 被删除的条目（样本）

"""
    
    for entry in consolidation.get('pruned', [])[:10]:
        report += f"- {entry.get('text', 'N/A')[:100]}\n"
    
    if not consolidation.get('pruned'):
        report += "- （无）\n"
    
    report += "\n## 被合并的条目（样本）\n\n"
    
    for item in consolidation.get('merged', [])[:10]:
        report += f"- 保留：{item.get('kept', 'N/A')[:80]}\n"
    
    if not consolidation.get('merged'):
        report += "- （无）\n"
    
    report_path.write_text(report, encoding="utf-8")
    return str(report_path)


def main():
    parser = argparse.ArgumentParser(description="AutoDream - 自动记忆整理")
    parser.add_argument("--workspace", default=".", help="OpenClaw 工作区根目录")
    parser.add_argument("--force", action="store_true", help="强制运行，忽略触发条件")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不写入文件")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    args = parser.parse_args()
    
    workspace = Path(args.workspace).expanduser().resolve()
    config_path = workspace / "skills" / "autodream" / "config" / "config.json"
    
    # 加载配置
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except:
        config = {
            "interval_hours": 24,
            "min_sessions": 5,
            "max_memory_lines": 200,
        }
    
    # 加载状态
    state = load_state(workspace)
    
    # 检查是否应该触发
    if not args.force:
        should_run, reason = should_trigger(state, workspace, config)
        if not should_run:
            print(f"⏸️  暂不运行：{reason}")
            print(f"   使用 --force 强制运行")
            return
    
    print(f"🚀 AutoDream 整理开始")
    print(f"   工作区：{workspace}")
    
    # 阶段 1: Orientation
    orientation = phase1_orientation(workspace)
    
    # 阶段 2: Gather Signal
    signals = phase2_gather_signal(workspace, orientation)
    
    # 阶段 3: Consolidation
    consolidation = phase3_consolidation(workspace, orientation, signals)
    
    # 阶段 4: Prune and Index
    prune_result = phase4_prune_and_index(workspace, consolidation)
    
    # 生成报告
    if not args.dry_run:
        report_path = write_report(workspace, consolidation, orientation, prune_result)
        
        # 保存整理后的条目
        entries_file = workspace / "memory" / "autodream" / "consolidated_entries.json"
        entries_file.parent.mkdir(parents=True, exist_ok=True)
        entries_file.write_text(json.dumps({
            "schema": "autodream-consolidated-v1",
            "timestamp": consolidation.get("timestamp"),
            "entries": consolidation.get("entries", []),
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 保存被删除的条目
        pruned_file = workspace / "memory" / "autodream" / "pruned_entries.json"
        pruned_file.write_text(json.dumps(consolidation.get("pruned", []), indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 保存被合并的条目
        merged_file = workspace / "memory" / "autodream" / "merged_entries.json"
        merged_file.write_text(json.dumps(consolidation.get("merged", []), indent=2, ensure_ascii=False), encoding="utf-8")
        
        # 更新状态
        state["last_run"] = now_iso()
        state["last_run_ts"] = datetime.now(timezone.utc).timestamp()
        state["session_count_since_last"] = 0
        save_state(workspace, state)
        
        print(f"📄 报告：{report_path}")
    
    print(f"✅ AutoDream 整理完成")
    
    # 返回 JSON 结果（供 OpenClaw 解析）
    result = {
        "ok": True,
        "orientation": orientation,
        "consolidation": {
            "original_count": consolidation.get("original_count", 0),
            "final_count": consolidation.get("final_count", 0),
            "pruned_count": len(consolidation.get("pruned", [])),
            "merged_count": len(consolidation.get("merged", [])),
            "updated_count": len(consolidation.get("updated", [])),
        },
        "prune_result": prune_result,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
