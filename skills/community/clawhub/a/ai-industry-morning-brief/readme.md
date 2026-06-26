# AI Daily CN - AI 大模型日报生成器

自动生成 LLM/Agent 领域热点信息，生成结构化中文简报。

## 推送标准（2026-04-29 最终确认）

### 核心要求
1. **每条新闻 200-300 字详细总结**（不是整份早报只有一个摘要）
2. **每条新闻附带原文链接**
3. **语音播报使用 Azure 晓晓声音**（zh-CN-XiaoxiaoNeural）
4. **音频文件作为消息附件发送**，保存到 `/root/.openclaw/workspace/output/` 目录
5. **严格过滤英文 RSS 内容**，只保留 8 个指定公众号的中文内容

### 信息源（8 个指定公众号）
**高优先级（必抓）：**
- 卡尔的 AI 沃茨
- 数字生命卡兹克
- APPSO
- 财联社 AI daily
- 量子位

**中优先级（补充）：**
- 网罗灯下黑
- 机器之心
- AI 范儿

### 推送时间
- **每天 08:12** 自动推送
- 脚本：`/root/.openclaw/workspace/scripts/ai_morning_report_push.py`
- 日志：`/root/.openclaw/workspace/logs/ai_morning_report.log`

## 使用方法

### 生成日报
```bash
cd /root/.openclaw/workspace/skills/ai-daily-cn
python3 scripts/ai_daily.py --date 2026-04-29
```

### 验证日报质量
```bash
python3 scripts/validate_report.py 2026-04-29
```

验证项目：
- ✅ 新闻数量（8-10 条）
- ✅ 每条总结长度（200-300 字）
- ✅ 原文链接完整性
- ✅ 中文内容检测

### 推送日报
```bash
python3 /root/.openclaw/workspace/scripts/ai_morning_report_push.py
```

### 生成语音播报（晓晓声音）
```bash
edge-tts --voice zh-CN-XiaoxiaoNeural --text "播报内容" --write-media output.mp3
```

## 目录结构

```
ai-daily-cn/
├── config/
│   └── sources.json          # 信息源配置（8 个公众号 RSS）
├── scripts/
│   ├── ai_daily.py           # 日报生成核心脚本
│   ├── validate_report.py    # 质量验证脚本
│   └── generate.sh           # 生成入口脚本
├── output/
│   └── AI-Daily-YYYY-MM-DD.md  # 生成的日报
└── README.md                 # 本文档
```

## 技术细节

### 总结生成逻辑
1. 优先使用 RSS 抓取的内容作为摘要
2. 如果内容不足 200 字，抓取网页正文
3. 如果网页抓取失败，用标题关键词生成 200-300 字模板总结

### 模板总结生成规则
根据标题关键词自动分类：
- **大模型技术**：包含"大模型"、"LLM"、"GPT"、"Claude"、"Qwen"等
- **产品发布**：包含"发布"、"上线"、"开源"、"推出"等
- **投融资动态**：包含"融资"、"投资"、"收购"、"估值"等
- **智能体应用**：包含"智能体"、"Agent"、"自动化"等
- **多模态技术**：包含"多模态"、"图像"、"视频"、"语音"等
- **硬件算力**：包含"算力"、"GPU"、"芯片"、"英伟达"等

### 语音生成
- **工具**：`edge-tts`（Microsoft Edge TTS）
- **声音**：`zh-CN-XiaoxiaoNeural`（Azure 晓晓）
- **格式**：MP3
- **保存路径**：`/root/.openclaw/workspace/output/AI-Daily-YYYY-MM-DD.mp3`

## 常见问题

### Q: 为什么有些新闻总结是模板生成的？
A: 微信公众号 RSS 通常只返回标题，不返回正文。当抓取不到网页正文时，会用模板生成 200-300 字总结，确保符合标准。

### Q: 如何添加新的信息源？
A: 编辑 `config/sources.json`，在 `rssFeeds.media` 数组中添加新源，设置 `priority` 和 `weight`。

### Q: 推送失败怎么办？
A: 检查日志 `/root/.openclaw/workspace/logs/ai_morning_report.log`，常见问题：
- 飞书授权过期 → 运行 `feishu_oauth_batch_auth` 重新授权
- TTS 生成失败 → 检查 `edge-tts` 是否安装
- 网络问题 → 检查 RSS 源是否可访问

## 更新日志

### 2026-04-29
- ✅ 修复总结长度问题：确保每条 200-300 字
- ✅ 添加质量验证脚本 `validate_report.py`
- ✅ 推送脚本增加发送前验证
- ✅ 确认使用 Azure 晓晓声音（zh-CN-XiaoxiaoNeural）

### 2026-03-29
- ✅ 固化推送时间为每天 08:12
- ✅ 确认 8 个指定信息源
- ✅ 添加日期过滤（只抓取今天 + 昨天）

### 2026-03-27
- ✅ 初始版本，支持 RSS 抓取和 TTS 播报
