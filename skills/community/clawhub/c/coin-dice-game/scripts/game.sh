#!/bin/bash
# 抛硬币 & 猜骰子游戏 - 快捷脚本
# 用法: ./scripts/game.sh coin|dice

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

case "$1" in
  coin)
    RESULT=$(python3 "$SKILL_DIR/scripts/game.py" coin)
    LABEL=$(echo "$RESULT" | grep "^抛硬币结果：" | cut -d： -f2)
    IMG=$(echo "$RESULT" | grep "^图片：" | cut -d： -f2)
    echo "结果：$LABEL"
    echo "图片路径：$SKILL_DIR/assets/$IMG.jpg"
    echo "MEDIA:$SKILL_DIR/assets/$IMG.jpg"
    ;;
  dice)
    RESULT=$(python3 "$SKILL_DIR/scripts/game.py" dice)
    SIZE=$(echo "$RESULT" | grep "^骰子大小结果：" | cut -d： -f2)
    POINT=$(echo "$RESULT" | grep "^具体点数：" | cut -d： -f2)
    IMG=$(echo "$RESULT" | grep "^图片：" | cut -d： -f2)
    echo "结果：$SIZE"
    echo "点数：$POINT"
    echo "图片路径：$SKILL_DIR/assets/$IMG.jpg"
    echo "MEDIA:$SKILL_DIR/assets/$IMG.jpg"
    ;;
  *)
    echo "用法: $0 coin|dice"
    exit 1
    ;;
esac
