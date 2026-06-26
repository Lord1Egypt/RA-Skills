# Agent Security DLP 规则探索与迭代计划

> 版本: v1.0.0  
> 日期: 2026-03-17  
> 状态: 规划中

---

## 一、当前规则分析

### 1.1 现有规则统计

| 类别 | 数量 | 覆盖率 |
|------|------|--------|
| 凭证密钥 | 45 | 60% |
| 金融 | 18 | 50% |
| 医疗 | 15 | 40% |
| 人力资源 | 11 | 30% |
| 物流 | 11 | 30% |
| 汽车销售 | 14 | 40% |
| 其他 | 32 | 20% |

### 1.2 缺失领域

| 优先级 | 领域 | 说明 |
|--------|------|------|
| 🔴 高 | 加密货币钱包 | BTC/ETH/USDT 地址格式 |
| 🔴 高 | 生物识别 | 指纹、虹膜、面部数据 |
| 🟠 中 | 军事安全 | 军籍、保密级别 |
| 🟠 中 | 司法取证 | 案件编号、指纹 |
| 🟡 低 | 工业控制 | SCADA、PLC 标识 |

---

## 二、规则探索方向

### 2.1 金融行业扩展

```python
# 扩展金融规则
FINANCIAL_RULES = {
    # 加密货币
    "btc_address": "比特币地址",
    "eth_address": "以太坊地址",
    "usdt_address": "USDT-TRC20/ERC20",
    
    # 证券
    " securities_account": "证券账户",
    "fund_account": "基金账户",
    "futures_account": "期货账户",
    
    # 银行
    "credit_card_cvv": "信用卡CVV",
    "bank_card_bin": "银行卡BIN",
}
```

### 2.2 中国特色规则

```python
CHINA_SPECIFIC = {
    # 政府类
    "civil_servant_number": "公务员编号",
    "police_id": "警官证号",
    "military_id": "军官证号",
    
    # 政务类
    "social_credit_code": "统一社会信用代码",
    "org_code": "组织机构代码",
    "tax_id": "税务登记号",
    
    # 教育类
    "student_id": "学号",
    "exam_ticket": "准考证号",
    "teacher_id": "教师资格证号",
}
```

### 2.3 国际规则

```python
INTERNATIONAL = {
    # 美国
    "us_passport": "美国护照",
    "us_driver_license": "美国驾照",
    "us_itin": "美国税号(ITIN)",
    
    # 欧盟
    "eu_passport": "欧盟护照",
    "eu_national_id": "欧盟身份证",
    "ni_number": "英国社保号(NI)",
    
    # 亚太
    "hk_id": "香港身份证",
    "tw_id": "台湾身份证",
    "sg_id": "新加坡身份证",
}
```

---

## 三、规则迭代机制

### 3.1 自动更新

```python
class RuleUpdater:
    """规则自动更新"""
    
    def __init__(self):
        self.remote_url = "https://api.example.com/rules"
    
    def check_update(self):
        """检查更新"""
        remote_version = self.fetch_version()
        local_version = self.get_local_version()
        return remote_version > local_version
    
    def update_rules(self):
        """更新规则"""
        rules = self.fetch_rules()
        self.merge_rules(rules)
        self.backup_current()
        self.apply_new_rules()
```

### 3.2 自定义规则

```python
# 用户自定义规则
CUSTOM_RULES = {
    "my_api_key": {
        "pattern": r"myapp_[A-Za-z0-9]{16,}",
        "action": "block",
        "severity": "high"
    }
}
```

---

## 四、探索计划

### 4.1 第一阶段: 补全 (本周)

- [ ] 加密货币地址规则 (BTC/ETH/USDT)
- [ ] 中国政务号码规则
- [ ] 国际护照/ID 规则

### 4.2 第二阶段: 深化 (下周)

- [ ] 行业专用规则 (医疗/金融)
- [ ] 上下文感知匹配
- [ ] 规则优先级优化

### 4.3 第三阶段: 智能化 (下月)

- [ ] AI 辅助规则生成
- [ ] 规则效果分析
- [ ] 自动规则测试

---

## 五、规则来源

### 5.1 公开数据源

- OWASP: 安全模式
- NIST: 敏感数据类型
- GDPR: 个人数据定义
- 中国: 《个人信息保护法》

### 5.2 威胁情报

- 暗网泄露数据格式
- 攻击Payload模式
- 社工库字段

---

## 六、效果评估

### 6.1 指标

| 指标 | 目标 |
|------|------|
| 规则覆盖率 | >90% 常见场景 |
| 误报率 | <3% |
| 检测速度 | <5ms/条 |
| 更新频率 | 每周迭代 |

### 6.2 测试

```bash
# 规则测试
python bin/agent-dlp test-rules

# 覆盖率测试
python bin/agent-dlp coverage

# 性能测试
python bin/agent-dlp benchmark
```

---

*待完善*
