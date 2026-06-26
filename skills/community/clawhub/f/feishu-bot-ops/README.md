# feishu-bot-ops

飞书（Feishu/Lark）机器人运维大全 — Hermes Agent 社区 Skill。

## 覆盖内容

- **20+ 故障场景**：飞书不回复、@ 不生效、消息丢失、bot 间通信失败、会话串线、卡片回调报错
- **完整诊断流程**：一键诊断命令 + 一键修复命令
- **环境变量速查**：FEISHU_GROUP_POLICY、FEISHU_REQUIRE_MENTION、FEISHU_ALLOW_BOTS、FEISHU_AT_MAP、GATEWAY_ALLOW_ALL_USERS
- **@mention 深入**：`\b` 边界匹配中文 bug、AT_MAP 代码回归陷阱、API 反查验证
- **Bot 间通信**：双向配置食谱 + 排查 checklist
- **会话串线修复**：gateway_auto_continue_freshness + session_reset 参数组合
- **安全运维**：安全重启、锁文件清理、多实例冲突、lark-oapi 依赖修复
- **API 调试**：飞书 Open API 查群成员、反查消息、认证错误码速查
- **一键恢复脚本**：`scripts/feishu-gateway-recover.sh`

## 安装

```bash
# 克隆到 skills 目录
mkdir -p ~/.hermes/skills/feishu/
git clone <repo-url> ~/.hermes/skills/feishu/feishu-bot-ops/

# 或手动复制 SKILL.md + scripts/ 过去
```

## 一键恢复脚本

```bash
bash ~/.hermes/skills/feishu/feishu-bot-ops/scripts/feishu-gateway-recover.sh
```

使用前请确保 `~/.hermes/.env` 中已配置 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`。

## 适用场景

- 飞书 bot 刚开始接入，需要了解平台约束和常见坑
- bot 突然不回复了，需要快速定位
- 多 bot 协作，需要互相 @
- 群聊中上下文混乱，bot 执行错误任务

## 贡献

此 Skill 基于 RONVUE 团队的生产环境运维经验总结。欢迎提 Issue/PR 补充新场景。

## License

MIT
