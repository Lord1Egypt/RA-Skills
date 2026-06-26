# wechat-formatter

`wechat-formatter` 是微信排版 skill。它把 Markdown 主稿渲染成微信公众号可用 HTML；如果主稿旁边有 `writing-pack.json`，它还会自动挂上摘要、金句和 CTA。

## 这个 skill 能做什么

- 把 Markdown 渲染成微信 HTML
- 自动消费 `*-writing-pack.json`
- 输出标准化 `ready/*-wechat.html`
- 当高级渲染失败时，自动回退到本地 HTML 渲染
- 产物可继续交给 `wechat-studio` 做预览或人工微调

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

本 skill 没有额外必须安装的第三方 CLI。

## 输入和输出

**输入**

- `content-production/drafts/<slug>-article.md`
- 可选同目录 sidecar：`content-production/drafts/<slug>-writing-pack.json`

**输出**

- `content-production/ready/<slug>-wechat.html`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill wechat-formatter \
  --input content-production/drafts/harness-engineering-一人公司-article.md
```

### 常见上游

- `case-writer-hybrid`
- `humanizer-zh` 清洗后的稿件

## 什么时候用

- 主稿已经定下来，需要转成微信公众号 HTML
- 你希望把摘要、金句、转发语自动附加到版面里
- 你需要一个稳定的 HTML 产物给后续发布或工作台使用

## 注意事项

- 它只负责排版，不负责写稿
- 如果输入已经是 HTML，通常不应再喂给本 skill
- 当前 HTML 质量仍取决于主稿内容和 sidecar 的完整度

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [wechat-formatter-execution-spec.md](../../docs/wechat-formatter-execution-spec.md)
