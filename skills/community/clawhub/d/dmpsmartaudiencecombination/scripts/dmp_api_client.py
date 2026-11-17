#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dmp_api_client.py

明日DMP OPENAPI 客户端——【强制通过鉴权技能调用】。

鉴权方式（必须，不可绕过）：
1. 通过 find_auth_skill 查找 mingdata-dmp-auth 鉴权技能的 minri_dmp_api.py
2. 用 subprocess.run 调用鉴权技能脚本（python3 minri_dmp_api.py POST <endpoint> '<json>'）
3. 解析stdout返回的JSON

⚠️ 本模块不自签、不读凭证文件、不裸写urllib。所有API调用必须通过鉴权技能。
⚠️ 若鉴权技能未安装，直接报错，不回退本地签名。

参考：dmp-segment技能的鉴权调用逻辑。
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from find_auth_skill import find_auth_skill_path  # noqa: E402


class DmpClient:
    """DMP客户端，所有调用通过鉴权技能subprocess执行。"""

    def __init__(self, timeout: int = 1800):
        """
        Args:
            timeout: 单次API调用超时（秒）。默认1800秒(30分钟)，
                因为人群创建/查询类接口可能需要长时间轮询计算结果。
                轻量接口(tag/list等)可在from_config时传入较短timeout。
        """
        self.auth_skill_path = find_auth_skill_path()
        if not self.auth_skill_path:
            raise RuntimeError(
                "未找到鉴权技能(mingdata-dmp-auth)。请先安装鉴权技能，或运行 preflight_check.py 检查。"
            )
        self.timeout = timeout

    def _call(self, method: str, endpoint: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """通过subprocess调用鉴权技能的minri_dmp_api.py"""
        cmd = ["python3", str(self.auth_skill_path), method.upper(), endpoint]
        if body is not None:
            cmd.append(json.dumps(body, ensure_ascii=False))
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=self.timeout
        )
        if result.returncode != 0:
            # 尝试解析stderr/stdout中的错误信息
            err_msg = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
            raise RuntimeError(f"DMP API调用失败(exit={result.returncode}): {err_msg[:500]}")
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(f"DMP API返回非JSON: {result.stdout[:500]}")

    def post(self, endpoint: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._call("POST", endpoint, body)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._call("GET", endpoint, params)

    @classmethod
    def from_config(cls, ak=None, sk=None, base_url=None, timeout=1800):
        """从配置创建客户端（ak/sk/base_url参数保留以兼容调用方，但实际由鉴权技能管理）。
        
        轻量接口建议传timeout=10~60，创建/轮询类接口使用默认1800即可。
        """
        return cls(timeout=timeout)


def ensure_ok(resp: Dict[str, Any]) -> Dict[str, Any]:
    """校验code=0，否则抛出异常"""
    code = resp.get("code")
    if str(code) != "0":
        raise RuntimeError(f"DMP API error: code={code}, msg={resp.get('msg')}")
    return resp
