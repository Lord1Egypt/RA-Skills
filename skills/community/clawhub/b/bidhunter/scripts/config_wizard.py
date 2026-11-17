#!/usr/bin/env python3
"""
config_wizard.py — BidHunter v1.2 推送通道交互式配置向导

用法:
  python3 config_wizard.py            # 交互式配置
  python3 config_wizard.py --show     # 查看当前配置（脱敏）
  python3 config_wizard.py --reset    # 清除配置

规则:
  - 未通过连通性测试，不允许写入配置
  - 配置文件: ~/.config/bidhunter/push.json，权限 600
  - 通道优先级: 🥇 钉钉 → 🥈 企微 → 📧 邮件兜底（飞书 v1.5 再加）
"""

import json
import os
import stat
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.expanduser("~/.config/bidhunter")
CONFIG_PATH = os.path.join(CONFIG_DIR, "push.json")

sys.path.insert(0, SCRIPT_DIR)
import push_manager  # noqa: E402

EMPTY = {"version": 1, "channels": {}}


def _mask(s, keep=8):
    if not s:
        return "(空)"
    return s[:keep] + "..." if len(s) > keep else "***"


def load_current():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ 现有配置损坏，将重建")
    return json.loads(json.dumps(EMPTY))


def save(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.chmod(CONFIG_PATH, stat.S_IRUSR | stat.S_IWUSR)  # 600
    print(f"\n✅ 配置已写入 {CONFIG_PATH}（权限 600）")


def test_channel(ch, ch_cfg):
    try:
        ok, err = push_manager.SENDERS[ch](ch_cfg, "[BidHunter] 配置向导测试",
                                           "若看到此消息，说明通道配置成功 ✅")
    except Exception as e:  # noqa: BLE001
        ok, err = False, str(e)[:200]
    print(f"  连通性测试: {'✅ 通过' if ok else '❌ 失败 — ' + err}")
    return ok


def ask(prompt, default="", required=True, secret=False):
    while True:
        suffix = f" [{_mask(default)}]" if default else ""
        val = input(f"{prompt}{suffix}: ").strip()
        if not val:
            if default:
                return default
            if not required:
                return ""
            print("  （必填，请重新输入）")
            continue
        return val


def wizard_dingtalk(existing):
    print("\n--- 🥇 钉钉自定义机器人 ---")
    print("群设置 → 智能群助手 → 添加机器人 → 自定义 → 获取 Webhook；安全设置选「加签」")
    webhook = ask("Webhook", existing.get("webhook", ""))
    secret = ask("加签密钥 SEC（未开启加签可回车跳过）",
                 existing.get("secret", ""), required=False)
    cfg = {"enabled": True, "webhook": webhook}
    if secret:
        cfg["secret"] = secret
    if not test_channel("dingtalk", cfg):
        print("  ❌ 未通过连通性测试，本通道不写入。")
        return None
    return cfg


def wizard_wecom(existing):
    print("\n--- 🥈 企业微信群机器人 ---")
    print("群聊 → 右上角「···」→ 群机器人 → 添加 → 复制 Webhook 地址")
    webhook = ask("Webhook", existing.get("webhook", ""))
    cfg = {"enabled": True, "webhook": webhook}
    if not test_channel("wecom", cfg):
        print("  ❌ 未通过连通性测试，本通道不写入。")
        return None
    return cfg


def wizard_email(existing):
    print("\n--- 📧 邮件兜底（SMTP）---")
    print("QQ邮箱: smtp.qq.com:465，密码填「授权码」（设置→账户→POP3/SMTP 开启后生成）")
    host = ask("SMTP 主机", existing.get("host", ""))
    port = ask("端口", str(existing.get("port", 465)))
    user = ask("发件邮箱", existing.get("user", ""))
    password = ask("密码/授权码", existing.get("password", ""))
    to = ask("收件邮箱", existing.get("to", user))
    try:
        port = int(port)
    except ValueError:
        print("  ❌ 端口必须是数字"); return None
    cfg = {"enabled": True, "host": host, "port": port,
           "user": user, "password": password, "to": to}
    if not test_channel("email", cfg):
        print("  ❌ 未通过连通性测试，本通道不写入。")
        return None
    return cfg


WIZARDS = {"dingtalk": wizard_dingtalk, "wecom": wizard_wecom, "email": wizard_email}


def show():
    cfg = load_current()
    chs = cfg.get("channels") or {}
    if not chs:
        print("尚未配置任何通道。直接运行: python3 config_wizard.py")
        return
    for name, c in chs.items():
        print(f"\n[{name}] enabled={c.get('enabled')}")
        for k, v in c.items():
            if k in ("password", "secret"):
                print(f"  {k}: ***")
            elif k == "webhook":
                print(f"  {k}: {_mask(v, 32)}")
            else:
                print(f"  {k}: {v}")


def main():
    if "--show" in sys.argv:
        show(); return
    if "--reset" in sys.argv:
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
            print("已清除配置")
        else:
            print("无配置可清除")
        return

    print("=== BidHunter 推送通道配置向导 ===")
    print("未通过连通性测试的通道不会写入配置。")
    cfg = load_current()

    while True:
        chs = cfg.get("channels", {})
        status = ", ".join(f"{k}{'' if v.get('enabled') else '(停)'}"
                           for k, v in chs.items()) or "(空)"
        print(f"\n当前已配置: {status}")
        print("1) 钉钉  2) 企微  3) 邮件  4) 完成退出  5) 查看配置")
        choice = input("选择通道 [1-5]: ").strip()
        if choice == "4":
            break
        if choice == "5":
            show(); continue
        name = {"1": "dingtalk", "2": "wecom", "3": "email"}.get(choice)
        if not name:
            print("无效选择"); continue
        result = WIZARDS[name](chs.get(name, {}))
        if result:
            cfg.setdefault("channels", {})[name] = result
            save(cfg)

    if not cfg.get("channels"):
        print("\n未配置任何通道，退出。")
    else:
        print("\n配置完成！用以下命令验证:")
        print("  python3 push_manager.py test")
        print("  python3 push_manager.py history")


if __name__ == "__main__":
    main()
