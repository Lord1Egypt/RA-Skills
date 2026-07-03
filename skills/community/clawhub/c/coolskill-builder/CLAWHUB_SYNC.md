# ClawHub 同步指南

## 当前状态

| 项目 | 状态 |
|------|------|
| GitHub 仓库 | ✅ 已创建并同步 |
| GitHub Topics | ✅ 10 个标签已添加 |
| 双语 README | ✅ 已推送 |
| ClawHub CLI | ✅ 已安装 |
| ClawHub 认证 | ⏳ 需你在浏览器中确认一次 |
| ClawHub 发布 | ⏳ 认证后一键完成 |

---

## 2 步完成 ClawHub 同步

### Step 1: 浏览器授权（30 秒）

点击或复制以下链接到浏览器打开：

👉 **https://clawhub.ai/cli/device?code=FU9D-UVEH**

然后点击 **"Sign In"** 按钮，用你的 GitHub 账号登录并授权。

> 这个授权码 15 分钟内有效。如果过期了，运行下面的命令获取新码：
> ```bash
> clawhub login --device
> ```

### Step 2: 发布 Skill（10 秒）

授权完成后，回到这里运行：

```bash
clawhub skill publish /mnt/agents/output/coolskill-builder \
  --slug coolskill-builder \
  --name "CoolSkill Builder" \
  --version 1.0.0 \
  --changelog "Initial release: zero-dependency skill forge with 5-layer security" \
  --tags latest
```

成功后会看到类似输出：
```
✔ Published coolskill-builder@1.0.0
  URL: https://clawhub.ai/fredtai/coolskill-builder
```

---

## 验证发布

```bash
# 查看已发布的 skill
clawhub inspect coolskill-builder

# 在 ClawHub 上查看
open https://clawhub.ai/fredtai/coolskill-builder
```

---

## 后续更新版本

当你更新 skill 后，只需：

```bash
# 1. 更新版本号
# 修改 SKILL.md 中的 version 字段

# 2. 推送到 GitHub
git add . && git commit -m "feat: v1.0.1 update" && git push

# 3. 发布到 ClawHub
clawhub skill publish . \
  --slug coolskill-builder \
  --version 1.0.1 \
  --changelog "Fix: ..." \
  --tags latest
```
