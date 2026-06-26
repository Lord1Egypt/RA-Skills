# 架构说明

## 🏗️ 技能架构

```
┌─────────────────────────────────────────────────────────┐
│  dingtalk-ai-table-insights (分析技能)                   │
│  - 跨表格洞察分析                                        │
│  - 风险识别                                              │
│  - 报告生成                                              │
│                                                          │
│  依赖 ↓                                                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  dingtalk-ai-table (基础技能)                            │
│  - MCP 配置管理                                          │
│  - 表格数据读取                                          │
│  - API 封装                                              │
│                                                          │
│  依赖 ↓                                                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  钉钉 AI 表格 MCP 服务器                                   │
│  - 数据源                                                │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 职责划分

### dingtalk-ai-table (基础技能)

**职责：**
- ✅ **MCP 配置管理** - 维护 MCP 服务器配置
- ✅ **数据读取** - 直接调用 MCP API
- ✅ **API 封装** - 提供统一的接口
- ✅ **权限处理** - 处理认证和授权

**配置文件：**
```
<workspace>/config/mcporter.json
```

**用户需要：**
1. 安装 `dingtalk-ai-table` skill
2. 配置 MCP 服务器信息
3. 确保可以访问钉钉 AI 表格

---

### dingtalk-ai-table-insights (分析技能)

**职责：**
- ✅ **跨表格分析** - 同时分析多个表格
- ✅ **洞察生成** - 使用 LLM 生成业务洞察
- ✅ **风险识别** - 识别异常和风险点
- ✅ **报告输出** - 生成可读的分析报告

**依赖：**
- `dingtalk-ai-table` skill（必需）
- MCP 配置（由 dingtalk-ai-table 管理）

**用户需要：**
1. 安装 `dingtalk-ai-table-insights` skill
2. 确保 `dingtalk-ai-table` 已正确配置
3. 运行分析命令

---

## 🔧 配置流程

### 步骤 1: 安装基础技能

```bash
clawhub install dingtalk-ai-table
```

### 步骤 2: 配置 MCP（一次配置）

```bash
# 创建配置文件
mkdir -p <workspace>/config
vim <workspace>/config/mcporter.json

# 填入配置（从钉钉管理员获取）
{
  "mcpServers": {
    "dingtalk-ai-table": {
      "baseUrl": "https://mcp-gw.dingtalk.com/server/YOUR_ID?key=YOUR_KEY"
    }
  }
}
```

### 步骤 3: 验证基础技能

```bash
# 测试表格列表
mcporter --config <workspace>/config/mcporter.json \
  call dingtalk-ai-table.search_accessible_ai_tables

# 测试数据读取
python3 ~/.openclaw/skills/dingtalk-ai-table/scripts/read_table.py \
  --doc-id <你的表格 ID> \
  --sheet Sheet1
```

### 步骤 4: 安装分析技能

```bash
clawhub install dingtalk-ai-table-insights
```

### 步骤 5: 运行分析

```bash
cd <workspace>/skills/dingtalk-ai-table-insights
python3 scripts/analyze_tables.py --keyword "销售"
```

---

## 🔄 调用关系

### 直接调用（当前实现）

```
dingtalk-ai-table-insights
    ↓ (mcporter CLI)
dingtalk-ai-table MCP
    ↓ (HTTP)
钉钉 AI 表格服务器
```

**优点：**
- 简单直接
- 性能好

**缺点：**
- 需要共享 MCP 配置
- 配置责任不清晰

---

### 理想架构（未来）

```
dingtalk-ai-table-insights
    ↓ (技能间调用)
dingtalk-ai-table skill
    ↓ (mcporter CLI)
dingtalk-ai-table MCP
    ↓ (HTTP)
钉钉 AI 表格服务器
```

**优点：**
- 职责清晰
- 配置隔离
- 易于维护

**实现方式：**
- OpenClaw 技能间通信
- 或共享配置目录

---

## 📁 配置位置

### 推荐方案

```
<workspace>/
├── config/
│   └── mcporter.json          # MCP 配置（.gitignore）
├── skills/
│   ├── dingtalk-ai-table/     # 基础技能
│   └── dingtalk-ai-table-insights/  # 分析技能
```

### 配置共享

两个 skill 共享同一个 MCP 配置：
- `dingtalk-ai-table` 使用配置进行数据读取
- `dingtalk-ai-table-insights` 使用配置获取表格列表

**配置路径优先级：**
1. 环境变量 `DINGTALK_MCP_CONFIG`
2. 默认路径 `<workspace>/config/mcporter.json`

---

## 🛡️ 安全说明

### 配置保护

```bash
# .gitignore
config/mcporter.json          # 忽略用户配置
!config/mcporter.json.example  # 保留模板
```

### 权限最小化

- `dingtalk-ai-table` - 需要表格读取权限
- `dingtalk-ai-table-insights` - 只读分析，不需要额外权限

### 责任分离

- **用户责任** - 提供 MCP 配置，保护敏感信息
- **技能责任** - 正确使用配置，不泄露信息

---

## 📊 版本兼容性

| dingtalk-ai-table | dingtalk-ai-table-insights | 状态 |
|-------------------|---------------------------|------|
| v1.0.0+ | v1.0.0+ | ✅ 兼容 |
| v1.0.0+ | v1.1.0+ | ✅ 兼容 |

---

## 🔍 故障排查

### 问题：找不到 MCP 配置

**症状：**
```
Error: Config file not found
```

**解决方案：**
1. 确认 `dingtalk-ai-table` 已正确配置
2. 检查配置文件路径
3. 设置环境变量 `DINGTALK_MCP_CONFIG`

### 问题：权限不足

**症状：**
```
Error: 403 - Access denied
```

**解决方案：**
1. 在 `dingtalk-ai-table` 中验证配置
2. 检查表格权限
3. 联系管理员

---

*最后更新：2025-02-28*  
*版本：v1.1.0*
