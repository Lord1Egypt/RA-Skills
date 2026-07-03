# 沙箱深度设计

> Sandbox is the LAST line of defense in a 6-layer security model.
> Even if permissions and hooks are bypassed, the sandbox limits what an Agent can do.

---

## 设计哲学

### 6 层安全模型中的位置

```
Layer 1: LLM 对齐 (RLHF/Constitutional AI)        ← 意图约束
Layer 2: System Prompt 注入防御                     ← 上下文约束
Layer 3: Tool 权限清单 (Allowlist)                  ← 能力约束
Layer 4: Hook 拦截 (Pre/Post Execution)             ← 行为约束
Layer 5: Permission 门禁 (Human-in-the-loop)       ← 审批约束
Layer 6: Sandbox 隔离 ★                             ← 执行约束 (最后防线)
```

当 L1-L5 全部被绕过时，Sandbox 是阻止 Agent 造成实际破坏的核⼼机制。
因此 Sandbox 必须独立于 Agent 自身的代码逻辑，作为外部执行容器运转。

### 核心原则

1. **最小权限 (Least Privilege)**：Agent 默认对文件系统、网络、进程无任何访问权，逐项白名单开放
2. **不可绕过 (Non-bypassable)**：Agent 代码无法脱离沙箱环境执行，即使用户同意豁免
3. **凭证外置 (Credential Externalization)**：敏感凭证绝不进入沙箱文件系统
4. **执行隔离 (Execution Isolation)**：每个 Agent 实例拥有独立的内核级命名空间

---

## 三层隔离模型

```
┌──────────────────────────────────────────────┐
│  第一层：文件系统隔离 (Mount Namespace)        │
│  ├─ 只读挂载: 项目源码、系统库                 │
│  ├─ 可写挂载: 工作目录 (限定了目录)            │
│  ├─ tmpfs: /tmp 临时文件（会话结束后销毁）      │
│  └─ 禁止挂载: .git/、.env、~/.ssh、credentials │
├──────────────────────────────────────────────┤
│  第二层：网络隔离 (Network Namespace)           │
│  ├─ 默认: 所有出站连接 deny                     │
│  ├─ Allowlist: 仅允许声明的域名/IP + 端口        │
│  ├─ DNS 解析: 通过白名单代理，防 DNS 隧道        │
│  └─ 入站: 完全禁止 (Agent 无需监听端口)          │
├──────────────────────────────────────────────┤
│  第三层：进程隔离 (PID Namespace + cgroups)      │
│  ├─ PID 命名空间: Agent 仅可见自身子进程         │
│  ├─ CPU limit: cgroups v2 限制 CPU 使用率       │
│  ├─ Memory limit: 硬限制 + OOM killer           │
│  ├─ Fork bomb 防护: 最大进程数限制              │
│  └─ 禁止的系统调用: mount, reboot, kmod, etc.   │
└──────────────────────────────────────────────┘
```

---

## 隔离技术深度对比

| 技术 | 启动时间 | 内核共享 | 隔离级别 | 资源开销 | 适用场景 | 代表性产品 |
|---|---|---|---|---|---|---|
| **Docker Container** | ~200ms | 共享宿主机内核 | 中等（命名空间） | 低 | Professional 级别 | docker-py, dockerode |
| **Firecracker microVM** | ~125ms | 独立 Guest 内核 | 高（硬件虚拟化） | 中 | Enterprise 级别 | AWS Lambda, Fly.io |
| **gVisor** | ~10ms | 用户态内核模拟 | 高（系统调用拦截） | 中 | Enterprise 级别 | Google Cloud Run |
| **WebAssembly (WASI)** | ~μs | 沙箱内虚拟机 | 指令级 | 极低 | 插件/扩展执行 | wasmtime, wasmedge |
| **bubblewrap (bwrap)** | ~5ms | 共享宿主机内核 | 中等（命名空间） | 极低 | Claude Code 采用 | flatpak 底层 |
| **Seccomp + Namespaces** | ~1ms | 共享宿主机内核 | 中-高 | 极低 | 定制化需求 | Linux 原生 |

### 技术选型决策矩阵

```
条件判断流程：
  信任级别 == "完全信任" → Minimal (路径白名单)
  信任级别 == "低信任" 且 平台 == "Linux" → bubblewrap
  信任级别 == "低信任" 且 平台 != "Linux" → Docker
  信任级别 == "零信任" 且 延迟敏感 → Firecracker
  信任级别 == "零信任" 且 延迟不敏感 → gVisor
  场景 == "插件系统" → WebAssembly (WASI)
```

---

## 凭证外置架构 (Credential Externalization)

### 设计原则

```
凭证 NEVER 进入沙箱文件系统
   ↓
生命周期：
  创建 (外部) → 存储 (加密) → 注入 (只读挂载) → 使用 (Agent) → 轮换 (外部) → 吊销 (外部)
```

### 架构流程

```
┌────────────┐     ┌──────────────┐     ┌─────────────────┐
│ 凭证管理器 │────→│ 加密存储     │────→│ 临时注入         │
│ (外部)     │     │ (Vault/KMS)  │     │ (tmpfs 只读挂载) │
└────────────┘     └──────────────┘     └─────────────────┘
                                              │
                                              ▼
┌────────────┐     ┌──────────────┐     ┌─────────────────┐
│ 使用后销毁 │←────│ 会话结束     │←────│ Agent 进程中     │
│ (吊销)     │     │ (沙箱销毁)   │     │ 环境变量引用     │
└────────────┘     └──────────────┘     └─────────────────┘
```

关键约束：
- 凭证以环境变量形式注入，不以文件形式存在
- tmpfs 在沙箱销毁时自动清除，无残留
- 凭证管理器与 Agent 运行在不同安全域
- 短期凭证 (STS Token)，有效期 ≤ 会话时长

---

## Sandbox 配置 → 权限规则映射

从 Claude Code 源码中抽象的模式：

| 权限规则 | 沙箱配置 | 作用域 |
|---|---|---|
| `Read(/path/to/dir)` | `sandbox.filesystem.allowRead: [/path/to/dir]` | 文件只读挂载 |
| `Edit(/path/to/dir/*)` | `sandbox.filesystem.allowWrite: [/path/to/dir]` | 文件可写挂载 |
| `Bash(allowed_cmds)` | `sandbox.process.allowedCommands: [cmd1, cmd2]` | 命令白名单 |
| `Bash(denied_cmds)` | `sandbox.process.blockedCommands: [rm -rf, sudo]` | 命令黑名单 |
| `WebFetch(domain:api.com)` | `sandbox.network.allowedDomains: [api.com]` | 网络白名单 |
| `WebSearch(allow)` | `sandbox.network.allowedDomains: [*google.com, *duckduckgo.com]` | 搜索域名 |

映射规则：
- 权限 grant 自动添加对应的沙箱开放项
- 权限 revoke 自动移除对应的沙箱开放项
- 规则变更在下一个 Turn 开始时生效（非即时，防止竞态）
- 所有规则集合取并集操作，无隐式拒绝

---

## 硬编码安全不变量

以下路径在**所有**沙箱配置中 ALWAYS deny write（不可配置）：

| 路径模式 | 原因 |
|---|---|
| `.claude/settings*.json` | 防止 Agent 自我提权 |
| `.claude/skills/` | 防止 Agent 注入恶意技能 |
| `.claude/commands/` | 防止 Agent 篡改命令定义 |
| `.git/HEAD` | 防止 Agent 破坏版本历史 |
| `.git/objects/` | 防止 Agent 破坏对象存储 |
| `.git/refs/` | 防止 Agent 篡改分支引用 |
| `.git/config` | 防止 Agent 修改仓库配置 |

bare repo 检测与清理：
```
在每轮命令执行后，检测 .git 目录结构完整性：
  1. 检查 HEAD 是否存在 → 不存在则恢复
  2. 检查 objects/ 完整性 → 损坏则 fsck
  3. 检查 refs/ 完整性 → 异常则从 reflog 恢复
  4. 检测额外文件（Agent 尝试注入） → 自动清除并告警
```

---

## 规模特定实现概要

### Minimal (~50 行)
```
核心组件：
  - PathResolver: 路径规范化 + 白名单检查
  - 无进程隔离，依赖 Python 自身限制
  - 无网络隔离

实现要点：
  - 所有文件操作前调用 PathResolver.validate(path, mode)
  - 拒绝符号链接（防逃逸）
  - 拒绝包含 ../ 的路径
```

### Professional (~200 行)
```
核心组件：
  - SandboxManager: 管理 Docker 容器生命周期
  - ImageBuilder: 构建预配置的容器镜像
  - 基于 docker-py 的容器操作

实现要点：
  - 构建最小化镜像（alpine-based，< 50MB）
  - 挂载卷时使用 :ro (只读) 标记
  - 网络使用 --internal (仅容器间通信)
  - 资源限制：--memory=512m --cpus=1
```

### Enterprise (~500 行)
```
核心组件：
  - FirecrackerManager: 微 VM 生命周期管理
  - CredentialInjector: 凭证注入模块
  - AuditLogger: 沙箱事件审计

实现要点：
  - 启动独立 Guest 内核 (linuxkit/firecracker-kernel)
  - 根文件系统为只读 squashfs
  - 以 tmpfs 作为可写层，会话结束销毁
  - 凭证通过 MMDS (MicroVM Metadata Service) 注入
  - 每次 Agent 实例分配独立 VM
  - VM 销毁前导出审计日志
```

---

## 攻击面与缓解

| 攻击向量 | 缓解措施 |
|---|---|
| 路径遍历 (`../../etc/passwd`) | 路径规范化后白名单匹配，拒绝 `..` |
| 符号链接逃逸 | 解析所有 symlink 后再做白名单校验 |
| 时间侧信道 | 禁用高精度计时器 (seccomp: `clock_gettime` only) |
| /proc 信息泄露 | 挂载独立的 procfs，隐藏宿主机进程 |
| DNS 隧道 | 仅允许通过受控 DNS 代理的解析请求 |
| 内核漏洞提权 | seccomp filter + 禁止 `unshare`, `clone` 等系统调用 |
| 资源耗尽 (Fork Bomb) | cgroups pids.max 限制 |
| 磁盘写满 | filesystem quota + 文件大小上限 |

---

⚠ **AI 构建提示**：

```
根据用户选择的规模实现沙箱：

Minimal 级别：
  1. 实现 PathResolver 类，包含白名单存储和验证方法
  2. 在所有文件 I/O 操作前调用 validate()
  3. 不引入任何外部依赖
  4. 提供清晰的错误消息提示路径被拒绝

Professional 级别：
  1. 定义 Dockerfile（最小化基础镜像）
  2. 使用 docker-py 创建/启动/停止容器
  3. 实现卷挂载映射（读写卷 + 只读卷）
  4. 设置容器资源限制
  5. 提供 stop_and_cleanup() 方法确保资源回收

Enterprise 级别：
  1. 集成 Firecracker SDK 或 bubblewrap
  2. 实现凭证注入模块
  3. 实现审计日志导出
  4. 添加 seccomp profile 限制系统调用
  5. 管理 VM 生命周期（创建/使用/销毁）

所有级别必须：
  □ 不出现在同一文件的沙箱实现和 Agent 逻辑
  □ 提供资源清理方法
  □ 对逃逸尝试记录告警
```