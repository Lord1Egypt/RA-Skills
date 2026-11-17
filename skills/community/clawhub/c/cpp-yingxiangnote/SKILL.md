---
name: cpp-yingxiangnote
slug: cpp-yingxiangnote
version: 1.0.0
displayName: C++课件 → 印象笔记
description: 把 C++ 课件 / 讲义类 PDF 提取整理成结构化笔记，并以「印象笔记超级笔记原生格式」写入指定笔记本。当用户提供 C++ 课件 PDF（或其它课程 PDF）并说「整理到印象笔记」「存到印象笔记的 XX 笔记本」「做成笔记放进印象笔记」「pdf 转印象笔记笔记」时使用。也适用于需要把已整理好的 Markdown 转成印象笔记原生格式（可折叠标题大纲 + 原生代码块 + 原生表格）的场景。本 skill 内含 PDF 文字/表格提取能力（pymupdf），扫描版页面会自动渲染为图片交由视觉识别，因此无需额外安装 pdf-image-text-extractor。别名 c++yingxiangnote、c++印象笔记笔记。关键词：课件、讲义、pdf、提取文字、整理笔记、印象笔记、超级笔记、string、C++。
trigger:
  command: "/cppnote"
metadata: {"openclaw": {"emoji": "📘", "primaryEnv": "YINXIANG_TOKEN"}}
dependency:
  python:
    - pymupdf>=1.23.0
    - evernote3
    - thrift
---

# C++ 课件 → 印象笔记（原生超级笔记格式）

## 任务目标

把课件 PDF 整理成一份**印象笔记原生超级笔记**，具备：

- 可折叠的**标题大纲导航**（点大纲能跳到每个标题）
- **原生代码块**：行距紧贴、灰底、语法高亮、带行号、带代码块标题
- **原生表格**（smarttable）
- 用户的强调规范：小提示橙底、注意红字粉底、行内代码灰底

## 触发条件

用户给出 PDF（通常是 C++ 课件）+ 印象笔记 token，要求整理成笔记。
典型说法：「帮我整理到印象笔记」「存到印象笔记的 string 笔记本」。

---

## 🔴 先读这个

**动手前必须先读 `references/native-format.md`。**

里面记录了印象笔记客户端的「规范化」行为——客户端同步时会**重写你的内容**，
把不符合原生写法的样式全部拍平。已知踩过的坑：

| 错误写法 | 后果 |
|---------|------|
| 代码块每行一个 `div` | ❌ 行距巨大 |
| 代码块用一个 `div` + `<br/>` 分行 | ❌ 客户端拆散，灰底丢 |
| 代码块自己写 `<span color>` 上色 | ❌ 颜色被拍平 |
| 自定义 `div` 上写 `font-family: monospace` | ❌ 触发代码块拍平，颜色全丢 |
| 不设 `source=yinxiang.superNote` | ❌ 大纲导航完全不生效 |

**结论**：代码块照抄 `references/native-format.md` 第三节的格式，
**语法高亮不要自己写**，只声明 `lang` 让客户端渲染。

---

## 前置准备

```bash
pip install pymupdf evernote3 thrift
```

- **token**：印象笔记**生产环境**开发者 token（`S=s63:...` 形式）。
  申请：`https://app.yinxiang.com/api/DeveloperToken.action`
  ⚠️ 必须是生产环境（非 sandbox），沙箱 token 写不进用户的真实账号。
- **author**：用户的印象笔记昵称（写入笔记属性用）。可先 `check` 看账号信息。

先用 `check` 验证 token：

```bash
python scripts/yinxiang_push.py check --token "S=..."
```

---

## 标准流程（4 步）

### Step 1 — PDF 提取文字

```bash
python scripts/pdf_to_markdown.py "<pdf路径>" -o work/raw.md --json
```

脚本会：
- 按字号识别标题层级 → `#` / `##` / `###`
- 按等宽字体识别代码块 → ```` ```cpp ````
- 自动剔除每页重复的页脚水印
- 自动剔除代码的行号栏（连续纯数字行）
- 表格用 `find_tables()` 提取到 `tables_markdown`
- 扫描版页面渲染到 `ocr_pages/`，返回 `ocr_images` 清单

**若 `ocr_images` 非空**：逐张用 `read_image` 识别，把文字并入正文，
并告知用户哪些页是扫描页。

### Step 2 — 整理成 Markdown

基于 Step 1 的产物做整理（这一步需要你做判断）：

1. **删掉页脚残留**、与笔记标题重复的大标题
2. **修好段落**：PDF 提取常把一句话拆成多行，要合并成完整段落
3. **补回代码缩进、注释**，确认代码块内容正确
4. **识别讲解文字的类型**，用约定标记：
   - 小提示 → `> **✅ 小提示：**` 后跟内容行
   - 注意事项 → `> **注意：**` 后跟内容行
   - 普通引用 → `>` 开头
5. **给每个代码块写标题**（写在代码围栏上一行）：

   ```markdown
   <!-- title: 用 cin 输入字符串 -->
   ```cpp
   ...
   ```
   ```

   **代码块标题要「结合正文内容」写，说清这段话在讲什么**，不要干巴巴复述代码。
   - ✅ 好：`和字符数组的区别：string 可直接赋值`
   - ❌ 差：`string 对象直接赋值`
   - 实在判断不出来的，留空（`<!-- title: -->`）

产物：`work/note.md`

### Step 3 — 转成印象笔记原生 ENML

```bash
python scripts/markdown_to_enml.py work/note.md -o work/note.enml \
    --lang C++ --drop-first-title --promote 1
```

- `--drop-first-title`：笔记标题栏已有标题，去掉正文里重复的一级标题
- `--promote 1`：配合上一条，把标题层级整体上提一级（顶层小节成为 h1）
- `--lang`：代码块语言，决定客户端语法高亮（C++ 用 `C++`）
- 也可用 `--titles titles.json` 传标题数组

脚本输出统计（代码块数 / 标题数 / 表格数），**核对数量是否合理**。

### Step 4 — 写入印象笔记

```bash
# 新建
python scripts/yinxiang_push.py create \
    --token "S=..." --notebook "string" \
    --title "第 5 章 string" --content work/note.enml \
    --author "<用户昵称>"
```

笔记本不存在会自动创建。脚本会自动写好原生属性
（`source=yinxiang.superNote` 等），这是大纲导航和代码块生效的前提。

覆盖已有笔记用 `update`：

```bash
python scripts/yinxiang_push.py update --token "S=..." \
    --guid <noteGuid> --title "第 5 章 string" --content work/note.enml
```

### Step 5 — 告知用户同步验证

写完**必须提醒用户**：在客户端**手动同步一次**，然后确认：

1. 标题大纲能否列出所有标题
2. 代码块是否：行距紧贴 + 灰底 + 语法高亮 + 行号 + 有标题
3. 表格、小提示（橙底）、注意（红字粉底）是否正常

---

## 排错

**不要靠猜。** 推送后读回笔记内容与推送前对比，看客户端改了什么：

```bash
python - <<'PY'
import re, subprocess
# 用 get-note 读回（脚本无此命令时，用 SDK/临时脚本读）
PY
```

判定技巧（详见 `references/native-format.md` 第七节）：
- `#ECEAE6` 变成 `rgb(236, 234, 230)` → 客户端已处理过
- 内容长度大幅缩水 → 被拍平了
- `monospace` 是否还在 → 代码块是否被特殊处理

**最可靠的澄清办法**：让用户在客户端里**手动创建**一个同类元素
（标题 / 代码块 / 表格），然后读回它的 ENML 照抄。
这比反复试探快得多——本次的代码块格式就是这么确定的。

---

## 资源索引

- **格式规范（必读）**：[references/native-format.md](references/native-format.md)
  - 客户端规范化行为、原生代码块/标题/表格格式、硬性约束、排错方法
- **PDF 提取**：[scripts/pdf_to_markdown.py](scripts/pdf_to_markdown.py)
  - `<pdf> [-o out.md] [--scan-dir DIR] [--dpi N] [--no-tables] [--no-render] [--json]`
- **Markdown 转 ENML**：[scripts/markdown_to_enml.py](scripts/markdown_to_enml.py)
  - `<in.md> -o out.enml [--lang C++] [--drop-first-title] [--promote N] [--titles F]`
- **写入印象笔记**：[scripts/yinxiang_push.py](scripts/yinxiang_push.py)
  - `check | notebooks | create | update`，`--token --notebook --title --content [--guid] [--author]`

---

## 注意事项

- **token 是敏感凭证**：用完提醒用户去开发者后台作废重发。
  不要把 token 写进任何持久化文件或提交到仓库。
- **不要创建本地文件代替 API 调用**，也不要编造接口返回结果。
- **不要改** `markdown_to_enml.py` 里的 `CB_STYLE`（原生代码块样式），
  它是照客户端生成的原样复制，改动会导致样式被拍平。
- 生成临时脚本请放在工作目录，**用完删除**（里面可能含 token）。
- 若用户的 PDF 不是 C++ 课件，本 skill 依然可用，
  只是 `--lang` 换成对应语言、强调规范按用户习惯调整。
