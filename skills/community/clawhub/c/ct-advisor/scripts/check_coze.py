#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_coze.py — ct-advisor Coze 端点一键诊断。

在 Coze 调用失败（stderr 出现 FALLBACK / ProxyError / Timeout，或 stdout 输出
"Coze 调用失败…请运行 check_coze.py"）时运行，定位是 死代理残留 / 断网 /
token 缺失 / 端点不可达 中的哪一种，并给出修复指引。

用法：python scripts/check_coze.py
纯本地、零敏感信息输出（不打印 token 明文、不打印环境代理值中的敏感段）。
"""
import json
import os
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # 确保 adapters/ 可导入（§16.9 出站常量与调用收口至此）
from adapters.http_probe import COZE_ENDPOINT, probe_get

ENDPOINT = COZE_ENDPOINT


def _proxy_envs() -> dict:
    keys = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
            "http_proxy", "https_proxy", "all_proxy", "NO_PROXY", "no_proxy"]
    return {k: os.environ.get(k) for k in keys if os.environ.get(k)}


def _port_open(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.close()
        return True
    except OSError:
        return False


def _probe(proxies=None, timeout: float = 8.0):
    """小请求探测端点。返回 (ok, 状态码或错误摘要)。出站逻辑与常量收口在 adapters/http_probe.py（§16.9）。"""
    return probe_get(ENDPOINT, timeout=timeout, proxies=proxies)


def main() -> int:
    print("=" * 56)
    print("ct-advisor Coze 端点诊断")
    print("=" * 56)
    issues = []

    # 1) token 是否就位
    try:
        sys.path.insert(0, str(ROOT))
        from adapters.coze_token_embedded import get_token  # noqa: PLC0415
        tok = get_token()
        if tok:
            print(f"[token]    配置存在（{len(tok)} 字符，不显示明文）✓")
        else:
            print("[token]    ⚠️ token 为空——检查 adapters/coze_token_embedded.py")
            issues.append("token 为空")
    except Exception as e:  # noqa: BLE001
        print(f"[token]    ⚠️ 读取失败: {e}")
        issues.append("token 读取失败")

    # 2) 环境代理
    pe = _proxy_envs()
    if pe:
        safe = {k: ("***" if "PROXY" in k.upper() and "NO_PROXY" not in k.upper() else v)
                for k, v in pe.items()}
        print(f"[proxy]    检测到环境代理变量: {json.dumps(safe, ensure_ascii=False)}")
        for k, v in pe.items():
            if "NO_PROXY" in k.upper():
                continue
            h = v.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
            port = 0
            try:
                port = int(v.replace("http://", "").replace("https://", "")
                           .split("/")[0].split(":")[1])
            except (IndexError, ValueError):
                pass
            if port and not _port_open(h, port):
                print(f"    ⚠️ {k}={v} → 端口不可达（死代理残留），requests 会因此报 ProxyError")
                issues.append(f"死代理残留: {k}={v}")
            elif port:
                print(f"    {k}={v} → 端口可达 ✓")
    else:
        print("[proxy]    无环境代理变量 ✓")

    # 3) 绕过代理直连探测（本技能内置的容错路径）
    ok, info = _probe(proxies={"http": None, "https": None})
    print(f"[direct]   绕过代理直连 {ENDPOINT}: {'✓ HTTP ' + str(info) if ok else '✗ ' + info}")
    if not ok:
        issues.append(f"直连失败: {info}")

    # 4) 按环境代理探测（若存在代理变量）
    if any(k.upper() in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY") for k in pe):
        ok2, info2 = _probe(proxies=None, timeout=8.0)
        print(f"[proxied]  按环境代理请求: {'✓ HTTP ' + str(info2) if ok2 else '✗ ' + info2}")

    # 5) 结论与修复指引
    print("-" * 56)
    if not issues:
        print("结论: 端点可达、token 就位、代理正常——问题可能不在网络层，请检查 payload / 日志。")
    else:
        print("发现以下问题，修复指引：")
        for i, it in enumerate(issues, 1):
            print(f"  {i}. {it}")
        if any("死代理" in x for x in issues):
            print("     → 关闭系统代理（Windows: 设置→网络和 Internet→代理），或设置环境变量")
            print("       NO_PROXY=ct-advisor.coze.site；本技能 v0.9.60+ 已内置代理失败自动绕过直连重试。")
        if any("直连失败" in x for x in issues):
            print("     → 检查网络连通性（能否访问公网）；若必须走代理，请配置可用代理后重试。")
        if any("token" in x for x in issues):
            print("     → 重新安装技能（adapters/coze_token_embedded.py 内含共享 token）或联系作者。")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
