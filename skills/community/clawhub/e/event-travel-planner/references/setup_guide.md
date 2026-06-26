# 环境配置指南

工具不可用、认证失效、或用户要求配置环境时，按本文档操作。

---

## Step 1：运行自动配置脚本

脚本会自动检测已安装的工具、安装缺失的依赖、检测认证状态，全程无需用户交互：

```bash
bash scripts/setup.sh
```

脚本执行流程：
1. **阶段 1**：检测已安装的工具（优先检查，已安装则跳过系统依赖检查）
2. **阶段 2**：安装缺失的工具（xhs-cli 需要 Python >= 3.10 + uv/pipx，flyai-cli 需要 Node.js >= 16）
3. **阶段 3**：检测配置状态（xhs 认证、flyai API Key）

脚本结束时会输出 `── NEXT_STEPS ──` 结构化摘要，根据 `STATUS` 判断下一步：

| STATUS | 含义 | Agent 动作 |
|--------|------|-----------|
| `ALL_READY` | 所有工具已安装且已认证 | 跳到"执行前检查"，可直接使用 |
| `XHS_AUTH_NEEDED` | xhs-cli 已安装但未认证 | 进入 Step 2 完成认证 |
| `NONE_READY` | 所有工具都未安装 | 查看"待解决问题"，协助用户修复依赖后重新运行脚本 |
| `PARTIAL` | 部分工具未就绪 | 查看具体标记和配置引导，按需处理 |

详细状态标记：
- `XHS_INSTALLED=yes/no` — xhs-cli 安装状态
- `XHS_AUTH=yes/no` — xhs-cli 认证状态
- `FLYAI_INSTALLED=yes/no` — flyai-cli 安装状态

## Step 2：配置小红书 Cookie（xhs-cli 认证）

如果脚本输出 `XHS_AUTH_NEEDED=yes`，需要引导用户完成 xhs-cli 认证。

**方式 A：浏览器 Cookie 提取（推荐）**

适用场景：用户在电脑浏览器中已登录过小红书。

```bash
# 1. 请用户确认已在浏览器中登录 https://www.xiaohongshu.com
# 2. 执行登录（自动检测浏览器）
xhs login
# 或指定浏览器：xhs login --cookie-source chrome
# 3. 验证
xhs status
```

**方式 B：二维码扫码登录**

适用场景：浏览器 Cookie 提取失败、或用户只有手机登录。

```bash
# 1. 执行二维码登录
xhs login --qrcode
# 2. 终端显示二维码，请用户用小红书 App 扫码
# 3. 验证
xhs status
```

**验证认证成功：**

```bash
xhs status --yaml | grep "authenticated: true"
xhs whoami --yaml | grep "nickname"
```

> **Cookie 有效期约 7 天。** 过期后重新执行 `xhs login` 即可。

## Step 3：配置飞猪 API Key（可选）

flyai-cli **无需 API Key 即可使用**，但配置后可获得增强搜索结果。

如果脚本提示未配置 API Key，且用户希望配置：

```bash
# 1. 访问官网获取 API Key
# https://flyai.open.fliggy.com/console
# 2. 配置
flyai config set FLYAI_API_KEY "your-api-key"
```

> 没有 API Key 不影响正常使用，可以跳过此步骤。
