# 零上传隐私计算（V7 核心承诺）

> V7 的核心承诺：**学生数据、试卷答案、家长隐私等敏感内容永远不离开本地电脑**。只有抽象后的元数据（标签 / 描述 / 决策请求）与云端交互。

## 1. 4 级 PII 自动脱敏

V7 在端侧实现 4 级 PII 自动脱敏：

### 1.1 一级 · 标识符脱敏
- 姓名（中文/英文）→ `学生A`、`学生B`、编号
- 身份证号 → `ID:**** **** **** 1234`
- 手机号 → `138****5678`
- 邮箱 → `***@***.com`
- 学号 / 工号 → 统一编码

### 1.2 二级 · 关系脱敏
- 家庭住址 → `某省某市`
- 学校名 → `某中学`
- 班级 → `某班`
- 父母姓名 / 职业 → `家长A`、`家长B`

### 1.3 三级 · 行为脱敏
- 答题时间戳 → 时间段（早/中/晚）
- 答题路径 → 抽象描述
- 行为日志 → 行为模式标签

### 1.4 四级 · 内容脱敏
- 学生作文内容 → 仅保留主题关键词
- 课堂发言 → 仅保留讨论方向
- 心理评估 → 仅保留维度分数，不保留具体回答

## 2. 零上传证明（Zero-Upload Proof · ZUP）

V7 提供可审计的零上传证明机制：

### 2.1 证明内容
- 上传数据大小（< 10KB/请求）
- PII 检测结果（`pii_detected: false`）
- 数据分类（`anonymous`）
- 上传文件 hash（如有）
- 接收方 + 时间戳

### 2.2 证明存储
```json
{
  "zup_id": "zup-uuid-xxx",
  "timestamp": "2026-08-15T10:00:00Z",
  "abstract_data_size_bytes": 8192,
  "abstract_data_hash": "sha256:abc...",
  "pii_scan_result": {
    "pii_detected": false,
    "scan_method": "regex+ml",
    "pii_types_scanned": ["name", "id", "phone", "email", "address", "school"]
  },
  "data_classification": "anonymous",
  "recipient": "openai-api",
  "purpose": "creative_decision",
  "audit_log": "/var/log/ai-literacy/audit.log"
}
```

### 2.3 证明验证
- 第三方可下载 zup_audit.json 验证
- 验证内容：每次请求的 abstract_data_size + pii_detected + data_classification
- 任何 `pii_detected: true` 的记录都标记为「**违规**」

## 3. 数据生命周期管理

### 3.1 原始数据 7 天保留
- **本地端**：原始数据保留 7 天
- **清理策略**：7 天后自动加密删除
- **合规依据**：GDPR「数据最小化原则」+ 中国《个人信息保护法》

### 3.2 抽象元数据 30 天保留
- 上传到云端的元数据，云端保留 30 天
- 30 天后云端自动删除
- 端侧保留元数据的本地副本（用于复盘）

### 3.3 教学决策永久保留
- 云端返回的"决策 / 建议 / 文本"作为教学资产
- 端侧归档到 IndexedDB
- 教师可随时查阅历史决策

## 4. 法规合规

V7 零上传架构符合 3 大法规：

### 4.1 GDPR（欧盟通用数据保护条例）
- ✅ 数据最小化
- ✅ 目的限制
- ✅ 存储限制
- ✅ 完整性与保密性
- ✅ 问责制

### 4.2 中国《个人信息保护法》
- ✅ 知情同意
- ✅ 最小必要
- ✅ 公开透明
- ✅ 数据本地化（中国公民数据境内存储）
- ✅ 安全保障

### 4.3 COPPA（美国儿童在线隐私保护法）
- ✅ 13 岁以下儿童数据需监护人同意
- ✅ 不收集超出必要的数据
- ✅ 家长可查看/删除子女数据
- ✅ 不用于商业广告

## 5. 实战场景

### 场景 1：试卷分析
```
[教师操作] 上传 40 名学生成绩单（CSV）
[端侧扫描] PII 检测 → 发现 40 个学生姓名 + 身份证号
[端侧脱敏] 姓名 → 学生A1-A40；身份证号 → 编码
[端侧抽象化] 数据压缩为标签 + 统计（< 8KB）
[云端] 上传匿名统计 → LLM 教学建议
[端侧] 接收建议 → 生成诊断报告
[端侧审计] ZUP 记录：抽象 8KB / PII false / 分类 anonymous
[7 天后] 端侧自动清理原始 CSV
```

### 场景 2：课堂录音分析
```
[教师操作] 上传 30 分钟课堂录音
[端侧 NPU] ASR 转写（30 分钟 → 全文 < 2s）
[端侧 PII] 检测学生姓名（出现 15 次）→ 脱敏
[端侧抽象] 文本 → 关键词 + 互动次数 + 教师提问数（< 5KB）
[云端] 上传抽象数据 → LLM 教学反思
[端侧] 接收反思 → 写入教师档案
[端侧审计] 原始录音保留 7 天 → 自动清理
```

### 场景 3：家长沟通
```
[教师操作] 输入学生姓名 + 最近表现描述
[端侧 PII] 检测学生姓名 + 家长姓名
[端侧抽象] 表现 → 维度分数（学业/品德/社交）（< 2KB）
[云端] 上传维度分数 → LLM 沟通话术
[端侧] 教师审阅话术 → 发送给家长
[端侧审计] 姓名不上传，仅上传维度分数
```

## 6. PII 检测实现

V7 端侧 PII 检测采用**正则 + ML 双重检测**：

### 6.1 正则检测
```python
PATTERNS = {
    'name_cn': r'[\u4e00-\u9fa5]{2,4}',  # 2-4 字中文名（高误报，需配合白名单）
    'id_card': r'\d{17}[\dXx]',         # 18 位身份证
    'phone': r'1[3-9]\d{9}',            # 11 位手机号
    'email': r'[\w.]+@[\w.]+',
    'address': r'[\u4e00-\u9fa5]{2,}[省市区县][\u4e00-\u9fa5]{0,20}',
    'school': r'[\u4e00-\u9fa5]{2,}(小学|初中|高中|大学)',
}
```

### 6.2 ML 检测（基于 BERT）
- 模型：`bert-base-chinese-pii-detect`
- 推理位置：NPU 优先
- 延迟：< 100ms / 1000 字符
- 召回率：> 95%

### 6.3 白名单管理
- 教师可维护白名单（如班级学生姓名表）
- 白名单内姓名不脱敏（避免破坏教学场景）
- 非白名单姓名自动脱敏

## 7. 端云交互审计

V7 在端侧维护完整的审计日志：

```json
{
  "audit_id": "audit-uuid-xxx",
  "timestamp": "2026-08-15T10:00:00Z",
  "event_type": "edge_cloud_interaction",
  "direction": "edge_to_cloud",
  "abstract_data_size_bytes": 5120,
  "abstract_data_preview": "学生成绩统计：平均 78...",
  "pii_scan": {
    "detected": false,
    "method": "regex+ml",
    "duration_ms": 23
  },
  "recipient": "openai-api",
  "purpose": "creative_decision",
  "response_size_bytes": 2048,
  "cost_usd": 0.0008,
  "zup_id": "zup-uuid-xxx"
}
```

## 8. 应急响应

### 8.1 误上传检测
- 监控 abstract_data_size 异常
- 检测到 > 10KB 立即报警
- 自动切断云端连接 5 分钟

### 8.2 隐私泄露响应
- 教师发现泄露 → 一键撤回
- 端侧生成撤回请求 → 云端删除数据
- 24 小时内提供泄露报告

### 8.3 教师申诉通道
- 教师可对脱敏结果申诉
- 申诉记录进入白名单
- 申诉过程全审计

## 9. PII 漏检（False Negative）应急机制

> **现实认知**：V7 端侧 PII 检测召回率 > 95%（正则 + ML 双重检测），但仍有最多 **5% 的 PII 可能漏检**并通过 abstract_data 上传到云端。本节定义漏检后的安全网机制。

### 9.1 五层安全网

1. **抽象数据大小异常检测**（已有）
   - `abstract_data` > 10KB 立即报警并切断
   - 大小异常往往是 PII 泄露的前兆信号

2. **内容抽样审计**
   - 每次请求后，随机抽取 5% 的 `abstract_data` 进行深度 PII 扫描
   - 抽样审计使用更严格的检测阈值（降低精确度、提高召回率）
   - 审计在端侧异步执行，不影响主流程延迟

3. **事后检测与应急响应**
   - 若在传输后发现 PII 漏检 → 立即触发「数据泄露应急预案」
   - 撤回云端响应（如尚未消费）
   - 请求云端删除已接收数据
   - 暂停云端调用 5 分钟（自动隔离）

4. **用户通知（GDPR 72 小时要求）**
   - 确认泄露后 **72 小时内**通知受影响用户
   - 通知内容：泄露数据类型、影响范围、已采取措施、用户可采取的保护措施
   - 通知方式：端侧弹窗 + 邮件（如有）

5. **根因分析与规则更新**
   - 分析漏检原因（新 PII 模式？白名单误配？正则覆盖不足？）
   - 更新 PII 检测规则库
   - 回归测试：用漏检样本验证新规则有效性
   - 记录经验教训到审计日志

### 9.2 漏检响应数据结构

```json
{
  "false_negative_response": {
    "incident_id": "fn-uuid-xxx",
    "detected_at": "2026-08-15T10:05:00Z",
    "detection_method": "post_transmission_sampling_audit",
    "pii_found": true,
    "pii_types": ["name", "phone"],
    "affected_request_id": "req-uuid-002",
    "actions": {
      "cloud_response_revoked": true,
      "cloud_data_deletion_requested": true,
      "cloud_calls_suspended": true,
      "suspension_duration_minutes": 5,
      "user_notification_sent": true,
      "user_notification_deadline": "2026-08-18T10:05:00Z",
      "root_cause_analysis_triggered": true
    },
    "root_cause": {
      "category": "regex_coverage_gap",
      "description": "新发现的地方方言姓名未被正则覆盖",
      "rule_updated": true,
      "regression_test_passed": true
    },
    "forensic_log_id": "forensic-uuid-xxx"
  }
}
```

### 9.3 漏检率持续监控

| 指标 | 目标 | 监控频率 |
|------|------|----------|
| PII 检测召回率 | > 95% | 每周评估 |
| 漏检事件数 | 0 | 实时监控 |
| 抽样审计覆盖率 | ≥ 5% | 每次请求 |
| 72h 用户通知达标率 | 100% | 每次事件 |
| 规则更新响应时间 | < 24h | 每次事件 |

## 10. 7 项检查清单

部署 V7 零上传隐私计算前必查：

- [ ] 启用端侧 PII 自动检测（正则 + ML）
- [ ] 配置白名单（教师可管理）
- [ ] 启用 7 天数据自动清理
- [ ] 启用 ZUP 零上传证明
- [ ] 启用端云交互审计
- [ ] 配置应急响应预案
- [ ] 教师培训（隐私合规 + 申诉流程）

---

> **核心承诺**：V7 = 「端云协同 + 零上传 + 7 天清理 + 100% 审计」= 教学 AI 隐私的最高标准。
