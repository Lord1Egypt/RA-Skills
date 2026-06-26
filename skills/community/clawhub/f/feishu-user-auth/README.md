# feishu-user-auth

`feishu-user-auth` 是飞书用户授权 skill。它只做一件事：通过浏览器完成一次飞书 OAuth，把用户级 token 缓存在本机，供后续多维表同步直接复用。

## 这个 skill 能做什么

- 打开浏览器进入飞书授权页
- 通过本地回调地址接收授权码
- 换取并缓存 `user_access_token + refresh_token`
- 给 `feishu-bitable-sync` 提供用户身份写表能力

## 安装

### 基础依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 必需环境变量

```bash
export FEISHU_APP_ID=...
export FEISHU_APP_SECRET=...
```

### 回调地址要求

- 飞书应用已开通网页应用能力
- 飞书应用回调地址包含 `http://127.0.0.1:14578/callback`

## 输入和输出

**输入**

- 任意一个 Markdown 请求文件即可，通常直接传 `wechat-report` 结果路径也行

**输出**

- `content-production/published/YYYYMMDD-feishu-user-auth.md`
- 本机缓存：`~/.codex/feishu-auth/content-system-sync.json`

## 使用方法

### 单独运行

```bash
.venv/bin/python -m skill_runtime.cli run-skill feishu-user-auth \
  --input content-production/inbox/20260407-harness-engineering-wechat-report.md
```

## 什么时候用

- 第一次准备把公众号报告同步到飞书时
- 之前的用户 token 已失效，需要重新授权时
- 你想避免一直用租户身份直写多维表时

## 注意事项

- 这是一次性授权 skill，不负责实际同步内容
- 授权成功后，再运行 `feishu-bitable-sync`
- 如果浏览器打不开或回调地址没配好，本 skill 会失败并在回执里写原因

## 相关文件

- [SKILL.md](./SKILL.md)
- [runtime.py](./runtime.py)
- [feishu_auth.py](../../skill_runtime/feishu_auth.py)
