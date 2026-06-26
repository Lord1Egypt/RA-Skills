# 搜索平台指南

## ⚠️ 重要说明：搜索工具使用

### 必须使用 browser 工具
- **唯一搜索工具**: `browser` 工具 + Bing 搜索引擎
- **禁止使用**: `web_search` 工具（API 依赖、功能受限）
- **原因**: browser 工具支持完整页面渲染、JavaScript 执行，可以访问需要登录或动态加载的内容

### 搜索执行流程
1. 打开浏览器：`browser(action=open, targetUrl="https://www.bing.com/search?q=[查询]")`
2. 构造搜索查询：
   - 通用搜索：`[关键词]`
   - 限定平台：`site:example.com [关键词]`
   - 学术搜索：`"[关键词]"` (Google Scholar)
3. 页面快照：`browser(action=snapshot)` 获取页面内容
4. 提取信息：从快照中提取标题、内容、日期等信息
5. 批量访问：对多个搜索结果重复上述步骤

### 注意事项
- 每次搜索后等待页面完全加载
- 对于需要登录的网站，记录访问限制
- 自动识别并跳过广告和 SEO 垃圾页面
- 优先选择高信誉域名（.edu, .gov, 权威媒体）

---

## 国际新闻平台

### Google News
- URL: https://news.google.com
- 适用场景：国际突发新闻、全球视角
- 搜索技巧：使用英文关键词，按时间排序

### BBC News
- URL: https://www.bbc.com/news
- 适用场景：国际政治、欧洲视角
- 搜索技巧：使用 site:bbc.com/news [关键词]

### CNN
- URL: https://www.cnn.com
- 适用场景：美国视角、全球商业新闻
- 搜索技巧：区分 CNN Business, CNN Politics 等子站点

### Reuters
- URL: https://www.reuters.com
- 适用场景：权威财经新闻、事实核查
- 搜索技巧：Reuters 内容可信度高，适合作为交叉验证源

### TechCrunch
- URL: https://techcrunch.com
- 适用场景：科技创业、互联网行业
- 搜索技巧：关注 Startup, AI, Enterprise 等栏目

## 国内权威媒体

### 新华社
- URL: https://www.xinhuanet.com
- 适用场景：官方消息、政策解读
- 搜索技巧：使用 site:xinhuanet.com [关键词]

### 人民日报
- URL: https://www.people.com.cn
- 适用场景：官方立场、重大事件
- 搜索技巧：关注评论员文章获取官方观点

### 财新网
- URL: https://www.caixin.com
- 适用场景：财经深度报道、商业分析
- 搜索技巧：部分内容需订阅，但摘要可公开访问

### 澎湃新闻
- URL: https://www.thepaper.cn
- 适用场景：国内社会新闻、调查报道
- 搜索技巧："思想"栏目提供深度分析

### 36Kr
- URL: https://www.36kr.com
- 适用场景：科技创业、互联网行业
- 搜索技巧：关注"创投"、"科技"栏目

## 社交媒体平台

### Bilibili (B 站)
- URL: https://www.bilibili.com
- 适用场景：视频深度解说、UP 主观点
- 搜索技巧：
  - site:bilibili.com [关键词]
  - 筛选"最多点击"获取高质量内容
  - 关注专业领域 UP 主（科技、财经、学术类）

### 抖音/TikTok
- URL: https://www.douyin.com
- 适用场景：热门话题、短视频趋势
- 搜索技巧：
  - site:douyin.com [关键词]
  - 关注话题标签（#）
  - 注意时效性强但深度有限

### 小红书
- URL: https://www.xiaohongshu.com
- 适用场景：用户体验、真实反馈、种草/避雷
- 搜索技巧：
  - site:xiaohongshu.com [关键词]
  - 筛选"最新"获取实时反馈
  - 关注"测评"、"体验"类笔记

## 学术文献平台

### Google Scholar
- URL: https://scholar.google.com
- 适用场景：学术论文、研究综述
- 搜索技巧：
  - 使用英文关键词
  - 按引用次数排序获取经典文献
  - 关注近 3-5 年的研究

### arXiv
- URL: https://arxiv.org
- 适用场景：计算机科学、人工智能、物理
- 搜索技巧：
  - 筛选特定领域（cs.AI, cs.CL 等）
  - 关注最新上传论文
  - 注意预印本性质，未经同行评审

### CNKI (中国知网)
- URL: https://www.cnki.net
- 适用场景：中文学术论文
- 搜索技巧：需要机构账号访问，但摘要可公开查看

## 搜索引擎技巧

### 通用搜索语法
- `site:example.com [关键词]` - 限定域名搜索
- `filetype:pdf [关键词]` - 搜索 PDF 文档
- `"精确短语"` - 精确匹配搜索
- `-排除词` - 排除特定词汇
- `OR` - 或者搜索（大写）

### 时间过滤
- Google: 工具 → 任意时间 → 自定义范围
- Bing: 使用"过去 24 小时/周/月/年"筛选

### 质量评估标准
1. **域名信誉**：.edu, .gov, 权威媒体优先
2. **作者资质**：专家、学者、行业从业者
3. **引用情况**：被其他权威来源引用
4. **时效性**：发布日期明确，内容不过时
5. **客观性**：避免明显偏见、营销内容

## 交叉验证策略

### 信息一致性检查
- 至少 3 个独立来源确认同一事实
- 国际与国内媒体报道对比
- 官方消息与媒体报道对比

### 争议点识别
- 不同来源间的明显分歧
- 缺乏共识的领域
- 需要进一步验证的说法

### 谣言识别
- 单一来源独家报道
- 缺乏具体数据支撑
- 情绪化语言过多
- 无法追溯原始出处
