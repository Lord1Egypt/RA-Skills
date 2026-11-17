"""
生成参考板（reference board），用于图生图时的角色/场景参考。
支持 16:9（横版）和 9:16（竖版）两种比例。

16:9 布局（默认）：场景左 2/3 + 角色/troops 右 1/3 竖排
9:16 布局：场景上 65% + 角色/troops 下 35% 横向排列

用法:
  python make_ref_board.py \\
    --scene "images/scenes/城楼议事堂_中景.png" \\
    --char "images/characters/墨雪_front.png" "images/characters/墨将_front.png" \\
    --output "images/troops/ref_shot02_kf2.png"

  # 竖版（9:16）
  python make_ref_board.py --aspect 9:16 \\
    --scene "images/scenes/龙南战场_广角.png" \\
    --troop "images/troops/明军_front.png" "images/troops/蛮兵_front.png" \\
    --output "images/troops/ref_shot01_9x16.png"

或通过 --config 传入 JSON:
  python make_ref_board.py --config ref_config.json

配置格式 (JSON):
  {
    "aspect": "16:9",       # "16:9" 或 "9:16", 默认 "16:9"
    "scene": "images/scenes/城楼议事堂_中景.png",
    "characters": ["images/characters/墨雪_front.png"],
    "troops": ["images/troops/明军_front.png"],
    "output": "images/troops/ref_shot02_kf2.png"
  }
"""

import argparse
import json
import os
import sys
from PIL import Image

GAP = 6  # 间距


def make_ref_board_16x9(scene_path: str | None, asset_paths: list[str],
                         output_path: str):
    """16:9 横版参考板：场景左 2/3 + 角色/troops 右 1/3 竖排。"""
    W, H = 1280, 720
    scene_ratio = 2 / 3

    scene_w = int(W * scene_ratio)
    canvas = Image.new("RGB", (W, H), (60, 60, 60))

    # 场景图（自适应缩放铺满左 2/3）
    if scene_path and os.path.isfile(scene_path):
        scene = Image.open(scene_path).resize((scene_w, H), Image.LANCZOS)
        canvas.paste(scene, (0, 0))
    else:
        print(f"  [WARN] 场景图不存在或未指定: {scene_path}")

    if not asset_paths:
        canvas.save(output_path)
        print(f"  [OK] {output_path}（无角色参考，仅场景）")
        return

    # 角色/troops 图竖排右侧，高度均分 + 保持宽高比
    x, tw = scene_w + GAP, W - scene_w - GAP * 2
    n = len(asset_paths)
    spacing_total = (n - 1) * GAP
    each_h = (H - GAP * 2 - spacing_total) // n
    y = GAP

    for ap in asset_paths:
        if not os.path.isfile(ap):
            print(f"  [WARN] 资产图不存在: {ap}")
            continue
        img = Image.open(ap)
        ratio = min(tw / img.width, each_h / img.height)
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        if new_w < 1 or new_h < 1:
            continue
        img = img.resize((new_w, new_h), Image.LANCZOS)
        bg = Image.new("RGB", (tw, each_h), (0, 0, 0))
        bg.paste(img, ((tw - new_w) // 2, (each_h - new_h) // 2))
        canvas.paste(bg, (x, y))
        y += each_h + GAP

    canvas.save(output_path)
    print(f"  [OK] {output_path}")


def make_ref_board_9x16(scene_path: str | None, asset_paths: list[str],
                         output_path: str):
    """9:16 竖版参考板：场景上 65% + 角色/troops 下 35% 横向排列。"""
    W, H = 720, 1280
    scene_ratio = 0.65  # 场景占上部 65%

    scene_h = int(H * scene_ratio)
    canvas = Image.new("RGB", (W, H), (60, 60, 60))

    # 场景图（自适应缩放铺满上部）
    if scene_path and os.path.isfile(scene_path):
        scene = Image.open(scene_path).resize((W, scene_h), Image.LANCZOS)
        canvas.paste(scene, (0, 0))
    else:
        print(f"  [WARN] 场景图不存在或未指定: {scene_path}")

    if not asset_paths:
        canvas.save(output_path)
        print(f"  [OK] {output_path}（无角色参考，仅场景）")
        return

    # 角色/troops 图底部横向排列，宽度均分 + 保持宽高比
    bottom_y = scene_h + GAP
    bottom_h = H - bottom_y - GAP
    n = len(asset_paths)
    spacing_total = (n - 1) * GAP
    each_w = (W - GAP * 2 - spacing_total) // n
    x = GAP

    for ap in asset_paths:
        if not os.path.isfile(ap):
            print(f"  [WARN] 资产图不存在: {ap}")
            continue
        img = Image.open(ap)
        ratio = min(each_w / img.width, bottom_h / img.height)
        new_w = int(img.width * ratio)
        new_h = int(img.height * ratio)
        if new_w < 1 or new_h < 1:
            continue
        img = img.resize((new_w, new_h), Image.LANCZOS)
        bg = Image.new("RGB", (each_w, bottom_h), (0, 0, 0))
        bg.paste(img, ((each_w - new_w) // 2, (bottom_h - new_h) // 2))
        canvas.paste(bg, (x, bottom_y))
        x += each_w + GAP

    canvas.save(output_path)
    print(f"  [OK] {output_path}")


def main():
    parser = argparse.ArgumentParser(description="生成参考板（16:9 横版 / 9:16 竖版）")
    parser.add_argument("--config", help="JSON 配置文件路径")
    parser.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"],
                        help="参考板比例（默认: 16:9）")
    parser.add_argument("--scene", help="场景图路径")
    parser.add_argument("--char", nargs="*", default=[], help="角色图路径")
    parser.add_argument("--troop", nargs="*", default=[], help="兵种图路径")
    parser.add_argument("--output", required=True, help="输出 PNG 路径")

    args = parser.parse_args()

    scene_path = args.scene
    asset_paths = list(args.char or []) + list(args.troop or [])

    if args.config:
        with open(args.config, encoding="utf-8") as f:
            cfg = json.load(f)
        scene_path = cfg.get("scene")
        asset_paths = cfg.get("characters", []) + cfg.get("troops", [])
        args.aspect = cfg.get("aspect", args.aspect)

    if args.aspect == "9:16":
        make_ref_board_9x16(scene_path, asset_paths, args.output or cfg.get("output"))
    else:
        make_ref_board_16x9(scene_path, asset_paths, args.output or cfg.get("output"))


if __name__ == "__main__":
    main()
