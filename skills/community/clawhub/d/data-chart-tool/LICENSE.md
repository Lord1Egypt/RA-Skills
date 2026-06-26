# 许可证系统使用指南

## 概述

data-chart-tool v1.1.0+ 引入了许可证机制，基础功能免费，高级功能（散点图）需要付费许可证。

## 许可证结构

许可证是一个签名的 JSON 文件，包含以下字段：

```json
{
  "license_key": "DCT-PREMIUM-001",
  "issued_to": "user@example.com",
  "skills": ["data-chart-tool"],
  "plan": "premium",
  "issued_at": "2026-03-22T18:13:17+00:00",
  "expires_at": "2027-03-21T18:13:17+00:00",
  "algorithm": "sha256",
  "signature": "..."
}
```

## 购买流程

1. **付款**：扫描下方收款码（微信/支付宝）支付 ¥99
   - 收款码：[预留]

2. **联系**：通过 OpenClaw 或 GitHub 发送付款凭证

3. **获取许可证**：我会生成并发送 `license.json` 文件

4. **安装**：
   ```bash
   # 复制许可证到用户目录
   mkdir -p ~/.data-chart-tool
   cp /path/to/license.json ~/.data-chart-tool/license.json
   ```

5. **配置密钥**：设置环境变量（密钥会随许可证发送）
   ```bash
   export SKILL_LICENSE_SECRET="your-secret-key"
   # 添加到 ~/.bashrc 或 ~/.zshrc 以持久化
   ```

6. **使用付费功能**：
   ```bash
   python source/data_visualizer.py -i data.csv -t scatter --x-col x --y-col y --license ~/.data-chart-tool/license.json
   ```

## 验证和管理

### 验证许可证
```bash
python3 skills/shared/license_manager.py verify --file ~/.data-chart-tool/license.json --secret $SKILL_LICENSE_SECRET
```

### 生成许可证（管理员用）
```bash
python3 skills/shared/generate_license.py \
  --secret "your-admin-secret" \
  --user "customer@example.com" \
  --plan premium \
  --skills data-chart-tool \
  --duration 365 \
  --output license.json \
  --key "DCT-CUSTOM-001"
```

## 免费 vs 付费功能

| 功能 | 免费版 | 付费版 |
|------|--------|--------|
| 柱状图 | ✅ | ✅ |
| 折线图 | ✅ | ✅ |
| 饼图 | ✅ | ✅ |
| 面积图 | ✅ | ✅ |
| **散点图** | ❌ | ✅ |
| 批量导出（无限制） | 有限制 | ✅ |
| 优先支持 | ❌ | ✅ |
| 未来新图表 | ❌ | ✅ |

## 常见问题

**Q: 许可证可以转卖吗？**
A: 不可以。许可证与购买者绑定。

**Q: 过期后怎么办？**
A: 当前版本许可证永久有效（一次性付费）。未来可能推出订阅制。

**Q: 可以在多台机器上使用吗？**
A: 可以，个人使用不限设备数量。

**Q: 丢失了许可证文件怎么办？**
A: 联系我，凭付款凭证重新签发。

**Q: 如何卸载许可证？**
A: 删除 `~/.data-chart-tool/license.json` 文件即可。

**Q: 批量部署（企业）？**
A: 企业授权需要单独洽谈，请直接联系。

## 技术细节

- 验证方式：HMAC-SHA256 签名，离线验证无需服务器
- 签名密钥：由管理者持有，随许可证发放给用户（`SKILL_LICENSE_SECRET`）
- 缓存：验证结果会缓存，无需每次调用都验证

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| "Signature mismatch" | 密钥错误或文件损坏 | 检查 `SKILL_LICENSE_SECRET` 环境变量 |
| "License expired" | 过期 | 联系续期 |
| "Skill not in license" | 许可证未包含此技能 | 请求包含该技能的许可证 |
| "License file not found" | 文件路径错误 | 检查 `--license` 参数或默认路径 |
