# 安全合规边界（v3.4.1 审计整改 + v3.4.2 强化）

> SKILL.md § 安全合规边界的详细补充。处理用户样本、爬虫、凭证、自动化脚本时，AI 必须读取本文件并遵守全部原则。
> v3.4.2 外迁自 SKILL.md，回应 ClawHub SkillSpector [SQP-2] persistence_privilege concern。

## 1. 敏感数据处理原则

本技能处理用户提供的样表/资料（简历、合同、发票、名片等）时，必须遵守以下原则：

### 1.1 数据最小化

只采集业务必需字段，禁止"先全抓再筛"：

| 样本类型 | ✅ 允许采集的字段 | ❌ 禁止采集的字段 |
|---------|----------------|----------------|
| 简历 | 岗位/姓名/学历/工作经验 | 身份证/银行卡号/家庭住址 |
| 合同 | 合同号/签订日期/金额/双方名称 | 完整条款文本/签字样本 |
| 发票 | 发票号/金额/日期/购买方 | 完整税号/购买方银行账号 |
| 名片 | 姓名/职位/公司/电话（已脱敏） | 个人邮箱/家庭地址 |

### 1.2 脱敏优先

处理含个人信息的样本前，必须提示用户脱敏：

- **提示话术**：`⚠️ 检测到您的样本含敏感字段（{字段名}），建议先用 [脱敏建议] 处理后再提交分析`
- **脱敏建议**：
  - 姓名 → 首字+`*`（如 "张三" → "张*"）
  - 手机号 → `138****1234`（保留前 3 后 4）
  - 身份证 → `110***********0011`（保留前 3 后 4）
  - 银行卡 → `6222************1234`（保留前 4 后 4）
  - 邮箱 → `zhang***@example.com`（用户名首字+星号）

### 1.3 本地优先

默认所有处理在用户本地完成，禁止将样本数据外发：

- 引导入口生成的 Prompt 不会把原始数据上传，只生成可执行代码
- WebFetch 仅抓取用户提供的 URL（场景 1 网页采集），不抓取本地文件
- 蒸馏入口产出的方法论文件不含用户原始数据

### 1.4 云端存储前脱敏

涉及飞书多维表格双存储（M26）时，必须先脱敏再上传：

- **提示话术**：`⚠️ 云端存储前，请确认数据已脱敏（敏感字段已替换/删除），飞书表将保存脱敏后的版本`
- **默认行为**：双存储时本地保留完整版，云端只存脱敏版
- **二次脱敏铁律**：即使用户表示已脱敏，AI 仍必须在生成上传代码前再次扫描字段名，发现敏感字段名（含"身份证""手机""银行卡""税号"等）必须提示用户

## 2. 爬虫合规边界（v3.4.0 引入，v3.4.1 强化）

本技能场景 1 网页采集 + M22-M26 爬虫方法论必须遵守：

### 2.1 七条铁律

1. **遵守 robots.txt**：抓取前先访问 `https://target.com/robots.txt`，禁止抓取 Disallow 路径
2. **遵守服务条款**：阅读目标网站 ToS，禁止抓取明确禁止自动化的内容
3. **礼貌限流**：默认 `time.sleep(1-3s)`，减轻目标站点压力，禁止高速并发爬取
4. **标识 User-Agent**：使用真实 UA（如 `Mozilla/5.0 (compatible; personal-research/1.0)`），禁止伪造他人 UA
5. **禁止绕过认证**：
   - ❌ 禁止绕过登录验证
   - ❌ 禁止破解/绕过验证码（reCAPTCHA/hCaptcha 等）
   - ❌ 禁止使用 IP 轮换代理池规避封禁
   - ❌ 禁止伪造 CSRF Token 绕过权限校验
6. **公开数据原则**：只抓取无需登录即可访问的公开数据
7. **数据用途限制**：抓取的数据仅用于个人分析/研究，禁止转售/公开再发布

### 2.2 触发时机

- 用户说"抓数据""爬取""网页表格" → 自动应用本节铁律
- AI 生成场景 1 Prompt 前必须读取本节
- M22 SPA 动态 API 识别 / M23 动态 Key 模拟 / M24 增量 ID / M25 HTML 定位 / M26 飞书双存储 均默认遵守

### 2.3 爬虫模板脱敏门控（v3.4.4 强制，回应 ClawHub Instruction Scope + Purpose & Capability concern）

⚠️ **生成爬虫/双存储代码模板时，必须强制执行以下 5 道脱敏门控**：

| 门控 # | 名称 | 触发位置 | 操作 |
|--------|------|---------|------|
| 1 | **cURL 脱敏门控** | 用户提供 cURL 给 AI 分析前 | 用户必须本地替换所有真实 Authorization/X-API-Key/Cookie 为 `<REDACTED_*>` 占位符 |
| 2 | **HTML 脱敏门控** | 用户复制 HTML 给 AI 分析前 | 用户必须本地替换所有 `<input value="...">` 中的 Token/Session/CSRF 为 `<REDACTED_*>` |
| 3 | **代码示例脱敏门控** | AI 生成代码示例时 | 禁止在示例中硬编码真实凭证值，统一从 `.env` 读取 |
| 4 | **日志脱敏门控** | AI 生成日志输出代码时 | 禁止 `print(api_key)`，必须用 `print(f"{api_key[:4]}****")` |
| 5 | **云端存储脱敏门控** | 调用 `dual_storage` 写入飞书前 | 必须传入 `sensitive_fields` 参数，云端只保存脱敏版 |

**禁止生成的模板模式**：
- ❌ `api_key = "sk-真实值..."`（硬编码）
- ❌ `headers = {"Authorization": "Bearer 真实token"}`（硬编码）
- ❌ `dual_storage(records, csv_path, feishu_config)`（无 sensitive_fields 参数）
- ❌ `print(f"Full token: {token}")`（日志泄露）
- ❌ 教用户"模拟登录用户的 Session 绕过 401"（绕过认证）

**正确生成的模板模式**：
- ✅ `api_key = os.getenv("TARGET_API_KEY")`（从 .env 读取）
- ✅ `headers = {"Authorization": f"Bearer {os.getenv('TARGET_TOKEN')}"}`（从 .env 读取）
- ✅ `dual_storage(records, csv_path, feishu_config, sensitive_fields=["手机号", "邮箱"])`（强制脱敏）
- ✅ `print(f"Using token: {token[:6]}****")`（日志脱敏）
- ✅ "401/403 = 认证被拒绝，立即停止，不模拟 Session 重试"（合规边界）

### 2.4 公开 API 与认证 API 的判定（v3.4.4 新增，回应 ClawHub Purpose & Capability concern）

⚠️ **判定 API 是否可抓取的 4 条规则**：

| API 类型 | 是否可抓取 | 判定依据 |
|---------|----------|---------|
| 公开搜索 API（Algolia/Meilisearch 等第三方服务） | ✅ 可抓取 | 网站前端 JS 公开调用，无登录要求 |
| 公开数据 API（GitHub Public API 等） | ✅ 可抓取 | 公开数据，无认证或仅需免费 Token |
| 用户自有 API（用户已注册并获授权） | ✅ 可抓取 | 用户拥有合法权限，且 API 速率限制内 |
| 需要登录的 API / 付费 API / 管理员 API | ❌ 禁止抓取 | 需要认证 = 非公开数据，本技能不支持模拟认证 |

**401/403 处理铁律**：
- 401 Unauthorized = 网站明确拒绝你的访问 → **立即停止，提示用户该 API 需要认证**
- 403 Forbidden = 网站明确禁止访问 → **立即停止，提示用户该 API 拒绝访问**
- ❌ 禁止通过"模拟 Session 重试"绕过 401/403
- ❌ 禁止通过"刷新 Cookie"绕过 401/403
- ❌ 禁止通过"更换 UA/Referer"绕过 401/403
- ✅ Key 刷新机制仅用于**公开 Key 的自然过期**（如 Algolia 每 5 分钟刷新的搜索 Key）

## 3. 凭证保护原则

### 3.1 四条铁律

1. **禁止硬编码 Token**：所有 Token（飞书 PERSONAL_BASE_TOKEN、API Key、Cookie）必须从环境变量读取
2. **本地保存限制**：用户提供的 Token 仅本地保存（用户工作目录的 `.env` 文件），不写入技能文件、不写入日志
3. **示例脱敏**：场景 1 Prompt 模板中 Token 字段必须用 `xxx` 占位，禁止保留真实值
4. **Token 失效处理**：如遇 401/403，提示用户重新生成 Token，不自动重试

### 3.2 .env 文件规范

生成的爬虫/飞书存储代码必须从 `.env` 读取 Token，示例：

```python
# ✅ 正确：从 .env 读取
import os
from dotenv import load_dotenv
load_dotenv()
feishu_token = os.getenv("FEISHU_PERSONAL_BASE_TOKEN")  # 从 .env 读取
api_key = os.getenv("ALGOLIA_API_KEY")  # 从 .env 读取

# ❌ 错误：硬编码 Token（禁止）
# feishu_token = "cli_xxxxxxxxxxxxx"  # 禁止！
# api_key = "sk-xxxxxxxxxxxxxxx"  # 禁止！
```

### 3.3 日志脱敏

生成的代码禁止在 print/log 中输出完整 Token：

```python
# ✅ 正确：日志只显示前 6 位 + 后 4 位
print(f"Using API Key: {api_key[:6]}...{api_key[-4:]}")

# ❌ 错误：完整输出（禁止）
# print(f"Using API Key: {api_key}")  # 禁止！会泄露 Token
```

## 4. 自动化脚本安全提示

涉及 .bat 自动化脚本（参考 [bat-template-spec.md](../asset-templates/bat-template-spec.md)）必须：

### 4.1 生成前必须告知 6 项副作用

| 副作用类型 | 说明 |
|----------|------|
| 文件覆盖 | .bat 执行会覆盖输出目录中同名文件 |
| 凭证消耗 | 调用飞书/外部 API 会消耗 Token 配额 |
| 系统资源 | 批量处理会占用 CPU/内存/磁盘 |
| 定时执行 | 如配置 Task Scheduler 会按计划自动运行 |
| 网络外发 | .bat 调用的脚本会向外部服务发请求 |
| 执行权限 | .bat 可能需要管理员权限运行 |

### 4.2 生成前必须等待用户确认

- **确认话术**：`我已了解上述 6 项副作用，确认生成 .bat 模板`
- **铁律**：用户未明确确认前，禁止生成 .bat 文件

### 4.3 生成后必须提供备份建议（v3.4.1 新增）

- **提示话术**：`📦 建议 .bat 执行前先备份关键数据：① 输出目录复制到 backup_<date>/ ② 数据库先 snapshot ③ 飞书表先导出 CSV`
- **模板内置**：.bat 模板必须包含 `BACKUP_DIR` 变量，默认备份到 `backup_%date%/`

## 5. 来源声明

- **v3.4.1**：安全合规边界首次引入，回应 ClawHub SkillSpector v3.2.0 的 Credentials concern 维度
- **v3.4.2**：从 SKILL.md 外迁到本文件，回应 SKILL.md 行数超 300 行硬门禁；同步强化"二次脱敏铁律"和"日志脱敏"规范
