# lark-cli 安装与认证

本文档说明如何安装和配置 lark-cli，使 skill 获得飞书文档读写能力。

## 前置条件

- Node.js 环境（用于 npm/npx）
- 飞书账号

## 安装步骤

### 1. 安装 CLI

```bash
npm install -g @larksuite/cli
```

### 2. 安装 Skills

```bash
npx skills add https://github.com/larksuite/cli -y -g
```

这会安装 19 个飞书 Agent Skills，覆盖日历、消息、文档、表格等 11 个业务域。

### 3. 初始化配置

```bash
lark-cli config init
```

这是一个交互式引导流程：
- 选择语言（中文/英文）
- 选择一键配置应用
- 选择飞书版本（国内版飞书 / 国际版 Lark）
- 扫码授权

### 4. 登录授权

```bash
lark-cli auth login --recommend
```

`--recommend` 会自动选择常用权限范围。

### 5. 验证状态

```bash
lark-cli auth status
```

成功输出应显示已登录的身份和权限列表。

## 检测 lark-cli 是否可用

在 skill 的 preflight 阶段：

```bash
# 检查 lark-cli 是否已安装
which lark-cli 2>/dev/null && echo "installed" || echo "not_installed"

# 检查认证状态
lark-cli auth status 2>&1
```

## 自动修复流程

如果 lark-cli 未安装或未认证，按以下顺序尝试修复：

### 情况 1：lark-cli 未安装
```bash
npm install -g @larksuite/cli
npx skills add https://github.com/larksuite/cli -y -g
```
安装后提示用户运行 `lark-cli config init` 完成交互式配置。

### 情况 2：已安装但未配置
提示用户运行：
```bash
lark-cli config init
```
此步骤需要用户扫码，无法自动完成。

### 情况 3：已配置但未登录
```bash
lark-cli auth login --recommend
```
此步骤可能需要用户在浏览器中确认授权。

### 情况 4：已登录但缺少特定权限
lark-cli 的错误信息会指导下一步，例如：
```
Error: 缺少权限 "docs:doc:readonly"
修复命令：lark-cli auth login --scope "docs:doc:readonly"
```
按错误提示的命令补充权限即可。

## 身份选择

| 场景 | 推荐身份 |
|------|----------|
| 访问用户自己的飞书文档 | `--as user` |
| 追加到用户自己的飞书文档 | `--as user` |
| 企业级自动化工作流 | `--as bot` |

本 skill 默认使用 `--as user`，除非用户明确要求使用 bot。

## 本 skill 常用命令

| 操作 | 命令 |
|------|------|
| 读取文档内容 | `lark-cli docs +fetch --doc "<doc_url>" --as user` |
| 搜索文档 | `lark-cli docs +search --keyword "<keyword>" --as user` |
| 追加内容到文档 | `lark-cli docs +update --doc "<doc_url>" --mode append --body "<markdown>" --as user` |
| 覆盖文档内容 | `lark-cli docs +update --doc "<doc_url>" --mode replace --body "<markdown>" --as user` |
