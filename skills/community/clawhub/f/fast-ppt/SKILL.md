---
name: fast-ppt
description: 把 PDF/文档做成可编辑 PPTX（云端处理），完成后返回 ppt.siping.me 下载链接。上传前须告知用户文件会传到第三方服务器。PDF 支持 AI 主题或仅转换。触发：改成ppt、做成幻灯片、仅转换、fast-ppt。
user-invocable: true
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["curl"]},"homepage":"https://ppt.siping.me"}}
---

# Fast PPT

用户要 **文件** → 调用 pingPPT API（Fast PPT skill 后端）→ 回复 **`https://ppt.siping.me/...` 下载链接**（不是本地路径、不是 API IP）。

---

## 隐私与数据外传（Agent 必读）

**本 skill 会把用户文件完整上传到第三方云端服务处理，内容会离开用户本机。** 在用户第一次上传前，或文件可能含敏感信息时，**必须先告知并取得同意**，再调用 API。

**须向用户说明的要点（用 plain language，不要省略）：**

| 项 | 说明 |
|----|------|
| **处理位置** | 文件上传到 **pingPPT 云端**（API：`47.103.80.109`；用户可见下载域名：`ppt.siping.me`），在远程服务器解析、生成 PPTX，**不是本地离线转换** |
| **谁可接触** | 文件与生成结果由 **siping.me 运营方** 的服务器处理；下载链接经 `ppt.siping.me` 对外提供 |
| **AI 主题模式** | 默认模式会把文档内容 **送入 LLM** 按主题重排；**仅转换**（`convert_only`）不走 LLM，但仍需上传 PDF 到云端 |
| **保留时间** | 上传文件与导出 PPTX 通常在服务器上 **约 24 小时内清理**（运维策略，**不保证**合规级留存期限；勿当作长期归档） |
| **不适合** | 涉密、未公开商业、个人身份/医疗/财务、受监管或合同禁止外传的文档 —— **默认不要上传**；若用户坚持，须明确风险提示后再执行 |

**Agent 执行前检查：**

1. 文件名/用户描述若含「机密 / 内部 / 合同 / 客户资料 / 身份证 / 病历」等 → **先问**「该文件将上传到 siping.me 云端处理，是否继续？」
2. 用户未确认 → **不要上传**；可建议本地工具或脱敏后再试
3. 用户已确认 → 再执行下方 curl 流程
4. 回复用户时 **不要** 声称「完全本地」「不上传服务器」

**鉴权（当前）**：API **暂不要求** `PINGAI_PPT_API_KEY`，curl 无需 `Authorization` 头。勿向用户索要密钥。

**两套地址（必须分清）**：

| 用途 | 地址 |
|------|------|
| Agent 调 API（上传/轮询/内部下载） | `http://47.103.80.109:8080` |
| **发给用户的下载链接** | 轮询 `done` 后 JSON 里的 **`download_url`**（`https://ppt.siping.me/v1/jobs/{id}/download`） |

勿把 `47.103.80.109`、相对路径 `/v1/jobs/...` 或本地 `.pptx` 路径发给用户。

---

## 用户怎么说

```text
把 report.pdf 做成 PPT，主题 kubernetes_blueprint_2026
```

```text
把 /path/to/doc.pdf 做成幻灯片，主题 cangzhuo
```

```text
把 手册.pdf 仅转换 成 PPT
```

```text
把 contract.pdf 保持原样转成可编辑幻灯片
```

```text
有哪些 PPT 主题？
```

问主题 → 发 [ppt.siping.me](https://ppt.siping.me) 或贴下方主题表。

---

## 从用户消息提取

| 项 | 规则 |
|----|------|
| 文件 | PDF / PPTX / DOCX / MD / TXT 等工作区路径 |
| `theme` | 用户写的主题 **id**；未写则用 `kubernetes_blueprint_2026`（**仅转换模式可省略**） |
| `mode` | 见下方 **PDF 处理模式** |

---

## PDF 处理模式

| 模式 | API `mode` | 适用 | 效果 |
|------|------------|------|------|
| **AI 主题排版**（默认） | 不传或 `theme` | PDF / Word / MD 等 | 转 Markdown → LLM 按主题重排幻灯片 |
| **仅转换** | `convert_only` | **仅 PDF** | 每页 PDF → 一页 PPT；**背景/图片保留**，**文字可编辑**；不用 LLM、不用主题 |

用户说法 → `mode` 映射：

- **仅转换**、**convert only**、**保持原样**、**原样转换**、**不要主题** → `convert_only`
- 其余 → 默认 AI 主题排版

**仅转换** 技术要点（内部参考，勿原样甩给用户）：

- 整页渲染为背景（redact 去掉背景图里的文字，避免重影）
- cover 缩放铺满 16:9，裁切溢出，避免左右白边
- 文字按 PDF 坐标叠加为可编辑层

**局限**：扫描版 PDF（纯图片无文字层）暂不支持 OCR；复杂多栏版式可能有轻微偏差。

---

## 执行（上传 → 轮询 → 下载）

**0. API 地址**

```bash
API="${PINGAI_PPT_API_URL:-http://47.103.80.109:8080}"
```

**1. 上传** → 记录 `job_id`

AI 主题排版（默认）：

```bash
THEME="kubernetes_blueprint_2026"
FILE="/path/to/source.pdf"
OUT="/path/to/output.pptx"

curl -sS \
  -F "file=@$FILE" \
  -F "theme=$THEME" \
  "$API/v1/jobs"
```

PDF 仅转换：

```bash
curl -sS \
  -F "file=@$FILE" \
  -F "mode=convert_only" \
  "$API/v1/jobs"
```

`mode` 也接受：`仅转换`

**2. 轮询** — 每 15–30 秒一次，最长 30 分钟，直到 `status` 为 `done`

```bash
curl -sS "$API/v1/jobs/$JOB_ID"
```

`done` 时响应示例：

```json
{
  "job_id": "job_abc123",
  "status": "done",
  "download_url": "https://ppt.siping.me/v1/jobs/job_abc123/download"
}
```

| status | 处理 |
|--------|------|
| `queued` / `processing` | 继续等 |
| `done` | 取 `download_url` 回复用户；可选再 curl 下载到本地 |
| `failed` | 用简单中文说明 `error` |

**3. 交付给用户**

- **必须**：把上一步 JSON 里的 **`download_url` 原样发给用户**（可点击下载 PPT）
- **可选**：Agent 如需本地副本，用 API 直连下载（勿把此 URL 给用户）：

```bash
curl -sS -o "$OUT" "$API/v1/jobs/$JOB_ID/download"
```

---

## 回复用户

**规则**：只给 **下载链接** + 简短说明；链接用 API 返回的 `download_url`，不要自己拼。

**首次成功交付时**（若此前未说明），补一句数据提示，例如：

> 说明：你的文件曾在 siping.me 云端处理；下载链接约 24 小时内有效，请勿用于长期存放敏感原件。

AI 主题排版：

> 你的 PPT 已生成。  
> 主题：Kubernetes 蓝图 2026  
> 下载：https://ppt.siping.me/v1/jobs/job_abc123/download  
> 主题预览：https://ppt.siping.me/viewer.html?theme=kubernetes_blueprint_2026  

仅转换：

> 你的 PPT 已生成（仅转换：保留原页背景，文字可编辑）。  
> 下载：https://ppt.siping.me/v1/jobs/job_abc123/download  

处理中：

> 正在生成 PPT，大约还需几分钟，完成后我会发下载链接。

**禁止**出现在用户回复里：`job_id`、API IP、`/v1/jobs/...` 相对路径、本地文件路径、报错 stack trace。

---

## 内置主题（19 套）

`theme=` 填 **id**。预览：`https://ppt.siping.me/viewer.html?theme=<id>`

| id | 名称 |
|----|------|
| `brutalist_ai_newspaper_2026` | AI 行业报纸 2026 |
| `building_effective_agents` | 构建高效 Agent |
| `cangzhuo` | 藏拙 |
| `fashion_weekly_digest` | 时尚美学周鉴 |
| `general_dark_tech_claude_code_auto_mode` | Claude Code 自动模式 |
| `glassmorphism_demo` | 毛玻璃风格演示 |
| `global_ai_capital_2026` | 全球 AI 资本 2026 |
| `high_rise_renewal` | 高层住宅「主动再生」 |
| `home_design_trends_2026` | 2026 家居设计趋势 |
| `image_text_showcase` | 图文范式展示 |
| `indie_bookstore_zine_guide` | 独立书店 Zine 指南 |
| `kimsoong_loyalty_programme` | 锦上客户忠诚计划 |
| `kubernetes_blueprint_2026` | Kubernetes 蓝图 2026（**默认**） |
| `lin_huiyin_architect` | 林徽因：当之无愧的建筑师 |
| `lin_huiyin_architect_revised` | 重识林徽因建筑师身份 |
| `liziqi_plant_dye_colors` | 李子柒植物染色彩 |
| `pritzker_2026` | 普利兹克奖 2026 |
| `sugar_rush_memphis` | Sugar Rush 孟菲斯音乐节 |
| `swiss_grid_systems` | 瑞士网格系统 |

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `PINGAI_PPT_API_URL` | 可选，默认 `http://47.103.80.109:8080`（Agent 调 API 用） |
| `PINGAI_PPT_PUBLIC_URL` | 可选，默认 `https://ppt.siping.me`（返回给用户的下载链接前缀） |
| `PINGAI_PPT_API_KEY` | **当前不需要**；日后服务端开启鉴权时再配 |

---

## 出错时（内部处理，勿原样甩给用户）

| 现象 | 处理 |
|------|------|
| `401` / `403` | 服务端已开启鉴权，需配置 Key |
| `503` | 服务未就绪 |
| 超时 | 换小文件或稍后重试 |
| `convert_only` + 非 PDF | 提示仅转换模式只支持 PDF |

对用户：生成失败，请稍后再试 + 简短原因。
