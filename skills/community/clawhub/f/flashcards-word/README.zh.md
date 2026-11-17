# 儿童认字卡 / 单词卡（可打印 Word .docx）

为 **5 岁左右**的小朋友制作**可打印、可裁剪**的闪卡，输出为排版干净的 Word（`.docx`）文件。
每页 A4 纸放 **4 张卡（四个角）**。**正面 = 可爱配图 + 大字**；**背面 = 只有一个大字**（用于认读/描摹背诵）。
版面按**双面长边翻转镜像对齐**，打印翻面后，每张背面的字正好落在对应配图的正下方。

**英文单词**开箱即用（本仓库默认）；**中文汉字 + 拼音**走同一套流水线（见 `hanzi-flashcards-word` 配套技能 / 下文「示例 D」）。

```
        +---------------------+---------------------+
        |   🐱                |   🐶                |
        |   cat               |   dog               |   <- 正面（图 + 字）
        +---------------------+---------------------+
        |   🐦                |   🐟                |
        |   bird              |   fish              |
        +---------------------+---------------------+

        +---------------------+---------------------+
        |                     |                     |
        |        dog          |        cat          |   <- 背面（只有大字，
        +---------------------+---------------------+      左右列镜像，供
        |                     |                     |       双面长边翻转使用）
        |        fish         |        bird         |
        +---------------------+---------------------+
```

> 本文件为**中文说明**，英文原版见 [README.md](README.md)。

---

## 1. 环境要求

- **Python** 3.9+
- **Python 依赖：** `pip install -r requirements.txt` → 安装 `Pillow`、`python-docx`
- **`rsvg-convert`**（把 emoji 的 SVG 转成清晰 PNG）。安装：
  - Debian/Ubuntu：`sudo apt-get install -y librsvg2-bin`
  - macOS：`brew install librsvg`
- **`curl`**（多数系统自带）
- **一个能读粗体无衬线字体的字体**（默认 DejaVu Sans Bold；Liberation / Noto Sans 亦可）。用 `fc-list | grep -i sans` 查找。

> ⚠️ 所有命令都要在**真实 shell**里跑。Pillow / python-docx 在未安装它们的沙箱 / REPL 里会 `ModuleNotFoundError`。

---

## 2. 快速上手（英文，40 个词）

```bash
# 0) 把脚本拿到一个工作目录里
cd my-flashcards          # 内含 scripts/ 、requirements.txt

# 1) 安装依赖
pip install -r requirements.txt
sudo apt-get install -y librsvg2-bin     # 若缺 rsvg-convert

# 2) 校验词表（数量、4 的倍数、无重复）
python3 scripts/words100.py

# 3) 下载配图（SVG -> 256px PNG），已做防竞争处理
python3 scripts/download_emoji.py

# 4) 渲染所有词的正面 + 反面 PNG
python3 scripts/generate_all.py

# 5) 组装双面的 .docx
python3 scripts/build_docx.py
```

输出：`English_Words_DoubleSided.docx`（1 张 A4 = 4 张卡 = 1 正 + 1 反）。

或直接一条命令：`make cards`（按顺序跑完上面四步）。

---

## 3. 词表 — `scripts/words100.py`

内容就是一个 Python 列表：

```python
WORDS = [
    (word, "", emoji),        # (卡片上的字) ("" 占位) (配图 codepoint)
    ...
]
```

- **`word`** — 卡片上放大显示的词。给 5 岁孩子用，尽量**短而简单**。大小写保留你输入的样子。
- **`""`** — 刻意留空的占位槽（为了和中文/拼音版保持同一个三元组结构，那边这里放拼音）。英文渲染时忽略。
- **`emoji`** — 用作配图的任意 Twemoji codepoint。ZWJ / VS16 组合都行（如 `"🍦"`、`"🦆"`），下载器会自动剥掉不可见修饰符再组文件名。

**三条规则：**
- `len(WORDS)` 必须是 **4 的倍数**（4 → 1 张，8 → 2 张，100 → 25 张）。
- 词必须**互不重复**。
- 每次改完都跑 `python3 scripts/words100.py` 自检（它会对以上三条做 `assert`）。

---

## 4. 示例

### 示例 A — 再追加 8 个食物词（40 → 48，仍是 4 的倍数）
编辑 `scripts/words100.py`，往 `WORDS` 里追加：
```python
    ("pasta",      "", "🍝"),
    ("rice",       "", "🍚"),
    ("bread",      "", "🍞"),
    ("carrot",     "", "🥕"),
    ("tomato",     "", "🍅"),
    ("pepper",     "", "🌶️"),
    ("potato",     "", "🥔"),
    ("mushroom",   "", "🍄"),
```
→ `python3 scripts/words100.py` 应打印 `OK: 48 unique English words`。重跑第 3–5 步。

### 示例 B — 一个主题小集合（如「颜色」8 个词）
把 `WORDS` 换成刚好 8 个：
```python
WORDS = [
    ("red",    "", "🔴"),
    ("blue",   "", "🔵"),
    ("yellow", "", "🟡"),
    ("green",  "", "🟢"),
    ("orange", "", "🟠"),
    ("purple", "", "🟣"),
    ("pink",   "", "🌸"),
    ("brown",  "", "🟤"),
]
```
→ 第 5 步会写出 2 张的 docx（1 正 + 1 反）。

### 示例 C — 相近的词共用一张图（允许）
```python
    ("sun",  "", "☀️"),
    ("star", "", "⭐"),        # 不同 emoji，不同图
    # 但"真的一张图都合适"时共用完全没问题：
    ("ear",  "", "👂"),
    ("hear", "", "👂"),        # 有意共用 -> 会被打印提示，不是错误
```
下载器最后会做 **md5 冲突检查**；有意共用的图会列在 `intentional shared images: [...]` 里，是允许的。只有**无意冲突**才需要处理。

### 示例 D — 中文 / 拼音（配套技能）
同样的版面，只是中间槽放**带声调的拼音（用预合成字符）**，字体换成 CJK：
```python
WORDS = [
    ("日", "rì",   None),     # None -> 手绘卡
    ("火", "huǒ",  "🔥"),     # emoji 图
    ...
]
```
用 CJK 字体（`EN_FONT`/`CJK_FONT` → 如文泉驿正黑 WenQuanYi Zen Hei / Noto Sans CJK）。其余流水线（下载 → 渲染 → .docx + 镜像对齐）完全一致。

### 示例 E — 没有 emoji 的数字/自定义卡
某些条目不是 emoji（如 1–10 数字键帽、自绘图）。把 emoji 槽设为自定义标记，并按匹配规则放一张预渲染 PNG：
```python
    ("one", "", "D1"),        # "D1" 表示：用 pre_one_front/back.png
```
把 `pre_one_front.png` 与 `pre_one_back.png` 放到脚本同目录，渲染时直接原样拷贝过去。

---

## 5. 版式原理（让你不用靠眼睛盯）

**长宽比。** A4 竖排、10 mm 边距 → 可用 190×277 mm。2×2 格里的一格是 95×138.5 mm。
每张卡的图按 **≈95:135** 的宽高比生成，于是 `add_picture(width=Mm(95), height=Mm(135))` 放进去**不变形**。

**每页一张无边框 2×2 表格。** 每页一张无边框表格，图充满每格。
跨页用 `document.add_section(NEW_PAGE)`（**不要**用会出错的“手动分页符 `add_break`”）。

**双面镜像对齐（关键技巧）。** Word 默认双面打印是**长边翻转 = 左右镜像**。所以背面要把两列互换：

```
正面：                  背面（两列互换）：
 w0  w1                  w1  w0
 w2  w3                  w3  w2
```
脚本对**每一对**卡都做 `assert` 校验（不是抽查）：
```python
mirror = {"TL":"TR", "TR":"TL", "BL":"BR", "BR":"BL"}
for pos, word in front.items():
    assert back[mirror[pos]] == word, f"misaligned {pos}"
```

### 打印设置（务必告诉使用者！）
- **双面打印 → 长边翻转**。
- **实际大小 / 不要“适应页面”** —— 不要缩放。
- **157 gsm 以上卡纸**更耐用（或普通纸打印后粘到卡纸上）。
- 沿四张卡之间的接缝裁剪。

---

## 6. 常见问题

| 现象 | 原因 / 解决 |
|---|---|
| `ModuleNotFoundError: Pillow / docx` | 不是真实 Python 环境。在装了 `pip install -r requirements.txt` 的 shell 里跑。 |
| `rsvg-convert: command not found` | `sudo apt-get install -y librsvg2-bin`（或 `brew install librsvg`）。 |
| emoji 下载 404 | VS16/ZWJ 组合 —— 脚本已自动剥离；自定义词 404 时改用其基础 codepoint。 |
| 词渲染成方框 / 豆腐块 | 字体缺字形。把 `EN_FONT` 指到含这些字形的字体（汉字用 CJK 字体）。 |
| 某个词被裁掉 | 自动缩字能解决；仍紧张就缩短词，或调 `generate_all.py` 里的最小字号下限。 |
| 并发下载时临时文件串号 | 已修（每个 codepoint 独立临时文件 + 并发前先按唯一 codepoint 去重）。 |

---

## 7. 重复运行 / 幂等

流水线可安全重跑：`download_emoji.py` 会清空旧 PNG 并重建 `emoji/_final.json`；
`generate_all.py` 覆盖 `all_front/` 和 `all_back/`；`build_docx.py` 重写 `.docx`。
想全新开始用 `make clean`（删 `emoji/ all_front/ all_back/` + docx）。

---

## 8. 目录结构

```
flashcards-word/
├── README.md                 # 英文版
├── README.zh.md              # 中文说明（本文件）
├── LICENSE                   # MIT
├── Makefile                  # `make cards` / `make clean`
├── requirements.txt          # Pillow, python-docx
├── .env.example              # EMOJI_OUT / EN_FONT / OUT_DOCX 覆盖项
├── SKILL.md                  # 完整规范：配方、踩坑、校验清单
└── scripts/
    ├── words100.py           # 词表 + emoji（改这个）
    ├── download_emoji.py     # Twemoji SVG -> PNG（防竞争、md5 检查）
    ├── generate_all.py       # 渲染正/反面卡 PNG（大字自动缩放）
    └── build_docx.py         # 双面 2x2 无边框 .docx 组装器
```

## 9. 开源许可

MIT —— 见 `LICENSE`。Emoji 配图来自 [Twemoji](https://github.com/twitter/twemoji)（CC / 可自由使用）。
