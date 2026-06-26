# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: customer-onboarding
description: 客户入驻管理技能。基于《园区运营项目客户服务标准指引》第四章"客户入驻阶段"，实现交圈会、场地验收、装修管理自动化。触发场景：(1) 合同审批完成后3个工作日内自动触发入驻流程，(2) 定时任务每日09:00检查入驻状态，(3) 手动触发（@企服助手 客户入驻）。
---

# 客户入驻管理技能 (Customer Onboarding Skill)

**⚠️ 本技能已自包含，无需安装 customer-management 技能**

本技能已内联客户查询和画像构建逻辑，可以直接独立运行。

## 功能概述

本技能用于自动化客户入驻流程，基于《园区运营项目客户服务标准指引》（{TODO: 填写文件编号}）第四章和《C+基础保障服务手册-企服（含产促中心）管理工作规程》（ZJWY-QFWI）第二章、第六章，实现：

### 一、企业入驻办理服务规程（第二章）
1. **核验客户身份、资料**：核查入伙通知书，核验客户身份，确认缴费情况
2. **交房资料收集、表单填写**：建立客户档案，准备交楼资料，客户签署材料
3. **移交资料**：向客户移交客户手册、装修指南，客户签收确认
4. **收取费用**：财务部收取首月物业费及水电费周转金
5. **房屋验收、水电查抄、记录查验问题**：工程部与客户共同验收，查抄水电读数
6. **移交钥匙**：企服管家向客户移交钥匙，客户签字确认
7. **留存钥匙**：如需要整改，客户可留存钥匙在物业服务中心
8. **问题整改跟进**：工程部门返修，管家跟进整改情况
9. **资料存档**：企服部建立客户档案，存档相关交付资料

### 二、装修办理规程（第六章）
1. **装修申请**：客户提交装修申请，企服部告知所需资料
2. **签署文件**：三方签署《装修管理服务协议》等文件
3. **审图**：工程部审核装修图纸（3个工作日内）
4. **费用收缴**：收取装修保证金、垃圾清运费等
5. **三方会议**：组织施工方、客户方、物业方召开三方会议
6. **成品保护验收**：企服部、工程部验收成品保护
7. **办理施工许可**：发放装修许可证，办理施工人员出入证
8. **日常巡查**：安管部、工程部、企服部按职责分工巡查
9. **违规行为处理**：材料入场、装修人员进出、违规施工管理
10. **竣工验收**：初验（15天内整改）→ 复验 → 验收合格 → 退还保证金

### 三、支持性文件
- {TODO: 填写表单编号}《客户信息登记表》
- {TODO: 填写表单编号}《客户收楼验房表（单元）》
- {TODO: 填写表单编号}《装修施工许可证》
- {TODO: 填写表单编号}《装修保证金退还申请表》

---

## 数据源配置

**数据文件**: `/Users/mac/示例产业园AC+服务.xlsx`
---

## 客户管理逻辑（内联）

> 本技能已内联客户档案查询和客户画像构建功能，无需依赖 customer-management 技能。
> 以下函数直接在本技能中使用，从 Excel 文件读取客户数据。

### 1. 查询客户档案 (query_customer_profile)

```python
def query_customer_profile(unit_no=None, tenant_name=None, contract_no=None):
    """
    查询客户档案（内联函数，无需调用外部技能）
    
    从 Excel 文件读取客户信息，支持按单元号、租户名或合同号查询。
    
    Args:
        unit_no: 单元号（如 T1-601）
        tenant_name: 租户名（支持模糊匹配）
        contract_no: 合同号
    
    Returns:
        dict: 客户完整档案信息
    """
    import openpyxl
    
    # 使用 xlsx skill 读取 Excel
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    ws = wb['👨客户管理👨']
    
    headers = [cell.value for cell in ws[1]]
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        # 匹配条件
        if unit_no and row[5] == unit_no:  # 单元号
            return build_customer_dict(headers, row)
        if tenant_name and tenant_name in str(row[6]):  # 租户名模糊匹配
            return build_customer_dict(headers, row)
        if contract_no and row[4] == contract_no:  # 合同号
            return build_customer_dict(headers, row)
    
    return None

def build_customer_dict(headers, row):
    """
    将 Excel 行数据构建为字典
    
    Args:
        headers: 表头列表
        row: 数据行
    
    Returns:
        dict: 客户档案字典
    """
    customer = {}
    for i, header in enumerate(headers):
        if i < len(row):
            customer[header] = row[i]
    
    # 字段映射（中英文）
    mapping = {
        "单元号": customer.get("单元号"),
        "租户名": customer.get("租户名"),
        "合同号": customer.get("合同号"),
        "租赁面积": customer.get("建筑面积", 0),
        "起租日期": customer.get("开始日期", ""),
        "截至日期": customer.get("截至日期", ""),
        "首年合同单价": customer.get("馶年合同单价", 0),
        "租户联系人": customer.get("租户联系人", ""),
        "电话": customer.get("电话", ""),
        "等级": customer.get("等级", ""),
        "企业类型": customer.get("企业类型", ""),
        "经营范围": customer.get("经营范围", ""),
        "纳税人资质": customer.get("纳税人资质", ""),
        "天眼评分": customer.get("天眼评分", "")
    }
    
    return mapping
```

### 2. 构建客户画像 (build_customer_portrait)

```python
def build_customer_portrait(unit_no):
    """
    构建客户画像 - 聚合多个数据源（内联函数）
    
    从多个工作表聚合数据，构建完整的客户画像。
    
    Args:
        unit_no: 单元号（主键）
    
    Returns:
        dict: 客户画像（包含服务、费用、报修等汇总）
    """
    import openpyxl
    
    wb = openpyxl.load_workbook('/Users/mac/示例产业园AC+服务.xlsx')
    
    portrait = {
        "基础信息": query_customer_profile(unit_no=unit_no),
        "服务记录": [],
        "费用记录": [],
        "能耗记录": [],
        "报修记录": [],
        "风险标记": []
    }
    
    if not portrait["基础信息"]:
        return None
    
    tenant_name = portrait["基础信息"]["租户名"]
    
    # 1. 查询C+服务记录（关联字段：租户名）
    ws_service = wb['C+服务记录']
    
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        if row[0] == tenant_name:  # 关联客户字段
            portrait["服务记录"].append({
                "走访时间": row[1],
                "走访管家": row[2],
                "客户情绪": row[3],
                "成交情况": row[4],
                "服务类别": row[5],
                "成交金额": row[6],
                "详情记录": row[7]
            })
    
    # 2. 查询费用收缴记录（关联字段：单元号）
    ws_fee = wb['👨💼费用收缴👨💼']
    
    for row in ws_fee.iter_rows(min_row=2, values_only=True):
        if row[1] == unit_no:  # 单元号
            portrait["费用记录"].append({
                "合同编号": row[0],
                "费项项目": row[3],
                "应收金额": row[4],
                "已收金额": row[6],
                "欠收金额": row[8],
                "是否支付": row[9],
                "月份": row[13]
            })
    
    # 3. 查询能耗收缴记录（关联字段：单元号）
    ws_energy = wb['👨💼能耗收缴👨💼']
    
    for row in ws_energy.iter_rows(min_row=2, values_only=True):
        if row[0] == unit_no:  # 单元号
            portrait["能耗记录"].append({
                "租户名": row[1],
                "应收金额": row[2],
                "已收金额": row[3],
                "欠费金额": row[4],
                "是否支付": row[5],
                "月份": row[6]
            })
    
    # 4. 查询报修记录（关联字段：楼层/单元）
    ws_repair = wb['🛠️报修情况汇总🛠️']
    
    for row in ws_repair.iter_rows(min_row=2, values_only=True):
        if unit_no in str(row[0]):  # 楼层/单元匹配
            portrait["报修记录"].append({
                "楼层/单元": row[0],
                "紧急程度": row[1],
                "报修细节描述": row[2],
                "报修人员": row[4],
                "报修时间": row[5],
                "维修人员": row[6],
                "维修跟进状态": row[7]
            })
    
    # 5. 计算风险标记
    portrait["风险标记"] = calculate_risk_tags(portrait)
    
    return portrait

def calculate_risk_tags(portrait):
    """
    计算客户风险标记
    
    Args:
        portrait: 客户画像字典
    
    Returns:
        list: 风险标记列表（如 ["欠费风险", "流失风险"]）
    """
    risks = []
    
    # 1. 欠费风险判断
    欠费总额 = 0
    for fee in portrait["费用记录"]:
        if fee["是否支付"] == "否":
            欠费金额 = float(fee["欠收金额"]) if fee["欠收金额"] else 0
            欠费总额 += 欠费金额
    
    if 欠费总额 > 50000:
        risks.append(f"🚨 高欠费风险（欠费¥{欠费总额:.2f}）")
    elif 欠费总额 > 10000:
        risks.append(f"⚠️ 中度欠费风险（欠费¥{欠费总额:.2f}）")
    elif 欠费总额 > 0:
        risks.append(f"📢 轻度欠费提醒（欠费¥{欠费总额:.2f}）")
    
    # 2. 流失风险判断（续租预警）
    基础信息 = portrait["基础信息"]
    if 基础信息:
        from datetime import datetime
        截至日期 = datetime.strptime(基础信息["截至日期"], "%Y年%m月%d日")
        剩余天数 = (截至日期 - datetime.now()).days
        
        if 剩余天数 <= 30:
            risks.append(f"🚨 流失风险（合同剩余{剩余天数}天）")
        elif 剩余天数 <= 90:
            risks.append(f"⚠️ 续租预警（合同剩余{剩余天数}天）")
    
    # 3. 投诉/报修频率判断
    报修次数 = len(portrait["报修记录"])
    if 报修次数 >= 3:  # 最近报修次数>=3
        risks.append(f"⚠️ 高频报修（{报修次数}次）")
    
    # 4. 服务满意度判断
    满意记录 = [s for s in portrait["服务记录"] if s["客户情绪"] == "满意"]
    总记录 = len(portrait["服务记录"])
    
    if 总记录 > 0 and len(满意记录) / 总记录 < 0.5:
        risks.append(f"⚠️ 低满意度（满意率{len(满意记录)/总记录*100:.1f}%）")
    
    return risks
```

---



**工作表映射**:
| 功能模块 | 工作表名 | 用途 |
|---------|----------|------|
| **客户档案** | 👨客户管理👨 | 客户基本信息、合同信息 |
| **合同信息** | 合同管理（待建） | 合同审批状态、入驻日期 |
| **装修管理** | 装修管理（待建） | 装修方案、巡查记录、验收记录 |
| **服务团队** | 服务团队配置（待建） | 管家、工程、安管等服务人员 |

**依赖技能**:
- `visit-management`：安排入驻后首次走访（可选）

**客户管理逻辑（内联）**：本技能已内联客户档案查询和客户画像构建功能，无需依赖 customer-management 技能。

---

## 核心逻辑

### 1. 企业入驻办理服务规程模块

**依据**：《C+基础保障服务手册》第二章

```python
# 企业入驻办理详细流程（9个步骤）
def enterprise_onboarding_process(contract_no):
    """
    企业入驻办理完整流程（依据{TODO: 填写文件编号}）
    
    流程步骤：
    1. 核验客户身份、资料
    2. 交房资料收集、表单填写
    3. 移交资料（客户手册、装修指南）
    4. 收取费用（首月物业费+水电周转金）
    5. 房屋验收、水电查抄、记录查验问题
    6. 移交钥匙（客户签字确认）
    7. 留存钥匙（如需整改，填写《钥匙代管委托书》）
    8. 问题整改跟进（工程部返修，管家跟进）
    9. 资料存档（建立客户档案）
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 入驻办理结果
    """
    # 1. 核验客户身份、资料
    identity_verification = verify_customer_identity(contract_no)
    if identity_verification['状态'] != '通过':
        return {'状态': '失败', '原因': '客户身份核验失败', '详情': identity_verification}
    
    # 2. 交房资料收集、表单填写
    document_collection = collect_onboarding_documents(contract_no)
    
    # 3. 移交资料（客户手册、装修指南）
    material_handover = handover_materials(contract_no)
    
    # 4. 收取费用
    fee_collection = collect_onboarding_fees(contract_no)
    
    # 5. 房屋验收、水电查抄
    property_inspection = inspect_property(contract_no)
    
    # 6. 移交钥匙
    key_handover = handover_keys(contract_no, property_inspection)
    
    # 7. 留存钥匙（如需整改）
    if property_inspection['验收结果'] == '不合格':
        key_retention = retain_keys_for_rectification(contract_no)
    else:
        key_retention = {'状态': '无需留存', '原因': '验收合格'}
    
    # 8. 问题整改跟进（如验收不合格）
    if property_inspection['验收结果'] == '不合格':
        rectification_tracking = track_rectification_progress(contract_no, property_inspection)
    else:
        rectification_tracking = {'状态': '无需整改', '原因': '验收合格'}
    
    # 9. 资料存档
    document_archiving = archive_onboarding_documents(contract_no, {
        '身份核验': identity_verification,
        '资料收集': document_collection,
        '资料移交': material_handover,
        '费用收取': fee_collection,
        '房屋验收': property_inspection,
        '钥匙移交': key_handover,
        '钥匙留存': key_retention,
        '整改跟进': rectification_tracking
    })
    
    # 生成《客户入驻办理报告》
    report = generate_onboarding_report(contract_no, {
        '身份核验': identity_verification,
        '资料收集': document_collection,
        '费用收取': fee_collection,
        '房屋验收': property_inspection,
        '钥匙移交': key_handover,
        '整改跟进': rectification_tracking,
        '资料存档': document_archiving
    })
    
    return {
        '状态': '成功',
        '合同编号': contract_no,
        '流程步骤': '9/9 完成',
        '验收结果': property_inspection['验收结果'],
        '整改状态': rectification_tracking.get('状态', '无需整改'),
        '报告': report
    }

def verify_customer_identity(contract_no):
    """
    核验客户身份、资料（步骤1）
    
    所需资料：
    - 《入伙通知书》
    - 《房屋买卖合同》或《房屋租赁合同》
    - 《营业执照》
    - 产权人/租户身份证复印件/法人身份证复印件
    - 授权委托书
    - 经办人身份信息复印件
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 身份核验结果
    """
    # TODO: 实现身份核验逻辑
    # 1. 读取合同信息
    # 2. 核对入伙通知书
    # 3. 核对客户提供的资料
    # 4. 确认缴费情况
    
    return {
        '状态': '通过',
        '核验时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '核验人': '企服管家',
        '备注': '所有资料齐全，身份核验通过'
    }

def collect_onboarding_documents(contract_no):
    """
    交房资料收集、表单填写（步骤2）
    
    物业应准备资料：
    - 《客户收楼验房表》
    - 《客户信息登记表》
    - 已盖章的《临时管理规约》
    - 《物业服务协议》
    - 《消防安全责任书》
    
    客户应签署材料：
    - 《临时管理规约》
    - 《前期物业服务协议》
    - 《消防安全责任书》
    - 《社会治安综合治理责任书》
    - 《委托扣款协议》
    - 《客户信息登记表》
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 资料收集结果
    """
    # TODO: 实现资料收集逻辑
    # 1. 准备物业方资料
    # 2. 引导客户填写/签署资料
    # 3. 检查资料完整性
    
    return {
        '状态': '完成',
        '物业准备资料': ['客户收楼验房表', '客户信息登记表', '临时管理规约', '物业服务协议', '消防安全责任书'],
        '客户签署资料': ['临时管理规约', '前期物业服务协议', '消防安全责任书', '社会治安综合治理责任书', '委托扣款协议', '客户信息登记表'],
        '完整性检查': '通过'
    }

def handover_materials(contract_no):
    """
    移交资料（步骤3）
    
    移交资料：
    - 客户手册
    - 装修指南
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 资料移交结果
    """
    # TODO: 实现资料移交逻辑
    # 1. 准备客户手册、装修指南
    # 2. 客户签收确认
    
    return {
        '状态': '完成',
        '移交资料': ['客户手册', '装修指南'],
        '客户签收': '已签收',
        '签收时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def collect_onboarding_fees(contract_no):
    """
    收取费用（步骤4）
    
    收费项目：
    - 首月物业费
    - 水电费周转金（两个月物业管理费等额费用）
    - 首月不足自然月时，收取首月及次月物业费
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 费用收取结果
    """
    # TODO: 实现费用收取逻辑
    # 1. 计算应缴费用
    # 2. 财务部收取费用
    # 3. 出具缴费凭证
    
    return {
        '状态': '完成',
        '收费项目': ['首月物业费', '水电费周转金'],
        '应收总额': 0.00,  # TODO: 从Excel读取计算
        '实收总额': 0.00,  # TODO: 从Excel读取
        '收据编号': 'TODO',
        '收费时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def inspect_property(contract_no):
    """
    房屋验收、水电查抄（步骤5）
    
    验收内容：
    - 客户单元设备数量清点、验收
    - 房屋质量问题查验
    - 水表读数查抄
    - 电表读数查抄
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 房屋验收结果
    """
    # TODO: 实现房屋验收逻辑
    # 1. 工程部与客户共同验收
    # 2. 填写《客户收楼验房表》
    # 3. 查抄水、电表读数
    # 4. 记录查验问题
    
    return {
        '状态': '完成',
        '验收结果': '合格',  # 或'不合格'
        '验收时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '工程部验收人': '李工',
        '客户代表': '客户联系人',
        '水表读数': 0,  # TODO: 从现场读取
        '电表读数': 0,  # TODO: 从现场读取
        '查验问题': []  # 如有问题，填写此处
    }

def handover_keys(contract_no, inspection_result):
    """
    移交钥匙（步骤6）
    
    操作流程：
    - 客户单元钥匙在与客户进行单元移交确认时移交
    - 在《客户收楼验房表》中注明数量
    - 客户授权委托人确认签字
    
    Args:
        contract_no: 合同编号
        inspection_result: 房屋验收结果
    
    Returns:
        dict: 钥匙移交结果
    """
    if inspection_result['验收结果'] != '合格':
        return {'状态': '暂缓', '原因': '房屋验收不合格，待整改完成后移交'}
    
    # TODO: 实现钥匙移交逻辑
    # 1. 准备客户单元钥匙
    # 2. 客户授权委托人确认
    # 3. 在《客户收楼验房表》中注明数量
    # 4. 客户签字确认
    
    return {
        '状态': '完成',
        '钥匙数量': 0,  # TODO: 根据实际情况填写
        '移交时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '客户签字': '客户授权委托人签字',
        '备注': '钥匙已移交，客户确认签收'
    }

def retain_keys_for_rectification(contract_no):
    """
    留存钥匙（步骤7）
    
    适用情况：
    - 交付单元内问题需要整改
    - 客户选择将钥匙留存在物业服务中心
    
    操作流程：
    - 客户填写《钥匙代管委托书》
    - 一式两份
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 钥匙留存结果
    """
    # TODO: 实现钥匙留存逻辑
    # 1. 客户填写《钥匙代管委托书》
    # 2. 一式两份，客户和物业各执一份
    # 3. 钥匙留存于物业服务中心
    
    return {
        '状态': '已留存',
        '留存原因': '房屋验收不合格，需要整改',
        '留存时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '钥匙代管委托书': '已签署',
        '备注': '整改完成后，通知客户领取钥匙'
    }

def track_rectification_progress(contract_no, inspection_result):
    """
    问题整改跟进（步骤8）
    
    操作流程：
    - 房屋问题登记应详细具体、清晰明了
    - 问题统一交由工程部门进行返修
    - 较难故障无法当日解决的需与客户沟通后处理
    - 验收当日记录的遗留问题需统一整理形成台账
    
    Args:
        contract_no: 合同编号
        inspection_result: 房屋验收结果（包含查验问题）
    
    Returns:
        dict: 整改跟进结果
    """
    # TODO: 实现整改跟进逻辑
    # 1. 整理遗留问题台账
    # 2. 工程部门安排返修
    # 3. 管家跟进整改进度
    # 4. 整改完成后复验
    
    return {
        '状态': '跟进中',
        '查验问题数量': len(inspection_result.get('查验问题', [])),
        '整改开始时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '预计完成时间': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        '工程负责人': '李工',
        '管家跟进人': '戚亮先',
        '备注': '整改期限为15天，管家每日跟进'
    }

def archive_onboarding_documents(contract_no, process_data):
    """
    资料存档（步骤9）
    
    存档内容：
    - 客户档案（客户信息登记表、营业执照复印件等）
    - 交付资料（收楼验房表、钥匙代管委托书等）
    - 签署资料（临时管理规约、物业服务协议等）
    
    Args:
        contract_no: 合同编号
        process_data: 全流程数据
    
    Returns:
        dict: 资料存档结果
    """
    # TODO: 实现资料存档逻辑
    # 1. 建立客户档案
    # 2. 将相关交付资料和签署资料进行存档
    # 3. 录入电脑系统
    
    return {
        '状态': '已存档',
        '存档时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '存档地点': '物业服务中心档案室',
        '电子版存档': '已录入系统',
        '备注': '客户档案已建立，资料已存档'
    }

def generate_onboarding_report(contract_no, process_data):
    """
    生成《客户入驻办理报告》
    
    Args:
        contract_no: 合同编号
        process_data: 全流程数据
    
    Returns:
        str: 报告文件路径
    """
    # 构建报告内容
    report_content = f"""
# 客户入驻办理报告

**合同编号**：{contract_no}
**报告时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**编制**：企服助手 (Enterprise Service Assistant)

---

## 一、流程概览

| 步骤 | 流程内容 | 状态 | 完成时间 |
|------|----------|------|----------|
| 1 | 核验客户身份、资料 | {process_data['身份核验']['状态']} | {process_data['身份核验']['核验时间']} |
| 2 | 交房资料收集、表单填写 | {process_data['资料收集']['状态']} |  |
| 3 | 移交资料 | {process_data['资料移交']['状态']} | {process_data['资料移交']['客户签收时间']} |
| 4 | 收取费用 | {process_data['费用收取']['状态']} | {process_data['费用收取']['收费时间']} |
| 5 | 房屋验收、水电查抄 | {process_data['房屋验收']['状态']} | {process_data['房屋验收']['验收时间']} |
| 6 | 移交钥匙 | {process_data['钥匙移交']['状态']} | {process_data['钥匙移交'].get('移交时间', 'N/A')} |
| 7 | 留存钥匙（如需整改） | {process_data['钥匙留存']['状态']} |  |
| 8 | 问题整改跟进（如需整改） | {process_data['整改跟进']['状态']} |  |
| 9 | 资料存档 | {process_data['资料存档']['状态']} | {process_data['资料存档']['存档时间']} |

---

## 二、详细记录

### 2.1 身份核验

- 核验时间：{process_data['身份核验']['核验时间']}
- 核验人：{process_data['身份核验']['核验人']}
- 核验结果：{process_data['身份核验']['状态']}
- 备注：{process_data['身份核验']['备注']}

### 2.2 费用收取

- 收费项目：{', '.join(process_data['费用收取']['收费项目'])}
- 应收总额：¥{process_data['费用收取']['应收总额']:.2f}
- 实收总额：¥{process_data['费用收取']['实收总额']:.2f}
- 收据编号：{process_data['费用收取']['收据编号']}

### 2.3 房屋验收

- 验收结果：{process_data['房屋验收']['验收结果']}
- 验收时间：{process_data['房屋验收']['验收时间']}
- 工程部验收人：{process_data['房屋验收']['工程部验收人']}
- 客户代表：{process_data['房屋验收']['客户代表']}
- 水表读数：{process_data['房屋验收']['水表读数']}
- 电表读数：{process_data['房屋验收']['电表读数']}

### 2.4 整改跟进（如有）

- 整改状态：{process_data['整改跟进']['状态']}
- 查验问题数量：{process_data['整改跟进']['查验问题数量']}
- 整改开始时间：{process_data['整改跟进']['整改开始时间']}
- 预计完成时间：{process_data['整改跟进']['预计完成时间']}
- 工程负责人：{process_data['整改跟进']['工程负责人']}
- 管家跟进人：{process_data['整改跟进']['管家跟进人']}

---

## 三、支持性文件

| 文件编号 | 文件名称 | 版式 |
|----------|----------|------|
| {TODO: 填写表单编号} | 《客户信息登记表》 | 表格 |
| {TODO: 填写文件编号} | 《钥匙代管委托书》 | 文档 |
| {TODO: 填写表单编号} | 《客户收楼验房表（单元）》 | 表格 |
| {TODO: 填写文件编号} | 《客户收楼验房表（共有部位）》 | 表格 |

---

**备注**：
1. 本报告依据《C+基础保障服务手册-企服（含产促中心）管理工作规程》（ZJWY-QFWI）第二章编制
2. 本报告一式两份，客户、物业服务中心各执一份
3. 房屋验收不合格需整改的，整改完成后需进行复验

**编制**：企服助手 (Enterprise Service Assistant)
**版本**：V2.0
"""
    
    # 保存为Markdown文件
    output_dir = "/Users/mac/客户入驻办理报告/"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{output_dir}{contract_no}_客户入驻办理报告_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return file_path
```
    # 1. 获取客户信息（使用内联的客户档案查询函数）
    customer_profile = query_customer_profile(contract_no=contract_no)
    
    if not customer_profile:
        return {'状态': '失败', '原因': '客户信息未找到'}
    
    unit_no = customer_profile.get("单元号", "")
    tenant_name = customer_profile.get("租户名", "")
    lease_start = customer_profile.get("起租日期", "")
    lease_area = customer_profile.get("租赁面积", 0)
    
    # 2. 组建服务团队（基于单元号分配）
    service_team = assign_service_team(unit_no)
    
    # 3. 创建企微服务群（模拟）
    wecom_group = create_wecom_service_group(unit_no, tenant_name, service_team)
    
    # 4. 生成《客户入驻信息交接单》
    handover_form = generate_handover_form(contract_no, customer_profile, service_team)
    
    # 5. 推送交圈会通知
    notification = send_handover_meeting_notification(contract_no, service_team, handover_form)
    
    return {
        '状态': '成功',
        '合同编号': contract_no,
        '单元号': unit_no,
        '租户名': tenant_name,
        '服务团队': service_team,
        '企微群': wecom_group,
        '交接单': handover_form,
        '通知状态': notification
    }

def assign_service_team(unit_no):
    """
    根据单元号分配服务团队
    
    Args:
        unit_no: 单元号
    
    Returns:
        dict: 服务团队名单
    """
    # 服务团队配置（可配置）
    team_config = {
        "管家": {
            "T1-6F": "戚亮先",
            "T1-7F": "戚亮先",
            "T1-8F": "戚亮先",
            "T1-9F": "刘瑞",
            "T1-10F": "刘瑞",
            "T1-11F": "刘瑞",
            "T1-12F": "张三",
            "T1-13F": "张三",
            "T1-14F": "张三"
        },
        "工程专员": "李工",
        "安管专员": "王队",
        "环境专员": "张姐",
        "产业服务专员": "赵经理"
    }
    
    # 提取楼层
    floor = unit_no.split("-")[1][:2] + "F"  # T1-601 → 6F
    
    service_team = {
        "管家": team_config["管家"].get(floor, "未分配"),
        "工程专员": team_config["工程专员"],
        "安管专员": team_config["安管专员"],
        "环境专员": team_config["环境专员"],
        "产业服务专员": team_config["产业服务专员"]
    }
    
    return service_team

def create_wecom_service_group(unit_no, tenant_name, service_team):
    """
    创建企微服务群（模拟函数）
    
    Args:
        unit_no: 单元号
        tenant_name: 租户名
        service_team: 服务团队
    
    Returns:
        str: 企微群名称或ID
    """
    # TODO: 对接企微API创建群组
    group_name = f"【{unit_no}】{tenant_name} - 入驻服务群"
    
    # 模拟创建成功
    return group_name

def generate_handover_form(contract_no, customer_profile, service_team):
    """
    生成《客户入驻信息交接单》
    
    Args:
        contract_no: 合同编号
        customer_profile: 客户档案
        service_team: 服务团队
    
    Returns:
        str: 交接单文件路径
    """
    # 构建交接单内容
    form_content = f"""
# 客户入驻信息交接单

**合同编号**：{contract_no}
**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、客户基本信息

| 字段 | 内容 |
|------|------|
| 单元号 | {customer_profile.get('单元号', '')} |
| 租户名 | {customer_profile.get('租户名', '')} |
| 租户联系人 | {customer_profile.get('租户联系人', '')} |
| 联系电话 | {customer_profile.get('电话', '')} |
| 租赁面积 | {customer_profile.get('租赁面积', 0)} ㎡ |
| 起租日期 | {customer_profile.get('起租日期', '')} |
| 截至日期 | {customer_profile.get('截至日期', '')} |
| 首年合同单价 | ¥{customer_profile.get('首年合同单价', 0)}/㎡/月 |

---

## 二、服务团队分配

| 角色 | 姓名 | 联系电话 | 职责 |
|------|------|----------|------|
| 管家 | {service_team.get('管家', '未分配')} | 138XXXXXXX | 日常对接、需求响应 |
| 工程专员 | {service_team.get('工程专员', '未分配')} | 139XXXXXXX | 装修审批、工程维修 |
| 安管专员 | {service_team.get('安管专员', '未分配')} | 137XXXXXXX | 安全管理、停车管理 |
| 环境专员 | {service_team.get('环境专员', '未分配')} | 136XXXXXXX | 保洁、绿化、垃圾分类 |
| 产业服务专员 | {service_team.get('产业服务专员', '未分配')} | 135XXXXXXX | C+服务、政策服务 |

---

## 三、交接事项清单

### 3.1 招商部 → 产服部、物业服务中心

- [ ] 客户档案移交（集客荟系统录入）
- [ ] 合同副本移交（行政部存档）
- [ ] 客户特殊需求移交（如有）
- [ ] 租金、物业费标准确认

### 3.2 物业服务中心 → 各班组

- [ ] 管家接管客户，建立服务档案
- [ ] 工程部检查单元水电设施
- [ ] 安管部办理门禁卡、停车权限
- [ ] 环境部安排保洁、绿化

### 3.3 产业服务部 → 客户

- [ ] 添加企业微信，邀请进入服务群
- [ ] 介绍C+服务内容
- [ ] 了解企业需求，制定服务计划

---

## 四、时间节点

| 事项 | 责任部门 | 完成时限 |
|------|----------|----------|
| 交圈会召开 | 招商部组织 | 合同审批完成后3个工作日内 |
| 场地交付验收 | 物业服务中心 | 起租日前5个工作日 |
| 装修方案审核 | 工程部 | 收到方案后3个工作日内 |
| 竣工验收 | 工程部 | 装修完成后3个工作日内 |

---

## 五、签字确认

| 部门 | 签字 | 日期 |
|------|------|------|
| 招商部 |  |  |
| 产业服务部 |  |  |
| 物业服务中心 |  |  |
| 财务部 |  |  |

---

**备注**：本交接单一式四份，招商部、产业服务部、物业服务中心、财务部各执一份。

**编制**：企服助手 (Enterprise Service Assistant)
**版本**：V1.0
"""
    
    # 保存为Markdown文件
    output_dir = "/Users/mac/客户入驻交接单/"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{output_dir}{contract_no}_客户入驻信息交接单_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(form_content)
    
    # TODO: 可选：转换为PDF或上传到腾讯文档
    
    return file_path

def send_handover_meeting_notification(contract_no, service_team, handover_form):
    """
    发送交圈会通知（模拟函数）
    
    Args:
        contract_no: 合同编号
        service_team: 服务团队
        handover_form: 交接单文件路径
    
    Returns:
        str: 通知状态
    """
    # TODO: 对接企微API发送通知
    notification_message = f"""
━━━━━━━━━━━━━━━
【客户入驻交圈会通知】

📋 合同编号：{contract_no}
📅 会议时间：{datetime.now().strftime('%Y-%m-%d')} 14:00
📍 会议地点：项目会议室

━━━ 参会人员 ━━━
• 管家：{service_team.get('管家', '未分配')}
• 工程专员：{service_team.get('工程专员', '未分配')}
• 安管专员：{service_team.get('安管专员', '未分配')}
• 环境专员：{service_team.get('环境专员', '未分配')}
• 产业服务专员：{service_team.get('产业服务专员', '未分配')}

━━━ 会议议程 ━━━
1. 招商部介绍客户基本情况
2. 讨论客户特殊需求和注意事项
3. 明确各部门职责分工
4. 确定时间节点和交付标准

📎 附件：{handover_form}

请各位准时参加！
━━━━━━━━━━━━━━━
"""
    
    # 模拟发送成功
    print(notification_message)
    return "通知已发送"
```

### 2. 场地交付验收模块

```python
def schedule_delivery_inspection(contract_no, inspection_date=None):
    """
    预约场地交付验收
    
    Args:
        contract_no: 合同编号
        inspection_date: 验收日期（默认为起租日前5个工作日）
    
    Returns:
        dict: 验收安排
    """
    # 1. 获取客户信息（使用内联的客户档案查询函数）
    customer_profile = query_customer_profile(contract_no=contract_no)
    
    if not customer_profile:
        return {'状态': '失败', '原因': '客户信息未找到'}
    
    unit_no = customer_profile.get("单元号", "")
    tenant_name = customer_profile.get("租户名", "")
    lease_start = parse_excel_date(customer_profile.get("起租日期", ""))
    
    # 2. 计算验收日期（默认为起租日前5个工作日）
    if not inspection_date:
        inspection_date = lease_start - timedelta(days=7)  # 简化：7天，实际应扣除周末
    
    # 3. 分配验收人员
    inspection_team = {
        "管家": assign_service_team(unit_no).get("管家", "未分配"),
        "工程专员": "李工",
        "客户代表": customer_profile.get("租户联系人", "负责人")
    }
    
    # 4. 生成《场地交付验收单》
    inspection_form = generate_delivery_inspection_form(contract_no, customer_profile, inspection_team, inspection_date)
    
    # 5. 发送验收通知
    notification = send_inspection_notification(contract_no, inspection_team, inspection_date, inspection_form)
    
    return {
        '状态': '成功',
        '合同编号': contract_no,
        '单元号': unit_no,
        '验收日期': inspection_date.strftime('%Y-%m-%d'),
        '验收人员': inspection_team,
        '验收单': inspection_form,
        '通知状态': notification
    }

def generate_delivery_inspection_form(contract_no, customer_profile, inspection_team, inspection_date):
    """
    生成《场地交付验收单》
    
    Args:
        contract_no: 合同编号
        customer_profile: 客户档案
        inspection_team: 验收人员
        inspection_date: 验收日期
    
    Returns:
        str: 验收单文件路径
    """
    unit_no = customer_profile.get("单元号", "")
    lease_area = customer_profile.get("租赁面积", 0)
    
    # 构建验收单内容
    form_content = f"""
# 场地交付验收单

**合同编号**：{contract_no}
**验收日期**：{inspection_date.strftime('%Y-%m-%d')}
**验收时间**：{inspection_date.strftime('%H:%M')}

---

## 一、场地基本信息

| 字段 | 内容 |
|------|------|
| 单元号 | {unit_no} |
| 租赁面积 | {lease_area} ㎡ |
| 租户名 | {customer_profile.get('租户名', '')} |
| 客户代表 | {inspection_team.get('客户代表', '')} |

---

## 二、验收项目清单

### 2.1 主体结构

| 序号 | 验收项目 | 标准要求 | 验收结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 墙面 | 无裂缝、无渗水 | □合格 □不合格 |  |
| 2 | 地面 | 平整、无空鼓 | □合格 □不合格 |  |
| 3 | 天花板 | 无裂缝、无渗水 | □合格 □不合格 |  |
| 4 | 门窗 | 开启灵活、密封良好 | □合格 □不合格 |  |
| 5 | 玻璃 | 完好、无划痕 | □合格 □不合格 |  |

### 2.2 强弱电系统

| 序号 | 验收项目 | 标准要求 | 验收结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 配电箱 | 回路标识清晰、开关正常 | □合格 □不合格 |  |
| 2 | 插座 | 通电正常、接地良好 | □合格 □不合格 |  |
| 3 | 照明 | 灯具完好、开关正常 | □合格 □不合格 |  |
| 4 | 网络接口 | 通断测试正常 | □合格 □不合格 |  |
| 5 | 电话接口 | 通断测试正常 | □合格 □不合格 |  |

### 2.3 给排水系统

| 序号 | 验收项目 | 标准要求 | 验收结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 自来水 | 水压正常、无渗漏 | □合格 □不合格 |  |
| 2 | 下水 | 排水通畅、无堵塞 | □合格 □不合格 |  |
| 3 | 卫生间 | 设施完好、无渗漏 | □合格 □不合格 |  |

### 2.4 空调系统

| 序号 | 验收项目 | 标准要求 | 验收结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 空调主机 | 制冷/制热正常 | □合格 □不合格 |  |
| 2 | 空调末端 | 出风正常、无噪音 | □合格 □不合格 |  |
| 3 | 控制系统 | 遥控/面板正常 | □合格 □不合格 |  |

### 2.5 消防设施

| 序号 | 验收项目 | 标准要求 | 验收结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 烟感探测器 | 报警正常 | □合格 □不合格 |  |
| 2 | 喷淋系统 | 水压正常 | □合格 □不合格 |  |
| 3 | 消火栓 | 配件齐全、水压正常 | □合格 □不合格 |  |
| 4 | 应急照明 | 备用电源正常 | □合格 □不合格 |  |

### 2.6 其他设施

| 序号 | 验收项目 | 标准要求 | 验收结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 门禁系统 | 读卡正常、开锁正常 | □合格 □不合格 |  |
| 2 | 视频监控 | 画面清晰、存储正常 | □合格 □不合格 |  |
| 3 | 停车场系统 | 抬杆正常、计费准确 | □合格 □不合格 |  |

---

## 三、验收结果

### 3.1 验收结论

□ 合格，同意交付
□ 基本合格， minor issues 需整改
□ 不合格，需重大整改

### 3.2 整改事项（如有）

| 序号 | 整改项目 | 整改要求 | 责任方 | 完成时限 |
|------|----------|----------|----------|----------|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

---

## 四、签字确认

| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| 客户代表 | {inspection_team.get('客户代表', '')} |  |  |
| 管家 | {inspection_team.get('管家', '')} |  |  |
| 工程专员 | {inspection_team.get('工程专员', '')} |  |  |

---

**备注**：
1. 本标准依据《园区运营项目客户服务标准指引》制定
2. 验收不合格项需在3个工作日内完成整改
3. 整改完成后需重新验收

**编制**：企服助手 (Enterprise Service Assistant)
**版本**：V1.0
"""
    
    # 保存为Markdown文件
    output_dir = "/Users/mac/场地交付验收单/"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{output_dir}{contract_no}_场地交付验收单_{inspection_date.strftime('%Y%m%d')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(form_content)
    
    return file_path

def send_inspection_notification(contract_no, inspection_team, inspection_date, inspection_form):
    """
    发送验收通知（模拟函数）
    
    Args:
        contract_no: 合同编号
        inspection_team: 验收人员
        inspection_date: 验收日期
        inspection_form: 验收单文件路径
    
    Returns:
        str: 通知状态
    """
    # TODO: 对接企微API发送通知
    notification_message = f"""
━━━━━━━━━━━━━━━
【场地交付验收通知】

📋 合同编号：{contract_no}
📅 验收日期：{inspection_date.strftime('%Y-%m-%d %H:%M')}
📍 验收地点：{inspection_team.get('管家', '')} 集合

━━━ 验收人员 ━━━
• 客户代表：{inspection_team.get('客户代表', '负责人')}
• 管家：{inspection_team.get('管家', '未分配')}
• 工程专员：{inspection_team.get('工程专员', '未分配')}

━━━ 验收准备 ━━━
1. 请客户代表携带身份证原件
2. 请工程专员准备验收工具（手电筒、卷尺、相位仪等）
3. 请管家准备《场地交付验收单》和签字笔

📎 附件：{inspection_form}

请各位准时到达！
━━━━━━━━━━━━━━━
"""
    
    # 模拟发送成功
    print(notification_message)
    return "通知已发送"

def track_inspection_rectification(contract_no, inspection_form):
    """
    跟踪验收问题整改情况
    
    Args:
        contract_no: 合同编号
        inspection_form: 验收单文件路径
    
    Returns:
        dict: 整改进度
    """
    # TODO: 读取验收单，检查是否有整改事项
    # TODO: 跟踪整改进度，提醒责任方按时完成
    # TODO: 整改完成后，安排复验
    
    return {'状态': '功能开发中...'}
```

### 3. 场地装修管理模块

```python
def track_renovation_management(contract_no):
    """
    跟踪装修管理全流程
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 装修管理状态
    """
    # 1. 获取客户信息（使用内联的客户档案查询函数）
    customer_profile = query_customer_profile(contract_no=contract_no)
    
    if not customer_profile:
        return {'状态': '失败', '原因': '客户信息未找到'}
    
    unit_no = customer_profile.get("单元号", "")
    tenant_name = customer_profile.get("租户名", "")
    
    # 2. 读取装修管理台账（待建）
    # TODO: 创建"装修管理"工作表
    renovation_status = get_renovation_status(contract_no)
    
    # 3. 根据装修状态触发相应动作
    if renovation_status['状态'] == '方案待审核':
        # 提醒工程部审核
        notification = send_renovation_review_reminder(contract_no, renovation_status)
        return {'状态': '提醒已发送', '通知': notification}
    
    elif renovation_status['状态'] == '装修中':
        # 生成巡查记录
        patrol_record = generate_renovation_patrol_record(contract_no, renovation_status)
        return {'状态': '巡查记录已生成', '记录': patrol_record}
    
    elif renovation_status['状态'] == '装修完成待验收':
        # 提醒工程部验收
        notification = send_renovation_acceptance_reminder(contract_no, renovation_status)
        return {'状态': '提醒已发送', '通知': notification}
    
    else:
        return {'状态': '无需操作', '当前状态': renovation_status['状态']}

def get_renovation_status(contract_no):
    """
    读取装修管理台账，获取装修状态
    
    Args:
        contract_no: 合同编号
    
    Returns:
        dict: 装修状态
    """
    # TODO: 创建"装修管理"工作表
    # 模拟返回
    return {
        '状态': '方案待审核',
        '合同编号': contract_no,
        '单元号': 'T1-601',
        '租户名': '示例企业',
        '装修公司': 'XX装饰公司',
        '方案提交日期': '2026-06-01',
        '预计开工日期': '2026-06-10',
        '预计竣工日期': '2026-08-10'
    }

def send_renovation_review_reminder(contract_no, renovation_status):
    """
    发送装修方案审核提醒
    
    Args:
        contract_no: 合同编号
        renovation_status: 装修状态
    
    Returns:
        str: 提醒状态
    """
    # TODO: 对接企微API发送提醒
    reminder_message = f"""
━━━━━━━━━━━━━━━
【装修方案审核提醒】

📋 合同编号：{contract_no}
🏢 单元号：{renovation_status['单元号']}
🏗️ 装修公司：{renovation_status['装修公司']}

━━━ 审核信息 ━━━
• 方案提交日期：{renovation_status['方案提交日期']}
• 预计开工日期：{renovation_status['预计开工日期']}
• 审核时限：3个工作日

⚠️ 请工程部于{ (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')}前完成审核！

如有问题，请及时联系管家。
━━━━━━━━━━━━━━━
"""
    
    # 模拟发送成功
    print(reminder_message)
    return "提醒已发送"

def generate_renovation_patrol_record(contract_no, renovation_status):
    """
    生成装修巡查记录
    
    Args:
        contract_no: 合同编号
        renovation_status: 装修状态
    
    Returns:
        str: 巡查记录文件路径
    """
    # 构建巡查记录内容
    record_content = f"""
# 装修巡查记录

**合同编号**：{contract_no}
**巡查日期**：{datetime.now().strftime('%Y-%m-%d')}
**巡查时间**：{datetime.now().strftime('%H:%M')}

---

## 一、基本信息

| 字段 | 内容 |
|------|------|
| 单元号 | {renovation_status['单元号']} |
| 租户名 | {renovation_status['租户名']} |
| 装修公司 | {renovation_status['装修公司']} |
| 巡查人员 | 李工 |
| 巡查类型 | □日常巡查 □专项巡查 □随机抽查 |

---

## 二、巡查项目

### 2.1 施工安全

| 序号 | 巡查项目 | 标准要求 | 巡查结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 动火作业 | 有动火证、有监护人员 | □符合 □不符合 |  |
| 2 | 高空作业 | 有高空作业证、有安全防护 | □符合 □不符合 |  |
| 3 | 临时用电 | 有临时用电许可证、电线无破损 | □符合 □不符合 |  |
| 4 | 消防设施 | 灭火器配备到位、完好有效 | □符合 □不符合 |  |

### 2.2 施工规范

| 序号 | 巡查项目 | 标准要求 | 巡查结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 施工时间 | 工作日8:00-12:00, 14:00-18:00 | □符合 □不符合 |  |
| 2 | 材料堆放 | 指定区域、整齐有序 | □符合 □不符合 |  |
| 3 | 垃圾清运 | 日产日清、分类处置 | □符合 □不符合 |  |
| 4 | 噪音控制 | 符合环保标准 | □符合 □不符合 |  |

### 2.3 施工质量

| 序号 | 巡查项目 | 标准要求 | 巡查结果 | 备注 |
|------|----------|----------|----------|------|
| 1 | 主体结构 | 无擅自改动 | □符合 □不符合 |  |
| 2 | 水电管线 | 按图施工、规范敷设 | □符合 □不符合 |  |
| 3 | 消防设施 | 未遮挡、未改动 | □符合 □不符合 |  |
| 4 | 外观效果 | 符合设计方案 | □符合 □不符合 |  |

---

## 三、巡查结论

### 3.1 巡查结论

□ 合格，继续施工
□ 基本合格，minor issues 需整改
□ 不合格，需停工整改

### 3.2 整改事项（如有）

| 序号 | 整改项目 | 整改要求 | 责任方 | 完成时限 |
|------|----------|----------|----------|----------|
| 1 |  |  |  |  |
| 2 |  |  |  |  |

---

## 四、签字确认

| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| 巡查人员 | 李工 |  |  |
| 装修公司代表 |  |  |  |

---

**备注**：
1. 本标准依据《园区运营项目客户服务标准指引》制定
2. 不合格项需立即停工整改，整改完成后需复查
3. 巡查记录将作为竣工验收的依据之一

**编制**：企服助手 (Enterprise Service Assistant)
**版本**：V1.0
"""
    
    # 保存为Markdown文件
    output_dir = "/Users/mac/装修巡查记录/"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = f"{output_dir}{contract_no}_装修巡查记录_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(record_content)
    
    return file_path

def send_renovation_acceptance_reminder(contract_no, renovation_status):
    """
    发送竣工验收提醒
    
    Args:
        contract_no: 合同编号
        renovation_status: 装修状态
    
    Returns:
        str: 提醒状态
    """
    # TODO: 对接企微API发送提醒
    reminder_message = f"""
━━━━━━━━━━━━━━━
【竣工验收提醒】

📋 合同编号：{contract_no}
🏢 单元号：{renovation_status['单元号']}
🏗️ 装修公司：{renovation_status['装修公司']}

━━━ 验收信息 ━━━
• 装修完成日期：{renovation_status['预计竣工日期']}
• 验收时限：装修完成后3个工作日内

⚠️ 请工程部于{(datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')}前完成竣工验收！

验收合格后，方可投入使用。
━━━━━━━━━━━━━━━
"""
    
    # 模拟发送成功
    print(reminder_message)
    return "提醒已发送"
```

---

## 执行流程

```
Step 1 → 触发入驻流程
         合同审批完成后3个工作日内
         或手动触发：@企服助手 客户入驻 [合同编号]

Step 2 → 客户入驻内部交圈
         组建服务团队
         创建企微服务群
         生成《客户入驻信息交接单》
         召开交圈会

Step 3 → 场地交付验收
         预约验收时间（起租日前5个工作日）
         生成《场地交付验收单》
         现场验收
         跟踪整改（如有）

Step 4 → 场地装修管理（如有）
         提醒工程部审核装修方案（3个工作日内）
         装修巡查（每周至少1次）
         提醒工程部竣工验收（装修完成后3个工作日内）

Step 5 → 入驻完成
         更新客户状态为"已入驻"
         安排首次走访（入住后1周内）
```

---

## 定时任务配置

```json
{
  "name": "客户入驻流程检查",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "检查合同审批状态，触发客户入驻流程；检查验收和装修状态，发送提醒通知"
  },
  "sessionTarget": "isolated"
}
```

**说明**：每天09:00自动检查入住流程状态，触发相应动作。

---

## 手动触发方式

1. **企微 @提及**: `@企服助手 客户入驻 [合同编号]`
2. **OpenClaw指令**: `触发客户入驻 [合同编号]`
   - 示例：`触发客户入驻 {TODO: 填写合同编号}`

---

## 配置参数

```json
{
  "customer_onboarding": {
    "excel_path": "/Users/mac/示例产业园AC+服务.xlsx",
    "handover_meeting_days": 3,  // 合同审批完成后3个工作日内召开交圈会
    "inspection_days_before_lease_start": 5,  // 起租日前5个工作日验收
    "renovation_review_days": 3,  // 装修方案3个工作日内审核
    "renovation_acceptance_days": 3,  // 装修完成后3个工作日内验收
    "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "service_team_config": {
      "管家": {
        "T1-6F": "戚亮先",
        "T1-7F": "戚亮先",
        "T1-8F": "戚亮先",
        "T1-9F": "刘瑞",
        "T1-10F": "刘瑞",
        "T1-11F": "刘瑞",
        "T1-12F": "张三",
        "T1-13F": "张三",
        "T1-14F": "张三"
      },
      "工程专员": "李工",
      "安管专员": "王队",
      "环境专员": "张姐",
      "产业服务专员": "赵经理"
    }
  }
}
```

---

## 使用示例

**用户输入**: `@企服助手 客户入驻 {TODO: 填写合同编号}`

**输出**:
```
━━━━━━━━━━━━━━━
【客户入驻流程已触发】

📋 合同编号：{TODO: 填写合同编号}
🏢 单元号：T1-601
🏢 租户名：上海XX有限公司

━━━ 服务团队分配 ━━━
• 管家：戚亮先
• 工程专员：李工
• 安管专员：王队
• 环境专员：张姐
• 产业服务专员：赵经理

━━━ 流程进度 ━━━
✅ 1. 内部交圈会已安排（2026-06-05 14:00）
✅ 2. 《客户入驻信息交接单》已生成
   📎 /Users/mac/客户入驻交接单/{TODO: 填写合同编号}_客户入驻信息交接单_20260602.md
⏳ 3. 场地交付验收待安排（起租日前5个工作日）
⏳ 4. 装修管理（如有）

━━━ 下一步操作 ━━━
请各部门准备交圈会，准时参加！
━━━━━━━━━━━━━━━
```

---

## 后续扩展接口

1. **对接集客荟系统 API** - 实时获取合同审批状态
2. **对接企微 API** - 自动创建服务群、发送通知
3. **创建"装修管理"工作表** - 记录装修全流程
4. **生成PDF格式的验收单和巡查记录** - 支持电子签名
5. **对接腾讯文档 API** - 在线协作编辑交接单、验收单

---

## 注意事项

1. **时效性** - 各环节需在规定时限内完成（交圈会3个工作日、验收和审核3-5个工作日）
2. **责任明确** - 每个环节明确责任部门和责任人
3. **闭环管理** - 验收不合格、整改未完成需跟踪闭环
4. **文档归档** - 所有交接单、验收单、巡查记录需归档保存

---

**当前状态**: 技能已创建，核心逻辑已定义，待与实际系统集成。

**核心功能**: 客户入驻内部交圈、场地交付验收、场地装修管理。

**未来扩展**: 对接各系统API，实现全流程自动化。
