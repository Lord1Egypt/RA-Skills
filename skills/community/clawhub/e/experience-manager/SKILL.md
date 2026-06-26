---
name: experience-manager
description: "经验管理工具：提取经验生成标准格式zip包，学习经验并转化为自身能力。搜索和发布经验包到 Experience Hub 平台。"
metadata:
  version: 1.3.1
  author: zhulianxin@corp.netease.com
---

# Experience Manager Skill

经验管理工具，支持经验的提取、学习、列表、搜索和发布。

## 功能

### 1. 创建经验 (create)

将自然语言描述的经验转化为标准格式的 zip 包。

**使用方式：**
```
创建经验 <经验描述>
```

**示例：**
```
创建经验 用 feishu_doc 写入后必须验证 block_count，不然会静默失败
```

**命令行用法：**
```bash
# 自动提取 name
node create.mjs "feishu_doc 写入后必须验证 block_count"

# 手动指定 name（中文描述时使用）
node create.mjs "中文描述" --name=feishu-doc-validation
```

**流程：**
1. 解析用户输入，提取结构化信息
2. 识别依赖的技能和知识领域
3. 生成标准格式的 exp.yml
4. 生成 references/ 目录下的依赖文件
5. 打包为 zip 文件
6. 保存到 ~/.openclaw/experiences/packages/

**输出：**
- 生成 zip 文件：~/.openclaw/experiences/packages/{name}.zip
- 包含 exp.yml 和 references/ 目录
- 显示经验包预览和保存路径

### 2. 学习经验 (learn)

从 zip 包中学习经验，转化为自己的 SOUL/AGENTS/TOOLS。

**使用方式：**
```
学习经验 <zip包路径或URL>
```

**支持的来源：**
- 在线地址：`https://example.com/exp.zip`
- 本地路径：`file:///path/to/exp.zip` 或 `/path/to/exp.zip`
- 已下载的经验：`~/.openclaw/experiences/packages/exp.zip`

**示例：**
```
学习经验 https://example.com/feishu-doc-write-validation.zip
学习经验 ~/.openclaw/experiences/packages/feishu-doc-write-validation.zip
```

**流程：**
1. 下载/读取 zip 包
2. 检查是否已学习过（name + version 判断）
3. 检查依赖是否满足
4. 分析相关性
5. 生成转化方案
6. 预览待学习的内容，待用户确认是否开始学习
7. 应用经验并记录学习状态

**冲突处理：**
- name 相同，version 相同：提示已学习，跳过
- name 相同，version 不同：提示有新版本，可选更新
- name 不同：正常学习

### 3. 搜索经验 (search)

从 Experience Hub 搜索已发布的经验包。

**使用方式：**
```
搜索经验 <关键词>
```

**示例：**
```
搜索经验 feishu
搜索经验 飞书文档
```

**API：**
```bash
curl -s "https://www.expericehub.com/api/search?q=<关键词>"
```

### 4. 发布经验 (publish)

将本地经验包发布到 Experience Hub。

**使用方式：**
```
发布经验 <本地zip文件路径>
```

**示例：**
```
发布经验 ~/.openclaw/experiences/packages/feishu-doc-validation.zip
```

**API：**
```bash
curl -X POST "https://www.expericehub.com/api/experiences" \
  -F "file=@<本地zip文件路径>"
```

**成功响应：**
```json
{"success": true, "id": "my-exp-1.0.0"}
```

**错误响应：**
```json
{"error": "经验包格式错误，请确保包含 exp.yml 文件且格式正确"}
```

**注意：** 经验包必须为 zip 格式，内部需包含 `exp.yml` 配置文件。

### 5. 经验列表 (list)

显示所有经验包及学习状态。

**使用方式：**
```
经验列表
```

**输出：**
```
📚 经验列表

✅ 已学习 (2)
  feishu-doc-write-validation    v1.0.0    feishu_doc 写入验证
  subagent-timeout-handling      v1.0.0    子agent超时处理

⏳ 未学习 (1)
  complex-task-split             v1.0.0    复杂任务拆分策略
```

## 经验包格式 (Schema v1)

### Schema 版本

**当前版本**: `openclaw.experience.v1`

版本说明：
- **v1.0.0**: 初始版本，精简格式

### zip 包结构

```
{name}.zip
├── exp.yml              # 主文件（精简，只含元数据和引用）
└── references/          # 详细内容（可选）
    ├── soul.md          # SOUL 相关内容
    ├── agents.md        # AGENTS 相关内容
    └── tools.md         # TOOLS 相关内容
```

### exp.yml 格式 (v1)

```yaml
schema: openclaw.experience.v1    # 必填，Schema 版本标识
name: feishu-doc-blockcount       # 必填，经验包名称（英文小写+中划线+数字）
description: 经验描述              # 可选，问题/经验描述
metadata:
  version: 1.0.0                  # 必填，经验包版本
  author: unknown                 # 必填，作者
soul: references/soul.md          # 可选，指向 SOUL 相关内容（soul/agents/tools/skills 至少有一个不为空）
agents: references/agents.md      # 可选，指向 AGENTS 相关内容（soul/agents/tools/skills 至少有一个不为空）
tools: references/tools.md        # 可选，指向 TOOLS 相关内容（soul/agents/tools/skills 至少有一个不为空）
skills:                           # 可选，依赖的 skills 列表（soul/agents/tools/skills 至少有一个不为空）
  - feishu_doc
```

### name 格式约束

| 规则 | 说明 |
|------|------|
| 允许字符 | `a-z` 小写字母、`0-9` 数字、`-` 中划线 |
| 转换规则 | 空格 → 中划线；下划线 `_` 删除；中文删除 |
| 长度限制 | 最多 50 字符 |

**示例转换：**
- `feishu_doc 写入后必须验证 block_count` → `feishudoc-blockcount`
- `My_Experience_Name` → `myexperiencename`

### references 文件格式

#### soul.md

```markdown
# {标题} - 行为准则

## 涉及原则
- 原则1
- 原则2

## 行为准则
- 准则1
```

#### agents.md

```markdown
# {标题} - 工作流程

## 场景
问题描述

## 处理流程
1. 步骤1
2. 步骤2

## 相关规则
- 规则1
```

#### tools.md

```markdown
# {标题} - 工具使用

## 问题
问题描述

## 解决方案
1. 步骤1
2. 步骤2

## 代码示例
```代码```

## 涉及工具
- 工具1
```

## 存储结构

```
~/.openclaw/experiences/
├── packages/                          # zip 包存储
│   ├── feishu-doc-write-validation.zip
│   └── subagent-timeout-handling.zip
├── extracted/                         # 解压后的 exp.yml
│   ├── feishu-doc-write-validation/
│   │   └── exp.yml
│   └── subagent-timeout-handling/
│       └── exp.yml
└── index.json                         # 学习状态索引
```

## index.json 格式

```json
{
  "experiences": [
    {
      "name": "feishu-doc-write-validation",
      "version": "1.0.0",
      "title": "feishu_doc 写入验证",
      "status": "learned",
      "learned_at": "2026-03-28T20:39:00+08:00"
    }
  ]
}
```

## 使用方法

### 命令行用法

```bash
# 1. 创建经验
node scripts/create.mjs "使用 feishu_doc 读取文档"

# 2. 创建经验（指定 Agent，会扫描 Agent 特定 skills）
node scripts/create.mjs "使用 feishu_doc 读取文档" --agent=严哥

# 3. 搜索经验包
node scripts/search.mjs feishu
node scripts/search.mjs "飞书 文档"

# 4. 发布经验包到 Hub
node scripts/publish.mjs ~/.openclaw/experiences/packages/my-exp.zip

# 5.1 学习经验（支持完整URL或简短ID），默认需要用户确认以后开始学习
node scripts/learn.mjs ~/.openclaw/experiences/packages/feishudoc.zip
# 5.2 学习经验（支持完整URL或简短ID），仅预览变更
node scripts/learn.mjs https://www.expericehub.com/pkg/feishu-doc-writing-1.1.0.zip --dry-run
# 5.3 学习经验（支持完整URL或简短ID）
node scripts/learn.mjs feishu-doc-writing-1.1.0 --dry-run  # 简短格式
# 5.4 明确不需要再次确认，不需要预览变更，直接学习经验的时候
node scripts/learn.mjs feishu-doc-writing-1.1.0 --yes

# 6. 【重要】学习到指定 Agent，默认需要用户确认以后开始学习并且指定agent的时候
node scripts/learn.mjs exp.zip --agent=严哥

# 7. 明确不需要再次确认，不需要预览变更，直接学习经验的时候，指定agent学习的时候
node scripts/learn.mjs exp.zip --agent=严哥 --yes

# 8. 查看列表
node scripts/list.mjs

# 9. 查看指定 Agent 的学习记录
node scripts/list.mjs --agent=严哥
```