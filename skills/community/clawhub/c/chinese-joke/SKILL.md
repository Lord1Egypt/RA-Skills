# 中文笑话库 Skill

## 概述

使用本地笑话数据库获取中文笑话，无需依赖外部 API。

## 笑话库

包含多种类型的中文笑话：
- 谐音梗
- 程序员笑话
- 生活趣事
- 脑筋急转弯
- 双关语

## 快速开始

### 使用 Bash

```bash
# 获取随机笑话
./scripts/joke.sh random

# 按类型获取
./scripts/joke.sh random --type pun      # 谐音梗
./scripts/joke.sh random --type program  # 程序员
./scripts/joke.sh random --type life     # 生活
./scripts/joke.sh random --type brain    # 脑筋急转弯
```

### 使用 Python

```bash
python3 scripts/joke.py random
python3 scripts/joke.py random --type program
```

## 笑话类型

- `pun` - 谐音梗/双关语
- `program` - 程序员/技术
- `life` - 生活趣事
- `brain` - 脑筋急转弯
- `story` - 短故事

## 示例

```bash
# 获取 5 个谐音梗
./scripts/joke.sh random --type pun --count 5

# 获取一个程序员笑话
./scripts/joke.sh random --type program
```

## 添加新笑话

编辑 `jokes.json` 文件添加新笑话：

```json
{
  "type": "pun",
  "joke": "你的笑话内容",
  "category": "可选分类"
}
```

## 相关链接

- 笑话库位于 `jokes.json`
- 可扩展添加更多类型
