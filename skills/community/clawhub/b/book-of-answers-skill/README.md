# 答案之书.skill

有些问题，适合被分析；有些问题，却只适合在夜深灯静时，交给一句恰到好处的话。

《答案之书.skill》想做的，正是这样一件温柔而克制的事。它不替人做决定，不夸张地许诺命运，也不试图用冗长的解释掩盖犹疑本身。它只是从电影的光影、文学的章节与音乐的旋律里，轻轻翻出一句带着出处的回答，让提问者在某个瞬间，恰好与一句话相遇。

当你问它明天会不会更好、旅行会不会顺利、是否该远行、是否该放下，它不会像一台冷冰冰的问答机那样给出结论，而更像一位深夜仍为你留灯的馆员，从不同书架之间替你抽出一页，交到你手里。也许那不是标准答案，却往往会成为当下最像答案的那一句。

这是一个基于纯文本交互的对话技能项目。当前版本内置三本书：

- `《电影答案之书》`
- `《文学答案之书》`
- `《音乐答案之书》`

它会在三本书之间随机翻页，也允许使用者指定其中一本来提问；回答始终保留出处，并以尽量简洁、稳定、可分享的形式呈现。

## 一句话简介

把问题轻轻放下，让电影、文学与音乐为你翻出一句带出处的回答。

## 功能特性

- 三书库模式：默认在电影、文学、音乐三本书之间随机抽取，也支持指定其中一本来提问
- 答案带出处：每次返回都会展示正文与出处
- 反重复/防刷：5 分钟内重复提问同一问题会直接返回上一次答案
- 换书追问：支持在上一题上下文上执行“那用电影版的再测一次”“换文学之书”“换音乐之书”
- 每日一签：从三本书中随机翻出一句今日指引
- 最小状态持久化：仅保存防刷与换书追问所需的最小上下文

## 数据说明

- 内置书库统一维护在 `data/books.json`
- 当前已整理为三套可直接调用的书库数据
- 每条答案都以 `{text, source}` 形式存储，并在回复时展示 `出处：...`

## 模块职责

- `main.py`：CLI 入口和对外暴露的 `handle_request`
- `service.py`：业务编排、意图处理、响应格式和状态更新
- `router.py`：显式选书、换书识别与默认随机路由
- `storage.py`：SQLite 最小状态持久化与脏数据恢复
- `tests/test_integration.py`：多轮状态流集成测试

## 快速开始

```bash
cd /Users/shaozhaoru/Documents/book-of-answers-skill
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

单次调用：

```bash
python3 main.py --user-id demo-user "明天会好吗"
```

启动欢迎语：

```bash
python3 main.py --user-id demo-user
```

交互模式：

```bash
python3 main.py --user-id demo-user --interactive
```

## 示例指令

- `明天会好吗`
- `用电影答案之书问明天会好吗`
- `请用文学答案之书回答我`
- `用音乐答案之书问我该放下吗`
- `那用电影版的再测一次`
- `换文学之书`
- `换音乐之书`
- `每日一签`

## 存储说明

- 默认数据库：`data/book-of-answers-skill.sqlite3`
- 默认仅保存 `last_question`、`last_answer`、`last_book`、`last_timestamp`
- 这些字段仅用于防刷与换书追问，不保留借阅历史记录
- 可通过环境变量覆盖数据库位置：

```bash
ANSWER_LIBRARY_DB=/tmp/book-of-answers-skill.sqlite3 python3 main.py --user-id demo-user "明天会好吗"
```

## 自定义书库

如需切换到你自己的外部书库文件：

```bash
ANSWER_LIBRARY_BOOKS=/absolute/path/to/books.json python3 main.py --user-id demo-user "明天会好吗"
```

## 校验与测试

运行单元测试：

```bash
python3 -m unittest discover -s tests
```

校验技能元数据：

```bash
python3 /Users/shaozhaoru/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/shaozhaoru/Documents/book-of-answers-skill
```

## 响应格式

常规问答严格输出：

```text
我感受到了你的困惑。
正在为你翻开 [book_name]...

它给你的指引是：
「 [答案正文] 」
出处：[出处]
```
