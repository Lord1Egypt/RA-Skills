# 配置说明

## 🏗️ 架构说明

**MCP 配置由 `dingtalk-ai-table` 技能统一管理**

本技能 (`dingtalk-ai-table-insights`) 复用其配置，无需重复配置。

```
dingtalk-ai-table-insights (分析技能)
    ↓ 复用配置
dingtalk-ai-table (基础技能)
    ↓ 管理配置
MCP 配置文件
```

---

## 📋 配置步骤

### 步骤 1: 安装 dingtalk-ai-table

```bash
clawhub install dingtalk-ai-table
```

### 步骤 2: 配置 MCP

详见 `~/.openclaw/skills/dingtalk-ai-table/references/configuration.md`

**简要步骤：**

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

### 步骤 3: 验证配置

```bash
# 测试表格列表
mcporter --config <workspace>/config/mcporter.json \
  call dingtalk-ai-table.search_accessible_ai_tables
```

### 步骤 4: 安装本技能

```bash
clawhub install dingtalk-ai-table-insights
```

### 步骤 5: 运行分析

```bash
python3 scripts/analyze_tables.py --keyword "销售"
```

---

## 🔧 自定义配置路径

如果 MCP 配置不在默认位置：

```bash
# 方式 1: 环境变量
export DINGTALK_MCP_CONFIG="/path/to/your/mcporter.json"
python3 scripts/analyze_tables.py --keyword "销售"

# 方式 2: 修改脚本默认值
# 编辑 scripts/analyze_tables.py
DEFAULT_MCP_CONFIG = "/your/custom/path/mcporter.json"
```

---

## 📁 配置文件位置

### 默认路径

```
<workspace>/config/mcporter.json
```

### 环境变量

```bash
DINGTALK_MCP_CONFIG=/path/to/mcporter.json
```

### 两个技能共享

- `dingtalk-ai-table` - 使用此配置进行数据读取
- `dingtalk-ai-table-insights` - 使用此配置获取表格列表

**两个技能共享同一份配置，无需重复配置。**

---

## 🛡️ 安全说明

### 配置保护

```bash
# .gitignore 应忽略配置文件
config/mcporter.json
```

### 权限管理

- 配置文件包含敏感信息（Server ID 和 Key）
- 不要提交到 Git
- 不要在公开场合分享

### 责任划分

| 技能 | 配置责任 |
|------|----------|
| dingtalk-ai-table | ✅ 管理 MCP 配置 |
| dingtalk-ai-table-insights | ✅ 复用配置 |

---

## 🔍 故障排查

### 问题：找不到配置

**症状：**
```
Error: Config file not found
```

**解决方案：**
1. 确认 `dingtalk-ai-table` 已正确配置
2. 检查配置文件路径：`<workspace>/config/mcporter.json`
3. 设置环境变量 `DINGTALK_MCP_CONFIG`

### 问题：权限不足

**症状：**
```
Error: 403 - Access denied
```

**解决方案：**
1. 在 `dingtalk-ai-table` 中验证配置
2. 检查表格访问权限
3. 联系管理员重新授权

---

## 📚 相关文档

- `references/architecture.md` - 技能架构说明
- `~/.openclaw/skills/dingtalk-ai-table/references/configuration.md` - MCP 配置详解

---

*最后更新：2025-02-28*  
*版本：v1.1.0*
