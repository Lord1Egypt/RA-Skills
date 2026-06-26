#!/bin/bash
# ============================================================
# deep_research_v3 orchestrator — 商业决策级深度调研编排脚本
# 用法: bash orchestrator.sh "[调研主题]"
# 设计: 强制逐步骤推进，每步完成后写 checkpoint，不可跳步
# V3.1: + Agent 执行指令块 + --self-check 自检模式
# ============================================================

set -euo pipefail

TOPIC="${1:-}"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECKPOINT_DIR="${SKILL_DIR}/.research_state"
REPORTS_DIR="${DEEP_RESEARCH_REPORTS_DIR:-${SKILL_DIR}/reports}"

# --- 启动依赖检查 ---
check_dependencies() {
    local missing=()
    if ! command -v jq &>/dev/null && ! command -v python3 &>/dev/null; then
        missing+=("jq 或 python3")
    fi
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}⛔ 缺少依赖: ${missing[*]}${NC}"
        echo "请安装 jq (brew install jq) 或确保 python3 可用"
        exit 1
    fi
}

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# ============================================================
# Agent 执行指令块（每步追加，指导 Agent 必须做什么/禁止什么）
# ============================================================
get_agent_instructions() {
    local step="$1"
    case "$step" in
        s0)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s0 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 将下方的 S0 6要素确认表输出到对话中
2. 如果用户未提供足够信息，**主动提问澄清**，不可猜测
3. 明确标注"待澄清问题"
4. 等待用户确认（或说"无需补充"）后才能推进

### 你禁止做：
- ❌ 不可猜测用户未明确的信息
- ❌ 不可跳过6要素中的任何一项
- ❌ 不可在用户确认前进入搜索阶段

### 完成后执行：
```bash
bash orchestrator.sh --complete s0 --next s1
```
<!-- /AGENT_INSTRUCTION:s0 -->
EOF
            ;;
        s1)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s1 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 将 S0 确认的核心问题拆解为 3-5 个子问题
2. 每个子问题必须是可以被证据回答的（不是观点）
3. 每个子问题配至少 2 组中英双语关键词
4. 输出完整拆解表（含论证目标、证据类型）

### 你禁止做：
- ❌ 子问题不可少于 3 个，不可多于 5 个
- ❌ 不可用"是/否"问题（必须有论证空间）
- ❌ 关键词不可只用中文（至少一组英文）

### 完成后执行：
```bash
bash orchestrator.sh --complete s1 --next s2
```
<!-- /AGENT_INSTRUCTION:s1 -->
EOF
            ;;
        s2)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s2 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 输出反思校验表（关键词检查 + 覆盖面检查 + 潜在偏差检查）
2. 检查关键词是否足够多元（不同角度、不同粒度）
3. 检查是否有"先入为主"的假设关键词（如"AI必然提升效率"）
4. 如有问题，立即修正关键词并记录修正原因

### 你禁止做：
- ❌ 不可跳过反思直接搜索——此步是V3最关键的断点
- ❌ 不可敷衍"覆盖面检查"为"已覆盖"
- ❌ 不可无反思就标注"无修正"

### 完成后执行：
```bash
bash orchestrator.sh --complete s2 --next s3
```
<!-- /AGENT_INSTRUCTION:s2 -->
EOF
            ;;
        s3)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s3 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 使用当前环境的搜索工具执行网络搜索
2. 每个子问题至少 2 组关键词搜索
3. 每批最多 4 个并行搜索，批间间隔 ≥5 秒
4. 记录每条结果的 URL、标题、摘要、来源、初步评级（P0-P4）

### 你禁止做：
- ❌ 不可跳过任何子问题
- ❌ 不可超过 4 个并行搜索
- ❌ 不可只搜一组关键词就满足

### 完成后执行：
```bash
bash orchestrator.sh --complete s3 --next s4
```
<!-- /AGENT_INSTRUCTION:s3 -->
EOF
            ;;
        s4)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s4 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 从 S3 结果中筛选 P0-P2 来源（官方/学术/权威媒体）
2. 对所有 P0 来源执行全文抓取（maxChars=50000）
3. P1 至少抓取 3 个，P2 至少抓取 2 个
4. 抓取失败必须记录原因并找替代来源

### 你禁止做：
- ❌ 不可只靠搜索摘要就跳过全文抓取
- ❌ 知乎等反爬平台抓不到正文的，不推送
- ❌ 不可跳过失败的 URL——必须记录+替代

### 完成后执行：
```bash
bash orchestrator.sh --complete s4 --next s5
```
<!-- /AGENT_INSTRUCTION:s4 -->
EOF
            ;;
        s5)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s5 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 从 S4 的抓取内容中提取至少 2 个新线索（新术语/被引报告/新角度）
2. 对新线索执行补充搜索（遵守并发限制）
3. 对核心结论进行交叉验证——每条结论至少 2 个独立来源

### 你禁止做：
- ❌ 即使 S3 看起来已经足够，也不可跳过此步
- ❌ 如果找不到新线索，说明 S4 深读不够，返回重读
- ❌ 单一来源结论不可作为核心论据（必须标注）

### 完成后执行：
```bash
bash orchestrator.sh --complete s5 --next s6
```
<!-- /AGENT_INSTRUCTION:s5 -->
EOF
            ;;
        s6)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s6 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 按子问题归类所有证据
2. 区分"强支撑"（T1-T2，可作核心论据）和"弱支撑"（T3-T4，仅参考）
3. 每个数据标注来源机构名称
4. 模糊表述（"大幅增长"）替换为具体数字或标注"数据不足"

### 你禁止做：
- ❌ T3-T4 级信源不可作为核心论点支撑
- ❌ 不可使用"大幅增长""显著提升"等模糊表述
- ❌ 不可将 AI 生成内容（P4/T5）作为任何级别的来源

### 完成后执行：
```bash
bash orchestrator.sh --complete s6 --next s7
```
<!-- /AGENT_INSTRUCTION:s6 -->
EOF
            ;;
        s7)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s7 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 每个子问题按"问题→证据→分析→判断"链撰写
2. 仅推测内容需要标注：【推测，置信度：高/中/低】
3. 事实陈述、分析推理、判断结论均不标注标签，自然行文即可
4. 写完每个子问题后自检"删除搜索引文后，这段话还有独立价值吗？"
5. 结论必须从证据中自然导出

### 你禁止做：
- ❌ 不可写"搜索摘要堆砌"——如果一段话只是翻译搜索结果，重写
- ❌ 不可先有结论再找证据
- ❌ 不可推测量不标注置信度
- ❌ 不可对事实/分析/判断内容标注标签（仅推测需要标注）

### 完成后执行：
```bash
bash orchestrator.sh --complete s7 --next s8
```
<!-- /AGENT_INSTRUCTION:s7 -->
EOF
            ;;
        s8)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s8 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 跨子问题寻找新的交汇洞察
2. 至少输出 2 条独立新判断
3. 每条洞察自检：是否在 S7 中不曾明确提出？

### 你禁止做：
- ❌ 交汇洞察不可缩写前文——必须是读完所有论述后才产生的新判断
- ❌ 不可少于 2 条洞察

### 完成后执行：
```bash
bash orchestrator.sh --complete s8 --next s9
```
<!-- /AGENT_INSTRUCTION:s8 -->
EOF
            ;;
        s9)
            cat <<'EOF'
<!-- AGENT_INSTRUCTION:s9 -->
## 🤖 当前步骤执行指令（必须遵守）

### 你必须做：
1. 生成执行摘要（3-5 句话，直接给结论）
2. 完成 12 项质量自检——全部 ✅ 才能交付
3. 任一未通过，返回对应步骤修正后重新自检
4. 保存报告到 `reports/YYYY-MM-DD-{主题}.md`
5. 发送摘要给用户

### 12 项自检表（逐项核验）：
| # | 检查项 | 检查方法 |
|---|--------|---------|
| 1 | 按 s0→s9 顺序完整执行 | 检查 session.json 是否有全部步骤完成记录 |
| 2 | s0 6要素确认表已输出 | 回顾对话中有无确认表 |
| 3 | s2 反思校验表已输出 | 回顾对话中有无反思表 |
| 4 | 核心数据有 3+ 独立来源印证 | 抽查 3 个核心数据的引用数 |
| 5 | 推测标注置信度，事实/分析无冗余标签 | 全文搜索【推测】是否出现，检查分析段无标签 |
| 6 | 找不到的信息明确说"数据暂缺" | 检查报告中有无"数据暂缺"相关表述 |
| 7 | T3-T4 未作核心论据支撑 | 检查核心章节是否引用了 T4 作为主要论据 |
| 8 | 纵轴叙事为故事体（因果链条） | 检查纵轴是否"2023→2024→2025"流水账 |
| 9 | 交汇洞察为独立新判断 | 对照 S7 和 S8，确认无缩写 |
| 10 | 数据缺口和低置信度结论已标注 | 检查报告中"数据不足""置信度低"等标注是否完整 |
| 11 | 给出可操作建议 | 检查结论章节是否有具体行动建议 |
| 12 | 报告保存在正确路径 | 检查 `reports/` 目录是否有当天文件 |

### 你禁止做：
- ❌ 任一项未打勾不可交付
- ❌ 不可跳过自检直接保存

### 完成后执行：
```bash
bash orchestrator.sh --complete s9 --next done
```
<!-- /AGENT_INSTRUCTION:s9 -->
EOF
            ;;
        *)
            echo "<!-- AGENT_INSTRUCTION: 未知步骤: $step -->"
            ;;
    esac
}

# --- 首次调用：初始化 ---
init_session() {
    if [[ -z "$TOPIC" ]]; then
        echo -e "${RED}⛔ 错误: 必须传入调研主题${NC}"
        echo "用法: bash orchestrator.sh \"调研主题\""
        exit 1
    fi

    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SESSION_ID="research_${TIMESTAMP}"
    mkdir -p "$CHECKPOINT_DIR"

    cat > "${CHECKPOINT_DIR}/session.json" <<EOF
{
  "session_id": "${SESSION_ID}",
  "topic": "${TOPIC}",
  "created_at": "$(date -Iseconds)",
  "completed_steps": [],
  "current_step": "s0",
  "status": "in_progress"
}
EOF

    echo -e "${GREEN}✅ 调研会话已初始化${NC}"
    echo -e "   会话ID: ${SESSION_ID}"
    echo -e "   主题:   ${TOPIC}"
    echo ""
}

# --- 读取会话状态 ---
load_session() {
    if [[ ! -f "${CHECKPOINT_DIR}/session.json" ]]; then
        echo -e "${RED}⛔ 没有活跃的调研会话，请先执行: bash orchestrator.sh \"主题\"${NC}"
        exit 1
    fi
}

# --- 标记步骤完成 ---
complete_step() {
    local step="$1"
    local state_file="${CHECKPOINT_DIR}/session.json"

    if command -v jq &>/dev/null; then
        jq --arg s "$step" '.completed_steps += [$s] | .current_step = ""' "$state_file" > "${state_file}.tmp" && mv "${state_file}.tmp" "$state_file"
    elif command -v python3 &>/dev/null; then
        python3 -c "
import json
with open('$state_file') as f:
    state = json.load(f)
state['completed_steps'].append('$step')
state['current_step'] = ''
with open('$state_file', 'w') as f:
    json.dump(state, f, indent=2)
"
    else
        echo -e "${RED}⛔ 需要 jq 或 python3 来管理状态${NC}"
        exit 1
    fi
}

# --- 推进到下一步 ---
advance_step() {
    local next_step="$1"
    local state_file="${CHECKPOINT_DIR}/session.json"

    if command -v jq &>/dev/null; then
        jq --arg s "$next_step" '.current_step = $s' "$state_file" > "${state_file}.tmp" && mv "${state_file}.tmp" "$state_file"
    elif command -v python3 &>/dev/null; then
        python3 -c "
import json
with open('$state_file') as f:
    state = json.load(f)
state['current_step'] = '$next_step'
with open('$state_file', 'w') as f:
    json.dump(state, f, indent=2)
"
    fi
}

# --- 显示步骤内容 + Agent 指令 ---
show_step() {
    local step="$1"
    local step_file="${SKILL_DIR}/steps/${step}.md"

    if [[ ! -f "$step_file" ]]; then
        echo -e "${RED}⛔ 步骤文件不存在: ${step_file}${NC}"
        exit 1
    fi

    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  📋 当前步骤: ${step}${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo ""
    cat "$step_file"
    echo ""
    echo -e "${MAGENTA}────────────────────────────────────────────────────────${NC}"
    get_agent_instructions "$step"
    echo -e "${MAGENTA}────────────────────────────────────────────────────────${NC}"
}

# ============================================================
# --self-check 模式：报告交付前 12 项质量自检
# ============================================================
run_self_check() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  🔍 S9 交付前质量自检${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════${NC}"
    echo ""

    # 查找最新的报告文件
    LATEST_REPORT=$(ls -t "${REPORTS_DIR}"/*.md 2>/dev/null | head -1)
    if [[ -z "$LATEST_REPORT" ]]; then
        echo -e "${RED}⛔ 未找到报告文件。请先保存报告到 ${REPORTS_DIR}/${NC}"
        echo ""
        echo -e "${YELLOW}💡 提示：报告是否已写入？如果报告在其他路径，请手动核对以下检查表。${NC}"
        echo ""
        REPORT_FOUND=false
    else
        echo -e "${GREEN}📄 检测到最新报告：${LATEST_REPORT}${NC}"
        echo ""
        REPORT_FOUND=true

        # 自动检查项
        echo -e "${YELLOW}─── 自动检查 ───${NC}"
        echo ""

        # 检查1: 文件是否有内容
        FILE_SIZE=$(wc -c < "$LATEST_REPORT")
        if [[ "$FILE_SIZE" -gt 5000 ]]; then
            echo -e "  #01 文件内容充足 (${FILE_SIZE} bytes)  ${GREEN}✅${NC}"
        elif [[ "$FILE_SIZE" -gt 0 ]]; then
            echo -e "  #01 文件内容偏少 (${FILE_SIZE} bytes)  ${YELLOW}⚠️${NC}"
        else
            echo -e "  #01 文件为空  ${RED}❌${NC}"
        fi

        # 检查2: 是否有执行摘要
        if grep -q "执行摘要" "$LATEST_REPORT"; then
            echo -e "  #02 包含执行摘要  ${GREEN}✅${NC}"
        else
            echo -e "  #02 缺少执行摘要  ${RED}❌${NC}"
        fi

        # 检查3: 是否有来源列表
        if grep -q "来源列表\|参考来源\|参考资料" "$LATEST_REPORT"; then
            echo -e "  #03 包含来源列表  ${GREEN}✅${NC}"
        else
            echo -e "  #03 缺少来源列表  ${RED}❌${NC}"
        fi

        # 检查4: 是否有推测标注
        if grep -q "【推测" "$LATEST_REPORT"; then
            SPEC_COUNT=$(grep -c "【推测" "$LATEST_REPORT" || true)
            echo -e "  #04 包含推测标注 (${SPEC_COUNT}处)  ${GREEN}✅${NC}"
        else
            echo -e "  #04 缺少推测标注  ${YELLOW}⚠️（可能无推测内容，需手动确认）${NC}"
        fi

        # 检查5: 是否有编号引用
        if grep -qE '\[[0-9]+\]' "$LATEST_REPORT"; then
            CITATION_COUNT=$(grep -oE '\[[0-9]+\]' "$LATEST_REPORT" | sort -u | wc -l)
            echo -e "  #05 包含编号引用 (${CITATION_COUNT}个不同引用)  ${GREEN}✅${NC}"
        else
            echo -e "  #05 缺少编号引用  ${RED}❌${NC}"
        fi

        # 检查6: 模糊表述检查
        if grep -qE "大幅(增长|提升|下降|减少)" "$LATEST_REPORT"; then
            echo -e "  #06 包含模糊表述（\"大幅增长\"等）  ${RED}❌${NC}"
        else
            echo -e "  #06 无模糊表述  ${GREEN}✅${NC}"
        fi

        echo ""
    fi

    # 手动检查项
    echo -e "${YELLOW}─── 手动检查（请逐项核验）───${NC}"
    echo ""

    cat <<'CHECKLIST'
  #07 是否按 s0→s9 顺序完整执行？             [ ] ✅ / ❌
  #08 s0 6要素确认表是否已输出？               [ ] ✅ / ❌
  #09 s2 反思校验表是否已输出？                 [ ] ✅ / ❌
  #10 核心数据是否有 3+ 独立来源印证？          [ ] ✅ / ❌
  #11 T3-T4 级信源是否未作为核心论据？          [ ] ✅ / ❌
  #12 纵轴叙事是否为故事体（非流水账）？        [ ] ✅ / ❌
  #13 交汇洞察是否为独立新判断（非缩写）？      [ ] ✅ / ❌
  #14 数据缺口和低置信度结论是否已标注？        [ ] ✅ / ❌
  #15 是否给出了可操作建议？                    [ ] ✅ / ❌
  #16 报告是否保存在正确路径？                  [ ] ✅ / ❌
CHECKLIST

    echo ""
    echo -e "${RED}⛔ 所有 16 项（自动 6 + 手动 10）必须全部 ✅ 才能交付${NC}"
    echo -e "${YELLOW}💡 如任一项 ❌，请返回对应步骤修正后重新执行 --self-check${NC}"
    echo ""
}

# --- 主流程 ---
main() {
    check_dependencies
    case "${1:-}" in
        --complete)
            load_session
            COMPLETE_STEP="${2:-}"
            NEXT_STEP="${4:-}"

            if [[ -z "$COMPLETE_STEP" ]]; then
                echo -e "${RED}⛔ 用法: bash orchestrator.sh --complete <步骤> --next <下一步>${NC}"
                exit 1
            fi

            complete_step "$COMPLETE_STEP"

            if [[ -n "$NEXT_STEP" ]]; then
                advance_step "$NEXT_STEP"
                echo -e "${GREEN}✅ ${COMPLETE_STEP} 已完成 → 推进到 ${NEXT_STEP}${NC}"

                if [[ "$NEXT_STEP" == "done" ]]; then
                    echo ""
                    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
                    echo -e "${GREEN}  🎉 调研流程全部完成！${NC}"
                    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
                    echo ""
                    echo -e "${YELLOW}  ⚠️ 交付前请执行最终自检:${NC}"
                    echo -e "${YELLOW}     bash orchestrator.sh --self-check${NC}"
                    # 清理状态文件
                    rm -f "${CHECKPOINT_DIR}/session.json"
                else
                    show_step "$NEXT_STEP"
                fi
            fi
            ;;

        --status)
            load_session
            echo -e "${CYAN}📊 调研状态:${NC}"
            cat "${CHECKPOINT_DIR}/session.json"
            ;;

        --reset)
            rm -f "${CHECKPOINT_DIR}/session.json"
            echo -e "${YELLOW}🔄 会话状态已重置${NC}"
            ;;

        --self-check)
            run_self_check
            ;;

        *)
            # 首次调用或继续
            if [[ ! -f "${CHECKPOINT_DIR}/session.json" ]]; then
                init_session
                show_step "s0"
            else
                load_session
                CURRENT=$(python3 -c "import json; f=open('${CHECKPOINT_DIR}/session.json'); s=json.load(f); print(s.get('current_step',''))")
                if [[ -z "$CURRENT" ]]; then
                    echo -e "${YELLOW}⚠️ 当前没有待执行的步骤。检查是否已完成所有步骤。${NC}"
                    echo "已完成的步骤:"
                    python3 -c "import json; f=open('${CHECKPOINT_DIR}/session.json'); s=json.load(f); print(', '.join(s.get('completed_steps',[])))"
                else
                    show_step "$CURRENT"
                fi
            fi
            ;;
    esac
}

main "$@"
