# LanguagelearningWhenCoding - 双语学习 Skill

当用户调用此 Skill 时，Agent 会在最终输出前强制进行双语学习处理。

## 项目结构

```
cn-en/
├── lib/
│   └── core.py          # 词库核心模块
├── data/                # 词库数据存储
├── scripts/
│   ├── cli.py           # CLI 工具 (add/delete/exchange/list/clear)
│   ├── exam.py          # 考试系统
│   ├── dice.py          # 随机生成器
│   └── skill.py         # Skill 主入口
└── README.md
```

## 词库格式

```json
{
  "id": "a1b2c3d4",
  "name": "apple",
  "pos": "n.",
  "field": "fruit",
  "book": "default",
  "added_time": "2026-05-13 19:00:00"
}
```

## 架构流程

```
难度调整层 → 选择题型层 → 考试层 → 双语输出
```

### 难度调整层

| 等级 | 名称 | 考试触发率 |
|------|------|-----------|
| rare | 稀少 | 30% |
| medium | 中等 | 50% |
| dense | 密集 | 80% |

### 选择题型层

| 类型 | 名称 | 概率 |
|------|------|------|
| pure_l1 | 纯第一层(检测生词层) | 40% |
| pure_l2 | 纯第二层(考考你层) | 40% |
| hybrid | 混合型 | 20% |

### 考试层

| 题型 | 行为 |
|------|------|
| pure_l1 | 直接执行检测层，**不调用随机筛子** |
| pure_l2 | 直接执行测验层，**不调用随机筛子** |
| hybrid | 两层都执行，但**顺序随机打乱**（调用随机筛子） |

1. **检测生词层**: 偶尔混杂语言，双语输出，检测用户不会的生词并自动加入生词库
2. **考考你层**: 从生词库随机抽题测试用户

**重要**：只有 hybrid 模式才调用随机筛子打乱顺序。

## CLI 使用

```bash
# 添加单词到生词库
python scripts/cli.py add apple n. fruit default

# 列出生词库
python scripts/cli.py list -n

# 列成熟词库
python scripts/cli.py list -k

# 删除生词库中的单词
python scripts/cli.py delete apple -n

# 生词库转熟词库
python scripts/cli.py exchange apple -n -k

# 熟词库转生词库
python scripts/cli.py exchange apple -k -n

# 清空词库
python scripts/cli.py clear -n   # 清空生词库
python scripts/cli.py clear -k   # 清空熟词库
```

## 运行考试

```bash
python scripts/exam.py medium
python scripts/exam.py rare
python scripts/exam.py dense
```

## 随机筛子

```bash
python scripts/dice.py          # 掷D6
python scripts/dice.py demo     # 演示模式
```

## 数据文件

- `data/new_words.json` - 生词库
- `data/known_words.json` - 熟词库
