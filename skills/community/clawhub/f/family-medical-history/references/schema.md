# Family Medical History — Schema Reference

## Directory Structure

```
medical_records/
├── [member_code]/            # 代号/昵称（脱敏处理）
│   ├── profile.md            # 个人核心健康主页（最重要，优先级最高读取）
│   ├── visits/               # 就诊记录
│   │   └── V-YYYYMMDD-XX.md   # 每一次就诊一个文件
│   ├── medications/           # 用药记录
│   │   └── M-YYYYMMDD-XXX.md  # 每疗程/每次处方一个文件
│   ├── exams/                 # 检查报告
│   │   └── E-YYYYMMDD-XXX.md  # 每项检查一个文件
│   ├── daily_vitals/         # 日常体征
│   │   ├── YYYY.md            # 或 YYYY.csv
│   │   └── YYYY.md
│   └── attachments/          # 影像与扫描件
│       ├── 2026/
│       │   ├── E-YYYYMMDD-XXX_Report_[检查名].jpg
│       │   ├── M-YYYYMMDD-XXX_Prescription_[药名].jpg
│       │   └── V-YYYYMMDD-XX_Summary_[类型].pdf
│       └── 2027/
└── templates/               # 标准模板（仅初始化时使用）
```

## ID Naming Conventions

| 记录类型 | 格式 | 示例 |
|----------|------|------|
| 就诊记录 | V-YYYYMMDD-XX | V-20260318-01 |
| 用药记录 | M-YYYYMMDD-XXX | M-20260318-01 |
| 检查报告 | E-YYYYMMDD-XXX | E-20260319-01 |

- `YYYYMMDD` = 就诊/检查/开药的实际日期
- `XX` / `XXX` = 同日多条的序号（01, 02, 03...）
- **注意**：不要按"药名"建立多个文件，同一药品的续疗程也要使用新的M-ID

## Attachment Naming Convention

```
[关联ID]_[文件类型]_[核心描述].[后缀]
```

| 文件类型标签 | 含义 |
|-------------|------|
| Report | 检查报告 |
| Scan | 影像胶片 |
| Photo | 现场照片 |
| Prescription | 处方单 |
| Package | 药品包装 |
| Summary | 病历摘要/出院小结 |
| Specimen | 标本/分泌物 |

**示例**：
- `E-20260319-01_Report_BloodRoutine.jpg` — 血常规报告
- `E-20260319-02_Scan_ChestCT.png` — 胸部CT影像
- `M-20260318-01_Prescription_Amoxicillin.jpg` — 阿莫西林处方
- `V-20260319-01_Summary_Discharge.pdf` — 出院小结
- `V-20260325-01_Specimen_NasalDischarge.jpg` — 鼻涕标本照

## Relationship Keys

```
Visit_ID (V-YYYYMMDD-XX)
  ├──→ Medication_ID (M-YYYYMMDD-XXX)
  ├──→ Exam_ID (E-YYYYMMDD-XXX)
  └──→ Attachment files
```

Every medication and exam should link back to its originating visit.

## Profile.md — Field Guide

### 🚨 紧急医疗摘要（文件最顶部）
| 字段 | 说明 | 示例 |
|------|------|------|
| 紧急联系人 | 姓名 / 电话 | 张三 / 138-0000-0000 |
| 血型 | 含RH阴阳性 | A型 / RH阳性 |
| 严重过敏 | 致死级危险标红 | 青霉素（过敏性休克史） |
| 当前重大疾病 | 慢性病/植入物 | 哮喘、心脏起搏器 |
| 当前长期用药 | 救命药 | 胰岛素、抗凝药 |

### 状态标记
- **Active** — 仍在影响健康，需要持续管理
- **Resolved** — 已治愈/已缓解
- **Chronic** — 慢性病标注（等同于Active但强调持续性）

## Visit Record — Field Guide

| 字段 | 说明 |
|------|------|
| 就诊类型 | 门诊（最常用）/ 急诊 / 住院 / 在线问诊 |
| 主诉 | 患者原话描述的最主要症状（患者视角） |
| 现病史 | 医疗专业人员整理的症状发生发展经过（医疗视角） |
| 诊断 | 主诊断=最主要需要处理的，次诊断=伴随/相关 |
| 病程记录 | 用于慢性/持续性症状：症状特征、频率、起始时间 |
| 随访提醒 | 下次复诊日期、观察指标 |

## Medication Record — Field Guide

| 字段 | 说明 |
|------|------|
| 按疗程记录 | 一个M-ID = 一次处方/一个疗程；同药续药 = 新M-ID |
| 追踪表 | 记录每次计划的日期和实际执行状态 |
| Status | Current = 仍在服用；Discontinued = 已停药（含原因） |
| 依从性 | 按计划 / 漏用 / 自行调整 / 中途停药 |
| 不良反应 | 有/无；如有需描述症状和停药决策 |

## Data Entry Rules

1. **Never fabricate**: If unknown, write "待确认" or "待填写"
2. **Use exact dates**: YYYY-MM-DD format everywhere
3. **Link everything**: Every record should reference its parent Visit_ID
4. **Update indices**: After creating any record, add to profile.md's index sections
5. **Mark resolved properly**: Don't close a visit/medication until confirmed
6. **Chronic symptoms**: Don't call "复发" unless explicitly confirmed as such
