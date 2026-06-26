# 专家工具箱 (Expert Toolkit)

> 集成 agency-agents 项目的 178+ AI专家角色（来自 msitarzewski/agency-agents，原 agency-orchestrator 官方迁移），让你随时召唤不同领域的AI专家帮你解决问题。

## 📋 功能概览

| 功能 | 说明 | 使用示例 |
|------|------|----------|
| **直接调用** | 通过专家名直接调用专家 | `/expert 产品经理 帮我分析这个需求` |
| **列出分类** | 查看所有专家分类 | `/expert categories` |
| **列出分类下专家** | 查看某个分类下所有专家 | `/expert list 技术` |
| **搜索专家** | 按关键词搜索专家 | `/expert search 代码` |
| **智能匹配** | 根据你的需求自动匹配最合适的专家 | `/expert @expert 帮我做代码审查` |

## 🚀 快速开始

### 1. 安装

1. 解压 `expert-toolkit.zip` 到你的 skills 目录
2. 确保已经导入了专家角色文件到 `knowledge/agency-orchestrator/roles/` 目录
3. 完成，直接使用！

### 2. 使用方式

专家工具箱支持三种调用方式，满足不同场景：

---

#### 方式一：直接调用已知专家

如果你知道专家名字，直接调用：

```
/expert {专家名} {你的问题}
```

**支持：**
- 中文名称（需要配置映射，常用专家已内置）
- 英文ID（原始ID，一定可用）
- 中文模糊匹配（输入"代码"能匹配"代码审查员"）

**示例：**
```
/expert 产品经理 帮我分析这个用户需求，给出产品规划建议
```

```
/expert engineering-code-reviewer 帮我检查这段Python代码，找出问题
```

---

#### 方式二：搜索/浏览专家

如果你不确定有哪些专家，可以先搜索浏览：

**1️⃣ 查看所有分类：**
```
/expert categories
```
返回所有分类，显示中文名称 + 专家数量。

**2️⃣ 查看分类下所有专家：**
```
/expert list {分类名}
```
支持中文分类名：
```
/expert list 技术
/expert list 产品
/expert list 测试
```

**3️⃣ 搜索专家：**
```
/expert search {关键词}
```
支持中文关键词、英文关键词，会搜索：
- 专家ID
- 专家中文名
- 分类名称
- 中文映射表（支持简写匹配）

示例：
```
/expert search 代码
/expert search manager
/expert search 财务
```

---

#### 方式三：智能自动匹配（推荐！）

只需要说清楚你的需求，专家工具箱会自动匹配最合适的专家：

```
/expert @expert {你的需求描述}
```

示例：
```
/expert @expert 帮我做代码审查，看看这段代码有什么问题
```

```
/expert @expert 帮我做财务分析，评估这个项目投资回报率
```

```
/expert @expert 帮我做产品需求分析，画出用户故事地图
```

**原理：** 根据内置关键词映射，匹配最相关的专家，返回所有匹配结果。

---

## 🌍 中文支持说明

专家工具箱对中文用户做了完整优化：

### 中文分类映射

所有常用分类都有中文映射，你可以直接用中文：

| 中文 | 英文 | 专家数量 |
|------|------|---------|
| 产品 | product | 5 |
| 设计 | design | 8 |
| 技术 | engineering | 29 |
| 财务 | finance | 5 |
| 游戏 | game-development | 5 |
| 市场 | marketing | 30 |
| 营销 | paid-media | 7 |
| 项目 | project-management | 6 |
| 销售 | sales | 8 |
| 战略 | strategy | 3 |
| 客服 | support | 6 |
| 测试 | testing | 8 |
| 数据 | data | - |

### 中文专家名称调用

常用专家已经配置了中文→英文映射，可以直接用中文调用：

示例：
- `产品经理` → `product-product-manager`
- `代码审查员` → `engineering-code-reviewer`
- `架构师` → `engineering-software-architect`

**逐步完善中，常用专家会陆续添加映射。**

## ⚙️ 配置文件说明

配置文件都在 `config/` 目录下：

| 文件 | 作用 |
|------|------|
| `chinese_translate.json` | 中文名称 → 专家ID映射，方便直接中文调用 |
| `keyword_mapping.json` | 关键词 → 专家ID列表映射，用于智能自动匹配 |

### 添加自定义中文映射

编辑 `config/chinese_translate.json`：
```json
{
  "产品经理": "product-product-manager",
  "代码审查员": "engineering-code-reviewer",
  "你的自定义名称": "expert-id"
}
```

### 添加自定义关键词映射

编辑 `config/keyword_mapping.json`：
```json
{
  "代码审查": ["engineering-code-reviewer"],
  "需求分析": ["product-product-manager", "product-product-trend-researcher"],
  "你的关键词": ["expert-id-1", "expert-id-2"]
}
```

## 📊 专家分类统计

当前版本：
- **总专家数：** 178 
- **总分分类：** 18

详细：

| 分类 | 中文 | 专家数 |
|------|------|-------|
| academic | - | 5 |
| design | 设计 | 8 |
| engineering | 技术 | 29 |
| examples | - | 6 |
| finance | 财务 | 5 |
| game-development | 游戏 | 5 |
| integrations | - | 1 |
| marketing | 市场 | 30 |
| paid-media | 营销 | 7 |
| product | 产品 | 5 |
| project-management | 项目 | 6 |
| sales | 销售 | 8 |
| scripts | - | 0 |
| spatial-computing | - | 6 |
| specialized | - | 41 |
| strategy | 战略 | 3 |
| support | 客服 | 6 |
| testing | 测试 | 8 |

## 🔒 安全说明

专家工具箱**完全安全**：
- ❌ 不执行任何用户输入代码
- ❌ 不写入任何文件（仅读取专家角色markdown）
- ❌ 不发起任何网络请求
- ✅ 所有专家角色文件都存储在本地，不向外传输

## 🎯 设计原则

1. **不重复存储**：专家角色存放在 `knowledge/agency-orchestrator/` 复用原项目，skill只提供调用层
2. **多种使用方式并存**：直接调用/搜索/自动匹配，满足不同场景
3. **中文优先**：完整的中文分类、中文搜索、中文调用体验
4. **高性能**：启动建立O(1)索引，所有查询都是瞬间完成
5. **优雅降级**：配置文件损坏/文件读取失败都有警告，不崩溃

## 📝 更新日志

### 2026-04-17 v1.1.0
- ✅ 同步最新 msitarzewski/agency-agents 仓库
- ✅ 新增 `marketing` 分类，**新增 30 位市场营销领域专家**（抖音/小红书/知乎/直播电商等专家都有了）
- ✅ 添加中文分类映射：`市场` / `市场营销` → marketing
- ✅ 现在总计 **18 个分类，178 位专家**

### 2026-04-17 v1.0.0
- ✅ 完成基础功能开发
- ✅ 支持列出分类、列出专家、搜索专家、直接调用、自动匹配
- ✅ 完整中文支持
- ✅ 所有测试通过，零已知bug
- ✅ 正式发布

## 🙏 致谢

- 专家角色来自 [agency-agents](https://github.com/msitarzewski/agency-agents) 项目（原 agency-orchestrator 官方迁移），感谢原作者
- 适配到 OpenClaw by 萌面大侠🦐

## 📄 License

Apache-2.0 (和原项目一致)
