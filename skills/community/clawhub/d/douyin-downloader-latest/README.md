# 🎵 抖音下载器 (douyin-downloader)

> 抖音视频下载工具 - OpenClaw Skill

## ⚠️ 当前状态

**基础功能可用，高级功能需要配置**

- ✅ 链接解析 - 支持多种抖音分享链接格式
- ✅ 视频 ID 提取 - 正确识别视频
- ⚠️ 视频下载 - 需要无头浏览器（Playwright）支持
- ⚠️ 元数据抓取 - 需要客户端渲染支持

## ✨ 功能

- 🔗 **链接解析** - 支持多种抖音分享链接格式
- 📹 **视频下载** - 需要 Playwright 获取真实地址
- 📦 **批量处理** - 一次处理多个链接
- 📝 **元数据保存** - 保存视频信息（可选）
- 🎯 **智能命名** - 自动生成有意义的文件名

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/douyin-downloader
npm install
```

### 2. 安装无头浏览器（必需）

抖音使用动态加载，需要 Playwright 来获取真实视频地址：

```bash
npm install playwright
npx playwright install chromium
```

### 3. 配置（可选）

在 `TOOLS.md` 中添加：

```markdown
### 抖音下载器

- 默认保存目录：~/Videos/douyin
- 保存元数据：true
- 使用无头浏览器：true
```

### 2. 使用方法

在 OpenClaw 中直接发送：

```
下载这个抖音视频：https://v.douyin.com/xxxxx
```

或批量下载：

```
下载这些视频：
- https://v.douyin.com/xxx1
- https://v.douyin.com/xxx2
- https://v.douyin.com/xxx3
```

### 3. 配置（可选）

在 `TOOLS.md` 中添加配置：

```markdown
### 抖音下载器

- 默认保存目录：~/Videos/douyin
- 保存元数据：true
- 并发下载数：3
```

## 📋 支持的链接格式

- `https://www.douyin.com/video/123456789`
- `https://www.douyin.com/note/123456789`
- `https://v.douyin.com/abc123`
- `https://m.douyin.com/abc123`
- `https://www.iesdouyin.com/abc123`

## 📁 输出示例

下载成功后：

```
✅ 下载成功！

📹 视频：精彩的舞蹈表演
👤 作者：舞蹈达人
📁 保存：C:\Users\xxx\Videos\douyin\舞蹈达人_精彩的舞蹈表演_123456789.mp4
💾 大小：15.3 MB
```

## ⚙️ API 参考

### 解析单个视频

```javascript
import { parseDouyinVideo } from './src/parser.js';

const videoInfo = await parseDouyinVideo('https://v.douyin.com/xxx');
console.log(videoInfo);
// { id, url, title, author, cover, videoUrl, ... }
```

### 下载视频

```javascript
import { downloadDouyinVideo } from './src/downloader.js';

const result = await downloadDouyinVideo(videoInfo, './videos', {
  saveMetadata: true
});
```

### 批量下载

```javascript
import { batchDownload } from './src/downloader.js';

const results = await batchDownload(videoInfos, './videos', {
  concurrency: 3
});
```

## 🔧 开发

### 测试

```bash
npm test
```

### 目录结构

```
douyin-downloader/
├── SKILL.md           # OpenClaw 技能定义
├── package.json       # 依赖配置
├── README.md          # 使用说明
├── src/
│   ├── index.js       # 主入口
│   ├── parser.js      # 链接解析
│   └── downloader.js  # 文件下载
└── scripts/
    └── setup.js       # 初始化脚本（可选）
```

## ⚠️ 注意事项

1. **仅用于个人学习** - 请勿用于商业用途
2. **遵守用户协议** - 尊重创作者版权
3. **频率限制** - 避免短时间内大量请求
4. **公开视频** - 仅支持公开可见的视频

## 🐛 常见问题

### Q: 下载失败怎么办？
A: 检查链接是否正确，确保视频是公开的。部分视频可能有访问限制。

### Q: 如何修改保存目录？
A: 在 TOOLS.md 中配置 `saveDir`，或在调用时传入配置。

### Q: 支持 TikTok 吗？
A: 当前版本仅支持抖音（中国版）。TikTok 需要单独的解析逻辑。

## 📄 许可证

MIT License

## 🙏 致谢

感谢 OpenClaw 社区和所有贡献者！
