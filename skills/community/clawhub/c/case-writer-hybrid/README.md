# case-writer-hybrid

`case-writer-hybrid` 是当前内容主链路里的**主稿生成 skill**。它把结构化 brief 变成公众号长文主稿，并同时产出写作包、审稿轨迹和质量门控结果。

## 这个 skill 能做什么

- 读取 `content-production/inbox/` 里的结构化 brief
- 生成 `drafts/*-article.md` 主稿
- 生成 `writing-pack.md`、`writing-pack.json`、`review-trace.json`
- 在本地跑 `writer -> critic -> humanizer -> judge` 多轮质量回路
- 如果三轮后仍不过线，会中断下游流程并产出质量门控通知

## 安装

### 通用依赖

在仓库根目录执行：

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 验证是否可用

```bash
.venv/bin/python -m skill_runtime.cli list-skills
```

输出中应包含 `case-writer-hybrid`。

## 输入和输出

**输入**

- `content-production/inbox/<slug>-brief.md`
- 需要至少包含 `基础信息`、`核心观点`、`背景与语境`、`论证方向`、`可用案例 / 素材`

**输出**

- `content-production/drafts/<slug>-article.md`
- `content-production/drafts/<slug>-writing-pack.md`
- `content-production/drafts/<slug>-writing-pack.json`
- `content-production/drafts/<slug>-review-trace.json`
- 若不过线：`content-production/published/YYYYMMDD-<slug>-quality-gate.md`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill case-writer-hybrid \
  --input content-production/inbox/20260407-harness-engineering-一人公司-brief.md
```

### 常见下游衔接

- 下游配图：`generate-image`
- 下游排版：`wechat-formatter`
- 默认 workflow：`stage1-pipeline`

## 什么时候用

- 你已经有明确观点、案例和目标读者，需要产出公众号主稿
- 你想把采集来的 brief 变成可继续排版的长文
- 你希望把标题候选、开头、结尾、转发语一并沉淀出来

## 注意事项

- 这是**结构化长文 skill**，不是自由聊天写作器
- brief 越完整，主稿和写作包越稳定
- 如果质量门控失败，先处理主稿问题，再进入 `generate-image` / `wechat-formatter`

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [case-writer-hybrid-execution-spec.md](../../docs/case-writer-hybrid-execution-spec.md)
