# 信息中心（数据 Owner）· 快速通道

你管数据的真实性与权限。这份工具给你的不是建模任务，而是**三份以你为准的报告和一个闭环文件**。

## 你的 4 个触点

**1. 数据画像（先看库里到底什么样）**
```bash
python scripts/profile_db.py --db physical.db --out profile.yaml
```
每张表的行数、枚举列实测取值、空值率、疑似时间列。
用途：建模前核对"库里长的"和"业务说的"是不是一回事。敏感字段名启发式仅供参考，不等于脱敏结论。

**2. 结构漂移巡检（上游改表了没有）**
```bash
python scripts/check_consistency.py --model semantic.yaml --db physical.db
```
ERROR = 模型引用的表/字段在库里不存在了（必须处理）；
WARN = 库里有模型没声明的新列等（评估后决定要不要纳入）。

**3. 约束验证报告（数据质量的可信凭据）**
```bash
python scripts/check_constraints.py --model semantic.yaml --db physical.db --out constraints.json
```
主键唯一性、枚举字典、引用完整——全量快照实证，带 NULL 策略。
空表、无规则、执行错误都**不算通过**（报告会如实写"未验证"）。

**4. gaps.yaml 是给你的闭环依据**
建模过程中凡涉及数据来源、结构、时效、权限的未决问题，都会汇总成
`gaps.yaml` 里 `owner_role: 信息中心` 的条目——你确认哪条，哪条才从"候选"变"事实"。

## 权限边界（已在工具层落地）

- 脚本对数据库只执行**只读聚合查询**（SELECT COUNT/SUM/AVG），连接以只读模式打开
- 网络访问默认仅本机/内网，远程必须显式 `--allow-remote`
- 完整声明见仓库根目录 [SECURITY.md](../SECURITY.md)，可直接作为安全审查材料

## 一句话记住

**任何关于数据来源的结论，你确认才算数；工具负责把"你没确认"这件事写得明明白白。**
