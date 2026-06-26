# HTML 分页问题修复说明

## 问题描述

用户反馈：生成的 HTML 封面只能看到两页内容，10 条资讯在第 2 页被裁切，无法完整显示。

## 问题原因

### 1. 固定页数配置
- 原代码使用 `config.htmlPages` 固定配置（默认 2 屏）
- 不管有多少条资讯，都只生成 2 页

### 2. 第 2 页内容溢出
- 第 2 页的 `.news-list` 使用 `flex-direction: column`
- 10 条资讯卡片总高度远超 1440px（页面高度）
- 超出部分被 `overflow: hidden` 裁切，无法看到

### 3. 缺少自动分页逻辑
- 没有根据资讯数量自动计算需要的页数
- 所有资讯塞进一页，导致内容溢出

## 解决方案

### 1. 自动计算页数

```javascript
// 每页最多 5 条卡片
const ITEMS_PER_PAGE = 5;
const detailPagesNeeded = Math.ceil(newsItems.length / ITEMS_PER_PAGE);
const numPages = 1 + detailPagesNeeded + 1; // 封面 + 详细页 + 观点页
```

### 2. 循环生成详细页

```javascript
// 第 2~N 屏：详细列表（自动分页，每页 5 条）
for (let pageNum = 0; pageNum < detailPagesNeeded; pageNum++) {
  const startIdx = pageNum * ITEMS_PER_PAGE;
  const endIdx = Math.min(startIdx + ITEMS_PER_PAGE, newsItems.length);
  const pageNews = newsItems.slice(startIdx, endIdx);
  
  pages.push(`
    <div class="page page-${pageNum + 2}">
      <div class="section-title">📊 详细资讯 ${startIdx + 1}-${endIdx} / ${newsItems.length}</div>
      <div class="news-list">
        ${pageNews.map(...).join('')}
      </div>
      ${isLastDetailPage ? '' : '<div class="page-hint">↓ 继续滑动查看更多 ↓</div>'}
    </div>
  `);
}
```

### 3. 优化 CSS 样式

**修改前**：
```css
.page-2 { background: #f8f9fa; padding: 80px 60px; }
.news-list { display: flex; flex-direction: column; gap: 30px; }
.news-card { padding: 35px; }
```

**修改后**：
```css
.page-detail { background: #f8f9fa; padding: 80px 60px; } /* 通用类名 */
.news-list { display: flex; flex-direction: column; gap: 25px; } /* 减小间距 */
.news-card { 
  padding: 30px; 
  break-inside: avoid; /* 避免卡片被分页切断 */
}
.news-card-header { margin-bottom: 12px; } /* 减小间距 */
.news-number { width: 45px; height: 45px; font-size: 22px; } /* 缩小序号 */
.news-card-title { font-size: 30px; line-height: 1.3; } /* 优化行高 */
.page-hint { 
  text-align: center; 
  font-size: 24px; 
  color: #999; 
  margin-top: 30px; 
  opacity: 0.7; 
} /* 新增提示 */
```

## 修复效果

### 资讯数量 vs 页数

| 资讯数量 | 详细页页数 | 总页数 |
|---------|-----------|--------|
| 1-5 条   | 1 页      | 3 页   |
| 6-10 条  | 2 页      | 4 页   |
| 11-15 条 | 3 页      | 5 页   |
| 16-20 条 | 4 页      | 6 页   |

### 实际效果

**5 条资讯**：
```
Page 1: 封面（标题 + 重磅 + 预览 3 条）
Page 2: 详细资讯 1-5 / 5
Page 3: 观点 + 互动
```

**10 条资讯**：
```
Page 1: 封面（标题 + 重磅 + 预览 3 条）
Page 2: 详细资讯 1-5 / 10  ← 新增提示"↓ 继续滑动查看更多 ↓"
Page 3: 详细资讯 6-10 / 10
Page 4: 观点 + 互动
```

## 修改文件

- `scripts/create-xiaohongshu-content.js`
  - `generateHTML()` 函数完全重写
  - 删除 `config.htmlPages` 配置的使用
  - 新增自动分页逻辑
  - 优化 CSS 样式

## 测试验证

```bash
# 测试 5 条资讯
node scripts/run-full-flow.js
grep -c '<div class="page page-' output/日期/cover.html
# 输出：3

# 测试 10 条资讯
node scripts/create-xiaohongshu-content.js --news-json '[...10 条...]'
grep -c '<div class="page page-' output/日期/cover.html
# 输出：4
```

## 后续优化建议

1. **响应式高度**：根据内容动态调整页面高度，而非固定 1440px
2. **可配置每页条数**：允许用户通过配置调整 `ITEMS_PER_PAGE`
3. **优化卡片密度**：根据屏幕尺寸调整字体大小和间距
4. **添加页码**：在每页底部显示"第 X 页 / 共 Y 页"

---

**修复时间**：2026-03-25  
**修复者**：爪爪 🛰️
