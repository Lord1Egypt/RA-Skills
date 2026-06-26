---
name: code-write
description: Implement or modify code in the current local project while matching local style and handling edge cases. Use when the user asks to add a feature, patch logic, fill in missing code, update tests, or make a concrete code change inside the workspace. Do not use for spawning external coding agents or managing remote repositories. Chinese triggers: 写代码、实现功能、补全代码、修改逻辑、直接改代码、补测试.
---

# 代码编写

先读上下文，再只改需求要求的部分。

## 工作流

1. 修改前先读受影响文件，以及附近的调用方、测试和配置。
2. 严格匹配项目现有命名、格式、结构和异常处理风格。
3. 只实现用户要求的行为，不顺手扩功能。
4. 明确处理非法输入、空状态、资源缺失和失败路径。
5. 不写死密钥、不伪造逻辑、不留下死代码和无用变量。
6. 只有在代码难读时才补简短注释。
7. 项目已有测试体系时，优先补或更新最相关的测试。
8. 改完后运行最小必要验证。

## 约束

- 没读过的文件不要直接改
- 没要求的新功能不要自行添加
- 除非项目本来就这样做，否则不要硬编码环境值
- 优先最小且安全的差异

## 输出

- 修改了哪些文件
- 实现理由的简短说明
- 已做验证，或未验证的阻塞原因
