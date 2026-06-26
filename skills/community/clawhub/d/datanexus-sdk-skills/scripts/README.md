# scripts/ — 能力7 自动化接入脚本集

> 这些脚本配合 SKILL.md **能力7** 使用。由 IDE Agent 在**用户明确请求自动接入**时串行调用。
>
> 单个脚本也可以独立使用，便于调试和排错。

## 脚本一览

### 能力7 自动化接入脚本（本次新增）

| 脚本 | 作用 | 输入 | 输出 |
|---|---|---|---|
| `detect_framework.py` | 识别客户项目的 SDK 端、框架、语言 | 项目根路径 | JSON / 人类可读 |
| `scan_integration_points.py` | 扫描生命周期入口、付费/登录/分享触点、已有 SDK | 项目根路径 + SDK 端 | JSON / 人类可读 |
| `generate_init_patch.py` | 综合上述结果 + 用户参数，生成结构化接入方案 | 两个 JSON + 接入参数 | 方案 JSON |
| `validate_integration.py` | 静态校验接入是否完整（init/start/依赖/权限/占位符等） | 项目根路径 + SDK 端 | 检查项 JSON / 人类可读 |

### 能力8 接入体检脚本

| 脚本 | 作用 | 输入 | 输出 |
|---|---|---|---|
| `audit_integration.py` | **已接入项目的深度体检**：必报事件覆盖度、初始化规范、用法正确性、自动采集冗余、合规性 | 项目根路径 + SDK 端 + 业务场景 | 检查项 JSON / 人类可读 |

> 与 `validate_integration.py` 的区别：validate 是"接入后快速过关检查"；audit 是"接入一段时间后的体检报告"。
> 详见 SKILL.md 能力8 章节。

### 排障/运维辅助脚本（原有）

| 脚本 | 作用 | 归属能力 |
|---|---|---|
| `查询上报日志.py` | 解析本地抓包导出的 SDK 上报日志，校验必报事件覆盖 | 能力6（问题排查） |
| `校验数据源配置.py` | 通过 DataNexus API 校验数据源 ID 是否有效、类型是否匹配 | 能力5（质量评估） |

> 两类脚本互不冲突：能力7 脚本用于"接入前 / 接入时"，辅助脚本用于"接入后 / 排障时"。

所有脚本遵循：
- **纯 Python 3 标准库**（无第三方依赖）
- **零副作用**（除 generate 可选落盘、校验数据源需调 API 外，不触碰客户项目）
- **能力7 脚本的 `--json` 模式**统一产生结构化输出，便于 Agent 消费

## 快速上手

### 场景 1：完整自动化接入（IDE Agent 场景）

由 IDE Agent 顺序执行：

```bash
cd <客户项目根目录>

# 1. 识别
python3 /path/to/datanexus-sdk-skills/scripts/detect_framework.py . --json > /tmp/detect.json

# 2. 扫描（从 detect.json 读 sdk_end）
SDK_END=$(python3 -c "import json; print(json.load(open('/tmp/detect.json'))['sdk_end'])")
python3 /path/to/.../scripts/scan_integration_points.py . --sdk-end "$SDK_END" --json > /tmp/scan.json

# 3. 生成方案（接入参数由 Agent 向用户收集）
python3 /path/to/.../scripts/generate_init_patch.py \
  --detect-json /tmp/detect.json \
  --scan-json /tmp/scan.json \
  --user-action-set-id 123456 \
  --secret-key YOUR_KEY \
  --appid wx1234567890abcdef \
  --output /tmp/plan.json

# 4. Agent 读取 /tmp/plan.json，按 step_3_code_changes 调用自身 edit 工具写入

# 5. 校验
python3 /path/to/.../scripts/validate_integration.py . --sdk-end "$SDK_END"
```

### 场景 2：仅识别场景（诊断用）

想知道"我这个项目能不能用自动接入"：

```bash
python3 scripts/detect_framework.py /path/to/my-project
```

输出示例：
```
🔍 项目场景识别结果
  SDK 端：mini-game  （置信度 100%）
  package_manager: npm
  language: TypeScript
  framework: Cocos Creator

🎯 自动化接入：✅ 支持
  原因：mini-game / Cocos Creator 在白名单
```

### 场景 3：仅质量校验（排障用）

接入完成后（无论是自动还是手动），跑一遍确认质量：

```bash
python3 scripts/validate_integration.py /path/to/my-project --sdk-end android
```

输出示例：
```
🔎 DataNexus SDK 接入质量校验（SDK 端：android）

  ✅ [dep_installed] GDTActionSDK 已在 build.gradle 引用
      → 已引用 GDTActionSDK
  ✅ [init_call] GDTAction.init 已调用
      → 找到 1 处 init 调用
  ❌ [start_call] GDTAction.start 已调用（v2.1+ 必须）
      → 未找到 GDTAction.start 调用；SDK 不会工作
  ✅ [internet_permission] AndroidManifest.xml 已声明 INTERNET 权限
      → 已声明
  ⚠️ [start_app_report] START_APP 事件已上报（Android 需手动）
      → 未发现 START_APP 上报...

📊 汇总：PASS 3 / WARN 1 / FAIL 1 （共 5 项）
❌ 存在错误，SDK 可能无法正常工作，请修复后重跑本脚本。
```

### 场景 4：已接入项目深度体检（能力8）

对已经接入一段时间的项目做系统性质量评估：

```bash
# mini-game 必须显式指定 --scenario（IAP / IAA 必报事件差异大）
python3 scripts/audit_integration.py /path/to/my-project --sdk-end mini-game --scenario iap-mini-game

# 其他端可不指定（使用合理默认）
python3 scripts/audit_integration.py /path/to/my-app --sdk-end android

# JSON 模式供 Agent 消费
python3 scripts/audit_integration.py /path/to/my-project --sdk-end mini-game --scenario iaa-mini-game --json
```

支持的场景：
- `mini-game`：`iap-mini-game` / `iaa-mini-game`
- `mini-program`：`drama` / `novel` / `ecommerce` / `general-mini-program`
- `android` / `ios`：`game-app` / `general-app`
- `harmony`：`general-app`

输出五大维度：**必报事件覆盖度**、初始化规范、用法正确性、自动采集冗余、合规。

## 安全声明

- ❌ 所有脚本**不采集客户代码**到任何外部服务
- ❌ **不写入** `secret_key` 等敏感信息到日志或缓存
- ✅ 运行全程在客户本地，脚本自身不发起任何外部网络请求
- ✅ 脚本支持 offline 运行，不依赖 DataNexus 平台 API

## 退出码约定

| 退出码 | 含义 |
|---|---|
| 0 | 正常完成 / 校验全部通过 |
| 1 | 识别失败 / 有 WARN 级别问题 |
| 2 | 致命错误 / 有 FAIL 级别问题 |

## 贡献指南

- 新增支持的 SDK 端 → 同时修改 4 个脚本的 `RULES_BY_SDK_END` / `VALIDATORS` / 模板常量
- 新增支持的框架 → 在 `detect_framework.py` 的 `JS_FRAMEWORK_PATTERNS` / `FILE_BASED_ENGINES` 中加规则
- 所有规则必须**先跑一遍真实项目验证**，避免误识别
- 保持**零依赖**（纯标准库）原则，便于部署
