# 图解

1. 查明规格、入口、状态、动作、调用方、查询、测试与失败路径。
2. 按[视图与证据](../references/spec-reading.md#视图与证据)选择当前问题需要的内容。
3. 交付 Markdown，说明行为，必要时配图，并附当前文件、符号与行号。
4. 对照源码与[规格记法](../references/spec-notation.md)检查；无实现时仅解释设计。

概念与同步关系图用 [map 流程](../references/diagram-contract.md#使用)生成。
MUST NOT 手工补齐生成器未解析的关系。
教学顺序 MUST NOT 被写成执行顺序、事务或运行正确性的证据。
