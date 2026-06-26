# humanizer-zh

`humanizer-zh` 是中文去 AI 味 skill。它不是重写文章，而是在尽量不改事实、结构和观点的前提下，对正文做一轮受约束清洗。

## 这个 skill 能做什么

- 识别中文稿件里的明显 AI 痕迹
- 对正文做“轻手术式”改写
- 保留标题、结构、事实、数字和核心立场
- 输出一份清洗后的稿件
- 输出一份 JSON 报告，说明命中了哪些规则

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

本 skill 没有额外 CLI 依赖。

## 输入和输出

**输入**

- 任意中文 Markdown 或纯文本
- 常见输入：`content-production/drafts/<slug>-article.md`

**输出**

- `content-production/drafts/<slug>-humanized.md`
- `content-production/drafts/<slug>-humanizer-report.json`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill humanizer-zh \
  --input content-production/drafts/harness-engineering-一人公司-article.md
```

## 什么时候用

- 主稿已经写完，但你觉得语气太“像 AI”
- 你想保留内容判断，只处理文字表面的机械感
- 你需要一份报告，知道它具体改了哪些地方

## 注意事项

- 它不会替你补事实或新增论据
- 它默认不改标题和章节结构
- 如果主稿本身逻辑有问题，不应把它当成“修文救火工具”

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
