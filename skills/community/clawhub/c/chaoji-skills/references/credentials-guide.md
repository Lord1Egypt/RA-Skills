# 获取 ChaoJi API 凭证（AccessKey）

本指南帮助你获取使用 ChaoJi Skills 所需的 AccessKey ID（AK）和 AccessKey Secret（SK）。

## 前置条件：注册潮际汇账号

如果你还没有潮际汇账号，需要先完成注册：

1. 打开潮际汇平台：https://marketing.k-fashionshop.com/
2. 完成账号注册
3. 登录后进入**个人中心**，确认已设置账户名和密码

> 登录账号与密码与「潮际主设」或「好麦」平台相同。如未设置密码，请先在个人中心修改账户名、设置密码。

## 步骤一：打开密钥管理页面

访问 ChaoJi 开放平台密钥管理页：

https://idm.metac-inc.com/pages/dashboard/index

## 步骤二：开通 API 权限

API 权限需要联系官方客服开通。请点击以下链接添加企业微信客服：

https://work.weixin.qq.com/ca/cawcdea59e18fadda7

添加后告知客服需要开通 OpenAPI 权限，等待开通完成后再进行后续步骤。

## 步骤三：登录

使用你的潮际汇账号登录密钥管理页。

## 步骤四：生成新令牌

登录后，点击**生成新令牌**（或 Create AccessKey），系统会生成一组：

- **AccessKey ID**（AK）
- **AccessKey Secret**（SK）

> 请立即保存 SK，页面关闭后将无法再次查看。

## 步骤四：配置凭证

获取 AK/SK 后，选择以下任一方式配置：

### 方式 A：环境变量（推荐用于 CI 或临时使用）

```bash
export CHAOJI_AK="your_access_key_id"
export CHAOJI_SK="your_access_key_secret"
```

### 方式 B：凭证文件（推荐用于本地开发）

创建文件 `~/.chaoji/credentials.json`：

```json
{
  "access_key": "your_access_key_id",
  "secret_key": "your_access_key_secret"
}
```

设置文件权限（仅限本人读写）：

```bash
chmod 600 ~/.chaoji/credentials.json
```

## 验证

配置完成后，运行余额查询命令确认凭证有效：

```bash
python chaoji-tools/scripts/run_command.py --command remaining_quantity_of_beans --input-json '{}'
```

返回 `"ok": true` 即表示凭证配置成功。

## 常见问题

| 问题 | 解决方式 |
|------|----------|
| 没有潮际汇账号 | 先到 https://marketing.k-fashionshop.com/ 注册 |
| 忘记密码 | 在潮际汇平台「个人中心」重置密码 |
| SK 丢失 | 重新生成新令牌，旧令牌作废 |
| 凭证配置后仍报错 | 检查 AK/SK 是否有多余空格，文件路径是否正确 |
