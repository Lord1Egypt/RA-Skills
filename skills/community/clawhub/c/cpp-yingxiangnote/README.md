# cpp-yingxiangnote · C++ 课件 → 印象笔记

把 **C++ 课件 / 讲义类 PDF** 提取整理成结构化笔记，并以**印象笔记「超级笔记」原生格式**写入指定笔记本。

生成出来的笔记具备：

- 🔖 **可折叠的标题大纲导航**（点大纲直接跳到每个标题）
- 💻 **原生代码块**：行距紧贴、灰底、语法高亮、带行号、**带代码块标题**
- 📊 **原生表格**（smarttable）
- 🎨 符合印象笔记原生习惯的强调样式：小提示橙底、注意红字粉底、行内代码灰底
- 📄 含 **PDF 文字 + 表格提取**，扫描版页面自动渲染成图片交给视觉识别

---

## 为什么需要它

直接把 Markdown 塞进印象笔记是**不行的**。印象笔记客户端同步时会「规范化」内容，
把不符合原生写法的样式统统拍平。本项目把这些坑全部踩过并固化下来：

| 常见错误做法 | 后果 |
|---|---|
| 代码块每行一个 `<div>` | ❌ 行距巨大，松散难看 |
| 代码块用一个 `<div>` + `<br/>` 分行 | ❌ 客户端拆散，灰底丢失 |
| 自己写 `<span style="color:#xxx">` 给代码上色 | ❌ 颜色被拍平 |
| 自定义 `div` 上写 `font-family: monospace` | ❌ 触发「代码块拍平」，颜色全丢 |
| 不设置 `source=yinxiang.superNote` | ❌ 标题大纲导航完全不生效 |

**正确做法**：代码块照抄客户端自己的生成格式，**语法高亮不自己写**，
只声明 `lang` 让客户端渲染。全部细节见 `references/native-format.md`。

---

## 安装

```bash
clawhub install cpp-yingxiangnote
```

安装后放到 `$DSH_HOME/skills/`，skill-filesystem 会自动热发现。

> ⚠️ 若技能没被加载，检查 `skill-filesystem` 插件是否启用
> （某些 bundle 的 overrides 会把它禁用）。

### 依赖

```bash
pip install pymupdf evernote3 thrift
```

---

## 使用

新开对话直接说：

> 帮我把 `D:\课件\第 6 章 数组.pdf` 整理到印象笔记的 `数组` 笔记本
> token: `S=s63:...`

或使用触发命令 `/cppnote`。

### 需要提供

1. **PDF 路径**
2. **印象笔记生产环境开发者 token**
   （申请：<https://app.yinxiang.com/api/DeveloperToken.action>）
   - ⚠️ 必须是**生产环境**（非 sandbox），沙箱 token 写不进真实账号
3. （可选）目标笔记本名、你的印象笔记昵称（写入笔记属性用）

---

## 内置脚本

| 脚本 | 作用 |
|---|---|
| `scripts/pdf_to_markdown.py` | PDF → 结构化 Markdown（标题层级、代码块、表格、去页脚、去行号） |
| `scripts/markdown_to_enml.py` | Markdown → 印象笔记原生 ENML |
| `scripts/yinxiang_push.py` | ENML → 印象笔记 API（`check` / `notebooks` / `create` / `update`） |

### 单独使用示例

```bash
# 1. 提取 PDF
python scripts/pdf_to_markdown.py "课件.pdf" -o raw.md --json

# 2. 整理后转原生格式
python scripts/markdown_to_enml.py note.md -o note.enml \
    --lang C++ --drop-first-title --promote 1

# 3. 写入印象笔记
python scripts/yinxiang_push.py create --token "S=..." \
    --notebook "string" --title "第 5 章 string" --content note.enml
```

---

## 实测效果

以 41 页 C++ 课件《第 5 章 string》为例：

| 项目 | 结果 |
|---|---|
| 代码块 | 63 个（原生格式，带标题 + 行号 + 语法高亮） |
| 标题 | 35 个（全部可折叠、可大纲导航） |
| 表格 | 1 个原生 smarttable |
| 空行 | 76 个（代码块后 + 每节内容结束后） |

---

## 文件结构

```
cpp-yingxiangnote/
├── SKILL.md                    主流程说明
├── README.md
├── LICENSE
├── references/
│   └── native-format.md         ★ 印象笔记原生格式规范（踩坑记录）
└── scripts/
    ├── pdf_to_markdown.py
    ├── markdown_to_enml.py
    └── yinxiang_push.py
```

`references/native-format.md` 是最值钱的部分，记录了印象笔记客户端的
「规范化」行为规律、各类原生元素的准确写法、以及排错方法。
**改动格式前请先读它。**

---

## 安全提示

- **token 是敏感凭证**，拥有你账号的完整读写权限。
  用完请去开发者后台**作废重发**，不要写进任何持久化文件或提交到仓库。
- 脚本只在你本机运行，不会上传任何数据到第三方。
- 生成临时脚本请放在工作目录并**用完删除**。

---

## License

MIT
