# CDISC Skill 速查表

## 🔑 常用量表代码 (QRS)

| 代码 | 名称 | 说明 |
|------|------|------|
| `AIMS01` | Abnormal Involuntary Movement Scale | 异常不自主运动量表 |
| `CGI01` | Clinical Global Impression | 临床总体印象量表 |
| `CGI02` | Clinical Global Impression - Severity | 临床总体印象 - 严重程度 |
| `HAM-A` | Hamilton Anxiety Rating Scale | 汉密尔顿焦虑量表 |
| `HAM-D` | Hamilton Depression Rating Scale | 汉密尔顿抑郁量表 |
| `MMSE` | Mini-Mental State Examination | 简易精神状态检查 |
| `PANSS` | Positive and Negative Syndrome Scale | 阳性和阴性症状量表 |
| `YMRS` | Young Mania Rating Scale | 杨氏躁狂评定量表 |
| `GAD-7` | Generalized Anxiety Disorder 7-item | 广泛性焦虑障碍量表 |
| `PHQ-9` | Patient Health Questionnaire 9 | 患者健康问卷抑郁量表 |
| `SF-36` | Short Form 36 | 健康调查简表 |
| `EQ-5D` | EuroQol 5 Dimensions | 欧洲五维健康量表 |

## 📊 ADaM 常用数据结构

| 代码 | 说明 |
|------|------|
| `ADSL` | Subject Level Analysis Data |
| `ADAE` | Adverse Events Analysis Data |
| `ADCM` | Concomitant Medications Analysis Data |
| `ADEC` | Disease Characteristics Analysis Data |
| `ADEG` | ECG Results Analysis Data |
| `ADEX` | Efficacy Results Analysis Data |
| `ADLB` | Laboratory Results Analysis Data |
| `ADMH` | Medical History Analysis Data |
| `ADPP` | Pharmacokinetics Results Analysis Data |
| `ADRS` | Response Results Analysis Data |
| `ADTTE` | Time to Event Analysis Data |
| `ADPC` | Pharmacokinetics Concentrations Analysis Data |
| `ADES` | Exposure Summary Analysis Data |

## 🏷️ SDTM 常用域

### 特殊目的域
| 代码 | 说明 |
|------|------|
| `DM` | Demographics |
| `SE` | Subject Elements |
| `SV` | Subject Visits |

### 试验设计域
| 代码 | 说明 |
|------|------|
| `TA` | Trial Arms |
| `TE` | Trial Elements |
| `TI` | Trial Inclusion/Exclusion |
| `TV` | Trial Visits |

### 发现域
| 代码 | 说明 |
|------|------|
| `LB` | Laboratory Results |
| `VS` | Vital Signs |
| `EG` | Electrocardiogram |
| `QS` | Questionnaires |
| `SC` | Subject Characteristics |
| `SD` | Supplemental Qualifiers for Findings |

### 事件域
| 代码 | 说明 |
|------|------|
| `AE` | Adverse Events |
| `CE` | Clinical Events |
| `MH` | Medical History |

### 干预域
| 代码 | 说明 |
|------|------|
| `CM` | Concomitant Medications |
| `EX` | Exposure |
| `PR` | Procedures |
| `ECOG` | ECOG Performance Status |

### 关系域
| 代码 | 说明 |
|------|------|
| `RELREC` | Related Records |
| `CO` | Comments |

## 🔢 受控术语代码列表示例

| 代码 | 说明 |
|------|------|
| `C102111` | Yes/No |
| `C118971` | Present/Absent |
| `C28077` | Male/Female |
| `C38114` | Alive/Dead |
| `C49487` | Completed/Not Completed |
| `C66742` | Screening/Enrollment |

## 📋 版本号格式

- **正确**: `2-0`, `1-1`, `3-4` (数字 - 数字)
- **错误**: `2.0`, `1.1`, `3.4` (不要用点)

### 常用版本
| 标准 | 常用版本 |
|------|---------|
| SDTMIG | `3-4`, `3-3`, `3-2` |
| CDASH | `1-0`, `1-1` |
| ADaM | `adam-2-1`, `adamig-1-3` |

## 🔧 命令速查

### 基础查询
```bash
# 查看所有产品
/cdisc-library-api products

# 查询量表（自动最新版）
/cdisc-library-api qrs AIMS01

# 查询指定版本
/cdisc-library-api qrs AIMS01 2-0

# 查看量表项目
/cdisc-library-api items AIMS01 2-0

# 查询 ADaM 产品
/cdisc-library-api adam adam-2-1

# 查询 ADaM 数据结构
/cdisc-library-api adam adam-2-1 ADSL

# 查询 SDTM 域
/cdisc-library-api sdtm 3-4 DM

# 查询 CDASH 域
/cdisc-library-api cdash 1-0 DM

# 查询受控术语
/cdisc-library-api ct C102111

# 查询术语包列表
/cdisc-library-api ct-packages
```

### 高级查询
```bash
# 搜索
/cdisc-library-api search USUBJID

# 版本比较
/cdisc-library-api compare qrs AIMS01 1-0 2-0

# 根资源
/cdisc-library-api root qrs

# 文档
/cdisc-library-api docs

# 规则
/cdisc-library-api rules adam
```

### 工具
```bash
# 导出 JSON
/cdisc-library-api export items AIMS01 2-0

# 导出 CSV
/cdisc-library-api export items AIMS01 2-0 --format=csv

# 批量查询
/cdisc-library-api batch queries.txt

# 缓存状态
/cdisc-library-api cache status

# 清除缓存
/cdisc-library-api cache clear
```

## 🌐 相关链接

- [CDISC Library Browser](https://library.cdisc.org/browser)
- [API Portal](https://api.developer.library.cdisc.org)
- [API Documentation](https://api.developer.library.cdisc.org/api-details)
- [Service Desk](https://jira.cdisc.org/servicedesk/customer/portal/2)
