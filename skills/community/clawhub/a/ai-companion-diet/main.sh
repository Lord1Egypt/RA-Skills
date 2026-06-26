#!/bin/bash

# AI智能陪伴减肥助手 - 主入口脚本
# 版本: 1.0.0

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SKILL_DIR/data"

# 初始化数据目录
mkdir -p "$DATA_DIR/daily_records"

# 加载功能模块
source "$SKILL_DIR/modules/calculator.sh"
source "$SKILL_DIR/modules/recorder.sh"
source "$SKILL_DIR/modules/analyzer.sh"
source "$SKILL_DIR/modules/notifier.sh"

# 显示帮助信息
show_help() {
    echo "AI智能陪伴减肥助手 v1.0.0"
    echo ""
    echo "使用方法:"
    echo "  init-user-data              初始化用户基础数据"
    echo "  start-daily-plan            开始今日减肥计划"
    echo "  record-breakfast <描述> [重量]  记录早餐"
    echo "  record-lunch <描述> [重量]      记录午餐"
    echo "  record-dinner <描述> [重量]     记录晚餐"
    echo "  record-snack <描述> [重量]      记录加餐"
    echo "  record-steps <步数>              记录今日步数"
    echo "  record-weight <体重(kg)>         记录今日体重"
    echo "  daily-summary                      查看今日总结"
    echo "  weight-trend                       查看体重趋势"
    echo "  weekly-analysis                    查看本周分析"
    echo "  plateau-analysis                   平台期分析"
    echo "  predict-weight-loss                预测减重趋势"
    echo "  help                               显示此帮助信息"
    echo ""
}

# 主命令分发
main() {
    local cmd="$1"
    shift

    case "$cmd" in
        init-user-data)
            init_user_data "$@"
            ;;
        start-daily-plan)
            start_daily_plan
            ;;
        record-breakfast)
            record_meal "breakfast" "$@"
            ;;
        record-lunch)
            record_meal "lunch" "$@"
            ;;
        record-dinner)
            record_meal "dinner" "$@"
            ;;
        record-snack)
            record_meal "snack" "$@"
            ;;
        record-steps)
            record_steps "$@"
            ;;
        record-weight)
            record_weight "$@"
            ;;
        daily-summary)
            show_daily_summary
            ;;
        weight-trend)
            show_weight_trend
            ;;
        weekly-analysis)
            show_weekly_analysis
            ;;
        plateau-analysis)
            analyze_plateau
            ;;
        predict-weight-loss)
            predict_weight_loss
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "未知命令: $cmd"
            echo "使用 'help' 查看帮助信息"
            return 1
            ;;
    esac
}

# 如果直接执行此脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
