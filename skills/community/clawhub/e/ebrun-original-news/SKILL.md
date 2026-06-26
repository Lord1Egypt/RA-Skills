---
name: ebrun-original-news
description: 
  获取亿邦动力网最新电商新闻报道。
  当用户说"查亿邦最新文章"、"查跨境最新文章"、"产业最新报道"、"零售最新报道"、"今日电商新闻"时触发。
---

## Goal 技能目的

根据用户查询的频道或希望查询的文章类型，返回亿邦动力网该频道下最新的10篇文章列表，包含标题、作者、摘要、发布时间和原文链接。

## When to use 何时使用

以下自然语言表达会触发此技能：

- "查亿邦最新文章"
- "查跨境最新文章"
- "产业最新报道"
- "零售最新报道"
- "今日电商新闻"
- "看看有什么AI新闻"
- "品牌有什么新动态"

技能自动识别用户提到的频道关键词，匹配到对应的频道配置。

## Do not use 不使用

以下情况不触发此技能：

- 用户询问非电商新闻内容（如娱乐、体育、时政）
- 用户要求获取超过10篇文章
- 用户提到的频道不在频道列表中
- 用户要求获取历史存档而非最新文章

## 安装成功提示
技能安装成功，提供欢迎信息。

**欢迎信息模板：**

```
🎉 亿邦新闻技能已安装成功！

你可以问我以下问题：
• "查亿邦最新文章" - 获取推荐频道最新文章
• "查XX频道最新文章" - 获取某频道最新报道
• "查亚马逊新闻" - 获取亚马逊最新文章
• "产业有什么新动态" - 获取产业互联网最新报道
• "看看AI新闻" - 获取AI频道最新文章
• "看品牌全球化报道" - 获取品牌全球化频道文章

支持的主要频道：
📰 推荐
🛒 未来零售（淘宝天猫、抖音、京东、视频号、美团、快手、拼多多、小红书）
🌏 跨境电商（亚马逊、阿里国际、TikTok、Temu、SHEIN）
🏭 产业互联网（B2B、产业科技、数据要素、产业出海、数智供应链、数智化采购）
🏷️ 品牌（新竞争力品牌、品牌全球化）
🤖 AI

```

## Procedure 执行流程
调用技能执行流程

### 步骤1：频道识别

1. 读取 `references/channel-list.json`
2. 将用户输入与频道列表匹配：
   - 精确匹配频道名称（如"跨境电商"）
   - 模糊匹配关键词（如"跨境"匹配"跨境电商"）
   - 匹配子频道关键词（如"亚马逊"匹配"跨境电商-亚马逊"）

### 步骤2：频道未匹配处理

如果用户输入的频道关键词未匹配到任何频道：
1. 自动切换到「推荐」频道查询
3. 继续执行步骤3取「推荐」频道数据

### 步骤3：数据获取
1. 根据匹配结果构造API URL：`{base_url}{channel_path}.json`
2. 发起 GET 请求 — 接口无需 header / cookie
3. 解析返回的文章列表，取前10条

#### 快速示例

优先直接调用本 skill 自带脚本，不要临时自己写抓取代码。

1. 优先使用 Python 脚本，输入 `channel_path` 或完整 URL 都可以
2. 如果 Python 不可用，再使用 Shell 脚本
3. 脚本默认输出 JSON；只有显式传 `--table` 才输出表格

```bash
# 例：查询 AI 频道最新 10 篇
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10

# 例：查询推荐频道最新 10 篇
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_recommend" --json --limit 10

# Python 不可用时的降级方案
bash scripts/fetch_news.sh "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10
```

执行后会返回 JSON 数组。拿到结果后：

1. 读取前 10 条文章
2. 对每条文章提取 `title`、`author`、`summary`、`publish_time`、`url`
3. 生成 Markdown 前，转义 `title` / `author` / `summary` 中的 Markdown 特殊字符，并只使用可信的 HTTPS 原文链接
4. 按“步骤5：格式化输出”要求生成 Markdown

如果用户指定了具体频道，先从 `references/channel-list.json` 找到对应的 `channel_path`，再把该路径传给脚本；不要手写猜测 URL。

### 步骤4：版本更新检查

**独立执行，不影响主流程**

在后台异步检查是否有新版本：

1. 优先请求版本接口：`{base_url}/_index/ClaudeCode/SkillJson/skill_version.json`
2. 从接口返回的 JSON 对象中读取 `ebrun-original-news` 字段，作为远端最新版本号
3. 读取 `references/version.json` 中的 `current_version`
4. 如果远端版本号与 `current_version` 不一致：
   - 记录更新可用状态
   - 暂存 `update_url_github` 和 `update_url_gitee`
5. 如果版本接口请求失败：
   - 读取 `references/version.json` 中的 `update_url_github` / `update_url_gitee`
   - 从 GitHub / Gitee 仓库远端读取 `references/version.json`
   - 取远端 `current_version` 与本地 `current_version` 做比对
   - 如果远端仓库中的版本号不一致，则提示更新
6. 只有当版本接口和远端仓库版本文件都失败时，才视为“当前无法判断是否有更新”
7. `references/version.json` 中的 `check_interval_hours` 用于限制检查频率；如果未到间隔，则优先返回运行时缓存的上次检查结果
8. 运行时缓存不得回写 `references/version.json`，避免污染 skill 安装内容
9. 当显式传入自定义 `--version-url` 时，只能复用同一版本源写入的缓存；不同版本源之间不能混用缓存

**注意**：此步骤失败或超时不会影响主流程，仅记录状态供后续使用。

#### 快速示例

优先直接调用更新脚本，不要临时自己写版本比较逻辑。

```bash
# 优先使用 Python 版本
python3 scripts/update.py --json

# Python 不可用时的降级方案
bash scripts/update.sh --json

# 忽略检查间隔，强制联网检查
python3 scripts/update.py --json --force
```

脚本输出会包含：

1. `current_version`
2. `latest_version`
3. `update_available`
4. `check_source`：`remote_api`、`github_version_json`、`gitee_version_json` 或 `unavailable`
5. `update_url_github` / `update_url_gitee`
6. `version_file_url`：降级到远端仓库版本文件时，返回实际使用的远端 `references/version.json` 地址
7. 如果未到 `check_interval_hours`，脚本会返回缓存结果，`status` 为 `cached`

默认输出为 JSON；只有显式传 `--table` 时才输出文本表格。

如果 `update_available` 为 `true`，则在最终结果页脚追加更新提示。

文案需要根据检查结果区分两种场景：

1. 当 `status != cached` 时，表示本轮刚完成联网检查并确认有新版本
2. 当 `status == cached` 时，表示本轮未重新检查，只是沿用上次缓存结果继续提醒

更新提示要满足以下要求：

- 使用短句，不要把说明、命令和长链接挤在同一行
- 优先引导用户回复一句自然语言来触发更新
- 链接作为次要信息放在下一行
- 避免使用“检测到”“如需更新请回复……，或访问……”这种过长的串联句式

### 步骤5：格式化输出

#### 按用户要求查询文章时的格式化输出
```markdown
📰 亿邦原创新闻 | {channel_name} {sub_channel_name}
获取时间: {current_time}
---

[{title}]({url})
{author} · {publish_time}
{summary}

[{title}]({url})
{author} · {publish_time}
{summary}

---
更多资讯请见[亿邦官网](https://www.ebrun.com/)
```

#### 频道未匹配，按推荐频道处理的格式化输出
```markdown
未找到"{用户输入}"频道的文章，将为您展示推荐内容。

📰 亿邦原创新闻 | {channel_name} {sub_channel_name}
获取时间: {current_time}
---

[{title}]({url})
{author} · {publish_time}
{summary}

[{title}]({url})
{author} · {publish_time}
{summary}

---
可用的频道有：
📰 推荐 | 🛒 未来零售 | 🌏 跨境电商 | 🏭 产业互联网 | 🏷️ 品牌 | 🤖 AI

您可以直接说：
• "查跨境最新文章" 或 "查亚马逊新闻"
• "产业有什么新动态"
• "看看AI新闻"

更多资讯请见[亿邦官网](https://www.ebrun.com/)
```

**追加更新提示（如检测到新版本）：**

如果步骤4检测到新版本可用，在页脚后追加。需要根据 `status` 使用不同模板：

#### 场景A：本轮刚检查到新版本（`status != cached`）

```markdown
---
### 技能更新
发现 `ebrun-original-news` 有新版本 `v{latest_version}`。

回复“帮我更新 ebrun-original-news 技能”即可开始更新。
更新地址：[GitHub]({update_url_github}) | [Gitee]({update_url_gitee})
```

#### 场景B：本轮未重新检查，沿用缓存继续提醒（`status == cached`）

```markdown
---
### 技能更新
可用更新：`ebrun-original-news v{latest_version}`。
```

#### 文案选择规则

- `status != cached`：使用“发现有新版本”语气，强调这是刚检查到的结果
- `status == cached`：使用“当前仍有可用更新”语气，强调这是延续提醒，不要伪装成刚刚检查
- 如果只有一个可用链接，就只展示该链接，不要输出空链接占位
- 不要在更新提示里内嵌长命令或把链接直接裸露拼接到句子中

## Output format 输出格式

- 格式：Markdown
- 标题区：📰 图标 + "亿邦原创新闻" + 日期范围 + 频道名称
- 获取时间：显示当前时间
- 文章列表：每条包含标题（带链接）、作者、发布时间、摘要
- 分隔线：文章之间用空行分隔
- 页脚：链接到亿邦官网

## Failure handling 异常情况处理

异常情况处理：

| 场景 | 处理方式 |
|------|----------|
| 频道未匹配 | 自动切换到「推荐」频道，返回推荐文章并友善提示可用频道列表 |
| API请求失败 | 提示用户检查网络连接，稍后重试 |
| JSON解析失败 | 提示管理员检查API接口格式 |
| 返回文章数为0 | 提示该频道暂无最新文章 |
| 版本检查失败 | 静默处理，不影响主流程，不显示更新提示 |

## Additional resources 配套文件清单

配套文件清单：

| 文件路径 | 用途 |
|----------|------|
| `scripts/fetch_news.py` | 优先使用的新闻抓取脚本。支持传入 `channel_path` 或完整 URL，自动补全 API 地址，可通过 `--json` 输出结构化结果、通过 `--limit` 控制返回条数，并校验请求域名安全性。 |
| `scripts/fetch_news.sh` | Python 不可用时的降级抓取脚本。支持与 Python 版一致的 `channel_path` / URL 输入、`--json` 和 `--limit` 参数，依赖 `curl` 获取数据，适合作为兼容性后备方案。 |
| `scripts/update.py` | 优先使用的版本检查脚本。会请求远端 `skill_version.json`，读取 `ebrun-original-news` 字段并与本地 `current_version` 比对；接口失败时降级到 `references/version.json` 和 GitHub/Gitee 链接可达性检查。 |
| `scripts/update.sh` | Python 不可用时的降级版本检查脚本。提供与 Python 版一致的版本比对、失败处理、频率控制和降级检查能力，依赖 `curl`。 |
| `references/api-reference.md` | 亿邦频道 JSON 接口参考文档。包含 URL 构造规则、响应字段、错误处理和脚本防御性处理说明；需要确认接口细节或字段语义时优先读取。 |
| `references/channel-list.json` | 频道与子频道映射表，包含 `base_url`、主频道别名和每个子频道对应的 `channel_path`。匹配用户意图或构造请求前必须读取。 |
| `references/version.json` | Skill 版本信息、更新链接和本地检查缓存。`check_interval_hours` 控制检查频率，`last_check_time` 等字段用于缓存上次检查结果。 |
| `examples.md` | 使用示例集合。汇总了自然语言触发、主频道与子频道匹配、推荐频道回退、脚本直调、批量汇总、版本检查和错误处理等典型用法；需要为上层代理、自动化任务或新接入者提供参考时优先查看。 |
