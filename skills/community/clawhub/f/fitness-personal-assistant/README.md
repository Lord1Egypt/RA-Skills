---
name: fitness-personal-assistant
description: 一体化健身追踪系统。自动同步饮食记录和身体状态到 intervals.icu。支持配置引导和错误处理。
allowed-tools:
  - Bash
  - Python
---

# 🏋️ Fitness Personal Assistant

Intervals.icu 数据同步工具 - **无需手动配置凭证**

---

## 🔧 OpenClaw 安装

```bash
openclaw skills install --from clawhub fitness-personal-assistant
```

首次使用时会自动引导输入 API 凭证，配置保存在技能目录的 `config/config.json`（已 gitignore）。

---

## 📝 使用示例

### 1️⃣ 查询身体状态报告

群里发送消息：
```
查看我的身体状态
今天的训练负荷怎么样？
我适合高强度训练吗？
```

或命令行：
```bash
cd ~/.openclaw/workspace/skills/fitness-personal-assistant/scripts
python3 body-status-reporter.py
```

**输出内容：**
- 竞技状态评分（基于 TSB、HRV、睡眠、静息心率）
- 训练负荷分析 + 深度解读
- 恢复指标详细分析
- 近 7 天训练记录
- 今日行动指南

---

### 2️⃣ 记录饮食摄入

自然语言输入：
```
早餐吃了两个鸡蛋和一片全麦面包
午餐吃了 200g 鸡胸肉和 250 克米饭
晚餐：300g 牛肉，不配菜
```

或指定日期：
```
今天早餐：一杯牛奶 + 一根香蕉
昨天晚餐：沙拉和烤三文鱼
```

指定餐次：
```
加餐：一勺蛋白粉
下午茶：希腊酸奶
```

系统自动识别：
- **时间**: 当前时刻（可用 `--date` 覆盖）
- **餐次**: 根据关键词判断（早餐/午餐/晚餐/加餐）
- **营养**: 中文食物规则库自动估算

---

### 3️⃣ 测试模式（不上传）

```bash
python3 meal-to-intervals.py --text "200g 牛肉" --dry-run
```

---

## 🎯 核心功能

✅ **配置文件不存在时自动引导创建**  
✅ **Athlete ID 格式验证**（必须以 `i` 开头）  
✅ **凭证实时验证**（保存前 test_connection）  
✅ **优雅的错误处理**（JSON 解析失败/字段缺失都引导重新配置）  
✅ **自然语言饮食记录**（中英文混合输入）  
✅ **职业级身体状态报告**（带深度解读和行动建议）  

---

## 🔐 安全说明

### API 凭证存储位置
- **路径**: `~/.openclaw/workspace/skills/fitness-personal-assistant/config/config.json`
- **权限**: `600` (仅所有者可读/写)
- **Git 状态**: ✅ 已忽略 (`gitignore`)，不会提交到 GitHub

### 网络请求白名单
- `https://intervals.icu/api/v1/*` (Wellness/Activities)
- `https://world.openfoodfacts.org/*` (Food nutritional data)

---

## 📚 引用资源

- [Intervals.icu API Integration Cookbook](https://forum.intervals.icu/t/intervals-icu-api-integration-cookbook/80090)
- [API access to Intervals.icu](https://forum.intervals.icu/t/api-access-to-intervals-icu/609)
- [Intervals.icu 官方文档](https://intervals.icu/api-docs.html)
