# English Learning Check-in Skill

每日英语学习打卡工具，基于 learning-checkin 实现，专为英语学习者设计。

## 功能概述

1. **每日打卡** - 记录英语学习完成情况
2. **学习类型** - 支持托福、雅思、PET、新概念等多种英语学习类型
3. **名言激励** - 每日由 Agent 自动生成英语名言（中英对照），确保不重复

## 项目结构

```
english-learning-checkin/
├── SKILL.md              - 本文档
├── english_checkin.py    - 主程序
└── data/                 - 数据目录（自动创建）
    ├── config.json       - 用户配置
    └── quotes_used.json  - 已使用名言记录
```

## 安装说明

### 1. 安装本 Skill

将本 Skill 目录复制到你的 Skill 目录中。

### 2. 安装依赖

本 Skill 依赖 [learning-checkin](https://clawhub.ai/daizongyu/learning-checkin)，需要先安装该 Skill。

### 3. 配置路径

由于不同工具的 Skill 目录位置不同，需要通过以下方式指定 learning-checkin 的路径：

**方式一：命令行参数**
```bash
python english_checkin.py --learning-checkin-path /path/to/learning_checkin.py checkin
```

**方式二：环境变量**
```bash
export LEARNING_CHECKIN_PATH=/path/to/learning_checkin.py
```

**方式三：放置在同一目录**
将 learning-checkin 目录放在本 Skill 同一目录下：
```
your-skill-dir/
├── english-learning-checkin/
│   └── english_checkin.py
└── learning-checkin/
    └── learning_checkin.py
```

## 命令列表

| 命令 | 说明 |
|------|------|
| `python english_checkin.py init` | 初始化（首次使用） |
| `python english_checkin.py checkin [学习类型]` | 打卡（如：checkin 托福） |
| `python english_checkin.py status` | 查看状态 |
| `python english_checkin.py used-quotes` | 获取已使用名言列表 |
| `python english_checkin.py record-quote [名言]` | 记录已使用的名言 |
| `python english_checkin.py set-type [类型]` | 设置学习类型 |
| `python english_checkin.py check` | 检查依赖 |

## 使用说明

### 1. 首次使用（初始化）

```bash
python english_checkin.py --learning-checkin-path /path/to/learning_checkin.py init
```

### 2. 每日打卡

1. 获取已使用名言：
   ```bash
   python english_checkin.py used-quotes
   ```

2. 生成今日名言（由 Agent 自动生成，确保不重复）

3. 执行打卡：
   ```bash
   python english_checkin.py --learning-checkin-path /path/to/learning_checkin.py checkin 托福
   ```

4. 记录名言：
   ```bash
   python english_checkin.py record-quote "Practice makes perfect"
   ```

### 3. 查看学习状态

```bash
python english_checkin.py --learning-checkin-path /path/to/learning_checkin.py status
```

## 版本

当前版本：1.0.0