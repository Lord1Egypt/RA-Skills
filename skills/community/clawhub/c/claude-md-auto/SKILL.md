# CLAUDE.md 自动发现技能

自动发现并加载项目根目录的 CLAUDE.md 文件，参考 Claude Code 实现。

## 功能
1. 自动查找 ./CLAUDE.md 和 ./ CLAUDE.md
2. 支持 @include 指令
3. 最大 40000 字符限制
4. 逆序加载（后面的文件优先级更高）

## 触发条件
- 当用户发送消息时自动执行
- 无需用户手动调用

## 实现
- 使用 fs.readFileWithinRoot 读取文件
- 遍历当前工作目录向上查找
- 解析 @include 指令
- 注入到系统上下文