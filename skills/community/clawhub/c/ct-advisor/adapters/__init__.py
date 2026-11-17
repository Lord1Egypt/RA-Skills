"""ct-advisor 适配层统一出口。

v1.2.0（2026-09-25）框架整理：删除三个从未被 entry.py 主链使用的 legacy seam
（backend / data_context / qa_store —— 早期「本地 LocalBackend 兜底 + QA 日志」
架构残留，与 coze-only 红线冲突，且仅被同样已删除的 test_modeB 引用）。

现存职责单一：
- refiner.py  → CozeRefiner（唯一精校后端）+ RefineRequest/RefineResult 契约
- sanitize.py → 出站 PII 脱敏（ct-base §11）
- coze_token_embedded.py → 内嵌混淆公开凭据
- http_probe.py / install_sibling.py / probe_publication.py → 诊断与兄弟技能安装
- bug_report.py → §20.3 缺陷上报通道
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .refiner import (
    CozeRefiner, RefineRequest, RefineResult, Refiner,
    compute_machine_id, ACCURACY_ENUM, DIFFICULTY_ENUM,
    _parse_query_meta, strip_display_tags, MissingDependencyError,
)
from .sanitize import sanitize
from .errsignal import emit_err_signal, ERR_CODES

__all__ = [
    "Refiner", "RefineRequest", "RefineResult", "CozeRefiner",
    "compute_machine_id", "ACCURACY_ENUM", "DIFFICULTY_ENUM",
    "_parse_query_meta", "strip_display_tags", "sanitize",
    "build_refiner", "MissingDependencyError",
    "emit_err_signal", "ERR_CODES",
]


def _load_config(config_path: str = "config.json") -> Dict[str, Any]:
    # Stdlib-only loader (no PyYAML dependency). Missing file falls back to defaults.
    p = Path(config_path)
    if p.exists():
        try:
            import json
            return json.loads(p.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}
    return {}


def build_refiner(config_path: str = "config.json") -> Refiner:
    """答案精校出口（唯一 Coze 后端）。

    所有问题经 CozeRefiner 全量直发 Coze（单次调用，90s / 长任务 300s 超时），
    失败/超时回退 draft（v1.1.0 起 draft 恒为空 → 上层输出"请稍后重试"）。

    token 解析：统一从 adapters/coze_token_embedded.py 内嵌 obfuscated blob 读取
    （XOR+base64 公开凭据，无参 get_token()）。
    """
    cfg = _load_config(config_path)
    rc = cfg.get("refiner", {}) or {}
    return CozeRefiner(
        endpoint=rc.get("endpoint", ""),
        token_env=rc.get("token_env", "CT_ADVISOR_COZE_TOKEN"),
        timeout=float(rc.get("timeout", 90.0)),
        long_timeout=float(rc.get("long_timeout", 300.0)),
        race_window=float(rc.get("race_window", 2.0)),
        answer_mode="fast",  # 2026-08-05 起仅保留 fast
    )
