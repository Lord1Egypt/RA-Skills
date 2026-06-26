# Browser Automation Routing - 统一 Spec

## 基本信息

- 名称：`browser-automation-routing`
- 目标：让 `skill-factory` 在强需求浏览器自动化任务里具备稳定的路线比较、推荐顺序和安装说明
- 当前阶段：文档与流程治理，不进入脚本实现

## 必须满足的要求

### 要求 1

如果任务强依赖浏览器自动化，调研阶段必须比较至少 2 条方向。

### 要求 2

比较时必须说明：

- 登录态复用
- 安装门槛
- 调试深度
- 稳定性
- 维护成本
- 替代路径

### 要求 3

如果用户接受额外安装，且业务被 `OpenCLI` 支持面覆盖，优先推荐 `OpenCLI`。

### 要求 4

推荐 `OpenCLI` 时，必须附带：

- Browser Bridge 扩展安装说明
- `opencli doctor` 验收方式

### 要求 5

如果 `OpenCLI` 覆盖不足，继续保留 `agent-browser` 或 `playwright-interactive` 作为替代路径。

## 输入

- `opencli` 本地 Skill
- `playwright-interactive` 本地 Skill
- `agent-browser` 本地 Skill
- `OpenCLI` 官方仓库
- `agent-browser` 官方仓库

## 输出

- 更新后的主 Skill 与阶段文档
- 更新后的浏览器原子能力文档
- 一份 `OpenCLI Browser Bridge` 安装指南
- 一组 `output/browser-automation-routing/` 构建产物

## 成功标准

- 浏览器自动化比较规则已经进入 `prd.md`
- 主 Skill 和调研、设计阶段文档已经写明路线比较与推荐顺序
- `OpenCLI` 安装指南已经进入仓库
- `output/` 下存在本次规则收口的完整样例产物
