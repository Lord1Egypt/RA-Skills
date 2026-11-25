# 设计

1. 明确受益者、应用目的、范围、现状与必需结果。
   有既有系统时检查入口、状态归属、失败路径和测试。
   保留有要求的安全、时限与可靠性边界。
2. 在[决策记录](../decision-records.md)中提出概念与场景。
3. 检查全部八项[概念判据](../model-criteria.md#概念)。
   按[规格记法](../spec-notation.md)写契约及其[执行约束](../architecture-execution.md#执行约束)；需要范例时读[示例](../spec-examples.md)中的对应场景。
4. 设计规则并检查[组合与子集](../model-criteria.md#组合)。
5. 涉及工程设计时，按[工程架构](../architecture.md)（Java/Spring 项目另读 [Java/Spring 约定](../architecture-java.md)）明确入口、规则实现、概念边界与依赖检查。

交付概念契约、规则、同步图、排除与未决。
必需响应 MUST 覆盖已声明的成功与拒绝分支。
默认按[阅读版](../spec-reading.md)说明模型，按需展开精度。
