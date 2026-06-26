# 电商运营套装 - 快速上手指南

## 🚀 5分钟快速开始

### 1. 安装套装

```powershell
git clone https://github.com/clawhub/ecommerce-bundle.git
cd ecommerce-bundle
./install.ps1
```

### 2. 配置店铺信息

```powershell
cp config/competitors.yaml.template config/competitors.yaml
notepad config/competitors.yaml
```

### 3. 开始运营

```
openclaw run ecommerce --config ./config
```

---

## 📋 常用命令速查

| 命令 | 功能 |
|------|------|
| `监控竞品价格` | 设置竞品监控 |
| `查看评价` | 评价监控报告 |
| `分析这个品类` | 选品分析 |
| `设置自动回复` | 配置客服话术 |
| `今日运营数据` | 数据汇总 |

---

## 🔧 故障排除

### 监控失败
- 检查目标网站是否可访问
- 确认反爬策略
- 调整监控频率

### 自动回复不触发
- 检查关键词配置
- 确认平台连接
- 查看日志排查

---

**开始你的智能电商运营！** 🛒
