# 08 术语表与 FAQ

> 用途：术语速查 + 高频疑问。配套工具命令 `--help` 可看全部命令。

## 1. 术语表

| 术语 | 全称/含义 |
|---|---|
| SaMD | Software as a Medical Device，软件即医疗器械 |
| AiMD | AI/ML-based Medical Device，AI/ML 医疗器械 |
| GMLP | Good Machine Learning Practice，良好机器学习实践（IMDRF） |
| IMDRF | 国际医疗器械监管机构论坛 |
| TPLC | Total Product Life Cycle，全生命周期管理 |
| PCCP | Predetermined Change Control Plan，预定变更控制计划（FDA） |
| PACMP | Post-Approval Change Management Protocol，上市后变更管理协议（日本 PMDA） |
| SBOM | Software Bill of Materials，软件物料清单 |
| QMSR | Quality Management System Regulation（FDA 2026-02 起） |
| CER | Clinical Evaluation Report，临床评价报告 |
| PMCF | Post-Market Clinical Follow-up，上市后临床跟踪 |
| PSUR | Periodic Safety Update Report，定期安全性更新报告 |
| RWD/RWE | 真实世界数据/证据 |
| CDSS | Clinical Decision Support System，临床决策支持系统 |
| Locked AI | 锁定型 AI（部署后不更新） |
| Adaptive AI | 自适应 AI（持续学习更新） |
| Data Leakage | 数据泄露（训练/测试集混淆） |
| De Novo | FDA 创新中低风险产品路径 |
| 510(k) | FDA 实质等同上市前通知 |
| PMA | FDA 上市前批准（高风险） |
| EUDAMED | 欧盟医疗器械数据库 |
| UDI | 唯一器械标识 |
| EU REP | 欧盟授权代表 |
| RTA | Refuse to Accept，不予受理（FDA 网络安全缺失时） |

## 2. FAQ

**Q：所有医疗 AI 软件都必须注册吗？**
看是否构成 SaMD（医疗目的软件）。纯健康管理、生活方式建议类一般不构成；涉及诊断/治疗/疾病监测/用药建议的通常构成。拿不准先做三地分类评估（01/02/03/04 模块）。

**Q：510(k) 和 De Novo 怎么选？**
有实质等同产品 → 510(k)；无实质等同但中低风险创新 → De Novo（获批后自身成谓词器械）；高风险/自主诊断 → PMA。

**Q：FDA 的 PCCP 能在中国用吗？**
不能——PCCP 是美国机制。中国 NMPA 变更控制更保守（核心权重重训通常触发变更注册），2026 年创新通道开始试点灵活方案；建议持续学习产品提前与审评中心沟通。

**Q：CE 认证包含 AI Act 吗？**
一个 CE 标志代表同时符合 MDR 和 AI Act（高风险义务 2028-08-02 起），同一公告机构一并审核——但两套体系并存，MDR 临床有效性 ≠ AI Act 算法透明度。

**Q：拿到 FDA 批准能直接进中国吗？**
不能——中国 Class III 诊断 AI 需以中国患者数据境内验证（1000+ 例、境内服务器），FDA 证据不能替代本地临床。

**Q：生成式 AI（LLM 医疗助手）怎么管？**
FDA/NMPA 倾向沙盒监管 + 人机协同底线：AI 只能做辅助，最终决策权归持证医师；自主诊断面临最高证据要求。幻觉风险需专门评估。

**Q：费用估算可信吗？**
公开渠道估算区间，仅作预算参考：FDA 费率按财年调整（可申请小企业减免 75%）；欧盟公告机构报价差异大（建议拿 3 家报价）；NMPA 费用随临床方案浮动。申报前复核。

**Q：工具脚本安全吗？**
本地运行、零网络、零数据采集、仅标准库。

**Q：法规更新怎么跟踪？**
FDA（510(k) 数据、指南页）、欧盟（MDR/AI Act 官方）、NMPA（CMDE 指南）——建议季度复核；本技能速查表随版本更新，引用关键结论前以官方原文为准。

## 3. 快速命令速查

```bash
python tools/ai_meddev_toolkit.py classify --product "..."   # 三地分类
python tools/ai_meddev_toolkit.py path --region us           # 路径推荐
python tools/ai_meddev_toolkit.py estimate --region eu --class III  # 费用周期
python tools/ai_meddev_toolkit.py change --desc "..."        # 变更触发判定
python tools/ai_meddev_toolkit.py compare                    # 三地总对比
```
