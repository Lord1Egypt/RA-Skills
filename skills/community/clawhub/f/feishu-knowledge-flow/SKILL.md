---
name: feishu-knowledge-flow
description: 知识管理全流程：文章链接/对话内容/文稿 → 结构化总结 → 飞书知识库归档。触发词："整理到飞书"、"帮我处理文章"、"/feishu-knowledge-flow"。
argument-hint: <url> | --chat [主题] | --summarize-only <url> | --screen-only <url> | --setup
allowed-tools: Bash(node *), Bash(lark-cli *), Bash(curl *), Bash(python3 *), Bash(rm *), Bash(mkdir *), Bash(cd *), WebFetch, Skill
---

# 知识管理工作流

输入（文章链接/对话/文稿）→ 抓取 → 总结 → 分类 → 飞书归档。

> **执行原则：全程自动，不中断不确认。** 用户说"整理到飞书"后，从抓取到总结到分类到写入到图片上传到索引更新，一口气跑完，中间不问用户任何问题。所有 bash 命令（curl/lark-cli/mkdir/rm 等）直接执行。

---

## 0. 首次使用引导（--setup 或自动检测）

每次执行工作流前，先做环境检查。**如果全部通过则静默继续，不打断用户**；只有检查失败时才进入引导流程。

### 0.1 检查清单

```bash
# 1) 检查 lark-cli 是否安装
which lark-cli 2>/dev/null || echo "NOT_INSTALLED"

# 2) 检查飞书认证状态
lark-cli auth status 2>/dev/null || echo "NOT_AUTHED"

# 3) 检查本 skill 目录下是否有 .wiki-config 配置文件
cat "${CLAUDE_SKILL_DIR}/.wiki-config" 2>/dev/null || echo "NOT_CONFIGURED"
```

### 0.2 引导流程（仅在检查失败时执行）

**Step 1：安装 lark-cli**（若未安装）

```
⚠️ 未检测到 lark-cli，这是连接飞书的必备工具。

安装方式（任选一种）：
  npm install -g @anthropic/lark-cli
  # 或参考 https://github.com/nicepkg/lark-cli

安装完成后重新运行 /knowledge-workflow --setup
```

**Step 2：飞书认证**（若未认证）

```
⚠️ 飞书尚未登录，需要先完成认证才能归档到知识库。

请运行：
  lark-cli config init    # 首次配置飞书应用
  lark-cli auth login      # 登录认证
```

提示用户运行命令后，等待用户确认再继续。

**Step 3：知识库配置**（若无 .wiki-config）

当认证通过后，引导用户完成知识库配置：

```
✅ 飞书已连接！现在配置你的知识库归档位置。

请提供以下信息：
1. 知识空间 ID（在飞书知识库 URL 中可以找到）
2. 索引文档 doc_id（可选，用于记录归档索引。没有的话我帮你新建一个）
```

收到信息后，自动：
1. 验证知识空间可访问：`lark-cli wiki spaces get --params '{"space_id":"<SPACE_ID>"}'`
2. 若用户没有索引文档，自动创建一个：
   ```bash
   lark-cli wiki nodes create --params '{"space_id":"<SPACE_ID>"}' \
     --data '{"node_type":"origin","obj_type":"docx","title":"【总】阅读文章索引"}' --as user
   ```
3. 将配置写入 `${CLAUDE_SKILL_DIR}/.wiki-config`：

```bash
cat > "${CLAUDE_SKILL_DIR}/.wiki-config" << 'WIKIEOF'
# 知识库配置（首次 setup 时自动生成）
WIKI_SPACE_ID=<用户提供的知识空间ID>
INDEX_DOC_ID=<索引文档的doc_id>
INDEX_NODE_TOKEN=<索引文档的node_token>
WIKIEOF
```

4. 初始化框架树配置 `${CLAUDE_SKILL_DIR}/.wiki-tree`（空模板）：

```bash
cat > "${CLAUDE_SKILL_DIR}/.wiki-tree" << 'TREEEOF'
# 知识库框架树
# 格式：分类路径 | node_token | doc_id
# 已有 doc 的节点直接用，新建节点后必须回填到此处。
#
# 示例：
# 大模型/Claude | L1n9xxxx | YoJHxxxx
# 大模型/GPT | AZubxxxx | HoBixxxx
# AI认知/AI方法论 | Mv8jxxxx | Hqfkxxxx
TREEEOF
```

**Step 4：确认完成**

```
🎉 配置完成！你的知识库已就绪：
  - 知识空间：<SPACE_ID>
  - 索引文档：<INDEX_DOC_ID>

现在你可以：
  - 发送文章链接，我会自动抓取、总结、归档到飞书
  - 说"整理到飞书"归档当前对话
  - /knowledge-workflow --setup 重新配置
```

### 0.3 加载配置

每次执行时从配置文件加载：

```bash
# 加载知识库配置
source "${CLAUDE_SKILL_DIR}/.wiki-config"
# 加载框架树（解析为查找表）
WIKI_TREE="${CLAUDE_SKILL_DIR}/.wiki-tree"
```

---

## 1. 模式路由

| 输入 | 模式 | 流程 |
|---|---|---|
| URL（无 flag） | 全流程 | 抓取 → 总结 → 归档 |
| 用户粘贴的文稿/口播 | 全流程 | 跳过抓取 → 总结 → 归档 |
| `--chat [主题]` | 对话归档 | 提取对话洞察 → 归档 |
| `--summarize-only <url>` | 仅总结 | 抓取 → 总结（不归档） |
| `--screen-only <url>` | 仅筛选 | 抓取 → 三维评分 |
| `--setup` | 配置 | 重新运行首次引导 |
| "整理到飞书" | 智能判断 | 根据上下文走全流程或对话归档 |

---

## 2. 内容抓取（两级回退，全自动）

依次尝试，成功即停。**禁止要求用户手动粘贴**，两级都失败则在最终报告中标记该条失败并跳过，不中断流程：

1. **Playwright**：`node "${CLAUDE_SKILL_DIR}/fetch-article.js" "<url>"`，返回 JSON，content > 200 字有效
2. **WebFetch**：prompt = "Extract full article: title, author, date, complete body text. Original language. Do not summarize."

---

## 3. 生成总结

### 格式模板

```markdown
---

# {序号}. {标题}

> 🔗 [原文链接]({url})
> ✍️ {作者}　　📅 {日期}

## 速览
{2-3句核心主张，10秒判断是否深读}

## 详细解读

### {块标题}
{150-300字，按原文逻辑复述}
```

> 序号规则：同一文档内的文章按写入顺序递增编号（1、2、3...），新文章追加时查看文档已有最大序号，+1 继续。

对话归档时，元数据行改为 `> 💬 对话归档　　📅 {日期}`，"详细解读"改为"核心洞察"。

### 图片处理

抓取文章时，同时提取文章中的图片 URL（`data-src` 属性，域名 `mmbiz.qpic.cn`）。筛选有价值的图片上传飞书：

**上传标准**：包含信息量大的图片才上传，包括：
- 数据图表、信息图、流程图、框架图
- 关键截图（产品界面、对比图、证据截图）
- 核心论点的可视化表达

**不上传**：纯装饰图、头像、二维码、广告图、表情包

**执行流程**：
1. 抓取时用正则提取所有 `data-src="https://mmbiz.qpic.cn/..."` 图片 URL
2. 判断哪些图片有信息价值（根据上下文位置和图片描述）
3. 下载到 `${CLAUDE_SKILL_DIR}/_imgs/` 临时目录
4. 文字内容写入飞书后，用 `+media-insert` 逐张上传并添加 caption
5. 上传完成后删除临时目录

```bash
# 下载图片
mkdir -p "${CLAUDE_SKILL_DIR}/_imgs"
curl -s -o "${CLAUDE_SKILL_DIR}/_imgs/name.png" "<img_url>" -H "Referer: https://mp.weixin.qq.com/"

# 上传到飞书文档（必须 cd 到图片目录用相对路径）
cd "${CLAUDE_SKILL_DIR}/_imgs" && lark-cli docs +media-insert \
  --doc "<doc_id>" --file "./name.png" --caption "图片说明" --align center --as user

# 清理
rm -rf "${CLAUDE_SKILL_DIR}/_imgs"
```

### 原则
- **用原作者的口吻和第一人称写**，不要用"作者认为"、"文章指出"等第三人称旁观视角。读起来像作者本人在讲给你听
- 忠于原文，不加外部知识
- 保留作者的语言风格、比喻、金句、口语化表达
- 作者/日期无法识别时省略该行
- 全流程模式不在对话中展示总结，直接归档

---

## 4. 飞书归档

### 4.1 加载配置

```bash
source "${CLAUDE_SKILL_DIR}/.wiki-config"
# WIKI_SPACE_ID, INDEX_DOC_ID, INDEX_NODE_TOKEN 均从配置文件读取
```

### 4.2 分类 → 查 token → 写入

**第一步：判断分类**

根据内容核心主张，匹配框架树（`.wiki-tree`）中已有的分类路径。无法匹配时新建节点。

**第二步：获取 doc_id**

- 框架树中已有 `doc_id` 的节点 → **直接用，不查 API**
- 框架树中无记录的分类 → 用 `lark-cli wiki nodes create` 创建，创建后立即更新 `.wiki-tree`

```bash
# 创建一级节点
lark-cli wiki nodes create --params "{\"space_id\":\"${WIKI_SPACE_ID}\"}" \
  --data '{"node_type":"origin","obj_type":"docx","title":"<名称>"}' --as user

# 创建二级节点（需指定 parent_node_token）
lark-cli wiki nodes create --params "{\"space_id\":\"${WIKI_SPACE_ID}\"}" \
  --data '{"node_type":"origin","obj_type":"docx","title":"<名称>","parent_node_token":"<父节点>"}' --as user
```

**第三步：写入内容**

```bash
cd "${CLAUDE_SKILL_DIR}" && lark-cli docs +update \
  --doc "<doc_id>" --mode append --as user --markdown @_temp.md
rm -f "${CLAUDE_SKILL_DIR}/_temp.md"
```

**第四步：更新索引**

新日期/新文章插入到索引文档**最顶部**（新的在上），使用 `insert_before` 定位到第一个日期标题前。**日期和星期必须用 `date` 命令动态获取，禁止写死或凭记忆**：

```bash
# 生成当日日期标题（中文星期）
TODAY=$(date +"%-m月%-d日 周$(date +%u | tr '1234567' '一二三四五六日')")
echo "## $TODAY"
```

```markdown
## {date 动态生成，如 4月23日 周四}
- [ ] [{标题}](https://www.feishu.cn/wiki/{node_token}) → {一级} / {二级}
```

```bash
# 插入到文档最前面（在第一个 ## 标题之前）
cd "${CLAUDE_SKILL_DIR}" && lark-cli docs +update \
  --doc "${INDEX_DOC_ID}" --mode insert_before \
  --selection-by-title "## " --as user --markdown @_index.md
rm -f "${CLAUDE_SKILL_DIR}/_index.md"
```

> 如果文档为空或找不到 `## ` 标题，回退用 `append` 模式。
> 同日追加文章时，用 `insert_after --selection-by-title "## {当日日期}"` 追加到该日期块下。

### 4.3 输出确认

```
✅ 已归档 → {一级} / {二级}
🔗 https://www.feishu.cn/wiki/{node_token}
📋 索引已更新
```

---

## 5. 对话归档（--chat 或"整理到飞书"）

### 触发条件

对话涉及以下话题时，可主动提示归档：
- AI 技术原理、大模型、Agent、提示工程
- 认知升级、思维框架、方法论
- 行业趋势、产品洞察、商业认知
- 社会现象、文化分析

日常闲聊、代码调试、文件操作不触发。

### 执行

1. 从对话中提取核心洞察，剥离噪声
2. 按第 3 节格式生成总结
3. 按第 4 节归档到飞书

---

## 知识库框架树

框架树存储在 `${CLAUDE_SKILL_DIR}/.wiki-tree`，格式为：

```
# 分类路径 | node_token | doc_id
大模型/Claude | <node_token> | <doc_id>
大模型/GPT | <node_token> | <doc_id>
AI认知/AI方法论 | <node_token> | <doc_id>
商业认知/AI产业 | <node_token> | <doc_id>
社会认知/人生哲学 | <node_token> | <doc_id>
```

> **已有 doc 的节点直接用，不查 API。新建节点后必须回填到 `.wiki-tree` 文件。**

### 分类速查（默认推荐分类，可自定义）

| 内容关键词 | 分类路径 |
|---|---|
| Claude/GPT/Gemini/具体模型 | 大模型 / {模型名} |
| Agent/多智能体/外化架构 | 大模型 / Agent架构 |
| MoE/Transformer/模型结构 | 大模型 / 模型架构 |
| AI使用心得/思维框架/方法论 | AI认知 / AI方法论 |
| 训练数据/算力/投融资/产业链 | 商业认知 / AI产业 |
| 产品/创业/商业模式 | 商业认知 / 产品/创业 |
| 社会现象/两性/文化心理 | 社会认知 / 两性与社会心理 |
| 人生哲学/认知框架/心态 | 社会认知 / 人生哲学 |
| 工作方法/效率/职业发展 | 职场效能 / {子类} |
| 以上都不匹配 | 新建最合适的一级+二级 |

---

## 错误处理

- 单篇失败不阻塞，跳过继续，最后汇总
- 权限不足 → 提示 `lark-cli auth login --domain all`
- 超过 5 篇 → 建议分批

---

## 附录：三维评分（--screen-only）

| 维度 | 5分 | 1分 |
|---|---|---|
| 信息密度 | 大量一手数据/案例 | 几乎无实质内容 |
| 原创性 | 全新框架/视角 | 纯搬运 |
| 实操性 | 读完立刻可照做 | 纯抽象讨论 |

总分 ≥ 10 通过。
