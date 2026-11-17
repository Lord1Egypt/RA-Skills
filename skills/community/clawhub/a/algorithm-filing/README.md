# Algorithm Filing — 大模型算法备案助手

[![Skill Type](https://img.shields.io/badge/type-workbuddy%20skill-blue)](https://github.com/bettermen/algorithm-filing)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/bettermen/algorithm-filing)

AI 大模型 / 算法合规备案全流程助手。帮助企业和开发者在中国网信办完成大模型备案、大模型登记、算法备案，涵盖从类型判定到持续合规的全生命周期管理。

## 功能

- **备案类型判定** — 根据产品形态自动判断大模型备案 / 大模型登记 / 算法备案 / 双新评估
- **材料清单生成** — 20 项完整材料清单，标注优先级、耗时预估和易错点
- **安全评估报告框架** — 基于 GB/T 45654-2025，7 章完整大纲，逐项填充指引
- **填报流程指引** — 5 步系统填报流程，含审核时间线与关键卡点预警
- **驳回应对** — TOP10 驳回原因 + 整改方案 + 10 条一次通过黄金法则
- **持续合规管理** — 公示义务 / 变更管理 / 年度自查 / 注销流程

## 触发词

算法备案、大模型备案、大模型登记、深度合成备案、生成式AI备案、beian.cac、安全评估报告、算法合规、备案材料、备案流程

## 依赖法规

| 法规/标准 | 发布年份 |
|-----------|---------|
| 《生成式人工智能服务管理暂行办法》 | 2023 |
| 《互联网信息服务深度合成管理规定》 | 2023 |
| 《互联网信息服务算法推荐管理规定》 | 2022 |
| GB/T 45654-2025 生成式人工智能服务安全基本要求 | 2025 |

## 结构

```
algorithm-filing/
├── SKILL.md                                 # 核心指令文件
├── README.md                                # 本文件
└── references/
    ├── laws-and-standards.md                # 法规速查表
    ├── material-checklist.md                # 完整材料清单
    ├── security-assessment-framework.md     # 安全评估报告框架
    ├── filing-workflow.md                   # 分步填报流程指引
    ├── common-rejection-reasons.md          # 高频驳回原因与应对
    └── post-filing-compliance.md            # 备案后持续合规管理
```

## 安装

将整个目录放入 WorkBuddy 的 skills 目录：

```bash
# 用户级（推荐）
cp -r algorithm-filing ~/.workbuddy/skills/

# 项目级
cp -r algorithm-filing .workbuddy/skills/
```

## License

MIT
