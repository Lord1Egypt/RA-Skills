# reference/ 文件夹说明

本文件夹包含**可选的参考代码**，用于实现**真正的多模型交叉验证**。

## ⚠️ 重要说明

- **这不是核心功能**，核心功能（零配置）在 `SKILL.md` 中已实现
- **需要自行配置 API Key**
- 普通用户无需理会此文件夹

---

## 功能说明

`multi_model_verify.py` 调用多个外部 LLM API，对同一内容进行验证，实现**真正的多模型交叉验证**。

支持的模型：
- **GLM-4-Plus**（智谱 AI）
- **DeepSeek-V3**
- **Hunyuan-Turbo**（腾讯混元）
- **Kimi-K2**（Moonshot）
- **MiniMax-M2.7**

---

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

在环境变量中设置至少一个模型的 API Key：

```bash
# GLM（智谱 AI）
export ZHIPUAI_API_KEY="your-glm-api-key"

# DeepSeek
export DEEPSEEK_API_KEY="your-deepseek-api-key"

# 混元（腾讯）
export HUNYUAN_API_KEY="your-hunyuan-api-key"

# Kimi（Moonshot）
export MOONSHOT_API_KEY="your-kimi-api-key"

# MiniMax
export MINIMAX_API_KEY="your-minimax-api-key"
```

### 3. 运行验证

**模式A：问答验证**
```bash
python multi_model_verify.py \
  --question "魏建军是谁？" \
  --answer "魏建军是长城汽车创始人，1964年出生，现任董事长，持有公司56%股份。"
```

**模式B：文章/论点验证**
```bash
python multi_model_verify.py \
  --text "比亚迪2024年销量400万辆，已经超过特斯拉成为全球第一，王传福是比亚迪创始人，公司成立于1995年，总部在深圳。"
```

### 4. 查看结果

验证结果会：
- 在终端打印
- 保存到 `verification_result.json`

---

## 各模型 API Key 获取方式

| 模型 | 获取地址 | 环境变量名 |
|------|---------|-----------|
| GLM（智谱 AI） | https://open.bigmodel.cn/ | `ZHIPUAI_API_KEY` |
| DeepSeek | https://platform.deepseek.com/ | `DEEPSEEK_API_KEY` |
| 混元（腾讯） | https://cloud.tencent.com/product/hunyuan | `HUNYUAN_API_KEY` |
| Kimi（Moonshot） | https://platform.moonshot.cn/ | `MOONSHOT_API_KEY` |
| MiniMax | https://api.minimax.chat/ | `MINIMAX_API_KEY` |

---

## 与核心功能（零配置）的区别

| 特性 | 核心功能（SKILL.md） | 本参考代码（reference/） |
|------|----------------------|------------------------|
| 配置要求 | ✅ 零配置 | ❌ 需配置 API Key |
| 多模型验证 | 模拟（多视角角色扮演） | ✅ 真正调用多个模型 |
| 适用场景 | 日常使用 | 高级用户、研究者 |
| 外部依赖 | 无 | openai, zhipuai, dashscope 等 |

---

## 注意事项

1. **API 费用**：调用外部 API 会产生费用，请注意各平台的计费规则
2. **数据安全**：您的文本会被发送到对应的 LLM 提供商，请 review 各平台的数据政策
3. **速率限制**：各平台有速率限制，并发调用时请注意
4. **本代码仅供参照**：您可以根据自己的需求修改代码，接入更多模型

---

_本文件夹为可选功能，不影响核心功能的使用。_
