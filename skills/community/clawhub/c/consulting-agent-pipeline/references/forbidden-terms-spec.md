# Forbidden Terms Spec — 禁用词机制

> 首钢吉泰安项目的惨痛教训：G1/G2/G3/G4 内部代号泄漏到 v4 才被发现。禁用词机制确保每轮审核自动扫描，零泄漏。

## FORBIDDEN_TERMS.yaml 格式

```yaml
schema_version: "1.0"
enforcement: all-rounds  # all-rounds | final-only
created: "2026-04-09"
updated: "2026-04-13"
terms:
  internal_codes:
    - G1           # 内部调研代号：污泥专题
    - G2           # 内部调研代号：硫酸亚铁专题
    - G3           # 内部调研代号：行业ESG横向评分
    - G4           # 内部调研代号：上市ESG披露要求
    - T2           # 内部代号：六安T2水量水质联动
    - T3           # 内部代号：六安T3行政边界
    - T4           # 内部代号：六安T4合同核查
    - E-6          # 内部参考代号：联合利华灯塔工厂方案
    - FMP          # 内部参考代号：Figma Make Prompt
    - E-4          # 内部参考代号
    - v4           # 版本代号（交付物中不应出现）
    - v5           # 版本代号（交付物中不应出现）

  reference_names:
    - 联合利华          # 内部参考来源，不应出现在交付物正文中
    - 原始听记
    - 任务书
    - 主线稿
    - 精简稿
    - 协作包
    - 导航与协作

  risk_expressions:
    - pattern: "\\d+万元.*奖励"
      note: "政策金额须标注'正式申报前待核'，且不得作为已适用收益写进主叙事"
    - pattern: "深交所|上交所|北交所"
      note: "不预设企业上市路径，交易所内容仅作公开披露规则参考"
    - pattern: "IPO"
      note: "不在概念规划阶段使用"
    - pattern: "Wind"
      note: "非公开数据源，不得作为交付物引用"
    - pattern: "立即可行|马上|立刻"
      note: "不得作为确定性结论，应改为'技术路径清晰，待XX确认'"
    - pattern: "唯一|绝对|必然"
      note: "高风险绝对化表述，降为条件性表述"
    - pattern: "通常可低于\\d+年"
      note: "ROI表述降为'较短周期内'，避免具体年数承诺"
```

## 三类禁用词

| 类型 | 示例 | 风险等级 | 处理方式 |
|------|------|---------|---------|
| `internal_codes` | G1/G2/G3/G4 | 🔴 P0 | 绝对禁止出现，一经发现立即退回 |
| `reference_names` | 联合利华/任务书/协作包 | 🔴 P0 | 仅允许出现在交接文档，不允许出现在交付物 |
| `risk_expressions` | "深交所"/"3000万元奖励"/"IPO" | 🟡 P1 | 有条件使用，须满足 note 中的约束 |

## 扫描执行流程

```
每轮交付物完成 →
  forbidden-terms-scan.sh 扫描所有产出文件 →
  发现 P0 违规 → status: failed → 立即退回修复 →
  发现 P1 违规 → 标注在 audit handoff 中 →
  全部通过 → status: completed → 进入下一阶段
```

## enforcement 模式

```yaml
enforcement: all-rounds  # 强烈推荐：每轮审核都扫描
# enforcement: final-only  # 不推荐：只在终审扫描，首钢吉泰安教训
```

## 首钢吉泰安实际扫描记录

2026-04-10 晚间收口（v4→v5），Claude 第三轮审核后执行扫描：

| 扫描项 | 发现 | 处理 |
|--------|------|------|
| G1/G2/G3/G4 | P16/P17/P18 正文中 3 处 | 立即清除 |
| E-6/FMP/联合利华/原始听记 | 全套脚注中 12 处 | 立即清除 |
| "通常可低于1年" | P16 ROI 表述 | 降调为"较短周期内" |
| "100万元绿色工厂奖励" | P10 页 | 标注"正式申报前待核" |
| "深交所/IPO" | P5 雷达图数据 | 删除，改写为"交易所可持续披露规则持续趋严" |

教训总结：必须在每轮交接时都扫描，不能只在最终交付时扫描。

## 扫描执行时机表

| 时机 | 由谁执行 | 说明 |
|------|---------|------|
| 项目初始化后 | 编排者 | 确认 FORBIDDEN_TERMS.yaml 已创建且非空 |
| 每次产物构建后 | 执行Agent | 构建完成后立即扫描（可通过 Claude Code PostToolUse hook 自动化） |
| 每轮审核中 | 审核Agent | 审核报告必须包含禁用词扫描结果段 |
| 交付前 | 编排者 | 最终确认扫描 |
| 发现新禁用词时 | 任何Agent | 立即追加到 FORBIDDEN_TERMS.yaml 并通知团队 |

## 新增禁用词流程

1. 任何Agent在工作中发现应禁用的词汇（如审核时发现新的内部代号泄漏）
2. 在当前交接文档的"约束与禁区"节标注：`建议新增禁用词: XXX，原因: YYY`
3. 编排者（Orion/Leroy）确认后追加到 FORBIDDEN_TERMS.yaml 的对应类别
4. 下一次 `forbidden-terms-scan.sh` 执行时自动生效，无需修改脚本
