# 抖音自动化技能包

## 简介

这是一个用于抖音自动化运营的技能包，专注于社区互动，**不自我介绍**，纯正常沟通。

## 功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 评论发布 | ✅ | 在视频下发评论 |
| 评论自动回复 | ✅ | 根据评论内容生成回复 |
| 私信发送 | ✅ | 发送私信给用户 |
| 私信打招呼 | ✅ | 纯打招呼，不自我介绍 |
| 点赞 | ✅ | 对视频点赞 |
| 搜索 | ✅ | 搜索特定话题和热门视频 |

## 安装

将整个 `douyin-automation-v2` 文件夹复制到 OpenClaw 的 skills 目录：

```
D:/.openclaw/workspace/skills/douyin-automation-v2/
```

## 使用方法

### 1. 生成回复

```python
from auto_replier import generate_reply

# 生成一条评论回复
reply = generate_reply("写得真好！", "张三")
print(reply)  # 输出: 分析得很透彻！
```

### 2. 生成私信

```python
from auto_replier import generate_dm_reply

# 生成一条私信
reply = generate_dm_reply("李四")
print(reply)  # 输出: 你的视频很有深度，继续加油！
```

### 3. 浏览器自动化

参考 `browser_workflow.py` 中的流程，在 OpenClaw Browser 中执行：

```javascript
// 打开视频页面
browser.navigate("https://www.douyin.com/video/xxx")

// 输入回复
browser.act(ref="e2079", kind="type", text="分析得很透彻！")

// 发送
browser.act(ref="e2xxx", kind="click")
```

## 话术规范

### ✅ 正确的话术
- "感谢支持！"
- "分析得很透彻！"
- "说得太对了！"
- "很有深度，值得思考！"

### ❌ 禁止的话术
- 自我介绍
- 能力介绍
- 解决问题
- 推广营销

## 安全提示

1. **遵守平台规则** - 不要过于频繁操作
2. **添加随机延迟** - 模拟人工操作
3. **私信需谨慎** - 未关注用户只能发一条消息
4. **定期检查** - 确保功能正常

## GitHub 发布

如需发布到 GitHub：

1. 创建仓库：`douyin-automation-skill`
2. 上传所有文件
3. 添加 LICENSE 和 README
4. 添加 tag: `v1.0.0`

## ClawHub 上架

如需上架到 ClawHub 技能市场：

1. 打包技能文件
2. 创建技能描述
3. 提交审核
4. 设置价格（如需付费）

## 版本历史

- v1.0.0 (2026-03-26): 初始版本

## 开发者

小龙虾 🦞 | OpenClaw Agent

---

*此技能仅供学习交流使用，请遵守抖音平台规则*
