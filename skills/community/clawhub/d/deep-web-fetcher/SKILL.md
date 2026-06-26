# Skill: Deep Web Fetcher

> 版本：1.0.0  
> 描述：免费网页抓取 + 内容提取 + 结构化输出，无需付费API

---

## 核心功能

- **网页抓取**：支持JS渲染，自动等待页面加载
- **正文提取**：智能识别文章主体，过滤广告/导航
- **元数据提取**：自动提取标题、作者、发布时间
- **指标提取**：从正文提取关键数据（样本量、AUC、成本等）

---

## 触发命令

```bash
/web-fetcher <url> [--domain <领域>]
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `url` | 必填 | 目标网页URL |
| `--domain` | general | 研究领域，影响指标提取规则 |

### 领域选项

- `general`：通用提取
- `healthcare`：医疗/健康领域
- `medical`：医学研究
- `insurance`：保险控费
- `machine_learning`：机器学习

---

## 执行流程

```
1. 启动Playwright浏览器
2. 访问目标URL，等待JS渲染完成
3. 使用Readability提取正文
4. 提取元数据（标题、作者、时间）
5. 根据领域规则提取关键指标
6. 输出生成JSON
```

---

## 输出格式

```json
{
  "url": "https://example.com/article",
  "success": true,
  "title": "文章标题",
  "author": "作者名",
  "published_date": "2024-01-15",
  "content_text": "正文内容...",
  "content_html": "<html>...</html>",
  "word_count": 1500,
  "extracted_metrics": {
    "sample_size": "9,080",
    "auc": 0.85,
    "accuracy": 92.5
  },
  "error": null
}
```

---

## 使用示例

### 抓取arXiv论文

```bash
/web-fetcher "https://arxiv.org/abs/2301.12345" --domain "machine learning"
```

### 抓取PubMed摘要

```bash
/web-fetcher "https://pubmed.ncbi.nlm.nih.gov/38134648/" --domain "medical"
```

### 抓取政府报告

```bash
/web-fetcher "https://www.gov.cn/zhengce/zhengceku/2024-01/15/content_6923456.htm" --domain "insurance"
```

---

## 依赖安装

```bash
# 安装Python依赖
pip install playwright readability-lxml lxml beautifulsoup4

# 安装浏览器驱动（首次运行需下载~100MB）
playwright install chromium
```

---

## 注意事项

### 反爬策略

部分网站有反爬机制，如遇失败可：

1. **增加延迟**：在脚本中调整 `time.sleep()`
2. **使用代理**：在 `browser.new_context()` 中添加代理
3. **轮换UA**：修改 `user_agent` 参数

### 提取准确率

- 标准网页（文章/博客）：✅ 效果优秀
- 复杂布局（多栏/动态加载）：⚠️ 可能需人工复核
- PDF页面：❌ 不支持，请用PDF专用工具

### 执行速度

- 单页抓取：5-15秒（含浏览器启动）
- 批量抓取：建议并发3-5个

---

## 与深度研究v6.0集成

```bash
# 生成卡片
/web-fetcher <url> --domain "insurance" > sources/card-xxx.json

# 转换卡片格式
python3 scripts/convert-to-card.py sources/card-xxx.json
```

---

## 文件结构

```
skills/web-fetcher/
├── SKILL.md
└── scripts/
    └── web-fetcher.py
```

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | 2026-03-19 | 初始版本 |

---

*完全免费，本地运行，数据不出机器*
