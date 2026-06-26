---
name: csdn-article-publish
description: 将 Markdown 文章通过用户目录浏览器会话发布到 CSDN。支持保存草稿、预览排版、人工确认发布；默认保持浏览器打开并复用登录态。
---

# CSDN 文章发布（会话保持版）

## 核心要求

- 使用用户目录浏览器会话（Edge/Chrome），复用已有登录态。
- 默认不关闭浏览器、不丢失上一次会话。
- 不硬编码文章路径、标题、文章 ID、标签等业务信息；全部参数化。
- 发布流程内置“页面排版模块”，默认在回填编辑器前执行。

## 目录结构

```text
csdn-article-publish/
├── SKILL.md
├── skill-config.json
├── scripts/
│   └── csdn_browser_publish.js
└── docs/
    └── usage.md
```

## 何时调用

- 用户要求“发布到 CSDN”“保存到 CSDN 草稿”“先预览再发布”。
- 用户明确要求保持浏览器会话、复用登录态。

## 脚本说明（参数化，无硬编码）

脚本：`scripts/csdn_browser_publish.js`

- `--mode draft`：打开发布弹窗并保存草稿
- `--mode draft-preview`：保存草稿后关闭弹窗并切换预览
- `--mode publish`：打开发布弹窗并提交发布

通用参数：

- `--file <markdown文件路径>`：必填
- `--title <标题>`：可选，默认用文件名
- `--article-id <文章ID>`：可选；传入则打开指定草稿
- `--browser edge|chrome`：可选，默认 `edge`
- `--profile-dir <浏览器用户目录>`：可选；不传则按浏览器类型取默认用户目录
- `--keep-open true|false`：可选，默认 `true`
- `--typeset true|false`：可选，默认 `true`
- `--typeset-profile readable|compact`：可选，默认 `readable`
- `--page-typeset true|false`：可选，默认 `true`（页面层排版：尝试关闭 AI 助手侧栏并进入预览态）

二维码文末策略（从配置文件读取）：

- 从 `skill-config.json` 的 `env` 字段读取：
  - `CSDN_VERTICAL_QR_IMAGE_URL`
  - `CSDN_VERTICAL_QR_DESCRIPTION`（可选）
- 若配置不存在，则自动追加“请添加公众号二维码图片及相关说明”的占位提示。

排版模块策略（回填编辑器前）：

- 统一标题/列表与正文空行
- 统一代码块前后留白
- 压缩异常连续空行
- `readable`：偏可读性（推荐）
- `compact`：偏紧凑展示

页面排版模块策略（浏览器页面层）：

- 自动尝试关闭 AI 助手侧栏，扩大阅读区域
- 自动切换到预览态，便于发布前检查
- 结果 JSON 返回 `pageTypesetActions`

## 推荐执行顺序

1. `draft-preview`：保存草稿并预览排版
2. 需要时重复 `draft-preview` 做排版迭代
3. 最终执行 `publish` 或让用户人工确认后发布

## 异常处理

- 若出现 `ProcessSingleton`/`SingletonLock`：说明浏览器目录被占用。
  - 优先复用已打开会话，不强制重启。
  - 仅在用户同意下重启浏览器恢复可控会话。
- 若页面元素变更导致按钮失效：更新选择器，不要写死 `ref`。

## 结果输出

- 每次执行输出 JSON 结果（按钮命中、当前 URL、截图路径）。
- 输出会包含二维码变量状态（`wechatQrConfigured`）。
- 截图默认保存到当前工作目录：`csdn_<mode>_result.png`。
