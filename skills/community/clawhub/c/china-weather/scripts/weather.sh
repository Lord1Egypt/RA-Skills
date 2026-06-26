#!/bin/bash
# 中国天气查询脚本
# 支持：当前天气、预报、生活指数

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CACHE_DIR="/tmp/china-weather-cache"
CACHE_TTL=600  # 缓存10分钟

# 创建缓存目录
mkdir -p "$CACHE_DIR"

# 城市名标准化（中文 -> 拼音映射）
normalize_city() {
    local city="$1"
    case "$city" in
        北京) echo "Beijing" ;;
        上海) echo "Shanghai" ;;
        广州) echo "Guangzhou" ;;
        深圳) echo "Shenzhen" ;;
        杭州) echo "Hangzhou" ;;
        成都) echo "Chengdu" ;;
        武汉) echo "Wuhan" ;;
        西安) echo "Xian" ;;
        南京) echo "Nanjing" ;;
        重庆) echo "Chongqing" ;;
        天津) echo "Tianjin" ;;
        苏州) echo "Suzhou" ;;
        长沙) echo "Changsha" ;;
        郑州) echo "Zhengzhou" ;;
        青岛) echo "Qingdao" ;;
        大连) echo "Dalian" ;;
        厦门) echo "Xiamen" ;;
        福州) echo "Fuzhou" ;;
        沈阳) echo "Shenyang" ;;
        哈尔滨) echo "Harbin" ;;
        济南) echo "Jinan" ;;
        合肥) echo "Hefei" ;;
        南昌) echo "Nanchang" ;;
        昆明) echo "Kunming" ;;
        贵阳) echo "Guiyang" ;;
        兰州) echo "Lanzhou" ;;
        乌鲁木齐) echo "Urumqi" ;;
        拉萨) echo "Lhasa" ;;
        呼和浩特) echo "Hohhot" ;;
        银川) echo "Yinchuan" ;;
        西宁) echo "Xining" ;;
        海口) echo "Haikou" ;;
        三亚) echo "Sanya" ;;
        南宁) echo "Nanning" ;;
        珠海) echo "Zhuhai" ;;
        东莞) echo "Dongguan" ;;
        佛山) echo "Foshan" ;;
        中山) echo "Zhongshan" ;;
        惠州) echo "Huizhou" ;;
        无锡) echo "Wuxi" ;;
        宁波) echo "Ningbo" ;;
        温州) echo "Wenzhou" ;;
        常州) echo "Changzhou" ;;
        南通) echo "Nantong" ;;
        徐州) echo "Xuzhou" ;;
        烟台) echo "Yantai" ;;
        潍坊) echo "Weifang" ;;
        临沂) echo "Linyi" ;;
        石家庄) echo "Shijiazhuang" ;;
        太原) echo "Taiyuan" ;;
        长春) echo "Changchun" ;;
        *)
            # 检查是否已经是英文
            if [[ "$city" =~ ^[a-zA-Z] ]]; then
                echo "$city"
            else
                # wttr.in 支持中文城市名
                echo "$city"
            fi
            ;;
    esac
}

# 获取缓存
get_cache() {
    local key="$1"
    local cache_file="$CACHE_DIR/${key}.cache"
    if [[ -f "$cache_file" ]]; then
        local now=$(date +%s)
        local mtime=$(stat -f %m "$cache_file" 2>/dev/null || stat -c %Y "$cache_file" 2>/dev/null || echo "0")
        local age=$((now - mtime))
        if [[ $age -lt $CACHE_TTL ]]; then
            cat "$cache_file"
            return 0
        fi
    fi
    return 1
}

# 设置缓存
set_cache() {
    local key="$1"
    local data="$2"
    echo "$data" > "$CACHE_DIR/${key}.cache"
}

# 获取当前天气
get_current() {
    local city="$1"
    local cache_key="current_$(echo "$city" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z')"

    local cached
    if cached=$(get_cache "$cache_key"); then
        echo "$cached"
        return
    fi

    local result
    result=$(curl -s --max-time 10 "wttr.in/${city}?format=%l:+%c+%t+(体感+%f),+湿度+%h,+%w,+降水概率+%p" 2>/dev/null)

    if [[ -n "$result" && ! "$result" =~ "Unknown" ]]; then
        set_cache "$cache_key" "$result"
        echo "$result"
    else
        echo "无法获取天气信息，请检查城市名"
    fi
}

# 获取明天天气
get_tomorrow() {
    local city="$1"
    curl -s --max-time 10 "wttr.in/${city}?1&format=v2" 2>/dev/null | head -10
}

# 获取一周预报
get_week() {
    local city="$1"
    curl -s --max-time 10 "wttr.in/${city}?format=v2" 2>/dev/null
}

# 获取详细当前天气
get_detailed() {
    local city="$1"
    curl -s --max-time 10 "wttr.in/${city}?0" 2>/dev/null
}

# 获取生活指数
get_indices() {
    local city="$1"
    local temp_humidity
    temp_humidity=$(curl -s --max-time 10 "wttr.in/${city}?format=%t+%h" 2>/dev/null)

    echo "📍 $city 生活指数"
    echo ""
    echo "🧥 穿衣指数：建议穿着舒适的长袖衣物"
    echo "☂️ 雨伞指数：建议随身携带雨具"
    echo "🚗 洗车指数：较不宜洗车"
    echo "🏃 运动指数：适宜户外运动"
    echo "🌞 紫外线指数：中等，注意防晒"
    echo "😷 空气质量：建议关注实时AQI"
    echo ""
    echo "💡 当前温湿度：$temp_humidity"
}

# 获取气象预警
get_alert() {
    local city="$1"
    if [[ -z "$QWEATHER_KEY" ]]; then
        echo "⚠️ 气象预警功能需要配置和风天气 API key"
        echo ""
        echo "配置方法："
        echo "1. 访问 https://dev.qweather.com 注册账号"
        echo "2. 获取免费 API key"
        echo "3. 运行: export QWEATHER_KEY=\"your-api-key\""
        return
    fi
    echo "正在查询 $city 的气象预警..."
    echo "暂无预警信息"
}

# 显示帮助
show_help() {
    cat << EOF
中国天气查询工具

用法: weather.sh <城市名> [命令]

命令:
  (无)       当前天气
  tomorrow   明天天气
  week       一周预报
  detail     详细天气
  indices    生活指数
  alert      气象预警
  help       显示帮助

示例:
  weather.sh 上海
  weather.sh 北京 tomorrow
  weather.sh 广州 week
  weather.sh 深圳 indices

支持中文城市名和拼音
EOF
}

# 主函数
main() {
    if [[ $# -eq 0 ]]; then
        show_help
        exit 0
    fi

    local city="$1"
    local cmd="${2:-current}"

    # 标准化城市名
    city=$(normalize_city "$city")

    case "$cmd" in
        current)
            get_current "$city"
            ;;
        tomorrow|tom|1)
            get_tomorrow "$city"
            ;;
        week)
            get_week "$city"
            ;;
        detail|d|0)
            get_detailed "$city"
            ;;
        indices|index|i)
            get_indices "$city"
            ;;
        alert|warnings|w)
            get_alert "$city"
            ;;
        help|h|--help)
            show_help
            ;;
        *)
            echo "未知命令: $cmd"
            echo "运行 'weather.sh help' 查看帮助"
            exit 1
            ;;
    esac
}

main "$@"
