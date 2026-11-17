# 印象笔记「超级笔记」原生格式规范

本文件记录的是**实测结论**，全部来自「读取客户端自己生成/改写后的笔记内容，前后对比」得出。
改动格式前请先读这里，否则会踩同样的坑。

---

## 一、为什么必须用「原生格式」

印象笔记客户端把笔记分成两类：

| 类型 | 判定依据 | 能力 |
|------|---------|------|
| **超级笔记（原生）** | `note.attributes.source == "yinxiang.superNote"` | 标题大纲导航、可折叠、原生代码块、原生表格 |
| 普通/旧笔记 | 没有该标记（API 直接写入的默认状态） | 标题只是普通 HTML 标题，**大纲导航失效** |

**关键**：通过 API 写入 ENML 时，如果不同时设置 `source = yinxiang.superNote`，
客户端不认这条笔记是原生笔记，标题导航、代码块、行距全部不生效。

必须设置的原生属性：

```
note.attributes.source            = "yinxiang.superNote"
note.attributes.sourceApplication = "yinxiang.win32"
note.attributes.author            = "<你的印象笔记昵称>"
applicationData["yinxiang.noteLayout"]
    = {"autoLayoutWidth":1,"autoLineSpace":"recommend","autoParagraphSpace":"recommend"}
```

`yinxiang.noteLayout` 要在 `updateNote` **之后**用
`setNoteApplicationDataEntry` 单独写，否则会被覆盖。

---

## 二、客户端的「规范化」行为（最重要）

**客户端在同步时会重写笔记内容**，把不认识的写法拍平。实测规律：

| 你写的 | 客户端怎么处理 | 结果 |
|--------|--------------|------|
| 自定义 `div` + `font-family: monospace` | 判定为「代码块」，**把内容拍平成纯文本** | ❌ 内部 `span color` **全部丢失** |
| 一个 `div` 里用 `<br/>` 分行 | 按 `<br/>` **拆成每行一个 div** | ❌ 灰底只剩第一行，行距变大 |
| 每行一个 `div`（代码） | 每个 `div` 当独立段落 | ❌ 段间距很大，行距松散 |
| 自己写 `<span style="color:#xxx">` 给代码上色 | 在代码块语境下被剥掉 | ❌ 颜色丢失 |
| `div` 带 `background-color`（正文/提示） | 保留（十六进制会被转成 `rgb()`） | ✅ 正常 |
| 纯 `div` + `span color`（正文强调） | 保留 | ✅ 正常 |
| `span color` 外套 `span background-color` | 保留 | ✅ 正常 |

**一句话结论**：代码块必须**完全照抄客户端自己的生成格式**，
语法高亮**不要自己写**，只声明语言让客户端渲染。

---

## 三、原生代码块的正确格式

```html
<div style="--en-codeblock:true;
            --en-blockId:C47nTC5rTbr;
            --en-meta:{&quot;title&quot;:&quot;代码块标题&quot;,&quot;lang&quot;:&quot;C++&quot;,&quot;theme&quot;:&quot;default&quot;,&quot;showLine&quot;:true,&quot;lineWrap&quot;:false};
            box-sizing: border-box; padding: 8px;
            font-family: Monaco, Menlo, Consolas, &quot;Courier New&quot;, monospace;
            font-size: 12px; color: rgb(51, 51, 51);
            border-top-left-radius: 4px; border-top-right-radius: 4px;
            border-bottom-right-radius: 4px; border-bottom-left-radius: 4px;
            background-color: rgb(251, 250, 248);
            border: 1px solid rgba(0, 0, 0, 0.14902);
            background-position: initial initial; background-repeat: initial initial;
            margin-top: 6px;margin-bottom: 6px;">#include &lt;iostream&gt;
#include &lt;string&gt;
using namespace std;
int main()
{
&nbsp;&nbsp;&nbsp;return 0;
}</div>
```

**四个必须遵守的要点：**

1. **整个代码块是一个 `div`**，行与行之间是**真正的换行符** `\n`（不是 `<br/>`，不是多 div）
2. **内容是纯文本**，只做 HTML 转义（`<` → `&lt;`，`>` → `&gt;`，`&` → `&amp;`）
3. **行首空格转成 `&nbsp;`** 保缩进
4. **`--en-meta` 里的 `lang` 决定语法高亮**，`title` 是代码块标题（显示在代码块左上角），
   `showLine: true` 显示行号

`--en-meta` 的值在 `style` 属性里，JSON 的双引号必须转义成 `&quot;`。

`--en-blockId` 是 11 位字母数字随机串。

---

## 四、PDF 里的代码配色（供参考，不需要手动上色）

原 PDF（课件）用的是 **Atom One Light** 配色，代码字体 `SourceCodePro`：

| 颜色 | 用途 | 样例 |
|------|------|------|
| `#4078F2` | 预处理 `#` | `#` |
| `#A626A4` | 关键字 | `include` `using` `namespace` `return` `if` `for` |
| `#50A14F` | 字符串 / 头文件 | `"hello world"` `<iostream>` |
| `#986801` | 类型 / 数字 | `int` `char` `size_t` `20` `0` |
| `#C18401` | 函数名 | `main` `getline` `size` |
| `#336DF4` | 类 / 对象 | `string` `cin` `cout` |
| `#0184BB` | 常量 | `NULL` `true` `false` |
| `#A0A1A7` | 注释 | `//添加string头文件` |
| `#2B2F36` | 默认代码文字 | 标识符、括号、分号 |

> **不要把这些颜色写进 ENML**。客户端会依据 `lang` 自己渲染等效的语法高亮。
> 这张表只用于理解「PDF 里长什么样」。另外两个界面色：
> `#646A73` = 行号，`#1F2329` = 正文文字。

---

## 五、其它原生元素

### 标题（可折叠大纲）

```html
<h1 style="other-props:eyJibG9ja0lkIjoieUpRQWV6WHhXVGcifQ==;">目录</h1>
```

`other-props` 的值是 `base64(JSON)`：`{"blockId":"<11位随机串>"}`。
没有它，标题不会成为可折叠的原生标题块。

### 正文段落

```html
<div>正文文字</div>
```
用 `div`，不要用 `p`。

### 行内代码（灰底加粗）

```html
<span style="background-color: #ECEAE6;"><span style="font-weight: bold;">代码</span></span>
```

### 小提示（橙底）

```html
<div><span style="background-color: #FFDEBD;">小提示：内容</span></div>
```

### 注意 / 警告（红字 + 粉底）

```html
<div><span style="color: #FF0000;"><span style="background-color: #FFDCEB;">注意：内容</span></span></div>
```

### 列表

```html
<ul><li><div>条目</div></li></ul>
<ol><li><div>条目</div></li></ol>
```
`li` 里面要再包一层 `div`。

### 表格（原生 smarttable）

```html
<table style="--en-type:smarttable;border-left:1px solid #d9d9d9;border-top:1px solid #d9d9d9;border-collapse:collapse;width:829px;" width="829px">
<colgroup><col style="width: 414px;"/><col style="width: 414px;"/></colgroup>
<thead><tr><td>表头</td><td>表头</td></tr></thead>
<tbody>
<tr><td style="border-right:1px solid #d9d9d9;border-bottom:1px solid #d9d9d9;padding:10px;text-align:center;">单元格</td>...</tr>
</tbody>
</table>
```

### 空行

```html
<div><br/></div>
```

放置规则（用户明确要求）：
- **代码块之后** 加一个
- **下一个标题之前** 加一个（即「上一节的内容到此结束」，标题下方**不**加）

---

## 六、其它硬性约束

- 笔记 `content` **不要**写 `<?xml version="1.0" encoding="UTF-8"?>` 声明，
  直接从 `<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">` 开始
- ENML 走严格 DTD 校验：
  - 标签必须闭合（XHTML 风格，`<br/>` 不能写成 `<br>`）
  - **不允许 `class` 属性**（例如 `<code class="language-cpp">` 会被拒）
- `&nbsp;` 可用（客户端自己也用）；`&bull;` 这类非标准实体不要用，直接写 `•`

---

## 七、排错思路（下次遇到问题先做这个）

**不要靠猜。** 正确做法是：**读回客户端改写后的内容，做前后对比**。

```bash
# 1. 推送后立刻读回，存一份
python yinxiang_push.py update ... # 推送
# 2. 让用户在客户端同步一次
# 3. 再读回，对比差异
python - <<'PY'
import re
c = open('before.xml', encoding='utf-8').read()
d = open('after.xml',  encoding='utf-8').read()
for k in ['--en-codeblock', 'monospace', '#ECEAE6', 'rgb(', '<br/>']:
    print('%-18s before=%d  after=%d' % (k, c.count(k), d.count(k)))
PY
```

判定技巧：
- 看到 `#ECEAE6` 变成 `rgb(236, 234, 230)` → 说明客户端**已经处理过**
- 长度大幅缩水 → 内容被拍平了
- 找 `monospace` 是否还在 → 判断代码块是否被特殊处理

如果想验证「某种写法客户端是否保留」，**最可靠的办法**是让用户
在客户端里手动创建一个同类元素（标题 / 代码块 / 表格），然后读回它的 ENML，
照抄即可。这比反复试探快得多。

---

## 八、PDF 课件提取的坑（`pdf_to_markdown.py` 已处理）

用「课件类 PDF」实测出来的规律，改脚本前务必先看：

### 1. 正文段落可能也用等宽字体，只靠字体分不出代码

本次课件的实际分布：

| 字号 | 字体 | 内容 |
|------|------|------|
| 25.5 | Type3 | 文档大标题 |
| 19.5 / 16.5 / 15.0 / 13.5 | Type3 | 各级标题 |
| **12.0** | **SourceCodePro-Regular** | **正文段落** |
| **10.5** | **SourceCodePro-Regular** | **代码** |
| 8.0 | SimSun | 页脚 |

正文和代码**同字体**，只有字号差 1.5。所以判定规则是：

```
代码 = 主导字体是等宽 且 字号 < 正文基准字号
```

正文基准字号的取法：取「出现次数 ≥ 总行数 5%」的字号构成正文带，
**取其中最大的字号**作为正文（本例 max(10.5, 12.0) = 12.0）。
直接取众数会拿到 10.5（代码行更多），把正文全判成标题。

### 2. 行的「主导字体」要用占字符最多的 span

一行里可能混有回退字体 span。用 `all()` 会漏掉真正的代码行，
用 `any()` 会把正文误判成代码。正确做法是取**字符数最多的那个 span** 的字体。

### 3. 表格文字会混进代码块

表格单元格也是 10.5 等宽字体，会被当成代码。
必须先 `find_tables()` 拿到表格矩形，再把落在矩形内的行**整体排除**，
表格内容单独走 `tables_markdown` 输出。

### 4. 其它

- 页脚（如「比特就业课 / 算法竞赛从小白到国奖：URL」）每页重复 →
  按「出现在 ≥50% 页面的短行」自动剔除
- 代码行号栏是独立的纯数字行 → 连续 ≥3 行纯数字整段剔除
- 扫描版页面（文字层 < 20 字符）→ 渲染成 PNG，交给 `read_image` 识别

### 5. 脚本产出的是「原料」，不是成品

`raw.md` 里段落常被 PDF 拆成多行、表格内容另存、代码块可能被打断。
**Step 2 必须由你（模型）做整理**：合并段落、补回代码、识别提示/注意、
给每个代码块写标题。脚本只负责把结构抽出来。

