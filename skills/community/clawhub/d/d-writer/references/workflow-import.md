# 模式 C：导入现有章节并续写

## 触发时机

手里有旧章节，但状态文件很弱或缺失。

## 步骤

1. **按文件顺序、标题、或用户给出的拆分规则把源文本拆成有序章节**。
2. **创建或选定目标书**。
3. **从已有证据而非凭空想象构建基础文件**：
   - 用早期章节推断前提与基调
   - 用晚期章节推断当前续写起点
   - 用中段锚点推断弧线演化
   - 用标题目录推断整体结构
4. **按模式 A 写基础文件**（详见 `references/workflow-new-book.md`）。
5. **把导入章节回放到运行时文件**：
   - 保存章节文件
   - 追加摘要
   - 提取当前状态与活跃钩子
   - 推断风格指南
6. **从第一个未写章节起按模式 B 续写**（详见 `references/workflow-continue.md`）。

## 相关文档

- 模式 A（创建新书）：`references/workflow-new-book.md`
- 模式 B（续写）：`references/workflow-continue.md`
- 文件职责与兼容命名：`references/file-contract.md`
- 基础文件模板：`references/templates.md`
