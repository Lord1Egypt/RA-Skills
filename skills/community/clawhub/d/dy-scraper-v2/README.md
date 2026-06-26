# 抖音爆款爬虫 Skill

使用 Playwright 自动化浏览器操作，爬取抖音爆款视频和文案数据。

## 📦 安装

### 方式一：一键安装（推荐）

```bash
# 进入 skill 目录
cd /root/.openclaw/workspace/skills/douyin-scraper

# 运行安装脚本
./install.sh
```

### 方式二：手动安装 - Python 版本

```bash
# 进入 skill 目录
cd /root/.openclaw/workspace/skills/douyin-scraper

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install playwright

# 安装浏览器
playwright install chromium
```

### 方式三：Node.js 版本

```bash
# 进入 skill 目录
cd /root/.openclaw/workspace/skills/douyin-scraper

# 安装依赖
npm install

# 安装浏览器
npx playwright install chromium
```

## 🚀 快速开始

### 方式一：使用启动脚本（推荐）

```bash
# 搜索关键词
./run.sh search --keyword "海鲜" --limit 10

# 获取热榜
./run.sh hot --limit 20

# 搜索并保存结果
./run.sh search --keyword "海鲜售卖" --limit 20 --output seafood_videos.json
```

### 方式二：手动激活虚拟环境

```bash
# 激活虚拟环境
source venv/bin/activate

# 搜索关键词
python scripts/scraper.py search --keyword "海鲜" --limit 10

# 获取热榜
python scripts/scraper.py hot --limit 20

# 搜索并保存结果
python scripts/scraper.py search --keyword "海鲜售卖" --limit 20 --output seafood_videos.json
```

### Node.js 版本

```bash
# 搜索关键词
node scripts/douyin_scraper.js search "海鲜" 10

# 获取热榜
node scripts/douyin_scraper.js hot 20

# 搜索并保存结果
node scripts/douyin_scraper.js search "海鲜售卖" 20 seafood_sales.json json
```

## 📝 使用示例

### 示例 1：搜索海鲜售卖视频

```bash
# Python 版本
python scripts/scraper.py search --keyword "海鲜售卖" --limit 15 --output seafood_sales.json

# Node.js 版本
node scripts/douyin_scraper.js search "海鲜售卖" 15 seafood_sales.json json
```

### 示例 2：获取美食热榜

```bash
# Python 版本
python scripts/scraper.py hot --category "美食" --limit 20 --output food_hot.json

# Node.js 版本
node scripts/douyin_scraper.js hot "美食" 20 food_hot.json json
```

### 示例 3：导出 CSV 格式

```bash
# Python 版本
python scripts/scraper.py search --keyword "小龙虾" --limit 10 --format csv --output crayfish.csv

# Node.js 版本
node scripts/douyin_scraper.js search "小龙虾" 10 crayfish.csv csv
```

## 📊 输出数据格式

### JSON 格式

```json
[
  {
    "title": "视频标题",
    "description": "视频描述",
    "author": "作者昵称",
    "play_count": 1000000,
    "like_count": 50000,
    "comment_count": 2000,
    "share_count": 1000,
    "url": "https://www.douyin.com/video/xxx",
    "tags": ["标签1", "标签2"],
    "publish_time": "2026-03-21"
  }
]
```

### CSV 格式

```csv
title,author,play_count,like_count,comment_count,url,tags
视频标题,作者昵称,1000000,50000,2000,https://...,标签1|标签2
```

## ⚙️ 配置选项

### Python 版本

```bash
# 无头模式（不显示浏览器）
--headless

# 请求间隔（秒）
--delay 3.0

# 输出格式
--format json|csv
```

### Node.js 版本

在代码中修改配置：

```javascript
const scraper = new DouyinScraper({
    headless: true,  // 无头模式
    delay: 2000      // 请求间隔（毫秒）
});
```

## ⚠️ 注意事项

1. **遵守抖音平台规则** - 合理使用，避免频繁请求
2. **请求间隔** - 建议在请求之间添加适当延时（默认 2 秒）
3. **数据用途** - 仅供学习和研究使用
4. **账号安全** - 不要登录账号，避免风控
5. **IP 限制** - 注意 IP 被封禁的风险

## 🔧 故障排除

### 问题：浏览器启动失败

**解决方案：**
```bash
# Python 版本
playwright install chromium

# Node.js 版本
npx playwright install chromium
```

### 问题：页面加载超时

**解决方案：**
- 增加超时时间
- 检查网络连接
- 尝试使用代理

### 问题：找不到元素

**解决方案：**
- 抖音页面可能已更新
- 检查选择器是否需要更新

## 📚 更多信息

- [Playwright 文档](https://playwright.dev/)
- [SKILL.md](./SKILL.md) - 详细使用说明

## 🤝 配合使用的 Skill

- `douyin-download` - 下载抖音视频
- `video-merger` - 合并视频
- `eachlabs-video-edit` - 视频编辑

---

**使用前请确保遵守相关法律法规和平台规则！**
