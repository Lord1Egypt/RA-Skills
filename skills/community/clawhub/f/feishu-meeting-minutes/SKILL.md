---
name: feishu-meeting-minutes
version: 1.2.0
description: 飞书会议纪要自动生成工具。从飞书妙记链接、minute token 或现成 transcript 文件生成结构化中文会议纪要，并可选导出 PDF、上传回飞书云空间。适用于用户提供飞书妙记链接要求整理会议纪要、要求将逐字稿转正式文档、或希望把会议录音对应 transcript 快速整理成可分发纪要的场景。
---

# 飞书会议纪要生成器

优先使用内置 Node 脚本，不要手写临时 shell 管道。

## 工作流

1. 从飞书妙记 URL 或原始 `minute_token` 中提取 token。
2. 使用 `lark-cli` 拉取会议基础信息。
3. 在独立 session 目录中下载 transcript。
4. 自动生成结构化 Markdown 会议纪要。
5. 可选使用 `pandoc + xelatex` 输出 PDF。
6. 可选将 PDF 上传回飞书云空间。

## 运行方式

从飞书妙记直接生成纪要：

```bash
node scripts/generate_minutes.mjs --minute-url "https://example.feishu.cn/minutes/obcnqx9afzs2xxmjy6g772nq" --output-dir "./output"
```

使用原始 token：

```bash
node scripts/generate_minutes.mjs --minute-token "obcnqx9afzs2xxmjy6g772nq" --output-dir "./output"
```

基于已有 transcript 文件生成：

```bash
node scripts/generate_minutes.mjs --transcript-file "./transcript.txt" --title "项目周会" --minute-token "obcnqx9afzs2xxmjy6g772nq" --output-dir "./output"
```

导出 PDF 并上传：

```bash
node scripts/generate_minutes.mjs --minute-token "obcnqx9afzs2xxmjy6g772nq" --output-dir "./output" --pdf --upload
```

## 依赖

- 需要 `node`
- 拉取妙记与上传文件时需要 `lark-cli`
- 使用 `--pdf` 时需要 `pandoc` 与 `xelatex`
- 建议安装中文字体 `Noto Sans CJK SC`

## 所需权限

拉取妙记与 transcript 前，需要这些 scope：

- `minutes:minutes:readonly`
- `minutes:minutes.artifacts:read`
- `minutes:minutes.transcript:export`
- `vc:note:read`

上传 PDF 前，还需要：

- `drive:file:upload`

授权示例：

```bash
lark-cli auth login --scope "minutes:minutes:readonly minutes:minutes.artifacts:read minutes:minutes.transcript:export vc:note:read drive:file:upload"
```

## 产物

- `meeting_minutes_YYYYMMDD_<slug>_<token>.md`
- `meeting_minutes_YYYYMMDD_<slug>_<token>.pdf`（仅 `--pdf`）

## 注意事项

- 脚本只会在它自己创建的 session 目录内搜索 transcript，避免误用历史文件。
- 会议纪要为结构化自动整理结果，分发前应结合原始 transcript 复核。
- 如需调整输出格式，按需读取 `references/template.md`。
