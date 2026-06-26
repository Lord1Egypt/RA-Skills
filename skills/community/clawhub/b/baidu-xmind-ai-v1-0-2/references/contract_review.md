# 百度智能文档分析平台 - 合同审查API

## 概述

合同审查支持多种合同场景审查，精准定位关键审查点，提供专业的风险评估、判断依据及修改建议，加速合同审查流程。

## API特点

- **异步接口**：需要先提交请求获取 taskId，然后轮询结果
- **建议轮询时间**：提交请求后 1～2 分钟开始轮询
- **QPS限制**：提交请求接口 2 QPS，获取结果接口 10 QPS

## 支持的合同类型

该清单类型为系统预置清单，每次审查任务仅可选择单一清单：

| 模板名称 | 说明 |
|---------|------|
| Sales_PartyA_V2 | 买卖合同-买方 |
| Sales_PartyB_V2 | 买卖合同-卖方 |
| Lease_PartyA_V2 | 租赁合同-出租方 |
| Lease_PartyB_V2 | 租赁合同-承租方 |
| TechDev_PartyA_V2 | 技术开发合同-委托方 |
| TechDev_PartyB_V2 | 技术开发合同-受托方 |
| Labor_PartyA_V2 | 劳动合同-用人单位 |
| Labor_PartyB_V2 | 劳动合同-劳动者 |
| Entrustment_PartyA_V2 | 委托合同-委托方 |
| Entrustment_PartyB_V2 | 委托合同-受托方 |
| Work-for-hire_PartyA_V2 | 承揽合同-定作人 |
| Work-for-hire_PartyB_V2 | 承揽合同-承揽人 |
| LaborDispatch_PartyA_V2 | 劳务派遣合同-用工单位 |
| LaborDispatch_PartyB_V2 | 劳务派遣合同-劳务派遣单位 |
| RealtySvcs_PartyA_V2 | 物业服务合同-业主 |
| RealtySvcs_PartyB_V2 | 物业服务合同-物业服务人 |
| EquipPur_PartyA_V2 | 设备采购合同-买方 |
| EquipPur_PartyB_V2 | 设备采购合同-卖方 |
| FinLease_PartyA_V2 | 融资租赁合同-出租方 |
| FinLease_PartyB_V2 | 融资租赁合同-承租方 |
| DebtAssign_PartyA_V2 | 债权转让合同-转让方 |
| DebtAssign_PartyB_V2 | 债权转让合同-受让方 |
| CISG_PartyA_V2 | 国际货物贸易合同-买方 |
| CISG_PartyB_V2 | 国际货物贸易合同-卖方 |
| GUAR_PartyA_V2 | 保证合同-保证方 |
| GUAR_PartyB_V2 | 保证合同-债权方 |
| CG_PartyA_V2 | 货运合同-承运方 |
| CG_PartyB_V2 | 货运合同-托运方 |
| Factoring_PartyA_V2 | 保理合同-保理商 |
| Factoring_PartyB_V2 | 保理合同-卖方 |
| Brokerage_PartyA_V2 | 中介合同-委托人 |
| Brokerage_PartyB_V2 | 中介合同-中介人 |
| TradingTrust_PartyA_V2 | 行纪合同-委托人 |
| TradingTrust_PartyB_V2 | 行纪合同-行纪人 |
| PNRship_V2 | 合伙合同-合伙人 |
| PT/PAT_PartyA_V2 | 专利（申请）权转让合同-受让方 |
| PT/PAT_PartyB_V2 | 专利（申请）权转让合同-转让方 |
| TST_PartyA_V2 | 技术秘密转让合同-受让方 |
| TST_PartyB_V2 | 技术秘密转让合同-转让方 |
| TechLic_PartyA_V2 | 技术许可合同-许可方 |
| TechLic_PartyB_V2 | 技术许可合同-被许可方 |
| EquipLea_PartyA_V2 | 设备租赁合同-出租方 |
| EquipLea_PartyB_V2 | 设备租赁合同-承租方 |
| ConstCtrl_PartyA_V2 | 建设工程施工合同-发包方 |
| ConstCtrl_PartyB_V2 | 建设工程施工合同-承包方 |

## 提交请求接口

**请求URL**：
```
POST https://aip.baidubce.com/file/2.0/brain/online/v1/textreview/task?access_token={access_token}
```

**请求参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| file | file | 二选一 | 文件数据（doc/docx/pdf） |
| fileURLList | string | 二选一 | 文件URL |
| templateName | string | 必填 | 合同类型模板名称（见上表） |
| commentRiskLevel | string | 否 | 风险等级筛选：normal/major/all |

## 获取结果接口

**请求URL**：
```
POST https://aip.baidubce.com/file/2.0/brain/online/v1/textreview/task/query?access_token={access_token}
```

**请求参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| taskId | string | 是 | 提交请求返回的任务ID |

## 返回结果说明

| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | 任务状态：Success/Failed |
| reason | string | 失败原因 |
| result | object | 审查结果，包含风险点和修改建议 |

## 使用示例

```python
from baidu_api_client import BaiduDocAIClient

client = BaiduDocAIClient()
result = client.contract_review(
    file_data=file_data,
    file_name="合同.pdf",
    template_name="Sales_PartyA_V2"  # 买卖合同-买方
)
```

## 参考链接

- [官方API文档](https://ai.baidu.com/ai-doc/OCR/olqc085rg)
