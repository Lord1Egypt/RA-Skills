---
name: cnn-english-learning-three
description: 当用户提供一段 CNN 新闻英文原文时，帮助用户进行逐句、逐词精读。
---

# CNN 新闻逐词精读 Skill

## 1. Skill 名称

**CNN News Word-by-Word Analyzer**

## 2. Skill 目标

当用户提供一段 CNN 新闻英文原文时，帮助用户进行**逐句、逐词精读**。

核心目标不是简单翻译新闻，而是让用户理解：

1. 每个单词本身是什么意思
2. 这个单词在当前句子中是什么意思
3. 这个单词在句子中的词性和语法作用
4. 为什么这里使用这个词，而不是其他近义词
5. 常见搭配和固定表达
6. 复杂句子的语法结构
7. 新闻英语中的常见表达方式

分析应该以**当前新闻语境**为核心，避免只给词典式释义。

---

## 3. 输入

用户通常会提供：

* 一段 CNN 新闻
* 一句话 CNN 新闻
* 一段新闻标题和正文
* 用户自己复制的新闻片段
* 新闻中的某一句或某个词

例如：

> The White House said Tuesday that the president would meet with foreign leaders later this week.

---

## 4. 输出原则

### 4.1 默认按照“句子 → 单词”进行分析

不要一开始把整篇文章所有单词混在一起解释。

应该按照：

**第 1 句 → 第 2 句 → 第 3 句**

逐句分析。

每个句子先给出：

1. 原句
2. 自然中文翻译
3. 句子结构
4. 单词逐词分析
5. 重要搭配
6. 语法重点

---

# 5. 单词分析要求

对于句子中的每个有实际意义的单词，都尽量提供以下信息：

| 单词 | 词性 | 基本含义 | 本句含义 | 本句用法 |
| -- | -- | ---- | ---- | ---- |

例如：

| 单词      | 词性   | 基本含义     | 本句含义 | 本句用法                            |
| ------- | ---- | -------- | ---- | ------------------------------- |
| meet    | v.   | 遇见；会面；满足 | 会见   | meet with sb. 表示“与某人会面”         |
| foreign | adj. | 外国的；对外的  | 外国的  | 修饰 leaders                      |
| leader  | n.   | 领导者      | 领导人  | foreign leaders 作 meet with 的宾语 |

---

# 6. 单词解释规则

## 6.1 不要只给一个中文意思

如果一个词有多个常见意思，应先列出核心含义，然后明确指出：

> **本句中取哪一个意思。**

例如：

**address**

* n. 地址
* n. 演讲
* v. 处理；解决；向……发表讲话

如果新闻句子是：

> The president addressed the nation.

应解释：

> **address：v.**
>
> 本义：向……讲话；处理；解决
> 本句：**向全国发表讲话**
>
> 这里不是“地址”的意思。
>
> `address + 人/群体` 可以表示“向某人/某群体发表讲话”。

---

## 6.2 必须区分词典义和语境义

例如：

> The government faces growing pressure.

对于 **face**：

不要只写：

> face = 面对

应写：

> **face：v.**
>
> 基本含义：面对；面临
> 本句含义：**面临**
>
> `face pressure` = 面临压力
> 这里不是字面上的“面对某个东西”，而是表示“处于某种困难或压力之下”。

---

# 7. 词性分析

使用常见英文缩写：

* n. = 名词
* v. = 动词
* vt. = 及物动词
* vi. = 不及物动词
* adj. = 形容词
* adv. = 副词
* prep. = 介词
* conj. = 连词
* pron. = 代词
* det. = 限定词
* modal v. = 情态动词
* auxiliary v. = 助动词
* phr. = 短语
* idiom = 习语

如果一个词在当前句子中发生了词性变化，要明确指出。

例如：

> The report was released Monday.

`released`：

> release 原形是动词，`released` 在这里是过去分词，和 `was` 构成一般过去时的被动语态。

---

# 8. 动词重点分析

新闻英语中，动词非常重要。

对于主要动词，应说明：

1. 原形
2. 时态
3. 语态
4. 是否及物
5. 后面接什么结构
6. 常见搭配
7. 本句具体含义

例如：

> The officials confirmed the report.

分析：

**confirmed**

* 原形：confirm
* 词性：v.
* 时态：一般过去时
* 含义：证实；确认
* 本句：证实了这份报道
* 用法：`confirm + 名词`
* `confirm that...` = 证实……

---

# 9. 名词重点分析

对于重要名词，说明：

* 单数/复数
* 可数/不可数
* 是否为专有名词
* 新闻语境中的具体含义
* 常见搭配

例如：

**officials**

* official → n.
* officials → 复数
* 含义：官员
* 本句：政府官员
* 常见搭配：

  * government officials
  * senior officials
  * U.S. officials

---

# 10. 形容词和副词

需要说明它修饰什么。

例如：

> The move was highly controversial.

分析：

**highly**

* adv.
* 高度地；非常
* 本句：非常
* 修饰 `controversial`

**controversial**

* adj.
* 有争议的
* 本句：具有很大争议的

并解释：

> `highly + adjective`

是新闻英语中非常常见的结构。

---

# 11. 介词重点分析

介词必须结合句子解释，而不能机械翻译。

例如：

> talks with China

不要简单解释：

> with = 和

应该解释：

> `talks with China`
>
> `with` 表示“与……之间”，说明 talks 的对象。

再例如：

> pressure on the government

解释：

> `on` 表示压力施加的对象，因此 `pressure on the government` = “施加在政府身上的压力 / 政府面临的压力”。

---

# 12. 短语和固定搭配

遇到固定搭配时必须整体解释。

例如：

* call for
* carry out
* step down
* take place
* be expected to
* according to
* in response to
* at least
* as a result
* amid concerns about
* in the wake of
* be likely to
* seek to do sth.

分析时不要把它们拆成完全独立的单词后就结束。

应该特别标记：

> ⭐ **固定搭配：call for**
>
> 表示：呼吁；要求
> `call for action` = 呼吁采取行动

---

# 13. 新闻英语特殊表达

CNN 等新闻媒体经常使用一些与普通英语不同的表达。

如果发现新闻英语表达，应标记：

> 📰 **新闻英语表达**

例如：

> officials said

解释为：

> “官员表示/官员说”

而不是机械翻译成“官员说”。

---

# 14. 句子结构分析

每个句子都应该先分析主干。

格式：

> **句子主干：**
>
> 主语 + 谓语 + 宾语

例如：

> The president announced new measures Tuesday.

分析：

> **主语（S）：** The president
> **谓语（V）：** announced
> **宾语（O）：** new measures
> **时间状语：** Tuesday

然后说明：

> 基本结构：
>
> **S + V + O + 时间状语**

---

# 15. 长难句处理

遇到 CNN 长难句时，不要一次性解释所有内容。

先把句子拆成结构：

> 主句
> ├── 定语从句
> ├── 状语从句
> ├── 插入语
> └── 非谓语结构

例如：

> The president, who spoke to reporters after the meeting, said that the government would take action.

分析：

> **主句：**
>
> The president said that...
>
> **插入的定语从句：**
>
> who spoke to reporters after the meeting
>
> **宾语从句：**
>
> that the government would take action

然后再进行逐词解释。

---

# 16. 中文翻译要求

翻译分成两层：

### 直译

尽量保持英文结构，帮助用户理解英文原句。

### 自然翻译

符合中文新闻表达习惯。

例如：

> The government faces growing pressure.

**直译：**

> 政府面临着不断增长的压力。

**自然翻译：**

> 政府承受的压力越来越大。

---

# 17. 新闻标题特殊处理

如果用户提供的是 CNN 标题，需要单独说明标题英语的特点。

例如标题：

> Trump faces new challenges in election campaign

可以解释：

* `faces` 使用一般现在时
* 新闻标题经常使用一般现在时描述刚刚发生或正在发生的事件
* `faces` = 面临，而不是“面对某人”
* `election campaign` = 竞选活动 / 竞选活动期间

如果标题省略冠词、be 动词或其他成分，应指出这是**新闻标题语言特点**，不要直接当成普通完整句子处理。

---

# 18. 不要过度分析

以下情况不需要长篇解释：

* the
* a
* an
* is
* are
* of
* to
* in

如果这些词只是普通基础用法，可以简洁说明。

但是如果某个基础词在当前句子中有特殊用法，则需要重点分析。

例如：

> be subject to

这里 `to` 就不能只解释成“到”。

---

# 19. 推荐输出模板

每句话按照以下格式：

## 第 1 句

> **原文：**
>
> The government faces growing pressure to act.

### ① 整句翻译

**直译：** 政府面临越来越大的采取行动的压力。

**自然翻译：** 政府面临越来越大的行动压力。

### ② 句子结构

> The government / faces / growing pressure / to act.

* **主语：** The government
* **谓语：** faces
* **宾语：** growing pressure
* **不定式：** to act，修饰/补充说明 pressure 的具体内容

基本结构：

> **S + V + O + to do**

### ③ 逐词分析

| 单词         | 词性                | 基本含义      | 本句含义  | 用法                     |
| ---------- | ----------------- | --------- | ----- | ---------------------- |
| The        | det.              | 这个/该      | 该     | 特指 government          |
| government | n.                | 政府        | 政府    | 作主语                    |
| faces      | v.                | 面对        | 面临    | `face pressure` = 面临压力 |
| growing    | adj.              | 增长的       | 越来越大的 | 修饰 pressure            |
| pressure   | n.                | 压力        | 压力    | `face pressure` 常见搭配   |
| to         | prep./inf. marker | 到；向；不定式标记 | ——    | 与 act 构成不定式            |
| act        | v.                | 行动        | 采取行动  | `act` 表示采取行动           |

### ④ ⭐ 重点搭配

**face pressure**

= 面临压力

**growing pressure**

= 越来越大的压力 / 日益增加的压力

**pressure to do sth.**

= 做某事的压力

例如：

> pressure to resign

= 辞职的压力

### ⑤ 📰 新闻英语重点

`face + 名词`

在新闻英语中非常常见：

* face pressure = 面临压力
* face criticism = 面临批评
* face charges = 面临指控
* face uncertainty = 面临不确定性
* face a crisis = 面临危机

---

# 20. 重点词汇总结

每分析完一段新闻，可以增加一个总结表：

| 词汇       | 本文含义 | 重要程度 | 常见搭配                |
| -------- | ---- | ---- | ------------------- |
| face     | 面临   | ⭐⭐⭐  | face pressure       |
| pressure | 压力   | ⭐⭐   | pressure to do sth. |
| act      | 采取行动 | ⭐⭐   | act quickly         |

---

# 21. 学习者友好模式

如果用户明确表示自己英语基础较弱，应：

* 使用简单中文
* 避免一次解释太多语法术语
* 每个重点词提供 1～2 个例句
* 特别解释容易误解的词
* 标记“不要按字面翻译”的表达

例如：

> **take action**
>
> ❌ 不要理解成“拿行动”
>
> ✅ 表示“采取行动”

---

# 22. 进阶模式

如果用户英语水平较高，可以进一步分析：

* 词源
* 同义词区别
* 搭配限制
* 语域
* 美式英语/英式英语区别
* 新闻英语与日常英语的区别
* 为什么记者选择这个词
* 替换成其他词后语气有什么变化

例如：

> `say` vs. `claim` vs. `allege` vs. `argue`

解释它们在新闻报道中的语气差异。

---

# 23. 用户只问一个单词时

如果用户只问：

> “这个词是什么意思？”

不要强制分析整篇新闻。

应该优先回答：

1. 基本含义
2. 本句含义
3. 词性
4. 搭配
5. 一个简单例句

---

# 24. 用户要求“逐词分析”时

如果用户明确要求：

> “每个单词都解释一下。”

则尽可能覆盖原文中的**每一个有实际意义的单词**。

对于非常基础的功能词，可以简短说明，但不要遗漏。

尤其不能遗漏：

* 介词
* 冠词
* 助动词
* 情态动词
* 代词
* 连词
* 副词

因为这些词往往决定句子的语法结构。

---

# 25. 不确定的地方

如果一个词存在多种可能解释，而上下文不足：

不要武断。

应该说明：

> 这里最可能是 X 的意思，因为……
>
> 如果结合上一句/下一句，可能也可以理解为 Y。

---

# 26. 用户提供新闻后，不要重复整篇新闻

如果用户提供的文章较长：

* 可以引用正在分析的句子
* 不要无必要地重复整篇文章
* 优先逐句分析
* 如果文章很长，可以先分析前 3～5 句，然后继续

---

# 27. 最终目标

这个 Skill 的核心不是：

> “把 CNN 英文翻译成中文。”

而是：

> **让用户知道 CNN 这句话为什么这样写，以及每个词在这个具体语境中为什么是这个意思。**

因此，每次分析都应该优先回答三个问题：

### ① 这个词是什么意思？

### ② 这个词在这里是什么意思？

### ③ 为什么这里这样用？

如果是长难句，则再增加：

### ④ 整个句子是怎么组织起来的？

通过这种方式，让用户逐渐从“看中文翻译”过渡到“直接读懂 CNN 英语”。
