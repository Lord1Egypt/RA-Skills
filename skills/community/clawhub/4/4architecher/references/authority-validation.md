# Authority Validation Reference

## 目录

- 使用原则
- 来源分级
- 常用权威源样例
- 检索与校验流程
- 不同问题的证据门槛
- 记录格式
- 禁止事项

## 使用原则

把外部资料校验视为架构输出的质量闸门，而不是附加装饰。

目标不是堆砌链接，而是验证以下内容：

- 关键业务假设是否符合行业现实
- 关键应用能力是否符合已知产品与生态边界
- 关键数据要求是否符合监管、合规或治理常识
- 关键技术方案是否符合官方能力、标准规范或部署约束

只校验会显著影响架构结论的主张，不要为了“看起来有引用”而做无意义搜索。

## 来源分级

### A 级：优先级最高的一手来源

- 官方产品文档、官方 API 文档、官方白皮书
- 法律法规、监管机构公告、官方标准文本
- 标准组织文档，如 ISO、NIST、W3C、IETF、CNCF、行业协会标准
- 公司正式披露文件，如年报、招股书、财报电话会纪要、官网方案页

适用于：

- 产品能力确认
- 技术限制确认
- 合规要求确认
- 标准协议确认

### B 级：高可信二手来源

- Gartner、Forrester、IDC、G2 等研究或分析
- Accenture、McKinsey、BCG、Deloitte、IBM 等头部机构研究
- 高质量行业报告、官方合作伙伴解决方案说明

适用于：

- 行业趋势
- 成熟度判断
- 标杆案例和能力分层

### C 级：仅作补充背景

- 主流媒体报道
- 技术博客
- 社区讨论
- 个人文章

只用于补充语境，不单独支撑关键结论。

## 常用权威源样例

按问题类型优先选择：

### 架构描述与视角组织

- ISO/IEC/IEEE 42010:2022
  https://www.iso.org/standard/74393.html
- The Open Group TOGAF Standards
  https://publications.opengroup.org/standards/togaf
- The Open Group 关于 TOGAF 与 ArchiMate 互补关系的官方说明
  https://help.opengroup.org/hc/en-us/articles/32115987894930-How-the-ArchiMate-Language-and-the-TOGAF-Standard-Complement-Each-Other

### 业务架构

- Business Architecture Guild
  https://www.businessarchitectureguild.org/
- Business Architecture Guild 行业参考模型
  https://www.businessarchitectureguild.org/page/INDREF

### 数据架构与治理

- DAMA-DMBOK 官方介绍
  https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/
- DAMA 官方站点
  https://dama.org/

### AI、风险与安全架构

- NIST AI RMF
  https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- NIST Zero Trust Architecture
  https://www.nist.gov/publications/zero-trust-architecture
- NIST Cybersecurity Framework
  https://www.nist.gov/cyberframework

### 行业或地区监管

- 优先使用适用地区的法律法规、监管机构官网、行业主管机关公告
- 如果是中国语境，优先国务院部门、国家标准全文公开系统、网信、工信、金融监管等官方渠道

## 检索与校验流程

1. 先把待验证内容改写成“主张”。
2. 判断主张类型：监管、产品能力、标准、市场、竞品、实施案例。
3. 先搜 A 级来源；找不到时再搜 B 级来源。
4. 记录每条来源对应支持或反驳了什么。
5. 如果来源之间冲突，优先使用日期更近、权威级别更高、与本地区或本行业更匹配的来源。
6. 最终把“证据支持结论”和“仍属推断的建议”分开写。

## 不同问题的证据门槛

### 监管 / 合规 / 法律

- 只用 A 级来源
- 必须写明适用地区和日期

### 技术标准 / 云服务能力 / API 约束

- 至少 1 条 A 级来源
- 涉及重要架构决策时，再补 1 条独立来源

### 竞品能力 / 市场格局 / 行业趋势

- 至少 1 条 A 级或官方产品页
- 最好补 1 条 B 级研究报告交叉验证

### 咨询式最佳实践

- 至少 1 条 A 级或 B 级来源
- 必须标记哪些是“证据支持”，哪些是“架构建议”

## 记录格式

在最终交付里增加一张证据表：

| 待验证主张 | 来源级别 | 来源名称 | 日期 | 支持结论 | 对架构的影响 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

必要时再补：

- 仍未解决的不确定性
- 本次未能获取的一手资料
- 需要用户补充的内部材料

## 禁止事项

- 不要用单一博客支撑关键架构结论
- 不要把过时资料当成当前事实
- 不要把“常见做法”写成“官方要求”
- 不要把咨询经验包装成外部权威结论
- 不要只列链接而不说明这些链接支持了什么
