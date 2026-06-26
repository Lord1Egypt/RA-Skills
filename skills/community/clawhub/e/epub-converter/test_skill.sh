#!/bin/bash
# EPUB Converter Skill 测试脚本

echo "🧪 测试 EPUB Converter Skill"
echo "================================"

# 检查脚本是否存在
if [ ! -f "scripts/convert_epub.py" ]; then
    echo "❌ 脚本文件不存在"
    exit 1
fi
echo "✅ 脚本文件存在"

# 检查脚本是否可执行
if [ ! -x "scripts/convert_epub.py" ]; then
    echo "⚠️  脚本不可执行，正在添加执行权限..."
    chmod +x scripts/convert_epub.py
fi
echo "✅ 脚本可执行"

# 检查帮助信息
echo ""
echo "📖 测试帮助信息："
python3 scripts/convert_epub.py --help | head -10

# 检查虚拟环境
if [ -d "$HOME/.openclaw/epub_venv" ]; then
    echo ""
    echo "✅ 虚拟环境已存在: ~/.openclaw/epub_venv"
    
    # 检查依赖
    source "$HOME/.openclaw/epub_venv/bin/activate"
    if python3 -c "import ebooklib, opencc" 2>/dev/null; then
        echo "✅ 依赖已安装"
    else
        echo "⚠️  依赖未完全安装"
    fi
    deactivate
else
    echo ""
    echo "ℹ️  虚拟环境将在首次运行时自动创建"
fi

echo ""
echo "🎉 技能测试完成！"
echo ""
echo "使用方法："
echo "  python3 scripts/convert_epub.py <input.epub>"
echo "  python3 scripts/convert_epub.py <input.epub> -o <output.epub>"
echo "  python3 scripts/convert_epub.py <input.epub> --direction s2t"
