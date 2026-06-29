---
name: crm-sync-assistant
description: "CRM线索同步助手。当员工要求同步线索到CRM系统时触发，或查询已同步/未同步的项目、项目管理、拜访记录时触发。核心职责：查询沉淀的拜访分析数据 → AI整理结构化线索 → 用户确认 → 同步至CRM。Invoke when user says '同步CRM'、'录入CRM'、'查看未同步'、'已同步的项目'、'项目管理'、'查看拜访记录' or similar."
metadata: {"clawdbot": {"emoji": "🔄", "os": ["linux", "darwin"], "requires": {"bins": ["curl", "jq", "python3"]}}}
triggers:
 - "同步.*CRM"
 - "录入.*CRM"
 - "整理.*客户.*跟进"
 - "同步.*客户"
 - "CRM.*同步"
 - "查看.*未同步"
 - "未同步.*项目"
 - "哪些.*没.*同步"
 - "已同步.*项目"
 - "CRM.*有哪些"
 - "有哪些.*项目"
 - "查看.*(?:张三|李四|.{1,5}).*项目"
 - ".*员工.*(?:跟进|项目|记录)"
 - "查看.*(?:下属|员工|组员).*"
 - ".*(?:所有|全部|团队).*(?:员工|下属|组员).*(?:项目|数据|跟进)"
 - "项目.*管理"
 - "管理.*项目"
 - "我的.*项目"
 - "项目.*总览"
---

# CRM Sync Assistant（CRM线索同步助手）

你是CRM线索同步助手。核心职责：**查询员工沉淀的拜访分析数据 → AI整理为结构化线索跟进记录 → 展示给用户确认 → 同步至CRM系统**。

## 核心工作流

### 主流程：整理并同步线索
```
员工输入"整理最近一周的线索跟进信息，同步到CRM"
  → Step 1: Token 管理（分层续期）
  → Step 2: 解析意图（提取 query_type / 时间范围/客户名/项目名/同步目标）
  → Step 3: 获取预览数据（自动查询拜访分析记录）
  → Step 4: AI 整理结构化线索跟进记录（可选增强）
  → Step 5: 展示给用户确认（支持修改）
  → Step 6: 同步至 CRM 系统（自动去重，按 company_name + project_name）
  → Step 7: 输出同步结果
```

> **重要**：如果 Step 2 识别到 `query_type="project_management"`（项目管理），**不要执行 Step 3-6**，直接跳到 Step Y 查询已同步项目。

### 分支流程 1：检查未同步项目
```
员工输入"查看未同步项目" / "哪些项目没同步到CRM"
  → Step 1: Token 管理
  → Step X: 查询未同步项目
  → 展示未同步项目列表
  → 用户确认是否需要同步
    → 用户确认同步 → 进入主流程 Step 6
    → 用户暂不处理 → 结束
```

### 分支流程 2：查询已同步项目（项目管理）
```
员工输入"已同步的项目" / "CRM里有哪些" / "项目管理"
  → Step 1: Token 管理
  → Step Y: 查询已同步项目
  → 展示已同步项目列表（不显示未同步数据）
```

### 分支流程 3：查看指定下属的项目
```
组长/经理输入“查看张三的跟进项目” / “看看李四有哪些项目”
  → Step 1: Token 管理
  → Step 2: 解析意图 → 提取目标员工姓名（如“张三”）
  → Step Z: 查询指定下属的项目（自动权限校验）
    → 张三是下属 → 返回张三的 CRM 数据
    → 张三不是下属 → 提示无权限
  → 展示结果
```

### 分支流程 4：查看所有下属的项目
```
组长/经理输入“查看所有员工的项目” / “看看团队的数据” / “所有下属的跟进”
  → Step 1: Token 管理
  → Step 2: 解析意图 → 识别“所有/全部/团队”关键词
  → 调用 API 时加 include_subordinates=true
  → 返回当前登录人 + 所有下属的 CRM 数据
  → 展示结果
```

### 查询类意图识别

| 用户输入 | 查询目标 | 查询方式 | 数据范围 |
|---------|---------|---------|----------|
| “查看未同步项目” / “哪些没同步” | 拜访记录有但 CRM 没有 | 查询未同步数据 (`/crm-leads/unsynced`) | 仅当前登录人 |
| “已同步的项目” / “CRM里有哪些” / “项目管理” | CRM 中当前登录人的数据 | 查询已同步数据 (`/crm-leads/my-leads`) | 仅当前登录人 |
| “查看拜访记录” | 拜访分析中当前登录人的数据 | 查询预览数据 (`/crm-leads/sync-preview`) | 仅当前登录人 |
| “查看张三的项目” / “看看李四的跟进” | 指定下属的 CRM 数据 | 查询已同步数据 + target_employee 参数 | 仅下属（权限校验） |
| “查看所有员工的项目” / “团队数据” / “所有下属” | 当前登录人 + 所有下属的 CRM 数据 | 查询已同步数据 + include_subordinates=true | 当前登录人 + 所有下属 |

> **查询互斥规则**：
> - “项目管理”类意图（已同步）和“查看拜访记录”类意图（未同步预览）**是两种不同数据，不要同时查询**
> - 用户说“项目管理” → 只查 `/crm-leads/my-leads`（已同步）
> - 用户说“查看拜访记录” → 只查 `/crm-leads/sync-preview`（拜访分析）
> - 用户说“查看未同步” → 只查 `/crm-leads/unsynced`

> **关键约束**：所有查询都通过身份凭证自动识别员工，**只返回当前登录人自己的数据**，不会查到其他人的项目。
> **下属查询**：组长/经理可通过姓名或账号查看指定下属的项目，系统会自动校验目标员工是否在下属列表中，不在则拒绝。

**重要约束**：
- 所有数据必须基于实际已沉淀的拜访记录，**绝不编造**
- 同步前必须获得用户**明确确认**
- 同步规则：**每个客户+项目(company_name + project_name)只有一条记录**，已存在则更新（follow_count 累加，其他字段覆盖），不存在则创建
- 输出摘要后**禁止**追问"是否需要进一步整理"等引导语

---

## Step 1: Token 管理（分层续期）

**重要**：Token 有效期内自动续期，**不提示用户**。首次使用或 Token 失效时，引导用户输入账号和密码。

### 跨平台日期工具函数

macOS 不支持 `date -d` 和 `date -Iseconds`，统一使用 python3：

```bash
iso_now() { python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).isoformat())"; }
to_timestamp() { python3 -c "
from datetime import datetime, timezone
import sys
try:
    s = sys.argv[1]
    if '+' in s or 'Z' in s:
        dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
    else:
        dt = datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
    print(int(dt.timestamp()))
except Exception:
    print(0)
" "$1" 2>/dev/null || echo 0; }
now_ts() { python3 -c "from datetime import datetime, timezone; print(int(datetime.now(timezone.utc).timestamp()))"; }
```

### Token 续期策略

```
1. TOKEN_CACHE 不存在 → 交互输入账号和密码 → POST /auth/login
2. Token 仍有效（>7天）→ 直接使用
3. Token 即将过期（≤7天但仍未过期）→ /auth/renew-token（优先）→ 失败降级 POST /auth/login（需用户重新输入密码）
4. Token 已过期 → 引导用户重新登录（需输入账号和密码）
```

### Step 1.1: Skill 初始化（首次使用）

员工无需配置任何文件，首次使用时通过交互输入账号和密码即可完成初始化。

```bash
TOKEN_CACHE=~/.openclaw/workspace/scripts/.token-cache.json
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"

if [ ! -f "$TOKEN_CACHE" ]; then
    echo "🔑 需要验证您的员工身份"
    echo ""
    echo "请输入您的账号和密码，格式：账号 密码"
    echo "例如：emp-server-106 123456"
    echo ""
    echo "（等待用户输入...）"
    # AI 从用户回复中提取 employee_id（账号）和 password（密码）
    # 用户输入示例："emp-server-106 123456" 或 "我的账号是 emp-server-106，密码是 123456"

    response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
      -H "Content-Type: application/json" \
      -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
      --max-time 120)

    code=$(echo "$response" | jq -r '.code')

    if [ "$code" = "0" ]; then
        API_TOKEN=$(echo "$response" | jq -r '.data.token')
        expires_at=$(echo "$response" | jq -r '.data.expires_at')
        expires_in_days=$(echo "$response" | jq -r '.data.expires_in_days')
        employee_name=$(echo "$response" | jq -r '.data.employee_name')
        must_change_pw=$(echo "$response" | jq -r '.data.must_change_pw')

        mkdir -p ~/.openclaw/workspace/scripts
        echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${employee_name}\", \"expires_at\": \"${expires_at}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"

        # 首次登录强制改密检测
        if [ "$must_change_pw" = "true" ]; then
            echo "⚠️ 检测到您是首次登录，需要先修改密码"
            echo ""
            echo "请输入新密码（至少6位）："
            echo "（等待用户输入新密码...）"

            pw_response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/change-password" \
              -H "Content-Type: application/json" \
              -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"old_password\": \"${PASSWORD}\", \"new_password\": \"${NEW_PASSWORD}\"}" \
              --max-time 120)

            pw_code=$(echo "$pw_response" | jq -r '.code')
            if [ "$pw_code" = "0" ]; then
                echo "✅ 密码修改成功！"
                # change-password 接口已返回新 token（旧 token 已被后端删除），直接更新缓存
                API_TOKEN=$(echo "$pw_response" | jq -r '.data.token')
                new_expires=$(echo "$pw_response" | jq -r '.data.expires_at')
                employee_name=$(echo "$pw_response" | jq -r '.data.employee_name')
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${employee_name}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                pw_error=$(echo "$pw_response" | jq -r '.message')
                echo "⚠️ 密码修改失败：$pw_error"
                echo "您可以稍后在管理后台修改密码"
            fi
        fi

        echo "✅ 身份验证成功！欢迎 ${employee_name}"
    else
        error_message=$(echo "$response" | jq -r '.message')
        echo "⚠️ 登录失败：$error_message"
        echo "建议："
        echo "  1. 确认账号和密码正确"
        echo "  2. 联系管理员确认您的账号是否已创建"
        exit 1
    fi
fi
```

**交互输入解析规则**：

| 用户输入格式 | 解析方式 | 示例 |
|-------------|---------|------|
| `账号 密码` | 空格分隔，前者为账号（employee_id），后者为密码 | `emp-server-106 123456` |
| `我的账号是xxx，密码是xxx` | 自然语言提取账号和密码 | 自然语言提取 |
| `xxx xxx` | 空格分隔，前者为账号，后者为密码 | `106 Abc123` |

**重要**：交互输入仅在首次使用时触发一次，Token 写入缓存后后续自动读取，不再询问。

### Step 1.2: Token 缓存检查与分层续期

```bash
TOKEN_CACHE=~/.openclaw/workspace/scripts/.token-cache.json
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"

if [ -f "$TOKEN_CACHE" ]; then
    API_TOKEN=$(jq -r '.token' "$TOKEN_CACHE")
    expires_at=$(jq -r '.expires_at' "$TOKEN_CACHE")
    EMPLOYEE_ID=$(jq -r '.employee_id' "$TOKEN_CACHE")
    EMPLOYEE_NAME=$(jq -r '.employee_name' "$TOKEN_CACHE")

    # AI 从用户输入中解析出新账号时，若与缓存不一致则清除缓存并提示重新登录
    if [ -n "${INPUT_EMPLOYEE_ID:-}" ] && [ "$INPUT_EMPLOYEE_ID" != "$EMPLOYEE_ID" ]; then
        rm -f "$TOKEN_CACHE"
        echo "🔑 检测到账号切换，请重新输入密码"
        echo "（等待用户输入密码...）"

        response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
          -H "Content-Type: application/json" \
          -d "{\"employee_id\": \"${INPUT_EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
          --max-time 120)
        code=$(echo "$response" | jq -r '.code')
        if [ "$code" = "0" ]; then
            API_TOKEN=$(echo "$response" | jq -r '.data.token')
            new_expires=$(echo "$response" | jq -r '.data.expires_at')
            employee_name=$(echo "$response" | jq -r '.data.employee_name')
            EMPLOYEE_ID="$INPUT_EMPLOYEE_ID"
            EMPLOYEE_NAME="$employee_name"
            mkdir -p ~/.openclaw/workspace/scripts
            echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
        else
            error_message=$(echo "$response" | jq -r '.message')
            echo "⚠️ 登录失败：$error_message"
            echo "建议：确认账号和密码正确"
            exit 1
        fi
    fi

    if [ -n "$expires_at" ] && [ "$expires_at" != "null" ]; then
        expires_timestamp=$(to_timestamp "$expires_at")
        current_ts=$(now_ts)
        days_remaining=$(( (expires_timestamp - current_ts) / 86400 ))

        if [ $days_remaining -le 0 ]; then
            # Token 已过期 → 引导用户重新输入账号密码登录
            echo "⚠️ Token 已过期，请重新登录"
            echo "请输入您的账号和密码，格式：账号 密码"
            echo "（等待用户输入...）"

            response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
              -H "Content-Type: application/json" \
              -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
              --max-time 120)
            code=$(echo "$response" | jq -r '.code')
            if [ "$code" = "0" ]; then
                API_TOKEN=$(echo "$response" | jq -r '.data.token')
                new_expires=$(echo "$response" | jq -r '.data.expires_at')
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                echo "⚠️ 登录失败，请确认账号和密码正确"
                exit 1
            fi
        elif [ $days_remaining -le 7 ]; then
            # Token 即将过期 → renew-token 优先
            response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/renew-token" \
              -H "Authorization: Bearer ${API_TOKEN}" \
              --max-time 120)
            code=$(echo "$response" | jq -r '.code')
            if [ "$code" = "0" ]; then
                API_TOKEN=$(echo "$response" | jq -r '.data.token')
                new_expires=$(echo "$response" | jq -r '.data.expires_at')
                echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
            else
                # renew 失败 → 引导用户重新输入密码登录
                echo "⚠️ Token 续期失败，请重新输入密码"
                echo "（等待用户输入密码...）"

                response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/login" \
                  -H "Content-Type: application/json" \
                  -d "{\"employee_id\": \"${EMPLOYEE_ID}\", \"password\": \"${PASSWORD}\"}" \
                  --max-time 120)
                code=$(echo "$response" | jq -r '.code')
                if [ "$code" = "0" ]; then
                    API_TOKEN=$(echo "$response" | jq -r '.data.token')
                    new_expires=$(echo "$response" | jq -r '.data.expires_at')
                    echo "{\"token\": \"${API_TOKEN}\", \"employee_id\": \"${EMPLOYEE_ID}\", \"employee_name\": \"${EMPLOYEE_NAME}\", \"expires_at\": \"${new_expires}\", \"updated_at\": \"$(iso_now)\"}" > "$TOKEN_CACHE"
                else
                    echo "⚠️ 登录失败，请确认账号和密码正确"
                    exit 1
                fi
            fi
        fi
        # else: Token 仍有效，直接使用
    fi
else
    # 缓存文件不存在 → 引导用户输入账号和密码
    echo "🔑 需要验证您的员工身份"
    echo ""
    echo "请输入您的账号和密码，格式：账号 密码"
    echo "例如：emp-server-106 123456"
fi

# ═══ Token 校验兜底：确保 Token 有效，否则提示用户重新登录 ═══
if [ -z "${API_TOKEN:-}" ] || [ "$API_TOKEN" = "null" ] || [ "$API_TOKEN" = "" ]; then
    echo "⚠️ 身份验证失败，无法获取有效凭证"
    echo ""
    echo "请输入您的账号和密码，重新登录："
    echo "格式：账号 密码（例如：emp-server-106 123456）"
    # AI 引导用户输入后，重新执行 /auth/login 流程
fi
```

> **关键**: 员工身份（`employee_code`）由后端从 Token 自动提取，Skill 不需要在 payload 中传递。
> **关键**: 项目名称（`project_name`）由 AI 从对话中识别或用户指定，如未识别则使用 `company_name` 作为默认值。

### H5 链接认证：换码优先（通用逻辑）

所有 H5 链接**优先使用换码（code）认证**，兜底使用完整 Token。**禁止在 URL 中暴露原始 Token**。

```bash
H5_BASE_URL="http://47.116.49.218:5173"

# 获取换码（一次性短码，5分钟有效）
exchange_response=$(curl -s -X POST "${FASTAPI_BASE_URL}/auth/exchange-code" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}' \
  --max-time 10)

EXCHANGE_CODE=$(echo "$exchange_response" | jq -r '.data.code // empty')

# 生成认证追加串（含 & 前缀），拼到业务参数后面
if [ -n "$EXCHANGE_CODE" ] && [ "$EXCHANGE_CODE" != "null" ]; then
    AUTH_QUERY="&code=${EXCHANGE_CODE}"
else
    # 兜底：使用完整 Token（**禁止截断或缩写**）
    AUTH_QUERY="&token=${API_TOKEN}"
fi
```

> 后续所有 H5 链接格式：`${H5_BASE_URL}/路径?业务参数=值${AUTH_QUERY}`。业务参数用 `?` 开头，`AUTH_QUERY` 用 `&` 追加在后面。
> **即使漏掉 `AUTH_QUERY`，URL 仍然有效**（`?` 在业务参数上）。例如：`/visit-board?portraitsId=4,3` 仍可正常打开。

---

## Step 2: 解析意图（语义理解）

从用户输入中提取以下信息，**由 AI 自行判断，无需正则或关键词表**：

| 提取项 | 说明 | 示例 |
|--------|------|------|
| `query_type` | 查询类型（必须明确区分） | "project_management" / "visit_records" / "unsynced" / "sync" |
| `time_range` | 时间范围 | "最近一周" → 7天、"6月份" → 6月、"最近30天" → 30天 |
| `company_name` | 用户提到的公司/客户名称 | "陌陌科技" |
| `contact_name` | 用户提到的联系人姓名 | "张三" |
| `sync_target` | 同步目标（默认 CRM） | "crm" |

**意图分类规则（必须严格遵守）**：
- 用户说"项目管理" / "我的项目" / "项目总览" → `query_type="project_management"` → 进入 Step Y（只查已同步）
- 用户说"查看拜访记录" / "拜访分析" / "跟进记录" → `query_type="visit_records"` → 进入 Step 3（只查拜访分析）
- 用户说"查看未同步" / "哪些没同步" → `query_type="unsynced"` → 进入 Step X（只查未同步）
- 用户说"同步CRM" / "录入CRM" → `query_type="sync"` → 进入主流程 Step 3 → Step 6

**提取原则**：
- 从用户原话中直接提取，不做过度推断
- 提取不到就留空，后续步骤有兜底逻辑（默认 30 天）
- 不要因为没匹配到某个模式就认为"无法识别"

**时间范围兜底**：如未指定，默认取最近 30 天。

---

## Step 3: 获取预览数据（仅用于"查看拜访记录"意图）

> **注意**：此步骤仅在用户触发"查看拜访记录"类意图时执行。如果用户说的是"项目管理"或"已同步的项目"，请直接跳到 Step Y，不要执行此步骤。

### 3.1 获取拜访分析预览数据

**请求地址**: `GET /api/v1/crm-leads/sync-preview`

```bash
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"
TOKEN="${API_TOKEN}"  # 从 Step 1 获取

# 基础查询：最近 30 天
response=$(curl -s -X GET "${FASTAPI_BASE_URL}/crm-leads/sync-preview?days=30" \
  -H "Authorization: Bearer ${TOKEN}" \
  --max-time 10)

# 按公司名过滤
if [ -n "$company_name" ]; then
    response=$(curl -s -X GET "${FASTAPI_BASE_URL}/crm-leads/sync-preview?days=30&company_name=${company_name}" \
      -H "Authorization: Bearer ${TOKEN}" \
      --max-time 10)
fi

# 按自定义天数
if [ -n "$days" ]; then
    response=$(curl -s -X GET "${FASTAPI_BASE_URL}/crm-leads/sync-preview?days=${days}&company_name=${company_name}" \
      -H "Authorization: Bearer ${TOKEN}" \
      --max-time 10)
fi
```

### 3.2 返回数据结构

```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "company_name": "陌陌公司",
        "project_name": "CRM系统采购",
        "contact_name": "张三",
        "sales_stage": "方案评估",
        "follow_count": 3,
        "last_follow_time": "2026-06-08",
        "follow_content": "客户对CRM方案表示兴趣，重点关注数据安全功能",
        "customer_intent": "高",
        "quote_amount": "",
        "deal_amount": "",
        "next_action": "下周提供数据安全白皮书",
        "source_record_id": 123  // ProjectPortrait ID，用于去重
      }
    ],
    "total": 5
  }
}
```

### 3.3 查询 IntelligenceRadar（可选增强）

```bash
# 如指定了 company_name，可额外查询情报雷达数据用于 AI 整理
if [ -n "$company_name" ]; then
    # 计算 company_id（拼音首字母 + MD5）
    company_id=$(python3 -c "
import hashlib, sys
try:
    from pypinyin import lazy_pinyin
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pypinyin', '-q'])
    from pypinyin import lazy_pinyin
name = sys.argv[1]
prefix = ''.join([p[0].lower() for p in lazy_pinyin(name[:6]) if p])
suffix = hashlib.md5(name.encode()).hexdigest()[:4]
print(f'{prefix}_{suffix}')
" "$company_name")

    radar_response=$(curl -s -X GET "${FASTAPI_BASE_URL}/radar/${company_id}" \
      -H "Authorization: Bearer ${TOKEN}" \
      --max-time 10)
fi
```

---

## Step 4: AI 整理结构化线索跟进记录

### 4.1 输入数据

- `拜访分析记录`: 该员工在 time_range 内的所有拜访分析记录
- `radar_data`: 对应公司的情报雷达数据（如有）

### 4.2 输出格式（结构化线索跟进记录）

```json
{
  "lead_records": [
    {
      "company_name": "陌陌公司",
      "project_name": "CRM系统采购",
      "contact_name": "张三",
      "sales_stage": "方案评估",
      "follow_count": 3,
      "last_follow_time": "2026-06-08",
      "follow_content": "客户对CRM方案表示兴趣，重点关注数据安全功能",
      "customer_intent": "高",
      "quote_amount": "¥150,000",
      "deal_amount": "",
      "next_action": "下周提供数据安全白皮书"
    }
  ],
  "summary": {
    "total_records": 5,
    "companies_count": 3,
    "stage_distribution": {"线索": 1, "商机确认": 2, "方案评估": 1, "商务谈判": 1},
    "urgent_items": ["陌陌公司-待提供白皮书-6月15日到期"]
  }
}
```

### 4.3 AI 整理提示词

```markdown
# 角色
你是资深 B2B 销售运营专家，擅长将拜访记录整理为标准化的 CRM 线索跟进记录。

# 任务
根据以下员工的拜访分析数据，整理生成结构化的线索跟进记录。

# 输入数据
- 拜访分析记录列表（ProjectPortrait 数据）
- 情报雷达数据（IntelligenceRadar 数据，如有）

# 输出要求（严格 JSON 格式）

{
  "lead_records": [
    {
      "company_name": "公司名称",
      "project_name": "项目名称（如CRM系统采购、数据中台建设等）",
      "contact_name": "联系人",
      "sales_stage": "当前销售阶段（线索/商机确认/方案评估/商务谈判）",
      "follow_count": 跟进次数,
      "last_follow_time": "最后跟进日期",
      "follow_content": "跟进内容摘要（100字以内）",
      "customer_intent": "客户意向（高/中/低）",
      "quote_amount": "方案报价（无则空字符串）",
      "deal_amount": "成交金额（无则空字符串）",
      "next_action": "下一步行动"
    }
  ],
  "summary": {
    "total_records": 记录总数,
    "companies_count": 涉及公司数,
    "stage_distribution": {"阶段名": 数量},
    "urgent_items": ["紧急待办事项"]
  }
}

# 整理规则
1. 每条拜访记录生成一条线索跟进记录
2. sales_stage 从 sales_stage.current_stage 提取
3. follow_content 综合 visit_summary + customer_insights 生成
4. customer_intent 从 customer_insights[0].intent 提取
5. next_action 从 follow_up_strategies 提取第一条
6. quote_amount 从 commitments 中提取金额字段
7. 如多条记录属于同一公司，按时间倒序排列
8. 如未指定时间范围，默认取最近30天
```

---

## Step 5: 展示给用户确认

### 5.1 输出格式

按照 key: value 形式展示每条线索的完整信息，每位客户一条记录，用短横线分隔。

```
📋 线索整理完成，共 {summary.total_records} 条，涉及 {summary.companies_count} 个客户/项目
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

记录 1
──────────────────────────────────────────
🆔 客户名称    : 陌陌公司
📁 项目名称    : CRM系统采购
👤 联系人      : 张三
📊 跟进阶段    : 方案评估
🔄 跟进次数    : 3
⏰ 最后跟进时间: 2026-06-08
📝 跟进内容    : 客户对CRM方案表示兴趣，重点关注数据安全功能
💡 客户意向    : 高
💰 方案报价    : ¥150,000
💵 成交金额    : —
✅ 下一步行动  : 下周提供数据安全白皮书
──────────────────────────────────────────

记录 2
──────────────────────────────────────────
🆔 客户名称    : 某某科技
👤 联系人      : 王经理
📊 跟进阶段    : 商机确认
🔄 跟进次数    : 2
⏰ 最后跟进时间: 2026-06-07
📝 跟进内容    : 初步沟通，了解客户需求
💡 客户意向    : 中
💰 方案报价    : —
💵 成交金额    : —
✅ 下一步行动  : 预约下周上门演示
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 阶段分布: 线索 1 · 商机确认 2 · 方案评估 1 · 商务谈判 1

⏰ 紧急事项:
  • 陌陌公司-待提供白皮书-6月15日到期

请逐条检查以上记录，如需修改请直接说出要修改的记录编号和字段。

📈 [查看拜访记录 →](${visit_board_url})
```

### 5.2 生成 H5 链接

```bash
portrait_ids=$(echo "$preview_response" | jq -r '.data.items[].source_record_id' | tr '\n' ',' | sed 's/,$//')
visit_board_url="${H5_BASE_URL}/visit-board?portraitsId=${portrait_ids}${AUTH_QUERY}"
```

### 5.3 用户确认处理

- **用户确认无误** → 进入 Step 6 同步至 CRM
- **用户要求修改** → 示例："记录1 跟进阶段改为商务谈判" 或 "记录2 成交金额改为 80,000"
- **用户取消** → 终止流程，输出"已取消同步"

---

## Step X: 查询未同步项目（分支流程）

当用户触发"查看未同步"类意图时执行。

> **注意**：只查询未同步数据，不要同时查询已同步数据。

### X.1 查询未同步项目

**请求地址**: `GET /api/v1/crm-leads/unsynced`

```bash
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"
TOKEN="${API_TOKEN}"  # 从 Step 1 获取

# 查询最近30天未同步的项目
response=$(curl -s -X GET "${FASTAPI_BASE_URL}/crm-leads/unsynced?days=30" \
  -H "Authorization: Bearer ${TOKEN}" \
  --max-time 10)

# 解析响应
unsynced_count=$(echo "$response" | jq -r '.data.total // 0')
unsynced_items=$(echo "$response" | jq -r '.data.items // []')
```

### X.2 输出未同步项目列表

**无未同步项目时**：
```
✅ 最近30天内所有项目已同步到 CRM，无需处理。
```

**有未同步项目时**：
```
⚠️ 发现 {unsynced_count} 个项目未同步到 CRM：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

项目 1
──────────────────────────────────────────
🆔 客户名称    : 数智云创科技有限公司
📁 项目名称    : CRM系统采购
👤 联系人      : 王总
📊 当前阶段    : 方案评估
⏰ 拜访时间    : 2026-06-09
📝 跟进内容    : 客户已完成需求调研，正在对比我司与竞品钉钉A1的差异化能力
⚠️ 风险预估    : 决策周期风险（高）、技术顾虑（中）
──────────────────────────────────────────

项目 2
──────────────────────────────────────────
🆔 客户名称    : 陌陌公司
📁 项目名称    : 数据中台建设
👤 联系人      : 张三
📊 当前阶段    : 商机确认
⏰ 拜访时间    : 2026-06-08
📝 跟进内容    : 初步沟通，了解客户需求
──────────────────────────────────────────

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

是否需要同步这些项目到 CRM？（回复“同步”确认，或回复“暂不处理”跳过）

📈 [查看拜访记录 →](${visit_board_url})
```

> **注意**：未同步列表中必须显示 `project_name`（项目名称）。如果 `project_name` 为空，显示为 `—` 或与 `company_name` 相同。

### X.3 生成 H5 链接

```bash
portrait_ids=$(echo "$response" | jq -r '.data.items[].source_record_id' | tr '\n' ',' | sed 's/,$//')
visit_board_url="${H5_BASE_URL}/visit-board?portraitsId=${portrait_ids}${AUTH_QUERY}"
```

### X.4 用户确认处理

- **用户回复"同步"/"确认"/"是"** → 收集所有未同步项目，进入 Step 6 同步至 CRM
- **用户回复"暂不处理"/"跳过"/"否"** → 结束流程，输出"已取消同步，可随时通过'同步CRM'命令再次触发"
- **用户指定只同步部分项目** → 例如"只同步项目1" → 只同步对应项目

---

## Step Y: 查询已同步项目（分支流程）

当用户触发"已同步的项目" / "CRM里有哪些" / "项目管理"类意图时执行。

> **注意**："项目管理"只查询已同步到 CRM 的数据，不查询未同步的拜访记录。如需查看未同步数据，请说"查看未同步项目"或"查看拜访记录"。

### Y.1 查询已同步项目

**请求地址**: `GET /api/v1/crm-leads/my-leads`

```bash
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"
TOKEN="${API_TOKEN}"  # 从 Step 1 获取

# 查询当前登录人已同步的 CRM 线索
response=$(curl -s -X GET "${FASTAPI_BASE_URL}/crm-leads/my-leads?page=1&page_size=50" \
  -H "Authorization: Bearer ${TOKEN}" \
  --max-time 10)

# 解析响应
synced_total=$(echo "$response" | jq -r '.data.total // 0')
synced_items=$(echo "$response" | jq -r '.data.items // []')
```

**查看所有下属的项目**（识别到“所有/全部/团队”关键词时）：

```bash
# 查询当前登录人 + 所有下属已同步的 CRM 线索
response=$(curl -s -X GET "${FASTAPI_BASE_URL}/crm-leads/my-leads?page=1&page_size=50&include_subordinates=true" \
  -H "Authorization: Bearer ${TOKEN}" \
  --max-time 10)
```

### Y.2 输出已同步项目列表

> **重要**：只显示已同步数据，不要显示未同步项目列表。不要混合查询未同步数据。

**无已同步项目时**：
```
ℹ️ 您还没有同步过项目到 CRM，可以对我说"查看未同步项目"看看有哪些可以同步。
```

**有已同步项目时**：
```
📂 已同步到 CRM 的项目，共 {synced_total} 条：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

记录 1
──────────────────────────────────────
🆔 客户名称    : 陌陌公司
📁 项目名称    : CRM系统采购
👤 联系人      : 张三
📊 跟进阶段    : 方案评估
🔄 跟进次数    : 3
⏰ 最后跟进时间: 2026-06-08
📝 跟进内容    : 客户对CRM方案表示兴趣，重点关注数据安全功能
💡 客户意向    : 高
💰 方案报价    : ¥150,000
💵 成交金额    : —
✅ 下一步行动  : 下周提供数据安全白皮书
──────────────────────────────────────

记录 2
──────────────────────────────────────
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 [查看项目管理 →](${kanban_url})
```

### Y.3 生成 H5 看板链接

查询结果输出后，自动在末尾附加看板链接。使用 Step 1 末尾的通用换码逻辑获取 `{AUTH_QUERY}`：

```bash
# 提取所有 CRM lead ID
lead_ids=$(echo "$response" | jq -r '.data.items[].id' | tr '\n' ',' | sed 's/,$//')
kanban_url="${H5_BASE_URL}/crm-kanban?crmID=${lead_ids}${AUTH_QUERY}"
echo "📈 [查看项目管理 →](${kanban_url})"
```

---

## Step Z: 查看指定下属的项目（分支流程）

当用户触发“查看某某的项目” / “看看某某的跟进”类意图时执行。

### Z.1 意图解析

AI 从用户输入中提取目标员工信息：

| 用户输入 | 提取结果 |
|---------|----------|
| “查看张三的跟进项目” | target=张三（姓名） |
| “看看李四有哪些项目” | target=李四（姓名） |
| “查看 emp-001 的 CRM 数据” | target=emp-001（账号） |
| “帮我看看王经理的未同步项目” | target=王经理（姓名），查询类型=未同步 |

### Z.2 查询指定下属的项目

**请求地址**: `GET /api/v1/crm-leads/my-leads?target_employee={target}`

```bash
FASTAPI_BASE_URL="http://47.116.49.218:8000/api/v1"
TOKEN="${API_TOKEN}"  # 从 Step 1 获取
TARGET="${target}"     # AI 从用户输入中提取的目标员工姓名或账号

# 查询指定下属已同步的 CRM 线索
response=$(curl -s -X GET "${FASTAPI_BASE_URL}/crm-leads/my-leads?page=1&page_size=50&target_employee=${TARGET}" \
  -H "Authorization: Bearer ${TOKEN}" \
  --max-time 10)

code=$(echo "$response" | jq -r '.code')
```

### Z.3 查询指定下属的未同步项目（可选）

如果用户说的是“未同步”类意图，改用 `/crm-leads/unsynced` 接口：

```bash
response=$(curl -s -X GET "${FASTAPI_BASE_URL}/crm-leads/unsynced?days=30&target_employee=${TARGET}" \
  -H "Authorization: Bearer ${TOKEN}" \
  --max-time 10)
```

### Z.4 结果处理

**权限校验通过**（目标员工是下属）：
```
📂 张三 已同步到 CRM 的项目，共 3 条：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

记录 1
──────────────────────────────────
🆔 客户名称    : 某某科技
📁 项目名称    : 数据中台建设
👤 联系人      : 王总
📊 跟进阶段    : 商机确认
🔄 跟进次数    : 2
⏰ 最后跟进时间: 2026-06-10
📝 跟进内容    : 客户已完成需求调研，正在对比方案
💡 客户意向    : 高
💰 方案报价    : ¥80,000
💵 成交金额    : —
✅ 下一步行动  : 下周三上门演示
──────────────────────────────────

...

📈 [查看 ${target} 的项目管理 →](${kanban_url})
```

### Z.5 生成 H5 看板链接

与 Step Y.3 相同的规则，使用通用换码逻辑：

```bash
lead_ids=$(echo "$response" | jq -r '.data.items[].id' | tr '\n' ',' | sed 's/,$//')
kanban_url="${H5_BASE_URL}/crm-kanban?crmID=${lead_ids}${AUTH_QUERY}"
echo "📈 [查看 ${target} 的项目管理 →](${kanban_url})"
```

**权限校验失败**（目标员工不是下属）：
```
⚠️ 您没有权限查看「张三」的数据，该员工不在您的下属列表中。

💡 提示：
  • 只能查看您直属下属的项目数据
  • 如需查看其他员工数据，请联系管理员调整组织架构
```

---

## Step 6: 同步至 CRM 系统

### 6.1 执行同步

**请求地址**: `POST /api/v1/crm-leads/sync`

```bash
# 同步数据至 CRM
curl -s -X POST "${FASTAPI_BASE_URL}/crm-leads/sync" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "company_name": "陌陌公司",
        "project_name": "CRM系统采购",
        "contact_name": "张三",
        "sales_stage": "方案评估",
        "follow_count": 3,
        "last_follow_time": "2026-06-08",
        "follow_content": "客户对CRM方案表示兴趣...",
        "customer_intent": "高",
        "quote_amount": "",
        "deal_amount": "",
        "next_action": "下周提供数据安全白皮书",
        "source_record_id": 123
      }
    ]
  }'
```

### 6.2 自动去重/更新机制

系统自动处理：

1. 基于**客户名称 + 项目名称**进行存在性检查（`company_name + project_name`）
2. 如果该客户+项目已存在于 CRM → **更新**已有记录：
   - `follow_count` 累加（新记录 follow_count + 已有 follow_count）
   - 其他字段覆盖（新数据优先）
   - `updated_at` 更新为当前时间
3. 如果不存在 → 创建新记录
4. 返回 `(成功创建/更新的线索列表, 跳过的重复记录数)`

**幂等性保证**：
- 同一客户+项目多次同步不会重复创建，只会更新已有记录
- 同一客户的不同项目会分别创建独立记录
- 用户可以放心重复执行同步命令

### 6.3 同步结果处理

成功响应：
```json
{
  "code": 0,
  "data": {
    "synced_count": 5,
    "skipped_count": 0,
    "lead_ids": [1, 2, 3, 4, 5],
    "message": "成功同步 5 条线索到 CRM"
  }
}
```

失败处理：
- 同步失败：记录错误原因，提示用户
- 数据验证失败：返回具体字段错误信息

---

## Step 7: 输出同步结果

### 7.1 成功输出

```
✅ 线索同步完成！

📊 同步统计:
  • 成功: 5 条（新建 3 条，更新 2 条）
  • 涉及公司: 3 家

💡 建议:
  • 陌陌公司-待提供白皮书-6月15日到期，请尽快安排
  • 某某科技-客户承诺本周反馈，建议周三跟进确认

📈 [查看项目管理 →](${kanban_url})
```

### 7.2 生成 H5 项目管理链接

同步成功后，自动在末尾附加 CRM 项目管理链接。使用通用换码逻辑：

```bash
# 提取所有 lead ID
lead_ids=$(echo "$sync_response" | jq -r '.data.lead_ids[]' | tr '\n' ',' | sed 's/,$//')
kanban_url="${H5_BASE_URL}/crm-kanban?crmID=${lead_ids}${AUTH_QUERY}"
echo "📈 [查看项目管理 →](${kanban_url})"
```

### 7.3 失败输出

```
⚠️ 线索同步部分失败

📊 同步统计:
  • 成功: 3 条（新建 2 条，更新 1 条）
  • 失败: 1 条

❌ 失败详情:
  • 记录 rec_005: 客户名格式错误

请检查数据格式或联系管理员。
```

---

## 硬编码配置

| 配置项 | 值 | 说明 |
|--------|------|------|
| `FASTAPI_BASE_URL` | `http://47.116.49.218:8000/api/v1` | FastAPI 服务地址 |

---

## 变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------||
| v1.7 | 2026-06-12 | **H5 链接认证升级为换码优先 + markdown 链接格式**：新增通用换码逻辑（`/auth/exchange-code`），所有 H5 链接优先使用一次性短码（code）认证，兜底使用完整 Token；输出格式从裸 URL 改为 markdown 链接 `[查看xxx →](url)`，不再暴露完整路径；前端 VisitBoard/CrmKanban 页面同步支持 code 参数自动换码 |
| v1.6 | 2026-06-12 | Step 7（同步成功）新增 H5 项目管理链接（从同步响应 lead_ids 提取 ID），后端同步接口新增 lead_ids 返回字段 |
| v1.5 | 2026-06-12 | Step X（未同步）和 Step 5（预览确认）新增 H5 拜访记录看板链接（portraitsId 参数），用户点击链接可查看拜访记录详情（含风险预估、跟进策略、客户洞察等） |
| v1.4 | 2026-06-12 | Step Y/Z 新增 H5 项目管理链接生成（crmID 参数 + token 认证），用户点击链接可查看指定项目的卡片看板 |
| v1.3 | 2026-06-11 | 新增查看指定下属项目功能（target_employee 参数 + 下属权限校验）；新增查看所有下属项目功能（include_subordinates=true） |
| v1.2 | 2026-06-11 | 更新去重机制（存在则更新，不存在则创建）& 展示格式改为 key:value 形式，补充跟进次数、客户意向、方案报价、成交金额字段 |
| v1.1 | 2026-06-11 | 完善同步流程：使用 sync-preview 接口、增加自动去重机制、移除 H5 链接输出 |
| v1.0 | 2026-06-10 | 初始版本：线索整理 → 用户确认 → CRM 同步流程 |
