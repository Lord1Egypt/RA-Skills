# Article Archiver - 经验总结

## 2026-03-10 完整实现记录（更新）

### 核心挑战

1. **粗体格式丢失**：Playwright 的 `textContent` 只提取纯文本，丢失所有 HTML 格式
2. **长文档写入**：Twitter Article 内容很长（400+ 行），飞书 API 单次写入有限制
3. **图片同步**：需要下载图片并上传到飞书，然后插入到文档中

### 解决方案

#### 1. HTML 格式保留

创建新脚本 `html-to-markdown.js`，正确处理 HTML 格式：
- 检测 `style="font-weight: bold"` 属性
- 将粗体 span 转换为 Markdown `**粗体**`
- 保留代码块、列表等其他格式

**关键代码**：
```javascript
const style = node.getAttribute('style') || '';
const isBold = style.includes('font-weight: bold');
if (isBold && !inBold) {
  return `**${children}**`;
}
```

#### 2. 长文档分批写入

由于飞书 API 限制，需要分批写入：
1. 先 write 前 50 行
2. 然后分批 append 剩余内容（每批 50-100 行）
3. 总共需要 8-10 次 append 操作

**教训**：
- 一次性写入 400+ 行会失败
- 需要耐心分批追加
- 每次追加后验证是否成功

#### 3. 图片处理流程

保持不变，使用 `feishu_doc upload_image` 工具。

### 最终方案

1. 使用 `html-to-markdown.js` 提取格式化内容
2. 创建新文档
3. 分批写入所有内容（write + 多次 append）
4. 上传并插入图片
5. 验证完整性

### 最佳实践

1. **先准备，后写入**：不要边抓取边写入，先把所有内容准备好
2. **分批处理**：长文档分批写入（write + append）
3. **自我检查**：写入后立即读取验证
4. **保存中间结果**：图片 tokens、文章内容都保存到临时文件
5. **记录经验**：每次遇到问题都更新这个文档

### 工具链

```
Twitter URL
    ↓
Playwright + Cookie → 完整文本
    ↓
提取图片 URL
    ↓
下载图片 → 上传飞书 → image_key
    ↓
格式化 Markdown
    ↓
feishu_doc write (前 50 行)
    ↓
feishu_doc append (剩余内容)
    ↓
feishu_doc read (验证)
```

### 常见错误

1. **Cookie 过期**：定期更新 `config/twitter-cookies.txt`
2. **API 404**：使用 feishu_doc 工具而不是直接调用 API
3. **内容截断**：确保 Playwright 等待足够长时间（8 秒）
4. **格式混乱**：使用标准 Markdown 格式，代码块用三个反引号
5. **内容不完整**：抓取的内容可能被简化，需要对比原文确认完整性
   - 问题：Playwright 抓取的纯文本内容丢失了格式信息（粗体、斜体等）
   - 解决：需要从 HTML 中提取格式信息，保留 `<strong>`、`<em>` 等标签
6. **粗体格式丢失**：纯文本抓取会丢失所有格式
   - 原因：`textContent` 只提取纯文本，不保留 HTML 格式
   - 解决：需要解析 HTML 结构，将 `<strong>` 转换为 Markdown `**粗体**`

### 文件位置

- Cookie 配置：`config/twitter-cookies.txt`
- 抓取脚本：`scripts/fetch-twitter-article.js`
- 主归档脚本：`scripts/archive-article.js`
- 经验文档：`LESSONS.md`（本文件）

### 下次改进

1. 支持更多图片格式（PNG、GIF）
2. 自动检测 Cookie 是否过期
3. 支持批量归档多篇文章
4. 添加进度显示
5. 支持更多平台（Medium、知乎等）
6. **HTML 格式保留**：使用 Playwright 解析 HTML 并转换为 Markdown，保留粗体、代码块等格式
7. **长文档处理**：对于超长文档（400+ 行），需要分批写入飞书，每批 50-100 行

---

*最后更新：2026-03-10 20:00*
*作者：影*

---

## 2026-03-10 21:45 - 长文章归档问题（主动进化）

### 问题

归档包含大量图片的长文章时（如 662 行内容 + 24 张图片），内容不完整，图片丢失。

**具体表现**：
- 文章内容被截断，只有部分内容
- 24 张图片全部丢失
- 用户反馈"内容不对，明显不完整"

### 原因分析

1. **内容截断**：原有脚本没有正确处理超长内容（662 行）
2. **图片位置错误**：没有解析文章结构，无法确定图片应该插入的位置
3. **缺少分段策略**：一次性写入太多内容导致失败
4. **图片未下载**：虽然识别了图片 URL，但没有下载和上传

### 解决方案

创建专门的长文章归档脚本 `archive-long-article.js`：

**核心改进**：
1. **内容解析**：解析文章结构，识别图片标记位置（`![图像]`）
2. **分段写入**：将文章分成多个段落（文本段 + 图片段）
3. **顺序处理**：按顺序写入文本和上传图片，确保位置正确
4. **完整性保证**：每段独立处理，避免内容丢失
5. **图片下载**：自动下载所有图片到临时目录
6. **高清图片**：将图片 URL 替换为 900x900 高清版本

**使用方法**：
```bash
node scripts/archive-long-article.js <twitter_url>
```

**处理流程**：
1. 抓取文章内容（使用 fetch-twitter-article-formatted.js）
2. 提取所有图片 URL（正则匹配 pbs.twimg.com）
3. 下载所有图片到 /tmp/article_images/
4. 解析文章结构，确定图片插入位置
5. 创建飞书文档
6. 写入元数据（原始链接、归档时间、作者）
7. 逐段写入内容和上传图片
8. 输出文档 URL

**关键代码**：
```javascript
// 解析文章结构
function parseArticleContent(content) {
  const lines = content.split('\n');
  const segments = [];
  let currentSegment = [];
  let imageIndex = 1;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // 检测图片标记
    if (line.includes('![图像]') || line.includes('](http')) {
      // 保存当前文本段
      if (currentSegment.length > 0) {
        segments.push({ type: 'text', content: currentSegment.join('\n') });
        currentSegment = [];
      }
      
      // 添加图片段
      segments.push({ type: 'image', index: imageIndex++ });
    } else {
      currentSegment.push(line);
    }
  }
  
  return segments;
}
```

### 教训

**主动进化意识**：
- ✅ 遇到问题立即改进，不等用户催促
- ✅ 总结经验并更新文档
- ✅ 创建专门的工具解决特定问题
- ✅ 保证以后不会再犯同样的错误

**技术要点**：
- **完整性优先**：长文章必须分段处理，确保内容完整
- **图片位置重要**：图片必须插入到正确的位置，不能堆在末尾
- **自动化验证**：写入后自动验证内容是否完整
- **高清图片**：使用 900x900 版本，不要用 small 版本

**文件结构**：
```
skills/article-archiver/
├── scripts/
│   ├── fetch-twitter-article.js          # 基础抓取
│   ├── fetch-twitter-article-formatted.js # 格式化抓取
│   ├── archive-article.js                 # 通用归档
│   └── archive-long-article.js            # 长文章归档（新增）
├── config/
│   └── twitter-cookies.txt
├── SKILL.md
└── LESSONS.md
```

### 下次改进方向

1. **自动选择脚本**：根据文章长度和图片数量自动选择合适的归档脚本
2. **进度显示**：显示当前处理进度（X/Y 段已完成）
3. **错误重试**：网络错误时自动重试
4. **并发下载**：多张图片并发下载，提高速度
5. **内容验证**：归档完成后自动对比原文，确保完整性

---

*最后更新：2026-03-10 21:45*
*作者：影*
*进化周期：#0033*

---

## 2026-03-10 22:00 - 脚本调试完成

### 最终方案

经过多次迭代，找到了最可靠的方案：

**分离关注点**：
1. **Python 脚本**：负责创建文档、解析内容结构、准备段落文件
2. **feishu_doc 工具**：负责实际的内容写入和图片上传

**核心脚本**：
- `archive-simple.py` - 创建文档并解析内容结构
- `prepare-segments.py` - 将内容分割成独立的段落文件

**工作流程**：
```bash
# 1. 抓取文章内容
node scripts/fetch-twitter-article-formatted.js <url> <cookie> > article.json

# 2. 下载图片
mkdir images && cd images
cat ../article.json | jq -r '.content' | grep -o 'https://pbs.twimg.com/media/[^)]*' | while read url; do
  wget "${url}?format=jpg&name=900x900"
done

# 3. 创建文档并解析结构
python3 scripts/archive-simple.py article.json images/ <url>

# 4. 准备段落文件
python3 scripts/prepare-segments.py article.json /tmp/segments

# 5. 使用 feishu_doc 工具逐段写入
# (通过 AI 助手调用 feishu_doc 工具)
```

### 关键经验

1. **避免 CLI 转义问题**：不要通过 `openclaw` CLI 传递长文本，直接用工具
2. **分离职责**：Python 负责逻辑，工具负责 API 调用
3. **段落化处理**：将长文章分成小段落，每段独立处理
4. **清单管理**：用 manifest.json 记录所有段落的顺序和类型
5. **图片位置准确**：通过解析内容确定图片应该插入的位置

### 文件结构

```
skills/article-archiver/
├── scripts/
│   ├── fetch-twitter-article-formatted.js  # 抓取文章
│   ├── archive-simple.py                    # 创建文档
│   ├── prepare-segments.py                  # 准备段落
│   └── (废弃的尝试)
│       ├── archive-long-article.js
│       ├── archive-long-article.py
│       ├── archive-long-article-v2.py
│       ├── write-to-doc.py
│       └── upload-image.py
├── config/
│   └── twitter-cookies.txt
├── SKILL.md
└── LESSONS.md
```

### 测试结果

✅ **成功案例**：
- 文档创建：https://qingzhao.feishu.cn/wiki/UUlNwgXSriOGf4kD0RLcECSVnYo
- 内容解析：49 个段落（25 文字 + 24 图片）
- 段落文件：已准备在 /tmp/article_segments/

### 下一步

现在脚本已经调试好，可以开始归档文章了。使用 feishu_doc 工具按照 manifest.json 的顺序逐段写入内容和上传图片。

---

*最后更新：2026-03-10 22:00*
*作者：影*
*进化周期：#0033 - 脚本调试完成*
