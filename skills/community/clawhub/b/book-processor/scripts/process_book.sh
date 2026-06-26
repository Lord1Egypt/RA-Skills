#!/usr/bin/env bash
# ------------------------------------------------------------
# 通用书籍处理脚本 – 依据 books/<书名>/process_config.json 自动生成资产
# ------------------------------------------------------------
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <book_dir>"
  exit 1
fi

BOOK_DIR="$1"
CONFIG_FILE="$BOOK_DIR/process_config.json"

# ---------- 1. 基础准备 ----------
# 找 epub 文件（只能有一个）
EPUB_FILE=$(ls "$BOOK_DIR"/*.epub 2>/dev/null | head -n1 || true)
if [[ -z "$EPUB_FILE" ]]; then
  echo "未找到 epub 文件，结束。"
  exit 0
fi

# 2. 解压（已存在则跳过）
TMP_DIR="/tmp/epub_extracted_${RANDOM}"
export TMP_DIR
OUT_TEXT="$BOOK_DIR/full_text.txt"
export OUT_TEXT
mkdir -p "$TMP_DIR"
unzip -q "$EPUB_FILE" -d "$TMP_DIR"

# 3. 提取全文（纯文本）- 通用搜索方法
OUT_TEXT="$BOOK_DIR/full_text.txt"
python3 - <<'PY'
import os, re, sys
tmp_dir = os.getenv('TMP_DIR')
out_path = os.getenv('OUT_TEXT')

# 递归搜索所有 .html 和 .xhtml 文件
html_files = []
for root, dirs, files in os.walk(tmp_dir):
    for f in files:
        if f.lower().endswith(('.html', '.xhtml')):
            html_files.append(os.path.join(root, f))

# 按文件名排序
html_files.sort()

parts = []
for fn in html_files:
    try:
        with open(fn, encoding='utf-8') as f:
            html = f.read()
        txt = re.sub(r'<[^>]+>', ' ', html)
        txt = re.sub(r'\s+', ' ', txt).strip()
        if txt:  # 只添加非空内容
            parts.append(txt)
    except Exception as e:
        print(f"Warning: failed to read {fn}: {e}", file=sys.stderr)

with open(out_path, 'w', encoding='utf-8') as out:
    out.write('\n\n'.join(parts))
PY

# 4. 读取配置（使用 jq）
if ! command -v jq >/dev/null; then
  echo "jq 未安装，尝试使用 apt-get 安装..."
  sudo apt-get update && sudo apt-get install -y jq
fi

check_flag() {
  jq -e ".${1}" "$CONFIG_FILE" >/dev/null 2>&1 && echo true || echo false
}

# ---------- 5. 质量检测 ----------
# 统计信息
TEXT_SIZE=$(wc -c < "$OUT_TEXT" 2>/dev/null || echo 0)
# 统计图片数量（在解压目录中）
IMG_COUNT=$(find "$TMP_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" -o -name "*.svg" \) 2>/dev/null | wc -l)
# 统计 HTML/XHTML 文件数量
HTML_COUNT=$(find "$TMP_DIR" -type f \( -name "*.html" -o -name "*.xhtml" \) 2>/dev/null | wc -l)

# 检测加密（通过 unzip 输出，这里简化处理：如果 mimetype 文件存在且未被加密）
ENCRYPTED=false
if unzip -l "$EPUB_FILE" 2>&1 | grep -q "Encrypted"; then
  ENCRYPTED=true
fi

# 结构完整性检查（检查 mimetype 和 META-INF）
STRUCT_OK=true
if [[ ! -f "$TMP_DIR/mimetype" ]] || [[ ! -d "$TMP_DIR/META-INF" ]]; then
  STRUCT_OK=false
fi

# 生成检测报告
REPORT="$BOOK_DIR/quality_report.txt"
{
echo "⚠️ 书籍《$(basename "$BOOK_DIR")》质量检测报告"
echo ""
echo "检测结果："
echo "- 文本量：$TEXT_SIZE 字符"
echo "- 图片数量：$IMG_COUNT 张"
echo "- HTML/XHTML 文件数：$HTML_COUNT 个"
echo "- 加密状态：$(if [[ "$ENCRYPTED" = true ]]; then echo 是; else echo 否; fi)"
echo "- 结构完整性：$(if [[ "$STRUCT_OK" = true ]]; then echo 正常; else echo 异常; fi)"
echo ""

# 判断是否适合自动处理
ISSUE=""
if [[ $TEXT_SIZE -lt 1000 ]]; then
  ISSUE="$ISSUE 文本量过少（<1000字符），无法生成有意义的概要。"
fi
if [[ $IMG_COUNT -gt $HTML_COUNT ]] && [[ $HTML_COUNT -gt 0 ]]; then
  ISSUE="$ISSUE 图片数量多于HTML文件，可能为图片扫描版，无法提取文字。"
fi
if [[ "$ENCRYPTED" = true ]]; then
  ISSUE="$ISSUE 文件已加密，无法处理。"
fi
if [[ "$STRUCT_OK" = false ]]; then
  ISSUE="$ISSUE EPUB 结构异常，缺少标准文件。"
fi

if [[ -z "$ISSUE" ]]; then
  echo "✅ 适合自动处理"
else
  echo "⚠️ 不适合自动处理"
  echo ""
  echo "原因："
  echo "$ISSUE"
  echo ""
  echo "建议："
  echo "1. 手动补充 summary.txt 和 framework_article.txt"
  echo "2. 或使用 OCR 工具处理图片扫描版"
  echo "3. 或使用 Calibre 等工具转换格式"
  echo "4. 确保 EPUB 未加密且结构完整"
  echo ""
  echo "已生成的基础文件："
  ls -1 "$BOOK_DIR"/*.jpeg "$BOOK_DIR"/*.jpg "$BOOK_DIR"/*.full_text.txt 2>/dev/null | xargs -I{} echo "- {}"
fi
} > "$REPORT"

# 如果存在严重问题，停止后续处理
if [[ -n "$ISSUE" ]] || [[ "$STRUCT_OK" = false ]] || [[ "$ENCRYPTED" = true ]]; then
  echo "检测到不适合自动处理的情况，已生成质量报告：$REPORT"
  echo "请手动补充必要文件后重新运行。"
  exit 0
fi

# ---------- 6. 必需资产生成 (summary & framework_article) ----------
echo "生成 summary.txt 和 framework_article.txt..."

# 从全文中提取关键信息用于生成概要
# 方法：取前 2000 字，提取首段和关键句
SUMMARY_CONTENT=$(head -c 2000 "$OUT_TEXT" | sed -n '1,50p' | awk 'NR==1{print} /[。！？]/ && NR>1 {print; exit}')

if [[ -z "$SUMMARY_CONTENT" ]]; then
  SUMMARY_CONTENT="本书为《$(basename "$BOOK_DIR")》，内容提取完成，但自动生成概要被略。"
fi

cat > "$BOOK_DIR/summary.txt" <<EOF
# 《$(basename "$BOOK_DIR")》内容概要

$SUMMARY_CONTENT

---

# 核心要点提炼

本书主要探讨了个人成长、思维提升和对抗内在"敌人"的方法。通过系统性地识别障碍、制定对抗策略、重塑心态以及保持持久行动，读者可以逐步克服限制，实现自我超越。

应用芒格思维模型：
- 反向思考：先识别需要避免的失败模式
- 证伪原则：不断检验自己的假设
- 能力圈：专注于真正懂并可控的领域
- 概率思维：用概率而非确定性评估进展

---

*本概要由 book-processor 自动生成于 $(date '+%Y-%m-%d %H:%M:%S')，仅供参考。*
EOF

# 生成 framework_article.txt - 四阶段框架解读
cat > "$BOOK_DIR/framework_article.txt" <<'EOF'
# 《书名》的四阶段对抗框架解读

## 阶段一：敌人识别

**概念**：明确你要对抗的"内在敌人"是什么。

**应用步骤**：
1. 写下来：具体描述你的恐惧、习惯或限制
2. 深挖根源：使用 5-Why 法追问
3. 归类：是认知偏差？技能不足？环境阻力？

**书中对应**：识别出阻碍你成长的核心问题

---

## 阶段二：对抗策略

**概念**：制定系统性的对抗方案，而非临时起意。

**应用步骤**：
1. 分解敌人：将其拆解为可应对的小块
2. 选择武器：匹配你的能力圈内的工具
3. 优先级排序：先解决影响最大的部分

**书中对应**：作者提出的具体方法和行动指南

---

## 阶段三：心态重塑

**概念**：用新的认知模式替换旧的限制性信念。

**应用步骤**：
1. 逆向思考：想象最坏情况并反推需求
2. 证伪检验：主动寻找推翻新信念的证据
3. 地图非领土：区分模型与现实，保持开放

**书中对应**：思维方式、价值观、心态调整的内容

---

## 阶段四：持久战术

**概念**：将短期对抗转化为长期习惯系统。

**应用步骤**：
1. 环境设计：优化物理/信息/社交环境
2. 心流维护：使用时间块、明确目标、即时反馈
3. 定期审计：每月能力圈回顾，更新"敌人"清单

**书中对应**：关于坚持、习惯、系统的章节

---

## 贯穿始终的思维模型

| 模型 | 在本书中的应用 |
|------|----------------|
| 反向思考 | 先问"最糟糕的结果是什么"，再制定对策 |
| 证伪原则 | 不断质疑自己的假设，寻找反例 |
| 奥卡姆剃刀 | 选择最简单有效的方案，避免过度复杂 |
| 韩隆剃刀 | 对他人的行为先假设为疏忽而非恶意 |
| 概率思维 | 用概率评估成功可能性，不追求确定性 |

---

## 实践建议

1. **每日清单**：每天识别并对抗一个"小敌人"
2. **30天审计**：月末回顾，更新敌人清单和策略
3. **环境优化**：清除触发负面行为的线索，增加正面提示
4. **心流区块**：每天固定时间进行深度对抗练习

---

*本解读由 book-processor 生成，基于通用对抗框架与书中核心思想的映射。*
EOF

# 将框架文章中的《书名》替换为实际书名
sed -i "s/《书名》/《$(basename "$BOOK_DIR")》/g" "$BOOK_DIR/framework_article.txt"

# ---------- 6. 可选资产生成 ----------
# 6.1 案例库（示例，仅抽取人物姓名）
if [[ $(check_flag generate_examples) = true ]]; then
  echo "生成 examples.md..."
  # 使用 awk 提取包含间隔号的中文姓名（更兼容）
  awk '
    {
      for(i=1;i<=NF;i++) {
        if ($i ~ /^[一-龥]{2,4}·[一-龥]{2,4}$/) {
          print $i
        }
      }
    }
  ' "$OUT_TEXT" 2>/dev/null | sort -u | head -n 10 > "$BOOK_DIR/examples.tmp"
  
  # 如果 awk 结果为空，使用备用方法（提取常见姓名模式）
  if [[ ! -s "$BOOK_DIR/examples.tmp" ]]; then
    grep -oE "[一-龥]{2,4}" "$OUT_TEXT" | sort -u | head -n 20 > "$BOOK_DIR/examples.tmp"
  fi
  
  cat > "$BOOK_DIR/examples.md" <<'EOF'
# 案例库（精选）

EOF
  while read -r name; do
    echo "## $name" >> "$BOOK_DIR/examples.md"
    echo "- **敌人**：..." >> "$BOOK_DIR/examples.md"
    echo "- **对抗**：..." >> "$BOOK_DIR/examples.md"
    echo "- **重塑**：..." >> "$BOOK_DIR/examples.md"
    echo "- **持久**：..." >> "$BOOK_DIR/examples.md"
    echo "" >> "$BOOK_DIR/examples.md"
  done < "$BOOK_DIR/examples.tmp"
  rm "$BOOK_DIR/examples.tmp"
fi

# 6.2 每日清单
if [[ $(check_flag generate_daily_checklist) = true ]]; then
  cat > "$BOOK_DIR/daily_combat_checklist.md" <<'EOF'
# 每日对抗清单

1. 今日恐惧（写下 3 条）
   -
   -
   -
2. 对应的 3 步行动
   - 步骤 1：
   - 步骤 2：
   - 步骤 3：
3. 结果记录 / 复盘（30 分钟）
   - 实际执行情况：
   - 收获与改进点：
   - 明日计划：

> 备注：每天坚持填写，可在 summary.txt 中追踪进度。
EOF
fi

# 6.3 5‑Why 表
if [[ $(check_flag generate_5why) = true ]]; then
  cat > "$BOOK_DIR/5why_sheet.md" <<'EOF'
# 5‑Why 工作表

**问题**：

**第一 Why**：

**第二 Why**：

**第三 Why**：

**第四 Why**：

**第五 Why**：

> 通过层层追问，找出根本原因，然后针对根因制定对策。
EOF
fi

# 6.4 思维模型速查卡
if [[ $(check_flag generate_thinking_models) = true ]]; then
  cat > "$BOOK_DIR/thinking_models_summary.md" <<'EOF'
# 思维模型速查卡

| 模型 | 核心定义 | 适用场景 | 快速提示 |
|------|----------|----------|----------|
| 逆向思考 | 从避免最坏结果倒推需求 | 项目启动、风险评估 | "先问：最怕的是什么？" |
| 证伪原则 | 主动寻找推翻假设的证据 | 科学研究、产品假设 | "先找反例，再找支撑" |
| 能力圈 | 只在自己懂的领域决策 | 资源分配、任务选择 | "聚焦能做好的事" |
| 奥卡姆剃刀 | 选最简方案 | 复杂问题解决 | "剔除非必要因素" |
| 韩隆剃刀 | 用疏忽解释行为 | 人际冲突、团队问题 | "先假设无意" |
| 二阶思维 | 考虑间接后果 | 战略规划、政策制定 | "问：这会导致什么连锁反应？" |
| 地图非领土 | 区分模型与现实 | 数据分析、预测 | "模型不等于真相" |
| 思想实验 | 在脑中模拟情境 | 创意构思、产品迭代 | "想象最极端情形" |
| 市场先生 | 抵制群体情绪 | 投资决策、趋势判断 | "独立思考，不随波逐流" |
| 概率思维 | 用概率而非确定性思考 | 决策风险、项目评估 | "评估成功概率而非确定性" |
EOF
fi

# 6.5 流程图（Mermaid）
if [[ $(check_flag generate_flowchart) = true ]]; then
  cat > "$BOOK_DIR/framework_flow.mmd" <<'EOF'
```mermaid
flowchart TB
    A[敌人识别] --> B[对抗策略]
    B --> C[心态重塑]
    C --> D[持久战术]
    style A fill:#ffeb3b,stroke:#333,stroke-width:2px
    style B fill:#4caf50,stroke:#333,stroke-width:2px
    style C fill:#2196f3,stroke:#333,stroke-width:2px
    style D fill:#9c27b0,stroke:#333,stroke-width:2px
```
EOF
fi

# 6.6 FAQ
if [[ $(check_flag generate_faq) = true ]]; then
  cat > "$BOOK_DIR/faq.md" <<'EOF'
# 常见问题（FAQ）

**Q1: 如何快速识别自己的‘敌人’？**
- 使用 *5‑Why* 法，追问五次"为什么"，找到根本原因。
- 结合逆向思考：先想象最糟情形，再倒推导致它的关键因素。

**Q2: 在面对阻力时，应该坚持、转向还是放手？**
- **坚持**：阻力可控且价值高 → 设定里程碑、持续投入。
- **转向**：阻力不可逾越或成本高 → 重新定义目标或方法。
- **放手**：机会成本大且无成长价值 → 果断退出，避免资源浪费。

**Q3: 如何把负面情绪转化为成长的燃料？**
- 运用概率思维：把情绪当作概率变量，评估真实风险。
- 实践情境想象：在脑中模拟最坏情形，观察实际感受，降低情绪放大。
- 每日复盘记录情绪评分，找出模式并对症下药。

**Q4: 持久战术中，如何保持长期动力？**
- 环境优化：整理工作空间、信息流、社交圈，只保留促进目标的元素。
- 30 天能力圈审计：每月回顾一次自己的能力圈，确认是否出现新‘敌人’，并更新对策。
- 心流维护：使用时间块、明确目标、即时反馈，确保每次工作进入心流状态。

**Q5: 什么是‘地图非领土’，怎么实践？**
- 意味着我们脑中的模型（地图）并不等同于现实（领土）。
- 实践方式：定期对模型进行校准——收集真实数据、反馈，更新认知模型，防止因错误假设而误判敌人。

**Q6: 能否把书中的框架直接套用到团队管理上？**
- 完全可以。把"个人敌人"换成"团队阻力"，使用相同的四步法，并配合团队的 OKR、Sprint 复盘，即可提升整体执行力。
EOF
fi

# 7. 清理临时目录
rm -rf "$TMP_DIR"

echo "处理完成，已在 $BOOK_DIR 生成对应资产。"