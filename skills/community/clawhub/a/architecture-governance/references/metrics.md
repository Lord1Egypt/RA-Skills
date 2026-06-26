# 指标定义与采集方案

## 指标总览

| 维度 | 指标 | 采集方式 | 自动化程度 | 采集频率 |
|------|------|----------|-----------|---------|
| 结构质量 | 圈复杂度 | 静态分析 | ✅ 自动 | 每日 |
| 结构质量 | 代码重复率 | 代码扫描 | ✅ 自动 | 每日 |
| 结构质量 | 单类行数 | 静态分析 | ✅ 自动 | 每日 |
| 结构质量 | 单方法行数 | 静态分析 | ✅ 自动 | 每日 |
| 结构质量 | 测试覆盖率 | CI 流水线 | ✅ 自动 | 每次提交 |
| 依赖关系 | 下游依赖数 | 架构图谱 | ✅ 自动 | 每周 |
| 依赖关系 | 上游依赖数 | 架构图谱 | ✅ 自动 | 每周 |
| 依赖关系 | 循环依赖 | 静态分析 | ✅ 自动 | 每日 |
| 依赖关系 | 跨层调用 | 架构检查 | ✅ 自动 | 每日 |
| 依赖关系 | 核心链路耦合 | 链路分析 | ⚠️ 半自动 | 每月 |
| 技术规范 | 代码规范违规 | Lint 检查 | ✅ 自动 | 每次提交 |
| 技术规范 | 安全漏洞 | 安全扫描 | ✅ 自动 | 每日 |
| 技术规范 | 文档完整度 | 文档检查 | ⚠️ 半自动 | 每月 |
| 技术规范 | API 规范符合度 | API 网关 | ✅ 自动 | 每周 |
| 技术规范 | 日志规范符合度 | 日志分析 | ⚠️ 半自动 | 每月 |
| 可演进性 | 部署频率 | 发布系统 | ✅ 自动 | 每周 |
| 可演进性 | 变更失败率 | 发布系统 | ✅ 自动 | 每周 |
| 可演进性 | 配置外部化 | 代码检查 | ✅ 自动 | 每月 |
| 可演进性 | 特性开关 | 代码检查 | ⚠️ 半自动 | 每月 |
| 可演进性 | 灰度能力 | 架构评审 | ⚠️ 手动 | 每季度 |
| 风险暴露 | 单点故障 | 架构评审 | ⚠️ 手动 | 每季度 |
| 风险暴露 | 核心人员依赖 | 团队评估 | ⚠️ 手动 | 每季度 |
| 风险暴露 | 技术栈过时 | 技术雷达 | ⚠️ 半自动 | 每季度 |
| 风险暴露 | 已知技术债务 | 债务系统 | ✅ 自动 | 每周 |
| 风险暴露 | 故障历史 | 故障系统 | ✅ 自动 | 每周 |
| 治理合规 | 架构评审通过率 | 评审记录 | ⚠️ 半自动 | 每月 |
| 治理合规 | 技术选型合规 | 技术雷达 | ⚠️ 半自动 | 每季度 |
| 治理合规 | 治理任务完成率 | 任务系统 | ✅ 自动 | 每周 |
| 治理合规 | 架构文档更新 | 文档系统 | ⚠️ 半自动 | 每月 |

---

## 自动化采集方案

### 1. 代码质量指标

#### SonarQube 集成

```yaml
# sonar-project.properties
sonar.projectKey=my-service
sonar.sources=src
sonar.tests=test
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.sourceEncoding=UTF-8
```

**采集指标**:
- 圈复杂度
- 代码重复率
- 单类/方法行数
- 代码规范违规
- 测试覆盖率

**API 示例**:
```bash
curl -u token: "http://sonarqube/api/measures/component?component=my-service&metricKeys=complexity,duplicated_lines_density,ncloc,function_complexity,coverage"
```

### 2. 依赖关系指标

#### 架构图谱采集脚本

```python
# scripts/dependency-scanner.py
import requests
from graphlib import Graph

def scan_dependencies(service_name):
    # 从服务注册中心获取依赖
    registry = requests.get(f"http://consul/v1/catalog/service/{service_name}")
    
    # 从调用链获取依赖
    traces = requests.get(f"http://jaeger/api/services/{service_name}/dependencies")
    
    # 构建依赖图
    graph = Graph()
    # ... 处理依赖关系
    
    return {
        'downstream': len(graph.downstream(service_name)),
        'upstream': len(graph.upstream(service_name)),
        'circular': graph.find_cycles()
    }
```

### 3. 发布指标

#### Jenkins/GitLab CI 集成

```python
# scripts/deployment-metrics.py
import requests

def get_deployment_metrics(service_name, days=30):
    # 获取部署记录
    deployments = requests.get(
        f"http://jenkins/job/{service_name}/api/json"
    ).json()['builds']
    
    # 计算指标
    total = len(deployments)
    failed = sum(1 for d in deployments if d['result'] == 'FAILURE')
    
    return {
        'deployment_frequency': total / days,
        'change_failure_rate': failed / total if total > 0 else 0
    }
```

### 4. 安全指标

#### Snyk 集成

```bash
# 扫描依赖漏洞
snyk test --json > snyk-report.json

# 解析结果
jq '.vulnerabilities | length' snyk-report.json
```

### 5. 故障指标

#### 故障系统 API

```python
# scripts/incident-metrics.py
import requests

def get_incident_count(service_name, days=90):
    incidents = requests.get(
        f"http://incident-system/api/incidents",
        params={
            'service': service_name,
            'since': f"{days}d"
        }
    ).json()
    
    return len(incidents)
```

---

## 手动评估检查单

### 核心链路耦合评估

```markdown
## 核心链路耦合评估

**系统**: _______________
**评估人**: _______________
**日期**: _______________

### 评估项

- [ ] 核心链路是否清晰可识别？
- [ ] 链路上服务间是否强耦合？
- [ ] 是否存在同步阻塞调用？
- [ ] 是否有熔断降级机制？
- [ ] 故障是否会级联传播？

### 评分

- 🟢 无强耦合：链路清晰，异步化，有熔断
- 🟡 弱耦合：部分同步，基本有保护
- 🔴 强耦合：同步阻塞，无保护，易级联

### 改进建议

_______________________________________________
```

### 单点故障评估

```markdown
## 单点故障评估

**系统**: _______________
**评估人**: _______________
**日期**: _______________

### 组件清单

| 组件 | 是否集群 | 故障切换 | 风险等级 |
|------|---------|---------|---------|
| 数据库 | [ ] 是 [ ] 否 | [ ] 自动 [ ] 手动 | 🟢🟡🔴 |
| 缓存 | [ ] 是 [ ] 否 | [ ] 自动 [ ] 手动 | 🟢🟡🔴 |
| 消息队列 | [ ] 是 [ ] 否 | [ ] 自动 [ ] 手动 | 🟢🟡🔴 |
| 网关 | [ ] 是 [ ] 否 | [ ] 自动 [ ] 手动 | 🟢🟡🔴 |

### 单点故障数量: ___

### 改进计划

_______________________________________________
```

### 核心人员依赖评估

```markdown
## 核心人员依赖评估

**系统**: _______________
**评估人**: _______________
**日期**: _______________

### 关键领域

| 领域 | 负责人 | 备份人员 | 文档完整 | 风险等级 |
|------|--------|---------|---------|---------|
| 核心逻辑 | | [ ] 有 [ ] 无 | [ ] 是 [ ] 否 | 🟢🟡🔴 |
| 运维部署 | | [ ] 有 [ ] 无 | [ ] 是 [ ] 否 | 🟢🟡🔴 |
| 故障处理 | | [ ] 有 [ ] 无 | [ ] 是 [ ] 否 | 🟢🟡🔴 |
| 业务逻辑 | | [ ] 有 [ ] 无 | [ ] 是 [ ] 否 | 🟢🟡🔴 |

### 核心人员依赖数量: ___

### 改进计划

_______________________________________________
```

---

## 阈值配置模板

```yaml
# config/thresholds.yaml
structure_quality:
  cyclomatic_complexity:
    healthy: 15
    warning: 30
    dangerous: 999
  code_duplication:
    healthy: 5
    warning: 10
    dangerous: 999
  lines_per_class:
    healthy: 500
    warning: 1000
    dangerous: 999
  lines_per_method:
    healthy: 50
    warning: 100
    dangerous: 999
  test_coverage:
    healthy: 80
    warning: 60
    dangerous: 0

dependency:
  downstream_count:
    healthy: 5
    warning: 10
    dangerous: 999
  upstream_count:
    healthy: 10
    warning: 20
    dangerous: 999
  circular_dependency:
    healthy: 0
    warning: 0
    dangerous: 1
  cross_layer_call:
    healthy: 0
    warning: 0
    dangerous: 1

# ... 其他维度
```

---

## 数据采集频率建议

| 指标类型 | 建议频率 | 原因 |
|----------|---------|------|
| 代码质量 | 每日 | 随代码变更快速变化 |
| 依赖关系 | 每周 | 相对稳定 |
| 技术规范 | 每次提交 + 每日扫描 | 实时 + 定期 |
| 可演进性 | 每周 | 与发布节奏相关 |
| 风险暴露 | 每月/每季度 | 变化较慢 |
| 治理合规 | 每月 | 管理指标 |

---

## 数据质量保障

1. **数据校验**: 采集后校验数据完整性和合理性
2. **异常处理**: 采集失败时记录日志并告警
3. **数据追溯**: 保留历史数据用于趋势分析
4. **定期校准**: 每季度校准阈值和权重
