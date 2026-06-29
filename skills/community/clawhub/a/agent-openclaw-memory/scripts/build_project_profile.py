"""
build_project_profile.py — 项目 Profile 构建
由 vault_to_qdrant.py 在同步后自动触发，或由 heartbeat 定期执行。

从 Qdrant knowledge_base 聚合出项目 Profile，写入 vault 00-索引/。

用法: python scripts/build_project_profile.py
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

from qdrant_utils import QDRANT_URL, KB_COLLECTION, scroll_all as _qdrant_scroll, is_available as _qdrant_ok

# Vault 配置
from shared_config import VAULT_DIR
PROFILE_FILE = VAULT_DIR / "00-索引" / "project_profile.json"


def fetch_qdrant_points(limit: int = 3000) -> list:
    """从 Qdrant scroll 所有点"""
    import requests
    points = []
    offset = None

    while len(points) < limit:
        payload = {
            "limit": min(500, limit - len(points)),
            "with_payload": True,
            "with_vector": False,
        }
        if offset:
            payload["offset"] = offset

        resp = requests.post(
            f"{QDRANT_URL}/collections/{KB_COLLECTION}/points/scroll",
            json=payload,
            timeout=30,
        )
        if resp.status_code != 200:
            break

        data = resp.json().get("result", {})
        batch = data.get("points", [])
        points.extend(batch)
        offset = data.get("next_page_offset")

        if not batch or offset is None:
            break

    return points


def build_profile() -> dict:
    """从 Qdrant 聚合项目 Profile"""
    points = fetch_qdrant_points()
    if not points:
        print("Qdrant 中没有数据")
        return {}

    concept_counter = Counter()
    file_counter = Counter()
    conventions = set()
    common_errors = set()
    latest_count = 0
    total_obs = 0

    for p in points:
        payload = p.get("payload", {})

        # 只统计最新版本
        if payload.get("is_latest", True) is False:
            continue
        latest_count += 1

        # 统计概念
        concepts = payload.get("concepts", [])
        if isinstance(concepts, list):
            for c in concepts:
                if isinstance(c, str) and len(c) > 1:
                    concept_counter[c.lower()] += 1

        # 统计文件
        files = payload.get("files", [])
        if isinstance(files, list):
            for f in files:
                if isinstance(f, str):
                    file_counter[f] += 1

        # 提取约定（type=convention 或 title 含"约定"）
        title = (payload.get("title", "") or "")
        content = (payload.get("content", "") or "")
        obs_type = payload.get("type", "")
        if "约定" in title or obs_type == "convention":
            conventions.add(title[:100])
        if "common_errors" in payload:
            errs = payload["common_errors"]
            if isinstance(errs, list):
                for e in errs:
                    common_errors.add(str(e)[:100])

        # 统计观察数
        if payload.get("source") == "compress.py":
            total_obs += 1

        # 从 narrative/content 提取错误模式
        if "error" in content.lower() or "错误" in content:
            # 提取错误摘要
            lines = content.strip().split("\n")
            for line in lines[:3]:
                if "error" in line.lower() or "错误" in line:
                    common_errors.add(line.strip()[:100])

    profile = {
        "updatedAt": datetime.now().astimezone().isoformat(),
        "topConcepts": [
            {"concept": c, "frequency": n}
            for c, n in concept_counter.most_common(30)
        ],
        "topFiles": [
            {"file": f, "frequency": n}
            for f, n in file_counter.most_common(20)
        ],
        "conventions": sorted(conventions)[:20],
        "commonErrors": sorted(common_errors)[:10],
        "latestPointCount": latest_count,
        "totalObservationCount": total_obs,
    }

    return profile


def load_profile() -> dict:
    """读取缓存的 Profile"""
    if PROFILE_FILE.exists():
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def format_profile_for_injection(profile: dict, max_lines: int = 15) -> str:
    """格式化为可注入的文本"""
    if not profile:
        return ""

    lines = ["## 项目概况"]
    tokens = 0

    if profile.get("topConcepts"):
        top = [c["concept"] for c in profile["topConcepts"][:8]]
        line = f"核心概念: {', '.join(top)}"
        lines.append(line)
        tokens += len(line)

    if profile.get("topFiles"):
        top = [f["file"] for f in profile["topFiles"][:5]]
        line = f"关键文件: {', '.join(top)}"
        lines.append(line)
        tokens += len(line)

    if profile.get("conventions"):
        convs = profile["conventions"][:3]
        line = f"项目约定: {'; '.join(convs)}"
        lines.append(line)
        tokens += len(line)

    if profile.get("commonErrors"):
        errs = profile["commonErrors"][:3]
        line = f"常见错误: {'; '.join(errs)}"
        lines.append(line)
        tokens += len(line)

    line = f"知识条目: {profile.get('latestPointCount', 0)}"
    lines.append(line)

    return "\n".join(lines)


def main():
    print("构建项目 Profile...")

    # 尝试连接 Qdrant
    try:
        import requests
        resp = requests.get(f"{QDRANT_URL}/collections/{KB_COLLECTION}", timeout=5)
        if resp.status_code != 200:
            print(f"Qdrant 集合 {KB_COLLECTION} 不存在，跳过")
            return
    except requests.exceptions.ConnectionError:
        print("Qdrant 不可用，跳过")
        return
    except ImportError:
        print("requests 未安装，跳过")
        return

    profile = build_profile()
    if not profile:
        print("Profile 为空，跳过")
        return

    # 确保目标目录存在
    PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(f"Profile 已写入: {PROFILE_FILE}")
    print(f"  核心概念: {len(profile['topConcepts'])} 个")
    print(f"  关键文件: {len(profile['topFiles'])} 个")
    print(f"  项目约定: {len(profile['conventions'])} 条")
    print(f"  常见错误: {len(profile['commonErrors'])} 条")

    # 打印注入格式样例
    print("\n--- 注入格式样例 ---")
    print(format_profile_for_injection(profile))

# ── Health report ──
try:
    from system_health import task_report
    task_report("build_project_profile", status="ok")
except Exception:
    pass


if __name__ == "__main__":
    main()
