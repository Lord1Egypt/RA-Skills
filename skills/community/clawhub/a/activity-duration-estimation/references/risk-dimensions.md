# 风险维度库（Risk Dimension Library）

> 内置7大类风险维度，根据项目特征自动匹配适用维度。
> 每个维度包含：选择条件、分析要素、典型缓解措施。

---

## 使用方法

`_build_analysis_section()` 根据项目上下文自动筛选维度：

```python
from risk_dimensions import select_dimensions
dims = select_dimensions(project_context={
    "domain": "ai-enterprise",  # 项目领域
    "scale": "large",           # 规模
    "tech_novelty": "high",     # 技术新颖度
    "team_size": 30,            # 团队规模
    "integration_count": 5,     # 集成系统数
    "critical_path_len": 16,    # 关键路径任务数
    "mc_p50_p90_gap": 21,       # P50-P90跨度(天)
    "phases": [...],            # 阶段列表
})
```

---

## 维度清单

### D1. 技术风险（Technical Risk）

| 选择条件 | 启用 |
|---------|------|
| 项目涉及AI/ML/大模型 | ✅ 总是 |
| 包含未经验证的技术栈 | ✅ |
| 含多系统集成 | ✅ |
| 纯传统软件开发 | ❌ |

**分析要素**：
- 技术选型风险：LLM模型选择（开源vs闭源）、框架版本锁定、API兼容性
- 技术实现复杂度：RAG准确性、Agent幻觉率、多智能体协调
- 集成风险：企业系统API兼容性、数据格式转换、认证集成
- 性能与扩展性：响应延迟、并发容量、资源消耗
- 安全与合规：数据隐私、模型安全审计、权限越界

**典型缓解**：
- 技术选型阶段配置PoC验证周期
- 关键路径的AI模块配置20%缓冲
- 集成测试前置到开发中期

---

### D2. 供应商/外部依赖风险（Vendor Risk）

| 选择条件 | 启用 |
|---------|------|
| 依赖第三方LLM API | ✅ |
| 使用开源框架/组件 | ✅ |
| 需要SaaS服务订阅 | ✅ |
| 全部自研无外部依赖 | ❌ |

**分析要素**：
- API依赖风险：LLM供应商定价变化、服务中断、模型版本淘汰
- 开源组件风险：许可更新、社区活跃度下降、安全漏洞
- 供应商锁定：难以迁移的自定义接口、专属格式
- 生态风险：框架更新导致的向下不兼容

**典型缓解**：
- 核心功能与API调用层解耦（抽象接口+适配器模式）
- 关键组件准备备选方案（多模型策略）
- 定期评估依赖健康状况

---

### D3. 相关方风险（Stakeholder Risk）

| 选择条件 | 启用 |
|---------|------|
| 跨部门协作项目 | ✅ |
| 涉及组织变革 | ✅ |
| 面向管理层的Dashboard | ✅ |
| 纯技术内部项目 | ❌ |

**分析要素**：
- 用户接受度：AI辅助决策的信任创建、工作流更新适应
- 管理层支持：预算持续保障、组织优先级变化
- 跨部门协作：数据共享壁垒、流程所有权模糊
- 更新管理：从人工到自动化的过渡阻力

**典型缓解**：
- 分层沟通策略（C-level关注ROI，用户关注使用体验）
- 渐进式上线（先辅助模式，后自动模式）
- 关键用户早期介入（UAT提前到开发中期）

---

### D4. 进度风险（Schedule Risk）

| 选择条件 | 启用 |
|---------|------|
| 所有项目 | ✅ 总是 |
| 存在并行任务链 | ✅ |
| 依赖第三方交付 | ✅ |

**分析要素**：
- 关键路径集中度：过多任务在单一路径
- 并行执行依赖：多分支汇合点的阻塞风险
- 估算偏差：P50-P90跨度反映的不确定性
- 资源冲突：关键人才在多任务间争用

**典型缓解**：
- 关键路径任务配置明确Owner
- P90-P50跨度>30%时设明确缓冲期
- 关键资源备选方案

---

### D5. 商务风险（Commercial Risk）

| 选择条件 | 启用 |
|---------|------|
| 对外交付/商业化项目 | ✅ |
| 有明确ROI要求 | ✅ |
| SaaS/订阅模式 | ✅ |
| 内部信息化项目 | ❌ |

**分析要素**：
- ROI不确定性：AI效率提升的可衡量性
- 市场时机：落地速度与竞品窗口
- 预算超支：技术探索成本不可预测
- 商业可持续性：API定价变动影响成本结构

**典型缓解**：
- 分阶段交付尽早验证价值
- 配置明确的ROI衡量指标（工时节省、错误率降低）
- 总预算保留15%-20%应急储备

---

### D6. 资源风险（Resource Risk）

| 选择条件 | 启用 |
|---------|------|
| AI/ML/大模型项目 | ✅ |
| 团队规模>15人 | ✅ |
| 涉及稀缺技能（AI/大模型） | ✅ |

**分析要素**：
- 人才获取：AI工程师、提示工程师的市场供给
- 技能匹配：现有团队与新技术栈的差距
- 团队稳定性：关键人员流失风险
- 培训成本：大模型/Skill开发的学习曲线

**典型缓解**：
- 核心模块安排两人交叉了解（Bus Factor>1）
- 提前规划培训周期（新的技能体系需要2-4周上手）
- 保留外部顾问/合作伙伴管道

---

### D7. 路径实现风险（Implementation Path Risk）

| 选择条件 | 启用 |
|---------|------|
| 包含多个子系统 | ✅ |
| 预计多次迭代 | ✅ |
| 存在技术债务积累风险 | ✅ |

**分析要素**：
- 架构演进风险：微服务拆分粒度的反复调整
- 技术债务：快速原型阶段遗留的临时方案
- 回溯兼容：早期设计决策对后期的约束
- 集成爆炸：N个系统对接的O(N²)测试复杂度

**典型缓解**：
- 架构决策记录（ADR）追踪每次关键选择
- 技术债定期偿还周期（每3-4个迭代预留1个）
- 集成测试自动化覆盖率目标（>80%）

---

## 选择算法

```python
def select_dimensions(context: dict) -> list[str]:
    """根据项目上下文选择匹配的风险维度"""
    active = []
    domain = context.get("domain", "")
    scale = context.get("scale", "medium")
    tech_novelty = context.get("tech_novelty", "medium")
    
    # D1 技术风险：涉及AI/创新技术
    if tech_novelty in ("high", "medium") or "ai" in domain.lower():
        active.append("D1")
    
    # D2 供应商风险：有外部依赖
    if domain in ("ai-enterprise", "saas", "platform"):
        active.append("D2")
    
    # D3 相关方风险：跨部门
    if scale in ("large", "enterprise") or context.get("integration_count", 0) > 3:
        active.append("D3")
    
    # D4 进度风险：总是
    active.append("D4")
    
    # D5 商务风险：商业化项目
    if context.get("is_commercial", False) or "roi" in str(context.get("phases", "")).lower():
        active.append("D5")
    
    # D6 资源风险：AI人才
    if "ai" in domain.lower() or tech_novelty == "high":
        active.append("D6")
    
    # D7 路径实现风险：多子系统
    if context.get("integration_count", 0) > 2 or context.get("critical_path_len", 0) > 10:
        active.append("D7")
    
    return active
```
