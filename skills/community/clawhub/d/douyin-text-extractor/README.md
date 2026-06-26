# 抖音文案提取工具 (douyin-text-extractor)

> 🎬 从抖音分享链接提取无水印视频，AI 自动识别语音文案  
> 🎓 新用户注册硅基流动使用邀请码 **`84kySW0S`** 获取免费额度  
> 🔌 支持 MCP Server 集成（Claude Desktop）  
> ⚡ 支持大文件自动分段处理，Markdown 格式输出

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Version](https://img.shields.io/badge/version-1.2.0-green.svg)

---

## ✨ 功能特性

- 🎬 **无水印视频下载** - 获取高质量无水印视频下载链接
- 🎙️ **AI 语音识别** - 使用硅基流动 SenseVoice API 自动提取文案
- 🔌 **MCP Server** - 支持 Claude Desktop 集成
- 🎓 **新用户引导** - 自动引导注册硅基流动，使用邀请码 `84kySW0S` 获取免费额度
- 📑 **大文件支持** - 自动分段处理超过 1 小时或 50MB 的音频
- 📄 **Markdown 输出** - 文案自动保存为 Markdown 格式，包含视频信息
- 🔧 **灵活使用** - 支持命令行、Python 调用、Skill 集成、MCP
- 📦 **自动安装 FFmpeg** - 首次使用自动下载并配置 FFmpeg（约 100MB）

---

## 🚀 快速开始

### 1. 安装 Skill

```bash
claw skill install douyin-text-extractor
cd douyin-text-extractor
```

### 2. 安装依赖

```bash
# 安装 Python 依赖
uv sync
# 或
pip install requests ffmpeg-python mcp dashscope
```

### 3. FFmpeg 自动安装（可选）

**无需手动安装！** 首次运行提取文案时会自动检测并安装 FFmpeg。

```bash
# 或手动预安装
python scripts/install_ffmpeg.py
```

**自动下载 FFmpeg 静态编译版本（约 100MB），支持：**
- ✅ macOS (Intel/Apple Silicon)
- ✅ Linux (x64)
- ✅ Windows (x64)

### 4. 获取 API Key（仅文案提取需要）

**首次使用需要先注册硅基流动：**

1. 访问注册页面：https://cloud.siliconflow.cn/i/84kySW0S
2. 使用邀请码 **`84kySW0S`** 注册（获得额外免费额度）
3. 登录后在控制台获取 API Key
4. 设置环境变量：

```bash
export API_KEY="sk-xxxxxxxxxxxxxxxx"
```

### 5. 开始使用

**方式 1: 智能体对话**
```
提取这个抖音视频的文案 https://v.douyin.com/xxxxx/
```

**方式 2: 命令行**
```bash
# 获取视频信息（无需 API）
python src/douyin_extractor.py -l "抖音分享链接" -a info

# 下载无水印视频（无需 API）
python src/douyin_extractor.py -l "抖音分享链接" -a download -o ./videos

# 提取文案（需要 API）
python src/douyin_extractor.py -l "抖音分享链接" -a extract -o ./output
```

**方式 3: MCP Server**

编辑 Claude Desktop 配置 `claude_desktop_config.json`：
```json
{
  "mcpServers": {
    "douyin-mcp": {
      "command": "python",
      "args": ["src/mcp_server.py"],
      "env": {
        "API_KEY": "sk-xxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

---

## 📖 使用示例

### 示例 1：获取视频信息

```bash
python src/douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a info
```

**输出：**
```
视频 ID: 7600361826030865707
标题：有趣的抖音视频
下载链接：https://aweme.snssdk.com/...
```

### 示例 2：下载视频

```bash
python src/douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a download -o ./videos
```

**输出：**
```
正在下载视频：有趣的抖音视频
下载进度：100.0%
视频已保存到：./videos/7600361826030865707.mp4
```

### 示例 3：提取文案

```bash
export API_KEY="sk-xxx"
python src/douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a extract -o ./output
```

**输出：**
```
正在下载视频：有趣的抖音视频
下载进度：100.0%

识别第 1/1 段...

✅ 文案已保存到：./output/7600361826030865707/transcript.md
```

### 示例 4：在 Python 代码中使用

```python
from douyin_extractor import DouyinExtractor

# 初始化提取器
extractor = DouyinExtractor(api_key="sk-xxx")

# 获取视频信息
info = extractor.get_video_info("https://v.douyin.com/xxxxx/")
print(f"标题：{info['title']}")

# 提取文案
result = extractor.extract_text("https://v.douyin.com/xxxxx/", output_dir="./output")
print(f"文案：{result['text'][:100]}...")
```

---

## 📁 输出格式

### 目录结构

```
output/
├── 7600361826030865707/          # 视频 ID 为文件夹名
│   ├── transcript.md             # 文案文件
│   └── 7600361826030865707.mp4   # 视频文件（使用 --save-video 时保存）
├── 7581044356631612699/
│   └── transcript.md
└── ...
```

### transcript.md 内容

```markdown
# 有趣的抖音视频

| 属性 | 值 |
|------|-----|
| 视频 ID | `7600361826030865707` |
| 提取时间 | 2026-03-23 14:30:00 |
| 下载链接 | [点击下载](https://...) |
| 分享链接 | https://v.douyin.com/xxxxx/ |

---

## 文案内容

这里是 AI 识别的语音文案内容...
大家好，今天给大家分享一个有趣的话题...

---

**提取工具:** 抖音文案提取工具  
**语音识别:** 硅基流动 SenseVoice API  
**邀请码:** 84kySW0S（注册获取免费额度）
```

---

## 🎓 硅基流动注册指南

### 为什么选择硅基流动？

- ✅ **免费额度** - 新用户注册送免费调用额度
- ✅ **邀请码奖励** - 使用邀请码 `84kySW0S` 额外获得奖励
- ✅ **高质量识别** - FunAudioLLM/SenseVoiceSmall 模型，准确率 > 95%
- ✅ **大文件支持** - 自动分段处理长音频
- ✅ **快速稳定** - 国内访问速度快，服务稳定

### 注册步骤

**步骤 1：访问注册页面**

打开链接：https://cloud.siliconflow.cn/i/84kySW0S

**步骤 2：填写邀请码**

在注册页面填写邀请码：`84kySW0S`

> 💡 **使用邀请码好处：** 获得额外免费额度，比直接注册更划算

**步骤 3：完成注册**

- 使用手机号或邮箱注册
- 完成验证
- 登录控制台

**步骤 4：获取 API Key**

1. 登录后进入「控制台」
2. 点击「API Keys」
3. 创建新的 API Key
4. 复制保存（只显示一次）

**步骤 5：设置环境变量**

```bash
# macOS/Linux
export API_KEY="sk-xxxxxxxxxxxxxxxx"

# Windows (PowerShell)
$env:API_KEY="sk-xxxxxxxxxxxxxxxx"

# Windows (CMD)
set API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 免费额度说明

- **新用户福利** - 注册即送免费调用额度
- **邀请码奖励** - 使用邀请码 `84kySW0S` 额外获得奖励
- **模型价格** - SenseVoiceSmall 模型价格低廉，免费额度可使用多次
- **查看余额** - 在控制台随时查看剩余额度

---

## 🔧 命令行参数

```
抖音文案提取工具 - 使用指南

📝 基本用法:
  python douyin_extractor.py -l "抖音分享链接" -a extract

🔧 可用操作:
  info     - 获取视频信息（无需 API）
  download - 下载无水印视频（无需 API）
  extract  - 提取文案（需要 API Key）

🎓 首次使用:
  1. 访问：https://cloud.siliconflow.cn/i/84kySW0S
  2. 使用邀请码 84kySW0S 注册
  3. 获取 API Key
  4. 设置环境变量：export API_KEY="sk-xxx"

📦 参数说明:
  -l, --link     抖音分享链接（必填）
  -a, --action   操作类型：info/download/extract（必填）
  -o, --output   输出目录（默认：./output）
  --save-video   提取文案时同时保存视频
  -q, --quiet    安静模式（减少输出）

💡 示例:
  # 获取视频信息
  python douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a info
  
  # 下载视频
  python douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a download -o ./videos
  
  # 提取文案
  export API_KEY="sk-xxx"
  python douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a extract -o ./output
  
  # 提取文案并保存视频
  python douyin_extractor.py -l "https://v.douyin.com/xxxxx/" -a extract -o ./output --save-video
```

---

## 🐛 常见问题

### Q: 没有 API Key 能用吗？

**A:** 可以！获取视频信息和下载无水印视频不需要 API Key，只有提取文案需要。

### Q: 邀请码有什么用？

**A:** 使用邀请码 `84kySW0S` 注册可以获得额外免费额度，比直接注册更划算。

### Q: 提取文案失败怎么办？

**A:** 检查以下几点：
1. API Key 是否正确设置
2. API Key 是否有余额
3. FFmpeg 是否正确安装
4. 视频链接是否有效

### Q: 如何检查 FFmpeg 是否安装？

```bash
ffmpeg -version
```

如果未安装，请参考「安装系统依赖」部分。

### Q: 支持其他平台吗？

**A:** 当前仅支持抖音，快手、视频号等平台支持正在开发中。

### Q: 大文件如何处理？

**A:** 超过 1 小时或 50MB 的音频会自动分段处理，无需手动操作。

### Q: API Key 安全吗？

**A:** API Key 仅保存在本地环境变量中，不会上传到任何服务器。请勿将 API Key 分享给他人。

---

## 🧪 运行测试

```bash
# 运行单元测试
python tests/test_extractor.py

# 或使用 uv
uv run pytest tests/
```

---

## 📊 技术架构

### 工作流程

```
用户输入抖音链接
    ↓
解析链接获取真实 URL
    ↓
获取视频信息（ID、标题、下载链接）
    ↓
下载无水印视频
    ↓
使用 FFmpeg 提取音频
    ↓
检测音频时长和大小
    ↓
[超过限制？] → 自动分段处理
    ↓
调用硅基流动 API 识别语音
    ↓
合并识别结果
    ↓
保存 Markdown 文案
    ↓
清理临时文件
```

### API 说明

语音识别使用 [硅基流动 SenseVoice API](https://cloud.siliconflow.cn/)：

- **模型:** `FunAudioLLM/SenseVoiceSmall`
- **限制:** 单次最大 1 小时 / 50MB
- **语言:** 支持中文、英文、日语、韩语
- **准确率:** 日常语音识别准确率 > 95%
- **价格:** 低廉（具体查看官网）

---

## 📝 更新日志

### v1.2.0 (2026-03-23)

- 📦 **FFmpeg 自动安装** - 首次使用自动下载并配置 FFmpeg
- 🔧 **改进错误提示** - 未安装 FFmpeg 时给出清晰的安装指南
- 🎓 硅基流动注册引导（邀请码：84kySW0S）

### v1.1.0 (2026-03-23)

- 🔌 **新增 MCP Server 支持** - 可在 Claude Desktop 中使用
- 🎙️ **支持阿里云百炼 API** - 多语音识别服务选择
- 🎓 硅基流动注册引导（邀请码：84kySW0S）

### v1.0.0 (2026-03-23)

- ✨ 初始版本发布
- 🎬 无水印视频下载
- 🎙️ AI 语音识别文案提取
- 🎓 硅基流动注册引导（邀请码：84kySW0S）
- 📑 大文件自动分段处理
- 📄 Markdown 格式输出
- 🔧 命令行和 Python API

---

## 🔗 相关链接

- **硅基流动注册:** https://cloud.siliconflow.cn/i/84kySW0S
- **邀请码:** `84kySW0S`
- **API 文档:** https://docs.siliconflow.cn/
- **GitHub 仓库:** https://github.com/rfdiosuao/openclaw-skills/tree/main/douyin-text-extractor
- **ClawHub 页面:** （发布后更新）

---

## 💡 应用场景

### 内容创作者
快速提取热门视频文案，分析爆款内容结构，获取创作灵感。

### 自媒体运营
批量提取竞品视频文案，研究内容策略，优化运营方案。

### 学习研究
提取教学视频文案，整理学习笔记，建立知识库。

### AI 训练
收集视频文案作为语料库，训练自定义模型。

### 市场调研
分析行业视频内容，了解市场趋势和用户需求。

---

## ⚠️ 免责声明

- 本项目仅供学习和研究使用
- 使用者需遵守相关法律法规
- 禁止用于侵犯知识产权的行为
- 作者不对使用本项目产生的损失承担责任

---

## 📄 许可证

MIT License

---

## 👨‍💻 作者

**OpenClaw Skill Master** ⚡

---

**最后更新:** 2026-03-23
