# 排错与常见问题

## 安装阶段

### 上游 install.sh 失败

```bash
# 1. 单独装 Python 依赖
pip3 install -r requirements.txt --user

# 2. 单独装 Playwright
playwright install chromium

# 3. 检查
./check_env.py
```

### MCP 注册后 WorkBuddy 不识别

| 现象 | 排查 |
|---|---|
| 重启后没看见新 MCP | 检查 `~/.workbuddy/mcp.json` 语法（缺逗号、引号） |
| 看见了但点 Trust 报错 | 检查 server.py 路径是绝对路径 |
| Trust 后调用报错 | 跑 `python3 <server.py>` 看是否能独立启动 |

## 抓取阶段

### 微信公众号 403

```
[Step 1] 抓取失败
  原因：cookie 失效 / 反爬识别
  解决：
    a) 从微信电脑版扫码登录后导出 cookie
    b) 多账号轮转（上游支持 cookie 池）
    c) 最后兜底：让用户复制粘贴
```

### NotebookLM 上传失败

| 错误 | 解决 |
|---|---|
| `not signed in` | 重跑 `notebooklm login`（获取 cookies 供 Playwright 使用） |
| CLI `source add-text` 假成功/HTTP 400 | **CLI 上传已废弃**，改用 Playwright `upload-text` |
| `quota exceeded` | NotebookLM 免费版每天 source 数有限，等待重置 |
| `source too long` | 拆分文档（按章节切片） |
| 一直转圈 | 网络问题，见 china-network.md |

### NotebookLM 生成失败

| 现象 | 解决 |
|---|---|
| CLI `generate` HTTP 400 | **CLI 生成已废弃**，改用 Playwright `generate` |
| 点击后无反应（audio/video/report） | 24h 滚动窗口配额已满，等次日或换账号 |
| 点击后无反应（mindmap/flashcards/quiz/presentation/infographic/datatable） | 该 notebook 今天已生成过此类型，新建 notebook 即可重置 |
| 生成超时（>2min） | 正常，audio/video/report/presentation/infographic 生成较慢，后台仍在运行 |

### Get笔记 转写卡住

```
> 等待回调超过 10 分钟
解决：
  1. 确认 GETNOTE_API_KEY 有效（curl 测试）
  2. 检查音频 URL 是否对 Get笔记可达（防盗链）
  3. fallback：本地 Whisper.cpp
```

## 生成阶段

### PPT 渲染质量差 / 失败

| 现象 | 解决 |
|---|---|
| python-pptx 生成单调（纯文字框） | 改用 `anthropics/skills@pptx` 的 `html2pptx` 工作流 |
| html2pptx 渲染失败（Playwright 超时） | fallback 到 `aktsmm/powerpoint-automation`（content.json + 模板） |
| 模板填充后格式错位 | 检查 content.json 字段是否与模板 placeholder 匹配 |
| 输出文件损坏（0 KB） | 检查 gen.js 是否正常 exit，用 `node --check gen.js` 验证语法 |

### PPT Skill 安装失败

| 错误 | 解决 |
|---|---|
| supercent-io 仓库 404 / 私有 | 改用 `igorwarzocha/powerpoint`（html2pptx 方案）或 `aktsmm/powerpoint-automation` |
| googleworkspace/cli 只能创建 Google Slides | 不适用于本地 PPT 场景，跳过 |

### html2pptx 依赖问题

```bash
# 检查 Playwright 是否正常
node -e "require('playwright')" && echo "✅ playwright ok"

# 检查 Sharp（html2pptx 内部依赖）
node -e "require('sharp')" && echo "✅ sharp ok"

# 全局安装（如果缺失）
npm install -g playwright @playwright/test
npx playwright install chromium
npm install -g sharp
```

### NotebookLM 生成质量调优

| 现象 | 解决 |
|---|---|
| Audio Overview 出现英文 | source 中混入英文，纯化 source |
| 音频时长不可控 | 在自定义 prompt 中明确要求"~15 分钟" |
| 音色固定 | NotebookLM 暂不支持自定义音色，需 fallback 到 ChatTTS |
| Mind Map JSON 太深 | NotebookLM 的 Mind Map 偶尔会生成 6-7 层深的树。本 Skill 默认裁剪到 4 层 |
| Presentation 超时 | 演示文稿生成通常 >2min，属正常，后台仍在运行 |

## 落地阶段

### 写入 IMA 失败

| 错误 | 解决 |
|---|---|
| `unauthorized` | 重新跑 IMA OAuth 授权 |
| 内容截断 | IMA Notes 单笔记上限 ~50KB，长文要分段 |
| 图片不显示 | IMA 仅支持 https 网络图片，本地图片需先上传图床 |

### 写入飞书失败

参考 `lark-master` 的排错文档。常见：

- App 权限不足 → 飞书后台勾选 docs / drive 权限
- 路径不存在 → 先创建目标文件夹

## PPT 生成工具链（场景 5 专项）

> 详见 `scenarios/05-shipinhao-to-ppt.md` 的「渲染选择」章节。

| 工具 | 用途 | 调用方式 |
|---|---|---|
| `anthropics/skills@pptx` | 专业设计 PPT | `html2pptx.js`（Playwright + PptxGenJS） |
| `aktsmm/powerpoint-automation` | 快速模板 PPT | `python create_from_template.py template.pptx content.json output.pptx` |
| `igorwarzocha/powerpoint` | html2pptx 备选 | 同 html2pptx.js 路径 |

### 快速选择决策树

```
PPT 场景？
├─ 需要专业设计感、自定义布局
│   → anthropics/skills@pptx（html2pptx）
│   → 依赖：Node.js + Playwright + Sharp（全局已装）
│
├─ 标准格式、快速出稿、批量生成
│   → aktsmm/powerpoint-automation（content.json + 模板）
│   → 依赖：Python + python-pptx（已装）
│
└─ 程序员、版本化管理
    → Marp / Slidev（Markdown → PPTX/PDF）
```

### content.json 格式（aktsmm 用）

```json
{
  "title": "PPT 标题",
  "slides": [
    {
      "title": "第 1 页标题",
      "content": ["要点 1", "要点 2", "要点 3"],
      "speaker_notes": "讲者备注"
    }
  ]
}
```

### html2pptx 调试技巧

```bash
# 1. 检查 HTML 是否语法正确
node --check gen.js

# 2. 单页测试渲染
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + process.cwd() + '/slides/slide01.html');
  await page.screenshot({ path: 'debug.png' });
  await browser.close();
})();
"

# 3. 检查 pptx 文件是否可打开
python3 -c "from pptx import Presentation; prs = Presentation('output.pptx'); print(f'OK: {len(prs.slides)} slides')"
```

## 网络问题

完整指引见 `china-network.md`。快速诊断：

```bash
# 1. 能否访问 Google
curl -I https://www.google.com

# 2. 能否访问 NotebookLM
curl -I https://notebooklm.google.com

# 3. 能否访问微信公众号
curl -I https://mp.weixin.qq.com

# 4. 能否访问财新
curl -I https://www.caixin.com
```

按场景启停代理。

## 反馈

遇到本文档没覆盖的问题：
- 在 Skill Hub 评论区反馈
- 或开 GitHub Issue（仓库地址在 SKILL.md）
