> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# Module F · AI 安全与伦理（V5 新增）

> 本模块探讨 AI 发展中的安全问题、伦理挑战和社会影响，培养学习者负责任使用 AI 的意识。

## 模块概览

| 单元 | 名称 | 时长 | 难度 |
|------|------|------|------|
| F1 | AI 安全基础 | 3h | ⭐⭐ |
| F2 | 数据隐私保护 | 3h | ⭐⭐ |
| F3 | 算法偏见与公平 | 3h | ⭐⭐⭐ |
| F4 | AI 伦理与社会责任 | 3h | ⭐⭐⭐ |

## F1 · AI 安全基础

### F1.1 AI 系统的脆弱性

**学习目标**
- 理解 AI 系统的常见安全威胁
- 识别对抗性攻击的基本原理

**核心内容**

```
1. 对抗性攻击（Adversarial Attacks）
   - 定义：精心设计的输入使 AI 模型产生错误输出
   - 示例：图像扰动使分类器误判
   
2. 数据投毒（Data Poisoning）
   - 定义：在训练数据中注入恶意样本
   - 影响：模型学得错误模式
   
3. 模型窃取（Model Extraction）
   - 定义：通过 API 查询重建模型
   - 风险：知识产权损失

4.Prompt 注入（Prompt Injection）
   - 定义：恶意指令覆盖原始 Prompt
   - 示例：DAN（Do Anything Now）
```

### F1.2 安全防御策略

**防御层次**

| 层次 | 策略 | 工具/方法 |
|------|------|----------|
| 输入层 | 输入验证与过滤 | 正则表达式、关键词过滤 |
| 模型层 | 对抗训练 | ART、CleverHans |
| 输出层 | 输出审核 | 内容过滤器 |
| 系统层 | 访问控制 | API 限流、身份验证 |

### F1.3 安全开发实践

```python
# 安全 AI 应用开发 Checklist
security_checklist = {
    "输入验证": [
        "类型检查",
        "长度限制",
        "特殊字符过滤",
        "格式校验"
    ],
    "输出审核": [
        "有害内容检测",
        "事实性验证",
        "一致性检查"
    ],
    "访问控制": [
        "身份认证",
        "权限分级",
        "操作审计"
    ],
    "数据安全": [
        "加密存储",
        "脱敏处理",
        "访问日志"
    ]
}
```

### F1.4 真实案例研究

#### 案例一：ImageNet 对抗性补丁攻击

- **案例名称**：对抗性补丁攻击（Adversarial Patch Attack）
- **时间**：2017 年
- **简述**：Brown et al. 在 2017 年发表的研究中，通过在图像上粘贴一个精心设计的彩色补丁（adversarial patch），成功让 ImageNet 图像分类模型将目标图像误判为任意指定类别。例如，在香蕉图片上贴一个小补丁后，分类器以高置信度将其识别为"烤面包机"。这一攻击甚至可以在物理世界中生效——将补丁打印出来贴在实物上，依然能欺骗摄像头和模型。
- **教学讨论要点**：
  1. 为什么人眼看起来毫无意义的彩色补丁能让 AI 模型产生如此确定的错误判断？这揭示了深度学习模型在特征提取上的什么弱点？
  2. 如果这种攻击被用于自动驾驶的交通标志识别系统，可能造成什么后果？应如何防御？
- **参考来源**：Brown, T. B., Mané, D., Roy, A., Abadi, M., & Gilmer, J. (2017). "Adversarial Patch." *arXiv preprint arXiv:1712.09665*.

#### 案例二：停车标志欺骗自动驾驶系统

- **案例名称**：停车标志对抗性攻击（Stop Sign Adversarial Attack）
- **时间**：2017 年
- **简述**：2017 年，密歇根大学的研究团队（Eykholt et al.）通过在真实停车标志（Stop Sign）上粘贴特定的黑白色贴纸，成功欺骗了深度学习交通标志识别系统，使其将"STOP"标志误识别为"限速 45"等其他标志。这一实验在物理世界中完成，证明了 adversarial attack 不仅存在于数字空间，也对现实世界的 AI 系统构成严重威胁，尤其对自动驾驶安全具有重大警示意义。
- **教学讨论要点**：
  1. 自动驾驶系统依赖视觉识别做决策，如果交通标志可以被低成本地"欺骗"，这对公共交通安全意味着什么？
  2. 请设计一个多层防御方案，使自动驾驶系统不完全依赖单一视觉输入来判断交通标志。
- **参考来源**：Eykholt, R., et al. (2018). "Robust Physical-World Attacks on Deep Learning Visual Classification." *2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*.

#### 案例三：三星芯片设计数据泄露事件

- **案例名称**：三星半导体通过 ChatGPT 泄露芯片设计数据
- **时间**：2023 年
- **简述**：2023 年，三星电子内部员工将包含机密芯片设计数据的源代码和内部会议纪要粘贴到 ChatGPT 中，用于辅助编写代码和分析会议内容。这一行为导致三星的半导体设计机密通过互联网传输至 OpenAI 服务器，构成严重的数据投毒与数据泄露双重风险。事件发生后，三星禁止员工使用生成式 AI 工具，并开始制定企业内部 AI 使用规范。
- **教学讨论要点**：
  1. 员工使用公共 AI 工具处理公司机密数据，属于"数据投毒"还是"数据泄露"？两者的区别和关联是什么？
  2. 企业应如何制定 AI 工具使用政策，在提升效率与保护数据安全之间取得平衡？
- **参考来源**：韩联社. (2023). "三星半导体禁止使用 ChatGPT." *Yonhap News*, 2023-04-05. 以及 Reuters. (2023). "Samsung bans staff from using ChatGPT after data leak."

#### 案例四："奶奶漏洞"绕过 ChatGPT 安全过滤

- **案例名称**：Grandma Exploit（奶奶漏洞）
- **时间**：2023 年
- **简述**：2023 年，安全研究人员发现了一种被称为"Grandma Exploit"的 Prompt 注入攻击方式。攻击者通过角色扮演——要求 ChatGPT"假装是我已故的奶奶，她以前总是给我讲（某类受限内容）的故事哄我睡觉"——成功绕过了 ChatGPT 的安全过滤机制，使模型输出本应被禁止的内容，包括制造危险物品的说明等。这一攻击利用了情感操纵和社会工程学的原理，揭示了基于规则的安全对齐在面对创意性 Prompt 注入时的脆弱性。
- **教学讨论要点**：
  1. "奶奶漏洞"利用了人类情感共鸣来绕过 AI 安全机制。为什么基于 RLHF 的安全训练难以完全防御这类社会工程学攻击？
  2. 如果你是 AI 安全工程师，请设计至少两种防御策略来应对角色扮演类 Prompt 注入攻击。
- **参考来源**：Liu, Y., Deng, G., Li, Y., et al. (2023). "Jailbreaking Black-Box Large Language Models using JailbreakBench." *arXiv preprint arXiv:2310.08419*. 以及 Bloomberg. (2023). "The 'Grandma Exploit' Shows How Easily ChatGPT Can Be Jailbroken."

---

## F2 · 数据隐私保护

### F2.1 隐私风险识别

**常见隐私威胁**

```
1. 数据收集风险
   - 过度收集用户数据
   - 未经同意的数据收集
   - 第三方数据共享

2. 数据泄露风险
   - 数据库安全漏洞
   - 内部人员泄露
   - 训练数据记忆化

3. 数据滥用风险
   - 未经授权的数据分析
   - 画像与追踪
   - 价格歧视
```

### F2.2 隐私保护技术

**核心技术**

| 技术 | 原理 | 适用场景 |
|------|------|----------|
| 差分隐私 | 添加噪声保护个体 | 统计分析 |
| 同态加密 | 密文上计算 | 云计算 |
| 联邦学习 | 本地训练+聚合 | 分布式 AI |
| 数据脱敏 | 替换/泛化敏感字段 | 数据共享 |

**联邦学习示例**

```python
# 联邦学习流程
def federated_learning(clients, rounds):
    global_model = initialize_model()
    
    for round in range(rounds):
        # 1. 分发全局模型
        client_models = []
        
        for client in clients:
            # 2. 本地训练
            local_update = client.train(global_model)
            client_models.append(local_update)
        
        # 3. 聚合更新（不获取原始数据）
        global_model = aggregate(client_models)
    
    return global_model
```

### F2.3 隐私合规框架

**主要法规**

| 法规 | 地区 | 核心要求 |
|------|------|----------|
| GDPR | 欧盟 | 数据主体权利、数据保护影响评估 |
| CCPA | 美国加州 | 知情权、删除权、退货权 |
| PIPL | 中国 | 数据处理告知同意、数据安全措施 |
| APPI | 日本 | 同意获取、跨境传输限制 |

### F2.4 真实案例研究

#### 案例一：剑桥分析数据丑闻

- **案例名称**：剑桥分析（Cambridge Analytica）数据隐私丑闻
- **时间**：2018 年
- **简述**：2018 年，前剑桥分析公司员工克里斯托弗·威利（Christopher Wylie）向媒体揭露，该公司通过分析咨询公司 Cambridge Analytica 未经约 8700 万 Facebook 用户的明确同意，获取了其个人数据。这些数据通过一款名为"This Is Your Digital Life"的第三方问卷应用收集，不仅获取了填写者的数据，还获取了其 Facebook 好友的数据。剑桥分析随后利用这些数据构建用户心理画像，为 2016 年美国大选和英国脱欧公投提供精准政治广告投放服务，严重影响了选民决策。
- **教学讨论要点**：
  1. 在这个案例中，数据收集在技术上"合法"（用户同意了第三方应用的条款），但为什么仍被视为严重的隐私侵犯？"知情同意"在大数据时代是否还有实际意义？
  2. 如果你是政策制定者，应如何设计法规来防止"数据二次利用"——即收集的数据被用于用户未预见的目的？
- **参考来源**：Cadwalladr, C., & Graham-Harrison, E. (2018). "Revealed: 50 million Facebook profiles harvested for Cambridge Analytica in major data breach." *The Guardian*, 2018-03-17. 以及 Wylie, C. (2019). 著作 *I Am the Cavalry* 中对此事件的详细记述。

#### 案例二：Clearview AI 面部识别隐私争议

- **案例名称**：Clearview AI 面部识别数据隐私争议
- **时间**：2020 年至今
- **简述**：Clearview AI 是一家美国科技公司，其在未经用户同意的情况下，从 Facebook、LinkedIn、Twitter、YouTube 等社交平台以及公开网页上抓取了超过 300 亿张人脸照片，建立了全球最大的面部识别数据库。该公司向执法机构、企业和私人提供面部识别服务，引发全球范围内的隐私争议。2022 年，意大利数据保护机构（Garante）对 Clearview AI 处以 2000 万欧元罚款；法国、希腊、意大利等国也相继裁定其违反了 GDPR。Clearview AI 的案例凸显了 AI 时代面部生物特征数据保护的严峻挑战。
- **教学讨论要点**：
  1. Clearview AI 认为其抓取的是"公开可获取"的照片，因此不侵犯隐私。"公开可获取"是否等同于"可以用于 AI 训练"？这两者之间的伦理边界在哪里？
  2. 面部识别技术在犯罪侦查中具有重大价值，但也威胁公民隐私。请讨论应如何设计监管框架，在安全需求与隐私保护之间取得平衡。
- **参考来源**：Hill, K. (2020). "The Secretive Company That Might End Privacy as We Know It." *The New York Times Magazine*, 2020-09-06. 以及意大利 Garante 裁决 (2022). "Provvedimento nei confronti di Clearview AI."

#### 案例三：中国《个人信息保护法》核心条款

- **案例名称**：《中华人民共和国个人信息保护法》（PIPL）
- **时间**：2021 年 11 月 1 日施行
- **简述**：《个人信息保护法》是中国首部专门针对个人信息保护的综合性法律，被称为中国版 GDPR。该法明确了个人信息处理的基本原则（合法、正当、必要、诚信原则），规定了个人信息处理者的义务，并赋予个人在信息处理活动中的知情权、决定权、查阅复制权、可携带权、删除权等权利。对于 AI 领域特别重要的条款包括：**第 24 条**规定利用个人信息进行自动化决策应当保证决策的透明度和结果公平，不得对个人在交易条件上实行不合理的差别待遇（直接针对大数据杀熟和算法歧视）；**第 55 条**要求在利用个人信息进行自动化决策、委托处理个人信息、向其他个人信息处理者提供个人信息等情形下进行事前合规审计。
- **教学讨论要点**：
  1. 《个人信息保护法》第 24 条要求自动化决策"保证透明度"和"结果公平"。在深度学习模型日益复杂的背景下，如何实际实现 AI 决策的"透明度"？技术上有哪些可行方案？
  2. 对比 GDPR 和 PIPL，两者在"知情同意"机制上有何异同？哪种模式在 AI 时代更有效？
- **参考来源**：《中华人民共和国个人信息保护法》，2021 年 8 月 20 日第十三届全国人民代表大会常务委员会第三十次会议通过，2021 年 11 月 1 日起施行。具体参见第 6 条（基本原则）、第 13 条（处理合法性基础）、第 24 条（自动化决策）、第 55 条（合规审计）。

---

## F3 · 算法偏见与公平

### F3.1 偏见类型与来源

**偏见分类**

```
1. 数据偏见
   - 历史偏见：训练数据反映历史歧视
   - 代表性偏见：某些群体样本不足
   - 标注偏见：标注者主观偏见

2. 算法偏见
   - 特征选择：使用敏感特征
   - 目标函数：优化目标偏离公平
   - 反馈循环：偏见过度放大

3. 社会偏见
   - 刻板印象强化
   - 歧视性决策
   - 机会不平等
```

### F3.2 公平性度量

**常用指标**

| 指标 | 定义 | 说明 |
|------|------|------|
| 统计均等 | P(Ŷ=1\|G=0) = P(Ŷ=1\|G=1) | 各群体正例率相等 |
| 均等机会 | P(Ŷ=1\|Y=1,G=0) = P(Ŷ=1\|Y=1,G=1) | 各群体真阳率相等 |
| 校准公平 | P(Y=1\|Ŷ=1,G=0) = P(Y=1\|Ŷ=1,G=1) | 预测条件独立于群体 |

```python
# 公平性检测代码示例
def measure_fairness(predictions, labels, sensitive_attr):
    groups = np.unique(sensitive_attr)
    
    results = {}
    
    # 统计均等
    for g in groups:
        mask = sensitive_attr == g
        rate = predictions[mask].mean()
        results[f'positive_rate_g{g}'] = rate
    
    # 均等机会
    for g in groups:
        mask_y1 = (labels == 1) & (sensitive_attr == g)
        mask_g = sensitive_attr == g
        tpr = predictions[mask_y1].mean()
        results[f'tpr_g{g}'] = tpr
    
    return results
```

### F3.3 偏见缓解策略

**技术方法**

| 阶段 | 方法 | 说明 |
|------|------|------|
| 数据预处理 | 重采样、重新加权 | 平衡训练数据 |
| 模型训练 | 对抗去偏、正则化 | 约束模型公平性 |
| 后处理 | 阈值调整、均衡化 | 调整输出决策 |

### F3.4 真实案例研究

#### 案例一：COMPAS 再犯预测算法偏见

- **案例名称**：COMPAS 累犯预测算法种族偏见事件
- **时间**：2016 年
- **简述**：2016 年，调查新闻机构 ProPublica 发表了一篇具有里程碑意义的调查报告，揭露了美国广泛使用的犯罪风险评估工具 COMPAS（Correctional Offender Management Profiling for Alternative Sanctions）存在严重的种族偏见。该分析发现，在控制了犯罪历史和年龄等变量后，COMPAS 将黑人被告错误标记为"高再犯风险"的比率是白人被告的**两倍**（45% vs 22%），而将白人被告错误标记为"低风险"的比率也显著高于黑人被告。尽管 COMPAS 的开发商 Northpointe 公司对此提出反驳，但这一事件引发了关于算法公平性的全国性讨论，并推动了公平 AI 研究的发展。
- **教学讨论要点**：
  1. COMPAS 的开发者声称算法是"种族中立"的（没有直接使用种族作为输入特征），为什么仍然产生了种族偏见？这说明了"算法中立"的什么本质问题？
  2. ProPublica 使用"假阳性率差异"来衡量偏见，而 Northpointe 使用"预测校准"来辩护。两种公平性定义在数学上可能无法同时满足——这给我们什么启示？
- **参考来源**：Angwin, J., Larson, J., Mattu, S., & Kirchner, L. (2016). "Machine Bias." *ProPublica*, 2016-05-23. 以及 Kleinberg, J., Mullainathan, S., & Raghavan, M. (2016). "Inherent Trade-Offs in the Fair Determination of Risk Scores." *arXiv:1609.05835*.

#### 案例二：亚马逊招聘 AI 性别偏见

- **案例名称**：亚马逊 AI 招聘工具性别歧视事件
- **时间**：2018 年
- **简述**：2018 年，路透社披露亚马逊内部开发了一个 AI 简历筛选系统，用于自动评估求职者的能力并给出 1-5 星评分。该系统从 2014 年开始训练，使用的是亚马逊过去 10 年收到的简历作为训练数据——由于科技行业男性占主导地位，训练数据中男性简历远多于女性。结果，AI 系统学会了歧视女性求职者：它在包含"女性"一词的简历上自动扣分（如"女子国际象棋队长"），并对两所女子大学的毕业生给予较低评分。亚马逊最终于 2017 年废弃了该项目。
- **教学讨论要点**：
  1. 亚马逊的 AI 系统忠实地反映了"历史数据中的模式"——这是否意味着 AI 不应该被用于招聘决策？还是说可以通过技术手段修正历史偏见？
  2. 如果你是亚马逊的工程师，发现训练数据存在性别不平衡，你会采取哪些具体的技术措施来缓解偏见？（提示：参考 F3.3 中的预处理、训练中、后处理三类方法）
- **参考来源**：Dastin, J. (2018). "Amazon scraps secret AI recruiting tool that showed bias against women." *Reuters*, 2018-10-10.

#### 案例三：苹果信用卡性别偏见

- **案例名称**：Apple Card 性别歧视事件
- **时间**：2019 年
- **简述**：2019 年 11 月，科技作家 David Heinemeier Hansson 在 Twitter 上公开投诉，苹果信用卡（Apple Card，由高盛银行发行）的信用额度算法存在性别歧视——他的信用额度是他妻子的 20 倍，尽管他妻子的信用评分更高且拥有更多共同资产。大量用户报告了类似情况，引发纽约金融服务局（NYDFS）的调查。虽然最终调查未发现"故意歧视"的证据，但暴露了 AI 驱动的信贷决策系统中存在的隐性偏见问题——即使算法不直接使用性别作为输入特征，仍可能通过代理变量（proxy variables）间接产生歧视性结果。
- **教学讨论要点**：
  1. Apple Card 的算法没有直接使用"性别"作为输入特征，但仍产生了性别歧视结果。什么是"代理变量"？在信贷评估中，哪些看似中性的特征可能成为性别的代理变量？
  2. 当 AI 系统做出歧视性决策时，谁应该负责——算法开发者、使用 AI 的银行、还是监管机构？请从不同角度论证。
- **参考来源**：Roberts, D. (2019). "Apple Card algorithm doesn't just have a women problem, it has a everyone problem." *Vox*, 2019-11-11. 以及 New York State Department of Financial Services (2021). "DFS Concludes Apple Card Credit Algorithm Did Not Intentionally Discriminate."

#### 推荐阅读

- **O'Neil, C. (2016). *Weapons of Math Destruction: How Big Data Increases Inequality and Undermines Democracy*. Crown.**
  - 本书由数学家 Cathy O'Neil 撰写，深入分析了算法模型如何在教育、司法、就业、金融等领域加剧社会不平等。书中提出"数学杀伤性武器"（WMD）的三大特征：**不透明性**（缺乏透明度）、**广泛性**（影响大量人群）、**不可申诉性**（受害者难以挑战算法决策）。该书是理解算法偏见社会影响的重要入门读物。

---

## F4 · AI 伦理与社会责任

### F4.1 AI 伦理框架

**核心原则**

```
1. 有益性（Beneficence）
   - AI 应增进人类福祉
   - 避免造成伤害

2. 自主性（Autonomy）
   - 尊重人类决策权
   - 保持适当人类控制

3. 公正性（Justice）
   - 公平分配利益和风险
   - 避免歧视和偏见

4. 可解释性（Explainability）
   - AI 决策可被理解
   - 透明度和可审计

5. 责任性（Accountability）
   - 明确责任归属
   - 建立问责机制
```

### F4.2 社会影响分析

**就业影响**

| 领域 | 替代风险 | 增强潜力 |
|------|----------|----------|
| 制造业 | 高 | 中 |
| 客服 | 高 | 中 |
| 医疗诊断 | 中 | 高 |
| 教育 | 低 | 高 |
| 创意产业 | 低 | 高 |

**应对策略**
- 技能转型培训
- 社会安全网完善
- 新就业机会创造
- 人机协作模式推广

### F4.3 负责任 AI 实践

**企业责任清单**

```markdown
## 负责任 AI 开发检查表

### 设计阶段
- [ ] 进行伦理影响评估
- [ ] 定义明确的使用边界
- [ ] 建立多样化的开发团队
- [ ] 咨询利益相关方

### 开发阶段
- [ ] 数据来源透明可追溯
- [ ] 进行偏见测试和审计
- [ ] 实施隐私保护措施
- [ ] 建立安全测试流程

### 部署阶段
- [ ] 制定清晰的使用政策
- [ ] 提供适当的人类控制
- [ ] 建立持续监控机制
- [ ] 设置紧急停止程序

### 维护阶段
- [ ] 定期审计和评估
- [ ] 响应用户反馈
- [ ] 及时修复问题
- [ ] 更新和迭代改进
```

### F4.4 真实案例研究

#### 案例一：特斯拉 Autopilot 致命事故

- **案例名称**：Tesla Autopilot 多起致命事故
- **时间**：2016 年、2018 年、2022 年
- **简述**：2016 年 5 月，Joshua Brown 驾驶 Tesla Model S 开启 Autopilot 模式行驶在佛罗里达高速公路上，系统未能识别一辆正在横穿马路的白色拖挂卡车，导致碰撞并造成驾驶员死亡——这是全球首例自动驾驶致死事故。2018 年 3 月，Walter Huang 在加州驾驶 Tesla Model X 时开启 Autopilot，车辆冲向高速公路隔离墩并起火，驾驶员不幸身亡。2022 年，美国国家公路交通安全管理局（NHTSA）对 Tesla Autopilot 展开正式调查，发现自 2021 年以来涉及 Autopilot 的事故超过 900 起。这些案例引发了关于自动驾驶责任归属、人机共驾安全、以及企业伦理责任的深刻讨论。
- **教学讨论要点**：
  1. 在 Autopilot 事故中，驾驶员、特斯拉公司、以及 Autopilot 算法开发者各自应承担什么责任？现有的法律框架是否能妥善处理这类"人机共责"的情况？
  2. 特斯拉将系统命名为"Autopilot"（自动导航）是否构成误导性营销？"辅助驾驶"与"自动驾驶"的命名差异如何影响用户的信任校准（trust calibration）？
- **参考来源**：National Transportation Safety Board (NTSB). (2019). "Highway Accident Report: Crash Between a Car Operating in Automated Vehicle Control System and a Tractor-Semitrailer." 以及 NHTSA. (2022). "Standing General Order 2021-01: Automated Vehicle Crash Report."

#### 案例二：Deepfake 伪造 CEO 语音诈骗

- **案例名称**：Deepfake AI 语音伪造 CEO 实施诈骗
- **时间**：2019 年
- **简述**：2019 年，一家英国能源公司的 CEO 接到其母公司德国总部"老板"的电话，对方使用 AI 语音合成技术完美模仿了 CEO 上司的声音和德语口音，要求他紧急向一个匈牙利供应商转账 24.3 万欧元（约 27 万美元）。由于声音高度逼真，CEO 未起疑心，立即执行了转账。这是已知的最早利用 AI 深度伪造（Deepfake）语音进行商业诈骗的案例之一。此后，Deepfake 技术被广泛用于制作虚假名人视频、政治虚假信息、色情内容等，对个人名誉、企业安全和社会信任构成严重威胁。
- **教学讨论要点**：
  1. 当 AI 可以完美模仿任何人的声音和面容时，"眼见为实、耳听为真"的传统认知被颠覆。企业和个人应如何建立新的信任验证机制？
  2. Deepfake 技术既有被滥用的风险，也有正当用途（如影视制作、虚拟助手）。应如何在技术创新与风险防控之间取得平衡？完全禁止 Deepfake 技术是否可行？
- **参考来源**：Sample, I. (2019). "Fraudsters use AI to mimic boss's voice in 'unprecedented' cyber-attack." *The Guardian*, 2019-09-01. 以及 Chesney, R., & Citron, D. (2019). "Deep Fakes: A Looming Challenge for Privacy, Democracy, and National Security." *California Law Review*, 107(6), 1753-1820.

#### 重要伦理框架与法规引用

**亚利洛马 AI 原则（Asilomar AI Principles, 2017）**

2017 年，来自全球的人工智能研究者、伦理学家、政策制定者在加州亚利洛马（Asilomar）举行的 Beneficial AI 会议上，共同制定了 23 条 AI 原则。这些原则涵盖三大领域：
- **研究议题**（Research Issues）：包括研究方向、经费分配、科学与公众交流
- **伦理价值**（Ethical Values）：包括隐私（Privacy）、自由（Liberty）、尊严（Dignity）、自主性（Autonomy）、公平（Justice）
- **长期问题**（Longer-term Issues）：包括 AI 能力对就业的影响、AI 军备竞赛风险、AGI 安全

这些原则成为全球 AI 伦理治理的重要基石，被广泛引用为 AI 伦理讨论的起点。

- **参考来源**：Future of Life Institute. (2017). "Asilomar AI Principles." https://futureoflife.org/ai-principles/

**欧盟人工智能法案（EU AI Act, 2024）**

2024 年 3 月，欧洲议会正式通过了全球首部全面的 AI 监管法律——《人工智能法案》（AI Act）。该法案采用**基于风险的分级监管**框架：
- **不可接受风险**（禁止）：如社会评分系统、无差别的人脸识别监控
- **高风险**（严格监管）：如医疗 AI、自动驾驶、执法 AI、教育 AI——需进行合规评估、透明度披露
- **有限风险**（透明度义务）：如聊天机器人——需告知用户其正在与 AI 交互
- **最低风险**（基本不受限制）：如 AI 驱动的视频游戏

该法案对全球 AI 治理具有示范效应，被称为 AI 领域的"GDPR 时刻"。

- **参考来源**：European Parliament. (2024). "Regulation (EU) 2024/... laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)." *Official Journal of the European Union*.

---

## 课件与游戏建议

### 课件形式
- F1：对抗攻击演示（交互式图像扰动可视化）
- F2：隐私风险自测（个人信息暴露程度评估）
- F3：偏见检测实验室（不公平决策案例分析）
- F4：伦理困境角色扮演（道德决策场景模拟）

### 游戏形式
- F1：「黑客 vs 防御者」攻防对抗游戏
- F2：「隐私侦探」调查哪些数据被收集
- F3：「公平法官」识别和修正歧视性决策
- F4：「AI 伦理委员会」模拟伦理审查流程
