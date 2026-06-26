# Subagent and Git Prerequisites

这个 skill 支持把“搜索与抓取”阶段并行化，但不应假设所有环境都天然支持 subagent/worktree。

## 一、何时适合用 subagent

适合：
- 需要扩展多组 query
- 需要并行搜索不同来源或不同语言关键词
- 需要并行核验多个候选平台

不适合：
- 任务量很小
- 当前环境不稳定
- 当前没有 git/worktree 前置条件
- 最终写入飞书阶段

## 二、subagent 的职责边界

subagent 可以做：
- query 扩展
- 搜索候选
- 抓取官网、docs、pricing、terms 等公开页
- 提取初步结构化字段
- 返回候选摘要和证据链接

subagent 不应做：
- 最终历史去重
- 风险等级定稿
- 飞书写入
- 最终面向用户的主结论

## 三、如果要用 worktree 隔离

某些 agent/worktree 运行依赖 git 仓库环境。开始前检查：

1. 当前目录是否在 git 仓库里
2. 仓库是否至少有一个 commit
3. `HEAD` 是否可解析

检测命令见 `smoke-tests.md` 第 7 项。

## 四、已知常见问题

### 1. 不在 git 仓库
可能出现：
- 无法创建 agent worktree

处理：
- 初始化 git 仓库，或不要使用依赖 worktree 的 subagent 模式

### 2. git 仓库存在，但没有 commit
可能出现：
- `Failed to resolve base branch \"HEAD\"`
- `git rev-parse failed`

处理：
- 创建至少一个初始 commit，再尝试使用 worktree/subagent

### 3. 多个 subagent 同时修改同一目标
风险：
- 冲突
- 重复写入
- 汇总格式漂移

处理：
- 搜索与抓取可并行
- 汇总与飞书写入必须由主代理串行完成

## 五、无 subagent 时的降级规则

如果环境没有 subagent，或 worktree 前置条件不满足：
- 改为主代理串行执行所有步骤
- 仍然保留相同纪律：
  - 先搜索和抓取
  - 再汇总去重
  - 再统一分层
  - 最后串行写飞书

没有 subagent 只会影响效率，不应该影响流程正确性。
