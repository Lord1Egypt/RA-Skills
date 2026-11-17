#!/usr/bin/env python3
"""共享加载器：从 references/file-contract.json 读取文件契约（单一来源）。

validate_book / snapshot_book / rollback_book / init_book / build_dashboard
通过本模块获取 canonical 路径、别名、必需/推荐文件、快照清单与排除规则，
避免各脚本各自硬编码副本导致漂移。文档、脚本、仪表盘共用这一份。
"""

import glob
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from typing import Dict, List, Tuple

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRACT_PATH = os.path.join(SKILL_ROOT, "references", "file-contract.json")
META_PATH = os.path.join(SKILL_ROOT, "_meta.json")

_contract_cache: Dict = None


def load_contract() -> dict:
    """加载并缓存 file-contract.json。"""
    global _contract_cache
    if _contract_cache is None:
        with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
            _contract_cache = json.load(f)
    return _contract_cache


def skill_version() -> str:
    """读取 _meta.json 中的 skill 版本号（用于 book.json / 快照 manifest 的 skillVersion）。"""
    try:
        with open(META_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("version", "")
    except (OSError, json.JSONDecodeError):
        return ""


def aliases() -> Dict[str, List[str]]:
    """canonical path -> [alias paths]。"""
    return load_contract().get("aliases", {})


def required_files() -> List[str]:
    """必需文件（缺失报错）。"""
    return load_contract().get("requiredFiles", [])


def recommended_files() -> List[str]:
    """推荐文件（缺失告警，不报错）。"""
    return load_contract().get("recommendedFiles", [])


def snapshot_files() -> List[str]:
    """快照必须包含的文件（书根相对路径，snapshot_book / rollback_book 共用）。"""
    return load_contract().get("snapshotFiles", {}).get("paths", [])


def resolve_snapshot_files(book_dir: str) -> List[str]:
    """将快照清单展开为书根相对的实际文件路径。

    非通配 pattern 原样返回（存在性由调用方检查并报告缺失）；
    通配 pattern（story/roles/** 等）用 glob 递归展开为存在的文件清单。
    快照写入（snapshot_book）与回滚读取（rollback_book）共用本函数，
    保证两者路径集一致。
    """
    result: List[str] = []
    for pat in snapshot_files():
        if any(ch in pat for ch in "*?["):
            base = os.path.join(book_dir, pat)
            for m in sorted(glob.glob(base, recursive=True)):
                if os.path.isfile(m):
                    rel = os.path.relpath(m, book_dir).replace(os.sep, "/")
                    if rel not in result:
                        result.append(rel)
        else:
            if pat not in result:
                result.append(pat)
    return result


def excluded_patterns() -> List[str]:
    """排除路径正则模式（快照 / 备份 / rewrite 候选等不作为权威数据）。"""
    return load_contract().get("excludedPaths", {}).get("patterns", [])


def character_legacy_files() -> dict:
    """旧版单文件多角色格式说明（不支持，提示用户迁移）。"""
    return load_contract().get("characterLegacyFiles", {})


def is_excluded_path(rel_path: str) -> bool:
    """判断相对书根的路径是否落在排除目录。"""
    p = rel_path.replace("\\", "/")
    return any(re.match(pat, p) for pat in excluded_patterns())


def file_exists_with_alias(book_dir: str, path: str) -> Tuple[bool, str]:
    """检查文件是否存在（含别名回退），返回 (是否存在, 实际路径)。"""
    if os.path.isfile(os.path.join(book_dir, path)):
        return True, path
    for alias in aliases().get(path, []):
        if os.path.isfile(os.path.join(book_dir, alias)):
            return True, alias
    return False, path


def read_file(book_dir: str, path: str) -> str:
    """读取文件（含别名回退），不存在返回空串。"""
    exists, actual = file_exists_with_alias(book_dir, path)
    if not exists:
        return ""
    with open(os.path.join(book_dir, actual), "r", encoding="utf-8") as f:
        return f.read()


# ---- 共享 IO / 时间 / 哈希 helper（snapshot_book / rollback_book / validate_book 共用）----

def now_iso() -> str:
    """当前 UTC 时间 ISO 8601 字符串。"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_join(base: str, *paths: str) -> str:
    """安全拼接路径，防止目录遍历，确保结果位于 base 之内。"""
    target = os.path.normpath(os.path.join(base, *paths))
    if not target.startswith(os.path.normpath(base) + os.sep) and target != os.path.normpath(base):
        raise ValueError(f"路径越界：{paths}")
    return target


def next_snapshot_dir(book_dir: str) -> str:
    """返回下一个快照目录编号（四位补零字符串），确保 snapshots 目录存在。"""
    snapshots_dir = os.path.join(book_dir, "story", "snapshots")
    os.makedirs(snapshots_dir, exist_ok=True)
    existing = []
    for name in os.listdir(snapshots_dir):
        if os.path.isdir(os.path.join(snapshots_dir, name)):
            try:
                existing.append(int(name))
            except ValueError:
                pass
    next_num = (max(existing) + 1) if existing else 0
    return f"{next_num:04d}"


def file_sha256(path: str) -> str:
    """计算文件 SHA-256，返回 'sha256:<hex>'（全仓统一格式）。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def count_words(text: str) -> int:
    """章节 index 的 wordCount 统计（与 rebuild_index 共用，避免两处算法漂移）。

    统计规则：连续的中文字符 / 英文字母数字串各计为一个"段"（非标点连续段）。
    用于 index 的 wordCount 与 index-正文一致性核对（两者同尺度）。
    """
    return len(re.findall(r"[一-鿿A-Za-z0-9]+", text))


def count_characters(text: str) -> int:
    """章节"字数"统计（去空白字符数）——与 book.json 的 chapterWordCount 目标同尺度。

    chapterWordCount 是作者按"字符"设定的单章目标，而 count_words 统计的是
    非标点连续段数（尺度不同），两者不可直接比较。对目标偏差用本函数。
    """
    return len(re.sub(r"\s", "", text))
