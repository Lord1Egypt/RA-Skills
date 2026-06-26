# 飞书英语游戏集成说明

这个 skill 用在飞书 / Lark 群聊里的英语游戏场景。

## 启动原则

- 用户说“英语游戏”时，优先进入模式选择。
- 只问最少的问题。
- 如果用户已经说了模式，就不要重复确认。
- 如果用户没说难度，默认 `cet6`。
- 不要输出 JSON。
- 不要把脚本原始返回直接贴到飞书。
- 最终发到飞书的一定是自然语言。

## 模式入口

统一建议入口：`/english`

推荐子命令：
- `/english start`
- `/english start vocab`
- `/english start guess`
- `/english start speaking`
- `/english hint`
- `/english pass`
- `/english stop`
- `/english rank`

## vocab 模式

开始时只给：
- 难度
- 单词长度
- 剩余次数

每次有人猜词：
- 调 `scripts/english_game.py vocab-score`
- 根据结果更新棋盘
- 继续等下一次猜词

猜中或结束后补：
- 音标
- 词性
- 中文释义
- 近义词
- 反义词（适合时再给）
- 英文例句

## guess 模式

默认使用 definition。

发题方式更像群聊抢答：
- 一次发一条 clue
- 不需要大棋盘
- 答对后再给学习总结

## speaking 模式

- 先发一个简短口语任务
- 用户发语音
- 下载语音后调用 `scripts/asr_transcribe.py`
- 用识别文本做反馈
- 反馈要短、自然、可执行

反馈建议结构：
1. 我听到的是
2. 是否表达清楚
3. 一个改进点
4. 一个更自然版本

## 上下文记忆

Claw 自己维护会话上下文：
- 当前模式
- 当前难度
- 目标词 / 题目
- 历史猜测
- 已经给过的提示
- 当前局是否仍在进行

正常情况下不要让用户重复上下文。
