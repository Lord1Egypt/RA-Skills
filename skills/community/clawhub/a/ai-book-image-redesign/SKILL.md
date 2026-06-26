---
name: AI 书稿图片重设计
description: >
  将用户提供的 HTML/前端原型整理成一个可复用的网页应用 skill。适用于用户说“把这段 HTML 做成 skill”
  “把这个网页原型封装成 skill”“生成一个可落地的静态页面 skill”“把图片重设计工具做成 skill”等场景。
  该 skill 会把现成前端页面模板落到本地，默认输出为静态 HTML，并支持让最终用户自行填写 API URL 和 API Key。
user-invocable: true
metadata: {"openclaw":{"emoji":"🖼️","skillKey":"ai-book-image-redesign"}}
---

# AI 书稿图片重设计 🖼️

把现成的网页原型（尤其是单文件 HTML/CSS/JS）整理成一个可复用 skill。

## 适用场景

当用户说这些话时使用：

- 「把这段 HTML 做成 skill」
- 「把这个网页原型封成 skill」
- 「做一个静态网页工具 skill」
- 「把这个 AI 图片重设计页面做成 skill」
- 「把前端 demo 打包成可复用 skill」

## 默认工作方式

1. **优先保留用户原始界面风格**，不要擅自大改视觉结构
2. **先做成本地可运行版本**，再考虑发布或接 API
3. **不在模板里写死密钥**，改为让最终用户自行输入 API Base URL 和 API Key
4. **静态资源放到 `assets/`**，便于直接复制、部署、二次修改
5. **如需脚本化初始化**，用 `scripts/` 放置生成脚本

## 目录说明

- `assets/index.html`：可直接打开的静态页面模板
- `assets/vercel.json`：Vercel 静态部署配置
- `scripts/setup.sh`：把模板复制到目标目录，快速落地
- `scripts/export-static.sh`：导出可直接部署到 Vercel / 静态站的文件

## 使用方式

### 1）快速落地页面

执行：

```bash
bash scripts/setup.sh /目标目录
```

默认会输出：

```text
/目标目录/
└── index.html
```

### 1.1）导出可部署到 Vercel / 静态站的版本

执行：

```bash
bash scripts/export-static.sh /目标目录
```

会输出：

```text
/目标目录/
├── index.html
└── vercel.json
```

部署方式：

- **Vercel**：把该目录导入 Vercel，或在目录内执行 `vercel`
- **静态站托管**：直接上传 `index.html`（以及 `vercel.json` 可忽略）

### 2）页面中的 API 连接方式

当前模板改成由最终用户自行填写：

- API Base URL
- API Key
- Model 名称
- 可选的异步轮询路径（例如 `/v1/tasks/{id}`）

填写后即可直接使用。页面默认请求：

```text
POST {API_BASE_URL}/v1/images/generations
```

支持能力：

1. **同步返回结果图**
2. **异步返回任务 ID 后自动轮询**
3. **多图批量处理（最多 10 张）**
4. **自定义 model 名称**

并优先兼容这些返回字段：

- `data[0].url`
- `data[0].b64_json`
- `images[0].url`
- `result.url`
- `image_url`
- `b64_json`

任务 ID 兼容字段：

- `task_id`
- `taskId`
- `id`
- `data.id`

适合快速验证页面交互和图片生成流程。

**但正式商用仍推荐：**

- 后端代理
- 环境变量注入
- 服务端签名中转

避免在浏览器前端长期直接暴露密钥。

## 修改建议

如果用户后续要求：

- 批量处理多张图
- 登录与额度系统
- 支付升级
- 服务端任务轮询
- OSS / S3 图片存储

优先在现有模板基础上增量改，而不是推倒重写。
