---
name: doc-export
version: 1.0.0
description: 将对话中解决的问题整理成方案文档，部署到 web 服务器供用户下载
---

# doc-export Skill

将对话中解决的问题整理成方案文档，部署到 web 服务器供用户下载。

## 触发条件

当用户说类似以下内容时触发：
- "整理成文档给我下载"
- "把解决方案整理成md我下载"
- "导出文档"
- "整理成方案文档"
- "生成文档并给我下载链接"

## 执行流程

### 1. 整理文档

- 根据对话内容整理解决方案
- 使用 Markdown 格式
- 包含：问题背景、解决步骤、配置示例、常见问题等
- 保存到 `/root/.openclaw/workspace/docs/` 目录
- 文件命名：`<主题>-guide.md` 或 `<主题>.md`

### 2. 部署到 Web

- 复制文件到 nginx web 目录：`/www/wwwroot/ucloud.demo.binyuli.top/`
- 用户的域名：`ucloud.demo.binyuli.top`（已配置 HTTPS）
- 下载链接格式：`https://ucloud.demo.binyuli.top/<文件名>`

### 3. 告知用户

- 提供下载链接
- **必须提醒用户：下载完告诉我要清理文件**

示例回复：
> 文档准备好了！
>
> **下载链接：** https://ucloud.demo.binyuli.top/xxx-guide.md
>
> 下载完告诉我，我帮你清理文件。

### 4. 清理文件

用户确认下载完成后：
- 删除 `/www/wwwroot/ucloud.demo.binyuli.top/` 下的临时文档
- 保留 `/root/.openclaw/workspace/docs/` 下的原始文档（作为归档）

## 相关配置

- Web 根目录：`/www/wwwroot/ucloud.demo.binyuli.top/`
- 文档归档目录：`/root/.openclaw/workspace/docs/`
- 用户域名：`ucloud.demo.binyuli.top`（HTTPS）

## 注意事项

- 文件名使用英文，避免中文和空格
- 使用 kebab-case 命名（如 `whatsapp-setup-guide.md`）
- 清理时只删 web 目录的文件，保留归档
