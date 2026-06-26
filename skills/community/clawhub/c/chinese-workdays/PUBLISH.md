# Chinese Workdays Skill - ClawHub 发布说明

## 📦 已打包文件

```
/root/.openclaw/workspace/skills/dist/chinese-workdays.skill
```

## 🚀 发布步骤

### 1. 登录 ClawHub

```bash
clawhub login
```

这会打开浏览器进行认证。按照提示完成登录。

### 2. 发布技能

```bash
cd /root/.openclaw/workspace/skills
clawhub publish ./dist/chinese-workdays.skill \
  --name "Chinese Workdays Calculator" \
  --slug "chinese-workdays" \
  --version "1.0.0" \
  --changelog "Initial release with 2026 official holiday data (国办发明电〔2025〕7号)" \
  --tags "utility,china,holidays,working-days" \
  --price 1.00
```

### 3. 验证发布

```bash
clawhub inspect chinese-workdays
```

## 💰 定价信息

- **价格**: $1.00 美元
- **定价策略**: 一次性购买，永久使用
- **包含**: 2026-2027年节假日数据，未来可手动更新

## 📝 技能详情

- **名称**: Chinese Workdays Calculator
- **Slug**: chinese-workdays
- **版本**: 1.0.0
- **许可**: MIT
- **描述**: 基于中国国务院官方节假日安排，精确计算法定工作日

## 🔧 前置要求

用户需要：
1. 安装 skill: `clawhub install chinese-workdays`
2. Python 3.11+ (标准库)
3. PyYAML (依赖): `pip install pyyaml`

## 📋 更新计划

- 每年12月自动更新下一年度节假日数据（通过定时任务）
- 支持更多年份的历史数据

## ⚠️ 注意事项

1. **数据准确性**: 当前2026年数据基于国务院官方通知，但较小概率可能有调整
2. **时区**: 使用 Asia/Shanghai 时区
3. **适用范围**: 仅适用于中国大陆地区

## 📞 支持

如有问题，请访问 https://clawhub.com 或联系技能发布者

---

**Ready to publish!** 🎉