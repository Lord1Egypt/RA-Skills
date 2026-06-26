# AEP 凭证配置指引（给 agent 看）

本文档给 agent 使用，**不要让用户直接编辑任何文件或设置环境变量**，所有持久化动作由 agent 后台完成。

## 工作流

### Step 1 · 启动前自检

每次接到查询请求，先跑：

```bash
python3 scripts/search_news.py --check-config
```

返回 JSON（通过 `configured` 字段判断状态，不看进程退出码）：

- `configured: true` → 凭证就位，直接走查询流程
- `configured: false` → 进入 Step 2

### Step 2 · 引导用户提供凭证

对用户说：

> 使用外贸资讯查询需要 AEP 凭证。请到 https://tools.mentarc.cn/aim-skills/ 注册获取 AEP_AUTHORIZATION（Bearer token），然后把凭证粘到对话框里发给我，我会帮你配好。

**不要**让用户自己编辑文件或设置环境变量。

### Step 3 · 持久化凭证

将凭证写入 skill 目录下的 `.env` 文件：

```
AEP_AUTHORIZATION=<用户提供的token>
```

只需填写 token 值，脚本会自动补全 `Bearer` 前缀。

### Step 4 · 验证

写入后重新执行自检：

```bash
python3 scripts/search_news.py --check-config
```

确认 `configured: true` 后，继续执行用户原请求。

## 禁止事项

1. **禁止把凭证写入 git 跟踪的文件** — 只能写入 `.env`（已 gitignore）
2. **禁止要求用户自己编辑文件** — 凭证由 agent 帮用户落盘
3. **禁止跨 agent 读凭证** — 不同 agent 可能使用不同的 AEP 账号
