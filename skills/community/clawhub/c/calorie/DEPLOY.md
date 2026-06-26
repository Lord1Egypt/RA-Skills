# Kimi Claw 部署指南

## 📦 前提条件

- ✅ 已订阅 Kimi Allegretto 套餐（¥199/月）
- ✅ 拥有 Kimi API Key
- ✅ 已安装 OpenClaw

---

## 🚀 一键部署

### 方式 1：Kimi Claw 控制台部署（推荐）

1. **访问 Kimi 控制台**
   ```
   https://platform.moonshot.cn/console/claw
   ```

2. **上传 Skill 包**
   - 点击"创建新 Claw"
   - 上传 `food-calorie-calculator-v1.0.1.zip`
   - 选择 `config/kimi_claw.yaml` 作为部署配置

3. **配置环境变量**
   ```
   KIMI_API_KEY=your_api_key
   KIMI_MODEL=k2.5
   ```

4. **部署**
   - 点击"部署"
   - 等待部署完成（约 1-2 分钟）

5. **测试**
   - 在 Kimi 对话框输入 `/卡路里`
   - 上传一张食物照片
   - 查看营养分析报告

---

### 方式 2：命令行部署

```bash
# 1. 安装 Kimi CLI（如果未安装）
pip install kimi-claw

# 2. 登录 Kimi
kimi login

# 3. 部署 Claw
cd food-calorie-release
kimi claw deploy --config config/kimi_claw.yaml

# 4. 查看部署状态
kimi claw status food-calorie-calculator

# 5. 测试
kimi claw test food-calorie-calculator --image food.jpg
```

---

## 📋 触发命令

部署成功后，可以使用以下命令触发：

| 命令 | 说明 | 示例 |
|------|------|------|
| `/卡路里` | 快捷命令 | `/卡路里` + 图片 |
| `/calorie` | 英文命令 | `/calorie` + 图片 |
| `算卡路里` | 自然语言 | "算卡路里" + 图片 |
| `食物热量` | 自然语言 | "食物热量" + 图片 |

---

## 🔧 自定义配置

### 修改触发命令

编辑 `config/kimi_claw.yaml`：

```yaml
trigger:
  commands:
    - "/你的命令"
    - "自定义触发词"
```

### 修改输出格式

编辑 `config/kimi_claw.yaml`：

```yaml
output:
  format: markdown  # 或 text, html
  include_image: true  # 返回原图
```

---

## 📊 使用统计

在 Kimi 控制台查看：

1. 访问 https://platform.moonshot.cn/console/claw
2. 选择 `food-calorie-calculator`
3. 查看"使用统计"标签页

**统计数据包括：**
- 📈 调用次数
- ⏱️ 平均响应时间
- 💰 额度消耗
- 👥 用户数

---

## 💰 额度消耗

**Allegretto 套餐包含：**
- K2.5 模型：4 倍基础额度
- Agent 任务：4 倍基础额度

**每次识别消耗：**
- 图片识别：约 0.1-0.2 倍额度
- 营养计算：约 0.05 倍额度
- **总计：约 0.15-0.25 倍额度/次**

**套餐可用次数估算：**
- 4 倍额度 ≈ 16-26 次识别/月
- 如果不够用，可以切换到按量付费模式

---

## 🛠️ 故障排除

### 1. 部署失败

**错误：** "资源不足"
```bash
# 解决方案：降低资源配置
编辑 config/kimi_claw.yaml:
resources:
  max_memory: "256MB"  # 降低内存
  timeout: 30  # 降低超时时间
```

### 2. 识别失败

**错误：** "模型调用失败"
```bash
# 检查 API Key
kimi auth check

# 重新登录
kimi login
```

### 3. 响应慢

**解决方案：**
- 检查网络连接
- 降低图片分辨率
- 使用 `moonshot-v1-auto` 替代 `k2.5`

---

## 📞 技术支持

- Kimi 文档：https://platform.moonshot.cn/docs
- API 状态：https://status.moonshot.cn
- 社区论坛：https://community.moonshot.cn

---

## 🎉 部署完成！

部署成功后，你可以在 Kimi 中这样使用：

```
用户：[上传食物照片] /卡路里

Kimi: 🍽️ **食物识别结果**

📝 一碗米饭配红烧肉和炒青菜

📊 **营养分析**

🔥 总卡路里：**520 大卡**
💪 蛋白质：28.5g
🍚 碳水化合物：65.2g
🥑 脂肪：18.3g

...
```

享受你的健康饮食管理之旅！🥗💪
