#!/usr/bin/env python3
"""
品牌列表查询脚本（v1.4新增）
功能：调用 /api/open-api/audience/rule/brand/list 查询当前租户下的品牌列表
返回：brandId, brandName
"""

import sys
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from find_auth_skill import find_auth_skill_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description='查询品牌列表')
    parser.add_argument('--format', default='json', choices=['json', 'table'], help='输出格式')
    args = parser.parse_args()

    auth_script = find_auth_skill_path()
    if not auth_script:
        print(json.dumps({"error": "AUTH_SKILL_NOT_FOUND", "message": "未找到鉴权技能"}, ensure_ascii=False))
        sys.exit(3)

    # 调用品牌列表接口（GET，无body）
    try:
        result = subprocess.run(
            ["python3", str(auth_script), "GET", "/api/open-api/audience/rule/brand/list", "{}"],
            capture_output=True, text=True, timeout=30
        )
        raw = result.stdout.strip()
        # 尝试解析JSON
        resp = json.loads(raw)
    except Exception as e:
        print(json.dumps({"error": "CALL_ERROR", "message": f"调用失败: {e}", "raw": raw if 'raw' in dir() else ""}, ensure_ascii=False))
        sys.exit(6)
        return

    if resp.get("code") != "0":
        print(json.dumps(resp, ensure_ascii=False))
        sys.exit(1)
        return

    brands = resp.get("data", []) or []

    if args.format == "table":
        # 表格输出（供AI展示给用户）
        print(json.dumps({
            "ok": True,
            "total": len(brands),
            "brands": [
                {"brandId": b.get("brandId"), "brandName": b.get("brandName", "")}
                for b in brands
            ]
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(resp, ensure_ascii=False))


if __name__ == "__main__":
    main()
