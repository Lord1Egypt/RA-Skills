#!/usr/bin/env python3
"""
品牌列表查询脚本（v1.4新增）
功能：调用 /api/open-api/audience/rule/brand/list 查询当前租户下的品牌列表
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

    try:
        result = subprocess.run(
            ["python3", str(auth_script), "GET", "/api/open-api/audience/rule/brand/list", "{}"],
            capture_output=True, text=True, timeout=30
        )
        resp = json.loads(result.stdout.strip())
    except Exception as e:
        print(json.dumps({"error": "CALL_ERROR", "message": f"调用失败: {e}"}, ensure_ascii=False))
        sys.exit(6)

    if resp.get("code") != "0":
        print(json.dumps(resp, ensure_ascii=False))
        sys.exit(1)

    brands = resp.get("data", []) or []

    if args.format == "table":
        print(json.dumps({
            "ok": True,
            "total": len(brands),
            "brands": [{"brandId": b.get("brandId"), "brandName": b.get("brandName", "")} for b in brands]
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(resp, ensure_ascii=False))


if __name__ == "__main__":
    main()
