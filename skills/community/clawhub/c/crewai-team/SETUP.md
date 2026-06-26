# CrewAI 配置指南

## ⚠️ 必须配置 API Key

CrewAI 需要 LLM API Key 才能运行。

---

## 方案 1：使用阿里云 DashScope（推荐，国内可用）

### 步骤 1：获取 API Key

1. 访问 https://dashscope.console.aliyun.com/
2. 登录/注册阿里云账号
3. 进入「API-KEY 管理」
4. 创建新的 API Key
5. 复制 Key（格式：`sk-xxxxxxxx`）

### 步骤 2：配置环境变量

```bash
# 方式 A：临时设置（当前终端会话有效）
export DASHSCOPE_API_KEY="sk-your-actual-key-here"

# 方式 B：永久设置（添加到 zshrc）
echo 'export DASHSCOPE_API_KEY="sk-your-actual-key-here"' >> ~/.zshrc
source ~/.zshrc

# 方式 C：创建 .env 文件
cd ~/.openclaw/workspace/crewai_team
cp .env.example .env
# 编辑 .env 文件，填入 API Key
```

### 步骤 3：测试

```bash
cd ~/.openclaw/workspace/crewai_team
python3.10 test_team.py
```

---

## 方案 2：使用 OpenAI

```bash
export OPENAI_API_KEY="sk-your-openai-key-here"
```

---

## 方案 3：使用 Ollama 本地模型（免费，无需 API Key）

```bash
# 安装 Ollama
brew install ollama

# 拉取模型
ollama pull qwen2.5:7b

# 配置
export OPENAI_API_KEY="ollama"
export OPENAI_API_BASE="http://localhost:11434/v1"
```

---

## 💰 费用参考（DashScope）

| 模型 | 输入价格 | 输出价格 | 推荐场景 |
|------|---------|---------|---------|
| Qwen3.5-Plus | ¥0.004/1K tokens | ¥0.012/1K tokens | 平衡性价比 |
| Qwen3-Max | ¥0.02/1K tokens | ¥0.06/1K tokens | 高质量输出 |

**完整 PRD 生成预估**: 约 5,000-10,000 tokens，费用约 ¥0.1-0.6 元

---

## ✅ 验证配置

```bash
# 测试 API Key 是否有效
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-your-key" \
  -d '{"model":"qwen3.5-plus","messages":[{"role":"user","content":"Hello"}]}'
```

如果返回包含 `choices` 的 JSON，说明配置成功。

---

## 🚀 运行团队

配置完成后：

```bash
cd ~/.openclaw/workspace/crewai_team

# 方式 1：测试团队配置
python3.10 test_team.py

# 方式 2：运行完整分析
python3.10 run_team.py "一个 AI 驱动的需求收集机器人"

# 方式 3：使用简化版配置
export DASHSCOPE_API_KEY="sk-your-key"
python3.10 team_config_simple.py
```

---

*先生，配置好 API Key 后告诉我，我可以立即测试运行。*
