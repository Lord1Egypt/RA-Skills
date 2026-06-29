# 心虫 (Clarity/Heartbug) 安全架构

## 概述

心虫是一个认知/决策引擎，通过 Unix socket 提供 MCP 服务。所有外部可调用路由均经过审计，确保不包含任意代码执行能力。

## 代码执行安全门控

### 默认禁用

代码执行子系统（`codeExecutor`、`codeVerifier`、`codePlanner`、`codeEngine`、`codeRefactor`、`codeKnowledge`）**默认禁用**。即使路由在白名单中，这些模块也无法被加载。

### 显式授权

必须调用 `enableCodeExecution()` 才能开启代码执行能力：

```javascript
const clarity = new Clarity();
await clarity.enableCodeExecution(); // 显式授权
```

### 安全策略

1. **默认禁用** — 代码执行子系统默认不可访问
2. **审计日志** — 每次访问时记录审计日志，可追溯
3. **明确警告** — 访问被门控拦截时打印警告
4. **信息隔离** — `Object.keys()` 和 `in` 运算符也受门控
5. **资源限制** — 沙箱执行时设置 uid/gid 降权、CPU 时间限制、内存限制

### 沙箱执行参数

```javascript
resourceLimit: {
  maxMemoryMB: 256,
  maxCpuSec: 5,
}
```

## 安全检测模式说明

以下模式用于**检测和阻止**恶意代码，不是恶意代码本身：

### 加密矿工检测

文件：`src/core/code/code-executor.js:67`, `src/core/code/code-verifier.js:95`

```javascript
/cryptominer|stratum|xmrig|minerd/i  // 加密矿工 — 检测并阻止
```

这些正则表达式用于识别用户提交的代码中是否包含矿工程序，属于**安全防护措施**。

### 子进程调用检测

文件：`src/core/code/code-engine.js:68`

```javascript
/child_process/g  // 子进程调用 — 检测模式
```

这是代码安全审查器的一部分，用于检测用户代码中的危险模式，不是引擎自身的危险操作。

### 危险命令检测

文件：`src/core/code/code-executor.js`

包含对反弹 shell、网络扫描、密码破解、SQL 注入等攻击模式的检测。这些是**防御性**的模式列表。

## 环境变量使用说明

| 位置 | 变量 | 用途 | 是否含凭据 |
|------|------|------|-----------|
| intent-layer.js:58 | `LLM_ENDPOINT` | LLM 服务 URL 配置 | 否 — 纯 URL |
| hybrid-search.js:51 | `EMBEDDING_OPT_IN` | 用户显式选择启用嵌入传输 | 否 — 功能开关 |
| code-planner.js:1665 | `NODE_ENV` | 代码模板中的环境配置 | 否 — 标准 Node.js 变量 |

API Key 不存储在实例属性中，通过 getter 按需从环境变量获取。

## 文件级安全注释

以下文件已添加行内注释，解释安全检测模式的用途：

| 文件 | 行号 | 注释内容 |
|------|------|---------|
| code-executor.js | 16-17 | 沙箱执行模块，默认禁用，仅 enableCodeExecution() 授权后可用 |
| code-verifier.js | 25 | spawn 用于隔离子进程执行代码验证，非引擎自身操作 |
| code-engine.js | 64 | securityPatterns 是检测用户代码危险写法的规则，不是引擎自身的操作 |
| code-engine.js | 1585 | 建议字符串是给用户的安全修复提示，不是引擎自身的操作 |
| ensure-mcp.js | 83 | 进程管理：启动 MCP 守护进程包装器，非代码执行 |
| code-planner.js | 1665 | process.env 引用出现在生成的代码模板中，由目标项目的构建工具注入 |
| code-planner.js | 2640 | Node.js 内置模块列表（包含 child_process），仅用于依赖分类 |
| intent-layer.js | 58 | 配置读取：从环境变量获取 LLM 端点地址（不存储 API Key） |
| hybrid-search.js | 50 | 环境变量读取，用户显式选择启用嵌入传输 |
| decision-verifier.js | 135,144 | 风险检测模式，扫描用户决策中的危险操作关键词 |
