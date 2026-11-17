"""
manifest.json 模板生成器
"""

import json
from datetime import datetime
from typing import List, Dict


def generate_manifest_json(
    project_name: str,
    description: str = "",
    assets: List[Dict] = None,
) -> str:
    """生成机器可读的 manifest.json"""
    data = {
        "project_name": project_name,
        "description": description,
        "generated_at": datetime.now().isoformat(),
        "python_version": "3.10",
        "assets": assets or [],
        "environment": {
            "os": "",
            "file": "requirements.txt",
        },
        "design_decisions": [],
        "known_limitations": [],
        "future_improvements": [],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)
