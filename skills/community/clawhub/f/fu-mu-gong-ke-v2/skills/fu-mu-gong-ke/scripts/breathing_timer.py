#!/usr/bin/env python3
"""
父母的功课 - 呼吸平静练习
科学证明的放松呼吸技术：4-7-8呼吸法

用法:
    python3 scripts/breathing_timer.py          # 4-7-8呼吸法 (4分钟)
    python3 scripts/breathing_timer.py 2       # 指定分钟数
    python3 scripts/breathing_timer.py --box  # 方框呼吸法 (4-4-4-4)
    python3 scripts/breathing_timer.py --calm  # 放松呼吸 (4-4)
"""

import sys
import time
import os

# ANSI颜色码
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'
CLEAR = '\033[2J'
HOME = '\033[H'


def clear_screen():
    print(CLEAR + HOME, end='')


def print_centered(text, width=None):
    if width is None:
        try:
            size = os.get_terminal_size()
            width = size.columns
        except OSError:
            width = 80
    print(text.center(width))


def print_big(text):
    """大字体显示（终端ASCII艺术风格）"""
    clear_screen()
    print(f"\n\n{BOLD}{BLUE}")
    print_centered("═══════════════════════════════")
    print_centered(f"  {text}")
    print_centered("═══════════════════════════════")
    print(f"{RESET}\n")


def breathing_cycle(inhale, hold1, exhale, hold2=0, cycles=4, label=""):
    """执行一个呼吸周期"""
    total = (inhale + hold1 + exhale + hold2) * cycles
    start = time.time()
    cycle_num = 0

    for cycle in range(cycles):
        cycle_num += 1
        remaining = total - (time.time() - start)
        if remaining < 0:
            break

        # 吸气
        print_big(f"吸气 {inhale}秒")
        print_centered(f"第 {cycle_num}/{cycles} 次循环")
        print_centered(f"剩余时间: {int(remaining)}秒")
        print(f"\n{GREEN}")
        print_centered("━━━" * (inhale * 3))
        print(f"{RESET}")
        time.sleep(inhale)

        if remaining <= 0:
            break

        # 屏息1
        if hold1 > 0:
            print_big(f"屏息 {hold1}秒")
            print_centered(f"第 {cycle_num}/{cycles} 次循环")
            print_centered(f"剩余时间: {int(remaining)}秒")
            print(f"\n{YELLOW}")
            print_centered("● ● ●" * hold1)
            print(f"{RESET}")
            time.sleep(hold1)

        if remaining <= 0:
            break

        # 呼气
        if exhale > 0:
            print_big(f"呼气 {exhale}秒")
            print_centered(f"第 {cycle_num}/{cycles} 次循环")
            print_centered(f"剩余时间: {int(remaining)}秒")
            print(f"\n{RED}")
            print_centered("○ ○ ○" * (exhale * 2))
            print(f"{RESET}")
            time.sleep(exhale)

        if remaining <= 0:
            break

        # 屏息2
        if hold2 > 0:
            print_big(f"保持 {hold2}秒")
            print_centered(f"第 {cycle_num}/{cycles} 次循环")
            time.sleep(hold2)

    clear_screen()


def method_478(cycles=4):
    """4-7-8呼吸法 - 最有效的放松技术"""
    print(f"\n{BOLD}4-7-8 呼吸法{RESET}")
    print("源于瑜伽，用于激活副交感神经系统")
    print("吸气4秒 → 屏息7秒 → 呼气8秒 → 循环4次\n")
    print("准备好后按Enter开始...")
    input()
    breathing_cycle(inhale=4, hold1=7, exhale=8, hold2=0, cycles=cycles)


def method_box(cycles=6):
    """方框呼吸法 - 常用于减压和焦虑缓解"""
    print(f"\n{BOLD}方框呼吸法 (Box Breathing){RESET}")
    print("海军海豹突击队用于高压环境下的冷静")
    print("吸气4秒 → 屏息4秒 → 呼气4秒 → 屏息4秒 → 循环6次\n")
    print("准备好后按Enter开始...")
    input()
    breathing_cycle(inhale=4, hold1=4, exhale=4, hold2=4, cycles=cycles)


def method_calm(cycles=8):
    """放松呼吸 - 简单的4-4呼吸"""
    print(f"\n{BOLD}放松呼吸 (4-4 呼吸){RESET}")
    print("最简单的平静技术，随时可用")
    print("吸气4秒 → 呼气4秒 → 循环8次\n")
    print("准备好后按Enter开始...")
    input()
    breathing_cycle(inhale=4, hold1=0, exhale=4, hold2=0, cycles=cycles)


def method_custom(inhale=4, hold1=4, exhale=4, hold2=0, cycles=6):
    """自定义呼吸法"""
    print(f"\n{BOLD}自定义呼吸法{RESET}")
    print(f"吸气{inhale}秒 → 屏息{hold1}秒 → 呼气{exhale}秒 → 屏息{hold2}秒")
    print(f"循环{cycles}次\n")
    print("准备好后按Enter开始...")
    input()
    breathing_cycle(inhale=inhale, hold1=hold1, exhale=exhale, hold2=hold2, cycles=cycles)


def completion_message():
    clear_screen()
    print(f"\n\n{GREEN}{BOLD}")
    print_centered("═══════════════════════════════")
    print_centered("  ✓ 练习完成")
    print_centered("═══════════════════════════════")
    print(f"{RESET}\n")
    print_centered("你做到了。")
    print_centered("呼吸是身体唯一的自主可控放松开关。")
    print_centered("当孩子让你崩溃时，先呼吸。")
    print("\n")


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        method_478(cycles=4)
    elif "--help" in args or "-h" in args:
        print(__doc__)
        return
    elif args[0] == "--box":
        method_box()
    elif args[0] == "--calm":
        method_calm()
    elif args[0] == "--478":
        method_478()
    else:
        try:
            minutes = int(args[0])
            # 根据分钟数调整循环次数
            # 4-7-8总时长约19秒/次, 4分钟约12次, 但质量比数量重要
            cycles = min(8, max(3, minutes // 1))
            method_478(cycles=cycles)
        except ValueError:
            print("未知参数。使用 --help 查看用法。")
            return

    completion_message()


if __name__ == "__main__":
    main()
