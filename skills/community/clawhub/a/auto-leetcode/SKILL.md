---
name: auto-leetcode
description: LeetCode刷题辅助技能。当用户提供LeetCode题目序号+名称时，自动获取题目内容、生成解题思路和带注释的代码，并在指定目录下创建题目文件夹。支持用户指定编程语言（默认Python）。当用户提到LeetCode刷题、做LeetCode题目、LeetCode题解、刷算法题等场景时触发。
---

# LeetCode 刷题助手

根据用户提供的题目序号+名称，自动生成题目内容、解题思路和代码，并创建本地文件夹。

## 输入要求

用户需提供：
- **题目序号+名称**（如 `42.接雨水`、`1.两数之和`）
- **本地目录路径**（如 `/Users/yihe/leetcode`）
- **编程语言**（可选，默认 Python；可选 `python`、`cpp`、`java`、`javascript`、`go`、`rust`）

若用户未提供目录或语言，主动询问。

## 工作流程

### 1. 获取题目内容

使用 `web-search-prime_web_search_prime` 搜索题目，关键词格式：`LeetCode {序号} {名称}`。

然后使用 `web-reader_webReader` 抓取题目页面内容（优先使用 LeetCode 中文站 `leetcode.cn` 的链接）。

从抓取内容中提取：
- 题目标题
- 难度（简单/中等/困难）
- 题目描述
- 输入输出示例
- 数据范围/约束条件

### 2. 生成解题思路

基于题目内容，分析并生成结构化的解题思路，包含：
- 问题分析与关键洞察
- 推荐解法（优先给出最优解）
- 算法步骤（伪代码或自然语言描述）
- 时间/空间复杂度分析
- 如有多种解法，列出对比（从暴力到最优）

### 3. 生成代码

根据用户指定语言（默认Python）生成带详细注释的代码：
- 函数/类签名词汇与LeetCode一致
- 中文注释解释关键逻辑
- 包含解题思路中的核心算法
- 代码风格参考 [references/code-style.md](references/code-style.md)

### 4. 创建本地文件

在用户指定目录下创建文件夹并写入文件。

**文件夹命名**：使用题目序号+名称（如 `42.接雨水`）

**文件结构**：
```
{目录}/{序号}.{名称}/
├── 题目内容.md
├── 解题思路.md
└── {序号}.{ext}
```

**语言与扩展名映射**：
| 语言 | 扩展名 |
|------|--------|
| python | .py |
| cpp | .cpp |
| java | .java |
| javascript | .js |
| go | .go |
| rust | .rs |

### 5. 文件内容格式

各文件格式参考 [references/output-templates.md](references/output-templates.md)。