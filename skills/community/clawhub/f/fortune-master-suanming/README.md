# fortune-master-suanming 🔮

八字命理专业分析技能。

专注八字/四柱命理分析，每个结论都有推理说明和经典依据。

---

## 适用场景

- 八字/四柱命理分析
- 大运流年运势
- 具体年份的婚姻/财运/健康/事业
- 人生重要节点规划

---

## 核心功能

### 基础分析（8 个模块）

| 模块 | 功能 |
|------|------|
| 日主旺衰 | 得令/得地/得势评分 |
| 调候分析 | 穷通宝鉴调候用神 |
| 格局分析 | 真假 + 层次评分 |
| 十神配置 | 力量百分比 |
| 用神选取 | 调候 + 扶抑综合 |
| 地支藏干 | 透干/通根分析 |
| 合冲刑害 | 五合/六合/六冲/相刑/六害 |
| 气势清浊 | 流通性/清纯度/有情度 |

### 大运流年（2 个模块）

| 模块 | 功能 |
|------|------|
| 大运排盘 | 起运时间 + 大运评分 |
| 大运流年 | 配合分析 + 节点判断 |

### 具体年份分析（8 维度）

| 维度 | 功能 |
|------|------|
| 婚姻感情 | 具体哪几年容易结婚/波动 |
| 财运 | 具体哪几年赚钱顺利/破财 |
| 健康状况 | 具体哪几年身体好/需注意 |
| 人际贵人 | 具体哪几年贵人旺/小人多 |
| 居住搬迁 | 具体哪几年容易搬迁/稳定 |
| 官司是非 | 具体哪年是非多/少 |
| 福禄寿数 | 具体哪年福厚/福减 |
| 大运流年 | 具体哪几年上升/压力/节点 |

### 增强功能（3 个）

| 功能 | 说明 |
|------|------|
| 经典引用 | 八字经典（原文 + 白话 + 应用） |
| 推理说明 | 每个结论说明为什么（规则 + 原局 + 推导） |
| 象法分析 | 干支象/十神象/宫位象/刑冲合害象 |

---

## 分析流程

```
用户八字
    ↓
1-8. 基础分析（旺衰/调候/格局/十神/用神/藏干/合冲/气势）
    ↓
9-10. 大运流年（排盘 + 整合分析）
    ↓
11-18. 具体年份 8 维度分析
    ↓
综合判断 → 具体应事（精确到年月）
```

---

## 使用示例

### S 级深度分析

```
用户提供：
- 农历：1990 年 5 月 15 日 巳时
- 出生地：北京市
- 性别：男
- 想看：全面分析

AI 自动启用：
1. 日主旺衰分析（附推理说明）
2. 调候分析（附推理说明）
3. 格局分析（附推理说明）
4. 十神配置分析（附推理说明）
5. 用神选取（附推理说明）
6. 地支藏干详解（附推理说明）
7. 合冲刑害分析（附推理说明）
8. 气势流通判断（附推理说明）
9. 大运排盘与整合（附推理说明）
10. 大运流年整合分析（附推理说明）
11-18. 具体年份 8 维度分析（附推理说明）
```

### A 级标准分析

```
用户提供：
- 出生年月日时
- 想看：事业财运

AI 自动启用：
1-8. 基础分析（简化版）
9-10. 大运流年（当前大运 +3 流年）
11-18. 具体年份分析（重点事业财运）
```

---

## 文件结构

```
fortune-master-suanming/
├── SKILL.md                          # 主技能说明
├── README.md                         # 使用说明
├── CHANGELOG.md                      # 更新日志
├── CLAUDE.md                         # Claude 专用指南
├── _meta.json                        # 元数据
└── references/                       # 29 个八字框架文件
    ├── bazi-framework.md             # 八字基础
    ├── bazi-classics-framework.md    # 八字经典
    ├── bazi-detailed-framework.md    # 八字详细
    ├── bazi-xiangfa-framework.md     # 八字象法
    ├── bazi-deep-analysis-guide.md   # 深度分析指南
    ├── classic-books-integration.md  # 经典著作整合
    ├── classic-citation-framework.md # 经典引用规范
    ├── reasoning-explanation-framework.md # 推理说明
    ├── wuxiang-shengke-framework.md  # 五行生克
    ├── dizhi-canggan-framework.md    # 地支藏干
    ├── tiangan-xingchong-framework.md # 天干刑冲
    ├── dayun-liunian-framework.md    # 大运流年
    ├── shensha-framework.md          # 神煞详解
    ├── liuqin-framework.md           # 六亲关系
    ├── geju-analysis-framework.md    # 格局分析
    ├── geju-yingtui-framework.md     # 格局应事
    ├── comprehensive-analysis-framework.md # 综合分析
    ├── comprehensive-inference-framework.md # 综合推断
    ├── annual-detailed-analysis-v2.md # 年度详细分析
    ├── case-studies-framework.md     # 案例库
    ├── terminology-glossary.md       # 术语词典
    ├── faq.md                        # 常见问题
    ├── intake-and-routing.md         # 分流规则
    ├── safety-and-ethics.md          # 安全伦理
    ├── output-templates.md           # 输出模板
    ├── output-templates-v3.md        # v3 输出模板
    ├── quick-reference.md            # 快速查询表
    └── xiangfa-analysis-framework.md # 象法分析
```

---

## 版本信息

- **当前版本：** 1.0.0
- **作者：** OpenClaw Community
- **许可：** MIT-0

---

⚠️ **免责声明：** 本技能提供的分析仅供娱乐和文化研究使用，请理性对待命理分析，不能作为医疗、法律、投资等专业建议。
