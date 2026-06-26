# 浏览器自动化学习笔记

**学习开始时间**: 2026-03-04  
**当前进度**: 3/10 视频（30%）  
**学习目标**: 掌握 browser 命令，用于流量号内容创作（抓取 B 站热榜、热门评论等）

---

## 核心命令速查

### 1. `browser open` - 打开网页
```bash
# 打开指定 URL
browser open https://www.bilibili.com/v/popular/rank/all

# 使用隔离浏览器（推荐）
browser open --profile openclaw https://example.com
```

**参数说明**:
- `targetUrl`: 要打开的网址
- `profile`: 
  - `openclaw` - 隔离浏览器（独立 Chrome 实例，无需扩展）
  - `chrome` - Chrome 扩展模式（需手动点击扩展图标连接标签页）

---

### 2. `browser snapshot` - 提取页面元素
```bash
# 提取页面所有可交互元素
browser snapshot --refs aria

# 提取特定区域
browser snapshot --selector ".video-list"
```

**参数说明**:
- `refs`: 元素引用方式
  - `aria` - 使用 ARIA 标签（稳定，推荐）
  - `role` - 使用角色 + 名称（默认）
- `selector`: CSS 选择器，定位特定区域

**输出示例**:
```json
{
  "elements": [
    {"ref": "e12", "role": "link", "name": "瓜摊斗舞", "type": "video"},
    {"ref": "e13", "role": "text", "name": "226 万播放"}
  ]
}
```

---

### 3. `browser screenshot` - 截图
```bash
# 全屏截图
browser screenshot --fullPage

# 截取特定区域
browser screenshot --selector ".video-card"
```

**参数说明**:
- `fullPage`: 是否截取整个页面
- `type`: 图片格式（png/jpeg）
- `selector`: 截取特定元素

---

### 4. `browser act` - 执行操作
```bash
# 点击元素
browser act --action click --ref e12

# 输入文本
browser act --action type --ref search-box --text "AI 教程"

# 滚动页面
browser act --action scroll --deltaY 500

# 等待元素出现
browser act --action wait --text "加载中" --textGone "加载中"
```

**常用操作**:
- `click` - 点击
- `type` - 输入文本
- `press` - 按键（Enter、ArrowDown 等）
- `hover` - 悬停
- `select` - 选择下拉选项
- `fill` - 填充表单
- `wait` - 等待条件

---

### 5. `browser navigate` - 页面导航
```bash
# 跳转到指定 URL
browser navigate https://example.com

# 前进/后退
browser act --action press --key "ArrowRight"  # 前进
browser act --action press --key "ArrowLeft"   # 后退
```

---

## 实战案例：抓取 B 站热榜 Top 10

### 步骤 1: 打开热榜页面
```bash
browser open https://www.bilibili.com/v/popular/rank/all
```

### 步骤 2: 等待加载 + 截图
```bash
browser act --action wait --timeMs 3000
browser screenshot --fullPage
```

### 步骤 3: 提取视频列表
```bash
browser snapshot --refs aria
```

### 步骤 4: 点击第一个视频
```bash
browser act --action click --ref e12  # e12 是 snapshot 返回的元素引用
```

### 步骤 5: 抓取评论区
```bash
browser snapshot --selector ".comment-list"
```

### 步骤 6: 提取热门评论
```bash
# 提取 Top 评论（带点赞数）
browser act --action evaluate --fn "
  () => {
    const comments = document.querySelectorAll('.comment-item');
    return Array.from(comments).map(c => ({
      text: c.querySelector('.text').innerText,
      likes: c.querySelector('.likes').innerText
    }));
  }
"
```

---

## 常见问题

### Q1: 浏览器无法启动
**解决**: 
```bash
# 检查浏览器状态
browser status

# 重启浏览器
browser stop
browser start --profile openclaw
```

### Q2: snapshot 返回空结果
**原因**: 页面未加载完成  
**解决**: 先等待再截图
```bash
browser act --action wait --timeMs 3000
browser snapshot
```

### Q3: 元素引用失效
**原因**: 页面动态刷新导致元素 ID 变化  
**解决**: 使用 `refs="aria"`（更稳定）或重新 snapshot

### Q4: Chrome 扩展模式无法连接
**原因**: 需要手动点击扩展图标  
**解决**: 
1. 点击 Chrome 工具栏的 OpenClaw 扩展图标
2. 确保徽章是 ON 状态
3. 或者改用 `--profile openclaw`（隔离浏览器）

---

## 流量号创作应用场景

### 场景 1: 抓取热门视频标题 + 播放量
```bash
# 用途：分析什么内容火，找选题灵感
browser snapshot --selector ".rank-list .title"
```

### 场景 2: 抓取热门评论
```bash
# 用途：学习神评论写法，用于自己视频的评论区运营
browser snapshot --selector ".comment .text"
```

### 场景 3: 监控竞品账号
```bash
# 用途：定期抓取竞对的视频数据，分析爆款规律
browser open https://space.bilibili.com/{UP 主 ID}
browser snapshot --selector ".video-list"
```

### 场景 4: 自动点赞 + 收藏
```bash
# 用途：批量运营自己的视频
browser act --action click --ref "like-btn"
browser act --action click --ref "fav-btn"
```

---

## 今日学习进度

| 视频 | 状态 | 关键收获 |
|------|------|----------|
| 1. 瓜摊斗舞 | ✅ 完成 | 学会 browser open/snapshot |
| 2. 金雨良缘 | ✅ 完成 | 学会 browser screenshot |
| 3. 雪地里的鸡你太美 | ❌ 跳过 | 链接失效 |
| 4-10. 剩余视频 | ⏳ 待学习 | |

**下一步**: 
- [ ] 完成剩余 7 个视频
- [ ] 实战：抓取 B 站热榜 Top 10
- [ ] 写第一个流量号脚本（用抓取的数据）

---

## 技术知识点

### JSON 数据格式
```json
{
  "title": "视频标题",
  "views": "226 万播放",
  "comments": [
    {"text": "现场 [doge]", "likes": 5929}
  ]
}
```
**理解**: JSON 就是带标签的数据文本，像 Excel 表格/快递单/菜单

### CORS 限制
**问题**: 浏览器不允许 `file://` 协议读取本地 JSON 文件  
**解决**: 
- 方案 A: 数据直接嵌入 HTML（刻在石头上，稳定但难修改）
- 方案 B: 用本地服务器提供 JSON（灵活但有 CORS 问题）

**推荐**: 简单项目用方案 A，复杂项目用方案 B

---

_Last Updated: 2026-03-05 11:15_
