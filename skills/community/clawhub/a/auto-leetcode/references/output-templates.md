# 输出模板

## 题目内容.md 模板

```markdown
# {序号}.{名称}

- 难度：{简单/中等/困难}
- 题目链接：{LeetCode题目URL}

## 题目描述

{题目描述原文}

## 示例

**示例 1：**
```
输入：{input}
输出：{output}
解释：{explanation}
```

**示例 2：**
```
输入：{input}
输出：{output}
解释：{explanation}
```

## 提示

{约束条件}
```

## 解题思路.md 模板

```markdown
# {序号}.{名称} 解题思路

## 问题分析

{对问题的核心分析，关键洞察}

## 解法一：{解法名称}

### 思路

{详细思路描述}

### 算法步骤

1. {步骤1}
2. {步骤2}
3. ...

### 复杂度分析

- 时间复杂度：O(?)
- 空间复杂度：O(?)

## 解法二：{最优解法名称}（推荐）

### 思路

{详细思路描述}

### 算法步骤

1. {步骤1}
2. {步骤2}
3. ...

### 复杂度分析

- 时间复杂度：O(?)
- 空间复杂度：O(?)
```

## 代码文件模板

### Python (.py)

```python
"""
{序号}.{名称}
难度：{难度}
链接：{URL}
"""


class Solution:
    def {method_name}(self, {params}):
        # {简要说明}
        {代码逻辑}
```

### C++ (.cpp)

```cpp
/*
 * {序号}.{名称}
 * 难度：{难度}
 * 链接：{URL}
 */

class Solution {
public:
    {return_type} {method_name}({params}) {
        // {简要说明}
        {代码逻辑}
    }
};
```

### Java (.java)

```java
/*
 * {序号}.{名称}
 * 难度：{难度}
 * 链接：{URL}
 */

class Solution {
    public {return_type} {method_name}({params}) {
        // {简要说明}
        {代码逻辑}
    }
}
```

### JavaScript (.js)

```javascript
/*
 * {序号}.{名称}
 * 难度：{难度}
 * 链接：{URL}
 */

/**
 * @param {type} {param}
 * @return {type}
 */
var {method_name} = function({params}) {
    // {简要说明}
    {代码逻辑}
};
```

### Go (.go)

```go
/*
 * {序号}.{名称}
 * 难度：{难度}
 * 链接：{URL}
 */

func {method_name}({params}) {return_type} {
    // {简要说明}
    {代码逻辑}
}
```

### Rust (.rs)

```rust
/*
 * {序号}.{名称}
 * 难度：{难度}
 * 链接：{URL}
 */

impl Solution {
    pub fn {method_name}({params}) -> {return_type} {
        // {简要说明}
        {代码逻辑}
    }
}
```