# 🛡️ 入侵检测与数据外泄防护能力分析报告

**分析时间**: 2026-04-07 22:59  
**分析范围**: DLP + 入侵检测 + 数据外传检测

---

## 📊 能力覆盖总览

| 能力 | 状态 | 模块 | 完整性 |
|------|------|------|--------|
| **数据外泄防护 (DLP)** | ✅ 有 | `dlp/check.py` | 🟡 60% |
| **入侵检测 (IDS)** | ⚠️ 部分 | `runtime/monitor.py` | 🟡 40% |
| **数据外传检测** | ✅ 有 | `scanner_v2.py` | 🟡 50% |
| **行为分析** | ⚠️ 基础 | `runtime/monitor.py` | 🟡 30% |

---

## ✅ 已有能力

### 1. 数据外泄防护 (DLP) ✅

**位置**: `dlp/check.py` (185 行)

**支持的数据类型**:

| 数据类型 | 规则 | 风险等级 | 处置方式 |
|---------|------|---------|---------|
| **中国身份证** | `[1-9]\d{5}(18|19|20)\d{2}...` | CRITICAL | BLOCK |
| **手机号** | `1[3-9]\d{9}` | HIGH | SANITIZE |
| **API 密钥** | `(api_key\|apikey)` | CRITICAL | BLOCK |
| **AWS 密钥** | `AKIA[0-9A-Z]{16}` | CRITICAL | BLOCK |
| **私钥** | `BEGIN.*PRIVATE KEY` | CRITICAL | BLOCK |
| **邮箱** | 标准邮箱格式 | MEDIUM | SANITIZE |
| **IP 地址** | IPv4 格式 | LOW | LOG |
| **银行卡** | `\d{4}-\d{4}-\d{4}-\d{4}` | CRITICAL | BLOCK |
| **密码** | `password=xxx` | HIGH | SANITIZE |

**处置动作**:
- ✅ **BLOCK**: 阻断传输
- ✅ **SANITIZE**: 脱敏处理
- ✅ **LOG**: 记录日志

**脱敏能力**:
```python
# 手机号脱敏
13812345678 → 138****5678

# 身份证脱敏
110101199001011234 → 110**********1234
```

**评价**:
- ✅ 覆盖常见敏感数据类型
- ✅ 支持多种处置方式
- ✅ 有脱敏功能
- ⚠️ 仅支持正则匹配
- ⚠️ 无法识别上下文
- ⚠️ 无法识别编码/加密数据

---

### 2. 入侵检测 (IDS) ⚠️

**位置**: `runtime/monitor.py` (132 行)

**检测能力**:

| 检测类型 | 规则 | 风险等级 |
|---------|------|---------|
| **危险 Shell 执行** | `execve\|fork\|clone` | CRITICAL |
| **批量删除** | `rm -rf\|del /f /s` | HIGH |
| **敏感路径访问** | `/etc/passwd\|~/.ssh/` | HIGH |
| **持久化配置** | `cron\|systemd\|registry` | HIGH |
| **异常外发** | `beacon\|exfil\|long-poll` | CRITICAL |

**评价**:
- ✅ 覆盖基础入侵行为
- ✅ 支持系统调用监控
- ✅ 支持文件访问监控
- ✅ 支持网络行为监控
- ⚠️ 仅支持简单模式匹配
- ⚠️ 无法检测行为序列
- ⚠️ 无法检测时间窗口异常
- ⚠️ 无法检测高级持续性威胁 (APT)

---

### 3. 数据外传检测 ✅

**位置**: `scanner_v2.py` (黑名单规则)

**检测规则**:

| 规则 | 风险等级 | 类别 |
|------|---------|------|
| `requests\.post\s*\([^)]*http` | HIGH | data_exfil |
| `urllib\.request\.urlopen\s*\(` | HIGH | data_exfil |
| `\.ssh/` | CRITICAL | credential_theft |
| `id_rsa` | CRITICAL | credential_theft |
| `curl.*\|.*(?:bash\|sh)` | CRITICAL | remote_load |
| `wget.*\|.*(?:bash\|sh)` | CRITICAL | remote_load |

**评价**:
- ✅ 覆盖常见外传方式
- ✅ 覆盖凭证窃取
- ✅ 覆盖远程加载
- ⚠️ 仅支持静态代码检测
- ⚠️ 无法检测动态外传
- ⚠️ 无法检测加密外传

---

## 🔴 能力缺口分析

### DLP 数据外泄防护缺口

| 缺口 | 当前状态 | 期望能力 | 优先级 |
|------|---------|---------|--------|
| **编码识别** | ❌ 无 | 识别 Base64/Hex/URL 编码 | 🔴 P0 |
| **加密识别** | ❌ 无 | 识别加密/混淆数据 | 🔴 P0 |
| **上下文感知** | ❌ 无 | 识别变量赋值/传递 | 🟡 P1 |
| **文件外传** | ❌ 无 | 检测文件读取 + 外发 | 🔴 P0 |
| **剪贴板监控** | ❌ 无 | 检测剪贴板访问 | 🟡 P1 |
| **截图检测** | ❌ 无 | 检测截图行为 | 🟡 P2 |
| **OCR 识别** | ❌ 无 | 识别图片中敏感数据 | 🟢 P3 |
| **流量分析** | ❌ 无 | 检测网络流量异常 | 🔴 P0 |

### 入侵检测缺口

| 缺口 | 当前状态 | 期望能力 | 优先级 |
|------|---------|---------|--------|
| **行为序列** | ❌ 无 | 检测多步攻击序列 | 🔴 P0 |
| **时间窗口** | ❌ 无 | 检测频率异常 | 🔴 P0 |
| **权限提升** | ❌ 无 | 检测提权行为 | 🔴 P0 |
| **横向移动** | ❌ 无 | 检测内网渗透 | 🟡 P1 |
| **持久化** | ⚠️ 基础 | 深度持久化检测 | 🟡 P1 |
| **隐蔽信道** | ❌ 无 | 检测 DNS/ICMP 隧道 | 🟡 P1 |
| **恶意下载** | ❌ 无 | 检测恶意文件下载 | 🟡 P1 |
| **内存注入** | ❌ 无 | 检测内存马 | 🟢 P2 |

### 数据外传检测缺口

| 缺口 | 当前状态 | 期望能力 | 优先级 |
|------|---------|---------|--------|
| **加密外传** | ❌ 无 | 检测 HTTPS 外传 | 🔴 P0 |
| **分片外传** | ❌ 无 | 检测分片数据外传 | 🟡 P1 |
| **隐蔽外传** | ❌ 无 | 检测 DNS/ICMP 外传 | 🟡 P1 |
| **云存储外传** | ❌ 无 | 检测上传到云盘 | 🟡 P1 |
| **邮件外传** | ❌ 无 | 检测邮件发送敏感数据 | 🟡 P1 |
| **即时通讯外传** | ❌ 无 | 检测微信/QQ 外传 | 🟢 P2 |

---

## 🎯 增强方案

### DLP 增强 (P0)

```python
class AdvancedDLP:
    """高级 DLP 引擎"""
    
    def __init__(self):
        self.detectors = [
            RegexDetector(),      # 正则检测 (已有)
            ContextDetector(),    # 上下文检测 (新增)
            EntropyDetector(),    # 熵值检测 (新增)
            EncodingDetector(),   # 编码识别 (新增)
            FileLeakDetector(),   # 文件外传检测 (新增)
        ]
    
    def detect(self, data: str, context: Dict) -> DLPResult:
        results = []
        
        # 1. 正则匹配
        results.extend(self.detectors[0].detect(data))
        
        # 2. 上下文分析
        if self.detectors[1].is_sensitive_context(context):
            results.append(Threat("敏感上下文"))
        
        # 3. 熵值检测 (识别加密/编码)
        entropy = self.detectors[2].calculate(data)
        if entropy > 7.5:  # 高熵值
            results.append(Threat("疑似加密数据"))
        
        # 4. 编码识别
        encodings = self.detectors[3].detect(data)
        if encodings:
            # 解码后再次检测
            decoded = self.detectors[3].decode(data)
            results.extend(self.detect(decoded, context))
        
        # 5. 文件外传检测
        if self.detectors[4].is_file_leak(context):
            results.append(Threat("文件外传"))
        
        return self.aggregate(results)
```

### 入侵检测增强 (P0)

```python
class BehavioralIDS:
    """行为入侵检测系统"""
    
    def __init__(self):
        self.event_buffer = []
        self.time_windows = defaultdict(list)
    
    def analyze(self, events: List[Event]) -> List[Threat]:
        threats = []
        
        # 1. 行为序列检测
        if self.detect_attack_sequence(events):
            threats.append(Threat("多步攻击序列"))
        
        # 2. 时间窗口检测
        if self.detect_frequency_anomaly(events):
            threats.append(Threat("频率异常"))
        
        # 3. 权限提升检测
        if self.detect_privilege_escalation(events):
            threats.append(Threat("提权攻击"))
        
        # 4. 横向移动检测
        if self.detect_lateral_movement(events):
            threats.append(Threat("横向移动"))
        
        return threats
    
    def detect_attack_sequence(self, events: List[Event]) -> bool:
        """检测攻击序列"""
        # 示例：文件读取 → 编码 → 网络外发
        sequence = [e.type for e in events[-10:]]
        attack_patterns = [
            ["file_read", "encode", "network_send"],
            ["credential_access", "compress", "exfiltrate"],
            ["exec", "network_connect", "data_transfer"],
        ]
        for pattern in attack_patterns:
            if self.contains_subsequence(sequence, pattern):
                return True
        return False
    
    def detect_frequency_anomaly(self, events: List[Event]) -> bool:
        """检测频率异常"""
        # 检测 1 分钟内超过 100 次网络请求
        recent = [e for e in events if e.timestamp > time.time() - 60]
        network_events = [e for e in recent if e.type == "network"]
        if len(network_events) > 100:
            return True
        return False
```

### 数据外传检测增强 (P0)

```python
class ExfiltrationDetector:
    """数据外传检测器"""
    
    def __init__(self):
        self.rules = [
            # 加密外传
            {"name": "HTTPS 外传", "pattern": r"https://[^\s]+", "risk": "MEDIUM"},
            # 分片外传
            {"name": "分片外传", "pattern": r"chunk|split|part_\d+", "risk": "HIGH"},
            # DNS 隧道
            {"name": "DNS 隧道", "pattern": r"dns\.query|nslookup|dig", "risk": "HIGH"},
            # 云存储
            {"name": "云盘上传", "pattern": r"dropbox|google\.drive|onedrive", "risk": "MEDIUM"},
            # 邮件
            {"name": "邮件发送", "pattern": r"smtplib|sendmail|email\.", "risk": "MEDIUM"},
        ]
    
    def detect(self, code: str, context: Dict) -> List[Threat]:
        threats = []
        
        # 检测网络外传
        if self.is_network_exfil(code):
            threats.append(Threat("网络外传"))
        
        # 检测加密外传
        if self.is_encrypted_exfil(code):
            threats.append(Threat("加密外传"))
        
        # 检测分片外传
        if self.is_chunked_exfil(code):
            threats.append(Threat("分片外传"))
        
        # 检测隐蔽信道
        if self.is_covert_channel(code):
            threats.append(Threat("隐蔽信道"))
        
        return threats
```

---

## 📊 能力对比

### 当前能力 vs 期望能力

| 能力维度 | 当前 | 期望 | 缺口 |
|---------|------|------|------|
| **DLP 数据类型** | 9 类 | 20+ 类 | -11 类 |
| **DLP 检测方式** | 正则 | 正则 + 上下文 +ML | -2 种 |
| **入侵检测方式** | 模式匹配 | 行为序列 + 异常检测 | -2 种 |
| **外传检测方式** | 静态检测 | 静态 + 动态 + 流量 | -2 种 |
| **编码识别** | ❌ | ✅ | -100% |
| **加密识别** | ❌ | ✅ | -100% |
| **行为分析** | ❌ | ✅ | -100% |
| **时间窗口** | ❌ | ✅ | -100% |

---

## 🎯 优先级建议

### P0 - 立即增强 (本周)

1. 🔴 **DLP 编码识别** - 识别 Base64/Hex/URL 编码
2. 🔴 **DLP 文件外传** - 检测文件读取 + 外发
3. 🔴 **入侵检测行为序列** - 检测多步攻击
4. 🔴 **入侵检测时间窗口** - 检测频率异常
5. 🔴 **外传检测加密** - 识别 HTTPS 外传

### P1 - 下周完成

6. 🟡 **DLP 上下文感知** - 识别变量传递
7. 🟡 **入侵检测权限提升** - 检测提权
8. 🟡 **入侵检测横向移动** - 检测内网渗透
9. 🟡 **外传检测分片** - 检测分片数据

### P2 - 本月完成

10. 🟡 **隐蔽信道检测** - DNS/ICMP 隧道
11. 🟡 **云存储外传** - 检测上传到云盘
12. 🟢 **内存注入检测** - 检测内存马

---

## 📋 总结

### ✅ 已有能力

- ✅ DLP 支持 9 类敏感数据
- ✅ DLP 支持 BLOCK/SANITIZE/LOG
- ✅ 入侵检测支持基础行为
- ✅ 外传检测支持常见方式

### 🔴 能力缺口

- 🔴 **编码/加密识别** - 无法识别 Base64/加密数据
- 🔴 **行为序列分析** - 无法检测多步攻击
- 🔴 **时间窗口检测** - 无法检测频率异常
- 🔴 **文件外传检测** - 无法检测文件读取 + 外发
- 🔴 **上下文感知** - 无法识别变量传递

### 🎯 建议

**当前设计包含入侵检测和数据外泄防护，但能力较为基础，建议立即增强 P0 级别能力。**

---

**分析完成时间**: 2026-04-07 22:59  
**分析者**: 安全能力评估系统  
**状态**: 🔄 待增强
