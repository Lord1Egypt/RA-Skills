# 工具调研

调研日2026-10-10。按官方说明和仓库内容评估；未登录税局、试付费服务或实测商业产品准确率。

| 工具 | 适用任务 | 使用决定 |
|---|---|---|
| [全国统一规范电子税务局（官方说明）](https://shanghai.chinatax.gov.cn/sjtax/ztzl/yshj/ldjj/202508/P020250801323902960538.pdf) | 认定、取票、预填申报、缴款、回执 | 正式办理首选。从[总局官网](https://www.chinatax.gov.cn/)进入所在地税务局；预填仍须补未开票等数据，支持表单以当前页面为准 |
| [自然人电子税务局](https://etax.chinatax.gov.cn/)、扣缴端和个税App | 工资扣缴、个人收入核验、汇算 | 个税复核首选；扣缴端有计算步骤，见[官方操作说明](https://shenzhen.chinatax.gov.cn/sztax/nsfw/xzzx/rjxz/202101/3b4eb0b6df1f447c9b8c44669719a193.shtml)。网页本次抓取失败，不代表不可用；历史说明不作为2026界面/政策依据 |
| [金蝶精斗云·云会计](https://www.kingdee.com/products/ykj.html) | 取票、凭证、税负测算、报表、申报 | 已有账套优先沿用；核实版本、地区、具体税种，不据宣传承诺准确率 |
| [畅捷通好会计·智能税务](https://h.chanjet.com/hkj/zhinengshuiwu/) | 智能计税、账务取数、报税 | 已有账套优先沿用。官网地区覆盖与部分宣传页不一致，需核拟用地区/版别/个税支持，不能直接承诺全国全税种 |
| [1688-finance-tax](https://github.com/next-1688/1688-finance-tax) | 含税报价、四税联算、整体税负 | 有CLI/SKILL，依赖ClawHub密钥及外部网关；未实测或集成。经营报价不等同申报底稿 |
| [xntj-ai/baoxiao](https://github.com/xntj-ai/baoxiao)、[Auromix](https://github.com/Auromix/expense-reimbursement-skill) | 发票及报销材料、PDF/Excel整理 | 作为输入整理候选，未安装实测；前者不做发票验真，也不是报税系统 |
| 本技能 calculate.py | 普通常见税费独立复算、JSON留痕 | 本地标准库、无密钥/上传；合成案例实际验证。范围有限，仍需当前政策核验 |

建议：既有账务导出→本技能对账复算→官方系统核对→授权范围内申报→归档。小团队可用官方导出+本地底稿，无需为本技能另购软件。

不把工资、身份证、发票、流水上传公共计算器。按环境可用浏览器操作真实官方渠道；无接口不编造税局API或“已接入”。第三方集成先核数据去向、授权及公司许可。
