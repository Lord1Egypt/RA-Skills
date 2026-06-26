# Collapse 速查

**用途**：折叠次要但不想删的内容（FAQ、长附录、详细推导、完整错误栈）。

## 语法

    <Collapse title="详细解释" defaultOpen={false}>
    折叠的正文内容
    </Collapse>

## Props

| 名称 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `title` | `string` | — | 折叠头标题（必填） |
| `defaultOpen` | `boolean` | `false` | 初始是否展开 |

## 硬规则

- **只用来藏次要信息**，不要藏主要论点
- 一个段落里 Collapse 数量不要超过 5 个
- 正文流程中不要强行插入 Collapse 打断阅读节奏

## 示例：FAQ

    <Collapse title="Q: 为什么要用这个方案？">
    因为方案 A 的 xx 问题...
    </Collapse>

    <Collapse title="Q: 性能如何？">
    QPS 测试结果：...
    </Collapse>
