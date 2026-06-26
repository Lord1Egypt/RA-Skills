---
name: article-archiver
description: Automatically archive web articles and Twitter Articles to Feishu documents. ALWAYS trigger when user shares URLs from x.com (Twitter), mp.weixin.qq.com (WeChat articles), or says "保存/记录/收藏 [链接]". Handles long articles (600+ lines), multiple images (20+ images), preserves formatting (bold, code blocks, lists), and sends success notification to user. Use immediately when detecting article URLs, don't ask for confirmation.
---

# Article Archiver

自动抓取网页文章和 Twitter Article，完整归档到飞书文档。

## ⚠️ 关键实现要点（必读）

**1. 必须读取配置文件获取归档位置**：
```bash
source ~/.openclaw/workspace/skills/article-archiver/config/feishu-locations.sh
# 使用 $DEFAULT_SPACE_ID 和 $DEFAULT_PARENT_NODE
```

**2. 图片处理流程**：
- 使用 `agent-browser` 打开页面
- 滚动加载所有图片（懒加载）
- 用 `img.preview` 或类似选择器过滤内容图片（排除头像、图标）
- 分析每张图片在文章中的位置（找到前面最近的段落文本）
- 下载图片到 `/tmp/`
- 使用 `feishu_doc upload_image` 并指定 `after_block_id` 插入到正确位置
- 关键：`upload_image` 支持 `after_block_id` 参数，可以精确控制图片位置

**3. 样式保留**：
- 引用块：使用 `>` 开头
- 粗体：使用 `**text**`
- 列表：使用 `-` 或 `1.`
- 代码块：使用 ` ``` `

**4. 内容传递方式**：
- 使用 OpenClaw 的 `read` 工具读取文件
- 不能在 feishu_doc 参数中使用 `$(cat file)`
- 大文件分批处理（每批 100 行）

**5. 去重检查**：
- 归档前先搜索同名文档
- 如果存在，返回已有文档链接
- 不要重复创建

**6. 防止乱码和格式问题**：
- **UTF-8 编码**：
  - 使用 `html-to-markdown-fixed.js`（而不是 `html-to-markdown-final.js`）
  - 该脚本使用 Buffer 确保 UTF-8 编码正确，避免中文字符被截断
  - 自动移除替换字符 `\ufffd` 和 `���`
- **标题格式修复**：
  - 脚本会自动修复 `# \n\n内容` 格式为 `# 内容`
  - 避免飞书渲染时标题为空、内容在下一行的问题
- **验证方法**：
  - 写入飞书前，检查 JSON 输出中是否有 `\ufffd` 或 `���`
  - 检查标题格式是否正确（标题标记和内容在同一行）
- **如果仍有问题**：
  - 不要手动重写原文内容，必须从原始来源精确提取
  - 长文本分段写入时，不要在多字节字符中间截断

**7. 避免重复标题**：
- 飞书文档已经有页面标题（Page title），不要在正文开头再写一次标题
- 从原文提取内容时，跳过第一个 H1 标题（通常就是文章标题）
- 如果 web_fetch 或 agent-browser 提取的内容以标题开头，删除第一行
- 正文应该从引言、摘要或第一段正文开始
- 元数据后直接接正文，不要插入标题

**8. 元数据格式（重要）**：
- **必须使用引用块格式**（灰色背景，有样式，好看）
- **标准格式**（参考 https://qingzhao.feishu.cn/wiki/ZVCFwN7bci1uyhknLpucA18FnSe）：
  ```markdown
  > **原始链接：** https://example.com/article
  > **归档时间：** 2026-03-12 22:16:00
  > **来源：** example.com
  > **作者：** 张三 (@username)
  
  ---
  ```
- **关键点**：
  - 每行以 `>` 开头（引用块）
  - 字段名用 `**粗体**` + 冒号
  - 字段值用普通文本
  - 元数据和正文之间用分隔线 `---` 分开
- **❌ 不要使用**：
  - Markdown 表格（会被渲染成飞书表格，不美观）
  - 普通文本（没有样式，不好看）
  - Emoji（📄、📅、✍️）在引用块中显示不好

**9. 图片位置精确控制**：
- 图片必须插入到正确的段落之后，不能随意放置
- 使用 `feishu_doc upload_image` 时，必须指定 `after_block_id`
- 步骤：
  1. 先写入全部正文内容
  2. 使用 `feishu_doc list_blocks` 获取所有 block_id
  3. 根据图片前面的文本内容，找到对应的 block_id
  4. 用 `after_block_id` 参数将图片插入到正确位置
- 不要在写入正文时就尝试插入图片（会导致位置错乱）

## 核心功能

- ✅ 支持长文章（600+ 行）
- ✅ 支持多图片（20+ 张），图片插入到正确位置
- ✅ 保留完整格式（粗体、代码块、列表）
- ✅ 按月份自动组织
- ✅ 自动去重（检测重复 URL）

## 使用方法

### 触发条件

**自动触发**（无需用户明确说"归档"）：
- 用户发送 Twitter/X 链接：`https://x.com/...` 或 `https://twitter.com/...`
- 用户发送微信公众号链接：`https://mp.weixin.qq.com/...`
- 用户说"保存 [链接]"、"记录 [链接]"、"收藏 [链接]"

**手动触发**：
- 用户明确说"归档这篇文章"、"保存到飞书"
- 用户发送其他网页链接并询问是否归档

**触发后的行为**：
1. 立即开始归档，不要询问确认
2. 归档过程中可以简短提示"正在归档..."
3. 归档成功后发送通知消息（包含文档链接）
4. 归档失败时说明原因，提供解决建议

### 归档流程

#### 0. 去重检查（必须先执行）

**在开始归档前，必须先检查文档是否已存在**：

```bash
# 1. 提取文章标题（使用修复版脚本）
TITLE=$(node scripts/html-to-markdown-fixed.js "$URL" "$(cat config/twitter-cookies.txt)" | jq -r '.title')

# 2. 在知识库中搜索同名文档
feishu_wiki nodes --space-id 7527734827164909572 --parent-node NqZvwBqMTiTEtkkMsRoc76rznce | \
  jq -r '.nodes[] | select(.title == "'"$TITLE"'") | .node_token'

# 3. 如果找到同名文档，跳过归档
if [ -n "$EXISTING_NODE" ]; then
  echo "⚠️ 文档已存在，跳过归档"
  echo "已存在的文档：https://qingzhao.feishu.cn/wiki/$EXISTING_NODE"
  exit 0
fi
```

**去重规则**：
- 标题完全一样 → 视为已存在
- 跳过归档，返回已存在文档的链接
- 不要重复创建相同标题的文档

**实现方式**：
1. 先提取文章标题（不需要完整内容）
2. 在目标位置搜索同名文档
3. 如果存在，直接返回链接并跳过
4. 如果不存在，继续正常归档流程

#### 1. 识别文章类型

```javascript
if (url.includes('x.com') && url.includes('/status/')) {
  // Twitter Article - 需要特殊处理
  return 'twitter-article';
} else {
  // 普通网页
  return 'web-page';
}
```

#### 2. 抓取内容

**Twitter Article**（长文章 + 多图片）：
```bash
# 使用修复版脚本（解决乱码和格式问题）
cd ~/.openclaw/workspace/skills/article-archiver
node scripts/html-to-markdown-fixed.js "$URL" "$(cat config/twitter-cookies.txt)" > /tmp/article.json
```

**普通网页**：
```bash
# 使用 web_fetch
web_fetch --url <url> --extract-mode markdown
```

#### 3. 分段写入（核心方法）

**⚠️ 重要：正确的文件内容传递方式**

在 OpenClaw 会话中，**不能使用 bash 命令替换 `$(cat file)` 直接传给 feishu_doc**，因为会被当成字面字符串。

**正确方法**：

**方法 1：使用 OpenClaw 的 read 工具**（推荐）
```javascript
// 1. 先用 read 工具读取文件
const content = await read({ path: '/tmp/content.txt' });

// 2. 然后传给 feishu_doc
await feishu_doc({
  action: 'append',
  doc_token: DOC_TOKEN,
  content: content
});
```

**方法 2：分批读取和上传**（适合大文件）
```javascript
// 读取文件总行数
const totalLines = parseInt(await exec({ 
  command: 'wc -l < /tmp/article-body.txt' 
}));

const BATCH_SIZE = 100;
let currentLine = 1;

while (currentLine <= totalLines) {
  const endLine = Math.min(currentLine + BATCH_SIZE - 1, totalLines);
  
  // 读取这批内容
  const content = await read({
    path: '/tmp/article-body.txt',
    offset: currentLine,
    limit: BATCH_SIZE
  });
  
  // 上传到飞书
  await feishu_doc({
    action: 'append',
    doc_token: DOC_TOKEN,
    content: content
  });
  
  currentLine = endLine + 1;
  
  // 延迟，避免 API 限流
  await new Promise(resolve => setTimeout(resolve, 300));
}
```

**图片处理**（关键步骤）：
```bash
# 1. 使用 agent-browser 打开页面并提取图片
agent-browser open "https://example.com/article"
sleep 3

# 2. 滚动页面加载所有图片（懒加载）
agent-browser scroll down 5000
sleep 2
agent-browser scroll down 5000
sleep 2

# 3. 提取图片 URL（过滤头像和 SVG）
agent-browser eval 'JSON.stringify(
  Array.from(document.querySelectorAll("img"))
    .filter(img => !img.src.startsWith("data:") && 
                   !img.src.includes("avatar") && 
                   img.naturalWidth > 300)
    .map(img => img.src)
)' > /tmp/image-urls.json

# 4. 下载并上传每张图片
cat /tmp/image-urls.json | jq -r '.[]' | while read url; do
  curl -s -o /tmp/img.jpg "$url"
  # 使用 feishu_doc upload_image 上传
  # 注意：必须用 file_path 参数，不是 path
done

# 5. 关闭浏览器
agent-browser close
```

**图片上传注意事项**：
- 使用 `feishu_doc` 的 `upload_image` action
- 参数名是 `file_path`，不是 `path`
- 每次上传后延迟 300ms 避免限流
- 图片会自动插入到文档末尾

**样式保留**：
- 使用 Markdown 格式保留样式
- 引用块：使用 `>` 开头
- 代码块：使用 ` ``` ` 包裹
- 列表：使用 `-` 或 `1.` 开头
- 粗体：使用 `**text**`

**关键原则**：
- 必须先读取文件内容到变量
- 然后把变量传给 feishu_doc
- 不能在 feishu_doc 参数中使用 bash 命令替换
- 大文件分批处理（每批 100 ���）
- 分批之间延迟 0.3 秒
- 图片单独上传，不要嵌入 Markdown

#### 4. 添加元数据头部

**标准格式**（引用块 + 粗体字段名，参考 https://qingzhao.feishu.cn/wiki/ZVCFwN7bci1uyhknLpucA18FnSe）：

```javascript
// 提取元数据
const metadata = JSON.parse(await exec({ 
  command: 'cat /tmp/article.json' 
}));

const title = metadata.title;
const author = metadata.author;
const username = metadata.username;
const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');

// 判断来源
let source, authorText;
if (url.includes('x.com') || url.includes('twitter.com')) {
  source = 'x.com (Twitter Article)';
  authorText = `${author} (@${username})`;
} else if (url.includes('mp.weixin.qq.com')) {
  source = '微信公众号';
  authorText = author;
} else {
  source = url.match(/https?:\/\/([^/]+)/)[1];
  authorText = author;
}

// 写入元数据头部（引用块格式）
await feishu_doc({
  action: 'append',
  doc_token: DOC_TOKEN,
  content: `> **原始链接：** ${url}
> **归档时间：** ${timestamp}
> **来源：** ${source}
> **作者：** ${authorText}

---`
});
```

**关键点**：
- 每行以 `>` 开头（引用块）
- 字段名用 `**粗体**` + 冒号
- 字段值用普通文本
- 不要用 Emoji（📄、📅、✍️）
- 元数据和正文之间用分隔线 `---` 分开

#### 5. 写入正文内容

**使用 OpenClaw read 工具读取并写入**：

```javascript
// 读取正文内容
const content = await read({ path: '/tmp/article.json' });
const articleContent = JSON.parse(content).content;

// 写入正文
await feishu_doc({
  action: 'append',
  doc_token: DOC_TOKEN,
  content: articleContent
});
```

**飞书会自动处理**：
- Markdown 图片语法 `![alt](url)` → 自动下载并转换为内部图片
- 代码块 ` ```language ... ``` ` → 渲染为代码块
- 粗体、列表、标题等 → 正确渲染

#### 6. 验证完整性

```bash
# 读取文档，检查块数
feishu_doc read --doc_token $DOC_TOKEN

# 验证：
# - 文字段落数 = 预期段落数
# - 图片数 = 预期图片数
# - 总块数 = 文字段落数 + 图片数
```

#### 7. 发送成功通知

**成功消息格式**：
```
✅ 文章已归档到飞书

📄 标题：[文章标题]
🔗 原文：[原始链接]
📁 位置：学习资料抓取 → 待阅读
🔗 飞书：[飞书文档链接]

📊 统计：
- 内容：[行数] 行
- 图片：[数量] 张
- 格式：完整保留
```

**失败消息格式**：
```
❌ 归档失败

原因：[失败原因]
建议：[解决建议]

原文链接：[原始链接]
```

**使用 message 工具发送**：
```javascript
// 成功通知
message({
  action: "send",
  target: "ou_a39e6975059f975a7ffd25892243b64a",  // 威哥的 user_id
  message: "✅ 文章已归档到飞书\n\n📄 标题：...\n🔗 飞书：..."
});

// 失败通知
message({
  action: "send",
  target: "ou_a39e6975059f975a7ffd25892243b64a",
  message: "❌ 归档失败\n\n原因：...\n建议：..."
});
```

## 配置

### 飞书归档位置

**配置文件**：`config/feishu-locations.sh`

```bash
# 默认归档位置
DEFAULT_SPACE_ID="7527734827164909572"
DEFAULT_PARENT_NODE="YziUwLVlBi9BX7kVtkJcf7nQns2"  # 学习资料抓取 → 待阅读

# 可选的归档位置
LOCATION_TO_READ="7527734827164909572:YziUwLVlBi9BX7kVtkJcf7nQns2"  # 待阅读
LOCATION_ROOT="7527734827164909572:Lfj1d3Pcmo0o2IxrHrOcMsffnZb"      # 根目录
```

**使用方法**：

1. **修改默认位置**：
   ```bash
   # 编辑配置文件
   vim ~/.openclaw/workspace/skills/article-archiver/config/feishu-locations.sh
   
   # 修改 DEFAULT_PARENT_NODE 为目标 node_token
   DEFAULT_PARENT_NODE="YziUwLVlBi9BX7kVtkJcf7nQns2"
   ```

2. **临时指定位置**（调用时传参）：
   ```bash
   # 归档到指定节点
   feishu_wiki create --parent-node <node_token> --title "文章标题"
   ```

3. **添加新位置**：
   ```bash
   # 在配置文件中添加
   LOCATION_ARCHIVE="7527734827164909572:XXX"  # 归档目录
   LOCATION_DRAFT="7527734827164909572:YYY"    # 草稿目录
   ```

**获取 node_token**：
```bash
# 方法 1：从飞书 URL 中提取
# https://qingzhao.feishu.cn/wiki/YziUwLVlBi9BX7kVtkJcf7nQns2
# node_token = YziUwLVlBi9BX7kVtkJcf7nQns2

# 方法 2：使用 feishu_wiki 工具查询
feishu_wiki nodes --space-id 7527734827164909572
```

**当前配置的位置**：
- **待阅读**（默认）：`YziUwLVlBi9BX7kVtkJcf7nQns2`
  - 路径：学习资料抓取 → 待阅读
  - 用途：新归档的文章默认放这里
- **根目录**：`Lfj1d3Pcmo0o2IxrHrOcMsffnZb`
  - 路径：学习资料抓取
  - 用途：直接归档到根目录

### Twitter Cookie

Twitter Article 需要登录 Cookie：

```bash
# Cookie 文件位置
~/.openclaw/workspace/skills/article-archiver/config/twitter-cookies.txt

# 格式
auth_token=xxx; ct0=yyy; twid=zzz

# 更新 Cookie
echo "auth_token=xxx; ct0=yyy; twid=zzz" > config/twitter-cookies.txt
```

### 文档格式

```markdown
# 学习资料抓取

# 2026-03

## 文章标题

> **原始链接**：https://example.com/article
> 
> **归档时间**：2026-03-11 20:00:00
> 
> **来源**：example.com
> 
> **作者**：作者名 (@username)

文章内容...

![图片1](image_url)

更多内容...

![图片2](image_url)

---
```

## 支持的平台

### Twitter / X

**URL 格式**：
- `https://x.com/username/status/123456789`
- `https://twitter.com/username/status/123456789`

**特点**：
- 支持长文章（Twitter Article）
- 支持多图片（20+ 张）
- 需要 Cookie 认证

### 微信公众号

**URL 格式**：
- `https://mp.weixin.qq.com/s/...`

**特点**：
- 支持富文本格式
- 支持图片
- 无需认证

### 普通网页

**支持的网站**：
- 技术博客（Medium、Dev.to、掘金等）
- 新闻网站
- 个人博客

**特点**：
- 使用 `web_fetch` 抓取
- 自动提取正文
- 保留基本格式

## 使用示例

### 示例 1：Twitter 链接（自动触发）

**用户**：https://x.com/mkdir700/status/2020652753190887566

**系统行为**：
1. 检测到 Twitter 链接，自动触发归档
2. **检查去重**：在知识库中搜索同名文档
3. 如果不存在，继续归档流程
4. 提示："正在归档..."
5. 抓取完整内容（672 行 + 24 张图片）
6. 归档到飞书（学习资料抓取 → 待阅读）
7. 发送成功通知：
   ```
   ✅ 文章已归档到飞书
   
   📄 标题：月成本不到 100 元，如何实现 Token 自由
   🔗 原文：https://x.com/mkdir700/status/2020652753190887566
   📁 位置：学习资料抓取 → 待阅读
   🔗 飞书：https://qingzhao.feishu.cn/wiki/XXX
   
   📊 统计：
   - 内容：672 行
   - 图片：24 张
   - 格式：完整保留
   ```

### 示例 2：重复文档（自动跳过）

**用户**：https://x.com/mkdir700/status/2020652753190887566

**系统行为**：
1. 检测到 Twitter 链接，自动触发归档
2. **检查去重**：发现同名文档已存在
3. 跳过归档，返回已存在文档的链接
4. 发送通知：
   ```
   ⚠️ 文档已存在，跳过归档
   
   📄 标题：月成本不到 100 元，如何实现 Token 自由
   🔗 已存在的文档：https://qingzhao.feishu.cn/wiki/XXX
   ```

### 示例 2：微信公众号（自动触发）

**用户**：https://mp.weixin.qq.com/s/abc123

**系统行为**：
1. 检测到微信公众号链接，自动触发归档
2. 抓取文章内容
3. 归档到飞书
4. 发送成功通知

### 示例 3：手动触发

**用户**：保存 https://example.com/article

**系统行为**：
1. 检测到"保存"关键词 + 链接
2. 自动触发归档
3. 归档成功后发送通知

### 示例 4：归档失败

**用户**：https://x.com/someuser/status/123（Cookie 过期）

**系统行为**：
1. 尝试抓取，发现 Cookie 过期
2. 发送失败通知：
   ```
   ❌ 归档失败
   
   原因：Twitter Cookie 已过期
   建议：
   1. 浏览器登录 x.com
   2. 复制 Cookie（auth_token, ct0, twid）
   3. 更新配置文件：config/twitter-cookies.txt
   
   原文链接：https://x.com/someuser/status/123
   ```

## 脚本工具

### html-to-markdown-fixed.js（推荐使用）

从 Twitter Article HTML 转换为格式化 Markdown，修复了 UTF-8 乱码和标题格式问题：

```bash
node scripts/html-to-markdown-fixed.js <article_url> <cookie_string>
```

**功能**：
- ✅ 修复 UTF-8 编码问题（使用 Buffer 确保中文字符不被截断）
- ✅ 修复标题格式问题（`# \n\n内容` → `# 内容`）
- ✅ 自动移除替换字符 `\ufffd` 和 `���`
- ✅ 保留粗体（`**text**`）
- ✅ 保留代码块（` ```shell ... ``` `）
- ✅ 保留列表（`- item`）
- ✅ 提取图片 URL

**与旧版本的区别**：
- `html-to-markdown-final.js`：旧版本，存在乱码和格式问题
- `html-to-markdown-fixed.js`：新版本，已修复所有已知问题

### archive-long-article.sh

处理长文章（600+ 行）+ 多图片（20+ 张）：

```bash
cd ~/.openclaw/workspace/skills/article-archiver/scripts
./archive-long-article.sh <article_url> <doc_token>
```

**功能**：
1. 抓取完整内容（使用 html-to-markdown-fixed.js）
2. 提取图片 URL
3. 按图片位置分段
4. 生成段落清单（manifest.json）
5. 输出 feishu_doc 命令（需要在 OpenClaw 环境执行）

## 常见问题

### Q1: 中文出现乱码（���）？

**原因**：UTF-8 多字节字符在传输或序列化时被截断。

**解决**：
- 使用 `html-to-markdown-fixed.js` 而不是 `html-to-markdown-final.js`
- 该脚本使用 Buffer 确保 UTF-8 编码正确
- 自动移除替换字符

### Q2: 标题为空，内容在下一行？

**原因**：Markdown 格式 `# \n\n内容` 导致飞书渲染时标题为空。

**解决**：
- 使用 `html-to-markdown-fixed.js`
- 脚本会自动修复标题格式为 `# 内容`

### Q3: 图片位置不对，都堆在文档末尾？

**原因**：先写完所有文字，再统一上传图片。

**解决**：按图片位置分段，交替写入文本和图片。

### Q4: 内容不完整，只有开头部分？

**原因**：长文章一次性写入失败。

**解决**：使用 `archive-long-article.sh` 脚本，分段处理。

### Q5: 格式丢失（粗体、代码块）？

**原因**：使用了简单的文本提取，没有保留 HTML 格式。

**解决**：使用 `html-to-markdown.js` 脚本，正确转换格式。

### Q4: 执行慢、消耗大量 token？

**原因**：手动逐个调用 `feishu_doc` 工具。

**解决**：用 bash 脚本批量处理，脚本执行不消耗 token。

### Q5: Cookie 过期怎么办？

**症状**：抓取 Twitter Article 失败，返回登录页面。

**解决**：
1. 浏览器登录 x.com
2. 打开开发者工具 → Application → Cookies
3. 复制 `auth_token`, `ct0`, `twid`
4. 更新 `config/twitter-cookies.txt`

## 成功案例

### 案例 1：mkdir700 长文章

- **URL**：https://x.com/mkdir700/status/2020652753190887566
- **标题**：月成本不到 100 元，如何实现 Token 自由
- **内容**：672 行
- **图片**：24 张
- **结果**：✅ 完整归档，图片位置正确，格式完整
- **文档**：https://qingzhao.feishu.cn/docx/NZHpd5xHxoTjYPxlVfpcaKtOnvh

### 案例 2：暂星的文章

- **URL**：https://x.com/lumoswhy/status/2030807300257300613
- **内容**：451 行
- **图片**：5 张
- **结果**：✅ 完整归档，格式正确

## 注意事项

1. **版权**：仅用于个人学习和归档
2. **去重**：同一 URL 不重复归档
3. **错误处理**：抓取失败时提示用户，记录日志
4. **API 限流**：每次操作间隔 0.3 秒
5. **Cookie 管理**：定期检查 Twitter Cookie 是否过期

## 改进历史

- **2026-03-10**：初始版本，支持基本归档
- **2026-03-11**：重大改进
  - 支持长文章（600+ 行）
  - 支持多图片（20+ 张）
  - 图片位置正确（分段写入 + 交替插入）
  - 格式完整保留（粗体、代码块、列表）
  - 添加 `archive-long-article.sh` 脚本
  - 添加完整性验证
  - 添加飞书归档位置配置（支持灵活修改目标位置）
  - **添加自动触发机制**（检测 Twitter/微信公众号链接）
  - **添加成功/失败通知**（自动推送消息给用户）
  - **支持微信公众号**（mp.weixin.qq.com）

---

*最后更新：2026-03-11 20:55*
*维护者：影*

## 最新改进（2026-03-11）

### 使用 turndown 库

article-archiver 现在使用业界标准的 **turndown** 库进行 HTML 到 Markdown 的转换，确保高质量的格式保留。

**核心脚本**：`scripts/html-to-markdown-final.js`

**关键特性**：
1. ✅ **代码块支持**：正确识别 `<pre>/<code>` 标签，保留语言标注（bash、json、yaml、text 等）
2. ✅ **图片支持**：保留 Markdown 图片语法 `![alt](url)`，飞书会自动下载并转换
3. ✅ **格式保留**：粗体、列表、标题、引用块、链接等全部正确转换
4. ✅ **GFM 扩展**：支持 GitHub Flavored Markdown（表格、删除线等）

**技术栈**：
- **Playwright**：无头浏览器，处理动态加载的内容
- **turndown**：HTML 转 Markdown（8.8k GitHub stars）
- **turndown-plugin-gfm**：GFM 扩展支持

**代码块处理**：
```javascript
// 自定义代码块规则：保留语言标注
turndownService.addRule('codeBlock', {
  filter: function (node) {
    return node.nodeName === 'PRE' && node.querySelector('code');
  },
  replacement: function (content, node) {
    const code = node.querySelector('code');
    const language = code.className.replace('language-', '') || '';
    const text = code.textContent;
    return '\n\n```' + language + '\n' + text + '\n```\n\n';
  }
});
```

**图片处理**：
- turndown 默认将 `<img>` 转换为 `![alt](url)` 格式
- 飞书 Markdown 解析器会自动下载外链图片并转换为内部图片
- 无需手动上传图片，速度快，不会超时

**元数据头部**：
```markdown
> **原始链接：** https://x.com/username/status/123456789
> **归档时间：** 2026-03-11 22:50:00
> **来源：** x.com (Twitter Article)
> **作者：** 作者名 (@username)

---
```

### 归档质量

**测试案例**：mkdir700 的 sub2api 教程
- 原文：https://x.com/mkdir700/status/2020652753190887566
- 归档结果：
  - ✅ 代码块：16 个（bash、json、yaml、text）
  - ✅ 图片：24 张（全部自动转换）
  - ✅ 总块数：229 个
  - ✅ 格式：完整保留

**性能**：
- 提取时间：~10 秒
- 上传时间：~3 分钟（包括图片自动下载）
- 总耗时：~4 分钟

### 故障排查

**问题 1：代码块丢失**
- **原因**：turndown 默认规则无法识别某些代码块结构
- **解决**：添加自定义 `codeBlock` 规则，显式处理 `<pre>/<code>` 标签

**问题 2：图片丢失**
- **原因**：自定义规则移除了图片
- **解决**：移除 `removeImages` 规则，让 turndown 保留图片的 Markdown 语法

**问题 3：图片位置不对**
- **原因**：先收集所有图片，然后按顺序插入，无法保证位置准确
- **解决**：使用 turndown 的默认行为，在遍历 DOM 时即时转换图片

**问题 4：Cookie 过期**
- **症状**：无法访问 Twitter Article，返回登录页面
- **解决**：更新 `config/twitter-cookies.txt` 文件

### 依赖安装

```bash
cd ~/.openclaw/workspace/skills/article-archiver
npm install turndown turndown-plugin-gfm playwright
```

### 使用最新脚本

```bash
# 提取文章（包含代码块和图片）
node scripts/html-to-markdown-final.js \
  "https://x.com/username/status/123456789" \
  "$(cat config/twitter-cookies.txt)" \
  > /tmp/article.json

# 检查提取结果
jq '.content' /tmp/article.json | head -50

# 统计代码块和图片
echo "代码块: $(jq -r '.content' /tmp/article.json | grep -c '```')"
echo "图片: $(jq -r '.content' /tmp/article.json | grep -c '!\[')"
```

### 未来改进

- [ ] 支持更多平台（Medium、知乎、微信公众号）
- [ ] 自动检测重复 URL
- [ ] 支持批量归档
- [ ] 添加标签和分类
- [ ] 支持全文搜索

## 已知限制和解决方案（2026-03-12）

### 1. 飞书嵌入文档无法抓取

**问题**：
- 某些网站（如火山引擎开发者社区）的文章是嵌入的飞书文档
- 页面显示"暂时无法在飞书文档外展示此内容"
- 无法通过普通网页抓取获取内容和图片

**识别方法**：
```javascript
// 检查是否为飞书嵌入文档
const firstParagraph = document.querySelector('article p')?.textContent;
if (firstParagraph?.includes('暂时无法在飞书文档外展示此内容')) {
  // 这是飞书嵌入文档，无法抓取
}
```

**解决方案**：
- **跳过归档**：这类文章本身就在飞书里，不需要重新归档
- **提示用户**：告知用户这是飞书文档，提供原始飞书链接
- **示例**：https://developer.volcengine.com/articles/7615547765435432996
  - 实际内容在：https://qingzhao.feishu.cn/wiki/ZVCFwN7bci1uyhknLpucA18FnSe

### 2. 嵌套代码块问题

**问题**：
- 当原文包含 markdown 代码块（教程类文章），飞书的 Markdown 解析器无法正确处理嵌套的代码块
- 例如：markdown 代码块中包含 markdown 代码示例

**表现**：
- 代码块内容会跑到外面，变成普通文本
- 格式混乱

**解决方案**：
- 目前无完美解决方案（飞书 Markdown 解析器限制）
- 内容完整，但格式可能不完美
- 建议：接受当前格式，或在飞书中手动调整

### 2. 嵌套代码块问题

**问题**：
- 某些 Twitter 图片链接格式特殊，飞书无法自动转换
- 例如：`https://pbs.twimg.com/media/...?format=jpg&name=small`

**解决方案**：
1. **方案 A**（推荐）：使用 turndown 提取的 Markdown，一次性写入，飞书自动处理
   - 优点：快速、简单
   - 缺点：某些特殊格式图片可能无法转换

2. **方案 B**：手动下载并上传图片
   - 下载图片到本地
   - 使用 `feishu_doc upload_image` 逐个上传
   - 优点：图片一定能显示
   - 缺点：慢、复杂

3. **方案 C**：分段写入（文本 → 图片 → 文本）
   - 按原文顺序交替写入文本和图片
   - 优点：图片位置准确
   - 缺点：最慢、最复杂

**推荐流程**：
1. 先尝试方案 A（一次性写入）
2. 如果图片无法显示，再使用方案 B（手动上传）

### 3. Twitter 图片处理

**重要规则**：
- ❌ 不要在云空间根目录创建文档（用户看不到，没有操作权限）
- ✅ 必须在知识库中创建文档（使用 `feishu_wiki create`）
- ✅ 默认位置：`NqZvwBqMTiTEtkkMsRoc76rznce`（学习资料抓取 → 待阅读）

**正确的创建方式**：
```bash
feishu_wiki create \
  --space-id 7527734827164909572 \
  --parent-node NqZvwBqMTiTEtkkMsRoc76rznce \
  --title "$TITLE" \
  --obj-type docx
```

### 4. 归档位置

**功能**：
- 在归档前检查是否已存在同名文档
- 标题完全一样 → 视为已存在
- 跳过归档，返回已存在文档的链接

**使用方法**：
```bash
# 检查去重
RESULT=$(bash scripts/check-duplicate.sh "$URL")

# 解析结果
if [[ $RESULT == EXISTS:* ]]; then
  NODE_TOKEN=$(echo "$RESULT" | cut -d: -f2)
  TITLE=$(echo "$RESULT" | cut -d: -f3)
  echo "⚠️ 文档已存在：https://qingzhao.feishu.cn/wiki/$NODE_TOKEN"
  exit 0
fi
```

**脚本位置**：`scripts/check-duplicate.sh`

## 最佳实践总结

### 归档流程（推荐）

1. **去重检查**：
```bash
bash scripts/check-duplicate.sh "$URL"
```

2. **提取文章**：
```bash
node scripts/html-to-markdown-final.js "$URL" "$(cat config/twitter-cookies.txt)" > /tmp/article.json
```

3. **创建文档**（知识库）：
```bash
TITLE=$(jq -r '.title' /tmp/article.json)
feishu_wiki create --space-id 7527734827164909572 --parent-node NqZvwBqMTiTEtkkMsRoc76rznce --title "$TITLE" --obj-type docx
```

4. **添加元数据头部**（引用块格式）：
```javascript
// 提取元数据
const metadata = JSON.parse(await exec({ command: 'cat /tmp/article.json' }));
const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');

// 判断来源
let source, authorText;
if (url.includes('x.com') || url.includes('twitter.com')) {
  source = 'x.com (Twitter Article)';
  authorText = `${metadata.author} (@${metadata.username})`;
} else if (url.includes('mp.weixin.qq.com')) {
  source = '微信公众号';
  authorText = metadata.author;
} else {
  source = url.match(/https?:\/\/([^/]+)/)[1];
  authorText = metadata.author;
}

// 写入元数据头部
await feishu_doc({
  action: 'append',
  doc_token: DOC_TOKEN,
  content: `> **原始链接：** ${url}
> **归档时间：** ${timestamp}
> **来源：** ${source}
> **作者：** ${authorText}

---`
});
```

5. **写入正文内容**：
```javascript
// 读取正文内容
const content = await read({ path: '/tmp/article.json' });
const articleContent = JSON.parse(content).content;

// 写入正文
await feishu_doc({
  action: 'append',
  doc_token: DOC_TOKEN,
  content: articleContent
});
```

6. **验证结果**：
```bash
feishu_doc list_blocks --doc_token $DOC_TOKEN | jq '.blocks | length'
```

### 故障排查

**问题 1：图片无法显示**
- 检查图片 URL 格式
- 尝试手动下载并上传

**问题 2：代码块格式错误**
- 检查是否有嵌套代码块
- 接受当前格式，或手动调整

**问题 3：文档创建在错误位置**
- 检查是否使用 `feishu_wiki create`
- 检查 `parent_node` 参数

**问题 4：重复归档**
- 使用去重检查脚本
- 检查标题是否完全一致

**问题 5：元数据头部没有样式**
- **症状**：元数据头部是普通文本，没有灰色背景
- **原因**：没有使用引用块格式
- **解决**：
  - 每行以 `>` 开头（引用块）
  - 字段名用 `**粗体**` + 冒号
  - 参考正确格式：https://qingzhao.feishu.cn/wiki/ZVCFwN7bci1uyhknLpucA18FnSe
  - 不要用 Emoji（📄、📅、✍️）
  - 不要用 Markdown 表格

**问题 6：内容写入错误（显示命令而非内容）**
- **症状**：文档中显示 `$(cat /tmp/file.md)` 而不是实际内容
- **原因**：在 OpenClaw 中使用了 bash 命令替换，不会被执行
- **解决**：
  - ❌ 错误：`feishu_doc append --content "$(cat file.md)"`
  - ✅ 正确：先用 `read` 工具读取文件，再传递内容
  ```javascript
  const content = await read({ path: '/tmp/file.md' });
  await feishu_doc({ action: 'append', content: content });
  ```

**问题 7：UTF-8 乱码（字符被截断）**
- **症状**：`那么��读和自媒体`（"阅"字显示为 `��`）
- **原因**：多字节 UTF-8 字符在传输或分段时被截断
- **解决**：
  - 确保完整的字符串传递，不要在字符中间截断
  - 使用 OpenClaw 的 `read` 工具读取文件（自动处理编码）
  - 避免使用 bash 命令的字符串截取（如 `head -c`）

**问题 8：归档位置错误**
- **症状**：文档创建在错误的知识库位置
- **原因**：使用了错误的 `parent_node_token`
- **解决**：
  - 检查配置文件：`config/feishu-locations.sh`
  - 确认 `DEFAULT_PARENT_NODE` 的值
  - 正确位置：`NqZvwBqMTiTEtkkMsRoc76rznce`（学习资料抓取 → 待阅读）
  - 错误位置：`YziUwLVlBi9BX7kVtkJcf7nQns2`（旧位置）

