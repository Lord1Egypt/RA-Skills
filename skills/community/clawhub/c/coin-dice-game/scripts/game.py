#!/usr/bin/env python3
"""
抛硬币 & 猜骰子大小 游戏引擎
随机生成结果并返回对应的图片索引
"""

import random
import sys

IMAGE_MAP = {
    "coin": {
        0: {"label": "正", "image": "正面"},
        1: {"label": "反", "image": "反面"},
    },
    "dice": {
        "big":  {0: {"label": "4", "image": "4"},
                 1: {"label": "5", "image": "5"},
                 2: {"label": "6", "image": "6"}},
        "small": {0: {"label": "1", "image": "1"},
                  1: {"label": "2", "image": "2"},
                  2: {"label": "3", "image": "3"}},
    }
}

def flip_coin():
    """抛硬币：返回 0=正 或 1=反"""
    result = random.randint(0, 1)
    return {
        "type": "coin",
        "result_raw": result,
        "result_label": IMAGE_MAP["coin"][result]["label"],
        "result_image": IMAGE_MAP["coin"][result]["image"],
    }

def roll_dice():
    """猜骰子大小：
       0=大(4-6), 1=小(1-3)
       然后在大/小范围内随机选一个具体数字
    """
    size = random.randint(0, 1)  # 0=大, 1=小
    if size == 0:
        size_label = "大"
        detail = random.randint(0, 2)  # 4, 5, 6
        entry = IMAGE_MAP["dice"]["big"][detail]
    else:
        size_label = "小"
        detail = random.randint(0, 2)  # 1, 2, 3
        entry = IMAGE_MAP["dice"]["small"][detail]

    return {
        "type": "dice",
        "result_raw": size,
        "result_label": size_label,
        "detail_label": entry["label"],
        "detail_image": entry["image"],
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 game.py <coin|dice>", file=sys.stderr)
        sys.exit(1)

    game_type = sys.argv[1].lower()
    if game_type == "coin":
        result = flip_coin()
        print(f"抛硬币结果：{result['result_label']}")
        print(f"图片：{result['result_image']}")
    elif game_type == "dice":
        result = roll_dice()
        print(f"骰子大小结果：{result['result_label']}")
        print(f"具体点数：{result['detail_label']}")
        print(f"图片：{result['detail_image']}")
    else:
        print(f"未知游戏类型：{game_type}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
