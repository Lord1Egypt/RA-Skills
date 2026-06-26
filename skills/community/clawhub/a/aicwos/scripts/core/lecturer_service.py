"""
讲师服务

CRUD + 按需加载 + 加权合并 + Write-Through 双写。

架构原则：每次数据变更同时更新 DB 和文件系统，无需手动同步。
- DB：查询层（检索、对比、FTS5、向量）
- 文件系统：人类可读层（查看、导出、用户编辑）
- 两者始终一致

核心优化：
- 生成文案时只加载qualitative+persona_mapping+style_dimensions（~400 tokens）
- 管理时才加载完整profile
- 增量学习时按字段类型加权合并
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from scripts.core.db_manager import DatabaseManager
from scripts.core.text2vec_embedder import Text2VecEmbedder


class LecturerService:
    """讲师服务（Write-Through 双写）"""

    def __init__(self, db: DatabaseManager, data_dir: str = None):
        self.db = db
        self.data_dir = Path(data_dir) if data_dir else None
        self.embedder = Text2VecEmbedder.get_instance()

    # ── 写操作（DB + 文件系统双写） ──────────────────────────

    def add_lecturer(self, lecturer_id: str, profile: dict) -> dict:
        """添加/更新讲师画像（Write-Through: DB + profile.json）"""
        now = datetime.now().isoformat(timespec="seconds")
        qualitative = profile.get("qualitative", {})
        # 多路径查找：persona_mapping 可能在顶层或 qualitative 下
        persona = self._deep_get(profile, "persona_mapping", "qualitative.persona_mapping")
        style_dims = self._deep_get(
            profile,
            "style_dimensions",
            "qualitative.style_dimensions",
            "persona_mapping.style_dimensions",
            "qualitative.persona_mapping.style_dimensions",
        )
        sample_count = self._deep_get(profile, "sample_stats.total_samples", fallback=0)

        self.db.execute(
            "INSERT OR REPLACE INTO lecturers "
            "(lecturer_id, lecturer_name, profile_json, qualitative, persona_mapping, "
            "style_dimensions, sample_count, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                lecturer_id,
                profile.get("lecturer_name", lecturer_id),
                json.dumps(profile, ensure_ascii=False),
                json.dumps(qualitative, ensure_ascii=False),
                json.dumps(persona, ensure_ascii=False),
                json.dumps(style_dims, ensure_ascii=False),
                sample_count,
                now,
                now,
            ),
        )
        self.db.commit()

        # Write-Through: 同步写入文件系统
        self._write_profile_file(lecturer_id, profile)

        return {"status": "ok", "lecturer_id": lecturer_id}

    def delete_lecturer(self, lecturer_id: str) -> dict:
        """删除讲师（Write-Through: DB + 移入回收站）"""
        self.db.execute("DELETE FROM lecturer_samples WHERE lecturer_id=?", (lecturer_id,))
        self.db.execute("DELETE FROM lecturers WHERE lecturer_id=?", (lecturer_id,))
        self.db.commit()

        # Write-Through: 移入回收站
        self._move_to_trash(lecturer_id)

        return {"status": "deleted", "lecturer_id": lecturer_id}

    def add_sample(self, lecturer_id: str, sample_name: str, content: str,
                   is_reference: bool = False) -> dict:
        """添加样本（Write-Through: DB + 样本文件）"""
        now = datetime.now().isoformat(timespec="seconds")
        self.db.execute(
            "INSERT INTO lecturer_samples (lecturer_id, sample_name, content, is_reference, added_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (lecturer_id, sample_name, content, 1 if is_reference else 0, now),
        )
        self.db.commit()

        # Write-Through: 写样本文件
        self._write_sample_file(lecturer_id, sample_name, content)

        return {"status": "ok", "lecturer_id": lecturer_id, "sample_name": sample_name}

    # ── 读操作（仅 DB） ─────────────────────────────────────

    def get_profile(self, lecturer_id: str) -> Optional[dict]:
        """获取完整画像"""
        row = self.db.query_one(
            "SELECT profile_json FROM lecturers WHERE lecturer_id=?", (lecturer_id,)
        )
        if not row:
            return None
        return json.loads(row["profile_json"])

    def get_lite(self, lecturer_id: str) -> Optional[dict]:
        """
        获取轻量画像（文案生成用，~400 tokens）

        只返回：lecturer_name + qualitative + persona_mapping + style_dimensions + reference_scripts
        不返回：quantitative（占1500+ tokens但对文案生成无用）
        """
        row = self.db.query_one(
            "SELECT lecturer_name, qualitative, persona_mapping, style_dimensions, profile_json "
            "FROM lecturers WHERE lecturer_id=?",
            (lecturer_id,),
        )
        if not row:
            return None

        profile = json.loads(row["profile_json"]) if row["profile_json"] else {}
        return {
            "lecturer_id": lecturer_id,
            "lecturer_name": row["lecturer_name"],
            "qualitative": json.loads(row["qualitative"]) if row["qualitative"] else {},
            "persona_mapping": json.loads(row["persona_mapping"]) if row["persona_mapping"] else {},
            "style_dimensions": json.loads(row["style_dimensions"]) if row["style_dimensions"] else {},
            "reference_scripts": profile.get("reference_scripts", []),
            "sample_excerpts": profile.get("sample_excerpts", {}),
        }

    def get_quantitative(self, lecturer_id: str) -> Optional[dict]:
        """单独获取定量数据（增量合并时使用）"""
        profile = self.get_profile(lecturer_id)
        if not profile:
            return None
        return profile.get("quantitative", {})

    def update_profile(self, lecturer_id: str, profile: dict) -> dict:
        """更新完整画像（委托 add_lecturer，自动双写）"""
        return self.add_lecturer(lecturer_id, profile)

    def list_lecturers(self) -> list:
        """列出所有讲师摘要"""
        rows = self.db.query_all(
            "SELECT lecturer_id, lecturer_name, sample_count, "
            "style_dimensions, updated_at FROM lecturers"
        )
        results = []
        for row in rows:
            dims = json.loads(row["style_dimensions"]) if row["style_dimensions"] else {}
            results.append({
                "lecturer_id": row["lecturer_id"],
                "lecturer_name": row["lecturer_name"],
                "sample_count": row["sample_count"],
                "style_dimensions": dims,
                "updated_at": row["updated_at"],
            })
        return results

    def get_samples(self, lecturer_id: str, references_only: bool = False) -> list:
        """获取样本列表"""
        sql = "SELECT sample_name, content, is_reference FROM lecturer_samples WHERE lecturer_id=?"
        if references_only:
            sql += " AND is_reference=1"
        rows = self.db.query_all(sql, (lecturer_id,))
        return [dict(r) for r in rows]

    def get_reference_samples(self, lecturer_id: str) -> list:
        """获取参考示例（文案生成时使用）"""
        return self.get_samples(lecturer_id, references_only=True)

    def compare(self, id_a: str, id_b: str) -> Optional[dict]:
        """对比两个讲师风格"""
        a = self.get_lite(id_a)
        b = self.get_lite(id_b)
        if not a or not b:
            return None
        dims_a = a.get("style_dimensions", {})
        dims_b = b.get("style_dimensions", {})
        return {
            "lecturer_a": a,
            "lecturer_b": b,
            "dimension_diff": {
                k: {"a": dims_a.get(k, 0), "b": dims_b.get(k, 0),
                    "diff": dims_a.get(k, 0) - dims_b.get(k, 0)}
                for k in ["formality", "emotion", "pace", "interaction", "depth"]
            },
        }

    # ── 增量合并 ────────────────────────────────────────────

    def weighted_merge(self, lecturer_id: str, new_quantitative: dict,
                       new_sample_count: int) -> dict:
        """
        加权合并定量数据（内部调用 update_profile → add_lecturer，自动双写）

        旧权重 = 旧样本数 / (旧样本数 + 新样本数)
        新权重 = 新样本数 / (旧样本数 + 新样本数)
        首次学习时旧权重=0，直接使用新数据
        """
        profile = self.get_profile(lecturer_id)
        if not profile:
            return {"status": "not_found"}

        old_quant = profile.get("quantitative", {})
        old_count = profile.get("sample_stats", {}).get("total_samples", 0)
        total = old_count + new_sample_count
        old_w = old_count / total if total > 0 else 0
        new_w = new_sample_count / total if total > 0 else 1

        merged = self._merge_fields(old_quant, new_quantitative, old_w, new_w)

        # 更新画像
        profile["quantitative"] = merged
        if "sample_stats" not in profile:
            profile["sample_stats"] = {}
        profile["sample_stats"]["total_samples"] = total
        profile["updated_at"] = datetime.now().isoformat(timespec="seconds")

        # 记录合并历史
        if "merge_history" not in profile:
            profile["merge_history"] = []
        profile["merge_history"].append({
            "date": datetime.now().isoformat(timespec="seconds"),
            "action": "merge",
            "samples_added": new_sample_count,
            "old_samples": old_count,
            "old_weight": round(old_w, 4),
            "new_weight": round(new_w, 4),
        })

        self.update_profile(lecturer_id, profile)
        return {"status": "merged", "old_count": old_count, "new_count": new_sample_count}

    # ── 私有方法：文件系统写透 ──────────────────────────────

    def _write_profile_file(self, lecturer_id: str, profile: dict):
        """写 profile.json 到讲师目录（Write-Through）"""
        if not self.data_dir:
            return
        lec_dir = self.data_dir / "讲师列表" / lecturer_id
        lec_dir.mkdir(parents=True, exist_ok=True)
        (lec_dir / "profile.json").write_text(
            json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _write_sample_file(self, lecturer_id: str, sample_name: str, content: str):
        """写样本文件到讲师目录（Write-Through）"""
        if not self.data_dir:
            return
        samples_dir = self.data_dir / "讲师列表" / lecturer_id / "样本"
        samples_dir.mkdir(parents=True, exist_ok=True)
        (samples_dir / sample_name).write_text(content, encoding="utf-8")

    def _move_to_trash(self, lecturer_id: str):
        """移讲师目录到回收站（Write-Through，含 .meta.json 恢复信息）"""
        if not self.data_dir:
            return
        lec_dir = self.data_dir / "讲师列表" / lecturer_id
        if not lec_dir.exists():
            return
        trash_dir = self.data_dir / "回收站"
        trash_dir.mkdir(parents=True, exist_ok=True)

        # 写恢复元数据
        meta = {
            "type": "lecturer",
            "original_path": str(lec_dir),
            "deleted_at": datetime.now().isoformat(timespec="seconds"),
        }
        meta_path = trash_dir / f"{lecturer_id}.meta.json"
        meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")

        # 移动目录
        dest = trash_dir / lecturer_id
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(lec_dir), str(dest))

    # ── 私有方法：合并算法 ──────────────────────────────────

    def _merge_fields(self, old: dict, new: dict, old_w: float, new_w: float) -> dict:
        """按字段类型合并"""
        result = {}
        for key in set(list(old.keys()) + list(new.keys())):
            ov = old.get(key)
            nv = new.get(key)

            if ov is None:
                result[key] = nv
                continue
            if nv is None:
                result[key] = ov
                continue

            # 根据类型分派
            if isinstance(ov, dict) and isinstance(nv, dict):
                result[key] = self._merge_dict(ov, nv, old_w, new_w)
            elif isinstance(ov, list) and isinstance(nv, list):
                result[key] = self._merge_list(ov, nv)
            elif isinstance(ov, (int, float)) and isinstance(nv, (int, float)):
                result[key] = self._merge_numeric(ov, nv, old_w, new_w)
            else:
                result[key] = nv  # 默认取新值

        return result

    def _merge_dict(self, old: dict, new: dict, old_w: float, new_w: float) -> dict:
        """合并字典中的数值字段"""
        result = {}
        for key in set(list(old.keys()) + list(new.keys())):
            ov = old.get(key)
            nv = new.get(key)
            if ov is None:
                result[key] = nv
            elif nv is None:
                result[key] = ov
            elif isinstance(ov, (int, float)) and isinstance(nv, (int, float)):
                result[key] = self._merge_numeric(ov, nv, old_w, new_w)
            elif isinstance(ov, dict) and isinstance(nv, dict):
                result[key] = self._merge_dict(ov, nv, old_w, new_w)
            else:
                result[key] = nv
        return result

    def _merge_numeric(self, old: float, new: float, old_w: float, new_w: float) -> float:
        """数值型加权平均"""
        return round(old * old_w + new * new_w, 4)

    def _merge_list(self, old: list, new: list) -> list:
        """列表型合并去重（保留最新50条）"""
        if not old:
            return new
        if not new:
            return old
        # 对含word/count等字段的列表，合并同key项
        if isinstance(old[0], dict) and isinstance(new[0], dict):
            key_field = "word" if "word" in old[0] else "phrase" if "phrase" in old[0] else None
            if key_field:
                merged = {}
                for item in old + new:
                    k = item.get(key_field, "")
                    if k in merged:
                        merged[k]["count"] = merged[k].get("count", 0) + item.get("count", 0)
                    else:
                        merged[k] = dict(item)
                items = list(merged.values())
                items.sort(key=lambda x: x.get("count", 0), reverse=True)
                return items[:50]
        # 普通列表：合并去重
        seen = set()
        result = []
        for item in new + old:
            key = json.dumps(item, ensure_ascii=False) if isinstance(item, dict) else str(item)
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result[:50]

    @staticmethod
    def _deep_get(d: dict, *paths, fallback=None):
        """
        多路径查找嵌套字段，返回第一个找到的值。

        用法: _deep_get(profile, "persona_mapping", "qualitative.persona_mapping")
        路径用点号分隔，如 "qualitative.persona_mapping" → d["qualitative"]["persona_mapping"]
        """
        for path in paths:
            obj = d
            for key in path.split("."):
                if isinstance(obj, dict) and key in obj:
                    obj = obj[key]
                else:
                    obj = None
                    break
            if obj is not None:
                return obj
        return fallback if fallback is not None else {}
