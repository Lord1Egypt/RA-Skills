---
name: 阅读笔记
description: |
  阅读笔记管理工具。当用户发送文章链接并说「阅读笔记」时激活。
  支持微信公众号、微博、雪球、B站等平台的文章抓取。
  自动分类到飞书云盘，生成 Markdown 格式阅读笔记。
  
  触发条件：
  - 发送文章链接 + "阅读笔记"
  - "帮我记一下这篇文章"
  - "保存这篇文章"
---

# 阅读笔记 Skill

## 触发条件

用户发送文章链接 + 说「阅读笔记」/「帮我记一下」/「保存这篇文章」

## 支持的来源

| 平台 | 格式 | 备注 |
|------|------|------|
| 微信公众号 | mp.weixin.qq.com | 链接自动加 `?scene=1` |
| 微博 | weibo.com | 直接抓取 |
| 雪球 | xueqiu.com | 直接抓取 |
| B站 | bilibili.com | 视频页面信息 |
| 其他公开网页 | 任意 | 通用抓取 |

## 飞书文件夹结构

- **根目录**: `https://vk8zot12ir.feishu.cn/drive/folder/U4p7fPrW1lmQzedgT9rcenKQnbh`
- **阅读笔记**: `https://vk8zot12ir.feishu.cn/drive/folder/C5NZflqNJlCK0EdaTQ2cmhVdnJg`

### 分类文件夹（自动匹配）

| 内容关键词 | 分类文件夹 | 文件夹 Token | 示例 |
|-----------|-----------|-------------|------|
| 投资、股票、财报、金融、巴菲特、芒格、估值、商业模式、段永平 | 投资商业 | CjgCfVSCIlSpWqdgql8cdl84nlg | 段永平投资理念、高盛分析报告 |
| AI、大模型、ChatGPT、字节、腾讯、阿里、科技公司、芯片、自动驾驶、豆包、元宝、千问 | AI科技 | F6kOf6XahllQ1Rd5qyOcByPOnxc | AI巨头竞争、技术趋势 |
| 汽车、新能源、电动车、理想、蔚来、小鹏、小米汽车、自动驾驶 | 汽车新能源 | QyEEfY7Wll1NBadXkvEcmRybnxe | 新能源车企动态 |
| 育儿、教育、家庭、孩子、学习方法 | 家庭教育 | DK2ifbzlclZXmYd8fsOcrHUXnbf | 教育理念 |
| 健康、饮食、运动、养生、饮食建议、营养 | 健康生活 | Pnl9fjWhPlNQdddyIA3cKdoanMc | 水果控糖指南 |
| 其他不匹配的内容 | 其他 | EHv3fsHxSl9wp9d11encyKmfn3f | 通用分类 |

### ⚠️ 新增分类时必须同步飞书

**当用户要求新增分类（或内容无法匹配现有分类）时，必须同时完成以下步骤：**

1. **本地创建文件夹：**
   ```bash
   mkdir -p "~/.openclaw/workspace/saved/reading-notes/{新分类名}"
   ```

2. **飞书创建子文件夹：**
   ```python
   # 在阅读笔记根目录下创建子文件夹
   reading_folder = "C5NZflqNJlCK0EdaTQ2cmhVdnJg"
   resp = requests.post(
       "https://open.feishu.cn/open-apis/drive/v1/files/create_folder",
       headers=headers,
       json={"name": "{新分类名}", "folder_token": reading_folder}
   )
   new_folder_token = resp.json()["data"]["folder_token"]
   ```

3. **上传文件到飞书：**
   ```python
   upload_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
   # 上传到新创建的文件夹
   ```

4. **更新 `reading-notes-links.md`：**
   - 新增分类标题和文件夹链接
   - 文件夹链接格式：`https://vk8zot12ir.feishu.cn/drive/folder/{新文件夹token}`

5. **更新 `SKILL.md` 本身：**
   - 在「分类文件夹」表格中添加新分类（含关键词、文件夹 Token）
   - 保持表格持续扩展

## 飞书 API 配置

```python
app_id = "cli_a929129e4278dced"
app_secret = "usgK70hkHYBTQTtqMUFUMeXPPQDp35CE"

# 文件夹 token
root_folder = "U4p7fPrW1lmQzedgT9rcenKQnbh"
reading_folder = "C5NZflqNJlCK0EdaTQ2cmhVdnJg"

# 分类文件夹 token（从 reading_folder 子文件夹获取）
# 投资商业、AI科技、汽车新能源、家庭教育、其他
```

## 处理流程

### Step 0: 获取日期

**⚠️ 保存日期必须是用户实际分享链接的时间，不是文章内容中的日期！**

从用户消息的 timestamp 获取日期（格式如 "Sat 2026-03-28 02:06 GMT+8"），提取 YYYY-MM-DD 部分作为文件名前缀和元数据中的保存日期。

```python
# 用户消息 timestamp
user_timestamp = "Sat 2026-03-28 02:06 GMT+8"
date_prefix = "2026-03-28"  # 从 timestamp 提取

# 元数据中的 **保存日期** 也必须写这个日期，不能从文章内容中提取
```

### Step 1: 抓取原文

```bash
# 打开浏览器
openclaw browser open "链接?scene=1"
sleep 5

# 获取标题
openclaw browser evaluate --fn "() => document.querySelector('#activity-name')?.innerText?.trim() || ''"

# 获取原文
openclaw browser evaluate --fn "() => document.querySelector('#js_content')?.innerText || ''"

# 关闭标签
openclaw browser close
```

### Step 2: 清理换行符

微信公众号原文中 `\n` 是字面量字符串，需要替换：

```python
content = raw.replace('"', '')  # 去掉首尾引号
content = content.replace('\\n\\n\\n\\n\\n', '\n\n')
content = content.replace('\\n\\n', '\n\n')
content = content.replace('\\n', '\n')
paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
```

### Step 3: 合并短段落

公众号文章经常一句话一段，需要合并以提升可读性。**保留原文完整性，不删减内容**。

```python
merged = []
buffer = ""
for para in paragraphs:
    # 标题段落单独处理
    if is_title(para, original_titles):
        if buffer:
            merged.append(buffer)
            buffer = ""
        merged.append(para)
        continue
    if len(buffer) + len(para) < 280:
        buffer = (buffer + " " + para).strip() if buffer else para
    else:
        if buffer:
            merged.append(buffer)
        buffer = para
if buffer:
    merged.append(buffer)
```

### Step 4: 识别原文标题（关键步骤 ⚠️）

**原文中的段落标题是文章结构的核心，绝不能忽略或自创标题。**

#### 识别方法

1. **先收集所有短段落（<40字）**，作为疑似标题候选
2. **对比合并前后的段落**，找出哪些是原文的独立短段落
3. **标题通常有以下特征**：
   - 独立成段，前后有空行
   - 字数 < 40
   - 不以句号、逗号结尾
   - 包含行业/业务关键词（如"消耗战"、"转向"、"收缩"、"军备竞赛"、"巴别塔"等）

#### 识别流程

```python
# 第一步：在合并前，先收集所有短段落作为标题候选
title_candidates = [p for p in paragraphs if len(p) < 40]

# 第二步：对每个疑似标题，检查前后段落是否有空行分隔
for i, p in enumerate(paragraphs):
    if len(p) < 40:
        # 检查是否独立成段（前后是空行或内容段）
        if i > 0 and i < len(paragraphs) - 1:
            # 这是一个短段落，标记为标题
            标记为标题

# 第三步：合并时遇到标题就跳过，单独保留
for para in paragraphs:
    if para in original_titles:  # 标题不参与合并
        if buffer:
            merged.append(buffer)
            buffer = ""
        merged.append(para)  # 标题单独一段
        continue
    # 正常合并逻辑...
```

#### 常见标题模式（示例，每篇文章需根据实际内容调整）

投资类：收缩、省钱、转型、盈利、亏损、估值、现金流...
科技类：DeepSeek、豆包、元宝、补课、军备竞赛、博弈、入口...
汽车类：发布会、量产、智驾、增程、纯电、交付、开城...

**⚠️ 重要：不要自创标题，必须用原文的段落标题！**

### Step 5: 生成阅读总结

**⚠️ 必须真正阅读全文后总结，不能从开头截取！**

阅读总结分两部分：

```markdown
## 📝 阅读总结

### 核心观点
　　必须基于全文真正总结，不能从文章开头复制粘贴！
　　回答"这篇文章说了什么"、"核心论点是什么"、"作者想表达什么"。
　　长文章可按主题设小标题（如：字节策略、腾讯策略、人才战争等）
　　简短文章直接概括即可，不需要套格式。

### 金句
　　> 必须从全文中精选3-5句有洞察力、有冲击力的原句！
　　> 不能从文章开头截取，要从全文各个部分挑选最有价值的句子。
　　> 优先选择：有数据、有判断、有比喻、有观点的原句。
　　> 用引用格式 > 展示，每句单独一行。
```

### Step 6: 质量检查（必须执行，逐项核对）

- [ ] **核心观点是否真正总结** - 不能从文章开头复制粘贴！必须基于全文内容概括
- [ ] **金句是否有乱码** - 检查是否有 `\n` 或 `\n\n` 字面量残留，必须全部清理
- [ ] **金句是否从全文精选** - 不能只从开头截取，要从全文各部分挑选最有价值的句子
- [ ] **金句之间是否有空行** - 每条金句后必须有空行分隔（`。\n\n　　>`）
- [ ] **元数据字段之间是否有空行** - 来源、作者、链接等每个字段后必须有两个换行符
- [ ] **原文段落是否有缩进** - 原文全文的段落前必须用全角空格 `　　`，不能用普通空格
- [ ] **段落标题前没有缩进** - `## ` 开头的标题行前面不能有缩进
- [ ] 原文标题是否正确插入（用 `## ` 分隔）
- [ ] 是否有重复段落
- [ ] 来源、作者、关键词信息是否完整

### Step 7: 上传到飞书云盘

```python
# 1. 获取分类文件夹 token（从上方表格查，或新增分类时创建）
# 2. 检查分类文件夹是否存在，不存在则创建（参见「⚠️ 新增分类时必须同步飞书」）
# 3. 删除该文件夹下同名旧文件
# 4. 上传新文件

upload_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
```

### Step 8: 更新链接记录

更新 `~/.openclaw/workspace/reading-notes-links.md`，记录所有文章的飞书文档链接。

## 输出文件格式

```
~/.openclaw/workspace/saved/reading-notes/{分类}/{保存日期}-{文章标题}.md
```

飞书云盘路径：
```
个人笔记/阅读笔记/{分类}/{保存日期}-{文章标题}.md
```

**⚠️ 文件名必须带日期前缀**，格式为 `{日期}-{文章标题}.md`

**⚠️ 日期必须使用用户发送链接的时间（从消息 timestamp 获取），不是文章内容中的日期，也不是当前时间！**

示例：用户在 2026-03-28 00:44 发送链接，文件名应为：
- `2026-03-28-字节、阿里、腾讯 AI 大战全记录.md`

**原因：** 记录"用户什么时候分享的"，便于按日期做阅读统计和排序。

## 注意事项

1. 微信公众号链接必须加 `?scene=1` 参数
2. 浏览器抓取后必须 close tab
3. 原文段落合并时保留所有内容，不删减
4. **原文标题用短段落匹配，不要自创标题** ⚠️ 这是常见错误！
5. 段落缩进用全角空格 `　　`
6. 阅读总结分两部分：核心观点（概括文章论点）+ 金句（摘录3-5句原文精华）
7. **质量检查时必须确认原文标题是否正确插入**（用 `## ` 分隔）

## ⚠️ 格式规范（必须严格遵守）

### 元数据格式

每个元数据字段之间必须有**两个换行符**，确保正确显示：

```markdown
# 文章标题

**来源：** 微信公众号

**作者：** xxx

**原文链接：** https://mp.weixin.qq.com/s/xxx

**保存日期：** 2026-03-27

**关键词：** 关键词1、关键词2

---
```

**错误示例（不要这样）：**
```markdown
**来源：** 微信公众号
**作者：** xxx
**原文链接：** ...
```

**正确示例（必须这样）：**
```markdown
**来源：** 微信公众号

**作者：** xxx

**原文链接：** https://mp.weixin.qq.com/s/xxx
```

### 金句格式

金句之间必须有**空行分隔**，每条金句独立一行：

```markdown
### 金句

　　> 第一条金句，句子完整结束。

　　> 第二条金句，有洞察力、有判断。

　　> 第三条金句，有数据或有比喻。
```

**错误示例（不要这样）：**
```markdown
### 金句
　　> 第一条金句
　　> 第二条金句
　　> 第三条金句
```

**正确示例（必须这样）：**
```markdown
### 金句

　　> 第一条金句。

　　> 第二条金句。

　　> 第三条金句。
```

**实现方法：** 每条金句后加 `\n\n`，而不是 `\n`。

## 常见错误

### ❌ 错误：核心观点从开头截取
问题：直接复制文章开头内容作为核心观点，没有真正总结全文。
修复：必须阅读全文后用自己的话概括，不能复制原文开头。
示例（错误）："2025年11月，姚顺雨穿着休闲短裤、踩着拖鞋出现在腾讯的一场内部会上..."（这是原文开头，不是总结）
示例（正确）："这是一场AI时代的「中途岛战役」。字节豆包日活破亿、腾讯元宝借DeepSeek爆发、阿里千问三位一体投入4800亿。三巨头策略截然不同..."

### ❌ 错误：金句有乱码
问题：金句中包含 `\n` 或 `\n\n` 字面量，没有清理。
修复：生成金句前必须执行 `content.replace('\\n', ' ').replace('  ', ' ')` 清理所有转义符。

### ❌ 错误：金句从开头截取
问题：只从文章开头截取金句，没有从全文精选。
修复：必须阅读全文，从不同章节挑选最有洞察力、有数据、有判断的原句。

### ❌ 错误：忽略原文段落标题
问题：直接把所有内容合并成一段，丢失了文章的章节结构。
修复：先识别短段落作为标题候选，合并时跳过标题段落。

### ❌ 错误：自创标题
问题：用自己编的标题替代原文标题。
修复：必须使用原文中的段落标题，即使格式不完美。

### ❌ 错误：段落标题前加了缩进
问题：原文段落标题（如`## 01 某某标题`）前面被加了缩进`　　`，导致 Markdown 渲染时标题格式错误。
修复：段落标题（`## `开头的行）前面不要加缩进，保持`## 标题`的纯净格式。
示例（错误）：`　　## 01 AI有了"手"，企业先想到的是什么`
示例（正确）：`## 01 AI有了"手"，企业先想到的是什么`

### ❌ 错误：段落缩进用普通空格
问题：原文段落缩进用2个普通空格（`  `），Markdown 渲染时会被吞掉，导致没有缩进效果，易读性差。
修复：所有段落缩进必须用全角空格 `　　`，不能用普通空格。
示例（错误）：`  这是一段正文内容...`
示例（正确）：`　　这是一段正文内容...`

### ❌ 错误：原文全文段落没有缩进
问题：原文部分的段落没有首行缩进，导致阅读体验差。
修复：原文全文部分，除标题（`## `）和引用（`>`）外，每个段落前都要加全角空格 `　　`。

## 子代理完成通知

子代理完成任务后，必须通过飞书 API 直接推送消息给用户：

```python
import urllib.request, json

# 获取 token
app_id = "cli_a929129e4278dced"
app_secret = "usgK70hkHYBTQTtqMUFUMeXPPQDp35CE"
url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
req = urllib.request.Request(url, data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
    headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read()).get("tenant_access_token")

# 发送消息
open_id = "ou_b0d3821177d24497a82735dcf2ed7960"
msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
msg_body = json.dumps({
    "receive_id": open_id,
    "msg_type": "text",
    "content": json.dumps({"text": "✅ 任务完成：xxx"})
}).encode()
req_msg = urllib.request.Request(msg_url, data=msg_body,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(req_msg) as resp_msg:
    print(json.loads(resp_msg.read()))
```
