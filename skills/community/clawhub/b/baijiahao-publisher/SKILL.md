---
name: baijiahao-browser
version: 2.0.0
description: 基于 OpenClaw 内置浏览器的百家号发布技能。打开发布页、扫码登录、填标题/正文、上传封面图、发布，全自动。零依赖 Python，任意 OpenClaw 环境均可运行。
author: Maynor
license: MIT
tags: ["baijiahao", "publish", "browser", "automation"]
language: agent
entry: SKILL.md
requirements: []
user-invocable: true
metadata: '{"openclaw":{"skillKey":"baijiahao-browser","requires":{"browser":true}}}'
---

# 百家号发布（浏览器版）

## 概述

本 Skill 使用 OpenClaw 内置浏览器完成百家号文章发布，**无需 Python/Playwright**，任意 OpenClaw 环境均可运行。

## 完整工作流

### Step 1 — 启动浏览器

```javascript
browser(action="start", profile="openclaw")
```

### Step 2 — 打开发布页

```javascript
browser(action="open", profile="openclaw", url="https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1")
```

### Step 3 — 处理登录

检查页面是否有登录弹窗：
- **如果有登录对话框**：请用户在浏览器中扫码登录（百家号APP或百度APP）。登录成功后告知助手。
- **如果页面已登录**：直接进入 Step 4。

### Step 4 — 关闭新手提示

按 Escape 或点击「知道了/关闭」按钮，关闭常见新手提示弹窗。

### Step 5 — 填入标题

1. `browser(action="snapshot")` 获取当前页面元素
2. 找到标题输入框（placeholder 含"请输入标题"），点击激活
3. `browser(action="act", request={"kind": "type", "ref": "<标题元素ref>", "text": "<文章标题>"})`

### Step 6 — 填入正文

正文在 iframe 内，需要通过 iframe 操作：
1. 点击 iframe 中的段落元素激活编辑区
2. `browser(action="act", request={"kind": "type", "ref": "<正文元素ref>", "text": "<正文内容>"})`
3. 支持分段输入（每段后换行）

### Step 7 — 设置封面（核心步骤）

封面必须上传图片文件，步骤如下：

1. **复制图片到上传目录**：
   将用户提供/AI生成的封面图复制到 `C:\Users\Administrator\AppData\Local\Temp\openclaw\uploads\cover.jpg`

2. **打开封面上传弹窗**：
   点击「选择封面」按钮

3. **点击「本地上传」触发文件选择**：
   通过 `browser(action="snapshot")` 找到正文/本地上传 tab

4. **上传文件**：
   ```javascript
   browser(action="upload", paths=["C:\\Users\\Administrator\\AppData\\Local\\Temp\\openclaw\\uploads\\cover.jpg"])
   ```

5. **确认封面**：
   点击「确定」按钮应用封面

**自动生成封面（可选）**：
若用户未提供封面图，可调用 `image_generate` 生成后保存再用上述方式上传。

### Step 8 — 勾选 AI 声明

在右侧面板找到「采用AI生成内容」复选框并勾选。

### Step 9 — 发布

1. 点击「发布」按钮
2. 若出现验证/提示，等待处理完成
3. 页面显示「文章发布成功」即为完成

---

## 关键实现细节

### 文件上传流程（必须严格按顺序）

```
1. browser(action="snapshot") → 找到封面上传弹窗的 ref
2. browser(action="act", kind="click", ref="<上传区域ref>") → 激活文件 input
3. 复制图片到: C:\Users\Administrator\AppData\Local\Temp\openclaw\uploads\cover.jpg
4. browser(action="upload", paths=["C:\\Users\\Administrator\\AppData\\Local\\Temp\\openclaw\\uploads\\cover.jpg"])
5. browser(action="snapshot") → 确认图片已出现在预览中
6. 点击「确定」
```

### 封面弹窗判断

封面弹窗有两种状态：
- **第一次打开**：tab 显示「正文/本地上传」
- **已上传过一张图后**：tab 显示「正文/本地上传(1)」

两种状态下的「确定」按钮 ref 不同，需 snapshot 确认后再点。

### Cookie 注入（备选方案）

如需绕过扫码登录，可尝试注入 cookie：

```javascript
browser(action="act", request={
  "kind": "evaluate",
  "fn": "document.cookie='<cookie string>'"
})
```

但百家号 cookie 有效期短，建议优先使用扫码登录。

### iframe 内操作

正文编辑器在 iframe 内，`browser(action="snapshot")` 的 ref 前缀为 `f37e` 开头。

---

## 调用约定

当用户提供以下任意意图时，使用本 Skill：
- 「帮我发布百家号文章」
- 「把 xxx 发布到百家号」
- 「上传图片发布百家号」
- 「生成一篇 xxx 的文章并发布」

Agent 应自动解析参数：
- **标题**：从用户请求或生成内容中提取
- **正文**：用户提供的文本或 AI 生成的完整文章
- **封面**：用户提供图片路径，或用 `image_generate` 生成

---

## 发布通道状态码

| 状态 | 含义 |
|------|------|
| 显示「文章发布成功」 | 发布完成 |
| 显示「内容已存入草稿」 | 存草稿成功，需人工确认后发布 |
| 显示「请添加封面」 | 封面未上传，需补封面后发布 |
| 显示「提交成功，正在审核中」 | 已提交审核 |

---

## 文件结构

```
baijiahao-browser/
├── SKILL.md          # 本文件
├── _meta.json        # 元数据
└── package.json      # 包信息
```
