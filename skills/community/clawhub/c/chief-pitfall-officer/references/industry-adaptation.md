# 行业适配指南 (分级加载路由)

本文件作为行业适配的索引入口。为优化上下文负载，具体的行业 SOP 已拆分至子目录。

---

## 1. 行业适配路由表

| 行业分类 | 核心子模块路径 | 包含内容 |
| :--- | :--- | :--- |
| **餐饮/零售** | `references/industries/catering.md` | 门店形象升级、新店开业 SOP、餐饮红线 |
| **电商/互联网** | `references/industries/digital.md` | 建站、私域体系、数据埋点、技术合规 |
| **制造业** | `references/industries/manufacturing.md` | 产线改造、质量体系、ERP/MES 导入 |
| **教育/培训** | `references/industries/education.md` | 课程研发、平台搭建、校区筹建合规 |
| **活动/会展** | `references/industries/events.md` | 公关活动、产品发布会、公安报批流程 |
| **房地产/建筑** | `references/industries/real-estate.md` | 项目开发、精装标准化、资质红线 |
| **直播带货** | `references/industries/livestream.md` | 品牌自播搭建、GMV 对赌、主播风控 |
| **城市更新/旧改** | `references/industries/urban-renewal.md` | 结构加固、历史保护红线、不可预见费管控 |
| **展览/门店改造** | `references/industries/exhibition.md` | 展厅设计、SI 标准化、多媒体集成审计 |
| **项目策划/咨询** | `references/industries/consulting.md` | 战略咨询、文旅全案、ROI 预估模型 |
| **医疗大健康** | `references/industries/healthcare.md` | 智慧医疗、GSP 合规、医疗数据隐私 |
| **金融科技** | `references/industries/fintech.md` | 信创改造、风控模型、金融数据一致性 |
| **政务数字化** | `references/industries/government.md` | 一网通办、数据入湖、总包审计 |

---

## 2. 跨行业组合通用规则

对于不在上表中的跨行业组合，按以下规则处理：

1. **确定主行业**：以核心交付物所在行业为主框架（如"做一场线上直播峰会"→活动策划为主，互联网为辅）
2. **分级加载**：先读取主行业子模块，根据需求深度再读取辅助行业子模块。
3. **角色合并**：两个行业的角色可能有重叠，合并为一个角色但职责覆盖两方面。
4. **流程不冲突**：如果两个行业的流程有冲突，以主行业流程为主，辅助行业要求作为检查项加入。
