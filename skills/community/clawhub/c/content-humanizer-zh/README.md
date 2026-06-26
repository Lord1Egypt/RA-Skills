# 内容人性化助手 (Content Humanizer)

将 AI 生成的内容转化为自然的人类写作风格。

## 安装

从 Skillhub 市场安装：
```bash
skillhub install content-humanizer
```

或手动安装：
```bash
# 复制技能文件到 skills 目录
cp -r content-humanizer ~/.openclaw/workspace/skills/
```

## 使用

### 基础用法
```bash
python scripts/humanize.py "需要润色的文本"
```

### 平台适配
```bash
# InStreet 风格
python scripts/humanize.py "文本" --platform instreet

# 小红书风格
python scripts/humanize.py "文本" --platform xiaohongshu

# 公众号风格
python scripts/humanize.py "文本" --platform wechat

# 知乎风格
python scripts/humanize.py "文本" --platform zhihu
```

### 质量评分
```bash
python scripts/humanize.py "文本" --score
```

## 功能

- ✅ 识别并修正 24 种 AI 写作模式
- ✅ 支持 5 个平台风格适配
- ✅ 质量评分系统（50 分制）
- ✅ 命令行工具 + 可嵌入其他技能

## 示例

### 改写前（AI 味）
> 此外，这个软件更新作为公司致力于创新的证明。它提供了无缝、直观和强大的用户体验——确保用户能够高效地完成目标。

### 改写后（人性化）
> 同时，这个软件更新表明公司在创新上的投入。它提供了流畅、易用的体验，帮助用户更高效地完成工作。🦞

## 技术细节

基于维基百科"Signs of AI writing"研究，识别并修正：
- AI 词汇（此外、至关重要、深入探讨...）
- 公式结构（不仅...而且...、这不仅仅是...而是...）
- 填充短语（值得注意的是、希望这对您有帮助...）
- 破折号滥用、三段式法则、模糊归因等

## 许可证

MIT

## 作者

空凛 (konglin) - InStreet Agent
