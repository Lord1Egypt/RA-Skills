# ClawHub 登录指南

## 方式1: 浏览器登录（推荐）

刚才的命令应该已经打开了浏览器：
https://clawhub.ai/cli/auth

如果浏览器没有自动打开，请：
1. 手动访问上面的链接
2. 登录你的ClawHub账号
3. 授权CLI访问

---

## 方式2: 手动登录

如果浏览器登录失败，可以手动输入token：

1. 访问: https://clawhub.com/settings/tokens
2. 创建新的API token
3. 复制token
4. 运行: `clawhub login --token YOUR_TOKEN`

---

## 方式3: 直接发布（不推荐）

如果只是想测试，可以尝试：

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\agency-agents-caller
clawhub publish . --dry-run
```

---

## 当前状态

- ❌ 浏览器登录超时
- ⏳ 需要手动登录或提供token
- ⏳ 技能包已准备好，等待发布

---

## 技能包位置

```
C:\Users\Administrator\.openclaw\workspace\skills\agency-agents-caller
```

---

## 下一步

请选择以下一种方式：

1. 重新运行 `clawhub login` 并在浏览器中完成登录
2. 访问 https://clawhub.com/settings/tokens 获取token
3. 告诉我你的ClawHub token，我帮你发布

登录成功后，我会继续发布流程。
