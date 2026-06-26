---
name: 1688-distribution-shop-bind-newton
version: 0.1.0
description: |
  牛顿客户端分销买家绑店 Skill。当用户提到"绑定店铺"、"绑店"、"店铺授权"、"添加店铺"、"关联店铺"、"连接店铺"时使用。
  通过对话引导用户在牛顿 Electron 内嵌浏览器中完成绑店全流程，包括平台选择、授权登录、店铺绑定。
---

# 1688 分销绑店 - 牛顿

牛顿客户端绑店 Skill，通过自然对话引导用户完成店铺绑定全流程。

## 前置条件

执行本 Skill 前必须满足以下条件，**按顺序检查**：

1. **AK 已配置**：环境变量 `ALI_1688_AK` 已设置，或 OpenClaw 配置文件中包含有效 AK（否则所有 API 调用将返回认证失败）
2. **requests 已安装**：Python 环境中已安装 `requests` 库（`pip install requests`）
3. **牛顿客户端环境**：运行在牛顿 Electron 客户端中，支持 `browser_action` 指令（非牛顿环境下浏览器操作将降级为 Playwright fallback）

## 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `ALI_1688_AK` | 是 | — | 1688 API 认证密钥（Base64 编码的 AccessKeySecret + AccessKeyID） |
| `DISTRIBUTE_BASE_URL` | 否 | `https://skills-gateway.1688.com` | 1688 网关地址，用于测试或切换环境 |
| `OPENCLAW_CONFIG_DIR` | 否 | `~/.openclaw` | OpenClaw 配置文件目录，AK fallback 读取路径 |
| `NEWTON_CLIENT` | 否 | — | 设为 `true` 表示运行在牛顿客户端中 |
| `NEWTON_BROWSER_RESULT` | 否 | — | 牛顿客户端回传的浏览器操作结果（JSON） |

## Workflow

以下步骤**必须按顺序执行**，每步依赖上一步的输出：

### Step 1：查询 ISV 工具列表

获取用户可用的 ISV 工具和已绑定店铺，确定绑店的目标平台。

```bash
python3 cli.py shop_info
```

解析返回 JSON 中 `data.options` 列表，展示给用户选择目标平台和工具。

### Step 2：启动绑店流程

用户选择平台后，初始化绑店流程。需要传入 Step 1 中用户选择的 `channel` 和 `appKey`。

```bash
python3 cli.py bind_shop --action start --channel <channel> --app-key <appKey>
```

如果用户尚未选择平台，也可以传入用户输入让 Skill 自动匹配：

```bash
python3 cli.py bind_shop --action start --user-input "抖音"
```

### Step 3：处理浏览器操作

如果返回 JSON 中包含 `browser_action` 字段，说明当前步骤需要浏览器操作（如打开授权链接）。将 `browser_action` 和 `browser_params` 交给牛顿客户端执行。

等待用户在浏览器中完成授权/登录后，继续流程：

```bash
python3 cli.py bind_shop --action continue --channel <channel> --app-key <appKey>
```

### Step 4：轮询与推进

重复 Step 3 直到返回 JSON 中 `flow_completed` 为 `true`。每次 `continue` 会自动查询流程状态并返回下一步引导。

如需主动查询当前进度：

```bash
python3 cli.py bind_shop --action query --channel <channel> --app-key <appKey>
```

### Step 5：流程完成或关闭

当 `flow_completed` 为 `true` 时，绑店流程全部完成。

如需中途关闭流程：

```bash
python3 cli.py bind_shop --action close --channel <channel> --app-key <appKey>
```

## 输出约定

所有命令通过 stdout 输出 JSON，通过 exit code 表达执行状态。详见 [references/output_schema.md](references/output_schema.md)。

**Exit Code**：0=成功，1=参数错误，2=认证失败，3=业务异常，4=网络异常。

**埋点日志**通过 stderr 输出 JSON（含 `_tracker: true`），不影响 stdout 解析。

## References

- [references/commands.md](references/commands.md) — 完整命令用法参考
- [references/output_schema.md](references/output_schema.md) — 输出格式和字段说明
- [references/api_reference.md](references/api_reference.md) — 1688 网关接口和认证说明

## 依赖

- **Python**: 3.8+
- **requests**: HTTP 客户端（`pip install requests`，Skill 脚本中 `_http.py` 依赖此包）
- **牛顿客户端**: Electron 内嵌浏览器（用于响应 `browser_action` 指令）

## 文件结构

```
.
├── cli.py                        # CLI 统一入口
├── SKILL.md                      # 本文件
├── references/
│   ├── commands.md               # 命令用法参考
│   ├── output_schema.md          # 输出格式规范
│   └── api_reference.md          # API 接口参考
├── scripts/
│   ├── _auth.py                  # CSK 签名认证
│   ├── _http.py                  # 1688 网关 HTTP 客户端
│   ├── _errors.py                # 异常定义
│   ├── _const.py                 # 常量配置
│   ├── _tracker.py               # 埋点打点
│   └── capabilities/
│       ├── shop_bind_process/    # 绑店流程
│       ├── shop_info/            # 店铺信息查询
│       └── browser/              # 浏览器操作
```
