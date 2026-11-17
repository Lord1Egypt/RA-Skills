# concept-radar

渠道无关、周期无关的概念发现 Skill。它从单个 URL 或作者池抓取内容，使用来源 revision、
内容哈希、语义哈希与概念指纹去重，并生成带证据的 Markdown/JSON 概念卡片。

## 快速开始

在仓库根目录运行：

```bash
python3 .trae/skills/concept-radar/scripts/concept_radar.py doctor
python3 .trae/skills/concept-radar/scripts/concept_radar.py scan --url https://example.com/article
```

阅读 `.trae/concept-radar/runtime/candidates.json` 后，按
`examples/selection.example.json` 生成 selection，再运行：

```bash
python3 .trae/skills/concept-radar/scripts/concept_radar.py \
  validate-selection \
  --selection /path/to/selection.json
```

默认产物：

- `.trae/concept-radar/runtime/concept-radar.md`
- `.trae/concept-radar/runtime/concept-radar.json`

## 作者池

配置沿用 `.trae/concept-radar/authors.yaml`。通用配置示例见
`config/authors.example.yaml`。当前支持 RSS/Atom 和 GitHub Gists：

```bash
python3 .trae/skills/concept-radar/scripts/concept_radar.py scan --mode author-pool
```

## 可选发布

默认流程不需要飞书，也不会发送消息。只有用户明确要求发布时运行：

```bash
python3 .trae/skills/concept-radar/scripts/concept_radar.py doctor --channel feishu
python3 .trae/skills/concept-radar/scripts/concept_radar.py publish --channel feishu
```

发布失败不会伪造 `published` 状态；只有 CLI 成功且返回 `ok: true` 与 message_id 后才提交。

## 测试

```bash
python3 -m unittest discover -s .trae/skills/concept-radar/tests -v
```

测试覆盖单 URL、Feed、Gist 降级、去重、卡片与证据校验、默认 doctor 无飞书依赖，
以及可选飞书发布的提交条件。

## 发布

发布包应包含 Skill 指令、脚本、references、config、examples 和 tests；不得包含运行状态、
抓取正文、凭证、缓存或生成结果。详见 `RELEASE.md` 与 `.skillignore`。
