# PRD: 抖音视频拆解分析器 (Douyin Video Analyzer)

> **Version**: 1.0
> **Status**: Draft
> **Owner**: Leo
> **Lead Developer**: Cipher

## 1. Executive Summary

- **Problem**: 内容创作者想要学习爆款视频的制作技巧，但手动拆解费时费力，缺乏系统化的分析框架
- **Solution**: 输入抖音视频链接，自动生成包含数据、结构、视觉、文案的完整拆解报告
- **Goals**: 
  1. 30秒内完成单视频的深度分析
  2. 输出可直接用于模仿学习的结构化报告
  3. 识别可复制的爆款元素

## 2. Requirements

### 2.1 Functional Requirements
- [ ] 接受抖音视频链接输入（支持短链和长链）
- [ ] 抓取视频页面获取基础数据（点赞、评论、分享、收藏数）
- [ ] 下载视频文件到本地临时目录
- [ ] 提取视频关键帧（每秒1帧或按场景分割）
- [ ] 音频提取并转文字（ASR）
- [ ] AI视觉分析：识别画面元素、字幕样式、场景切换
- [ ] 生成结构化分析报告（Markdown格式）

### 2.2 Non-Functional Requirements
- **Performance**: 单视频分析 < 60秒
- **Scalability**: 支持并发处理多个视频
- **Security**: 不存储用户视频，分析后自动清理临时文件

## 3. Technical Stack

- **Runtime**: Node.js (与现有抖音热榜技能保持一致)
- **Video Processing**: ffmpeg
- **Web Scraping**: playwright / axios + cheerio
- **AI Analysis**: Gemini Vision API (图像分析) + Gemini Pro (文案分析)
- **ASR**: 智谱 ASR 技能 (已有) 或 Gemini Audio

## 4. Implementation Plan (OpenSpec)

### Phase 1: Foundation
- [ ] 1.1 创建技能目录结构和 _meta.json
- [ ] 1.2 实现视频链接解析（短链转长链）
- [ ] 1.3 实现网页数据抓取（基础信息）

### Phase 2: Core Logic
- [ ] 2.1 集成 ffmpeg 下载和处理视频
- [ ] 2.2 实现关键帧提取功能
- [ ] 2.3 集成 AI 视觉分析
- [ ] 2.4 集成 ASR 音频转文字

### Phase 3: Integration & Testing
- [ ] 3.1 整合所有模块，生成完整报告
- [ ] 3.2 编写 SKILL.md 文档
- [ ] 3.3 测试不同类型的视频（带货、知识、娱乐）

## 5. Risk Assessment

- **抖音反爬机制**: 使用随机 User-Agent + 请求间隔，必要时使用 Playwright
- **视频下载限制**: 部分视频可能无法直接下载，需要处理异常情况
- **API成本**: Gemini Vision 调用成本，需要优化帧提取策略（关键帧而非全帧）

## 6. CLI Interface

```bash
# 分析单个视频
node scripts/analyze.js <video_url>

# 输出示例
node scripts/analyze.js https://v.douyin.com/xxxxx
```

## 7. Output Format

```markdown
📊 视频拆解报告
━━━━━━━━━━━━━━━━━━━━━━
🔗 视频链接: [链接]
👤 作者: [@username]

📈 基础数据
• 点赞: 128.5万 | 评论: 3.2万 | 分享: 8.7万 | 收藏: 12.1万
• 发布日期: 2026-03-11
• 视频时长: 45秒

📝 内容结构
• 0-3秒: [黄金钩子分析]
• 3-15秒: [主体内容]
• 15-45秒: [结尾转化]

🎬 视觉分析
• 画面风格: [大字报/实拍/混剪]
• 字幕特征: [字号/颜色/出现频率]
• 场景切换: [切换次数和节奏]

🎯 可复制元素
• 开场话术模板
• 字幕样式建议
• BGM选择策略
• 节奏控制技巧
```
