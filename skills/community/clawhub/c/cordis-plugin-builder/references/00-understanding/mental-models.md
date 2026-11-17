# 认知模型：插件系统的组织方式（心智地图，2026-08 对话蒸馏）

> 操作流程见 [deployment-overview.md](../50-ship/deployment-overview.md) / [packaging.md](../50-ship/packaging.md)；本文件沉淀**如何理解**插件系统的
> 认知框架——先建立地图，再记操作，避免"每条都试错"。

## 1. 核心认知：三种加载机制并存，不是"都是动态的"

```
             作用域 ──────────────►
            整个进程            单会话
    ┌─────────────────┬────────────────┐
 持 │ ① 声明式装配      │ ② Agent Preset │
 久 │  cordis.patch.yml│  agent.cordis. │
 性 │  bundle→entry 树 │  yml→单会话工具 │
 持久│  启动+HMR 热更    │  会话结束卸载    │
 性 ├─────────────────┼────────────────┤
    │ ③ 动态 Cordis    │ （无对应——动态  │
 临 │  cordis_define/  │  插件总是进程内）│
 时 │  run→进程内即时   │                │
    └─────────────────┴────────────────┘
```

- 机制 ① 管"整个 DSH 进程装什么"（持久、共享）
- 机制 ② 管"这个会话有什么"（单会话、随会话卸载）
- 机制 ③ 管"临时实验"（进程内、重启即失）

**区分本质**：持久性（磁盘 vs 进程）× 作用域（整进程 vs 单会话）——不是"动态与否"。

## 2. 代码形态 × 部署形态正交（最易混淆的认知）

| | 代码形态（[plugin-forms.md](../00-understanding/plugin-forms.md)） | 部署形态（[deployment-overview.md](../50-ship/deployment-overview.md)） |
|---|---|---|
| 回答 | 插件长什么样 | 以什么形式进入 DSH |
| 维度 | 函数 / 对象 / Service 子类 | ①Bundle ②声明式 ③Preset ④Skill ⑤动态 ⑥Client |
| 可组合 | 任意代码形态 × 任意部署形态 | |

**推论**：dsh-memory 是 Service 子类（代码形态）× 声明式装配（部署形态 ②）——两个维度各占一位，互不冲突。

## 3. 装配成败由"配置语义"决定，不是会话模式

> 用户困惑"是不是创造/普通模式没选对"——**模式无关**：创造（cordis）/普通（standard）
> 是 Agent preset（会话侧工具集差异），不影响宿主组合装配。

装配成败的真正变量（实测）：
1. patch 条目语义：插入用 `- insert:`，裸 `- id:` 是覆盖（根列表空 → 静默跳过）
2. Windows 路径形态：`file:///E:/...`（裸盘符 → `ERR_UNSUPPORTED_ESM_URL_SCHEME`）
3. 改对文件层：只改 `cordis.patch.yml`，不动 profile 根 `cordis.yml`（启动被重写）

**排查心法**：插件"没装上"先怀疑配置语义，再怀疑代码——静默跳过不报错是 patch 语义错误的典型特征。

## 4. 判断口诀（选形态）

```
要构建什么？
│
├─ 有第三方依赖、要长期部署、跨会话共享 ──► ② 声明式装配（dsh-memory 即此）
├─ 复用"怎么做"的流程知识、零代码 ────────► ④ Skill
├─ 先验证想法 / 临时挂工具/UI（用完即弃） ──► ⑤ 动态插件
├─ 正式前端 UI / 主题 ───────────────────► ⑥ Client 插件
├─ 给角色/任务配不同工具集 ───────────────► ③ Agent Preset
└─ 只是用 DSH（不扩展）──────────────────► ① Bundle（不用管）
```

- 有第三方依赖的正式插件 → **声明式 ②**（dsh-memory 即此）
- 只想复用"怎么做"的流程知识、零代码 → **Skill ④**
- 先验证一个想法、临时挂工具/UI → **动态 ⑤**（用完即弃）
- 正式前端 UI/主题 → **Client ⑥**
- 给角色配工具集 → **Preset ③**
- 什么都不是、只是用 DSH → **Bundle ①**（不用管）

**铁律**：动态插件（⑤）纯 JS、不能 import 磁盘模块——有依赖的正式插件**绝不用动态方式**；先用 ⑤ 验证想法，再固化成 ②。

## 5. 卸载与装载的对称性（HMR 事务认知）

- 装载 = 配置出现 → watcher 装配 entry；卸载 = 配置消失 → watcher 拆除 entry
- **同一事务路径**：任一 entry 失败整体回滚到上一棵好树，不会半装载/半卸载
- 声明式卸载 = 删 patch 行（不是 `cordis_undefine`，那是动态插件的工具）
- 验证信号对称：装上 = 子进程出现 + 工具列表出现；卸下 = 两者消失

## 6. 部署视角：变更入口决定生效方式

七种部署流程（详见 [deployment-overview.md](../50-ship/deployment-overview.md)）背后一条认知：
**"改配置免重启，改代码层（bundle/client 生产态）要重启"**——HMR watcher 只覆盖
profile/home 两个 patch 层；bundle 层、client 生产 bundle 不在热更范围。

## 7. 打包认知：发布 ≠ 打包

- **npm pack**（tarball）是"打包"：本地产出可分发的 `.tgz`，不碰 registry——可立即验证
- **npm publish** 是"发布"：需要账号权限，且依赖版本必须 registry 可解析
- 打包前置：`workspace:^` → 真实版本；cordis/dsh-tools 进 peerDependencies（宿主同实例，防 Service 基类分裂）
- **版本对齐坑**：本地构建版本（如 dsh-tools 0.1.0-rc.5）可能不在 registry——先 `npm view` 查，再声明 `^` 范围
