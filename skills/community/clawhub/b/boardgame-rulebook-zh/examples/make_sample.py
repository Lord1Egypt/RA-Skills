#!/usr/bin/env python3
"""Build a small, synthetic two-column rulebook used by the self-test and demo."""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict

import fitz
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent


def make_assets(asset_dir: Path) -> Dict[str, str]:
    asset_dir.mkdir(parents=True, exist_ok=True)
    board_path = asset_dir / "board.png"
    icon_path = asset_dir / "icon.png"
    if not board_path.exists():
        image = Image.new("RGB", (600, 400), (245, 240, 230))
        draw = ImageDraw.Draw(image)
        colors = ["#e76f51", "#f4a261", "#e9c46a", "#2a9d8f", "#264653"]
        for index in range(5):
            cx = 120 + 90 * index
            cy = 200 + (index % 2) * 40
            points = [
                (cx + 70 * math.cos(math.radians(60 * k)),
                 cy + 70 * math.sin(math.radians(60 * k)))
                for k in range(6)
            ]
            draw.polygon(points, fill=colors[index])
            draw.line(points + [points[0]], fill="white", width=4)
        draw.ellipse((60, 300, 120, 360), fill="white", outline="#333333", width=3)
        image.save(board_path)
    if not icon_path.exists():
        image = Image.new("RGB", (60, 60), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((6, 6, 54, 54), fill="#2a9d8f")
        draw.text((22, 18), "E", fill="white")
        image.save(icon_path)
    return {"board": str(board_path), "icon": str(icon_path)}


def build_pdf(pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    assets = make_assets(pdf_path.parent / "assets")
    doc = fitz.open()

    page = doc.new_page(width=595, height=842)
    page.draw_rect(fitz.Rect(0, 0, 595, 38), color=None, fill=(38/255, 70/255, 83/255))
    page.insert_text((40, 25), "STARFALL EXPEDITION", fontsize=16,
                     color=(1, 1, 1), fontname="hebo")
    page.insert_text((475, 25), "RULEBOOK", fontsize=8, color=(1, 1, 1))
    page.insert_text((50, 75), "A cooperative tile-laying adventure",
                     fontsize=10, color=(0.3, 0.3, 0.3))

    page.insert_text((50, 120), "SETUP", fontsize=16, fontname="hebo")
    page.insert_textbox(
        fitz.Rect(50, 132, 280, 210),
        "Place the board in the center of the table. Each player takes 1 player "
        "board and 2 meeples. Shuffle the deck and deal 3 cards to each player.",
        fontsize=9.5, lineheight=1.35, fontname="helv",
    )
    page.draw_rect(fitz.Rect(50, 225, 280, 290), color=None, fill=(252/255, 235/255, 200/255))
    page.insert_text((60, 245), "IMPORTANT", fontsize=9, fontname="hebo")
    page.insert_textbox(
        fitz.Rect(60, 250, 270, 285),
        "The active player draws 1 card at the start of each turn.",
        fontsize=9, lineheight=1.35, fontname="helv",
    )
    page.insert_text((50, 315), "On your turn:", fontsize=9.5, fontname="hebo")
    page.insert_text((60, 335), "- Gain 2 resources.", fontsize=9.5)
    page.insert_text((60, 353), "- Place 1 worker on an adjacent space.", fontsize=9.5)
    page.insert_text((60, 371), "- Draw 1 card, then discard 1 card.", fontsize=9.5)
    page.insert_text((50, 405), "Gain         2 energy, then place a meeple.", fontsize=9.5)
    page.insert_image(fitz.Rect(82, 394, 104, 412), filename=assets["icon"])

    page.insert_text((315, 120), "HOW TO PLAY", fontsize=16, fontname="hebo")
    page.insert_textbox(
        fitz.Rect(315, 132, 545, 195),
        "On your turn, you may place a worker or play a card. If you place a "
        "worker, resolve its action immediately.",
        fontsize=9.5, lineheight=1.35, fontname="helv",
    )

    x0, y0 = 315, 220
    cols = [315, 390, 465, 545]
    rows = [220, 260, 300, 340]
    for x in cols:
        page.draw_line((x, y0), (x, rows[-1]))
    for y in rows:
        page.draw_line((x0, y), (cols[-1], y))
    cells = [
        ["Resource", "Cost", "Effect"],
        ["Wood", "2", "Gain 1 VP"],
        ["Stone", "3", "Draw 1 card"],
    ]
    for row_index, row in enumerate(cells):
        for col_index, text in enumerate(row):
            page.insert_text(
                (cols[col_index] + 7, rows[row_index] + 24), text, fontsize=9.5,
                fontname="hebo" if row_index == 0 else "helv",
            )

    page.insert_image(fitz.Rect(315, 370, 545, 520), filename=assets["board"])
    page.insert_text((365, 540), "Example: a completed board.", fontsize=9)
    page.insert_text((500, 815), "Page 1", fontsize=8, color=(0.35, 0.35, 0.35))

    page2 = doc.new_page(width=595, height=842)
    page2.insert_text((50, 80), "SCORING", fontsize=20, fontname="hebo")
    page2.insert_textbox(
        fitz.Rect(50, 100, 545, 190),
        "At the end of the game, score 1 victory point for each adjacent pair of "
        "matching tiles. The player with the most victory points wins. In case of "
        "a tie, the player who placed the most workers wins.",
        fontsize=10, lineheight=1.4, fontname="helv",
    )
    page2.insert_text((50, 220), "End-game bonuses", fontsize=12, fontname="hebo")
    for index, text in enumerate([
        "1. Each completed set: 3 points.",
        "2. Each remaining coin: 1 point.",
        "3. Each unused worker: 0 points.",
    ]):
        page2.insert_text((60, 245 + index * 20), text, fontsize=10)
    page2.insert_image(fitz.Rect(330, 220, 545, 420), filename=assets["board"])
    page2.insert_text((360, 440), "A scoring example.", fontsize=9)
    # A small vector icon inside a text line (tests vector-art obstacle handling).
    page2.insert_text((50, 520), "Place a worker on any       space.", fontsize=10)
    page2.draw_circle(fitz.Point(175, 516), 7, color=None, fill=(231/255, 111/255, 81/255))
    page2.insert_text((500, 815), "Page 2", fontsize=8, color=(0.35, 0.35, 0.35))

    doc.save(str(pdf_path), garbage=4, deflate=True)
    doc.close()


SAMPLE_TRANSLATIONS = {
    "STARFALL EXPEDITION": "星陨远征",
    "RULEBOOK": "规则书",
    "A cooperative tile-laying adventure": "一场合作式板块拼放冒险",
    "SETUP": "游戏准备",
    "Place the board in the center of the table. Each player takes 1 player board and 2 meeples. Shuffle the deck and deal 3 cards to each player.":
        "将游戏版图放在桌面中央。每名玩家拿取1块玩家版图和2个米宝。洗混牌库，然后向每名玩家发3张牌。",
    "IMPORTANT": "重要",
    "The active player draws 1 card at the start of each turn.":
        "当前玩家在每个回合开始时抽1张牌。",
    "On your turn:": "在你的回合中：",
    "- Gain 2 resources.": "• 获得2个资源。",
    "- Place 1 worker on an adjacent space.": "• 在相邻格放置1名工人。",
    "- Draw 1 card, then discard 1 card.": "• 抽1张牌，然后弃置1张牌。",
    "Gain 2 energy, then place a meeple.": "获得2点能量，然后放置1个米宝。",
    "HOW TO PLAY": "游戏流程",
    "On your turn, you may place a worker or play a card. If you place a worker, resolve its action immediately.":
        "在你的回合中，你可以放置1名工人或打出1张牌。若你放置工人，则立即结算其行动。",
    "Resource": "资源",
    "Cost": "费用",
    "Effect": "效果",
    "Wood": "木材",
    "2": "2",
    "Gain 1 VP": "获得1胜利点",
    "Stone": "石材",
    "3": "3",
    "Draw 1 card": "抽1张牌",
    "Example: a completed board.": "示例：一块完成的版图。",
    "Page 1": "第1页",
    "SCORING": "计分",
    "At the end of the game, score 1 victory point for each adjacent pair of matching tiles. The player with the most victory points wins. In case of a tie, the player who placed the most workers wins.":
        "游戏结束时，每对相邻的相同板块计1胜利点。拥有最多胜利点的玩家获胜。若出现平局，则放置工人最多的玩家获胜。",
    "End-game bonuses": "终局加成",
    "1. Each completed set: 3 points.": "1. 每套完成的成套收集：3分。",
    "2. Each remaining coin: 1 point.": "2. 每枚剩余的金币：1分。",
    "3. Each unused worker: 0 points.": "3. 每名未使用的工人：0分。",
    "A scoring example.": "一个计分示例。",
    "Place a worker on any space.": "在任意格放置1名工人。",
    "Page 2": "第2页",
}


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "_out" / "sample.pdf"
    build_pdf(out)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
