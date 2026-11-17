#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py —— 秽土转生技能配置读写（用户侧「设置」指令的底层实现）

用法（由 SKILL.md 的「设置」动词调用）:
    python config.py get <key>
    python config.py set <key> <value>
    python config.py reset <key>
    python config.py list

配置落点（两层，刻意分离，确保技能包发布时绝不携带个人路径）：
  - 出厂默认：技能根目录的 config.yaml（随技能包发布，只含说明，不含任何个人路径）
  - 个人配置：用户主目录 ~/.edo-tensei/config.yaml（由「设置」写入，不进技能包）
    —— 因此 Windows / macOS / Linux / 云端会话 均不会泄露本地绝对路径，
       也不会因不同平台的绝对路径错位而失效。

读取优先级：个人配置 > 出厂默认；两者皆空时回退到 APP_DEFAULT_EXPORT_DIR。
零配置时 export_dir 回退到 <用户主目录>/.edo-tensei/exports。

说明：为免依赖 PyYAML，这里用极简 flat `key: value` 读写；仅支持简单标量值。
"""

import os
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _guard_not_skill_pkg(path: str, label: str):
    """安全硬闸（§〇 安全铁律）：禁止任何写盘路径落在技能包目录（~/.workbuddy/skills/）下。
    动词脚本绝不修改技能包自身；命中立即 abort。"""
    p = os.path.abspath(os.path.expanduser(path)).replace("\\", "/").lower()
    skills = os.path.abspath(os.path.expanduser("~/.workbuddy/skills")).replace("\\", "/").lower()
    if p == skills or p.startswith(skills + "/"):
        print(f"[安全闸·拒绝] {label} 目标路径落在技能包目录内：{p}\n"
              f"        本技能的动词脚本禁止写入/修改技能包自身（~/.workbuddy/skills/）。\n"
              f"        若你确需改包，请直接编辑文件，不要通过动词脚本代劳。", file=sys.stderr)
        sys.exit(2)
# 出厂默认配置（随技能包发布，绝不含个人路径）
BUNDLED_CONFIG = os.path.join(SKILL_ROOT, "config.yaml")
# 个人配置（存于用户主目录，绝不进入技能包）
USER_CONFIG_DIR = os.path.expanduser("~/.edo-tensei")
USER_CONFIG = os.path.join(USER_CONFIG_DIR, "config.yaml")

# 应用默认导出目录（~ 在任意平台自动解析为主目录）
APP_DEFAULT_EXPORT_DIR = os.path.join(os.path.expanduser("~"), ".edo-tensei", "exports")

DEFAULTS = {
    "export_dir": APP_DEFAULT_EXPORT_DIR,
    "context_depth": "standard",  # minimal | standard | full
}

# 上下文深度合法值（控制转生/导出的交接文档与导出包内联信息量）
ALLOWED_DEPTHS = ("minimal", "standard", "full")


def _parse(path: str) -> dict:
    cfg = {}
    if not os.path.isfile(path):
        return cfg
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if k:
                # 空值视为「未设置」，交由上层回退默认
                cfg[k] = v
    return cfg


def _read() -> dict:
    """出厂默认 ← 出厂 config.yaml ← 个人 config.yaml（后者优先）"""
    cfg = dict(DEFAULTS)
    cfg.update(_parse(BUNDLED_CONFIG))
    cfg.update(_parse(USER_CONFIG))
    # 空字符串视为未设置，回退到默认值
    for k in list(cfg.keys()):
        if cfg[k] == "":
            cfg[k] = DEFAULTS.get(k, "")
    return cfg


def get_export_dir() -> str:
    """返回生效的导出目录（已展开 ~、绝对化）。"""
    d = _read().get("export_dir", "") or APP_DEFAULT_EXPORT_DIR
    d = os.path.expanduser(d)
    return os.path.abspath(d) if not os.path.isabs(d) else d


def get_context_depth() -> str:
    """返回生效的上下文深度（已校验合法，默认 standard）。"""
    d = _read().get("context_depth", "") or "standard"
    return d if d in ALLOWED_DEPTHS else "standard"


def _write_user(cfg: dict) -> None:
    _guard_not_skill_pkg(USER_CONFIG, "个人配置文件")
    os.makedirs(USER_CONFIG_DIR, exist_ok=True)
    with open(USER_CONFIG, "w", encoding="utf-8") as f:
        f.write("# 秽土转生 · 个人配置（由「设置」指令写入，存于用户主目录，不随技能包发布）\n")
        for k in sorted(cfg.keys()):
            f.write(f"{k}: {cfg[k]}\n")


def get(key: str):
    return _read().get(key)


def set_key(key: str, value: str) -> None:
    # 只动「个人配置」，绝不修改出厂 config.yaml —— 保证技能包干净
    if key == "context_depth" and value not in ALLOWED_DEPTHS:
        print(f"[错误] context_depth 仅允许: {', '.join(ALLOWED_DEPTHS)}（你给了: {value}）")
        sys.exit(1)
    cfg = _parse(USER_CONFIG)
    if key == "export_dir" and value:
        os.makedirs(os.path.expanduser(value), exist_ok=True)
    cfg[key] = value
    _write_user(cfg)


def reset_key(key: str) -> None:
    cfg = _parse(USER_CONFIG)
    if key in cfg:
        del cfg[key]
        _write_user(cfg)


def list_all() -> dict:
    return _read()


def main():
    # H3 加载验签（密钥门禁）：技能包 SEAL 被篡改或缺失签名则拒绝执行
    try:
        sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))
        import maintenance_lock
        if not maintenance_lock.verify_seal(SKILL_ROOT):
            print("[门禁·拒绝] 技能包 SEAL 验签失败（缺签名/被篡改），拒绝执行。", file=sys.stderr)
            sys.exit(1)
    except Exception as _e:
        print("[门禁·警告] 验签跳过（%s）；若这是已发布包请检查 assets/pubkey.pem 与 provenance/SEAL.json。" % _e, file=sys.stderr)
    if len(sys.argv) < 2:
        print("用法: config.py [get <key>|set <key> <value>|reset <key>|list]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "get":
        key = sys.argv[2] if len(sys.argv) > 2 else "export_dir"
        print(_read().get(key, ""))
    elif cmd == "set":
        if len(sys.argv) < 4:
            print("[错误] set 需要 <key> <value>")
            sys.exit(1)
        set_key(sys.argv[2], sys.argv[3])
        print(f"[OK] {sys.argv[2]} = {sys.argv[3]}（已写入个人配置 {USER_CONFIG}）")
    elif cmd == "reset":
        key = sys.argv[2] if len(sys.argv) > 2 else "export_dir"
        reset_key(key)
        print(f"[OK] 已重置 {key}（回退默认: {DEFAULTS.get(key, '')}）")
    elif cmd == "list":
        eff = _read()
        print(f"# 生效配置（个人配置 {USER_CONFIG} 优先于出厂默认）")
        for k, v in sorted(eff.items()):
            print(f"{k}: {v}")
    else:
        print(f"[错误] 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
