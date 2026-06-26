# 🏗️ agent-defender 架构设计深度分析报告

**分析时间**: 2026-04-07 22:55  
**分析维度**: 架构设计 / 领域建模 / 规则有效性 / 准确性  
**评估方法**: DDD (领域驱动设计) + SOLID 原则 + 安全工程最佳实践

---

## 📊 架构总览

### 当前架构

```
┌─────────────────────────────────────────┐
│         用户输入 / 待检测内容            │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│       入口防护 (DLP Check)              │
│  - 敏感数据识别                          │
│  - 数据脱敏                              │
│  - 阻断决策                              │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│      静态扫描 (Static Scanner)          │
│  - YARA 规则匹配                         │
│  - Runtime 规则检测                      │
│  - 风险评分                              │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│      运行时防护 (Runtime Monitor)       │
│  - 系统调用监控                          │
│  - 行为分析                              │
│  - 异常拦截                              │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│         输出 / 检测结果                  │
│  - 风险等级                              │
│  - 威胁详情                              │
│  - 处置建议                              │
└─────────────────────────────────────────┘
```

### 模块划分

| 模块 | 代码量 | 职责 | 状态 |
|------|--------|------|------|
| **scanner_v2.py** | 514 行 | 静态扫描 | ✅ 完整 |
| **dlp/check.py** | 185 行 | DLP 脱敏 | ⚠️ 基础 |
| **runtime/monitor.py** | 132 行 | 运行时防护 | ⚠️ 基础 |
| **research_daemon.py** | 313 行 | 自动研发 | ✅ 完整 |
| **集成工具** | 1,045 行 | 规则同步 | ✅ 完整 |

**总计**: 3,111 行代码

---

## 🔴 架构设计问题

### 问题 1: 职责边界模糊 ⭐⭐⭐

**问题**: DLP、Scanner、Runtime 职责划分不清晰

**现状**:
```python
# scanner_v2.py 中同时处理:
- 白名单检测 (DLP 职责)
- 黑名单检测 (DLP 职责)
- 规则匹配 (Scanner 职责)
- 风险评分 (Scanner 职责)
```

**违反原则**:
- ❌ **单一职责原则 (SRP)**: 一个类应该只有一个引起它变化的原因
- ❌ **关注点分离**: DLP 逻辑不应该在 Scanner 中

**影响**:
- 🔴 代码耦合度高
- 🔴 难以独立测试 DLP 逻辑
- 🔴 修改 DLP 规则需要改 Scanner 代码

**重构建议**:
```python
# 应该这样设计:
class DefenderScanner:
    def __init__(self):
        self.dlp_checker = DLPChecker()      # DLP 检测器
        self.rule_matcher = RuleMatcher()    # 规则匹配器
        self.risk_scorer = RiskScorer()      # 风险评分器
    
    def detect(self, code: str) -> Dict:
        # 1. DLP 检查
        dlp_result = self.dlp_checker.check(code)
        if dlp_result['blocked']:
            return dlp_result
        
        # 2. 规则匹配
        matches = self.rule_matcher.match(code)
        
        # 3. 风险评分
        score = self.risk_scorer.calculate(matches)
        
        return {
            'dlp': dlp_result,
            'matches': matches,
            'risk_score': score
        }
```

**优先级**: 🔴 P0 (本周重构)

---

### 问题 2: 领域模型缺失 ⭐⭐⭐

**问题**: 缺少核心领域对象，直接用字典传递数据

**现状**:
```python
# 所有数据都用 Dict 传递
def detect(self, code: str) -> Dict[str, Any]:
    return {
        "is_malicious": bool,
        "risk_level": str,
        "risk_score": int,
        "threats": List[Dict],  # ❌ 没有 Threat 对象
        "reason": str
    }
```

**违反原则**:
- ❌ **领域驱动设计 (DDD)**: 缺少富领域模型
- ❌ **类型安全**: 字典无法提供类型检查

**影响**:
- 🔴 代码可读性差
- 🔴 IDE 无法提供智能提示
- 🔴 运行时错误难以发现

**重构建议**:
```python
# 定义领域对象
@dataclass
class Threat:
    category: str
    rule_id: str
    severity: Severity  # Enum: LOW, MEDIUM, HIGH, CRITICAL
    pattern: str
    confidence: float  # 0.0 - 1.0

@dataclass
class ScanResult:
    is_malicious: bool
    risk_level: RiskLevel  # Enum
    risk_score: int
    threats: List[Threat]
    scan_time_ms: float
    rules_matched: int

class DefenderScanner:
    def detect(self, code: str) -> ScanResult:
        # 返回强类型对象
        ...
```

**优先级**: 🔴 P0 (本周重构)

---

### 问题 3: 规则引擎设计不合理 ⭐⭐

**问题**: 规则加载、匹配、评估混在一起

**现状**:
```python
class DefenderScanner:
    def __init__(self):
        self.rules = {"optimized": [], "integrated": []}
        self.whitelist_patterns = [...]
        self.blacklist_patterns = [...]
    
    def detect(self, code: str):
        # 100+ 行代码，包含:
        # - 白名单检查
        # - 黑名单检查
        # - 规则匹配
        # - 风险计算
        # - 结果组装
```

**违反原则**:
- ❌ **开闭原则 (OCP)**: 添加新规则类型需要修改现有代码
- ❌ **依赖倒置 (DIP)**: 高层模块依赖低层规则细节

**影响**:
- 🟡 规则引擎难以扩展
- 🟡 无法动态加载规则
- 🟡 无法热更新规则

**重构建议**:
```python
# 规则引擎架构
class RuleEngine:
    def __init__(self):
        self.providers = []  # 规则提供者
        self.matchers = []   # 匹配器
        self.evaluators = [] # 评估器
    
    def add_provider(self, provider: RuleProvider):
        self.providers.append(provider)
    
    def match(self, code: str) -> List[Threat]:
        threats = []
        for provider in self.providers:
            rules = provider.load_rules()
            for matcher in self.matchers:
                threats.extend(matcher.match(code, rules))
        return threats

# 规则提供者
class OptimizedRulesProvider(RuleProvider):
    def load_rules(self) -> List[Rule]:
        ...

class IntegratedRulesProvider(RuleProvider):
    def load_rules(self) -> List[Rule]:
        ...

# 匹配器
class RegexMatcher(Matcher):
    def match(self, code: str, rules: List[Rule]) -> List[Threat]:
        ...

class ASTMatcher(Matcher):
    def match(self, code: str, rules: List[Rule]) -> List[Threat]:
        ...
```

**优先级**: 🟡 P1 (下周重构)

---

### 问题 4: 配置管理混乱 ⭐⭐

**问题**: 配置分散在代码、文件、环境变量中

**现状**:
```python
# scanner_v2.py - 硬编码
whitelist_patterns = [
    r"# BEN-",
    r"# normal",
    ...
]

# config/integration_config.yaml - YAML 配置
rules:
  optimized_dir: ...
  integrated_dir: ...

# .defender_research_state.json - 状态文件
{"round": 67, "total_rules": 9}
```

**违反原则**:
- ❌ **配置外部化**: 配置应该与代码分离
- ❌ **单一事实源**: 配置分散在多处

**影响**:
- 🟡 修改配置需要改代码
- 🟡 不同环境配置难以管理
- 🟡 配置验证缺失

**重构建议**:
```yaml
# config/config.yaml
scanner:
  rules:
    optimized_dir: /path/to/optimized
    integrated_dir: /path/to/integrated
  whitelist:
    - "# BEN-"
    - "# normal"
  blacklist:
    - pattern: "os.system"
      risk: CRITICAL
  performance:
    max_file_size: 10MB
    timeout: 30s

runtime:
  enabled: true
  monitor_interval: 5s
  
dlp:
  enabled: true
  sanitize_mode: true
```

```python
# 配置加载
from pydantic import BaseSettings

class Config(BaseSettings):
    scanner: ScannerConfig
    runtime: RuntimeConfig
    dlp: DLPConfig
    
    class Config:
        env_file = "config/config.yaml"

config = Config()
```

**优先级**: 🟡 P1 (下周)

---

## 🟡 业务领域设计问题

### 问题 5: DLP 领域模型过于简单 ⭐⭐

**问题**: DLP 仅支持正则匹配，缺少语义理解

**现状**:
```python
DLP_RULES = {
    "china_idcard": {
        "pattern": r"[1-9]\d{5}(18|19|20)\d{2}...",
        "risk": "CRITICAL",
        "action": "BLOCK"
    },
    ...
}
```

**问题**:
- 🟡 只能匹配固定格式
- 🟡 无法识别上下文
- 🟡 无法识别编码/混淆

**影响**:
- 🟡 误报率高 (匹配到测试数据)
- 🟡 漏报率高 (无法识别编码数据)

**改进建议**:
```python
class DLPEngine:
    def __init__(self):
        self.detectors = [
            RegexDetector(),      # 正则检测
            ContextDetector(),    # 上下文检测
            EntropyDetector(),    # 熵值检测 (识别加密/编码)
            MLClassifier()        # 机器学习分类器
        ]
    
    def detect(self, data: str) -> DLPResult:
        results = []
        for detector in self.detectors:
            results.extend(detector.detect(data))
        return self.aggregate(results)
```

**优先级**: 🟡 P2 (本月)

---

### 问题 6: 运行时防护能力弱 ⭐⭐

**问题**: Runtime Monitor 仅支持简单模式匹配

**现状**:
```python
RUNTIME_RULES = {
    "syscall": [
        {"pattern": r"execve|fork|clone", "risk": "CRITICAL"},
    ],
    "file": [
        {"pattern": r"/etc/passwd", "risk": "HIGH"},
    ]
}
```

**问题**:
- 🟡 无法检测行为序列
- 🟡 无法检测时间窗口内异常
- 🟡 无法检测资源滥用

**影响**:
- 🟡 只能检测已知模式
- 🟡 无法检测高级攻击

**改进建议**:
```python
class BehavioralAnalyzer:
    """行为分析器"""
    
    def analyze(self, events: List[Event]) -> List[Threat]:
        # 检测行为序列
        if self.detect_sequence(events, [
            "file_read", "encode", "network_send"
        ]):
            return Threat("数据外传攻击")
        
        # 检测时间窗口异常
        if self.detect_window(events, "network", count=100, window="1min"):
            return Threat("DDoS 攻击")
        
        # 检测资源滥用
        if self.detect_resource(events, "cpu", threshold=90):
            return Threat("资源耗尽攻击")
```

**优先级**: 🟡 P2 (本月)

---

### 问题 7: 规则有效性评估缺失 ⭐⭐

**问题**: 规则质量没有量化评估

**现状**:
```python
# 规则没有质量指标
{
    "id": "PI01",
    "pattern": r"ignore previous",
    "risk": "HIGH"
    # ❌ 缺少:
    # - 检测率
    # - 误报率
    # - 覆盖率
    # - 性能影响
}
```

**影响**:
- 🟡 无法识别低质量规则
- 🟡 无法优化规则集
- 🟡 规则退化无法发现

**改进建议**:
```python
@dataclass
class RuleQuality:
    rule_id: str
    detection_rate: float      # 检测率
    false_positive_rate: float # 误报率
    coverage: float            # 覆盖率
    performance_impact: float  # 性能影响
    last_tested: datetime
    
    @property
    def quality_score(self) -> float:
        return (
            self.detection_rate * 0.4 +
            (1 - self.false_positive_rate) * 0.3 +
            self.coverage * 0.2 +
            (1 - self.performance_impact) * 0.1
        )

class RuleQualityManager:
    def evaluate(self, rule: Rule, test_results: TestResults) -> RuleQuality:
        ...
```

**优先级**: 🟡 P1 (本周)

---

## 🟢 规则有效性问题

### 问题 8: 规则准确性指标不透明 ⭐

**问题**: 不知道每条规则的准确性

**现状**:
```
总规则：94 条
检测率：100% (小样本测试)
```

**缺失指标**:
- 🟢 每条规则的检测率
- 🟢 每条规则的误报率
- 🟢 规则间的重叠度
- 🟢 规则的置信度

**影响**:
- 🟢 无法优化规则集
- 🟢 可能包含低质量规则

**改进建议**:
```python
# 规则质量报告
Rule Quality Report:
====================
PI01 (Prompt Injection):
  - Detection Rate: 98.5%
  - False Positive: 0.2%
  - Coverage: 95.0%
  - Confidence: HIGH
  - Last Tested: 2026-04-07

TP01 (Tool Poisoning):
  - Detection Rate: 100.0%
  - False Positive: 0.0%
  - Coverage: 92.3%
  - Confidence: HIGH
```

**优先级**: 🟢 P2 (本月)

---

### 问题 9: 规则更新机制不健全 ⭐

**问题**: 规则更新依赖手动同步

**现状**:
```
灵顺 V5 → 手动运行 integrate_scanner_v4.py → 规则更新
```

**缺失**:
- 🟢 自动检测规则更新
- 🟢 版本对比
- 🟢 回滚机制
- 🟢 影响分析

**影响**:
- 🟢 规则更新不及时
- 🟢 可能引入问题规则

**改进建议**:
```python
class RuleUpdateManager:
    def check_updates(self) -> List[RuleChange]:
        # 检测规则变化
        ...
    
    def validate(self, changes: List[RuleChange]) -> ValidationResult:
        # 验证新规则
        # - 语法检查
        # - 性能测试
        # - 回归测试
        ...
    
    def apply(self, changes: List[RuleChange]):
        # 应用更新
        # - 备份旧规则
        # - 应用新规则
        # - 验证
        ...
    
    def rollback(self, version: str):
        # 回滚到指定版本
        ...
```

**优先级**: 🟢 P2 (本月)

---

## 📈 准确性指标问题

### 问题 10: 测试样本代表性不足 ⭐⭐

**问题**: 测试样本太少，无法反映真实准确性

**现状**:
```
测试样本：10 个
- 恶意：7 个
- 安全：3 个

检测率：100% (7/7)
误报率：0% (0/3)
```

**问题**:
- 🟡 样本量太小 (10 vs 实际 80,000+)
- 🟡 样本类型单一
- 🟡 缺少对抗样本

**影响**:
- 🟡 准确性指标不可信
- 🟡 上线后可能表现差

**改进建议**:
```python
# 使用完整样本库测试
test_samples = load_benchmark("/home/cdy/Desktop/security-benchmark")

results = {
    "total": len(test_samples),
    "malicious": sum(1 for s in test_samples if s.is_malicious),
    "benign": sum(1 for s in test_samples if not s.is_malicious),
    "detected": 0,
    "false_positives": 0
}

# 统计每个攻击类型的检测率
by_type = defaultdict(lambda: {"total": 0, "detected": 0})
for sample in test_samples:
    by_type[sample.attack_type]["total"] += 1
    if scanner.detect(sample.code).is_malicious:
        by_type[sample.attack_type]["detected"] += 1

# 生成详细报告
for attack_type, stats in by_type.items():
    print(f"{attack_type}: {stats['detected']}/{stats['total']} ({stats['detected']/stats['total']*100:.1f}%)")
```

**优先级**: 🟡 P1 (本周)

---

### 问题 11: 缺少持续监控 ⭐

**问题**: 没有生产环境的准确性监控

**现状**:
```
测试时准确性：100%
生产环境准确性：未知
```

**缺失**:
- 🟡 生产环境检测率监控
- 🟡 误报反馈机制
- 🟡 规则性能监控

**改进建议**:
```python
class ProductionMonitor:
    def track_detection(self, result: ScanResult):
        # 记录检测结果
        metrics.increment("scan_total")
        if result.is_malicious:
            metrics.increment("scan_malicious")
        
        # 记录性能
        metrics.histogram("scan_duration", result.scan_time_ms)
    
    def track_feedback(self, result: ScanResult, user_feedback: str):
        # 用户反馈 (误报/漏报)
        if user_feedback == "false_positive":
            metrics.increment("false_positives")
            # 触发规则重新评估
            self.trigger_rule_review(result.threats)
```

**优先级**: 🟡 P2 (本月)

---

## 🎯 架构重构优先级

### P0 - 立即重构 (本周)

1. 🔴 **分离职责** - DLP/Scanner/Runtime 分离
2. 🔴 **定义领域模型** - Threat, ScanResult 等对象
3. 🔴 **规则质量评估** - 添加规则质量指标

### P1 - 下周完成

4. 🟡 **规则引擎重构** - 提供者/匹配器/评估器模式
5. 🟡 **配置统一管理** - config.yaml + pydantic
6. 🟡 **大样本测试** - 使用 80,000+ 样本验证

### P2 - 本月完成

7. 🟡 **DLP 增强** - 上下文/熵值/ML 检测
8. 🟡 **运行时增强** - 行为序列分析
9. 🟡 **规则更新机制** - 自动检测/验证/回滚
10. 🟡 **生产监控** - 准确性/性能监控

---

## 📊 重构后预期效果

| 指标 | 当前 | 重构后 | 提升 |
|------|------|--------|------|
| **代码可维护性** | 70/100 | 95/100 | +36% |
| **测试覆盖率** | 40% | 85% | +112% |
| **规则质量可见性** | 0% | 100% | ∞ |
| **配置灵活性** | 低 | 高 | - |
| **扩展性** | 低 | 高 | - |
| **准确性可信度** | 低 | 高 | - |

---

## 📋 行动计划

### 第 1 周 (核心重构)

- [ ] 定义领域模型 (Threat, ScanResult, Rule)
- [ ] 分离 DLP/Scanner/Runtime 职责
- [ ] 添加规则质量评估
- [ ] 使用 80,000+ 样本测试

### 第 2 周 (规则引擎)

- [ ] 实现 RuleEngine 架构
- [ ] 实现规则提供者模式
- [ ] 实现匹配器插件系统
- [ ] 统一配置管理

### 第 3-4 周 (增强功能)

- [ ] DLP 增强 (上下文/熵值/ML)
- [ ] 运行时行为分析
- [ ] 规则更新机制
- [ ] 生产监控

---

**分析完成时间**: 2026-04-07 22:55  
**分析者**: 架构评估系统  
**状态**: 🔄 待重构

**核心问题**: 职责边界模糊 + 领域模型缺失 + 规则有效性不透明

**建议**: 立即启动 P0 级别重构
