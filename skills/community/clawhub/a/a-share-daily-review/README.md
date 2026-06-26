# A股每日复盘模板

7种专业复盘风格的 Markdown 模板生成器。

## 安装

将本文件夹放入 OpenClaw skills 目录：
```bash
cp -r a-share-daily-review ~/.openclaw/workspace/skills/
```

## 使用

```bash
# 生成完整复盘模板（职业交易员版）
/a-share-review

# 指定复盘类型
/a-share-review --type 情绪      # 短线情绪流
/a-share-review --type 龙头      # 龙头战法
/a-share-review --type 趋势      # 趋势交易
/a-share-review --type 数据      # 量化数据
/a-share-review --type 个人      # 个人交易复盘
/a-share-review --type 游资      # 顶级游资复盘（14模块完整版）⭐推荐
/a-share-review --type 完整      # 完整复盘（默认）

# 指定输出路径
/a-share-review --type 游资 --output ~/my-review.md
```

## 复盘类型

| 类型 | 特点 | 模块数 |
|------|------|--------|
| 情绪 | 涨停数、连板梯队、炸板率、热点题材 | 6 |
| 龙头 | 龙头周期、梯队结构、分歧/加速判断 | 4 |
| 趋势 | 板块趋势、强势股、回踩/突破买点 | 4 |
| 数据 | 核心数据统计、成功率分析 | 6 |
| 个人 | 今日操作、对错总结、改进计划 | 6 |
| 游资 | 14模块完整框架，覆盖所有维度 ⭐ | 14 |
| 完整 | 精简综合框架 | 9 |

## 顶级游资复盘核心

**只抓3个东西：**
1. 情绪周期 — 市场处在什么阶段
2. 龙头是谁 — 资金围绕谁
3. 明天怎么玩 — 资金可能去哪里

**14模块：** 指数→情绪→梯队→题材→龙头→赚钱效应→亏钱效应→资金→轮动→信号→推演→计划→个人→总结

## 输出

文件保存至 `~/a-share-reviews/YYYY-MM-DD-{type}.md`

## 依赖

- Python 3.8+
- 无第三方依赖
