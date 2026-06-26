# Install & Initialization

## 1) Prerequisites
- `curl`（必需）：调用 `news/search`
- `jq`（可选）：解析 JSON
- 可用抓取工具之一（可选）：`agent_browser` / `web_search` / `web_fetch`

## 2) Load Params from metadata.json

`{baseDir}/metadata.json` 中的 `skill.envParams` 是环境变量的唯一来源。安装时建议先从 `metadata.json` 读取，再在初始化完成后回写。

```bash
META_FILE="{baseDir}/metadata.json"

SHENME_DOMAIN="$(jq -r '.skill.envParams.SHENME_DOMAIN // empty' "$META_FILE")"
SHENME_FETCH_LIMIT="$(jq -r '.skill.envParams.SHENME_FETCH_LIMIT // "20"' "$META_FILE")"
PROFILE="$(jq -r '.skill.envParams.PROFILE // ""' "$META_FILE")"
INTEREST_LABELS="$(jq -c '.skill.envParams.INTEREST_LABELS // []' "$META_FILE")"
LANGUAGE="$(jq -r '.skill.envParams.LANGUAGE // ""' "$META_FILE")"
```

说明：
1. 时区固定为 `Asia/Shanghai`，不通过环境变量覆盖。
2. `news_label` 不在环境变量中固定，由 Agent 执行时自主选择。
3. 建议 `SHENME_FETCH_LIMIT >= 5`。
4. `PROFILE`、`INTEREST_LABELS` 与 `LANGUAGE` 需在初始化阶段生成并写入。
5. 初始化完成后，需同步回写到 `{baseDir}/metadata.json`，确保配置单一来源。

## 3) Personalization Init (PROFILE, INTEREST_LABELS & LANGUAGE)

可选 labels：`财经`、`科技`、`教育`、`社会`、`娱乐`、`港澳台`、`国际关系`。

初始化要求：
1. `PROFILE`：由用户直接填写偏好信息，生成约 100 字描述，包含内容类型偏好与表达风格偏好。
2. `INTEREST_LABELS`：从可选 labels 中选择最少 1 个、最多 3 个，使用 JSON 数组字符串。
3. `LANGUAGE`：设置日报输出语言，建议使用 `zh-CN`（中文）或 `en-US`（英文）。

用户填写流程：
1. 向用户发起简短引导问题：
  - 你最关注哪 1-3 个方向（从 `财经`、`科技`、`教育`、`社会`、`娱乐`、`港澳台`、`国际关系` 中选）？
  - 你更偏好的内容类型是什么（如行业机会、政策变化、公司动态、投融资）？
  - 你喜欢的表达风格是什么（如结论先行/数据驱动/简洁要点）？
  - 你希望日报使用哪种语言（`zh-CN` 或 `en-US`）？
2. Agent 根据用户回答生成：
  - `PROFILE`：约 100 字，总结内容偏好 + 表达风格。
  - `INTEREST_LABELS`：1-3 个合法标签的 JSON 数组字符串。
  - `LANGUAGE`：合法语言值（建议 `zh-CN` / `en-US`）。
3. 先回写 `{baseDir}/metadata.json`，再进入 export 步骤与后续安装流程。

初始化示例：
```bash
PROFILE="偏好关注科技，尤其科技创业的市场机会，重点跟踪 AI 应用、开发者工具、企业服务与企业出海，并关注中美关系变化对市场准入、供应链与合规成本的影响。阅读时优先看赛道增速、需求强度、商业模式、获客成本与竞争壁垒。表达风格偏好结构化、结论先行、数据与案例支撑，并给出可执行建议和风险提示。"
INTEREST_LABELS='["科技","国际关系","财经"]'
LANGUAGE="zh-CN"
```

可选校验（需要 `jq`）：
```bash
echo "$INTEREST_LABELS" | jq -e '
  (type == "array") and
  (length >= 1 and length <= 3) and
  all(.[]; IN("财经";"科技";"教育";"社会";"娱乐";"港澳台";"国际关系"))
' >/dev/null || {
  echo "INTEREST_LABELS 配置无效：必须为 1-3 个可选标签组成的 JSON 数组"
  exit 1
}

if [ "$LANGUAGE" != "zh-CN" ] && [ "$LANGUAGE" != "en-US" ]; then
  echo "LANGUAGE 配置无效：仅支持 zh-CN 或 en-US"
  exit 1
fi
```

## 4) Export Runtime Environment Variables

初始化并回写 `metadata.json` 完成后，再将参数导出到当前会话：

```bash
META_FILE="{baseDir}/metadata.json"

export SHENME_DOMAIN="$(jq -r '.skill.envParams.SHENME_DOMAIN // empty' "$META_FILE")"
export SHENME_FETCH_LIMIT="$(jq -r '.skill.envParams.SHENME_FETCH_LIMIT // "20"' "$META_FILE")"
export PROFILE="$(jq -r '.skill.envParams.PROFILE // ""' "$META_FILE")"
export INTEREST_LABELS="$(jq -c '.skill.envParams.INTEREST_LABELS // []' "$META_FILE")"
export LANGUAGE="$(jq -r '.skill.envParams.LANGUAGE // ""' "$META_FILE")"
```

## 5) Local Setup
```bash
SKILL_DIR="$HOME/.openclaw/workspace/skills/claws_daily"
REQUIRED_FILES=("SKILL.md" "install.md" "daily_example.md" "metadata.json")

if [ ! -d "$SKILL_DIR" ]; then
  echo "缺少技能目录: $SKILL_DIR"
  exit 1
fi

MISSING_FILES=()
for f in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$SKILL_DIR/$f" ]; then
    MISSING_FILES+=("$f")
  fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
  echo "技能文件检查不通过，缺失文件如下："
  for f in "${MISSING_FILES[@]}"; do
    echo "- $SKILL_DIR/$f"
  done
  exit 1
fi

echo "本地技能文件检查通过: $SKILL_DIR"
```

## 6) Heartbeat Scheduling
在初始化阶段创建并维护 OpenClaw Heartbeat，每天触发两次：
1. `09:00`（Asia/Shanghai）：处理前一天 `18:00` 到当天 `09:00` 的资讯。
2. `18:00`（Asia/Shanghai）：处理当天 `09:00` 到当天 `18:00` 的资讯。

执行幂等要求：同一时间窗只允许生成并推送一次，重复触发识别为同批次重试。

## 7) API Call Examples
单标签检索：
```bash
NEWS_LABEL="科技"

curl -s -G "https://${SHENME_DOMAIN}/api/v2/news/search" \
  --data-urlencode "label=${NEWS_LABEL}" \
  --data-urlencode "limit=${SHENME_FETCH_LIMIT}"
```

多标签检索（结果需再合并去重与排序）：
```bash
for NEWS_LABEL in "科技" "国际关系"; do
  curl -s -G "https://${SHENME_DOMAIN}/api/v2/news/search" \
    --data-urlencode "label=${NEWS_LABEL}" \
    --data-urlencode "limit=${SHENME_FETCH_LIMIT}"
done
```
