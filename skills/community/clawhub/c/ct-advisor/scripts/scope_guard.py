#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 能力域路由（domain routing）与超范围转介（2026-10-22 重写）

═══ 本次重写的动因（来自飞书 advisorlog 近 30 天实测）═══
  68 条真实提问的主题分布：合规 68% · 项目/运营 66% · 终点 53% · 医学写作 47%
  · 安全性 35% · 样本量仅 32%。
  即用户真正高频的三块是「合规应答 / 项目运营 / 交付物撰写」，而旧版 scope_guard
  把「撰写/大纲/模板」类一律判为**超范围**并前置免责转介 —— 与真实需求直接冲突：
  近半提问被打上"超出核心范围"的标签，用户却仍在反复使用。
  同时 6 条 kb_route_pass=0 里真正该拒答的只有 1 条（U 盘市场调研）。

  新口径（用户 2026-10-22 明确）：**尽量扩大适用范围，只有明确超出适用范围的
  才发送提示建议**。

═══ 新的判定模型（两段式）═══
  第一段  domain 分类（受控词表，多标签，最多 3 个）：
      compliance   合规应答（CDE/监管意见、GCP、伦理、稽查、数据合规）
      ops          项目运营（中心管理、报价预算、供应商/CRO、质控监查、SOP、交接）
      writing      交付物撰写（方案/制度/CSR/报告/PPT/模板/审稿回复）
      design       方案设计 · methodology 方法学 · stats 统计分析
      registry     注册申报 · safety 安全性/PV · data 数据管理
      rws          真实世界研究/IIT · medical 一般医学 · device 器械 · vet 兽药
  第二段  范围判定：
      命中任一 domain        → 在范围内（含 writing / ops / compliance，不再转介）
      未命中但有弱医学信号   → 在范围内（domain=general_medical）
      未命中 + 明确非医药域  → 超范围，给**建设性**转介建议（指向具体工具，不空拒）
      其余                   → 在范围内（宁多答，不误拦）

  ⚠️ 与旧版的不兼容点：`medical_writing` 不再是一个超范围 tag。旧调用方
  （refine_answer.apply_referral）收到空 tag 即不注入声明，行为自动兼容。

设计红线：
  - 不阻断、不硬答替代：超范围仅产出建议文本，云端仍会产出一份尽力参考。
  - 任何异常 → 一律判「在范围内」（宁多答，不误拦）。stdlib-only。

用法：
  python scripts/scope_guard.py --q "<问题>"         # 打印判定与 domain
  python scripts/scope_guard.py --selftest           # 离线用例自测（含放宽回归）
"""

import re
import sys

# ══════════════════════════════════════════════════════════════════════════
# 受控 domain 词表（顺序 = 优先级；命中多个时按此顺序取前 3）
# 词表来源：advisorlog 近 30 天 68 条真实提问归纳（非凭空设计）
# ══════════════════════════════════════════════════════════════════════════
DOMAIN_RULES = [
    ("compliance", re.compile(
        r"(合规|法规|监管|监管科学|GCP|ICH|NMPA|CDE|药监|FDA|EMA|指导原则|管理办法|"
        r"伦理|伦理审查|IRB|知情同意|稽查|核查|视察|监管意见|审核意见|通知书|"
        r"批件|受理号|沟通交流|pre-IND|preIND|数据合规|个人信息保护|劳务费|反商业贿赂|"
        r"互联网医院|互联网诊疗|远程访视|去中心化|DCT|第三方|受试者隐私|"
        r"药物警戒|\bPV\b|警戒体系|不良反应报告|风险点|法规依据|条款)", re.I)),

    ("ops", re.compile(
        r"(项目运营|运营管理|中心管理|分中心|参研中心|研究中心|site|中心退出|中心关闭|"
        r"进度|里程碑|成本|预算|报价|报价方案|费用|结算|付款|合同|CRO|供应商|"
        r"招募|入组|入组进度|依从性|脱落|失访|质控|质量控制|监查|监查计划|"
        r"SOP|标准操作规程|制度|管理制度|财务制度|组织架构|职责|交接|离职交接|"
        r"物料|口袋书|研究者支持|培训|启动会|机构|医院|社区医院|民营医院|"
        r"基金会|公益|公益项目|病例收集|平台|审核机制|驻点|人员配置|"
        r"多中心|中心(退出|关闭|中止|终止|撤销|暂停|更换)|执行不一致|"
        r"访视安排|合并用药|发放窗口|方案违背|偏离)", re.I)),

    ("writing", re.compile(
        r"(撰写|起草|拟写|拟稿|写一份|写一?份|写个|帮我写|请写|请直接输出|输出一份|"
        r"大纲|框架|目录|结构|提纲|成文|全文|正式文本|制度文本|条文|第X条|"
        r"综述|文献综述|稿件|论文|投稿|摘要|海报|科普|模板|范本|范例|"
        r"知情同意书|研究者手册|\bIB\b|\bCSR\b|临床试验方案|研究方案|方案摘要|"
        r"报告.*怎么写|怎么写.*报告|PPT|幻灯片|汇报|阅读汇报|审稿意见|回复信|"
        r"撰写.*方案|方案.*撰写|逐条回应|逐条判断|逐条回复|梳理.*输出|章节骨架)", re.I)),

    ("design", re.compile(
        r"(方案设计|试验设计|研究设计|设计类型|单臂|双臂|平行|交叉|队列|"
        r"剂量递增|剂量爬坡|3\+3|DLT|MTD|RP2D|扩展队列|篮式|伞式|"
        r"主(要)?终点|次(要)?终点|替代终点|复合终点|探索性终点|终点指标|"
        r"对照(组|选择)?|安慰剂|标准治疗|最佳支持治疗|加载设计|附加版方案|子研究|"
        r"估计目标| estimand|伴发事件)", re.I)),

    ("stats", re.compile(
        r"(样本量|样本含量|病例数|入组例数|检验效能|把握度|power|效应量|"
        r"假设检验|显著性|统计方法|统计分析|SAP|统计分析计划|"
        r"回归|logistic|cox|生存分析|Kaplan|Meier|log-?rank|混合效应|mixed|"
        r"缺失值|多重比较|期中分析|interim|成组序贯|贝叶斯|bayes|"
        r"非劣|优效|等效|ITT|FAS|PPS|分析集|敏感性分析|亚组|交互作用|"
        r"中位数|标准差|置信区间|\bCI\b|变异系数|精密度|一致性|发生率|事件率)", re.I)),

    ("safety", re.compile(
        r"(不良事件|\bAE\b|\bSAE\b|SUSAR|安全性|毒性|不良反应|严重不良|"
        r"DLT|剂量限制|安全性评价|风险评估|风险受益|获益风险|信号检测|"
        r"肝毒性|心脏毒性|过敏反应|"
        # ── 2026-11-10 补：信号检测/药物警戒方法学与数据源（原词表缺，
        #    导致「阿司匹林 FAERS PRR/ROR」类高频问题 domain=[]）
        r"\bFAERS\b|\bPRR\b|\bROR\b|\bEBGM\b|\bIC\b|药物警戒|安全信号|"
        r"自发报告|信号比|不均衡分析|信息成分|报告比值比|比例失衡|"
        r"警戒信号|个例安全性报告|\bICSR\b|\bPBRER\b|定期安全性)", re.I)),

    ("registry", re.compile(
        r"(注册|申报|上市申请|上市许可|IND|NDA|BLA|ANDA|"
        r"临床试验登记|信息公示|登记平台|ClinicalTrials|clinicaltrials\.gov|"
        r"突破性疗法|优先审评|附条件批准|完全批准|加速审批|孤儿药|"
        r"eCTD|递交|申报资料|沟通交流会议|pre-?NDA|"
        # ── 2026-11-10 补：试验检索/在研试验查询（原词表缺，
        #    导致「NSCLC 在研临床试验有哪些」类问题 domain=[]）
        r"在研(临床试验|试验|研究)|"
        r"在研.{0,10}(有哪些|清单|列表|汇总|检索|查询)|"
        r"试验检索|试验查询|注册检索|注册查询|注册信息查询|"
        r"ChiCTR|药物临床试验登记|临床试验信息)", re.I)),

    ("data", re.compile(
        r"(SDTM|ADaM|CDISC|\bCRF\b|eCRF|EDC|数据管理|数据库|数据集|"
        r"编程|SAS|统计编程|TFL|图表|列表|"
        r"编码|MedDRA|WHODrug|医学编码|数据清洗|逻辑核查|质疑|"
        r"源数据|源数据核查|SDV|盲态审核|数据审核|锁定|揭盲|盲底|编盲)", re.I)),

    ("rws", re.compile(
        r"(真实世界|真实世界研究|真实世界数据|\bRWS\b|\bRWE\b|"
        r"IIT|研究者发起|investigator.?initiated|非干预|观察性研究|"
        r"登记研究|队列研究|回顾性|前瞻性|数据库研究|医保数据)", re.I)),

    ("methodology", re.compile(
        r"(随机化|随机|区组随机|分层随机|中央随机|盲法|双盲|开放|单盲|"
        r"偏倚|混杂|因果|优效性|非劣效|等效性|多重性|分配隐藏|意向性)", re.I)),

    ("device", re.compile(
        r"(医疗器械|器械临床|器械临床试验|器械缺陷|体外诊断|\bIVD\b|"
        r"试剂|仪器|设备|耗材|植入|导管|支架|瓣膜|血压计|血糖仪)", re.I)),

    ("vet", re.compile(
        r"(兽药|兽医|宠物|猫用|犬用|狗用|动物用|动物实验|畜禽|水产)", re.I)),

    ("medical", re.compile(
        r"(疾病|适应症|适应证|诊断|诊断标准|诊疗|治疗|疗法|用药|给药|剂量|"
        r"疗效|预后|流行病学|患病率|发病率|指南|专家共识|"
        r"抑郁|焦虑|精神分裂|ADHD|ASD|强迫症|肿瘤|癌|骨质疏松|骨折|"
        r"肺纤维化|糖尿病|高血压|贫血|哮喘|肝炎|肾病|卒中|心衰|矮小|"
        r"神经|脑电|\bEEG\b|\bMEG\b|脑磁|神经调控|心理|精神|认知|"
        r"生理(学)?标志物|标志物|生物标志)", re.I)),
]

# 弱医学/生命科学信号（domain 全未命中时的兜底：仍在范围内）
WEAK_LIFE_SCIENCE = re.compile(
    r"(医药|药学|药企|制药|生物|临床|医学|医院|患者|受试者|健康|"
    r"药|药品|药物|疫苗|生物制品|细胞|基因|抗体|注射液|胶囊|片剂|"
    r"试验|研究项目|科研项目|卫健|卫生|审批)", re.I)

# 明确非医药域信号（只有在**完全没有** domain / 弱医学信号时才判超范围）
NON_MEDICAL_DOMAIN = re.compile(
    r"(U盘|U 盘|闪迪|SanDisk|存储卡|移动硬盘|固态硬盘|内存条|"
    r"消费电子|手机|笔记本电脑|平板电脑|耳机|音箱|家电|空调|冰箱|洗衣机|"
    r"服装|鞋帽|美妆|日化|食品饮料|快消|零食|酒水|餐饮|"
    r"零售|电商|跨境电商|直播带货|仓储物流|快递|"
    r"银行|证券|基金|保险|理财|信贷|地产|楼盘|租房|装修|"
    r"汽车|新能源车|充电桩|游戏|手游|动漫|影视|音乐|"
    r"旅游|酒店|机票|教育|K12|考研|留学|招聘|猎头|"
    r"人力资源|行政|财税|税务|商标注册)", re.I)

MAX_DOMAINS = 3

# ── 转介建议（建设性：说清覆盖范围 + 给下一步，不空拒）────────────────────
REFERRAL_ZH = (
    "ℹ️ 本题未识别到医药 / 临床试验相关语境，超出本技能的核心覆盖范围"
    "（合规应答、项目运营、交付物撰写、试验设计、统计分析、注册申报、安全性、数据管理）。"
    "若确属医药健康领域，请补充试验 / 产品 / 监管背景后重问；"
    "若属其他领域，建议改用对应的通用分析或写作工具。以下为基于通用知识的参考，"
    "未经临床试验知识库核验，仅供参考、不构成规范依据。"
)

REFERRAL_EN = (
    "ℹ️ No medical / clinical-trial context was detected in this question, which falls "
    "outside this skill's core coverage (regulatory response, trial operations, deliverable "
    "drafting, study design, statistics, submission, safety, data management). "
    "If it is in fact a healthcare topic, please add the trial / product / regulatory context "
    "and ask again; otherwise consider a general-purpose analysis or writing tool. "
    "The content below is general knowledge only, not verified against the clinical-trial "
    "knowledge base."
)


def classify_domains(question: str, max_domains: int = MAX_DOMAINS) -> list:
    """受控词表 domain 分类（多标签）。命中顺序即优先级；无命中返回 []。

    这是替换飞书 `category` 字段（现 36 种自由取值、中英混写）的规范口径。
    """
    q = question or ""
    if not q.strip():
        return []
    hits = [name for name, pat in DOMAIN_RULES if pat.search(q)]
    return hits[:max_domains]


def domain_hint(question: str) -> str:
    """domain 列表 → 逗号分隔字符串（供 payload.scope_hint / 日志 category 使用）。"""
    return ",".join(classify_domains(question))


def assess(question: str, lang: str = "") -> tuple:
    """评估是否在核心范围内（向后兼容旧签名：返回 3 元组）。

    返回 (in_scope, scope_tag, referral)：
      - in_scope=True              → (True, "", "")
      - in_scope=False（明确超范围）→ (False, "non_medical", 转介建议文本)
    异常 → (True, "", "")。
    """
    try:
        q = question or ""
        if classify_domains(q):
            return True, "", ""
        if WEAK_LIFE_SCIENCE.search(q):
            return True, "", ""
        # 无任何医药信号 + 命中明确非医药品类 → 才判超范围
        if NON_MEDICAL_DOMAIN.search(q):
            referral = REFERRAL_EN if str(lang).lower().startswith("en") else REFERRAL_ZH
            return False, "non_medical", referral
        return True, "", ""
    except Exception:  # noqa: BLE001
        return True, "", ""


def apply_referral(final_answer: str, scope_tag: str, lang: str = "") -> str:
    """把超范围建议前置注入最终答案（不截断原答案）。已含声明则跳过。

    ⚠️ 2026-10-22：仅 `non_medical` 一个 tag 会触发。旧 `medical_writing`
    已不再判超范围（占真实提问 47%，属核心域 writing）。
    ⚠️ 2026-10-30 修正：原实现 `if not scope_tag: return` —— 只要 tag 非空就注入，
    与上面的约定相反（`medical_writing` 等旧 tag 会被误注入转介声明）。
    现改为严格白名单，仅 `non_medical` 触发。调用点（proxy / entry）只在
    `assess()` 判超范围时注入 `scope_hint`，而该分支唯一取值就是 `non_medical`
    → 线上行为不变，仅消除「文档说不注入、实现却注入」的漂移。
    """
    if str(scope_tag or "").strip() != "non_medical":
        return final_answer
    fa = final_answer or ""
    if "超出本技能的核心覆盖范围" in fa or "outside this skill's core coverage" in fa:
        return fa
    referral = REFERRAL_EN if str(lang).lower().startswith("en") else REFERRAL_ZH
    return referral + "\n\n---\n\n" + fa


# ══════════════════════════════════════════════════════════════════════════
# 离线自测（用例全部取自 advisorlog 真实提问，含"放宽"回归）
# ══════════════════════════════════════════════════════════════════════════
_SELFTEST = [
    ("药企（蛤蚧定喘胶囊）向微爱基金会提出合规公益合作需求，请制定项目方案与预算方案",
     True, ["compliance", "ops"]),
    ("请直接输出两份可直接发布的正式制度全文，条文以'第X条'连续编号", True, ["writing", "ops"]),
    ("制作一个互联网医院分中心的CRO报价方案，覆盖没有伦理审查资质的社区医院",
     True, ["ops", "compliance"]),
    ("请生成一份临床试验协调员（CRC）离职交接的交接计划模板", True, ["ops", "writing"]),
    ("请重新构思一份《EEG/神经调控在医学心理学中的应用》的报告大纲", True, ["writing", "medical"]),
    ("CDE药物临床试验登记与信息公示平台审核意见：请声明本试验是否为批准的试验", True, ["compliance"]),
    ("多中心研究中如果一个中心突然要退出怎么处理", True, ["ops"]),
    ("计划开展一个IIT（研究者发起的临床研究），研究对象为同种异体瓣膜", True, ["rws", "device"]),
    ("审核用户粘贴的中国医疗器械临床试验方案第七至十七章", True, ["device", "writing"]),
    ("猫用三方复方滴剂（皮肤局部滴用）需要开展哪些毒理/安全性试验", True, ["vet", "safety"]),
    ("III期非小细胞肺癌，主要终点OS，单侧α=0.025，把握度80%，样本量怎么估算", True, ["stats"]),
    ("制作一个2+N+1模式的真实世界研究（RWS）方案框架，以益盛药业心悦胶囊RWS项目为背景",
     True, ["rws", "writing"]),
    ("申办方需要给研究者提供口袋书，还需要制作什么？按启动前、试验执行期分类列出", True, ["ops"]),
    # ── 2026-11-10 新增：advisorlog 高频漏判样本（原词表 domain=[]）
    ("阿司匹林肝损伤在 FAERS 里的安全信号 PRR 和 ROR 是多少？", True, ["safety"]),
    ("基于 FAERS 的 EBGM 与 IC 值怎么做不均衡分析？", True, ["safety"]),
    ("请查一下 NSCLC 在研临床试验有哪些", True, ["registry"]),
    ("用户上传了一份外部市场调研文档《SanDisk added questions》（闪迪U盘中国区Topline）",
     False, []),
    ("帮我看看这台笔记本电脑的性价比如何", False, []),
]


def _selftest() -> int:
    fail = 0
    for q, want_scope, want_domains in _SELFTEST:
        ok, tag, _ = assess(q)
        doms = classify_domains(q)
        ok_scope = (ok == want_scope)
        ok_dom = all(d in doms for d in want_domains) if want_domains else True
        status = "PASS" if (ok_scope and ok_dom) else "FAIL"
        if status == "FAIL":
            fail += 1
        print(f"[{status}] in_scope={ok}(want {want_scope}) tag={tag!r} "
              f"domains={doms} want⊇{want_domains} | {q[:42]}")
    print(f"\n{len(_SELFTEST) - fail}/{len(_SELFTEST)} passed")
    return 1 if fail else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    if "--q" in sys.argv:
        _q = sys.argv[sys.argv.index("--q") + 1]
        _ok, _tag, _ = assess(_q)
        print(f"in_scope={_ok} tag={_tag!r} domains={classify_domains(_q)} "
              f"hint={domain_hint(_q)!r}")
        sys.exit(0)
    print(assess("请帮我起草一份 EEG 神经调控研究报告的大纲"))
    print(assess("请帮我设计这个抗肿瘤药的随机对照试验方案"))
    print(assess("帮我看看这台笔记本电脑的性价比如何"))
