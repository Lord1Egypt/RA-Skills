# CodeTabs 速查

**用途**：同一个事情的多个代码版本（不同语言、不同框架、不同平台）。

## 语法

    <CodeTabs tabs='["Python","JavaScript","Go"]'>

    ```python
    print("hello")
    ```

    ```javascript
    console.log("hello");
    ```

    ```go
    fmt.Println("hello")
    ```

    </CodeTabs>

## Props

| 名称 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `tabs` | `string[]` (JSON 字符串) | auto | tab 标签名数组，顺序和 children 对应 |

## 注意

- `tabs` 必须是 **JSON 字符串**（单引号包裹）而不是 JSX 表达式
- children 按顺序对应到 tab，首个默认激活
- 交互：用户点击 tab 切换 panel（vanilla JS 实现）

## 何时不用

- 只有一种语言 → 普通 code block
- 代码很短（<5 行）且语言相关不大 → 并排两个 code block
