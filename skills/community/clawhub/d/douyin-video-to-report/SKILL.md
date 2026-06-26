---
version: "1.0.0"
name: douyin-video-to-report
description: "抖音视频链接 → 完整图文报告。自动完成：绕过验证抓取视频 → 下载 → 音频提取 → 语音转文字 → 炫酷HTML报告 → 飞书发送。触发词：抖音视频总结、抖音视频分析、这个视频说了什么、总结这个视频"
override-tools:
  - douyin_report
---

# Douyin Video → Report Pipeline

将抖音视频链接自动转换为可阅读的 HTML 报告，适合需要提炼视频内容的场景。

## 完整工作流程

```
抖音短链 (v.douyin.com/xxx)
    │
    ▼
1. Playwright (headless Chrome)
   - 绕过 JS 验证 / 滑动验证码
   - 提取视频直链
    │
    ▼
2. curl 下载视频 (.mp4)
    │
    ▼
3. ffmpeg 提取音频 (.mp3)
    │
    ▼
4. miaoda-studio-cli speech-to-text
   - 中文普通话识别
   - 100% 转录
    │
    ▼
5. 生成炫酷 HTML 报告
   - 深色渐变主题
   - 核心数据卡片
   - 洞察总结
   - 完整转录（可展开）
   - Ctrl+P 可打印成 PDF
    │
    ▼
6. 飞书附件发送给用户
```

## 核心脚本

脚本位于：`/home/gem/workspace/agent/skills/douyin-video-to-report/douyin_pipeline.py`

### 使用方式

```bash
# 方式一：直接运行（传入抖音URL）
python3 /home/gem/workspace/agent/skills/douyin-video-to-report/douyin_pipeline.py "https://v.douyin.com/xxxxx"

# 方式二：分步执行（见下方分步说明）
```

## 分步执行命令

### Step 1：提取视频直链
```python
# douyin_fetch.py - Playwright 提取视频 URL
import asyncio
from playwright.async_api import async_playwright

async def get_video_url(douyin_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            '--no-sandbox', '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
        ])
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            viewport={'width': 390, 'height': 844},
            locale='zh-CN',
        )
        page = await context.new_page()
        await page.goto(douyin_url, timeout=30000, wait_until="networkidle")
        await asyncio.sleep(3)
        # 从 video 元素获取直链
        video_info = await page.evaluate("""
            () => {
                const v = document.querySelector('video');
                if (v && v.src) return v.src;
                return null;
            }
        """)
        await browser.close()
        return video_info
```

### Step 2：下载视频
```bash
curl -L -o /tmp/douyin_video.mp4 "视频直链" \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" \
  --max-time 60 -s
```

### Step 3：提取音频
```bash
ffmpeg -i /tmp/douyin_video.mp4 -vn -acodec libmp3lame -q:a 2 /tmp/douyin_audio.mp3 -y
```

### Step 4：语音转文字
```bash
miaoda-studio-cli speech-to-text --file /tmp/douyin_audio.mp3 --lang zh --output text
```

### Step 5：生成报告
使用 `miaoda_coding` 或直接使用 `report_generator.py`（见下方）

## 依赖环境

| 依赖 | 安装命令 |
|------|---------|
| Playwright | `pip install playwright && python3 -m playwright install chromium` |
| ffmpeg | 系统自带或 `apt install ffmpeg` |
| yt-dlp | `pip install yt-dlp` |
| miaoda-studio-cli | 系统自带 |

## 关键经验

1. **必须用 Playwright headless Chrome**，不能用 requests/httpx，抖音会拦截
2. **移动端 UA 更容易绕过**，用 iPhone UA 而非桌面 Chrome
3. **视频直链从 `document.querySelector('video').src` 获取**，不要从 network 请求里找
4. **下载视频时必须加 User-Agent header**，否则 403
5. **飞书附件发送**：文件必须放在 `/home/gem/workspace/agent/workspace/` 或 `/tmp/openclaw/` 目录

## 报告模板结构

- Hero：标题 + 视频元信息
- 数据卡片：关键数字高亮
- 洞察区：6个核心发现卡片
- 对比表：进门 vs 留存因素
- 案例区：引用高亮
- 行动指南：5项建议
- 完整转录：可展开/收起

## 相关工具

- `miaoda-studio-cli speech-to-text`：音频转文字
- `miaoda-studio-cli doc-parse`：文档解析
- `miaoda-coding`：生成可视化报告
