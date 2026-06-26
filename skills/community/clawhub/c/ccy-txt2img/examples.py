#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCY txt2img / smart_draw 使用示例
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from txt2img import text_to_image, create_code_image
from smart_draw import smart_draw, render_scene


def main():
    print("开始运行示例...")

    text_to_image(
        text="Hello World!\n这是一个文本转图片的示例",
        output_path="basic_example.png"
    )

    text_to_image(
        text="自定义样式示例\n支持多行文本和自定义颜色",
        output_path="custom_style.png",
        font_size=20,
        text_color="#2c3e50",
        background_color="#ecf0f1",
        width=500,
        height=300
    )

    create_code_image(
        "print('hello')\nprint('world')",
        output_path="code_example.png",
        theme="github"
    )

    smart_draw(
        "白色背景，一个蓝色圆，一个红色矩形，一条黑线，写上：你好，开发点点",
        "smart_draw_example.png"
    )

    smart_draw(
        "可爱的小猫咪，简笔画风格，粉色一点",
        "smart_draw_cat.png"
    )

    smart_draw(
        "现代办公室场景，有办公桌、电脑、椅子和台灯，写上：Office",
        "smart_draw_office.png"
    )

    scene = {
        "canvas": {"width": 900, "height": 500, "background": "#ffffff"},
        "layers": [
            {"type": "rect", "x": 60, "y": 60, "w": 220, "h": 140, "fill": "#E6F4FF", "stroke": "#1677ff", "stroke_width": 3},
            {"type": "circle", "cx": 420, "cy": 140, "r": 70, "fill": "#FFF1F0", "stroke": "#ff4d4f", "stroke_width": 3},
            {"type": "line", "x1": 80, "y1": 260, "x2": 820, "y2": 260, "stroke": "#222222", "stroke_width": 4},
            {"type": "text", "text": "中英文字测试 Hello 123", "x": 60, "y": 300, "w": 780, "h": 120, "font_size": 30, "color": "#111111"}
        ],
        "output": {"path": "scene_example.jpg", "format": "JPEG"}
    }
    render_scene(scene, output_path="scene_example.jpg", format="JPEG")

    print("示例完成，已生成:")
    for name in [
        "basic_example.png",
        "custom_style.png",
        "code_example.png",
        "smart_draw_example.png",
        "smart_draw_cat.png",
        "smart_draw_office.png",
        "scene_example.jpg",
    ]:
        print(f"- {name}")


if __name__ == "__main__":
    main()
