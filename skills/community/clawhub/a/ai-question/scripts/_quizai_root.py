"""Resolve QuizAI repository root from skill script location."""

from __future__ import annotations

from pathlib import Path


def quizai_root() -> Path:
    here = Path(__file__).resolve().parent
    for parent in [here, *here.parents]:
        if (parent / "run.py").is_file() and (parent / "app" / "main.py").is_file():
            return parent
    raise RuntimeError(
        "未找到 QuizAI 项目根目录（需包含 run.py 与 app/main.py）。请在仓库根目录打开 Agent。"
    )
