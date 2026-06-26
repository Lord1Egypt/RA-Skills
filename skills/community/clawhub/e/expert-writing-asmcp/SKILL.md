---
name: expert-writing-asmcp
description: 基于 AnyShare 的专家写作助手 - 上传项目文件到文档库，调用全文写作技能生成大纲文档，确认后基于大纲生成正文
version: 2.1.1
triggers: ["专家写作", "asmcp写作", "帮我写作", "基于资料写作"]
---

> **安全与排障文档**（必读）
> - 配置/Token 管理 → 本文件「🚀 首次配置」章节
> - 错误排查 → [references/troubleshooting.md](references/troubleshooting.md)
> - 安全约束与审计 → [SECURITY.md](SECURITY.md)

---

# Expert Writing ASMCP - 专家写作助手

基于 AnyShare ASMCP 的全文写作工具，采用「大纲 → 确认 → 正文」两阶段流程。

---

## 🚀 首次配置

### 术语说明

| 术语 | 含义 |
|------|------|
| Access Token | AnyShare 用户访问令牌，用于 API 身份认证 |
| source_ranges | 写作引用的源文档范围，格式为 `[{"id":"短ID","type":"doc"}]` |
| skill_name | 写作技能标识：`__全文写作__3`（大纲）、`__大纲写作__1`（正文） |

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

### Step 3: 配置 OpenClaw 运行时超时（必须）

正文生成为长耗时调用，**必须**在 `~/.openclaw/config.toml` 中配置超时：

```toml
[skills.entries.expert-writing-asmcp]
env.MCPORTER_CALL_TIMEOUT = "300000"  # 5 分钟，毫秒
```

或使用 `gateway config.patch`：

```json
{
  "skills": {
    "entries": {
      "expert-writing-asmcp": {
        "env": {
          "MCPORTER_CALL_TIMEOUT": "300000"
        }
      }
    }
  }
}
```

---


---

## ⚠️ 核心流程约束

### 大纲确认规则

| 场景 | 处理方式 |
|-----|---------|
| 用户确认大纲 | 进入生成正文阶段 |
| 用户要求修改大纲 | 1. 修改大纲内容 2. 保存为"大纲v2.md" 3. 展示给用户确认 4. **等待用户明确确认** 5. 才能写正文 |
| 用户说"可以了"/"没问题" | 必须用户说"确认，开始写正文"才算确认 |
| **5分钟无响应** | **自动进入写正文环节**（不再等待） |

### 关键原则

1. **大纲确认后才能写正文** - 必须得到用户明确回复"确认，开始写正文"
2. **修改大纲必须重新确认** - 任何大纲调整都需要新版大纲+用户确认
3. **大纲微调≠重新生成** - 只修改用户要求的内容，其他章节保持不变
4. **超时自动执行** - 展示大纲后等待5分钟，如用户无操作则自动进入写正文

---

## ⚠️ 关键经验总结（2026-05-08 更新）

### 1. 正文生成技能区分

| 任务 | 技能 | times | 说明 |
|-----|------|-------|------|
| 生成大纲 | `__全文写作__3` | `times=0` | 基于模板生成章节结构 |
| 生成正文 | `__大纲写作__1` | `times=1` | 基于大纲生成完整正文内容 |

**重要**：生成正文必须用 `__大纲写作__1` + `times=1`，不要用 `__全文写作__3`（它会把正文需求也输出成提纲"本节将..."格式）

### 2. 超时问题

- **默认超时**：mcporter 默认 60000ms（60秒），完整正文生成会超时
- **解决方案**：调用时必须加 `--timeout 180000`（180秒）或设置环境变量 `MCPORTER_CALL_TIMEOUT=300000`
- 示例：`mcporter call ... --timeout 180000`

### 3. source_ranges JSON 格式

- 格式必须严格为：`[{"id":"短ID","type":"doc"}]`
- 如果 JSON 格式不正确，会报错：`cannot unmarshal string into Go struct`
- 建议使用 Python 脚本构建参数，避免 shell 转义问题

### 4. selection 传大纲内容

- 生成正文时，`selection` 参数传入大纲完整内容
- 大纲内容较长时，建议通过文件读取后传递给脚本（避免 shell 特殊字符冲突）

### 5. 建议的 Python 脚本方式

复杂参数（大纲内容、超长 query）建议用 Python 构建脚本，避免 shell 转义问题：

```bash
# 保存大纲内容到文件
python3 -c "import json; print(json.load(open('/tmp/template_outline.json')).get('document_content',''))" > /tmp/selection.txt

# 通过文件传递
nohup bash -c 'mcporter call ... selection:"$(cat /tmp/selection.txt)" skill_name:__大纲写作__1 times:1 --timeout 180000' &
```

---

## 使用流程

```
用户：帮我写个技术总结，基于这些项目资料
      ↓
系统：请上传项目文件或提供文件路径
      ↓
用户：[上传文件：技术方案.docx, 会议纪要.pdf]
      ↓
系统：📤 上传中... ⏳ 等待索引... ✅ 完成
      ↓
系统：📄 获取内置写作模板...
      ↓
系统：🔍 正在生成大纲文档...
      ↓
系统：
      ┌─────────────────────────────────────┐
      │ 📄 大纲已生成并保存                  │
      │ 位置：文档库/写作成果/           │
      │        2025-04-22/技术总结/          │
      │        大纲.md                       │
      │                                     │
      │ 内容预览：                          │
      │ 1. 项目背景                         │
      │ 2. 技术方案概述                     │
      │ 3. 实施过程                         │
      │ 4. 成果与总结                       │
      └─────────────────────────────────────┘
      请确认大纲，如需修改请告诉我
      ↓
用户：确认，开始生成正文  ← 5分钟内确认
      ↓
或：5分钟后无响应 → 自动进入写正文
      ↓
系统：✍️ 正在基于大纲生成正文（使用 __大纲写作__1 + times:1）...
      ↓
系统：
      ✅ 写作完成
      📄 大纲：写作成果/2025-04-22/技术总结/大纲.md
      📄 正文：写作成果/2025-04-22/技术总结/正文.md
      📁 原文：写作成果/2025-04-22/技术总结/参考资料/
      🔗 分享链接：https://anyshare.aishu.cn/link/xxx
```

---

## 模板配置

技能支持两种大纲生成方式：

| 优先级 | 模板类型 | 来源 | 说明 |
|-------|---------|------|------|
| **优先** | 内置模板 | API 获取 | 调用 `__全文写作__3` 内置模板接口，基于模板结构生成大纲 |
| **备用** | 无模板 | 直接生成 | 直接基于项目资料和query生成大纲 |

### 方式一：API 获取内置模板（推荐）

```bash
# 获取内置全文写作模板
curl -s -X GET \
  "https://anyshare.aishu.cn/api/intelli-search/v1/skills/templates/default?skill_name=__全文写作__3" \
  -H "authorization: $ACCESS_TOKEN" \
  -H "content-type: application/json" > /tmp/template_response.json

TEMPLATE_CONTENT=$(python3 -c "import json; print(json.load(open('/tmp/template_response.json')).get('template',''))")

if [ -z "$TEMPLATE_CONTENT" ]; then
    echo "⚠️ API获取模板失败，使用直接生成方式"
else
    echo "✅ 使用内置模板（API获取），${#TEMPLATE_CONTENT} 字符"
fi
```

---

## 📋 写作场景模板

技能内置了 9 种专业写作场景模板，涵盖常用写作需求。

### 模板列表

| 编号 | 模板名称 | 适用场景 | 核心章节 |
|-----|---------|---------|---------|
| 1 | 可行性研究报告 | 项目立项、技术改造 | 项目概述、市场分析、技术方案、投资估算、效益分析、风险分析 |
| 2 | 项目建议书 | 立项申请、审批汇报 | 项目概况、必要性分析、建设方案、投资估算、效益分析 |
| 3 | 商业计划书 | 创业融资、商务合作 | 执行摘要、市场分析、商业模式、财务预测、融资计划 |
| 4 | 技术方案 | 实施方案、技术评审 | 需求分析、总体设计、详细设计、实施计划、风险分析 |
| 5 | 项目总结报告 | 项目复盘、经验沉淀 | 项目概述、实施过程、成果交付、经验教训、后续建议 |
| 6 | 市场调研报告 | 市场分析、行业研究 | 市场概况、竞争分析、用户分析、市场趋势、结论建议 |
| 7 | 产品介绍文档 | 产品宣传、方案展示 | 产品概述、功能介绍、应用场景、技术优势、案例展示 |
| 8 | 年度工作报告 | 部门总结、年度汇报 | 年度概述、重点工作、业绩成果、问题分析、下年计划 |
| 9 | 解决方案 | 投标文件、客户方案 | 需求理解、方案设计、产品介绍、实施保障、服务保障 |

### 如何使用模板

**方式一：用户选择模板**

用户在写作时指定模板名称（如"用商业计划书写"），技能自动调用对应模板结构生成大纲。

**方式二：用户描述场景，技能自动匹配**

- 用户说"帮我写个融资用的计划书" → 自动匹配【商业计划书】
- 用户说"写个项目立项报告" → 自动匹配【项目建议书】
- 用户说"做个市场调研" → 自动匹配【市场调研报告】

### 模板匹配逻辑（内置于技能 prompt）

```
当用户提到以下关键词时，自动匹配对应模板：
- "融资" / "商业计划" / "BP" → 商业计划书
- "项目立项" / "项目建议" / "可研" → 可行性研究报告 或 项目建议书
- "技术方案" / "实施方案" / "技术设计" → 技术方案
- "项目总结" / "复盘" / "总结报告" → 项目总结报告
- "市场调研" / "行业分析" / "调研报告" → 市场调研报告
- "产品介绍" / "产品宣传" / "产品手册" → 产品介绍文档
- "年度总结" / "年度报告" / "年度汇报" → 年度工作报告
- "投标" / "解决方案" / "客户方案" → 解决方案
- 默认 → 可行性研究报告
```

### 模板结构文件

详细模板结构定义保存在：
```
templates/
├── README.md                    # 模板分类索引
├── 文档类/                      # 项目立项类文档
│   ├── 01_可行性研究报告.md
│   ├── 02_项目建议书.md
│   └── 03_商业计划书.md
├── 报告类/                      # 总结汇报类文档
│   ├── 04_项目总结报告.md
│   ├── 05_年度工作报告.md
│   └── 06_市场调研报告.md
└── 方案类/                      # 技术/商务方案
    ├── 07_技术方案.md
    ├── 08_产品介绍文档.md
    └── 09_解决方案.md
```

包含 9 种模板的完整章节结构，每种模板独立文件方便维护。

---

## 目录结构设计

```
文档库/
├── 写作成果/                    ← 主目录（复用已存在的）
│   └── 2025-04-22/             ← 日期目录（每天新建）
│       └── 项目名称/           ← 项目专属目录
│           ├── 参考资料/       ← 上传的原始文件
│           │   ├── 技术方案.docx
│           │   └── 会议纪要.pdf
│           ├── 大纲.md         ← 生成的大纲
│           └── 正文.md         ← 生成的正文
└── ...
```

---

## MCP Tool 调用详解

### 1. smart_assistant (大纲生成: __全文写作__3 / 正文生成: __大纲写作__1)

**用途**：
- 调用 `__全文写作__3`（times=0）生成大纲
- 调用 `__大纲写作__1`（times=1）生成完整正文

**⚠️ 正文生成必须加 --timeout**：默认 60 秒会超时，必须加 `--timeout 180000`

```bash
# 生成大纲 (times=0) - 使用 __全文写作__3
mcporter call anyshare-asmcp.smart_assistant \
    bot_id:smart_assistant \
    query:"写作主题：项目可行性研究报告" \
    skill_name:__全文写作__3 \
    source_ranges:"[{\"id\":\"短ID\",\"type\":\"doc\"}]" \
    times:0

# 生成正文 (times=1, selection=大纲) - 使用 __大纲写作__1（必须加 --timeout）
SHORT_ID=$(cat /tmp/verify_short_id.txt)
OUTLINE=$(python3 -c "import json; print(json.load(open('/tmp/template_outline.json')).get('document_content',''))")

nohup mcporter call anyshare-asmcp.smart_assistant \
    bot_id:smart_assistant \
    query:"基于以下大纲，撰写完整的可行性研究报告正文内容" \
    selection:"$OUTLINE" \
    skill_name:__大纲写作__1 \
    source_ranges:"[{\"id\":\"$SHORT_ID\",\"type\":\"doc\"}]" \
    times:1 \
    --timeout 180000 > /tmp/writing_result.json 2>&1 &
```

**参数说明**：

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|-----|
| bot_id | string | 是 | 固定值 "smart_assistant" |
| query | string | 是 | 查询文本 |
| skill_name | string | 是 | 大纲用 `__全文写作__3`，正文用 `__大纲写作__1` |
| source_ranges | string | 是 | 文件ID列表，格式: `[{"id":"xxx","type":"doc"}]` |
| selection | string | 生成正文时 | 传入大纲完整内容 |
| times | int | 是 | 0=大纲，1=正文 |

**返回结构**：
```json
{
  "code": 0,
  "document_content": "生成的完整内容...",
  "status": "completed"
}
```

**注意**：从 `document_content` 字段获取生成的内容

---

### 2. folder_sub_objects (目录复用检查)

**用途**：列出目录内容，检查是否已存在同名目录

```bash
mcporter call anyshare-asmcp.folder_sub_objects \
    access_token="$ACCESS_TOKEN" \
    id="$PARENT_GNS" \
    limit=100
```

**返回**：
```json
{
  "dirs": [
    {"name": "写作成果", "id": "gns://xxx/yyy"}
  ],
  "files": [...]
}
```

---

### 3. dir_create (创建目录)

```bash
mcporter call anyshare-asmcp.dir_create \
    access_token="$ACCESS_TOKEN" \
    docid="$PARENT_GNS" \
    name="目录名"
```

---

### 4. file_osbeginupload / file_osendupload (上传文件)

```bash
# 开始上传
UPLOAD=$(mcporter call anyshare-asmcp.file_osbeginupload \
    access_token="$ACCESS_TOKEN" \
    docid="$TARGET_DIR" \
    name="文件名.docx" \
    length=12345)

# 提取凭证
URL=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][1])")
AUTH=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][2])")
DATE=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][4])")
DOCID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['docid'])")
REV=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['rev'])")

# 上传文件
curl -X PUT -H "$AUTH" -H "Content-Type: application/octet-stream" -H "$DATE" \
    --data-binary @"文件路径" "$URL"

# 确认上传
mcporter call anyshare-asmcp.file_osendupload \
    access_token="$ACCESS_TOKEN" \
    docid="$DOCID" \
    rev="$REV"
```

---

### 5. file_sharedlink_realname_create (生成分享链接)

**注意**：item.id 需要使用完整的 GNS 路径，不能只使用短 ID

```bash
mcporter call anyshare-asmcp.file_sharedlink_realname_create \
    access_token="$ACCESS_TOKEN" \
    item="{\"id\":\"完整GNS路径\",\"type\":\"file\"}"
```

**返回**：
```json
{
  "code": 0,
  "link_url": "https://anyshare.aishu.cn/link/xxx",
  "id": "xxx"
}
```

---

## 完整执行示例

### Phase 0: 配置

```bash
ACCESS_TOKEN="$ACCESS_TOKEN"  # 从 mcporter 配置读取，禁止硬编码
# 使用指定的文档库
DOC_LIB_GNS="gns://743EFFF4E4B341E8A14DE5B375401365"
```

### Phase 1: 创建目录

```bash
# 检查并复用"写作成果"目录
echo "📁 检查写作成果目录..."
LIST=$(mcporter call anyshare-asmcp.folder_sub_objects \
    access_token="$ACCESS_TOKEN" \
    id="$DOC_LIB_GNS" limit:100)

# 检查是否存在
WRITING_DIR=$(echo "$LIST" | python3 -c "
import sys,json
data=json.load(sys.stdin)
for d in data.get('dirs',[]):
    if d.get('name')=='写作成果':
        print(d.get('id',''))
        break
")

if [ -z "$WRITING_DIR" ]; then
    echo "🆕 创建写作成果目录..."
    RESULT=$(mcporter call anyshare-asmcp.dir_create \
        access_token="$ACCESS_TOKEN" \
        docid="$DOC_LIB_GNS" name="写作成果")
    WRITING_DIR=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('docid',''))")
else
    echo "📁 复用已有目录: $WRITING_DIR"
fi

# 创建日期目录（复用已存在的）
TODAY=$(date +%Y-%m-%d)
DATE_LIST=$(mcporter call anyshare-asmcp.folder_sub_objects \
    access_token="$ACCESS_TOKEN" \
    id="$WRITING_DIR" limit:100)

DATE_DIR=$(echo "$DATE_LIST" | python3 -c "
import sys,json
data=json.load(sys.stdin)
for d in data.get('dirs',[]):
    if d.get('name')=='$TODAY':
        print(d.get('id',''))
        break
")

if [ -z "$DATE_DIR" ]; then
    echo "🆕 创建日期目录: $TODAY"
    DATE_RESULT=$(mcporter call anyshare-asmcp.dir_create \
        access_token="$ACCESS_TOKEN" docid="$WRITING_DIR" name="$TODAY")
    DATE_DIR=$(echo "$DATE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('docid',''))")
else
    echo "📁 复用已有日期目录: $TODAY"
fi

# 创建项目目录
PROJECT_NAME="技术总结"
PROJECT_RESULT=$(mcporter call anyshare-asmcp.dir_create \
    access_token="$ACCESS_TOKEN" docid="$DATE_DIR" name="$PROJECT_NAME")
PROJECT_DIR=$(echo "$PROJECT_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('docid',''))")

# 创建参考资料目录
REF_RESULT=$(mcporter call anyshare-asmcp.dir_create \
    access_token="$ACCESS_TOKEN" docid="$PROJECT_DIR" name="参考资料")
REF_DIR=$(echo "$REF_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('docid',''))")

echo "✅ 目录创建完成: $PROJECT_DIR"
```

### Phase 2: 上传文件

```bash
echo "📤 上传参考文件..."
for FILE in 技术方案.docx 会议纪要.pdf; do
    SIZE=$(stat -f%z "$FILE")

    # 获取上传凭证
    UPLOAD=$(mcporter call anyshare-asmcp.file_osbeginupload \
        access_token="$ACCESS_TOKEN" \
        docid="$REF_DIR" name="$FILE" length=$SIZE)

    URL=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][1])")
    AUTH=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][2])")
    DATE=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][4])")
    DOCID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['docid'])")
    REV=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['rev'])")

    # 上传
    curl -X PUT -H "$AUTH" -H "Content-Type: application/octet-stream" -H "$DATE" \
        --data-binary @"$FILE" "$URL"

    # 确认
    mcporter call anyshare-asmcp.file_osendupload \
        access_token="$ACCESS_TOKEN" docid="$DOCID" rev="$REV"

    # 收集短ID
    SHORT_ID=$(echo "$DOCID" | awk -F'/' '{print $NF}')
    echo "✅ 上传完成: $FILE -> $SHORT_ID"
done

# 构建 source_ranges
SOURCE_RANGES="[{\"id\":\"$SHORT_ID1\",\"type\":\"doc\"},{\"id\":\"$SHORT_ID2\",\"type\":\"doc\"}]"

# 等待索引（建议等待30秒以上）
echo "⏳ 等待文件索引..."
sleep 30
```

### Phase 3: 生成大纲

```bash
echo "📄 获取内置写作模板..."
curl -s -X GET \
  "https://anyshare.aishu.cn/api/intelli-search/v1/skills/templates/default?skill_name=__全文写作__3" \
  -H "authorization: $ACCESS_TOKEN" \
  -H "content-type: application/json" > /tmp/template_response.json

TEMPLATE_CONTENT=$(python3 -c "import json; print(json.load(open('/tmp/template_response.json')).get('template',''))")

if [ -z "$TEMPLATE_CONTENT" ]; then
    echo "⚠️ API获取模板失败，使用直接生成方式"
    TEMPLATE_CONTENT=""
fi

echo "🔍 生成大纲（基于内置模板）..."

# 使用 Python 构建 query（避免 shell 转义问题）
python3 << PYEOF
import json

template_content = """${TEMPLATE_CONTENT}"""

query = f"""基于以下内置模板的结构格式，为项目撰写一份可行性研究报告大纲。

模板结构参考：
{template_content}

要求：
1. 参考模板的层级结构格式（一级标题、二级标题、表格等）
2. 内容替换为项目的可行性研究报告章节
3. 章节要专业、完整，体现可行性研究报告的标准结构
4. 可以包含项目概述、市场分析、建设方案、技术方案、投资估算、效益分析、风险分析等核心章节"""

with open('/tmp/writing_query.txt', 'w', encoding='utf-8') as f:
    json.dump({"query": query}, f, ensure_ascii=False)
PYEOF

QUERY=$(python3 -c "import json; print(json.load(open('/tmp/writing_query.txt'))['query'])")

OUTLINE_RESULT=$(mcporter call anyshare-asmcp.smart_assistant \
    access_token="$ACCESS_TOKEN" \
    bot_id="smart_assistant" \
    query="$QUERY" \
    skill_name="__全文写作__3" \
    source_ranges="$SOURCE_RANGES" \
    times=0)

# 提取内容
OUTLINE_CONTENT=$(echo "$OUTLINE_RESULT" | python3 -c "
import sys,json
data=json.load(sys.stdin)
print(data.get('document_content',''))
")

if [ -z "$OUTLINE_CONTENT" ]; then
    echo "❌ 获取大纲失败"
    exit 1
fi

# 保存大纲
OUTLINE_MD="# 技术总结大纲

${OUTLINE_CONTENT}

---
*由 OpenClaw 写作助手生成*"

echo "$OUTLINE_MD" > /tmp/大纲.md
SIZE=$(stat -f%z /tmp/大纲.md)

# 上传大纲
UPLOAD=$(mcporter call anyshare-asmcp.file_osbeginupload \
    access_token="$ACCESS_TOKEN" docid="$PROJECT_DIR" name="大纲.md" length=$SIZE)

URL=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][1])")
AUTH=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][2])")
DATE=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][4])")

curl -X PUT -H "$AUTH" -H "Content-Type: application/octet-stream" -H "$DATE" \
    --data-binary @/tmp/大纲.md "$URL"

mcporter call anyshare-asmcp.file_osendupload \
    access_token="$ACCESS_TOKEN" \
    docid="$(echo "$UPLOAD" | python3 -c 'import sys,json; print(json.load(sys.stdin)["docid"])')" \
    rev="$(echo "$UPLOAD" | python3 -c 'import sys,json; print(json.load(sys.stdin)["rev"])')"

echo "✅ 大纲已保存"
```

### Phase 4: 展示大纲等待确认

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 大纲内容预览"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$OUTLINE_CONTENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "请确认大纲，如需修改请告诉我"
echo "确认后请说：确认，开始写正文"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

### Phase 5: 生成正文（用户确认后执行）

```bash
echo "✍️ 生成正文（使用 __大纲写作__1 + times:1，约2-4分钟）..."
SHORT_ID=$(cat /tmp/verify_short_id.txt)

# 大纲内容通过文件传递（避免shell转义问题）
python3 -c "import json; print(json.load(open('/tmp/template_outline.json')).get('document_content',''))" > /tmp/selection.txt

# 后台执行，避免60秒超时
nohup mcporter call anyshare-asmcp.smart_assistant \
    access_token="$ACCESS_TOKEN" \
    bot_id:smart_assistant \
    query:"基于以下大纲，撰写完整的可行性研究报告正文内容" \
    selection:"$(cat /tmp/selection.txt)" \
    skill_name:__大纲写作__1 \
    source_ranges:"[{\"id\":\"$SHORT_ID\",\"type\":\"doc\"}]" \
    times:1 \
    --timeout 180000 > /tmp/writing_result.json 2>&1 &

# 等待生成完成
echo "⏳ 等待正文生成（约2-4分钟）..."
sleep 150

# 提取内容
DOC_CONTENT=$(python3 -c "
import json
data=json.load(open('/tmp/writing_result.json'))
print(data.get('document_content',''))
")

if [ -z "$DOC_CONTENT" ]; then
    echo "❌ 正文生成失败，请检查 /tmp/writing_result.json"
    exit 1
fi

# 保存正文
DOC_MD="# 技术总结

\${DOC_CONTENT}

---
*由 OpenClaw 写作助手生成*"

echo "$DOC_MD" > /tmp/正文.md
SIZE=$(stat -f%z /tmp/正文.md)

# 上传正文
UPLOAD=$(mcporter call anyshare-asmcp.file_osbeginupload \
    access_token="$ACCESS_TOKEN" docid="$PROJECT_DIR" name="正文.md" length=$SIZE)

URL=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][1])")
AUTH=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][2])")
DATE=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['authrequest'][4])")
FULL_GNS=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['docid'])")

curl -X PUT -H "$AUTH" -H "Content-Type: application/octet-stream" -H "$DATE" \
    --data-binary @/tmp/正文.md "$URL"

mcporter call anyshare-asmcp.file_osendupload \
    access_token="$ACCESS_TOKEN" \
    docid="$FULL_GNS" \
    rev="$(echo "$UPLOAD" | python3 -c 'import sys,json; print(json.load(sys.stdin)["rev"])'")

echo "✅ 正文已保存"
```

### Phase 6: 生成分享链接

```bash
echo "🔗 生成分享链接..."
SHARE_RESULT=$(mcporter call anyshare-asmcp.file_sharedlink_realname_create \
    access_token="$ACCESS_TOKEN" \
    item="{\"id\":\"$FULL_GNS\",\"type\":\"file\"}")

SHARE_URL=$(echo "$SHARE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('link_url',''))")
echo "分享链接: $SHARE_URL"
```

---

## 输出结果

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 写作完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 位置：写作成果/2025-04-22/技术总结/
📄 大纲：大纲.md
📄 正文：正文.md
📁 原文：参考资料/
🔗 分享：https://anyshare.aishu.cn/link/xxx
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 依赖

- **MCP**: `anyshare-asmcp`
- **Tools**:
  - `doc_lib_owned` - 获取文档库
  - `folder_sub_objects` - 检查目录复用
  - `dir_create` - 创建目录
  - `file_osbeginupload/endupload` - 文件上传
  - `smart_assistant` - 大纲/正文生成
  - `file_sharedlink_realname_create` - 分享链接

---

*版本：2.0.0*
