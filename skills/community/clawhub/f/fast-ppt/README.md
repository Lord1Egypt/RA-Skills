# Fast PPT · OpenClaw Skill

把 **PDF / 文档** 做成 **可编辑 PPTX**。主题样板：[ppt.siping.me](https://ppt.siping.me)

---

## 重要：隐私与云端处理

**使用本 skill 即表示你把文件上传到第三方服务器**，内容会离开你的电脑，在远程生成 PPT 后再通过链接下载。

| 你需要知道的 | |
|---|---|
| **处理方** | [siping.me](https://ppt.siping.me) 运营的 pingPPT 云端（非本地转换） |
| **上传内容** | 你提供的 PDF / DOCX / PPT 等 **全文**（含图片、表格、文字） |
| **AI 主题模式** | 默认会把文档内容 **发送给 LLM** 重排幻灯片 |
| **仅转换模式** | 不用 LLM，但仍需 **上传 PDF 到云端** |
| **保留时间** | 上传与生成文件通常在服务器 **约 24 小时** 内清理（非永久存储承诺） |
| **请勿用于** | 机密合同、未公开财报、客户隐私、医疗/身份敏感、任何禁止外传的资料 |

Agent 在上传前应向你确认；若你不希望文件出网，**请不要使用本 skill**。

---

## 两步上手（ClawHub / OpenClaw）

| 步骤 | 做什么 |
|------|--------|
| 1 | 安装 skill（见下方） |
| 2 | 在 OpenClaw 里说：**文件 + 主题**（或 PDF **仅转换**）→ 拿到 **`https://ppt.siping.me/...` 下载链接** |

生成完成后，Agent 会发一条可点击的 **ppt.siping.me 下载链接**（不是本地路径）。

---

## 下载链接示例

```
https://ppt.siping.me/v1/jobs/job_abc123/download
```

浏览器打开即可下载 `.pptx`。主题预览仍在 [ppt.siping.me](https://ppt.siping.me)。

---

## PDF：两种处理方式

| 方式 | 怎么说 | 说明 |
|------|--------|------|
| **AI 主题排版**（默认） | 把 report.pdf 做成 PPT，主题 kubernetes_blueprint_2026 | LLM 按 19 套主题重排内容，适合汇报/演讲 |
| **仅转换** | 把 手册.pdf **仅转换** 成 PPT | **保留原页背景**，**文字可编辑**，一页 PDF → 一页幻灯片；不用选主题 |

Word / Markdown 等仅支持 AI 主题排版；**仅转换** 目前只支持 **PDF**。

---

## 怎么说（复制即用）

```text
把 report.pdf 做成 PPT，主题 kubernetes_blueprint_2026
```

```text
把 强脉冲光临床手记.pdf 仅转换 成 PPT
```

```text
把 季度总结.docx 做成幻灯片，主题 cangzhuo
```

```text
有哪些 PPT 主题？
```

- **文件**：PDF、PPTX、DOCX、Markdown、TXT 等  
- **主题**：在 [ppt.siping.me](https://ppt.siping.me) 浏览；不写主题时默认 `kubernetes_blueprint_2026`（仅转换模式不需要主题）

---

## 预览主题

| | 链接 |
|---|------|
| 全部 19 套 | https://ppt.siping.me/ |
| 默认主题 | https://ppt.siping.me/viewer.html?theme=kubernetes_blueprint_2026 |

完整主题 id 与 API 细节：[SKILL.md](SKILL.md)

---

## 安装

### 从 ClawHub 安装

```bash
openclaw skills install fast-ppt
```

（以 ClawHub 上实际 slug 为准。）

可选环境变量（一般不用改）：

```bash
export PINGAI_PPT_API_URL=http://47.103.80.109:8080   # Agent 调 API
# 用户看到的下载链接默认为 https://ppt.siping.me/...（服务端已配置）
```

当前 API **暂不要求 API Key**，安装后即可使用。

### 本地路径安装（开发）

```bash
openclaw skills install /path/to/pingPPT/skill
```

---

## 发布到 ClawHub（维护者）

- 只发布 `SKILL.md`、`README.md` 等**不含密钥**的文件  
- **禁止**把 `config/defaults.env` 打进包（已加入 `.gitignore` 与 `.clawhubignore`）

---

## Agent 技术说明

[SKILL.md](SKILL.md)
