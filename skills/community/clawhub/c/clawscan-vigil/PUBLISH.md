# ClawScan 发布指南

## 产品形态

**ClawScan** 以 OpenClaw Skill 形式分发，包含：
- 免费版：5次/月基础扫描
- Premium：无限扫描 + 依赖分析 + 批量扫描（¥49/年）

---

## 安装方式

用户通过以下命令安装：

```bash
clawhub install clawscan
```

安装后自动注册 `clawscan` CLI 命令。

---

## 发布准备

### 1. 清理和打包

```bash
# 清理缓存
rm -rf core/__pycache__ tests/__pycache__
rm -rf build/ dist/ *.egg-info

# 创建发布包
mkdir -p clawscan-skill
cp -r core cli.py pyproject.toml README.md skill/ clawscan-skill/
rm -rf clawscan-skill/core/__pycache__

# 打包
tar -czf clawscan-v0.2.0.tar.gz clawscan-skill/
```

### 2. 发布到 ClawHub

```bash
# 注册 ClawHub 账号
# https://clawhub.ai/signup

# 登录
clawhub login

# 发布
clawhub publish clawscan-v0.2.0.tar.gz
```

### 3. 设置付费（可选）

ClawHub 目前不支持内置支付，付费通过以下方式实现：

**方案A：自建支付**
- 搭建简单的 license 生成服务
- 用户购买后通过 `clawscan activate KEY` 激活
- License 格式验证本地完成

**方案B：第三方平台**
- 在 爱发电 / 面包多 等平台销售
- 手动发放 License key
- 用户自行激活

---

## 定价策略

| 方案 | 价格 | 包含内容 |
|------|------|----------|
| 免费 | ¥0 | 5次/月基础扫描 |
| 个人版 | ¥49/年 | 无限扫描 + 依赖分析 |
| 团队版 | ¥199/年 | 批量扫描 + 5个 License |

---

## 推广渠道

### 小红书（优先级最高）
- 发布教程笔记：《安装Skill前必做安全检查》
- 对比图：扫描前后的风险发现
- 引流到个人网站或 GitHub

### V2EX
- 发布 Show 节点：独立开发者作品
- 技术贴：如何检测恶意 OpenClaw Skill

### 即刻
- AI 创作者圈子分享
- 效率工具推荐

### GitHub
- 开源核心代码（MIT）
- Premium 功能闭源
- 吸引贡献和 Star

---

## 变现验证指标

**MVP 阶段目标（1个月）**:
- [ ] 100+ 安装量
- [ ] 5+ Premium 付费用户
- [ ] 回收开发时间成本

**健康指标**:
- 免费→付费转化率 > 3%
- 用户留存率 > 30%（次月仍使用）
- NPS > 40

---

## 后续迭代

**v0.3.0**:
- [ ] CI/CD 集成插件
- [ ] 邮件/Slack 风险告警
- [ ] 规则库自动更新

**v1.0.0**:
- [ ] 企业版（SSO、审计日志）
- [ ] SaaS 化（Web 界面）
- [ ] 社区风险情报共享

---

## 技术债务

- [ ] 添加完整单元测试
- [ ] 优化动态分析沙箱
- [ ] 支持更多语言（JS/TS Skill）
- [ ] Windows 兼容性测试
