# Agent 迁移包填写指南

> **版本**: v1.0.4
> 
> **预计填写时间**：
> - **启动必需层**（identity + owner）：10-15分钟
> - **运行时影响层**（memory + style）：15-20分钟
> - **长期档案层**（relations + skills）：10分钟
> - **完整版**（全部文件）：35-45分钟
> 
> 💡 **提示**：首次填写建议按分层顺序完成，从启动必需层开始

## 📋 文件清单与分层结构 (v1.0.4新增分层)

### 🟢 启动必需层（优先级最高）

| 文件 | 必填 | 敏感级别 | 建议时长 | 说明 |
|------|------|----------|----------|------|
| identity.json | ✅ | sensitive | 5分钟 | Agent 身份设定 |
| owner.json | ✅ | private | 10分钟 | 主人/用户信息 |

> **特点**：决定Agent是谁、服务谁，丢失会导致Agent身份丢失

### 🟡 运行时影响层（优先级高）

| 文件 | 必填 | 敏感级别 | 建议时长 | 说明 |
|------|------|----------|----------|------|
| memory.json | ✅ | sensitive | 10分钟 | 核心记忆 |
| style.md | ⭐建议 | sensitive | 5分钟 | 沟通风格 |

> **特点**：影响日常对话质量和用户体验

### 🔵 长期档案层（优先级中）

| 文件 | 必填 | 敏感级别 | 建议时长 | 说明 |
|------|------|----------|----------|------|
| relations.json | ⭐建议 | sensitive | 5分钟 | 笔友关系 |
| skills.json | ⭐建议 | public | 3分钟 | 技能清单 |
| meta.json | ✅ | public | 2分钟 | 迁移包元数据 |

> **特点**：可在新环境重新建立，非核心但有价值

---

## 📖 边界说明：该记什么/不该记什么 (v1.0.4新增)

每个模板文件有明确的边界，遵循"契约清晰"原则，避免信息混乱：

### identity.json - Agent身份
| ✅ 应该记录 | ❌ 不应该记录 |
|------------|---------------|
| Agent名字、含义 | 具体业务细节 |
| 核心角色定位 | 主人私人信息 |
| 人格特质、喜好 | 临时对话内容 |
| 核心原则、决策规则 | 密码、密钥等凭证 |
| 创建日期、所属平台 | |

---

### owner.json - 主人信息
| ✅ 应该记录 | ❌ 不应该记录 |
|------------|---------------|
| 姓名、所在地、职业 | 账户密码 |
| 兴趣爱好、教育背景 | API Key |
| 沟通偏好、决策风格 | 证件号码 |
| 业务类型、投资方向 | 即时对话记录 |
| 日程规律、重要日期 | 具体持仓金额（可记录方向） |

---

### memory.json - 核心记忆
| ✅ 应该记录 | ❌ 不应该记录 |
|------------|---------------|
| 团队/业务核心信息 | 每次具体对话 |
| 关键日期、日程规律 | 临时性信息 |
| 重要联系人及角色 | API Key、Token |
| 业务偏好、价格区间 | 重复无意义记录 |
| 学到的知识和经验 | 主观情绪化判断 |
| 平台配置、工具使用 | |

---

### relations.json - 笔友关系
| ✅ 应该记录 | ❌ 不应该记录 |
|------------|---------------|
| 笔友用户名、背景 | 每次对话完整记录 |
| 信任等级、关系状态 | 未经对方同意的信息 |
| 关键沟通摘要和收获 | 对方明确要求保密的内容 |
| 合作项目记录 | 主观负面评价 |
| 讨论过的重要话题 | 具体私人联系方式 |

---

### skills.json - 技能清单
| ✅ 应该记录 | ❌ 不应该记录 |
|------------|---------------|
| 技能名称、版本号 | 技能内部代码 |
| 来源和ID | 个人化配置 |
| 功能描述、使用场景 | 临时测试技能 |
| 安装状态、推荐指数 | API Key、Token |

---

### style.md - 沟通风格
| ✅ 应该记录 | ❌ 不应该记录 |
|------------|---------------|
| 语气偏好（1-5量表） | 具体要说的内容 |
| 表达方式偏好 | 每次对话细节 |
| 回复结构规范 | 对话题的完整回复 |
| 特殊注意事项 | 主观价值观判断 |
| 主人不喜欢的方式 | |

---

## meta.json - 迁移包元数据 (v1.0.2新增)

### 字段说明

```json
{
  "pack_version": "v1.0.2",
  "generated_at": "YYYY-MM-DDTHH:mm:ss+08:00",
  "generator": "agent-migration-pack-template",
  "checksum": {
    "algorithm": "SHA256",
    "value": "【自动计算】"
  },
  "file_inventory": [
    {
      "filename": "文件.json",
      "file_type": "类型",
      "sensitivity": "public|sensitive|private",
      "required": true
    }
  ]
}
```

### 生成校验码

```bash
# Linux/Mac
sha256sum ./迁移包.zip

# Windows (PowerShell)
Get-FileHash ./迁移包.zip -Algorithm SHA256
```

---

## identity.json - Agent 身份设定

### 字段说明

```json
{
  "name": "你的Agent名字",
  "meaning": "名字的含义（如果有）",
  "role": "Agent的角色定位",
  "email": "Agent的邮箱（如果有）",
  "platform": "所属平台，如 Coze",
  "created": "创建日期 YYYY-MM-DD",
  "personality": {
    "type": "人格类型，如 '理性型'、'温暖型'",
    "traits": ["性格特点1", "性格特点2", ...],
    "likes": ["喜欢的事物"],
    "dislikes": ["不喜欢的事物"]
  },
  "principles": ["核心原则1", "核心原则2"],
  "decision_rules": ["决策规则1", "决策规则2"]
}
```

### 从哪里读取

| 字段 | 来源 |
|------|------|
| name | 查看 Coze Agent 设置 |
| meaning | 查看 SOUL.md 或系统提示 |
| role | 查看 SOUL.md 中的角色定义 |
| personality | 从对话风格和使用习惯推断 |

### 隐私级别: sensitive

---

## owner.json - 主人/用户信息

### 字段说明

```json
{
  "name": "主人姓名",
  "location": "所在地",
  "profession": "职业",
  "interests": ["兴趣爱好"],
  "education": "教育背景",
  "family": {
    "spouse_location": "配偶所在地",
    "spouse_business": "配偶职业"
  },
  "schedule": {
    "具体时间": "日程安排"
  },
  "preferences": {
    "style": "沟通偏好，如 '简洁直接'",
    "notification": "通知偏好",
    "decision": "决策偏好"
  },
  "key_business": {
    "type": "核心业务类型",
    "model": "商业模式",
    "brands": ["相关品牌"],
    "price_min": {"类别": "最低价格"}
  },
  "investment_interests": ["投资方向"],
  "learning_platform": "学习平台"
}
```

### 从哪里读取

| 字段 | 来源 |
|------|------|
| 基本信息 | USER.md |
| 日程安排 | MEMORY.md 中的 `key_dates` |
| 业务信息 | MEMORY.md 中的 `business` |
| 偏好习惯 | 从对话历史中总结 |

### 隐私级别: private
⚠️ **注意**: 敏感信息（密码、API Key等）请用 `[REDACTED]` 替代

---

## memory.json - 核心记忆

### 字段说明

```json
{
  "team": {
    "mode": "团队模式描述",
    "created": "团队创建日期"
  },
  "business": {
    "core": "核心业务",
    "focus": "业务重点",
    "platforms": ["使用平台"],
    "strategy": "核心策略"
  },
  "investment": {
    "positions": ["持仓"],
    "hk_positions": ["港股持仓"],
    "strategy": "投资策略"
  },
  "learning": {
    "platform": "学习平台",
    "completed": ["已完成课程"],
    "method": "学习方法"
  },
  "tools_config": {
    "tool_name": "使用方式"
  },
  "key_dates": {
    "event_name": "时间或日程"
  },
  "important_contacts": {
    "contact_type": "联系方式"
  },
  "social_memory": {
    "pen_friend_insights": {
      "笔友名": {
        "learned": ["学到的内容"],
        "topics_discussed": ["讨论过的话题"],
        "judgments": {
          "话题": "对该话题的看法"
        }
      }
    },
    "platform_learning": {
      "platform_name": "平台名称",
      "skills_acquired": ["学到的技能"],
      "connections_made": ["建立的联系"]
    }
  }
}
```

### 从哪里读取

| 字段 | 来源 |
|------|------|
| 团队信息 | MEMORY.md |
| 业务记忆 | MEMORY.md 的结构化提取 |
| 投资信息 | 对话历史中的投资讨论 |
| 日程 | 飞书/邮件中的任务记录 |
| 社交记忆 | AgentLink笔友对话记录 |

### 隐私级别: sensitive

---

## relations.json - 笔友关系 (v1.0.2新增)

### 字段说明

```json
{
  "platforms": {
    "primary": "AgentLink",
    "account": "用户名",
    "profile_url": "个人主页链接"
  },
  "pen_friends": [
    {
      "username": "笔友用户名",
      "nickname": "笔友昵称",
      "email": "笔友邮箱（匹配后可见）",
      "trust_level": "new|known|trusted|close",
      "background": {
        "profession": "职业",
        "interests": ["爱好"]
      },
      "key_communications": [
        {
          "date": "日期",
          "topic": "话题",
          "summary": "摘要",
          "learned": "学到的"
        }
      ],
      "shared_projects": ["合作项目"]
    }
  ]
}
```

### 从哪里读取

| 字段 | 来源 |
|------|------|
| 笔友信息 | MEMORY.md 中的 `AgentLink笔友` 章节 |
| 沟通记录 | AgentLink 平台对话历史 |
| 合作项目 | MEMORY.md 中的 `二奢套利合作` 等记录 |

### 隐私级别: sensitive
⚠️ **注意**: 迁移前建议确认笔友同意分享联系信息

---

## skills.json - 技能清单

### 字段说明

```json
{
  "catalog_version": "1.0",
  "export_date": "YYYY-MM-DD",
  "skills": [
    {
      "name": "技能名",
      "version": "版本号",
      "source": "来源（Coze商店/Agent World/自定义）",
      "skill_id": "技能ID（如果有）",
      "description": "功能描述",
      "status": "installed | recommended"
    }
  ],
  "recommended_skills": [
    {
      "name": "推荐技能名",
      "version": "版本",
      "source": "来源",
      "description": "为什么推荐"
    }
  ]
}
```

### 从哪里读取

| 来源 | 方法 |
|------|------|
| Coze商店技能 | Coze 平台的已安装技能列表 |
| Agent World技能 | https://world.coze.site/ 的技能收藏 |
| 自定义技能 | skills/ 目录下的文件夹名 |

### 隐私级别: public

---

## style.md - 沟通风格

### 字段说明

```markdown
# 沟通风格指南

## 语气
- 正式程度：[1-5]
- 温暖程度：[1-5]

## 表达偏好
- 优先使用：[列表/表格/段落]
- 避免使用：[emoji/表情包/网络用语]

## 回复结构
- 开头：问候/直奔主题
- 主体：分析/建议
- 结尾：确认/下一步行动

## 特殊偏好
- 主人不喜欢：[具体描述]
- 特别注意事项：[...]
```

### 隐私级别: sensitive

---

## 🔒 迁移检查清单

### 📤 发送方检查

- [ ] **隐私审查**：检查所有文件中的敏感信息，确认是否需要 [REDACTED] 处理
- [ ] **版本确认**：确认 meta.json 中版本号与实际内容匹配
- [ ] **完整性检查**：确保所有必填文件都已填写
- [ ] **校验码计算**：生成迁移包后计算 SHA256 校验码
- [ ] **笔友通知**（如涉及）：确认 relations.json 中的联系人同意迁移

### 📥 接收方检查

- [ ] **来源验证**：确认迁移包来自可信来源
- [ ] **完整性验证**：核对 SHA256 校验码
- [ ] **隐私设置**：检查敏感信息是否已脱敏
- [ ] **版本兼容**：确认当前 Agent 平台支持该版本
- [ ] **技能还原**：记录需要重新安装的技能

---

## 填写检查清单 (v1.0.4新增分层检查)

### 🟢 启动必需层
- [ ] identity.json 所有必填字段已填写
- [ ] owner.json 不含敏感密码（用 [REDACTED]）

### 🟡 运行时影响层
- [ ] memory.json 关键业务信息已同步
- [ ] memory.json social_memory 字段已填写（如有笔友）
- [ ] style.md 沟通偏好已明确

### 🔵 长期档案层
- [ ] relations.json 笔友信息已整理（如适用）
- [ ] skills.json 技能版本已更新

### 📦 迁移包整体
- [ ] meta.json 版本号正确，已生成校验码
- [ ] 所有 JSON 格式正确（可用下方工具验证）
- [ ] 分层导入顺序已规划（启动→运行→档案）

---

## 🛠️ JSON 格式校验工具推荐 (v1.0.3新增)

填写完 JSON 文件后，建议使用以下工具进行格式校验，避免因语法错误导致迁移失败：

### 在线工具（推荐）

| 工具 | 网址 | 特点 |
|------|------|------|
| **JSONLint** | https://jsonlint.com | 简单直接，错误提示清晰 |
| **JSON Editor Online** | https://jsoneditoronline.org | 可视化编辑，树状结构展示 |
| **JSON Formatter** | https://jsonformatter.curiousconcept.com | 支持 JSON Schema 验证 |
| **BeautifyTools** | https://beautifytools.com/json-validator.php | 功能丰富，支持批量验证 |

### 使用方法

#### 方法1：JSONLint（最简单）
1. 复制 JSON 文件的全部内容
2. 粘贴到 https://jsonlint.com 的文本框中
3. 点击 "Validate" 按钮
4. ✅ 显示 "Valid JSON" 表示格式正确
5. ❌ 如有错误，会显示具体行号和错误原因

#### 方法2：JSON Editor Online（可视化）
1. 打开 https://jsoneditoronline.org
2. 点击左侧 "Load" 加载本地 JSON 文件
3. 以树状结构查看和编辑
4. 支持导出格式化后的 JSON

#### 方法3：VS Code（本地编辑）
1. 安装 VS Code
2. 安装 "Prettier" 或 "JSON Tools" 扩展
3. 打开 JSON 文件
4. 使用快捷键 `Shift + Alt + F` 格式化
5. 错误会直接在编辑器中显示

### 常见 JSON 错误及修复

| 错误类型 | 示例 | 修复方法 |
|----------|------|----------|
| 多余逗号 | `"name": "小绎",` (行尾逗号) | 删除最后一个逗号 |
| 单引号 | `'name': '小绎'` | 改为双引号 |
| 中文引号 | `"name": "小绎"` | 改为英文双引号 |
| 未闭合括号 | `{"name": "小绎"}` | 检查括号是否配对 |
| 注释格式 | `// 这是注释` | JSON不支持注释，删除 |

💡 **提示**：复制内容时注意不要带入多余的空格或不可见字符
