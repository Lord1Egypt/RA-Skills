#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
academic-research 命令行脚本
"""

import sys
import json
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from academic_client import AcademicResearchClient


def main():
    params = {}
    if len(sys.argv) > 1:
        try:
            params = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("参数格式错误，应为 JSON")
            return

    client = AcademicResearchClient(params)
    try:
        client.initialize()
        query = params.get("query", "machine learning")
        result = client.search_papers(query)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        client.close()


if __name__ == "__main__":
    main()
