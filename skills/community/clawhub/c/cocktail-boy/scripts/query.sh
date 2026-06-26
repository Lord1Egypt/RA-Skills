#!/bin/bash

# Cocktail-Boy: 鸡尾酒查询脚本
# 数据库路径（相对于脚本所在目录）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DB_FILE="$SCRIPT_DIR/../data/rohan_cocktails.csv"

# 检查数据库是否存在
if [ ! -f "$DB_FILE" ]; then
    echo "❌ 数据库文件未找到：$DB_FILE"
    exit 1
fi

# 函数 1: 搜索鸡尾酒名称
search_drink() {
    local query="$1"
    
    if [ -z "$query" ]; then
        echo "❌ 请提供酒名，例如：/cocktail mojito"
        exit 1
    fi
    
    # 转换为小写并搜索
    echo "🍸 正在搜索：**$query**..."
    echo ""
    
    # 使用 awk 进行大小写不敏感搜索
    result=$(awk -F',' -v drink="$query" '
        NR==1 {next}  # 跳过表头
        {
            if (tolower($1) ~ tolower(drink)) print $0
        }
    ' "$DB_FILE" | head -20)
    
    if [ -z "$result" ]; then
        echo "❌ 未找到匹配的鸡尾酒："
        echo "💡 建议：尝试英文名称，例如：mojito, margarita, old fashioned"
        exit 1
    fi
    
    # 提取所有不同的酒 ID
    drink_ids=$(echo "$result" | awk -F',' '{print $1}' | sort -u)
    
    for id in $drink_ids; do
        echo "📍 找到匹配的酒：$(echo "$result" | grep "^$id," | head -1 | cut -d',' -f1)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # 显示该酒的所有原料
        ingredients=$(awk -F',' -v id="$id" 'NR==1 {next} $1 == id {print $0}' "$DB_FILE")
        
        echo ""
        echo "🥤 **原料清单**:"
        awk -F',' -v id="$id" '$1 == id' "$DB_FILE" | while IFS=',' read -r drink_id ingredient amount use glass howto; do
            echo "  • $ingredient - $amount ($use)"
        done
        
        echo ""
        echo "🧊 **调制方法**:"
        # 去重显示做法
        unique_methods=$(awk -F',' -v id="$id" '$1 == id {print $6}' "$DB_FILE" | sort -u | tr '\n' ' ')
        echo "  $unique_methods"
        
        echo ""
        echo "🍷 **使用酒杯**: $(echo "$ingredients" | head -1 | cut -d',' -f5)"
        echo ""
    done
    
    # 提示用户如果想找其他酒，可以继续查询
    echo "💡 如需继续查找其他鸡尾酒，请告诉我酒名！"
}

# 函数 2: 搜索原料
search_by_ingredient() {
    local ingredient="$1"
    
    if [ -z "$ingredient" ]; then
        echo "❌ 请提供原料名称，例如：/ingredients vodka"
        exit 1
    fi
    
    echo "🔍 正在查找含 **$ingredient** 的鸡尾酒..."
    echo ""
    
    # 搜索包含该原料的所有酒
    drinks=$(awk -F',' -v ing="$ingredient" 'NR==1 {next} tolower($2) ~ tolower(ing) {print $1}' "$DB_FILE" | sort -u)
    
    count=$(echo "$drinks" | wc -l)
    
    if [ "$count" -eq 0 ]; then
        echo "❌ 未找到含 **$ingredient** 的鸡尾酒"
        exit 1
    fi
    
    echo "✅ 找到了 $count 款包含 **$ingredient** 的鸡尾酒："
    echo ""
    
    # 列出前 10 个
    for id in $(echo "$drinks" | head -10); do
        drink_name=$(awk -F',' -v id="$id" '$1 == id {print $1; exit}' "$DB_FILE")
        ingredient_in_drink=$(awk -F',' -v id="$id" -v ing="$ingredient" 'NR==1 {next} $1 == id && tolower($2) ~ tolower(ing) {print $3 " " $2; exit}' "$DB_FILE")
        echo "  🍸 $drink_name"
        echo "     原料：$ingredient_in_drink"
        echo ""
    done
    
    if [ "$count" -gt 10 ]; then
        echo "... 还有 $((count-10)) 款未显示，请输入具体酒名获取详细信息"
    fi
}

# 函数 3: 随机推荐
recommend_random() {
    # 从第二行开始（跳过表头），随机选择一行
    random_line=$(awk -F',' 'NR>1' "$DB_FILE" | shuf | head -1)
    
    drink_name=$(echo "$random_line" | cut -d',' -f1)
    
    echo "🎲 **今日推荐酒单**："
    echo ""
    echo "🍸 $drink_name"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 查找所有原料
    echo "🥤 **原料清单**:"
    awk -F',' -v name="$drink_name" '$1 ~ tolower(name) {print "  • " $3 " " $2}' "$DB_FILE" | head -10
    
    echo ""
    echo "🧊 **调制方法**:"
    unique_methods=$(awk -F',' -v name="$drink_name" '$1 ~ tolower(name) {print $6}' "$DB_FILE" | sort -u | tr '\n' ' ')
    echo "  $unique_methods"
    
    echo ""
    echo "🍷 **使用酒杯**: $(echo "$random_line" | cut -d',' -f5)"
}

# 主程序
main() {
    local command="$1"
    local query="$2"
    
    case "$command" in
        "search")
            search_drink "$query"
            ;;
        "ingredient")
            search_by_ingredient "$query"
            ;;
        "recommend")
            recommend_random
            ;;
        *)
            echo "🍹 **Cocktail-Boy - 你的私人调酒师** 🍹"
            echo ""
            echo "使用方式:"
            echo "  /cocktail [酒名]          - 查询特定鸡尾酒"
            echo "  /ingredients [原料]       - 搜索含某原料的鸡尾酒"
            echo "  /recommend                - 随机推荐一款鸡尾酒"
            echo ""
            echo "🔍 数据库包含 **1635** 款鸡尾酒配方！"
            echo ""
            ;;
    esac
}

# 执行主函数
main "$@"
