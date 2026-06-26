"""配置向导 — 引导用户配置推送平台等选项"""

from pathlib import Path

PLATFORMS = [
    ("wechat", "微信", "通过微信发送PDF和摘要"),
    ("feishu", "飞书", "通过飞书发送PDF和摘要"),
    ("telegram", "Telegram", "通过Telegram发送PDF和摘要"),
    ("discord", "Discord", "通过Discord发送PDF和摘要"),
    ("slack", "Slack", "通过Slack发送PDF和摘要"),
    ("whatsapp", "WhatsApp", "通过WhatsApp发送PDF和摘要"),
    ("none", "不推送", "只在本地生成PDF，不推送到任何平台"),
]


def run_setup(skip_cookies: bool = False):
    """运行完整配置向导

    Args:
        skip_cookies: True 时跳过Cookie配置（已有Cookie的情况下）
    """
    print("=" * 50)
    print("  bilibili-reader 配置向导")
    print("=" * 50)

    env_path = Path(__file__).parent.parent / ".env"
    existing = _read_env(env_path)

    # 1. Cookie 配置
    if not skip_cookies:
        print("\n── 第 1 步：B站登录 ──\n")
        print("需要B站Cookie才能访问收藏夹。")
        print("  1. 扫码登录（推荐，自动获取Cookie）")
        print("  2. 手动配置（从浏览器F12复制）")
        print("  3. 跳过（已有Cookie）")

        choice = _ask_choice("请选择", ["1", "2", "3"], "1")
        if choice == "1":
            # 检查 playwright 是否安装
            try:
                import playwright
            except ImportError:
                print("\n  需要先安装 playwright：")
                print("    pip install playwright")
                print("    playwright install chromium")
                print()
                print("  安装完成后重新运行此命令")
                return
            from .auth import login_via_browser
            cookies = login_via_browser(save_to_env=True)
            if not cookies:
                print("登录失败，Cookie未更新")
        elif choice == "2":
            _manual_cookie_setup(existing, env_path)
        else:
            print("  跳过Cookie配置")
    else:
        print("\n── 跳过Cookie配置（已有） ──")

    # 2. 推送平台配置
    print("\n── 第 2 步：推送配置 ──\n")
    print("生成PDF后是否自动推送到聊天平台？\n")

    for i, (key, name, desc) in enumerate(PLATFORMS, 1):
        marker = " ← 当前" if existing.get("DELIVERY_PLATFORM", "none") == key else ""
        print(f"  {i}. {name} — {desc}{marker}")

    choice = _ask_choice(
        "\n请选择平台",
        [str(i) for i in range(1, len(PLATFORMS) + 1)],
        "7",
    )
    platform_key, platform_name, _ = PLATFORMS[int(choice) - 1]

    # 3. 保存配置
    existing["DELIVERY_PLATFORM"] = platform_key
    existing.pop("DELIVERY_TARGET", None)
    _write_env(env_path, existing)

    print(f"\n{'='*50}")
    print(f"  配置完成!")
    print(f"{'='*50}")
    print(f"\n  推送平台: {platform_name}")
    print(f"  推送目标: 由 agent 默认对话决定")
    print(f"\n  配置文件: {env_path}")
    print(f"  修改配置: python -m src --config")
    print()


def _manual_cookie_setup(existing: dict, env_path: Path):
    """手动Cookie配置"""
    print("\n  请从浏览器获取Cookie：")
    print("  1. 登录 bilibili.com")
    print("  2. 按 F12 → Application → Cookies → bilibili.com")
    print("  3. 复制以下三个值：\n")

    for key, name in [
        ("BILIBILI_SESSDATA", "SESSDATA"),
        ("BILIBILI_BILI_JCT", "bili_jct"),
        ("BILIBILI_BUVID3", "buvid3"),
    ]:
        current = existing.get(key, "")
        if current:
            print(f"  {name} (当前: {current[:20]}...，留空不修改)")
        value = input(f"  {name}: ").strip()
        if value:
            existing[key] = value

    _write_env(env_path, existing)
    print("\n  Cookie已保存")


def _ask_choice(prompt: str, valid: list[str], default: str) -> str:
    """询问用户选择"""
    while True:
        choice = input(f"  {prompt} [{default}]: ").strip() or default
        if choice in valid:
            return choice
        print(f"  请输入 {'/'.join(valid)}")


def _read_env(env_path: Path) -> dict:
    """读取.env文件"""
    existing = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, _, value = line.partition("=")
                    existing[key.strip()] = value.strip()
    return existing


def _write_env(env_path: Path, data: dict):
    """写入.env文件"""
    with open(env_path, "w", encoding="utf-8") as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")


if __name__ == "__main__":
    run_setup()
