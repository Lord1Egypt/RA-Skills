---
name: calorie-detective-v1-0-2
description: 热量侦探 v1.0.2 - AI 食物卡路里计算器。通过照片识别食物并自动计算卡路里、蛋白质、碳水、脂肪等营养数据。支持 Kimi 视觉识别，内置常见食物营养数据库。用于健康饮食管理、减肥健身追踪。再隐蔽的热量也逃不过我的眼睛！
---

# 🔍 热量侦探 v1.0.0

🕵️ **再隐蔽的热量也逃不过我的眼睛！**

通过 AI 视觉识别技术，像侦探一样找出食物中隐藏的热量，自动计算卡路里和营养成分，帮助你更好地管理饮食健康。

## ✨ 功能特性

1. **📸 拍照识别** - 上传食物照片，AI 自动识别食物种类
2. **🔥 卡路里计算** - 自动计算总卡路里和宏量营养素
3. **📊 营养报告** - 生成详细的营养分析报告
4. **💡 健康建议** - 提供饮食改进建议
5. **🌐 中文优化** - 专为中餐优化，识别更准确
6. **💾 本地数据库** - 内置常见食物营养数据

## 🚀 快速开始

### 方式 1：Kimi Claw 一键部署（推荐）

```bash
# 1. 访问 Kimi 控制台
https://platform.moonshot.cn/console/claw

# 2. 上传 skill 包
# 选择 calorie-detective-v1.0.2.zip

# 3. 使用 config/kimi_claw.yaml 配置

# 4. 部署完成后，在 Kimi 中使用：
/卡路里 [上传食物照片]
```

**优点：**
- ✅ 一键部署，无需配置环境
- ✅ 自动扩展，无需管理服务器
- ✅ 使用 K2.5 模型（Allegretto 套餐包含）
- ✅ 支持自然语言触发

---

### 方式 2：本地安装

```bash
# 解压 skill
unzip calorie-detective-v1.0.2.zip -d calorie-detective
cd calorie-detective

# 安装依赖
pip install -r requirements.txt

# 配置 API Key
export KIMI_API_KEY="your_kimi_key"

# 运行
./run.sh data/food.jpg
```

## ⚙️ 配置

### 配置 API Key

**方式 1：环境变量（推荐）**
```bash
export KIMI_API_KEY="your_kimi_key"
```

**方式 2：配置文件**
编辑 `config/config.local.yaml`：
```yaml
api_keys:
  kimi: "your_kimi_key"
```

**获取 Kimi API Key：**
1. 访问 https://platform.moonshot.cn
2. 注册/登录账号
3. 进入控制台 → API Keys
4. 创建新 Key
5. 新用户注册送免费额度

### config/config.yaml

```yaml
# 视觉识别配置
vision:
  provider: kimi        # 推荐使用 Kimi
  model: moonshot-v1-auto
  
# 使用限制
usage:
  max_requests_per_day: 10
  max_requests_per_user: 5
```

## 📤 输出示例

```
🕵️ **热量侦探 - 营养分析报告**

📝 一碗牛肉拉面，配有青菜和红油汤底

📊 **营养分析**

🔥 总卡路里：**696 大卡**
💪 蛋白质：26.4g
🍚 碳水化合物：50.9g
🥑 脂肪：43.1g

📋 **详细分解**

• **面条** (1 碗)
  - 卡路里：220 大卡
  - 蛋白质：5.0g | 碳水：50g | 脂肪：1.0g

• **牛肉** (80 克)
  - 卡路里：200 大卡
  - 蛋白质：20.8g | 碳水：0g | 脂肪：12.0g

• **青菜** (30 克)
  - 卡路里：6 大卡
  - 蛋白质：0.6g | 碳水：0.9g | 脂肪：0.1g

• **红油汤底** (300ml)
  - 卡路里：270 大卡
  - 蛋白质：0g | 碳水：0g | 脂肪：30.0g

──────────────────────────────
💡 侦探建议：
• 红油汤底热量较高，建议少喝汤
• 蛋白质含量充足，适合作为主食
• 可搭配凉拌菜增加膳食纤维
```

## 📅 定时任务管理

```bash
# 查看所有定时任务
openclaw cron list

# 手动立即运行一次
openclaw cron run <job-id>

# 暂停任务
openclaw cron update <job-id> --enabled false

# 删除任务
openclaw cron remove <job-id>
```

## 📁 文件结构

```
calorie-detective/
├── SKILL.md                  # 本文件
├── config/
│   ├── config.yaml           # 配置文件
│   ├── config.local.yaml     # 本地配置（含 API Key）
│   └── kimi_claw.yaml        # Kimi Claw 部署配置
├── src/
│   └── calorie_calculator.py # 主程序
├── data/
│   ├── food.jpg              # 示例图片
│   └── calorie.log           # 运行日志
├── requirements.txt          # 依赖列表
├── run.sh                    # 运行脚本
└── test.sh                   # 测试脚本
```

## 🍎 内置食物数据库

已内置 100+ 种常见食物营养数据（每 100 克）：

| 类别 | 食物举例 |
|------|----------|
| 🍚 主食 | 米饭、面条、馒头、面包、土豆 |
| 🥚 蛋白质 | 鸡蛋、牛奶、鸡肉、猪肉、牛肉、鱼 |
| 🍎 水果 | 苹果、香蕉、橙子、葡萄、草莓 |
| 🥬 蔬菜 | 青菜、番茄、黄瓜、胡萝卜、西兰花 |
| 🍔 快餐 | 汉堡、薯条、炸鸡、披萨 |

## 🔧 支持的视觉服务

| 服务商 | 模型 | 价格 | 需要 API Key | 推荐度 |
|--------|------|------|-------------|--------|
| **Kimi** | moonshot-v1-auto | ¥0.008/张 | ✅ | ⭐⭐⭐⭐⭐ |
| Kimi | k2.5 | 套餐包含 | ✅ | ⭐⭐⭐⭐⭐ |
| OpenAI | GPT-4o / GPT-4V | $0.01/张 | ✅ | ⭐⭐⭐⭐ |
| Claude | Claude 3 Vision | $0.003/张 | ✅ | ⭐⭐⭐⭐ |

**推荐使用 Kimi：**
- ✅ 中文识别最好
- ✅ 价格便宜（约 OpenAI 的 1/10）
- ✅ 国内直接访问
- ✅ 注册送免费额度

## 🛠️ 故障排除

### 1. 依赖安装失败
```bash
pip install --break-system-packages -r requirements.txt
```

### 2. API Key 无效
- 检查 API Key 是否正确
- 确认账户有可用额度
- 检查网络连接

```bash
# 测试 API Key
curl https://api.moonshot.cn/v1/chat/completions \
  -H "Authorization: Bearer $KIMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "moonshot-v1-auto", "messages": [{"role": "user", "content": "Hello"}]}'
```

### 3. 图片识别不准确
- 确保图片清晰、光线充足
- 尽量拍摄食物特写
- 避免过多餐具干扰

### 4. 营养数据不准确
- 内置数据库为估算值
- 建议接入专业营养 API 获取精确数据
- 可在代码中添加自定义食物

## 📊 使用统计

在 Kimi 控制台查看：

1. 访问 https://platform.moonshot.cn/console/claw
2. 选择 `calorie-detective`
3. 查看"使用统计"标签页

**统计数据包括：**
- 📈 调用次数
- ⏱️ 平均响应时间
- 💰 额度消耗
- 👥 用户数

## 🔄 扩展开发

### 添加新食物
编辑 `src/calorie_calculator.py` 中的 `COMMON_FOODS` 字典：

```python
COMMON_FOODS = {
    '你的食物': {'calories': 100, 'protein': 5, 'carbs': 15, 'fat': 3},
    ...
}
```

### 添加新的视觉服务
继承 `VisionRecognizer` 类并实现 `_recognize_xxx` 方法。

## 📝 更新日志

### v1.0.0 (2026-03-03) - 正式发布版
- ✅ 基础功能实现
- ✅ Kimi 视觉识别支持
- ✅ 本地食物营养数据库（100+ 种食物）
- ✅ 营养报告生成
- ✅ 健康饮食建议
- ✅ Kimi Claw 一键部署支持
- ✅ 中文食物识别优化
- ✅ 品牌：热量侦探

## ⚠️ 免责声明

- 本工具提供的营养数据仅供参考，不构成医疗或营养建议
- 实际食物营养含量可能因烹饪方式、食材来源等因素有所不同
- 如有特殊饮食需求或健康问题，请咨询专业营养师或医生
- 开发者不对使用本工具造成的任何损失承担责任

## 📄 License

MIT

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请提交 Issue 或联系开发者。

---

**🕵️ 热量侦探，再隐蔽的热量也逃不过我的眼睛！** 🍽️
