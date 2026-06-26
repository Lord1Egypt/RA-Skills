#!/bin/bash
# Deep Research Work For Me - 图表转换脚本
# 将 Mermaid 文件批量转换为 PNG 图片

set -e

# 配置
OUTPUT_DIR="${OUTPUT_DIR:-mermaid_charts}"
WIDTH="${WIDTH:-1200}"
BACKGROUND="${BACKGROUND:-transparent}"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 统计
total=0
success=0
failed=0

echo "🚀 开始转换 Mermaid 图表..."
echo "📁 输出目录: $OUTPUT_DIR"
echo "📐 图片宽度: ${WIDTH}px"
echo "🎨 背景: $BACKGROUND"
echo "---"

# 遍历所有 .mmd 文件
for mmd_file in *.mmd; do
    if [ -f "$mmd_file" ]; then
        total=$((total + 1))
        output_file="${OUTPUT_DIR}/${mmd_file%.mmd}.png"
        
        echo "📊 处理: $mmd_file"
        
        if npx -y @mermaid-js/mermaid-cli \
            -i "$mmd_file" \
            -o "$output_file" \
            -b "$BACKGROUND" \
            -w "$WIDTH" \
            2>/dev/null; then
            success=$((success + 1))
            echo "   ✅ 成功: $output_file"
        else
            failed=$((failed + 1))
            echo "   ❌ 失败: $mmd_file"
        fi
    fi
done

echo "---"
echo "📈 转换完成!"
echo "   总计: $total"
echo "   成功: $success"
echo "   失败: $failed"

# 返回状态码
if [ $failed -gt 0 ]; then
    exit 1
fi
