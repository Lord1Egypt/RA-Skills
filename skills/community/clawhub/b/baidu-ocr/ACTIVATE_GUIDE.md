# 🔑 百度 OCR 权限开通指南

## 当前状态

**API Key**: `4LceeJ8wBDSqa3SqDHmgXuk1` ✅ 有效
**Token 获取**: ✅ 成功

**已有权限**:
- ✅ vis-classify_dishes (菜品识别)
- ✅ vis-classify_car (车辆识别)
- ✅ vis-classify_animal (动物识别)
- ✅ vis-classify_plant (植物识别)
- ✅ vis-classify_flower (花卉识别)
- ✅ vis-ocr_虚拟人物助理

**缺少权限**:
- ❌ 通用文字识别（标准版）
- ❌ 通用文字识别（高精度版）
- ❌ 表格文字识别
- ❌ 公式识别

---

## 📋 开通步骤（详细图解）

### 步骤 1：登录百度 AI 控制台

**网址**: https://console.bce.baidu.com/ai/

1. 使用百度账号登录
2. 进入控制台首页

---

### 步骤 2：找到文字识别服务

1. 点击左侧菜单 **"应用管理"**
2. 在应用列表中找到您的应用（API Key: `4LceeJ8wBDSqa3SqDHmgXuk1`）
3. 点击应用名称进入详情页

---

### 步骤 3：开通文字识别服务

在应用详情页：

1. 点击 **"服务"** 或 **"功能列表"** 标签
2. 找到 **"文字识别"** 分类
3. 点击以下服务后面的 **"开通"** 按钮：

   | 服务名称 | 推荐 | 免费额度 |
   |----------|------|----------|
   | **通用文字识别（标准版）** | ✅ 必开 | 500 次/天 |
   | **通用文字识别（高精度版）** | ✅ 必开 | 50 次/天 |
   | **表格文字识别** | ✅ 推荐 | 500 次/月 |
   | **公式识别** | ✅ 推荐 | 500 次/月 |
   | 手写文字识别 | ⭕ 可选 | 500 次/月 |
   | 生僻字识别 | ⭕ 可选 | 500 次/月 |

4. 确认开通（可能需要同意服务协议）

---

### 步骤 4：等待生效

开通后通常**立即生效**，有时需要等待 1-2 分钟。

---

### 步骤 5：验证开通成功

**方法 1：在控制台查看**

1. 返回应用详情页
2. 点击 **"服务"** 标签
3. 查看已开通服务列表
4. 确认文字识别服务显示为 **"已开通"**

**方法 2：使用测试脚本**

```bash
python3 /root/.openclaw/workspace/skills/baidu-ocr/baidu_ocr.py /path/to/image.jpg
```

**成功输出**:
```
📷 读取图片：image.jpg
🔑 获取 access_token...
✅ access_token 获取成功
🔍 执行 OCR 识别（高精度版）...

============================================================
识别结果:
============================================================
(2) 核算压力降
管程压力降
ΣΔp_i=(Δp_1+Δp_2)×F_t×N_p
其中，F_t=1.4,N_p=2
============================================================
✅ 识别完成！共 4 行
```

---

## 🎯 快速直达链接

### 控制台链接
- [百度 AI 控制台](https://console.bce.baidu.com/ai/)
- [应用管理列表](https://console.bce.baidu.com/ai/#/ai/ocr/app/list)
- [文字识别服务页](https://ai.baidu.com/ai-doc/OCR)

### 开通链接（如果找不到）
- [通用文字识别开通](https://console.bce.baidu.com/ai/#/ai/ocr/overview/index)
- [服务开通指南](https://ai.baidu.com/ai-doc/OCR/Wk3h7x8bv)

---

## ⚠️ 常见问题

### Q1: 找不到"开通"按钮？
**A**: 
1. 确认已登录正确的百度账号
2. 确认是应用的所有者或有管理权限
3. 尝试刷新页面或重新登录

### Q2: 开通后还是提示"No permission"？
**A**:
1. 等待 1-2 分钟让权限生效
2. 清除浏览器缓存后重试
3. 重新获取 Token（Token 可能缓存了旧权限）

### Q3: 提示"应用不存在"？
**A**:
1. 确认 API Key 和 Secret Key 正确
2. 确认应用未被删除
3. 重新创建应用并获取新的 Key

### Q4: 免费额度是多少？
**A**:
- 通用文字识别（标准版）：500 次/天
- 通用文字识别（高精度版）：50 次/天
- 表格文字识别：500 次/月
- 公式识别：500 次/月

对于个人使用和测试完全够用！

---

## 📞 需要帮助？

如果遇到问题：

1. **查看官方文档**: https://ai.baidu.com/ai-doc/OCR/Ek3h7xypm
2. **联系客服**: 控制台页面右下角"在线客服"
3. **查看 FAQ**: https://ai.baidu.com/ai-doc/OCR/uk3h7xzzq

---

## ✅ 开通后测试

开通服务后，运行以下命令测试：

```bash
# 测试图片 1（管程压力降）
python3 /root/.openclaw/workspace/skills/baidu-ocr/baidu_ocr.py \
  /root/.openclaw/media/inbound/8ea7eb5f-dfba-45ab-8887-02ef1ebc0ef5.jpg

# 测试图片 2（壳程压力降）
python3 /root/.openclaw/workspace/skills/baidu-ocr/baidu_ocr.py \
  /root/.openclaw/media/inbound/9afbfd04-9a15-437b-bf0e-b24388943406.jpg
```

---

*更新时间：2026-03-07 01:41*
*技能版本：v1.0.0*
