---
name: fitness-personal-assistant
description: 一体化健身追踪系统。自动同步饮食记录和身体状态到 intervals.icu。支持配置引导和错误处理。
allowed-tools:
  - Bash
  - Python
---

# 🏋️ Fitness Personal Assistant（Python 重构版）

一体化健身追踪系统，集成**饮食记录 + 身体状态报告 + 训练分析**。数据自动同步到 intervals.icu，隐私优先，本地处理。

---

## 🎯 功能概览

### 🍽️ 智能饮食记录
- **自然语言输入**: 直接说中文即可，如"早餐吃了两个鸡蛋和全麦面包"
- **自动营养计算**: 中文食物规则库 + 智能估算
- **多餐次识别**: 自动判断早餐/午餐/晚餐/加餐
- **实时同步**: 写入 intervals.icu wellness 数据
- **累计更新**: 自动累加同一天的多餐数据

### 💪 身体状态监控
- **训练负荷**: CTL/ATL/TSB 疲劳度监测
- **恢复指标**: HRV、静息心率、睡眠评分
- **AI 建议**: 根据 TSB 值给出训练/休息指导
- **详细训练记录**: 显示最近 5 次训练的时长/距离/卡路里

### 📊 可视化报告
- Markdown 格式自动生成
- 趋势分析
- Apple Notes / Obsidian 导出支持

---

## 🚀 快速开始

### 1️⃣ 准备 intervals.icu 账号

注册地址：https://intervals.icu/register  
免费版即可，付费版解锁更多高级功能。

### 2️⃣ 获取 API 凭证

1. 登录 intervals.icu
2. 进入 Settings → API Keys
3. 复制你的 `Athlete ID` 和 `API Key`

示例（**注意替换为你的真实凭证**）：
```
Athlete ID: iXXXXXXXXX
API Key: YOUR_INTERVALS_ICU_API_KEY_HERE
```

⚠️ **安全提示**: 
- 永远不要将真实 API Key 提交到 Git
- 使用 `.env` 文件或环境变量管理密钥
- 示例中的 `iXXXXXXXXX` 和 `YOUR_INTERVALS_ICU_API_KEY_HERE` 为占位符

### 3️⃣ 配置凭证（可选）

工具会在首次运行时**自动引导你创建配置文件**。

**默认存储路径:** `~/.openclaw/workspace/skills/fitness-personal-assistant/config/`  
**可自定义:** 通过环境变量 `BODY_MANAGEMENT_DATA`

如果脚本检测到配置文件不存在或读取失败，会提示你输入:
- Athlete ID (例如：`iXXXXXXXXX`)
- API Key

凭证会自动保存到 `config.json`,权限设置为 `600`。

---

## 🔧 首次配置引导 🎯

如果你是第一次使用此技能，按以下步骤操作：

### 步骤 1：注册 intervals.icu 账号

1. 访问 [https://intervals.icu/register](https://intervals.icu/register)
2. 填写邮箱和密码完成注册
3. 登录账户

### 步骤 2：获取 API 凭证

1. 登录后点击右上角头像 → **Settings**
2. 选择 **API Keys** 标签页
3. 复制以下两个信息:
   - **Athlete ID**: 格式为 `iXXXXXXXXX`（如 `i206099`）
   - **API Key**: 长字符串（如 `abc123def456...`）

### 步骤 3：运行任意命令触发自动配置

群里发送消息或使用命令行：

```bash
cd ~/.openclaw/workspace/skills/fitness-personal-assistant/scripts
python3 body-status-reporter.py
```

系统会显示：

```
⚠️ 配置文件未找到：~/.../config/config.json

🔧 正在帮您初始化配置...

==================================================
🔐 配置 Intervals.icu API 凭证
==================================================

请先注册账号：https://intervals.icu/register
获取凭证：Settings → API Keys

请输入 Athlete ID (例如：iXXXXXXXXX): i206099
请输入 API Key: *************

✅ 凭证验证成功！
✅ 配置已保存到：~/.../config/config.json
==================================================
```

### 步骤 4：测试连接

重新运行查看身体状态：

```bash
python3 body-status-reporter.py
```

应该能正常输出分析报告！

---

## 📝 使用示例

### 方法 A：自然语言输入（推荐）

群里直接发消息或使用命令行：

```bash
# 单条记录
python3 meal-to-intervals.py --text "300g 牛肉和 200 克米饭"

# 混合多种食物
python3 meal-to-intervals.py --text "早餐两个鸡蛋一片全麦面包，一杯牛奶"

# 指定日期
python3 meal-to-intervals.py --text "午餐吃了沙拉" --date 2026-03-09

# 干跑模式（测试，不上传）
python3 meal-to-intervals.py --text "300g 牛肉" --dry-run
```

系统自动识别：
- **时间**: 当前时刻（可用 `--date` 覆盖）
- **餐次**: 根据关键词判断（早餐/午餐/晚餐/加餐）
- **营养**: 自动计算

### 方法 B：JSON 文件输入

创建 `meal.json`:
```json
{
  "meal_name": "午餐",
  "meal_time": "2026-03-10T12:30:00+08:00",
  "notes": "公司食堂",
  "items": [
    {"name": "鸡胸肉", "grams": 200, "calories": 220, "protein_g": 46, "carbs_g": 0, "fat_g": 3},
    {"name": "西兰花", "grams": 150, "calories": 52, "protein_g": 4.5, "carbs_g": 10.5, "fat_g": 0.75},
    {"name": "米饭", "grams": 250, "calories": 325, "protein_g": 6.25, "carbs_g": 70, "fat_g": 1.25}
  ]
}
```

执行：
```bash
python3 meal-to-intervals.py --input meal.json
```

### 方法 C：查询身体状态

#### 方式 1: 群里发消息
```
查看我的身体状态
今天的训练负荷怎么样？
我适合高强度训练吗？
```

#### 方式 2: 命令行
```bash
cd ~/.openclaw/workspace/skills/fitness-personal-assistant/scripts
python3 body-status-reporter.py
```

**指定日期（查看历史）：**
```bash
# 查看昨天
python3 body-status-reporter.py --date 2026-03-10

# 查看过去某天的报告
python3 body-status-reporter.py -d 2026-03-09
```

---

## 🔧 高级选项

### 干跑模式（测试）

不上传数据，只计算营养：
```bash
python3 meal-to-intervals.py --text "300g 牛肉" --dry-run
```

### 批量导入

编写脚本循环处理多个 JSON 文件：
```bash
for file in meals/*.json; do
    python3 meal-to-intervals.py --input "$file"
done
```

### 自定义存储路径

```bash
export BODY_MANAGEMENT_DATA=/path/to/your/data
python3 meal-to-intervals.py --text "早餐"
```

---

## 🛠️ 技术细节

### 营养计算引擎

**三层策略**：

1. **第一层：中文食物规则库**
   ```python
   肉类分类：
   - 鸡胸：110kcal/100g, 23g 蛋白质
   - 牛肉：200kcal/100g, 22g 蛋白质
   - 猪肉：250kcal/100g, 20g 蛋白质
   - 鱼：120kcal/100g, 20g 蛋白质
   
   主食分类：
   - 米饭：130kcal/100g, 28g 碳水
   - 面条：110kcal/100g, 25g 碳水
   - 面包：270kcal/100g, 50g 碳水
   - 方便面：450kcal/100g, 55g 碳水
   
   蛋奶：
   - 鸡蛋：155kcal/100g, 13g 蛋白质
   - 牛奶：50kcal/100ml, 3.5g 蛋白质
   
   蔬果类:
   - 蔬菜：30kcal/100g
   - 水果：60kcal/100g
   ```

2. **第二层：智能解析**
   - 支持"250ml 牛奶"、"200 克鸡胸"、"两个鸡蛋"、"一碗米饭"
   - 自动按"和"、"、"分割多种食物
   - 优先匹配更长关键词（"方便面"优先于"面"）

3. **第三层：默认估算**
   - 未知食物使用通用值：150kcal/100g

### API 客户端特性

- **自动重试**: 最多 3 次，指数退避（2s, 4s, 8s）
- **错误处理**: 403/404/500 等状态码优雅降级
- **Basic Auth**: 使用 `API_KEY:<key>` 格式
- **连接测试**: `client.test_connection()`
- **配置引导**: 配置文件不存在时自动引导用户输入凭证
- **格式验证**: 验证 Athlete ID 格式 (必须是以 `i` 开头)

### Wellness 数据字段

| 字段 | 说明 | 单位 |
|------|------|------|
| `calories` | 饮食热量（累计） | kcal |
| `protein` | 蛋白质（累计） | g |
| `carbs` | 碳水（累计） | g |
| `fat` | 脂肪（累计） | g |
| `note_breakfast` | 早餐备注 | text |
| `note_lunch` | 午餐备注 | text |
| `note_dinner` | 晚餐备注 | text |
| `hrv` | 心率变异性 | ms |
| `restingHR` | 静息心率 | bpm |
| `sleepSecs` | 睡眠时长 | seconds |
| `steps` | 步数 | count |
| `weight` | 体重 | kg |
| `locked` | 锁定数据（防止同步覆盖） | bool |

---

## 📁 目录结构

```
~/.openclaw/workspace/
├── skills/
│   └── fitness-personal-assistant/
│       ├── .gitignore            # 忽略 config/ 目录
│       ├── README.md             # 简化版使用指南
│       ├── SKILL.md              # 本文档
│       ├── config/               # ← 用户配置 (gitignore)
│       │   └── config.json       # API 凭证
│       └── scripts/
│           ├── intervals_api_client.py    # API 客户端（核心）
│           ├── body-status-reporter.py    # 身体状态报告
│           └── meal-to-intervals.py       # 饮食记录
│
```

---

## ❓ FAQ

**Q: 如何修改运动员 ID？**  
A: 编辑 `~/.openclaw/workspace/skills/fitness-personal-assistant/config/config.json`，无需重启，下次运行自动读取新配置。

**Q: 如何备份我的数据？**  
A: 所有原始数据存储在 intervals.icu 云端，本地仅缓存配置。定期 export intervals.icu 数据即可。

**Q: 不支持某些中国食材怎么办？**  
A: 编辑 `meal-to-intervals.py` 中的 `FOOD_RULES` 字典，添加更多中文食物的精确数值。

**Q: 如何提高营养估算精度？**  
A: 可以扩展 `FOOD_RULES` 字典，或手动创建 JSON 文件输入精确营养数据。

**Q: 数据为什么没有同步？**  
A: 检查：
1. API key 是否有效（运行 `intervals_api_client.py` 测试）
2. 网络连接是否正常
3. 配置文件路径是否正确

**Q: 如何解锁被锁定的 wellness 数据？**  
A: 在 intervals.icu 网页端手动解锁，或使用 API 设置 `"locked": false`。

**Q: 配置文件损坏了怎么办？**  
A: 删除 `config/config.json`,重新运行任意脚本会自动引导你重新配置。

---

## 🔐 安全说明 ⭐

### 🛡️ API 凭证存储安全

| 项目 | 详情 |
|------|------|
| **加密级别** | Basic Auth (HTTP Header Authorization) |
| **传输安全** | HTTPS TLS 1.2+ 加密传输 |
| **存储位置** | `~/.openclaw/workspace/skills/fitness-personal-assistant/config/config.json` |
| **文件权限** | `600` (仅所有者可读/写，`chmod 600 config.json`) |
| **Git 状态** | ✅ 已忽略 (`config/` 在 `.gitignore`) |
| **磁盘加密** | 依赖系统级加密 (macOS FileVault / Windows BitLocker) |

### 🌐 网络请求白名单

此技能**仅向以下可信 API 发送请求**：

| 域名 | 用途 | 安全性验证 |
|------|------|-----------|
| `https://intervals.icu/api/v1/*` | Wellness/Activities 数据同步 | ✅ 官方 API，Basic Auth 认证 |
| `https://world.openfoodfacts.org/api/v0/product/*` | 食品营养数据库查询 | ✅ 开源项目，无认证需求 |

**❌ 绝不出站请求到其他域名！**

### 🔍 代码审计清单

运行以下命令可验证网络行为：

```bash
# 1. 搜索所有 HTTP 请求
grep -r "requests\." scripts/

# 2. 提取所有 URL
grep -rohE 'https?://[^\s")]+' scripts/ | sort -u

# 3. 预期输出（应仅包含上述白名单）
# https://intervals.icu/api/v1
# https://world.openfoodfacts.org/api/v0
```

### 📋 凭证保护最佳实践

1. **✅ 已自动 gitignore** - `config/` 目录不会提交到 GitHub
2. **⚠️ 检查文件权限**:
   ```bash
   ls -l ~/.openclaw/workspace/skills/fitness-personal-assistant/config/config.json
   # 应为：-rw------- (600)
   chmod 600 ~/.openclaw/workspace/skills/fitness-personal-assistant/config/config.json
   ```
3. **🔒 使用环境变量** (最安全):
   ```bash
   # ~/.profile 或 ~/.zshrc
   export INTERVALS_API_KEY="your_key_here"
   export INTERVALS_ATHLETE_ID="iYourID"
   source ~/.zshrc
   ```
4. **🔄 定期检查凭证有效期** - 在 [intervals.icu Dashboard](https://intervals.icu/dashboard) 吊销旧 Key

### 🚨 敏感信息扫描

运行以下命令确认无硬编码凭证：

```bash
# 搜索可能的 API Key 字符串
grep -rn "api_key.*=.*['\"]" scripts/ || echo "✅ No hardcoded keys found"

# 搜索可能被泄露的 Athlete ID
grep -rn "i206099\|leozvc" scripts/ && echo "⚠️ Check for hardcoded athlete info"
```

### 🤖 第三方安全扫描响应

针对 clawhub 的安全扫描提示，本技能已提供：

| 问题 | 解决方案 |
|------|---------|
| Unicode 控制字符 | ✅ 已验证为正常 UTF-8 中文字符 |
| 硬编码开发者信息 | ✅ v3.4.2 移除，动态读取配置 |
| 凭证存储路径不明 | ✅ 文档明确标注存储位置 |
| 网络外联不可信 | ✅ 代码开源，URL 白名单可审计 |
| 配置文件安全风险 | ✅ gitignore + 600 权限 |

---

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v3.5.0 | 2026-03-10 | 配置文件移至技能目录 (`config/`) |
| v3.4.2 | 2026-03-10 | 修复硬编码运动员信息 + 完善安全文档 |
| v3.4.1 | 2026-03-10 | 删除冗余的 package.json |
| v3.4.0 | 2026-03-10 | 简化 README + 配置引导功能 |
| v3.3.0 | 2026-03-10 | 新增配置引导功能：配置文件不存在/损坏时自动提示用户输入凭证 |
| v3.2.0 | 2026-03-10 | 默认输出详细分析报告，含竞技状态准备度 + 深度解读表格 |
| v3.1.0 | 2026-03-10 | Python 完整重构，基于官方 API 文档，支持完整 wellness 字段 |
| v2.1 | 2026-03-10 | 支持自定义存储路径，自动创建子目录 |
| v2.0 | 2026-03-09 | 合并 body-management-system，新增自然语言输入 |
| v1.3.2 | 2026-03-09 | bug fix，field names 修正 |
| v1.3.1 | 2026-03-08 | API 响应检查修复，限流保护 |
| v1.3.0 | 2026-03-08 | 纯云营养计算 + 智能估算 |
| v1.2.0 | 2026-03-08 | Zero dependency migration（纯 Bash） |
| v1.0.0 | 2026-03-06 | 初始版本 |

---

## 📚 引用资源

- [Intervals.icu API Integration Cookbook](https://forum.intervals.icu/t/intervals-icu-api-integration-cookbook/80090)
- [API access to Intervals.icu](https://forum.intervals.icu/t/api-access-to-intervals-icu/609)
- [Intervals.icu 官方文档](https://intervals.icu/api-docs.html)
- [OpenFoodFacts API](https://wiki.openfoodfacts.org/Main_Page)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

---

## ⚠️ 注意事项

1. **网络依赖**: 需要能访问 intervals.icu API 和 OpenFoodFacts
2. **数据准确性**: 营养估算是近似值，精确数据请使用 JSON 输入
3. **锁定机制**: 使用 `"locked": true` 可防止外部同步覆盖手动数据
4. **隐私政策**: 所有数据仅在你指定的 intervals.icu 账户下存储，不会收集到第三方服务器

---

**MIT License** © 2026 leozvc (modded by OpenClaw community)
