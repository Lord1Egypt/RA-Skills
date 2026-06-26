# Playground 速查

**用途**：可运行的代码演示 + 预期输出展示。

## 语法

    <Playground
      title="快速排序"
      language="python"
      code={`def sort(arr):
          if len(arr) <= 1: return arr
          return sort([x for x in arr[1:] if x < arr[0]]) + [arr[0]] + sort([x for x in arr[1:] if x >= arr[0]])
      print(sort([3,1,4,1,5,9,2,6]))`}
      output="[1, 1, 2, 3, 4, 5, 6, 9]"
    />

## Props

| 名称 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `code` | `string` | — | 代码正文（必填） |
| `language` | `string` | `"javascript"` | 语言标记（仅展示用） |
| `title` | `string` | `"${language} playground"` | 标题栏文字 |
| `output` | `string` | — | 可选的输出结果，有则显示"运行"按钮 |

## 交互

- 复制按钮：拷贝 `code` 到剪贴板
- 运行按钮（仅有 output 时显示）：切换输出区域显隐

## 注意

- 代码**不会真正执行**，output 是作者预先填好的静态结果
- 多行代码用模板字符串，注意转义
- 需要真实可运行的 REPL → 不在本 skill 范围

## 何时不用

- 代码无需"运行"演示 → 普通 code block
- 要展示多语言同一算法 → 用 CodeTabs
