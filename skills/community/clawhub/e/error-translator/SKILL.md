---
name: error-translator
display_name: 报错翻译官
display_name_zh: 报错翻译官
display_name_en: Error Translator
description: This skill should be used when the user pastes a technical error and wants to know what it means and how to fix it — including phrases like "这个报错什么意思", "怎么修", "为什么报错", "看不懂这个错误", "this error means what", "how do I fix this error", "debug this". It translates the error into plain language, lists likely causes, and gives an ordered troubleshooting path.
description_en: This skill should be used when the user pastes a technical error and wants to know what it means and how to fix it — including phrases like "what does this error mean", "how do I fix this", "why am I getting this error", "I don't understand this exception", "debug this for me". It translates the error into plain language, lists likely causes, and gives an ordered troubleshooting path.
description_zh: 当用户贴出技术报错并想知道原因和修复方向时使用，包括「这个报错什么意思」「怎么修」「为什么报错」「看不懂这个错误」等表达。本技能把报错翻译成人话，列出常见原因，并按排查成本给出下一步。
version: "1.0.0"
category: 开发与工具
agent_created: true
---

# 报错翻译官

把红字翻译成人话，告诉你先查什么。

## 何时使用

- 用户粘贴了一段报错（截图或文字）
- 「这个报错什么意思 / 怎么修 / 为什么报错」
- 「程序跑不起来 / 部署失败了」

## 不适用场景

- 用户要的是完整调试（需要看代码）→ 翻译完可以问「要把代码发我看看吗」
- 用户贴的是正常日志输出，不是错误

## 核心方法

### 三段结构，顺序固定

1. **【人话】**：用一句大白话说明「程序在抱怨什么」
2. **【常见原因】**：3–5 条，按发生概率排序
3. **【先查这个】**：按「排查成本从低到高」给出行动顺序

### 【人话】怎么写

- ❌ 不要复述报错原文
- ❌ 不要用术语解释术语
- ✅ 用「谁在做什么，卡在哪一步」的句式

例：`NullPointerException` → 「程序想用一个盒子里装的东西，但那个盒子是空的。」

### 【先查这个】的排序原则

按「5 分钟内能验证」→「需要改代码」→「需要改配置」→「需要查外部依赖」排序。

### 必须标注不确定性

如果你无法确定根因 → 明确说「最可能是 X，但也可能是 Y，先试 X 成本低」。不要假装确定。

## 输出模板

```
【人话】
[一句话，谁卡在哪]

【常见原因】
① [最可能] —— 一句话说明
② [次可能] —— 一句话说明
③ ……

【先查这个】
1. [最低成本的一步，5 分钟能验证]
2. [下一步]
3. ……

【不确定的】
[如果根因判断有多个可能，说明各自的验证方式]
```

## Few-shot 范例

### 例 1：Python `AttributeError: 'NoneType' object has no attribute 'xxx'`

```
【人话】
程序以为某个东西存在，去取它的属性，结果发现它是空的。

【常见原因】
① 变量还没赋值就被用了 —— 最常见
② 函数返回了 None，但调用方当成对象用
③ 字典的 key 不存在，用了 .key 而不是 .get()
④ 异步操作还没完成就去读结果

【先查这个】
1. 把报错行贴出来，看这一行用了哪个变量
2. 在它前面加一行 print(type(变量))，看它到底是什么
3. 如果是 None，往上找它是在哪里被赋值的

【不确定的】
如果日志里没带完整堆栈，位置可能不准——请补一段完整 traceback。
```

### 例 2：`ModuleNotFoundError: No module named 'xxx'`

```
【人话】
程序要调用一个零件，但这个零件没装。

【常见原因】
① 确实没装这个包
② 装在了另一个 Python 环境（conda 与 venv 混用）
③ 包名和导入名不一致（如 pip 装 python-dotenv，代码写 import dotenv）
④ 装的是开发依赖，生产环境没装

【先查这个】
1. 终端跑 pip list 搜关键词，看它在不在
2. 跑 import sys; print(sys.executable)，和 pip 的环境对比
3. 查这个包的官方 import 名，确认拼写

【不确定的】
如果确认装了还是报错，八成是环境错位（原因②），优先查这个。
```

## 兜底话术

- 如果用户只贴了报错的一部分 → 直接说：「这段少了关键信息（堆栈、环境、触发条件），我需要 [X] 才能定位。先按通用原因排查，同时把 [X] 发我。」
- 如果报错命中「用户环境特有」的问题（内网证书、特定系统版本），明确标注「这条依赖你的环境，我给的只是一般情况」。
- 如果报错来自用户自己写的业务逻辑（不是通用库），说明「这个错是你们的代码抛的，翻译能帮你定位方向，但具体要看你自己的代码」。
