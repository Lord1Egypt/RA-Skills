"""Interactive terminal menu."""

from __future__ import annotations


def show_menu(installed: list, *, allow_all: bool = True):
    """交互式菜单。返回 Agent 实例 / 'all' / None(退出)。"""
    print("\n🔍 选择你要查看的 AI 助手：")
    print("─" * 40)
    for i, cls in enumerate(installed, 1):
        print(f"  [{i}] {cls.display_name()}")
    if allow_all:
        print("  [a] 所有")
    print("  [q] 退出")
    print("─" * 40)

    while True:
        try:
            try:
                choice = input("请选择：").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            if choice == "q":
                return None
            if allow_all and choice == "a":
                return "all"
            idx = int(choice) - 1
            if 0 <= idx < len(installed):
                return installed[idx]()
            valid = f"1-{len(installed)}"
            if allow_all:
                valid += "、a"
            valid += " 或 q"
            print(f"请输入 {valid}")
        except (ValueError, EOFError):
            valid = f"1-{len(installed)}"
            if allow_all:
                valid += "、a"
            valid += " 或 q"
            print(f"请输入 {valid}")
