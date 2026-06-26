# 百度语音合成 API 设置指南

## 概述
本指南介绍如何获取和配置百度智能云语音合成（TTS）API 的访问密钥。百度目前支持多种认证方式，请根据您的需求选择合适的方式。

## 认证方式详解

百度语音合成 API 支持以下三种认证方式（任选其一）：

### 1. access_token 鉴权（传统方式）
- **适用场景**：仅使用 AI 开放能力（语音合成、文字识别等）的用户
- **获取方式**：使用 API Key + Secret Key 换取 access_token（有效期30天）
- **请求参数**：`tok=your_access_token`

### 2. API Key 鉴权（新版方式）
- **适用场景**：同时使用 AI 开放能力、ModelBuilder、AppBuilder 的用户
- **获取方式**：从百度智能云控制台直接获取 API Key（格式如 `bce-v3/ALTAK-...`）
- **请求参数**：`iam-apikey=your_api_key` 或 `apikey=your_api_key`

### 3. Access Key ID/Secret Access Key 鉴权（百度云基础产品）
- **适用场景**：同时使用百度云基础产品（云服务器、对象存储等）和 AI 能力的用户
- **获取方式**：从百度云控制台获取 Access Key ID 和 Secret Access Key
- **请求参数**：需使用签名算法，本技能暂未集成，建议使用前两种方式

**本技能支持前两种方式：**
1. **API Key + Secret Key** → 自动获取 access_token → 使用 `tok` 参数
2. **直接提供 access_token**（以 `1.` 开头） → 直接使用 `tok` 参数
3. **直接提供 IAM Key**（以 `bce-v3/` 开头） → 使用 `iam-apikey` 参数

## 步骤1：注册百度智能云账号

### 1.1 访问官网
- 百度智能云官网：https://cloud.baidu.com/
- 点击右上角 "注册" 或 "登录"

### 1.2 完成实名认证
- 个人用户：身份证认证
- 企业用户：企业认证（可选）
- 认证后可以获得更高额度和更多服务

## 步骤2：开通语音合成服务

### 2.1 控制台导航
1. 登录后进入控制台
2. 在左侧菜单找到 "产品服务" → "人工智能" → "语音技术"
3. 选择 "语音合成"

### 2.2 开通服务
- 点击 "立即开通"
- 阅读并同意服务协议
- 选择计费方式（默认后付费）
- 开通成功

## 步骤3：获取认证密钥

### 3.1 获取 API Key + Secret Key（传统方式）
1. 进入 "语音合成" 控制台
2. 左侧菜单选择 "应用列表"
3. 点击 "创建应用"
4. 填写应用信息：
   - **应用名称**：`OpenClaw-TTS`（可自定义）
   - **应用描述**：`OpenClaw 语音合成技能`
   - **接口选择**：确保选中 "语音合成"
   - **包名**：留空或填写 `com.example.openclaw`
5. 创建成功后，在应用列表中获取：
   - **API Key**：客户端访问密钥
   - **Secret Key**：服务器端密钥（需保密）

### 3.2 获取 IAM Key（新版 API Key）
1. 进入百度智能云控制台
2. 左侧菜单选择 "访问管理" → "API 密钥管理"
3. 点击 "创建密钥"
4. 选择 "API Key" 类型
5. 获取到的密钥格式为 `bce-v3/ALTAK-...`，即为 IAM Key

### 3.3 获取 access_token（直接使用）
如果您已有 API Key + Secret Key，可以通过以下方式获取 access_token：
```bash
curl "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=YOUR_API_KEY&client_secret=YOUR_SECRET_KEY"
```
返回的 `access_token` 字段即为令牌（以 `1.` 开头）。

**重要**：立即复制并保存您的密钥！

## 步骤4：配置环境变量

### 4.1 根据您的密钥类型选择配置方式

#### 方式 A：使用 API Key + Secret Key（自动获取 token）
```bash
export BAIDU_API_KEY="你的API Key（非 bce-v3 格式）"
export BAIDU_SECRET_KEY="你的Secret Key"
```

#### 方式 B：直接使用 access_token
```bash
export BAIDU_API_KEY="YOUR_ACCESS_TOKEN"
# BAIDU_SECRET_KEY 无需设置
```

#### 方式 C：使用 IAM Key（bce-v3 格式）
```bash
export BAIDU_API_KEY="YOUR_IAM_KEY_HERE"
# BAIDU_SECRET_KEY 无需设置
```

### 4.2 永久配置（推荐）
在 `~/.bashrc` 或 `~/.zshrc` 中添加上述环境变量，然后执行：
```bash
source ~/.bashrc
```

### 4.3 项目级配置
创建 `.env` 文件：
```bash
BAIDU_API_KEY=你的密钥
BAIDU_SECRET_KEY=你的Secret Key（如果需要）
```

然后在脚本中加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

## 步骤5：验证配置

### 5.1 测试命令
使用技能提供的测试脚本：
```bash
cd ~/.openclaw/skills/baidu-speech-synthesis/scripts
python baidu_tts.py --text "测试语音合成" --output test.mp3
```

### 5.2 检查输出
- 成功：生成 `test.mp3` 文件并可以播放
- 失败：显示错误信息

### 5.3 常见错误及解决方案

#### 错误1：`"tok, appid, apikey or iam-apikey is empty"`
**原因**：认证参数缺失。
**解决方案**：
1. 检查 `BAIDU_API_KEY` 环境变量是否正确设置
2. 确认密钥格式：
   - 如果使用 `bce-v3/` 格式，技能会自动使用 `iam-apikey` 参数
   - 如果使用 `1.` 开头的 access_token，技能会自动使用 `tok` 参数
   - 如果使用普通 API Key，必须同时设置 `BAIDU_SECRET_KEY`
3. 运行 `echo $BAIDU_API_KEY` 确认环境变量已加载

#### 错误2：`"authentication failed"`
**原因**：密钥无效或已过期。
**解决方案**：
1. 访问控制台查看密钥状态
2. 重新生成密钥并更新环境变量
3. 如果使用 access_token，重新获取（有效期30天）

#### 错误3：`"internal error"` 或 `"service not available"`
**原因**：服务端问题或额度不足。
**解决方案**：
1. 查看服务状态页面
2. 检查免费额度是否用完

## 免费额度与计费

### 免费额度
- **标准音色**：每月 **500 万字符** 免费额度（2026年最新政策）
- **精品音色**：可能有额外限制或单独计费
- **有效期**：永久免费额度（每月1日重置）

### 查看使用情况
1. 控制台 → 语音合成 → 使用统计
2. 查看调用次数、字符数、费用
3. 设置用量告警（建议设置阈值告警）

### 超出免费额度
- **按量计费**：标准音色约 0.003元/千字符
- **套餐包**：购买预付费套餐更优惠
- **预算设置**：防止意外费用，可设置每月预算上限

## 安全建议

### 密钥安全
1. **不要提交到代码仓库**
   ```bash
   # .gitignore 添加
   .env
   *.key
   secrets/
   ```

2. **使用环境变量**而非硬编码
3. **定期轮换密钥**（控制台可重新生成）
4. **限制IP白名单**（企业版支持）

### 访问控制
1. **子账号权限**：为不同应用创建单独密钥
2. **API调用限制**：设置QPS限制防止滥用
3. **操作日志**：开启审计日志追踪调用记录

## 故障排除进阶

### 问题1：IAM Key 认证失败
**可能原因**：
- IAM Key 未授权语音合成服务
- 密钥格式错误

**解决方案**：
1. 在 API 密钥管理页面，点击密钥右侧的 "授权"
2. 确保勾选 "语音技术" → "语音合成"
3. 等待1-2分钟授权生效

### 问题2：access_token 过期
**现象**：之前正常，突然认证失败。
**解决方案**：
1. access_token 有效期30天，需要定期刷新
2. 本技能在 `apikey_secret` 模式下会自动刷新
3. 如果直接使用 access_token，需自行重新获取并更新环境变量

### 问题3：SSML模式失败
**可能原因**：
- API版本过低（需V5.5+）
- SSML格式错误
- 音色代码不正确

**解决方案**：
- 使用 `per=511` 参数
- 验证SSML格式（参考官方文档）
- 回退到分段合并模式（使用 `--merge` 参数）

### 问题4：音频质量差
**优化建议**：
- 调整语速（`spd`）、音调（`pit`）参数
- 使用精品音色（per=5003, 5118等）
- 添加适当停顿（SSML中使用 `<break>`）
- 避免过长单句（建议每句不超过120字符）

## 进阶配置

### 多环境配置
```bash
# 开发环境
export BAIDU_API_KEY_DEV="dev_key"
export BAIDU_SECRET_KEY_DEV="dev_secret"

# 生产环境  
export BAIDU_API_KEY_PROD="prod_key"
export BAIDU_SECRET_KEY_PROD="prod_secret"
```

在脚本中根据环境变量选择：
```python
import os
env = os.getenv("ENV", "dev")
api_key = os.getenv(f"BAIDU_API_KEY_{env.upper()}")
secret_key = os.getenv(f"BAIDU_SECRET_KEY_{env.upper()}")
```

### 自动化部署
```yaml
# Dockerfile
ENV BAIDU_API_KEY=${BAIDU_API_KEY}
ENV BAIDU_SECRET_KEY=${BAIDU_SECRET_KEY}
```

```yaml
# Kubernetes Secret
apiVersion: v1
kind: Secret
metadata:
  name: baidu-tts-secret
type: Opaque
stringData:
  BAIDU_API_KEY: your_api_key
  BAIDU_SECRET_KEY: your_secret_key
```

## 支持与资源

### 官方文档
- [语音合成API文档](https://ai.baidu.com/ai-doc/SPEECH/Tk4o0bmio)
- [错误码列表](https://ai.baidu.com/ai-doc/SPEECH/7k4o0bx8k)
- [SSML参考](https://ai.baidu.com/ai-doc/SPEECH/Tk4o0bmio#ssml)
- [鉴权机制说明](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu)

### 社区支持
- 百度智能云论坛
- GitHub Issues（本技能仓库）
- 技术交流群

### 联系我们
- 技术支持：控制台在线客服
- 商务合作：4008-777-818
- 邮件支持：cloud_support@baidu.com

## 更新日志
- **2026-03-26**：重大更新，支持三种认证方式（access_token、IAM Key、API Key+Secret Key）
- **2026-03-26**：更新免费额度为每月500万字符（基于最新政策）
- **2026-03-26**：增强错误引导和密钥获取指南
- 定期检查官方文档以获取更新

---

## 重要提醒：现有 bce‑v3/ 密钥可能不适用

### 如果您已有 `BAIDU_API_KEY="bce‑v3/ALTAK‑..."` 格式的密钥：

1. **该密钥为百度搜索专用**，无法用于语音合成 API
2. **需要创建专门的语音合成应用**获取正确的 API Key + Secret Key
3. **错误示例**：
   ```
   错误: "tok, appid, apikey or iam‑apikey is empty"
   或: "合成失败 501: parameter error"
   ```

### 解决方案：
1. 按照本指南**第2步**创建语音合成应用
2. 获取新的 **API Key + Secret Key**（非 `bce‑v3/` 格式）
3. 设置环境变量：
   ```bash
   export BAIDU_API_KEY="新的API_Key"
   export BAIDU_SECRET_KEY="新的Secret_Key"
   ```

### 为什么需要新密钥？
- 百度不同服务（搜索、语音、OCR等）需要独立授权
- `bce‑v3/` 是 IAM（统一身份认证）格式，但语音合成可能需特定权限
- 免费额度（每月500万字符）仅适用于语音合成专用应用

---

**提示**：如果您遇到任何问题，请先检查本指南的"故障排除"部分。大多数问题都能在这里找到解决方案。