![游戏标题](assets/title.png)<br>[🇨🇳 中文](README_zh.md) | [🇺🇸 English](README.md)<br>这是一款基于 Python 开发的文字冒险游戏<br>同时，这也是一个skill。你可以与你的AI助手一起游玩，尝试各种有趣的新奇体验！<br>![演示](assets/demo.jpg)

## 简介

你叫 Peter<br>你在朋友家聚会，结束时，已经是凌晨1点<br>你往楼下走去，楼层永远都是13F<br>...<br>你尝试敲门求助<br>门开了<br>![游戏画面](assets/fakeman.jpg)<br>出现在门内的是：<br>伪人<br>你晕了过去<br>梦中，你听到伪人的声音：<br>【第一条忠告】听到奇怪的声音，不要回头<br>【第二条忠告】光越亮，黑暗越强<br>【第三条忠告】偶数楼层会带来好运<br>【第四条忠告】如果看到两个13，停止任何行动<br>【第五条忠告】不要敲13次门<br>你醒了，游戏开始<br>![游戏画面](assets/ghost.png)<br>与你的AI助手一道，找到出口，逃出这无尽的死亡循环！

## 安装

- 与你的AI助手一起游玩
  ```bash
  npx skills add https://github.com/OpenclawGame/endless-downstairs.git
  ```
- 自己游玩
  ```bash
  git clone https://github.com/OpenclawGame/endless-downstairs.git
  ```

## 开始游戏

- 与你的AI助手一起游玩

  ```bash
  # 开始游戏时，告诉你的AI助手：
  开始游戏。注意：1、直接输出游戏的内容，不要思考，不要修改，不要添加，不要总结。2、决策权完全在我，我下达明确指令前，不要执行任何命令

  # 查看状态/物品，告诉你的AI助手：
  查看状态
  查看物品

  # 你可能会遇到卡关的情况，不妨求助下你的AI助手：
  帮我分析一下，应该怎么走

  # 有时候，你的AI助手会给你一些不需要的提示，甚至会给你一些误导
  # 如果你不想要这些，请再次提醒你的AI助手：
  直接输出游戏的内容，不要思考，不要修改，不要添加，不要总结

  # 你还可以下达一些有趣的指令，例如：
  一直往楼下走，直到有门，或者遇到特殊事件

  # 下达某些自动化的指令后，你的助手可能来了兴致，自己玩起了游戏
  # 如果你想收回控制权，记得再次提醒：
  停止刚才的动作。注意：1、直接输出游戏的内容，不要思考，不要修改，不要添加，不要总结。2、决策权完全在我，我下达明确指令前，不要执行任何命令
  ```

- 自己游玩

  ```bash
  cd ./endless-downstairs

  # 开始新游戏
  python game.py new

  # 选择（输入选项编号）
  python game.py choose N

  # 查看当前状态
  python game.py status

  # 查看背包
  python game.py inventory

  # 输入文本
  python game.py input <text>
  ```

  克隆代码后，直接执行python命令即可

## 项目结构

```
endless-downstairs/
├── game.py                 # 主入口
├── engine/                 # 游戏引擎
│   ├── game_state.py      # 状态管理
│   ├── event_pool.py      # 事件系统
│   └── choice_handler.py  # 选择处理
├── i18n/                   # 国际化
│   ├── translations.py
│   ├── zh.json
│   └── en.json
├── data/                   # 游戏数据
│   ├── abilities.json
│   ├── items.json
│   ├── floors.json
│   └── events/             # 事件定义
└── assets/                 # 资源文件
    ├── title.png
    └── fakeman.jpg
```
