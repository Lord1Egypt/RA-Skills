## 构建与编码错误自检规范（Auto Run）

本文件从 `SKILL.md` 的「构建与编码错误自检」章节抽取而来，用于规范与百度地图 HarmonyOS SDK 相关改动的构建流程。

### 1. 适用范围（强制）

每次在本仓库内**完成任意与百度地图 HarmonyOS SDK 相关的代码改动后（尤其是在提交 / 合并前）**，都需要执行一次构建自检流程。

### 2. Auto Run 构建流程

在工程根目录（例如 Harmony 应用根目录）执行：

1. 安装依赖：

```bash
ohpm install
```

2. 执行构建与 ArkTSCheck：

```bash
hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon
```

> 提示：在 CI 中建议将以上命令作为固定步骤，保证所有与地图相关的改动都经过同样的构建校验。

### 3. 对构建失败的处理要求

#### 3.1 编码错误（必须修复）

若构建命令报告**编译 / 语法 / 类型检查等编码错误**（例如 ArkTS 语法错误、类型不匹配、缺少符号等），开发者或代理必须：

- 根据错误信息主动回溯到本次改动的相关文件和代码位置；
- 对代码进行修正，而不是仅给出文字说明；
- 再次执行同样的构建命令，直至与本次改动相关的编码错误被消除；
- 在对外说明中明确标注「已按 auto run 规范完成一次构建并修复由本次修改引入的错误」。

#### 3.2 环境 / 工具链问题

若构建失败的原因属于**环境 / 工具链问题**（例如 Hvigor 版本与 `modelVersion` 不匹配、SDK 安装不完整、网络异常导致依赖无法下载等），则应：

- 在说明中**明确区分**这是环境问题而非编码问题；
- 原样展示或概述关键错误信息（如「Unsupported modelVersion of Hvigor 6.0.0. The supported Hvigor modelVersion is 5.0.4」）；
- 提示需要在本地或 CI 环境中调整 Hvigor 版本、SDK 或网络环境后重新尝试构建。

### 4. 无法在当前环境执行构建时

在某些无法实际执行上述命令的场景（例如当前运行环境不支持 Hvigor 或 ohpm）下，开发者或代理需要：

- 在文档或回答中**显式提示**：需要在本地工程目录手动执行 `ohpm install` 与 `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon`；
- 将本地构建是否通过作为本次修改是否可用的最终判定依据。

