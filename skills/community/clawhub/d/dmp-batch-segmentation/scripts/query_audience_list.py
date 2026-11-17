#!/usr/bin/env python3
"""
查询人群列表
功能：查询DMP已有人群包列表，支持按名称关键词搜索
"""

import sys
import json
import subprocess
from pathlib import Path


def find_auth_skill_path():
    """查找鉴权技能的API脚本路径"""
    possible_paths = [
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.cwd() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    scan_dirs = [
        Path.home() / ".skills",
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".openclaw" / "skills",
        Path.cwd() / ".skills",
    ]
    for scan_dir in scan_dirs:
        if scan_dir.exists():
            for skill_dir in scan_dir.iterdir():
                if skill_dir.is_dir():
                    auth_path = skill_dir / "scripts" / "minri_dmp_api.py"
                    if auth_path.exists():
                        try:
                            with open(auth_path, 'r', encoding='utf-8') as f:
                                content = f.read(500)
                                if "明日DMP" in content or "mingdata" in content.lower():
                                    return auth_path
                        except:
                            continue
    return None


def call_api(endpoint, request_body, method="POST"):
    """调用鉴权技能的统一API模块"""
    auth_skill_path = find_auth_skill_path()

    if not auth_skill_path:
        print(json.dumps({
            "error": "AUTH_SKILL_NOT_FOUND",
            "message": "未找到鉴权技能，请先安装mingdata-dmp-auth技能"
        }, ensure_ascii=False))
        sys.exit(3)

    try:
        result = subprocess.run(
            ["python3", str(auth_skill_path), method, endpoint, json.dumps(request_body)],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result.stdout)
        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print(json.dumps({
            "error": "TIMEOUT",
            "message": "API调用超时"
        }, ensure_ascii=False))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({
            "error": "CALL_ERROR",
            "message": f"调用鉴权技能失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(6)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='查询DMP人群包列表')
    parser.add_argument('--keyword', '-k', help='按人群名称关键词搜索')
    parser.add_argument('--page-size', type=int, default=50, help='每页数量（默认50，最大100）')
    parser.add_argument('--page', type=int, default=1, help='页码（默认1）')
    parser.add_argument('--audience-ids', help='按人群ID列表查询（逗号分隔）')
    args = parser.parse_args()

    # 构建请求体
    request_body = {
        "pageSize": min(args.page_size, 100),
        "pageNum": args.page
    }

    if args.keyword:
        request_body["name"] = args.keyword

    if args.audience_ids:
        try:
            ids = [int(x.strip()) for x in args.audience_ids.split(',') if x.strip()]
            request_body["audienceIds"] = ids
        except ValueError:
            print(json.dumps({
                "error": "INVALID_PARAM",
                "message": "人群ID必须为数字，多个用逗号分隔"
            }, ensure_ascii=False))
            sys.exit(1)

    call_api("/audience/manage/list", request_body, method="POST")


if __name__ == "__main__":
    main()
