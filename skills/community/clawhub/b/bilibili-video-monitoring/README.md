# bilibili 视频监控 Skill

> 自动监控 B站 UP主投稿数据，生成周报并通过微信 + Agent Mail 双通道推送。采用 Apache-2.0 协议开源。
> SkillHub Slug：`bibili-video-monitoring`

> ⚠️ **隐私提醒**：本仓库**不包含任何真实 Cookie 文件**。请在你自己的机器上创建 `bilibili_cookie.txt` 并填入你的 B站 Cookie；切勿将该文件提交到任何公开仓库。

## ✨ 功能

- 🔐 读取 B站 Cookie，通过内置 **WBI 签名算法** 验证身份（无需额外依赖）
- 📹 获取 UP主最新投稿列表（默认 UID 请在 `bibili_weekly.js` 中配置）
- 📊 统计每支稿件的播放、点赞、收藏、分享、评论数据
- 💬 获取最新 3 个视频的高赞评论（TOP5）
- 📄 生成结构化文字报告
- 📲 双通道自动推送（微信 + Agent Mail）

## 📂 文件结构

```
bilibili-video-monitoring/
├── SKILL.md            # Skill 定义文件
├── bibili_weekly.js    # 主执行脚本（Node.js）
├── bilibili_wechat_push.js  # 微信推送联动脚本
├── bilibili_cookie.txt # Cookie 配置模板（需自行创建，切勿提交真实值）
└── README.md           # 本文件
```

## 🚀 快速开始

### 第一步：配置 Cookie

在本目录**自行创建** `bilibili_cookie.txt`，填入你的 B站 Cookie 值：

```
SESSDATA=你的SESSDATA值
bili_jct=你的bili_jct值
DedeUserID=你的DedeUserID
DedeUserID__ckMd5=你的DedeUserID__ckMd5值
```

**获取方式：**
1. 浏览器登录 https://www.bilibili.com
2. 按 `F12` 打开开发者工具
3. 进入 **Application → Cookies → https://www.bilibili.com**
4. 找到上述四个字段，复制对应值填入

> ⚠️ Cookie 有效期约 30 天，过期后脚本会提示"Cookie 失效"，需重新获取并更新文件。Cookie 为敏感信息，请勿分享或提交到公开仓库。

### 第二步：配置 UP主 UID

编辑 `bibili_weekly.js` 顶部的：

```js
const UID = 'YOUR_BILIBILI_UID'; // 改为你要监控的 UP主 UID
```

### 第三步：手动运行测试

```bash
node bibili_weekly.js
```

运行后自动完成：
1. ✅ 验证 Cookie 有效性
2. 📹 拉取最新投稿数据
3. 💬 获取高赞评论
4. 📄 生成报告写入 `./bilibili_report.txt`
5. 📲 （若由 Skill 调用）自动双通道推送

### 第四步：接入 WorkBuddy 自动化

可通过 WorkBuddy 自动化功能配置每周定时运行，实现完全无人值守的周报推送。

示例使用场景：每周六 10:00 自动运行并推送。

## 📲 双通道推送说明

| 通道 | 实现方式 | 推送目标 |
|------|----------|----------|
| 通道1 | 微信 PC 端自动控制 Skill | 微信联系人（在 `bilibili_wechat_push.js` 中配置 `YOUR_WECHAT_CONTACT`） |
| 通道2 | agently-mail Skill（agently-cli，两阶段确认） | 你的 Agent Mail 地址（请在配置中填写） |

> 使用前需确保：
> - 微信 PC 端已登录（微信 Windows 客户端）
> - agently-cli 已完成 `auth login`（Agent Mail 已授权）

## 📊 报告内容示例

```
🦞 B站每周播报
UP主：YOUR_BILIBILI_NAME
数据周期：本周
─────────────────────
📹 投稿概览（共 2 个视频）

▎【视频标题】
  BV号：BV1xx411x7xx
  发布时间：2026-04-20
  播放：12.3万 | 点赞：8456 | 收藏：2345 | 分享：876 | 评论：1234

  💬 高赞评论 TOP5：
    1. 评论内容示例...
       👍 1234
    ...

─────────────────────
📊 本周合计
  总播放：XXX | 总点赞：XXX | 总评论：XXX

Powered by WorkBuddy 🦞
```

## 🔧 依赖要求

| 依赖 | 说明 |
|------|------|
| Node.js | 建议使用系统 PATH 中的 `node` |
| WBI 签名 | 内置在脚本中，无需额外安装 |
| 微信 PC 端自动控制 Skill | 用于通道1推送 |
| agently-mail Skill | 用于通道2推送（Agent Mail） |

## ⚠️ 注意事项

1. **Cookie 安全**：Cookie 为敏感信息，请勿分享给他人，切勿提交到公开仓库
2. **Cookie 过期**：约 30 天后需重新获取，脚本会自动检测并提示
3. **无 npm 依赖**：脚本纯 Node.js 实现 WBI 签名，无需 `npm install`
4. **报告文件路径**：默认写入 `./bilibili_report.txt`

## 🐛 常见问题

**Q：脚本报错"Cookie 失效"**
→ Cookie 已过期，重新获取并填入 `bilibili_cookie.txt`

**Q：推送没有收到**
→ 检查微信是否登录、agently-cli 是否已完成 auth login（Agent Mail 授权）

**Q：能监控其他 UP主吗**
→ 修改 `bibili_weekly.js` 中的 `const UID` 为目标 UP主 UID

## 📜 更新日志

### v1.0.0（2026-04-27）
- ✅ 初始版本，提交 SkillHub 审核
- ✅ Slug：`bibili-video-monitoring`
- ✅ 内置 WBI 签名算法，无额外依赖
- ✅ 双通道推送（微信 + 邮箱）
- ✅ 适配 WorkBuddy Skill 规范

### v1.1.0（2026-07-17）
- ✅ 推送通道2 由「QQ邮箱」替换为「Agent Mail（agently-mail Skill）」
- ✅ 引入 Agent Mail 两阶段确认安全机制：发信前展示摘要，用户确认后发出
- ✅ 微信通道保持不变
- ✅ 自动化定时任务默认走微信无感推送；Agent Mail 作为用户主动索取时的确认发送通道

## 📄 许可证

Apache License 2.0 — 可自由使用、修改、分发。详见 [LICENSE](LICENSE) 文件。

---

**作者**：微光浮影
**SkillHub**：https://skillhub.cn/skills/bilibili-video-monitoring
