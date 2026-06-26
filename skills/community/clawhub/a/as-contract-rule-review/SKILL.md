---
name: contract-rule-review
description: 合同规则审阅助手 - 上传本地合同文件到 AnyShare 并调用规则审阅技能进行自动化审阅，支持保存结果和生成分享链接
version: 2.0.0
triggers: ["审阅合同", "规则检查", "合同审核"]
---

> **安全与排障文档**（必读）
> - 配置/Token 管理 → 本文件「🚀 首次配置」章节
> - 错误排查 → [references/troubleshooting.md](references/troubleshooting.md)
> - 安全约束与审计 → [SECURITY.md](SECURITY.md)

---

# Contract Rule Review

合同规则审阅助手：
1. 上传桌面合同文件到 AnyShare 个人文档库
2. **获取审阅模板**（默认使用内置模板，**支持用户自定义模板**）
3. 调用 `__规则审阅__1` 技能进行审阅
4. **保存审阅结果到「合同审阅/日期/合同名称/」目录结构并生成分享链接**

---

## 🚀 首次配置

### 术语说明

| 术语 | 含义 |
|------|------|
| Access Token | AnyShare 用户访问令牌，用于 API 身份认证 |
| 个人文档库 GNS | 个人文档库的 GNS 路径标识 |

### Step 1: 配置 MCP 服务与 Token

本技能依赖 `anyshare-asmcp` MCP 服务，Token 须预先配置到 `~/.openclaw/workspace/config/mcporter.json`：

```json
{
  "mcpServers": {
    "anyshare-asmcp": {
      "type": "Streamable",
      "url": "https://anyshare.aishu.cn/asmcp/",
      "headers": {
        "Authorization": "Bearer <your_token_here>"
      }
    }
  }
}
```

获取 Token：登录 AnyShare Web → 右上角头像 → MCP授权凭证 → 复制令牌。

### Step 2: 验证连通性

```bash
mcporter call anyshare-asmcp.doc_lib_owned
```

返回文档库列表即表示认证成功。

### Step 3: 配置 OpenClaw 运行时超时（针对长耗时调用）

编辑 `~/.openclaw/config.toml`，在 `[skills]` 或 `[skills.entries.contract-rule-review]` 下添加：

```toml
[skills.entries.contract-rule-review]
env.MCPORTER_CALL_TIMEOUT = "600000"  # 10 分钟，毫秒
```

或通过 `gateway config.patch` 更新。

### Step 4: 确认个人文档库 GNS

首次运行后，技能会自动将个人文档库 GNS 记录到日志输出中（`PERSONAL_DOC_LIB_GNS: gns://...`），后续无需重复配置。

---


## 目录结构设计

```
个人文档库/
└── 合同审阅/                    ← 主目录（复用已存在的）
    └── 2026-04-27/             ← 日期目录（每天新建）
        └── 储能电站合同/       ← 合同名称目录
            ├── 合同原文/       ← 上传的原始合同文件
            │   └── 储能电站能源管理合同.docx
            └── 审阅报告.md     ← 生成的审阅报告
```

**严格遵守**：合同原文必须上传到「合同原文/」子目录，审阅报告直接放在合同名称目录下。

---

## 模板配置

技能支持两种模板获取方式：

| 优先级 | 模板类型 | 来源 | 说明 |
|-------|---------|------|------|
| **优先** | 内置模板 | API 获取 | 调用 `__规则审阅__1` 内置模板接口 |
| **备用** | 本地模板 | 本地 `.md` 文件 | 模板获取失败时的兜底方案 |
| **用户自定义** | 自定义模板 | 用户提供 | **用户指定模板时优先使用用户模板** |

---

### 方式一：API 获取内置模板（推荐）

```bash
# 获取内置规则审阅模板
TEMPLATE_RESPONSE=$(curl -s -X GET \
  "https://anyshare.aishu.cn/api/intelli-search/v1/skills/templates/default?skill_name=__规则审阅__1" \
  -H "authorization: $ACCESS_TOKEN" \
  -H "content-type: application/json")

# 解析模板内容
TEMPLATE_CONTENT=$(echo "$TEMPLATE_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('template',''))" 2>/dev/null)
TEMPLATE_SOURCE="内置模板(API)"

if [ -z "$TEMPLATE_CONTENT" ]; then
    echo "⚠️ API获取模板失败，尝试本地模板..."
    # 落入本地模板逻辑
else
    echo "✅ 使用内置模板（API获取）"
    echo "   模板长度: ${#TEMPLATE_CONTENT} 字符"
fi
```

---

### 方式二：本地模板读取（兜底）

```bash
# 读取本地模板
TEMPLATE_DIR="$HOME/.openclaw/skills/contract-rule-review/templates"

case "$CONTRACT_TYPE" in
  "采购"|"采购合同")
    TEMPLATE_FILE="$TEMPLATE_DIR/采购合同审阅模板.md"
    ;;
  "服务"|"服务合同")
    TEMPLATE_FILE="$TEMPLATE_DIR/服务合同审阅模板.md"
    ;;
  *)
    TEMPLATE_FILE="$TEMPLATE_DIR/通用合同审阅模板.md"
    ;;
esac

if [ -f "$TEMPLATE_FILE" ]; then
    TEMPLATE_CONTENT=$(cat "$TEMPLATE_FILE")
    echo "✅ 使用本地模板: $(basename $TEMPLATE_FILE)"
else
    echo "⚠️ 本地模板不存在，使用默认模板"
    TEMPLATE_CONTENT="请按照通用合同审阅标准进行审阅"
fi
```

---

## 工作流程

```
用户请求 ──→ 获取模板 ──→ 创建目录结构 ──→ 上传合同原文 ──→ temporary-area ──→ index-check轮询 ──→ smart_assistant ──→ 保存审阅报告 ──→ 生成分享链接
                            │              ↓              ↓                  ↓              ↓                    ↓                    ↓                    ↓
                        API获取内置   dir_create       file_osbegin       file_osendupload  POST             index-check API      file_osbegin         file_sharedlink
                        失败则本地   (4级目录)                            → file_osendupload   temporary-area   (最多600秒)         file_osendupload      _realname_create
```

---

## 完整调用示例

```bash
#!/bin/bash

# ========== 配置 ==========
# Token 须预先配置到 ~/.openclaw/workspace/config/mcporter.json
# 以下变量由 mcporter 自动注入，无需在此硬编码
# ACCESS_TOKEN 由 mcporter call 工具通过 --access_token 参数传递
PERSONAL_DOC_LIB_GNS="your_personal_doc_lib_gns_here"
LOCAL_FILE="~/Desktop/合同/采购合同.docx"
CONTRACT_TYPE="采购合同"
FILE_NAME=$(basename "$LOCAL_FILE")
FILE_SIZE=$(stat -f%z "$LOCAL_FILE")
TODAY_DIR=$(date +%Y-%m-%d)

echo "=========================================="
echo "📋 合同规则审阅 v1.8.2"
echo "=========================================="

# ========== Step 1: 获取模板 ==========
echo ""
echo "📄 获取审阅模板..."

TEMPLATE_RESPONSE=$(curl -s -X GET \
  "https://anyshare.aishu.cn/api/intelli-search/v1/skills/templates/default?skill_name=__规则审阅__1" \
  -H "authorization: $ACCESS_TOKEN" \
  -H "content-type: application/json")

TEMPLATE_CONTENT=$(echo "$TEMPLATE_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('template',''))" 2>/dev/null)
TEMPLATE_SOURCE="内置模板(API)"

if [ -z "$TEMPLATE_CONTENT" ]; then
    echo "⚠️ API获取失败，尝试本地模板..."
    TEMPLATE_DIR="$HOME/.openclaw/skills/contract-rule-review/templates"
    case "$CONTRACT_TYPE" in
      "采购合同") TEMPLATE_FILE="$TEMPLATE_DIR/采购合同审阅模板.md" ;;
      "服务合同") TEMPLATE_FILE="$TEMPLATE_DIR/服务合同审阅模板.md" ;;
      *) TEMPLATE_FILE="$TEMPLATE_DIR/通用合同审阅模板.md" ;;
    esac
    if [ -f "$TEMPLATE_FILE" ]; then
        TEMPLATE_CONTENT=$(cat "$TEMPLATE_FILE")
        TEMPLATE_SOURCE=$(basename "$TEMPLATE_FILE")
    else
        TEMPLATE_CONTENT="请按照通用合同审阅标准进行审阅"
        TEMPLATE_SOURCE="默认模板"
    fi
fi
echo "✅ 使用模板: $TEMPLATE_SOURCE"

# ========== Step 2: 创建目录结构（4级） ==========
echo ""
echo "📁 创建目录结构..."

# 辅助函数：检查目录是否已存在，返回完整GNS
# 关键：folder_sub_objects 用真实ID查询才能返回子目录，用中文路径名查会返回空
check_dir_exists() {
    local parent_gns="$1"
    local dir_name="$2"
    local result=$(mcporter call anyshare-asmcp.folder_sub_objects \
        access_token:"$ACCESS_TOKEN" \
        id:"$parent_gns" limit:100 2>&1)
    echo "$result" | python3 -c "
import sys,json
data=json.load(sys.stdin)
for d in data.get('dirs',[]):
    if d.get('name')=='$dir_name':
        print(d.get('id',''))
        break
" 2>/dev/null
}

# 1. 主目录 "合同审阅"
# 先用 check_dir_exists 查；查不到则创建，创建后必须用返回值中的真实 id
MAIN_DIR_GNS=$(check_dir_exists "$PERSONAL_DOC_LIB_GNS" "合同审阅")
if [ -z "$MAIN_DIR_GNS" ]; then
    MAIN_DIR_RESULT=$(mcporter call anyshare-asmcp.dir_create \
        access_token:"$ACCESS_TOKEN" \
        docid:"$PERSONAL_DOC_LIB_GNS" \
        name:"合同审阅" 2>&1)
    MAIN_DIR_GNS=$(echo "$MAIN_DIR_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('docid',''))" 2>/dev/null)
    if [ -z "$MAIN_DIR_GNS" ]; then
        echo "⚠️ 主目录创建失败，无法继续"
        exit 1
    fi
fi

# 2. 日期目录
DATE_DIR_GNS=$(check_dir_exists "$MAIN_DIR_GNS" "$TODAY_DIR")
if [ -z "$DATE_DIR_GNS" ]; then
    DATE_DIR_RESULT=$(mcporter call anyshare-asmcp.dir_create \
        access_token:"$ACCESS_TOKEN" \
        docid:"$MAIN_DIR_GNS" \
        name:"$TODAY_DIR" 2>&1)
    DATE_DIR_GNS=$(echo "$DATE_DIR_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('docid',''))" 2>/dev/null)
    if [ -z "$DATE_DIR_GNS" ]; then
        echo "⚠️ 日期目录创建失败，无法继续"
        exit 1
    fi
fi

# 3. 合同名称目录
CONTRACT_DIR_NAME="${FILE_NAME%.docx}"
CONTRACT_DIR_GNS=$(check_dir_exists "$DATE_DIR_GNS" "$CONTRACT_DIR_NAME")
if [ -z "$CONTRACT_DIR_GNS" ]; then
    CONTRACT_DIR_RESULT=$(mcporter call anyshare-asmcp.dir_create \
        access_token:"$ACCESS_TOKEN" \
        docid:"$DATE_DIR_GNS" \
        name:"$CONTRACT_DIR_NAME" 2>&1)
    CONTRACT_DIR_GNS=$(echo "$CONTRACT_DIR_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('docid',''))" 2>/dev/null)
    if [ -z "$CONTRACT_DIR_GNS" ]; then
        echo "⚠️ 合同目录创建失败，无法继续"
        exit 1
    fi
fi

# 4. 「合同原文」子目录
ORIG_DIR_GNS=$(check_dir_exists "$CONTRACT_DIR_GNS" "合同原文")
if [ -z "$ORIG_DIR_GNS" ]; then
    ORIG_DIR_RESULT=$(mcporter call anyshare-asmcp.dir_create \
        access_token:"$ACCESS_TOKEN" \
        docid:"$CONTRACT_DIR_GNS" \
        name:"合同原文" 2>&1)
    ORIG_DIR_GNS=$(echo "$ORIG_DIR_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('docid',''))" 2>/dev/null)
    if [ -z "$ORIG_DIR_GNS" ]; then
        echo "⚠️ 合同原文目录创建失败，无法继续"
        exit 1
    fi
fi

echo "✅ 目录: 合同审阅/$TODAY_DIR/$CONTRACT_DIR_NAME/合同原文/"
echo "   合同目录: $CONTRACT_DIR_GNS"
echo "   合同原文目录: $ORIG_DIR_GNS"

# ========== Step 3: 上传合同原文到「合同原文」子目录 ==========
echo ""
echo "📤 上传合同原文到「合同原文/」..."

UPLOAD=$(mcporter call anyshare-asmcp.file_osbeginupload \
  access_token:"$ACCESS_TOKEN" \
  docid:"$ORIG_DIR_GNS" \
  name:"$FILE_NAME" \
  length:$FILE_SIZE 2>&1)

URL=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][1])")
AUTH=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][2])")
DATE=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][4])")
DOCID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['docid'])")
REV=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['rev'])")

cat "$LOCAL_FILE" | curl -s -X PUT \
  -H "$AUTH" \
  -H "Content-Type: application/octet-stream" \
  -H "$DATE" \
  -T - \
  "$URL" > /dev/null 2>&1

END_RESULT=$(mcporter call anyshare-asmcp.file_osendupload \
  access_token:"$ACCESS_TOKEN" \
  docid:"$DOCID" \
  rev:"$REV" 2>&1)

END_CODE=$(echo "$END_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code',0))" 2>/dev/null)
SHORT_ID=$(echo "$DOCID" | awk -F'/' '{print $NF}')

if [ "$END_CODE" = "0" ] || [ -z "$END_CODE" ]; then
    echo "✅ 合同原文上传完成: $SHORT_ID"
    UPLOAD_SUCCESS=true
else
    echo "⚠️ 合同原文上传失败: code=$END_CODE"
    echo "   响应: $END_RESULT"
    SHORT_ID=""
    UPLOAD_SUCCESS=false
fi

# ========== Step 4: 上传至临时区域（仅上传成功时） ==========
if [ "$UPLOAD_SUCCESS" = true ]; then
echo ""
echo "📤 上传至临时区域..."

TEMPORARY_AREA_RESULT=$(curl -s -X POST \
    "https://anyshare.aishu.cn/api/intelli-search/v1/temporary-area" \
    -H "authorization: $ACCESS_TOKEN" \
    -H "content-type: application/json" \
    -d "{\"source\":[{\"id\":\"$SHORT_ID\",\"type\":\"doc\"}],\"bot_id\":\"smart_assistant\"}" 2>&1)

TEMPORARY_AREA_CODE=$(echo "$TEMPORARY_AREA_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code',0))" 2>/dev/null)
if [ "$TEMPORARY_AREA_CODE" = "0" ] || [ -z "$TEMPORARY_AREA_CODE" ]; then
    echo "✅ 临时区域上传成功"
else
    echo "⚠️ 临时区域上传返回: $TEMPORARY_AREA_RESULT"
fi
else
    echo "⚠️ 跳过临时区域（上传失败）"
fi

# ========== Step 5: 等待索引建立（仅上传成功时） ==========
if [ "$UPLOAD_SUCCESS" = true ]; then
echo ""
echo "⏳ 等待索引建立..."

# 注意：file_osendupload 返回值中不包含 details 字段
# 因此 FILE_DETAILS 直接使用文件短 ID 构建，details 留空
# 关键：index-check 不带 retry=false，让索引服务重新处理文件
FILE_DETAILS="[{\"id\":\"$SHORT_ID\",\"type\":\"doc\",\"details\":{}}]"
echo "✅ FILE_DETAILS 已构建（details 留空，由 temporary-area 触发索引）"

MAX_WAIT=600
INTERVAL=5
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
    INDEX_CHECK_RESULT=$(curl -s -X POST \
        "https://anyshare.aishu.cn/api/intelli-search/v1/index-check?target_index=pageindex" \
        -H "authorization: $ACCESS_TOKEN" \
        -H "content-type: application/json" \
        -d "$FILE_DETAILS" 2>&1)
    PROCESS=$(echo "$INDEX_CHECK_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('process',0))" 2>/dev/null)
    if [ "$PROCESS" = "100" ]; then
        echo "✅ 索引建立完成（${ELAPSED}秒）"
        break
    else
        echo "   索引进度: ${PROCESS:-0}%（${ELAPSED}秒）..."
        sleep $INTERVAL
        ELAPSED=$((ELAPSED + INTERVAL))
    fi
done
[ $ELAPSED -ge $MAX_WAIT ] && echo "⚠️ 索引超时，继续..."

# ========== Step 6: 调用 smart_assistant 审阅（仅上传成功时） ==========
if [ "$UPLOAD_SUCCESS" = true ]; then
echo ""
echo "🔍 执行规则审阅..."

REPORT_CONTENT=$(mcporter call anyshare-asmcp.smart_assistant \
  --timeout 180000 \
  access_token:"$ACCESS_TOKEN" \
  query:"帮我审核这份合同，按照以下模板审阅：$TEMPLATE_CONTENT" \
  skill_name:"__规则审阅__1" \
  source_ranges:"[{\"id\":\"$SHORT_ID\",\"type\":\"doc\"}]" 2>&1)

REPORT_CONTENT=$(echo "$REPORT_CONTENT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('completion_answer',''))" 2>/dev/null)

if [ -z "$REPORT_CONTENT" ]; then
    echo "⚠️ 审阅返回内容为空"
    REPORT_CONTENT="审阅失败，未获取到审阅内容"
else
    echo "✅ 审阅完成"
fi
else
    echo "⚠️ 跳过审阅（合同原文上传失败）"
    REPORT_CONTENT="合同原文上传失败，无法进行审阅。"
fi

# ========== Step 7: 保存审阅报告到合同目录 ==========
echo ""
echo "📄 保存审阅报告..."

REPORT_FILE="审阅报告.md"
REPORT_SIZE=${#REPORT_CONTENT}

REPORT_BEGIN=$(mcporter call anyshare-asmcp.file_osbeginupload \
  access_token:"$ACCESS_TOKEN" \
  docid:"$CONTRACT_DIR_GNS" \
  name:"$REPORT_FILE" \
  length:$REPORT_SIZE 2>&1)

AUTH_H=$(echo "$REPORT_BEGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][2])")
DATE_H=$(echo "$REPORT_BEGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][4])")
UPLOAD_URL=$(echo "$REPORT_BEGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][1])")
R_DOCID=$(echo "$REPORT_BEGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['docid'])")
R_REV=$(echo "$REPORT_BEGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['rev'])")

# ⚠️ 必须使用原始 Content-Type (application/octet-stream)，不得覆盖
echo -n "$REPORT_CONTENT" | curl -s -X PUT \
  -H "$AUTH_H" \
  -H "Content-Type: application/octet-stream" \
  -H "$DATE_H" \
  -T - \
  "$UPLOAD_URL" > /dev/null 2>&1

mcporter call anyshare-asmcp.file_osendupload \
  access_token:"$ACCESS_TOKEN" \
  docid:"$R_DOCID" \
  rev:"$R_REV" > /dev/null 2>&1

echo "✅ 审阅报告已保存"

# ========== Step 8: 生成分享链接 ==========
echo ""
echo "🔗 生成分享链接..."

SHARE_RESULT=$(mcporter call anyshare-asmcp.file_sharedlink_realname_create \
  access_token:"$ACCESS_TOKEN" \
  item:"{\"id\":\"$R_DOCID\",\"type\":\"file\"}" 2>&1)

SHARE_URL=$(echo "$SHARE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('link_url','生成失败'))" 2>/dev/null)

# ========== 输出结果 ==========
if [ "$UPLOAD_SUCCESS" = true ]; then
    ORIG_STATUS="✅ 合同原文/$FILE_NAME"
else
    ORIG_STATUS="⚠️ 合同原文（上传失败）"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 审阅完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📄 $ORIG_STATUS"
echo "📄 审阅报告：$REPORT_FILE"
echo "📍 保存位置："
echo "   个人文档库/合同审阅/$TODAY_DIR/$CONTRACT_DIR_NAME/"
if [ "$UPLOAD_SUCCESS" = true ]; then
    echo "   ├─ 合同原文/$FILE_NAME"
    echo "   └─ 审阅报告.md"
else
    echo "   └─ 审阅报告.md"
fi
echo "🔗 分享链接：$SHARE_URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## MCP Tool 完整列表

| Tool | 用途 | 调用阶段 |
|-----|------|---------|
| `dir_create` | 创建目录（4级） | Step 2 |
| `folder_sub_objects` | 检查目录是否存在 | Step 2 |
| `file_osbeginupload` | 获取上传凭证 | Step 3, Step 7 |
| `file_osendupload` | 确认上传完成 | Step 3, Step 7 |
| `smart_assistant` | 规则审阅 | Step 6 |
| `file_sharedlink_realname_create` | 创建分享链接 | Step 8 |

---

## 依赖

- **模板目录**: `~/.openclaw/skills/contract-rule-review/templates/`
- **MCP**: `anyshare-asmcp`
- **Tools**: `file_osbeginupload`, `file_osendupload`, `dir_create`, `folder_sub_objects`, `smart_assistant`, `file_sharedlink_realname_create`

---

## 注意

- 需预先配置 `PERSONAL_DOC_LIB_GNS`（个人文档库GNS路径）和有效的 `ACCESS_TOKEN`
- **目录结构严格遵守**：合同原文必须上传到「合同原文/」子目录，审阅报告直接放在合同名称目录下
- **上传 curl 命令**：`Content-Type` 必须使用原始的 `application/octet-stream`，不得覆盖，否则签名失败
- **目录复用逻辑**：使用 `folder_sub_objects` 检查已存在目录，避免重复创建
- 分享链接为实名链接

---

*版本：2.0.0*
