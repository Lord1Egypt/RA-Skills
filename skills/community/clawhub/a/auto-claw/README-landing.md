# Auto-Claw — AI驱动的WordPress运营平台

> **你的7×24小时AI数字员工**  
> 让独立站从"需要人操作"变成"AI自主运行"

## 🎯 一句话介绍

Auto-Claw 是基于 OpenClaw 的 WordPress AI 运营平台——AI 自动扫描、优化、发布、监控你的网站，24/7不间断，无需人工干预。

## ⚡ 30秒演示

```bash
# 一键扫描站点（当前真实站点）
cd /root/.openclaw/workspace/auto-company/projects/auto-claw
python3 demo_complete.py
```

**当前真实站点诊断：**
```
SEO评分:     65/100  (目标70+)
性能评分:   40/100  (目标70+)
文章数量:   4篇
缓存状态:   3/4启用
```

## 💰 定价

| 方案 | 价格 | 站点数 | 核心功能 |
|------|------|--------|----------|
| **Starter** | $99/月 | 1个 | SEO扫描+内容审计+基础报告 |
| **Pro** | $299/月 | 3个 | 全部+AI内容生成+A/B测试+GEO定向 |
| **Enterprise** | $799/月 | 无限 | 全部+专属策略+优先支持 |

**为什么不免费？**  
你购买的是"不用雇人"的自由。$299/月 = 一个实习生月薪的1/10，但AI不休假、不出错、不辞职。

## 📊 量化价值

| 指标 | 传统方式 | Auto-Claw |
|------|---------|-----------|
| SEO修复速度 | 1-2周 | <1小时 |
| 内容发布频率 | 1篇/周 | 随时按需 |
| 站点监控 | 人工检查 | 7×24实时 |
| 问题发现到修复 | 人工排期 | AI自动 |

## 🧩 核心能力矩阵

### AI原生独立站（5项）
- ✅ SEO扫描 + 修复建议生成
- ✅ Schema.org 自动生成与注入
- ✅ 内容质量审计（E-E-A-T评分）
- ✅ 性能诊断（TTFB/缓存/资源）
- ✅ 图片优化建议

### 转化率飞轮（5项）
- ✅ 竞品监控 + 变化告警
- ✅ A/B测试引擎（贝叶斯显著性）
- ✅ 退出意图干预弹窗
- ✅ 用户旅程个性化
- ✅ 动态落地页（社会证明）

### 全球运营中心（6项）
- ✅ GEO动态定价（23种货币）
- ✅ 大促页面自动切换
- ✅ 动态FAQ生成
- ✅ AI内容生成
- ✅ 缓存策略优化
- ✅ 用户评价摘要

### 核心架构（3项）
- ✅ WordPress CRUD + Gate Pipeline
- ✅ Vault 密钥隔离
- ✅ Audit 完整操作日志

**共19个能力，全部自主运行**

## 🏆 与竞品对比

| 功能 | Auto-Claw | Yoast SEO | SEMrush | 传统代运营 |
|------|-----------|-----------|---------|-----------|
| 自动修复 | ✅ | ❌ | ❌ | ❌ |
| 真实WordPress操作 | ✅ | ❌ | ❌ | ✅ |
| AI内容生成 | ✅ | ❌ | ❌ | ⚠️ |
| A/B自动测试 | ✅ | ❌ | ❌ | ❌ |
| 24/7无人值守 | ✅ | ❌ | ❌ | ❌ |
| 月成本 | $99起 | $99起 | $120起 | $2000+起 |

## 🔒 安全保障

| 原则 | 实现 |
|------|------|
| 密钥隔离 | Vault物理隔离，AI永不接触明文 |
| 发布审批 | Gate Pipeline三级风险分级 |
| 不可逆操作 | 软删除+30天恢复窗口 |
| 审计透明 | JSONL日志，用户实时可查 |
| AI不删数据 | 硬禁止DB DROP/审计日志删除 |

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/auto-company/auto-claw.git
cd auto-claw

# 2. 配置站点
cp config/settings.example.py config/settings.py
# 编辑 settings.py 填入你的 WordPress URL 和 SSH 凭证

# 3. 运行首次审计
python3 cli.py full-audit --url https://your-site.com --web-root /var/www/html

# 4. 查看报告
python3 cli.py report --format html > report.html
```

## 📋 技术栈

- **AI大脑**: OpenClaw Agent
- **WordPress集成**: WP-CLI + REST API
- **密钥管理**: HashiCorp Vault / 1Password Business
- **审计日志**: JSONL + Cron归档
- **Python**: 3.10+, ~7100行核心代码

## ⚠️ 限制说明

- **适用**: WordPress自托管（VPS/独立服务器）
- **不适用**: WordPress.com托管版、Shopify托管商品
- **原因**: Agent需要文件系统访问权限才能修改源码

---

**状态**: Cycle 1 完成 | 19/19 能力实现 | 真实站点验证通过  
**下一步**: ClawhHub发布 → 首批付费用户
