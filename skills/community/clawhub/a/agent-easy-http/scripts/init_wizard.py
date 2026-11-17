#!/usr/bin/env python3
"""init_wizard.py — agent-easy-http v3.0 交互式初始化向导

v3.0 改动：
- ✅ 新增 Step 2：自动检测/启用 OpenClaw hooks（参考 html-go-live --setup-hooks）
- ❌ 删除：选择 OpenClaw session（hooks 自动管理）
- ❌ 删除：HMAC secret 生成（callback 链路已删）

引导用户：
1. 监听端口和地址
2. 检测/启用 OpenClaw hooks（自动写入 openclaw.json + 可选同步到外部配置源）
3. 生成或复用 API Key（外部调用方鉴权）
4. 生成 TLS 证书（带 SAN）
5. 配置 deny_skills 黑名单
6. 写入 config.json

支持子命令：
    python3 init_wizard.py                    # 完整向导
    python3 init_wizard.py --setup-hooks-only  # 只跑 hooks 启用步骤
    python3 init_wizard.py --check-hooks       # 只检测 hooks，不修改
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SKILL_NAME = "agent-easy-http"

# 导入同级 tls_auth 模块
sys.path.insert(0, str(Path(__file__).parent))
from tls_auth import (  # noqa: E402
    ensure_dirs,
    generate_api_key,
    save_api_key,
    load_api_key,
    DEFAULT_CERT_PATH,
    DEFAULT_KEY_PATH,
    API_KEYS_DIR,
    HTTP_ROOT,
)


def _detect_data_root() -> Path:
    """与 server.py 保持一致的数据根路径探测。"""
    env_root = os.environ.get("AGENT_EASY_HTTP_DATA_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    workspace = os.environ.get(
        "OPENCLAW_WORKSPACE",
        str(Path.home() / ".openclaw" / "workspace"),
    )
    ws_path = Path(workspace)
    if ws_path.exists() and (ws_path / "skills").exists():
        return ws_path / ".agent-easy-http"
    return Path.home() / ".agent-easy-http"


DATA_ROOT = _detect_data_root()
CONFIG_PATH = DATA_ROOT / "config.json"

# OpenClaw 配置同步路径（防外部配置中心覆盖，如托管环境的 config manager）
# 默认空——普通部署无需同步。托管/容器环境若有额外 config 源，可通过环境变量
# OPENCLAW_CONFIG_SYNC_PATHS（冒号分隔多个路径）指定，写入 openclaw.json 后一并同步过去。
OPENCLAW_CFG_PATH = Path.home() / ".openclaw" / "openclaw.json"
_sync_env = os.environ.get("OPENCLAW_CONFIG_SYNC_PATHS", "").strip()
OPENCLAW_SYNC_PATHS = [
    Path(p).expanduser() for p in _sync_env.split(":") if p.strip()
] if _sync_env else []
DEFAULT_GATEWAY_PORT = 18789

# 推荐拒绝清单（有副作用 / 会对外发消息 / 改系统配置的 skill）
# 这里给的是通用示例；请根据你本机实际安装的 skill 调整。
# init wizard 只会保留下面这些里「本机确实装了」的作为默认拒绝项。
RECOMMENDED_DENY = [
    "hello-env",              # 示例占位（无副作用，通常不必拒；仅演示格式）
    "skill-creator",
    "skill-creator-plus",
    "collective-memory",
]


def ask(prompt: str, default: str = "", allow_empty: bool = True) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        ans = input(f"{prompt}{suffix}: ").strip()
        if not ans:
            ans = default
        if ans or allow_empty:
            return ans
        print("  ❌ 不能为空，请重新输入")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        ans = input(f"{prompt} {suffix}: ").strip().lower()
        if not ans:
            return default
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False


def detect_local_ips() -> list[str]:
    ips: list[str] = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
    except Exception:
        pass
    try:
        result = subprocess.run(
            ["hostname", "-I"], capture_output=True, text=True, timeout=3
        )
        for ip in result.stdout.strip().split():
            if ip and ip != "127.0.0.1" and ip not in ips:
                ips.append(ip)
    except Exception:
        pass
    return ips


def list_installed_skills() -> list[str]:
    workspace = os.environ.get(
        "OPENCLAW_WORKSPACE",
        str(Path.home() / ".openclaw" / "workspace"),
    )
    skills_dir = Path(workspace) / "skills"
    if not skills_dir.exists():
        return []
    return sorted([
        entry.name for entry in skills_dir.iterdir()
        if entry.is_dir() and (entry / "SKILL.md").exists()
    ])


def banner(text: str) -> None:
    print()
    print("─" * 60)
    print(f"  {text}")
    print("─" * 60)


# ── OpenClaw hooks 检测 / 启用 ──────────────────────────────────────
def _deep_merge(target: dict, patch: dict) -> None:
    """深合并 patch 到 target（in-place）。"""
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(target.get(k), dict):
            _deep_merge(target[k], v)
        else:
            target[k] = v


def _patch_openclaw_json(patch: dict) -> tuple[bool, str]:
    """安全 patch openclaw.json + 可选同步到外部配置源（防被覆盖）。"""
    try:
        if OPENCLAW_CFG_PATH.exists():
            cfg = json.loads(OPENCLAW_CFG_PATH.read_text(encoding="utf-8"))
        else:
            cfg = {}
        _deep_merge(cfg, patch)
        OPENCLAW_CFG_PATH.parent.mkdir(parents=True, exist_ok=True)
        OPENCLAW_CFG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")

        synced = []
        for sp in OPENCLAW_SYNC_PATHS:
            try:
                if sp.exists():
                    shutil.copy2(OPENCLAW_CFG_PATH, sp)
                    synced.append(str(sp))
            except Exception as e:
                print(f"  ⚠️  同步到 {sp} 失败: {e}（不影响运行）")
        return True, f"已写入 {OPENCLAW_CFG_PATH}" + (f"，同步 {len(synced)} 个源文件" if synced else "")
    except Exception as e:
        return False, str(e)


def _probe_hook_endpoint(hook_url: str, hook_token: str, timeout: int = 5) -> tuple[bool, str]:
    """探活 POST /hooks/agent，验证 token 和 URL 都正确。"""
    try:
        req = urllib.request.Request(
            hook_url,
            data=json.dumps({"message": "ping"}).encode(),
            headers={
                "Authorization": f"Bearer {hook_token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            data = json.loads(body)
            if data.get("ok") and data.get("runId"):
                return True, f"runId={data['runId'][:8]}..."
            return False, f"unexpected response: {data}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read()[:200].decode(errors='replace')}"
    except Exception as e:
        return False, str(e)


def ensure_hooks_enabled(interactive: bool = True, force_new_token: bool = False,
                          read_only: bool = False) -> dict:
    """检测 + 启用 OpenClaw hooks。

    参数：
      interactive: True 时未启用会询问用户；False 时未启用直接报失败
      force_new_token: True 时即使已启用也重新生成
      read_only: True 时不允许任何写操作（即使 interactive 拿到 y 同意也不写）

    返回: {
        "ok": bool,
        "action": "ok"|"enabled"|"skipped"|"failed"|"not_enabled",
        "token": str,
        "url":   str,
        "message": str,
    }
    """
    if not OPENCLAW_CFG_PATH.exists():
        return {
            "ok": False, "action": "failed",
            "token": "", "url": "",
            "message": f"找不到 {OPENCLAW_CFG_PATH}，确认 OpenClaw 已安装并运行过 setup",
        }

    try:
        cfg = json.loads(OPENCLAW_CFG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        return {
            "ok": False, "action": "failed",
            "token": "", "url": "",
            "message": f"读取 openclaw.json 失败: {e}",
        }

    hooks = cfg.get("hooks") or {}
    enabled = hooks.get("enabled", False)
    token = (hooks.get("token") or "").strip()
    gateway_port = (cfg.get("gateway") or {}).get("port") or DEFAULT_GATEWAY_PORT
    hook_url = f"http://127.0.0.1:{gateway_port}/hooks/agent"

    # Case 1: 已启用且 token 完整
    if enabled and token and not force_new_token:
        # 检查 allowRequestSessionKey + allowedSessionKeyPrefixes 是否齐全
        # 缺失则补写（v1.0.4+ 的 /result 接口需要这两个配置才能精确匹配）
        needs_patch = (
            not hooks.get("allowRequestSessionKey")
            or "hook:" not in (hooks.get("allowedSessionKeyPrefixes") or [])
        )
        if needs_patch and not read_only:
            print("  ℹ️  hooks 缺 allowRequestSessionKey 配置，自动补写...")
            print("     ⚠️  注意：开启 allowRequestSessionKey 会影响所有 /hooks/agent 调用方")
            print("        （受 allowedSessionKeyPrefixes=['hook:'] 限制，安全可控）")
            patched, msg = _patch_openclaw_json({"hooks": {
                "enabled": True,
                "token": token,
                "allowRequestSessionKey": True,
                "allowedSessionKeyPrefixes": ["hook:"],
            }})
            if patched:
                print(f"  ✅ 已补写：{msg}")
                time.sleep(2)  # 等热加载
        elif needs_patch and read_only:
            # L3: read_only 模式下也要让用户感知配置缺失
            print("  ⚠️  hooks 缺 allowRequestSessionKey 或 allowedSessionKeyPrefixes 配置")
            print("     read_only 模式未自动修复。/result 接口会持续报 not_found")
            print("     运行 `python3 scripts/server.py setup-hooks` 修复")

        ok, info = _probe_hook_endpoint(hook_url, token)
        return {
            "ok": ok,
            "action": "ok" if ok else ("config_incomplete" if needs_patch and read_only else "failed"),
            "token": token,
            "url": hook_url,
            "message": (
                "hooks 已启用并验证通过" if ok
                else f"hooks 配置不完整（read_only 未修复）" if needs_patch and read_only
                else f"hooks 已配置但探活失败: {info}"
            ),
        }

    # Case 2: 需要新生成 token（未启用 / 强制重新生成 / enabled 但 token 缺失）
    # read_only 模式：只报状态，不做任何写
    if read_only:
        return {
            "ok": False, "action": "not_enabled",
            "token": token, "url": hook_url,
            "message": "hooks 未启用或 token 缺失（read_only 模式，未做修改）。运行 setup-hooks 修复。",
        }
    if interactive and not force_new_token:
        prompt = ("OpenClaw 原生 hooks 未启用，agent-easy-http 需要它才能工作。\n"
                  "  - 会写入 ~/.openclaw/openclaw.json（添加 hooks.enabled + token）\n"
                  "  - 若设了 OPENCLAW_CONFIG_SYNC_PATHS，会一并同步到那些外部配置源\n"
                  "    （托管/容器环境防被外部 config 中心覆盖；普通部署无需设置）\n"
                  "  - 会启用 hooks.allowRequestSessionKey=true（受 ['hook:'] 前缀限制）\n"
                  "    ⚠️  此选项影响所有 /hooks/agent 调用方，不只是 agent-easy-http\n"
                  "  - Gateway 热加载，无需重启\n"
                  "是否现在启用？")
        if not ask_yes_no(prompt, default=True):
            return {
                "ok": False, "action": "skipped",
                "token": "", "url": "",
                "message": "用户选择不启用，可稍后运行: python3 server.py setup-hooks",
            }
    elif not interactive and not force_new_token:
        # 非交互且不强制，未启用则报失败（不写）
        return {
            "ok": False, "action": "not_enabled",
            "token": "", "url": hook_url,
            "message": "hooks 未启用且非交互模式（不会自动写入）。运行 setup-hooks 启用。",
        }

    new_token = secrets.token_urlsafe(32)
    # 同时启用 allowRequestSessionKey + allowedSessionKeyPrefixes
    # 让 agent-easy-http 能自定义 sessionKey=hook:<uuid>，/result 接口精确匹配
    # prefix 限制为 ["hook:"]，防止调用方污染其他 session
    success, msg = _patch_openclaw_json({"hooks": {
        "enabled": True,
        "token": new_token,
        "allowRequestSessionKey": True,
        "allowedSessionKeyPrefixes": ["hook:"],
    }})
    if not success:
        return {
            "ok": False, "action": "failed",
            "token": "", "url": "",
            "message": f"写入 openclaw.json 失败: {msg}",
        }

    print(f"  ✅ {msg}")
    print(f"  ⏳ 等待 Gateway 热加载（3s）...")
    time.sleep(3)

    ok, info = _probe_hook_endpoint(hook_url, new_token)
    if ok:
        return {
            "ok": True, "action": "enabled",
            "token": new_token, "url": hook_url,
            "message": f"hooks 已启用并验证通过 ({info})",
        }
    else:
        return {
            "ok": False, "action": "failed",
            "token": new_token, "url": hook_url,
            "message": f"hooks 已写入但探活失败: {info}（可能 Gateway 未运行，或还在热加载中）",
        }


# ── 完整向导 ─────────────────────────────────────────────────────────
def run_full_wizard():
    print()
    print("=" * 60)
    print("  🚀 agent-easy-http v3.0 初始化向导")
    print("=" * 60)
    print("  本向导会引导你配置 HTTPS 服务、OpenClaw hooks、TLS 证书等。")
    print("  全程可按 Ctrl+C 取消。")
    print()

    existing_config = {}
    if CONFIG_PATH.exists():
        try:
            existing_config = json.loads(CONFIG_PATH.read_text())
            print(f"⚠️  发现已有配置：{CONFIG_PATH}")
            if not ask_yes_no("是否覆盖重新配置？", default=False):
                print("已取消")
                return
        except Exception:
            pass

    config: dict = {}

    # ── Step 1: 监听配置 ───────────────────────────────────────────
    banner("Step 1/5: 监听配置")
    config["listen_host"] = ask(
        "监听地址（127.0.0.1=仅本机[默认/推荐]，0.0.0.0=允许内网访问，需配合 HTTPS 或显式豁免）",
        default=existing_config.get("listen_host", "127.0.0.1"),
    )
    config["port"] = int(ask(
        "监听端口",
        default=str(existing_config.get("port", 7720)),
    ))

    # ── Step 2: OpenClaw hooks（新增）──────────────────────────────
    banner("Step 2/5: 检测 OpenClaw hooks")
    print("📋 检测 ~/.openclaw/openclaw.json 中的 hooks 配置...")
    hooks_result = ensure_hooks_enabled(interactive=True)
    if hooks_result["ok"]:
        print(f"  ✅ {hooks_result['message']}")
        # hook_url/token 留空 = 走 server.py 自动推导
        config["hook_url"] = ""
        config["hook_token"] = ""
    else:
        print(f"  ⚠️  {hooks_result['message']}")
        print("     稍后可运行: python3 server.py setup-hooks 重试")
        if not ask_yes_no("是否仍继续配置（agent-easy-http 启动时会再次校验）？", default=True):
            print("已取消")
            return
        config["hook_url"] = ""
        config["hook_token"] = ""

    # ── Step 3: API Key ───────────────────────────────────────────
    banner("Step 3/5: API Key（外部调用方鉴权）")
    existing_api_key = load_api_key(SKILL_NAME)
    if existing_api_key and ask_yes_no(
        f"已有 API Key（{existing_api_key[:8]}...），继续使用？", default=True
    ):
        config["api_key"] = existing_api_key
    else:
        config["api_key"] = generate_api_key()
        path = save_api_key(SKILL_NAME, config["api_key"])
        print(f"✅ 已生成新 API Key 并保存到：{path}")
    print(f"   预览：{config['api_key'][:8]}...{config['api_key'][-4:]}")

    # ── Step 4: TLS 证书（默认关闭，按需开启）──────────────────────
    banner("Step 4/5: TLS / HTTPS")
    print("HTTPS 提供传输层加密，但需要生成自签证书 + 客户端导入，有一定门槛。")
    print("说明：")
    print("  - 不开 HTTPS  → 调用方直接 curl 即可，零门槛（推荐先跑通再加 TLS）")
    print("  - 开 HTTPS    → 调用方需要 --cacert 指定证书（或导入系统信任库）")
    if config.get("listen_host") == "0.0.0.0":
        print("  ⚠️  当前监听 0.0.0.0（局域网可达）：v1.1.0 起 0.0.0.0 + HTTP 需显式豁免")
        print("      （allow_insecure_public_bind=true 或 AGENT_EASY_HTTP_ALLOW_INSECURE=1），")
        print("      跨机器调用强烈建议开 TLS")
    print()
    config["tls_enabled"] = ask_yes_no(
        "现在启用 HTTPS？（n=先用 HTTP 跑通，需要时跑 gen_cert.py 再切回 HTTPS）",
        default=False,
    )
    if config["tls_enabled"]:
        config["cert_path"] = str(DEFAULT_CERT_PATH)
        config["key_path"] = str(DEFAULT_KEY_PATH)
        if DEFAULT_CERT_PATH.exists():
            print(f"✅ 已有证书：{DEFAULT_CERT_PATH}")
            if ask_yes_no("是否重新生成？", default=False):
                _run_gen_cert()
        else:
            print("⚠️  尚未生成证书")
            if ask_yes_no("现在生成？", default=True):
                _run_gen_cert()
            else:
                print("⚠️  稍后手动跑：python3 scripts/gen_cert.py --san auto")
    else:
        # 仍保留默认 cert/key 路径，方便用户后续直接改 config 切回 HTTPS
        config["cert_path"] = str(DEFAULT_CERT_PATH)
        config["key_path"] = str(DEFAULT_KEY_PATH)
        print()
        print("ℹ️  已选 HTTP 模式。想后续切回 HTTPS：")
        print("     1. python3 scripts/gen_cert.py --san auto    # 生成证书")
        print(f"     2. 编辑 {CONFIG_PATH} 把 tls_enabled 改 true")
        print("     3. python3 scripts/server.py restart")

    # ── Step 5: deny_skills 黑名单 ──────────────────────────────────
    banner("Step 5/5: deny_skills 黑名单")
    installed = list_installed_skills()
    print(f"📦 本机已装 {len(installed)} 个 skill")
    print()
    print("推荐拒绝的 skill（有副作用 / 改系统 / 发外部消息）：")
    suggested = [s for s in RECOMMENDED_DENY if s in installed]
    for s in suggested:
        print(f"  - {s}")
    print()

    deny_choice = ask(
        "采用推荐清单 [y]，全部允许 [n]，自定义 [c]",
        default="y",
    ).lower()
    if deny_choice == "y":
        config["deny_skills"] = suggested
    elif deny_choice == "c":
        user_deny = ask(
            "请输入要拒绝的 skill（逗号分隔）",
            default=",".join(suggested),
        )
        config["deny_skills"] = [s.strip() for s in user_deny.split(",") if s.strip()]
    else:
        config["deny_skills"] = []
        print("⚠️  所有 skill 都将被允许执行，仅靠 API Key 把关")

    # 其他默认值
    config["expose_skills"] = []
    config["max_concurrent_jobs"] = 10
    config["hook_request_timeout"] = 30

    # ── 写入配置 ────────────────────────────────────────────────────
    ensure_dirs()
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2))
    os.chmod(CONFIG_PATH, 0o600)

    print()
    print("=" * 60)
    print("  ✅ 初始化完成！")
    print("=" * 60)
    print(f"  配置文件：{CONFIG_PATH}")
    print(f"  API Key ：{API_KEYS_DIR / (SKILL_NAME + '.key')}")
    if config["tls_enabled"]:
        print(f"  TLS 证书：{config['cert_path']}")
    print()
    print("  🚀 启动服务：")
    print("     python3 scripts/server.py start")
    print()
    print("  📖 客户端调用示例：")
    proto = "https" if config["tls_enabled"] else "http"
    host = config["listen_host"] if config["listen_host"] != "0.0.0.0" else "<your-ip>"
    print(f"     curl -H 'X-API-Key: $(cat {API_KEYS_DIR / (SKILL_NAME + '.key')})' \\")
    if config["tls_enabled"]:
        print(f"          --cacert {config['cert_path']} \\")
    print(f"          -H 'Content-Type: application/json' \\")
    print(f"          -d '{{\"message\":\"hello\"}}' \\")
    print(f"          {proto}://{host}:{config['port']}/agent/run")
    print()


def _run_gen_cert():
    script = Path(__file__).parent / "gen_cert.py"
    try:
        subprocess.run([sys.executable, str(script)], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  证书生成失败，可稍后重试")


# ── 子命令分发 ───────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="agent-easy-http v3.0 init wizard")
    parser.add_argument("--setup-hooks-only", action="store_true",
                        help="只跑 OpenClaw hooks 启用步骤（不动 config.json）")
    parser.add_argument("--check-hooks", action="store_true",
                        help="只检测 hooks 状态，不修改")
    parser.add_argument("--force-new-token", action="store_true",
                        help="强制重新生成 hooks.token（仅配合 --setup-hooks-only）")
    args = parser.parse_args()

    try:
        if args.check_hooks:
            print("📋 检测 OpenClaw hooks 状态...")
            result = ensure_hooks_enabled(interactive=False, read_only=True)
            print(f"\n  状态: {result['action']}")
            print(f"  消息: {result['message']}")
            if result.get("url"):
                print(f"  URL : {result['url']}")
            if result.get("token"):
                print(f"  Token: {result['token'][:8]}... (隐藏剩余)")
            sys.exit(0 if result["ok"] else 1)

        if args.setup_hooks_only:
            print("🔧 启用 OpenClaw hooks（独立模式）")
            print()
            result = ensure_hooks_enabled(interactive=True, force_new_token=args.force_new_token)
            print(f"\n  状态: {result['action']}")
            print(f"  消息: {result['message']}")
            if result.get("url"):
                print(f"  URL : {result['url']}")
            if result.get("token"):
                print(f"  Token: {result['token'][:8]}...")
            sys.exit(0 if result["ok"] else 1)

        # 默认：跑完整向导
        run_full_wizard()
    except KeyboardInterrupt:
        print("\n\n❌ 已取消")
        sys.exit(1)


if __name__ == "__main__":
    main()
