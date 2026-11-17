# 工程脚手架与初始化（实测 2026-08）

> 环境就绪（[environment.md](environment.md)）开始初始化工程。本文件解决"新插件工程长什么样、先配什么、怎么验证能跑通"。
> 形态选型见 [plugin-forms.md](../00-understanding/plugin-forms.md)；打包发布见 [packaging.md](../50-ship/packaging.md)。

## 1. 目录结构

```
<plugin-root>/
├── package.json          # 元数据 + 依赖 + 发布入口（files/exports/peerDependencies）
├── tsconfig.json         # 类型工程配置（moduleResolution/outDir/declaration）
├── cordis.patch.yml      # 声明式装配：entry 树 + 插件启用 + HMR 重载（依赖 dsh scaffold 场景才需要）
├── src/
│   ├── index.ts          # 插件入口（导出 apply / Service 子类）
│   └── *.ts              # 会话逻辑 / hook / tool / service
├── client/               # （可选）Client UI bundle，包名通常 -client
└── tests/
```

## 2. 关键配置文件

### package.json
- `name`：npm 包名（小写+连字符），被 `dsh plugin add` 直接引用
- `type`：`module`（DSH/ESM 生态）
- `exports`：声明子路径入口（如 `"./client"` 供 Client UI bundle 定位）
- `files`：白名单决定打进 tarball 的文件——**漏配会丢运行时资产**（见 `traps.md` #43）
- `peerDependencies`：与宿主共享的依赖必须显式声明，漏声明会导致 Service 基类分裂（见 `traps.md` #44）
- `dsh.bundle` / `dsh.client.platform`：声明插件在 DSH 的加载形态（Client 装载声明见 `client-ui.md` 7.4）

### tsconfig.json
- 常见工程坑：`tsx` 找不到、`@types/node` 缺失、`paths` 指到 junction 导致类型分裂（见 `traps.md` #40）

### cordis.patch.yml
- 声明式装配：`plugin: { id, apply }` 条目 + `Config` schema；HMR 事务式重载
- 装配坑：条目无 id → HMR 全量重挂；patch 整体替换非深度合并（见 `traps.md` §16）

## 3. 初始化顺序

1. **形态选型**：决定函数 / 对象 / Service 子类（[plugin-forms.md](../00-understanding/plugin-forms.md)）
2. **配置骨架**：`package.json` → `tsconfig.json` → 目录结构
3. **声明式装配**（需要注入/多插件场景）建 `cordis.patch.yml`
4. **环境验证**：本地以 loader 启动 `node --import tsx vendor/cordis/bin.js` 跑通最小 `apply`
5. **写代码前**：用 `cordis_inspect_*` 精确确认每个用到的 Service/Event/Slot 契约（[inspect-workflow.md](inspect-workflow.md)）

## 4. 预留扩展

- 需要 Client UI → 建 `client/` 并声明 `exports["./client"]` + `dsh.client.platform`
- 需要动态脚本 → 建 `scripts/`（纯 JS，不可 import 磁盘模块）
- 需要技能资产 → 建 `skills/` 或资产目录，用 `resourceBase` 定位