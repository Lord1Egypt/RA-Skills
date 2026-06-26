#!/usr/bin/env python3
"""
数据库初始化 + 控制台目录搭建 + 模型下载

用法:
  python scripts/db_init.py --setup --parent-dir <存放位置>     # 在指定位置下创建"控制台"文件夹并初始化
  python scripts/db_init.py --download-model --data-dir <目录>  # 下载语义模型
  python scripts/db_init.py --download-model --force-download   # 强制重新下载模型

注意:
  --setup 必须配合 --parent-dir，脚本会自动在指定位置下创建名为"控制台"的文件夹，
  文件夹名称固定为"控制台"，不可更改。所有数据文件和数据结构均在此文件夹内。
"""

import argparse
import json
import sys
from pathlib import Path

SKILL_ROOT = str(Path(__file__).resolve().parent.parent)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)

from scripts.core.db_manager import DatabaseManager, resolve_db_path
from scripts.core.semantic_model import check_model_files, download_model

# 控制台文件夹名称——固定不可更改
CONSOLE_DIR_NAME = "控制台"

# 默认行为规则模板
DEFAULT_ALLOWED = {
    "description": "文案中必须遵守的用词和表述规则，生成文案时逐条执行",
    "rules": []
}

DEFAULT_FORBIDDEN = {
    "description": "文案中严格禁止的用词和表述，违反将导致法律风险或品牌损害",
    "rules": []
}

DEFAULT_WORKSPACE = {
    "data_dir": "./控制台",
    "trash_dir": "./控制台/回收站",
    "version": "2.0",
    "knowledge_sync": {
        "base_url": "",
        "auto_sync": True
    }
}


def resolve_console_dir(parent_dir: str) -> Path:
    """
    根据用户指定的存放位置，推导控制台目录路径。
    控制台文件夹名称固定为"控制台"，不可更改。

    例如: parent_dir="C:/Users/xxx/Desktop" → "C:/Users/xxx/Desktop/控制台"
    """
    parent = Path(parent_dir)
    if not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)
    console_dir = parent / CONSOLE_DIR_NAME
    return console_dir


def setup_data_dir(data_dir: Path) -> dict:
    """
    创建控制台基础目录结构和默认文件

    结构:
      控制台/
      ├── workspace.json
      ├── 回收站/
      ├── 讲师列表/
      └── 知识库集/
          ├── 公共/
          │   └── 公共行为/
          │       ├── 允许行为.json
          │       └── 禁止行为.json
          └── 私有/
    """
    created = []
    skipped = []

    # workspace.json
    data_dir.mkdir(parents=True, exist_ok=True)
    ws_path = data_dir / "workspace.json"
    if not ws_path.exists():
        ws_path.write_text(json.dumps(DEFAULT_WORKSPACE, ensure_ascii=False, indent=2), encoding="utf-8")
        created.append("workspace.json")
    else:
        skipped.append("workspace.json")

    # 基础目录
    dirs = [
        data_dir / "回收站",
        data_dir / "讲师列表",
        data_dir / "知识库集" / "公共" / "公共行为",
        data_dir / "知识库集" / "私有",
    ]
    for d in dirs:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(str(d.relative_to(data_dir)) + "/")
        else:
            skipped.append(str(d.relative_to(data_dir)) + "/")

    # 默认行为规则
    beh_dir = data_dir / "知识库集" / "公共" / "公共行为"

    allowed_path = beh_dir / "允许行为.json"
    if not allowed_path.exists():
        allowed_path.write_text(json.dumps(DEFAULT_ALLOWED, ensure_ascii=False, indent=2), encoding="utf-8")
        created.append("知识库集/公共/公共行为/允许行为.json")
    else:
        skipped.append("知识库集/公共/公共行为/允许行为.json")

    forbidden_path = beh_dir / "禁止行为.json"
    if not forbidden_path.exists():
        forbidden_path.write_text(json.dumps(DEFAULT_FORBIDDEN, ensure_ascii=False, indent=2), encoding="utf-8")
        created.append("知识库集/公共/公共行为/禁止行为.json")
    else:
        skipped.append("知识库集/公共/公共行为/禁止行为.json")

    return {"status": "ok", "created": created, "skipped": skipped}


def main():
    parser = argparse.ArgumentParser(description="Aicwos 数据库初始化")
    parser.add_argument("--setup", action="store_true",
                        help="创建控制台目录结构（需配合 --parent-dir，自动在指定位置下创建'控制台'文件夹）")
    parser.add_argument("--parent-dir", default=None,
                        help="控制台存放位置（如桌面路径），脚本自动在其下创建'控制台'文件夹（--setup 时必填）")
    parser.add_argument("--data-dir", default=None,
                        help="控制台目录路径（仅 --download-model 时使用，直接指向已有的控制台文件夹）")
    parser.add_argument("--download-model", action="store_true",
                        help="下载ONNX语义模型（优先INT8量化版~98MB）")
    parser.add_argument("--force-download", action="store_true", help="强制重新下载模型")
    args = parser.parse_args()

    results = {}

    # --setup 模式：从 --parent-dir 推导控制台路径
    if args.setup:
        if not args.parent_dir:
            print(json.dumps({
                "status": "error",
                "message": "--setup 必须配合 --parent-dir 指定存放位置。脚本会自动在该位置下创建'控制台'文件夹。例如: --parent-dir C:/Users/xxx/Desktop"
            }, ensure_ascii=False))
            return

        console_dir = resolve_console_dir(args.parent_dir)
        data_dir_for_db = str(console_dir)
    else:
        data_dir_for_db = args.data_dir

    # 解析数据库路径
    try:
        resolved_db = resolve_db_path(None, data_dir_for_db)
    except ValueError as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        return

    # 1. 初始化数据库
    db = DatabaseManager(resolved_db)
    init_result = db.initialize()
    results["database"] = init_result
    db.close()

    # 2. 创建控制台目录结构
    if args.setup:
        results["console_dir"] = str(console_dir)
        results["console_dir_name"] = CONSOLE_DIR_NAME
        results["setup"] = setup_data_dir(console_dir)

    # 3. 检查/下载模型
    model_status = check_model_files()
    results["model_status"] = model_status

    if args.download_model or args.force_download:
        dl_result = download_model(force=args.force_download)
        results["model_download"] = dl_result

        # 重新检查状态
        model_status = check_model_files()
        results["model_status_after"] = model_status

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
