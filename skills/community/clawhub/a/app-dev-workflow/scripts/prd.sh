#!/bin/bash
#
# 产品功能设计工具 - 生成PRD、用户流程、数据埋点
#
# 用法: bash scripts/prd.sh <命令> [选项]
#   init <feature>        初始化PRD文档
#   flow <feature>        生成用户流程图
#   tracking <feature>    生成埋点设计
#   checklist <feature>   功能验收清单
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️${NC}  $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
step() { echo -e "${CYAN}▶ $1${NC}"; }

# 项目目录
PROJECT_DIR="${PROJECT_DIR:-.}"
PRD_DIR="docs/prd"

show_banner() {
    echo ""
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║     📋 产品功能设计工具                          ║"
    echo "║     PRD / 用户流程 / 数据埋点                    ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 初始化PRD文档
cmd_init() {
    local feature="${1:-}"

    if [ -z "$feature" ]; then
        error "缺少功能名称"
        echo "用法: bash scripts/prd.sh init <功能名称>"
        echo "示例: bash scripts/prd.sh init '风味骰子'"
        exit 1
    fi

    show_banner
    step "初始化PRD: $feature"

    mkdir -p "$PRD_DIR"

    local prd_file="$PRD_DIR/${feature}_PRD.md"
    local today=$(date +%Y-%m-%d)

    cat > "$prd_file" << EOF
# $feature 产品需求文档 (PRD)

> **文档状态**: 🚧 草稿
> **创建日期**: $today
> **负责人**:
> **优先级**: P1

---

## 1. 功能概述

### 1.1 背景与目标

**背景**:
<!-- 描述为什么要做这个功能，解决什么问题 -->

**目标**:
<!-- 列出具体可衡量的目标 -->

### 1.2 价值主张

| 用户痛点 | 解决方案 | 预期收益 |
|---------|---------|---------|
| <!-- 痛点 --> | <!-- 方案 --> | <!-- 收益 --> |

### 1.3 成功指标

- **北极星指标**: <!-- 如：周活跃用户数 -->
- **关键指标**:
  - 功能使用率: 目标 <!-- % -->
  - 功能完成率: 目标 <!-- % -->

---

## 2. 用户场景

### 2.1 目标用户

#### 主要用户 (60%)
- **画像**: <!-- 描述用户特征 -->
- **痛点**: <!-- 用户面临什么问题 -->
- **使用场景**: <!-- 在什么情况下使用 -->

### 2.2 用户故事

\`\`\`
作为: [用户角色]
我想要: [完成什么任务]
所以当: [触发条件]
我能: [执行什么操作]
并且: [获得什么结果]
\`\`\`

### 2.3 用户流程

\`\`\`
[开始] → [步骤1] → [步骤2] → [完成]
\`\`\`

---

## 3. 功能设计

### 3.1 功能清单

| 功能点 | 优先级 | 描述 | 验收标准 | 预估工时 |
|-------|-------|------|---------|---------|
| 核心功能 | P0 | <!-- 描述 --> | <!-- 标准 --> | 4h |
| 增强功能 | P1 | <!-- 描述 --> | <!-- 标准 --> | 2h |
| 可选功能 | P2 | <!-- 描述 --> | <!-- 标准 --> | 1h |

### 3.2 页面结构

\`\`\`
┌─────────────────────────────┐
│  页面标题                    │
├─────────────────────────────┤
│                             │
│      内容区域               │
│                             │
├─────────────────────────────┤
│  [操作按钮]                  │
└─────────────────────────────┘
\`\`\`

### 3.3 交互设计

#### 关键交互
**交互名称**:
- 触发: <!-- 如何触发 -->
- 反馈: <!-- 什么反馈 -->
- 异常: <!-- 异常情况 -->

### 3.4 数据需求

| 数据项 | 类型 | 来源 | 用途 |
|-------|------|------|------|
| <!-- 数据名 --> | <!-- 类型 --> | <!-- 来源 --> | <!-- 用途 --> |

---

## 4. 技术方案

### 4.1 技术实现要点

- <!-- 技术要点1 -->
- <!-- 技术要点2 -->

### 4.2 依赖服务

| 服务 | 用途 | 风险 |
|-----|------|------|
| <!-- 服务名 --> | <!-- 用途 --> | <!-- 风险 --> |

### 4.3 性能要求

- 页面加载: < <!-- 时间 -->ms
- 交互响应: < <!-- 时间 -->ms

---

## 5. 数据埋点

### 5.1 埋点事件

| 事件名 | 触发时机 | 属性 | 用途 |
|-------|---------|------|------|
| <!-- 事件名 --> | <!-- 触发 --> | <!-- 属性 --> | <!-- 用途 --> |

### 5.2 分析指标

- **<!-- 指标名 -->**: <!-- 描述 --> (目标: <!-- 目标值 -->)

---

## 6. 风险与应对

| 风险 | 等级 | 应对策略 |
|-----|------|---------|
| <!-- 风险描述 --> | <!-- 高/中/低 --> | <!-- 应对 --> |

---

## 7. 排期计划

| 阶段 | 任务 | 开始 | 结束 | 负责人 |
|-----|------|------|------|-------|
| 设计 | PRD+原型 | <!-- 日期 --> | <!-- 日期 --> | <!-- 人 --> |
| 开发 | 功能实现 | <!-- 日期 --> | <!-- 日期 --> | <!-- 人 --> |
| 测试 | 验收测试 | <!-- 日期 --> | <!-- 日期 --> | <!-- 人 --> |

---

## 8. 附录

### 8.1 参考文档
- [技术方案](../../豆因_技术方案_v3.2_完整版.md)

### 8.2 变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|-----|------|---------|------|
| $today | v0.1 | 创建文档 | <!-- 作者 --> |
EOF

    success "PRD文档已创建: $prd_file"
    echo ""
    echo "下一步:"
    echo "  1. 编辑PRD文档: code $prd_file"
    echo "  2. 生成用户流程: bash scripts/prd.sh flow '$feature'"
    echo "  3. 生成埋点设计: bash scripts/prd.sh tracking '$feature'"
}

# 生成用户流程图
cmd_flow() {
    local feature="${1:-}"

    if [ -z "$feature" ]; then
        error "缺少功能名称"
        exit 1
    fi

    show_banner
    step "生成用户流程: $feature"

    local flow_file="$PRD_DIR/${feature}_flow.md"

    cat > "$flow_file" << 'EOF'
# 用户流程设计

## 主流程

```
[开始]
  │
  ▼
[页面加载]
  │
  ├─→ [加载失败] → [错误提示] → [结束]
  │
  ▼
[页面展示]
  │
  ├─→ [用户操作A] ──→ [处理A] ──→ [结果A]
  │
  ├─→ [用户操作B] ──→ [处理B] ──→ [结果B]
  │
  └─→ [退出] ───────────────→ [结束]
```

## 分支流程

### 分支1: 正常流程

| 步骤 | 用户动作 | 系统响应 | 页面变化 |
|-----|---------|---------|---------|
| 1 | 点击按钮 | 校验输入 | 显示loading |
| 2 | 等待 | 处理请求 | 进度条更新 |
| 3 | 接收结果 | 展示结果 | 跳转结果页 |

### 分支2: 异常流程

| 步骤 | 触发条件 | 处理方式 | 用户提示 |
|-----|---------|---------|---------|
| 1 | 网络断开 | 缓存数据 | "已切换到离线模式" |
| 2 | 服务超时 | 重试机制 | "正在重试..." |
| 3 | 数据错误 | 降级展示 | "使用默认推荐" |

## 页面流转

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ 页面A   │────→│ 页面B   │────→│ 页面C   │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     └───────────────┴───────────────┘
                     │
                     ▼
               ┌─────────┐
               │  结束   │
               └─────────┘
```

## 状态机

```
          ┌─────────┐
    ┌────→│  初始   │
    │     └────┬────┘
    │          │ 加载数据
    │          ▼
    │     ┌─────────┐
    └─────│  加载中 │←────┐
          └────┬────┘     │
               │ 成功     │ 重试
               ▼          │
          ┌─────────┐     │
          │  正常   │─────┘
          └────┬────┘
               │ 操作
               ▼
          ┌─────────┐
          │  处理中 │
          └────┬────┘
               │
       ┌───────┴───────┐
       ▼               ▼
  ┌─────────┐     ┌─────────┐
  │  成功   │     │  失败   │
  └─────────┘     └─────────┘
```
EOF

    success "用户流程文档已创建: $flow_file"
}

# 生成埋点设计
cmd_tracking() {
    local feature="${1:-}"

    if [ -z "$feature" ]; then
        error "缺少功能名称"
        exit 1
    fi

    show_banner
    step "生成埋点设计: $feature"

    local tracking_file="$PRD_DIR/${feature}_tracking.md"
    local feature_snake=$(echo "$feature" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')

    cat > "$tracking_file" << EOF
# $feature 数据埋点设计

## 概览

| 类别 | 事件数 | 覆盖功能 |
|-----|-------|---------|
| 曝光 | <!-- 数量 --> | <!-- 功能 --> |
| 点击 | <!-- 数量 --> | <!-- 功能 --> |
| 业务 | <!-- 数量 --> | <!-- 功能 --> |
| 性能 | <!-- 数量 --> | <!-- 功能 --> |

## 埋点事件清单

### 页面曝光

| 事件名 | 触发时机 | 属性 | 用途 |
|-------|---------|------|------|
| ${feature_snake}_page_view | 页面可见 | page_name, source | PV统计 |
| ${feature_snake}_page_stay | 离开页面 | duration | 停留时长 |

### 用户交互

| 事件名 | 触发时机 | 属性 | 用途 |
|-------|---------|------|------|
| ${feature_snake}_click | 点击元素 | element_name, position | 点击热区 |
| ${feature_snake}_slide | 滑动操作 | direction, distance | 交互分析 |

### 业务流程

| 事件名 | 触发时机 | 属性 | 用途 |
|-------|---------|------|------|
| ${feature_snake}_start | 开始流程 | timestamp, source | 转化漏斗起点 |
| ${feature_snake}_complete | 完成流程 | duration, result | 转化漏斗终点 |
| ${feature_snake}_error | 发生错误 | error_code, message | 错误分析 |

## 属性定义

### 通用属性

| 属性名 | 类型 | 说明 | 示例 |
|-------|------|------|------|
| user_id | string | 用户ID | "u_123456" |
| session_id | string | 会话ID | "s_abc123" |
| timestamp | number | 时间戳(ms) | 1710825600000 |
| page_name | string | 页面名称 | "dice_page" |
| source | string | 来源页面 | "home_page" |

### 业务属性

| 属性名 | 类型 | 说明 | 示例 |
|-------|------|------|------|
| feature_param | string | 功能参数 | "value" |
| result_status | string | 结果状态 | "success/fail" |
| duration | number | 耗时(ms) | 1500 |

## 指标计算

### 核心指标

| 指标名 | 计算公式 | 目标值 |
|-------|---------|-------|
| 功能使用率 | ${feature_snake}_complete / ${feature_snake}_start | > 80% |
| 平均完成时间 | AVG(duration) | < 30s |
| 错误率 | error_count / total_count | < 5% |

### 漏斗分析

\`\`\`
步骤1 [页面曝光] ──→ 步骤2 [开始操作] ──→ 步骤3 [完成操作]
  100%                 80%                    60%
\`\`\`

## 代码示例

### 曝光埋点

\`\`\`typescript
// 页面曝光
Analytics.track('${feature_snake}_page_view', {
  page_name: '${feature_snake}_page',
  source: this.params.source || 'unknown'
});
\`\`\`

### 点击埋点

\`\`\`typescript
// 点击事件
Analytics.track('${feature_snake}_click', {
  element_name: 'submit_button',
  position: { x: event.x, y: event.y }
});
\`\`\`

### 业务埋点

\`\`\`typescript
// 流程完成
Analytics.track('${feature_snake}_complete', {
  duration: Date.now() - startTime,
  result: 'success',
  params: { /* 业务参数 */ }
});
\`\`\`

## 验证清单

- [ ] 所有P0功能都有埋点覆盖
- [ ] 埋点代码已Code Review
- [ ] 数据上报正常（无丢失）
- [ ] 实时分析数据准确
- [ ] 漏斗数据与业务一致
EOF

    success "埋点设计文档已创建: $tracking_file"
}

# 功能验收清单
cmd_checklist() {
    local feature="${1:-}"

    show_banner
    step "功能验收清单"

    cat << 'EOF'
# 功能验收清单模板

## 功能验收

- [ ] 核心功能正常可用
- [ ] 边界情况处理正确
- [ ] 异常流程有提示
- [ ] 数据持久化正常

## UI验收

- [ ] 符合设计稿
- [ ] 适配不同屏幕
- [ ] 动效流畅
- [ ] 暗色模式支持

## 性能验收

- [ ] 首屏加载 < 2s
- [ ] 交互响应 < 100ms
- [ ] 内存无泄漏
- [ ] 列表滚动流畅

## 兼容性验收

- [ ] HarmonyOS 4.0+
- [ ] 不同分辨率
- [ ] 横竖屏切换
- [ ] 弱网环境

## 安全验收

- [ ] 敏感数据加密
- [ ] 输入校验
- [ ] 权限申请合理
- [ ] 日志脱敏

## 埋点验收

- [ ] 事件触发正确
- [ ] 属性完整
- [ ] 数据上报成功
- [ ] 分析数据准确

EOF

    if [ -n "$feature" ]; then
        echo ""
        echo "功能: $feature"
        echo "请在PRD文档中补充具体验收标准"
    fi
}

# 帮助信息
cmd_help() {
    show_banner
    echo "产品功能设计工具"
    echo ""
    echo "用法: bash scripts/prd.sh <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  init <功能名称>       初始化PRD文档"
    echo "  flow <功能名称>       生成用户流程图"
    echo "  tracking <功能名称>   生成埋点设计"
    echo "  checklist [功能名称]  功能验收清单"
    echo "  help                  显示帮助"
    echo ""
    echo "示例:"
    echo "  bash scripts/prd.sh init '风味骰子'"
    echo "  bash scripts/prd.sh flow 'DIY实验室'"
    echo "  bash scripts/prd.sh tracking '智能推荐'"
    echo ""
    echo "输出目录: docs/prd/"
    echo ""
}

# 主程序
main() {
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        init)
            cmd_init "$@"
            ;;
        flow)
            cmd_flow "$@"
            ;;
        tracking)
            cmd_tracking "$@"
            ;;
        checklist)
            cmd_checklist "$@"
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            error "未知命令: $cmd"
            cmd_help
            exit 1
            ;;
    esac
}

main "$@"
