---
version: "1.0.0"
name: "epub-translator"
description: "将英文 EPUB 文件逐段翻译为中文（保留原文，译文紧跟其下），自动跳过代码块、保留公式样式、表格采取双表对照。基于 Deepseek 大模型并行翻译。当用户提供 EPUB 并要求翻译/中英对照/汉化时调用。"
---
> **Bilingual note**: This English edition mirrors `SKILL.zh-CN.md`. For the authoritative Chinese version, see `SKILL.zh-CN.md`.


# EPUB Translator (英→中 双语对照)

本 skill 将英文 EPUB 文件中的内容**逐段翻译为中文**，并把中文译文**放在原英文段落的紧下方**，形成"英在上、中在下"的双语对照排版。翻译完成后**必须**调用 `epub-reader-optimizer` skill 对成品进行样式美化。



## ⚠️ Security & Side-Effects Disclosure

| Behaviour | Default | Rationale |
|---|---|---|
| Network access | OFF | Only fetch remote resources when user explicitly approves. |
| Host toolchain install | OFF / fail-closed | Never auto-run `pip install`, `npm install -g`, `apt install`, etc. Report missing deps and wait for manual confirmation. |
| LaTeX `-shell-escape` | OFF | Disabled by default; only enabled when user consents AND environment is sandboxed AND content is trusted. |

**Core principles:**

1. Offline by default — all side-effects require explicit user consent.
2. Fail closed on missing dependencies — never auto-install packages.
3. Never enable `-shell-escape` on untrusted input.
4. Pin remote fetches to release tags (never master/main) — require user approval before network access.

## ⚠️ 安全与副作用声明

| 行为 | 默认值 | 说明 |
|---|---|---|
| 网络访问 | 关闭 | 仅在用户明确同意后访问网络资源。 |
| 主机工具链安装 | 关闭 / 失败即止 | 不会自动运行 `pip install`、`npm install -g`、`apt install` 等。缺失依赖时报告给用户并等待手动确认。 |
| LaTeX `-shell-escape` | 关闭 | 默认不启用 `-shell-escape`；仅在用户明确同意、沙箱/容器化环境、受信内容三者同时满足时才可开启。 |

**核心原则：**

1. 默认离线，所有副作用需用户明确同意。
2. 缺失依赖时**失败即止**，不自动安装任何包。
3. 对不受信内容禁用 `-shell-escape`。
4. 远程获取资源时**固定版本/标签**，不追踪 master/main，并需用户批准。

## 灵活输入支持

本技能接受多种输入格式：

| 输入类型 | 说明 |
|---|---|
| Markdown / TXT 文件 | 最常见输入，直接处理。 |
| JSON 结构化数据 | 包含 `title`、`chapters[]`、`content` 字段时作为结构化大纲处理。 |
| 直接 LLM 上下文 | 当用户以对话方式提供内容时，自动从上下文提取大纲与正文。 |
| URL / 仓库地址 | 仅在用户明确同意后抓取远程内容。 |

## When to Invoke

满足以下任一条件时调用本 skill：

- 用户提供英文（或其他外文）EPUB 文件，要求"翻译成中文" / "做中英对照版" / "汉化这本书"。
- 用户希望保留原文阅读体验的同时增加中文译文（不是替换原文）。
- 用户希望把一本英文电子书做成"段落级双语对照"版本，方便边读边对照。

## When Not to Invoke

- 用户提供的是中文 EPUB 想翻成英文 → 不在本 skill 范围（可参考本 skill 改 prompt）。
- 用户只想优化排版而不翻译 → 改用 `epub-reader-optimizer`。
- 用户提供的不是 EPUB（如 PDF/mobi/azw3）→ 先转 EPUB 再来。
- 用户希望"机器翻译重写原文"（即替换而非追加）→ 不属于本 skill 默认行为，需要显式确认后修改脚本。

## Core Constraints

1. **代码块不翻译**：识别 `<pre>`、`<code>` 标签包裹的内容，原样保留，不调用翻译 API。
2. **公式保留样式**：识别 `<math>`、MathML、`<img>` 公式（含 alt LaTeX）、行内 `$...$` / `\(...\)`、块级 `$$...$$` / `\[...\]` 等结构，**整段跳过翻译**或仅翻译纯文本上下文，公式本身原样保留。
3. **表格翻译策略**：对每个 `<table>`，**生成一份中文翻译表追加到原表下方**（而非原地覆盖），保持原表完整。
4. **段落级双语对照**：对普通段落（`<p>`、`<li>`、标题 `<h1>~<h6>`、`<blockquote>` 等），在该元素的紧下方插入一个**同类型**的中文节点，并加上 `class="translated-zh"` 便于后续 CSS 样式化。
5. **并行翻译**：使用 `concurrent.futures.ThreadPoolExecutor` 并发调用 Deepseek API（默认并发 16，可调），显著提升整本书的翻译效率。
6. **翻译完成后必须调用 `epub-reader-optimizer`** 对最终 EPUB 做排版美化（字体、行距、双语段落样式、白底白字修复等）。

## Model Configuration（OpenAI 兼容）

**不再硬编码** API key / base_url / model_name！全部通过 `config.json` 配置，且自动兼容任意 OpenAI 兼容服务（DeepSeek、OpenAI、通义千问、智谱、自建网关 ...）。

### Config File Location (priority order)

1. 命令行 `--config <path>` 显式指定
2. 脚本同目录 `assets/config.json`
3. skill 根目录 `config.json`（推荐放这里）
4. 当前工作目录 `config.json`
5. 兜底使用 `config.example.json`

### config.json 结构

```jsonc
{
    "model_name": "deepseek-v4-flash",
    "api_key":    "sk-...",
    "base_url":   "https://opencode.ai/zen/go/v1",
    "extra_body": {},
    "system_prompt": "你是一位专业的英→中技术翻译...（可选，有默认值）"
}
```

字段说明：

- `model_name`：OpenAI 兼容模型名。例：`deepseek-v4-flash`、`deepseek-chat`、`gpt-4o-mini`、`qwen-plus`、`glm-4-flash`。
- `api_key`：API key。**敏感字段，不要提交到公共仓库。** 推荐用环境变量 `API_KEY` 覆盖。
- `base_url`：服务根地址（**不含 `/chat/completions`**）。脚本会自动剥掉末尾的 `/chat/completions` 与多余斜杠。例：
  - DeepSeek 官方：`https://api.deepseek.com`
  - OpenCode 网关：`https://opencode.ai/zen/go/v1`
  - OpenAI 官方：`https://api.openai.com/v1`
  - 通义千问兼容模式：`https://dashscope.aliyuncs.com/compatible-mode/v1`
  - 智谱：`https://open.bigmodel.cn/api/paas/v4`
- `extra_body`：附加请求体。DeepSeek 关闭推理：`{"thinking": {"type": "disabled"}}`，其它模型一般留空 `{}`。
- `system_prompt`：翻译用 system prompt。脚本内置默认值，按需覆盖。

### 环境变量覆盖（最高优先级）

适合临时切换 / CI：

```bash
$env:API_KEY     = "sk-..."
$env:MODEL_NAME  = "deepseek-chat"
$env:BASE_URL    = "https://api.deepseek.com"
$env:SYSTEM_PROMPT = "...（可选）"
```

### 安全建议

- `config.json` 默认提供示例 key 仅供测试；生产请改为占位符或加入 `.gitignore`。
- 推荐做法：`config.json` 仅写 `model_name` / `base_url` / `extra_body` / `system_prompt`，而 `api_key` 通过环境变量 `API_KEY` 注入。

调用示例（脚本内部）：

```python
from openai import OpenAI

client = OpenAI(api_key=CONFIG["api_key"], base_url=CONFIG["base_url"])

resp = client.chat.completions.create(
    model=CONFIG["model_name"],
    messages=[
        {"role": "system", "content": CONFIG["system_prompt"]},
        {"role": "user",   "content": text_to_translate},
    ],
    stream=False,
    extra_body=CONFIG.get("extra_body") or {},
)
translated = resp.choices[0].message.content
```

依赖：`openai`、`beautifulsoup4`、`lxml`。不要自动运行 `pip install`；报告缺失依赖并等待用户手动安装。

## Workflow Overview

```
1. 准备工作目录，复制输入 EPUB 到临时目录
2. 解包 EPUB（unzip / Python zipfile）
3. 探查 content.opf，列出所有 (x)html 章节文件
4. 遍历章节：用 BeautifulSoup 解析 HTML
   - 收集所有需要翻译的"翻译单元"（段落、列表项、标题、表格单元格、引用）
   - 跳过：<pre>/<code>、公式（math/含 LaTeX 的 img/含 $...$ 的纯文本段）
5. 并行调用 Deepseek 翻译（ThreadPoolExecutor + 缓存去重）
6. 写回 HTML：
   - 普通段落 → 紧跟一个 class="translated-zh" 的同类型节点
   - <table> → 在其后追加一个 class="translated-zh table-zh" 的整表翻译版
7. 注入 CSS（追加到现有 stylesheet 或新建 translated.css）
8. 重新打包 EPUB（mimetype STORED 第一个条目）
9. 调用 epub-reader-optimizer 做最终样式美化
10. 把成品放到用户的 workspace 目录并给出 computer:// 链接
```

## Translation Unit Identification Rules (Key)

**跳过翻译**的节点：
- 标签：`<pre>`、`<code>`、`<math>`、`<svg>`、`<script>`、`<style>`、`<noscript>`、`<kbd>`、`<samp>`、`<tt>`
- div class（Springer/O'Reilly/Apress 等常见出版社）：
  - `ProgramCode`、`LineGroup`、`FixedLine`、`EmphasisFontCategoryNonProportional`
  - `Code`/`code-block`/`CodeBlock`/`listing`/`Listing`
  - `informalexample`、`programlisting`、`screen`、`literallayout`
  - 公式相关：`MathJax`、`equation`、`Equation`、`EquationContent`
- `<img>`（公式图片或装饰图片）
- 纯文本只包含 LaTeX/公式（如 `$E = mc^2$`、`\(x_i\)`、`\[ \sum ... \]`）的段落
- 文本长度 < 2 或只含数字/标点的段落
- 文本已超过 50% 是 CJK（已经是中文）的段落

**需要翻译**的节点（按类型保留原标签）：
- 标签：`<p>`、`<blockquote>`、`<li>`、`<h1>`~`<h6>`、`<figcaption>`、`<caption>`、`<dd>`、`<dt>`
- div class：`<div class="Para">`（出版社段落容器，常见于 Springer/Apress）
- 表格 `<table>` 的 `<th>`、`<td>` 文本

**特殊处理**：
- 段落内的 inline `<code>`、行内公式 `$...$`：翻译时把这些片段用占位符 `⟦KEEP_n⟧` 替换，翻译完后再还原。
- 段落级 div 内部含有代码块子节点时，**提取文本时自动跳过 skippable 子树**，只翻译散文部分。
- `class` 属性可能是 list 或 str，统一用 `_classes_of()` 辅助函数取规范化的 list。

## Publisher Compatibility Notes

**Springer / Apress** 的常见 EPUB 结构：
- 段落用 `<p class="Para">` 或 `<div class="Para">`（两种都要收集）
- 代码块嵌套：`<div class="ProgramCode"><div class="LineGroup"><div class="FixedLine">...</div></div></div>`（完全没有 `<pre>` / `<code>`！）
- 行内等宽文字：`<span class="EmphasisFontCategoryNonProportional">`
- 章节标题：`<h1 class="ChapterTitle">`、`<h2 class="Heading">`
- 内联术语：`<span id="ITerm1">...</span>` — 不必处理，文本提取会自动忽略 id

**O'Reilly** 类 EPUB 通常用语义化 `<pre><code>` —— 已经覆盖。

**注意**：处理新出版社时，先用 `class` 出现频率统计快速识别其代码块 class 名，必要时把它加入 `SKIP_DIV_CLASSES`。

## System Prompt（翻译质量关键）

```
你是一位专业的技术翻译专家，擅长把英文技术书籍/文档翻译为简体中文。
要求：
1. 译文准确、自然、符合中文技术写作习惯，不要逐字硬译。
2. 保留所有占位符 ⟦CODE_n⟧、⟦MATH_n⟧、⟦KEEP_n⟧ 原样不变，不要翻译它们。
3. 保留专有名词、API 名、类名、函数名、产品名的英文原文（必要时可加中文解释）。
4. 保留 Markdown / HTML 标记（如 **bold**、`code`、<em>）不变。
5. 只输出译文本身，不要加任何"翻译："、"以下是译文"之类的前缀。
6. 如果输入是标题，译文也应该是标题语气的短句。
```

## Reusable Assets

- `assets/translate_epub.py` — 主脚本：解包 → 提取翻译单元 → 并行翻译 → 写回 → 打包。
- `assets/translated.css` — 双语段落基础 CSS（`.translated-zh` 样式）。

## Usage

```bash
# 基本用法（输入英文 EPUB，输出中英对照 EPUB）
python assets/translate_epub.py <input.epub> <output.epub>

# 可选参数
python assets/translate_epub.py input.epub output.epub \
    --concurrency 64 \                                # 默认 64；测试 96 仍可线性 scale
    --work-dir <path> \                              # 工作目录（解包/缓存所在）
    --resume                                          # 断点续传：复用 cache.json
```

### Concurrency Benchmarks

200 条段落（平均 141 字符），DeepSeek `deepseek-v4-flash`：

| 并发 | 耗时 | 速率 | 相对提升 |
|---|---|---|---|
| 16 | 15.5 s | 12.9/段·秒 | 1.0× |
| 32 | 7.0 s | 28.4/段·秒 | 2.2× |
| 64 | 4.0 s | 49.5/段·秒 | 3.8× |
| 96 | 3.2 s | 62.8/段·秒 | 4.9× |

DeepSeek API 几乎线性扩展，**推荐默认并发 64，急速档 96**。整本 ~3300 段的书在 96 并发下约 1 分钟可全量翻译完。

### Idempotency / Repeat-Run Safety

- 重复运行**不会重复插入译文**。脚本在三处都做幂等检查：
  1. `collect_units_in_html`：跳过 class 含 `translated-zh` 的节点 + 跳过紧邻已是 translated-zh 的源节点
  2. `insert_translation_node`：插入前再次检查 next sibling
  3. `translate_table_node`：同样检查 next sibling 是否为已生成的翻译表
- `--resume` 模式下**强制重新解包源 EPUB**（不复用已写过译文的 extract 目录），从干净 DOM 上重做"复用缓存 → 写回译文"，避免污染。
- class 去重：`["Para", "translated-zh"]` 不会变成 `["Para", "translated-zh", "translated-zh"]`。

### Global Two-Phase Parallelism

旧版本按"章节串行"循环翻译，章节切换时线程池闲置；新版本改为**全局两阶段**：

1. **PHASE 1**：扫描所有章节，把全部 unique 待翻文本汇总到一个全局列表（DOM 解析快，串行即可）
2. **PHASE 2**：一次性提交全局线程池并行翻译，线程池满负荷一路跑到底
3. **PHASE 3**：按缓存把译文写回各章节 DOM 并保存

这样让 API 调用 100% 重叠，**端到端再省 15-20% 时间**。


## 关键实现要点

### 1. 段落抽取与去重缓存

把"待翻译文本 → 译文"存到一个 `dict` 缓存（同时序列化为 `cache.json`），同一本书里重复出现的短语只翻一次，节省 API 调用。

### 2. 并行调度

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def translate_one(text: str) -> str:
    if text in CACHE:
        return CACHE[text]
    resp = client.chat.completions.create(
        model=DEEPSEEK_MODEL_NAME,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": text}],
        stream=False,
        extra_body={"thinking": {"type": "disabled"}},
    )
    out = resp.choices[0].message.content.strip()
    CACHE[text] = out
    return out

with ThreadPoolExecutor(max_workers=16) as pool:
    futures = {pool.submit(translate_one, t): t for t in unique_texts}
    for fu in as_completed(futures):
        results[futures[fu]] = fu.result()
```

### 3. 写回 HTML（保留段落标签类型）

```python
from bs4 import BeautifulSoup

def insert_translation(soup, node, zh_text):
    new_tag = soup.new_tag(node.name)
    new_tag['class'] = (node.get('class', []) or []) + ['translated-zh']
    new_tag.string = zh_text
    node.insert_after(new_tag)
```

### 4. 表格翻译（整表克隆 + 翻译所有单元格 + 追加）

```python
import copy
def translate_table(soup, table_node, translator):
    cloned = copy.copy(table_node)  # 浅拷贝后递归处理或直接 deepcopy
    # ... 遍历 cloned 的 th/td，把 text 替换为译文 ...
    cloned['class'] = (cloned.get('class', []) or []) + ['translated-zh', 'table-zh']
    table_node.insert_after(cloned)
```

### 5. 占位符保护公式 / 行内代码

```python
import re
PLACEHOLDER_RE = re.compile(r'(`[^`]+`|\$[^$\n]+\$|\\\([^)]+\\\))')

def protect(text):
    keeps = []
    def _sub(m):
        keeps.append(m.group(0))
        return f"⟦KEEP_{len(keeps)-1}⟧"
    masked = PLACEHOLDER_RE.sub(_sub, text)
    return masked, keeps

def restore(text, keeps):
    for i, k in enumerate(keeps):
        text = text.replace(f"⟦KEEP_{i}⟧", k)
    return text
```

### 6. CSS 注入

往现有 stylesheet 末尾追加（或新建 `translated.css` 并在 OPF/HTML head 中引用）：

```css
.translated-zh {
    color: #1a4d8c;
    font-family: "LXGW WenKai", "Source Han Serif SC", "Noto Serif CJK SC", serif;
    margin-top: 0.2em;
    margin-bottom: 1em;
    line-height: 1.75;
}
.translated-zh.table-zh {
    margin-top: 0.5em;
    border-top: 2px dashed #888;
}
```

## 异常处理

- **API 限流**：捕获 429 / RateLimitError，指数退避重试（最多 5 次）。
- **超长段落**：>3000 字符的段落，先按句号切分再翻，最后拼回。
- **空响应**：如果 Deepseek 返回空，回退为"[翻译失败，原文保留]"标记，不阻塞整体流程。
- **断点续传**：每翻译 50 段落 flush 一次 `cache.json`，意外中断后下次启动自动复用。

## 文件位置约定

- 输入 EPUB：用户提供的路径
- 临时工作目录：`c:\Users\<USER>\.trae-cn\work\<SESSION>\epub-translate\`
- 输出 EPUB：`d:\TARE-WORK\<原文件名>_中英对照.epub`
- 翻译缓存：临时工作目录下的 `cache.json`

## 后续步骤（必做）

翻译完成并打包出 EPUB 后，**必须**调用 `epub-reader-optimizer` skill 对成品做样式美化，重点处理：
- 中文段落字体（LXGW WenKai）
- `.translated-zh` 颜色与左侧色条
- 表格双语对照视觉区分
- 修复阅读器白底白字、行距过挤等通用问题
