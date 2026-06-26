#!/bin/bash

# Скрипт установки reference-creator skill в OpenClaw

set -e

echo "=== Reference Creator Skill Installer ==="
echo ""

# Определяем путь к OpenClaw KB
if [ -z "$OPENCLAW_KB" ]; then
    # Пытаемся найти OpenClaw KB автоматически
    if [ -d "OpenClaw KB" ]; then
        OPENCLAW_KB="OpenClaw KB"
    elif [ -d "../OpenClaw KB" ]; then
        OPENCLAW_KB="../OpenClaw KB"
    elif [ -d "../../OpenClaw KB" ]; then
        OPENCLAW_KB="../../OpenClaw KB"
    else
        echo "Ошибка: Не могу найти директорию 'OpenClaw KB'"
        echo "Установите переменную окружения OPENCLAW_KB или запустите из директории проекта"
        echo ""
        echo "Пример:"
        echo "  export OPENCLAW_KB=/path/to/OpenClaw\\ KB"
        echo "  ./install.sh"
        exit 1
    fi
fi

TARGET_DIR="$OPENCLAW_KB/skills/reference-creator"

echo "Целевая директория: $TARGET_DIR"
echo ""

# Создаём директорию если её нет
if [ ! -d "$TARGET_DIR" ]; then
    echo "Создаю директорию: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
else
    echo "Директория уже существует: $TARGET_DIR"
    read -p "Перезаписать? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Установка отменена"
        exit 0
    fi
fi

# Копируем файлы
echo "Копирую файлы..."
cp SKILL.md "$TARGET_DIR/"
cp LICENSE.txt "$TARGET_DIR/"
cp README.md "$TARGET_DIR/"

echo ""
echo "✓ Скилл успешно установлен!"
echo ""
echo "Следующие шаги:"
echo "1. Назначьте скилл агенту в его SOUL.md:"
echo "   Skills:"
echo "   - reference-creator"
echo ""
echo "2. Или добавьте в agent spec:"
echo "   skills:"
echo "     - reference-creator"
echo ""
echo "Готово!"
