# Changelog

## v1.0.2 (2026-05-10)

### 🏗️ LLM 多平台抽象

- **统一 LLM 配置**：`config.py` 移除 DashScope 专属字段（`dashscope_api_key`/`dashscope_base_url`/`dashscope_model`），改为 `LLM_API_KEY` + `LLM_BASE_URL` + `LLM_MODEL` 通用配置
- **统一配置**：移除 `DASHSCOPE_API_KEY` 等平台专属 Key，统一使用 `LLM_API_KEY` + `LLM_BASE_URL` + `LLM_MODEL` 三个环境变量
- **重构 `tag_extractor.py`**：`extract_tags_llm()` 改为 OpenAI 兼容接口，支持 DeepSeek / DashScope / OpenAI / Groq 等任意平台
- **LLM 可用性标记**：config 新增 `llm_available` 属性，一次判断即可决定是否启用 LLM
- **升级日志**：LLM 调用增加模型名称打印（如 `deepseek-v4-pro`），便于排错

---

## v1.0.1 (2026-05-07)

### 🔒 安全修复（ClawScan 扫描）

- **Cookie 域隔离**: `base_fetcher.py` 重构 `_load_cookies()` 保留 domain 字段，新增 `_apply_cookies_for_url(url)` 按目标域名过滤，防止登录态泄露到非目标站点
- **URL 严格校验**: `platform_detector.py` 改用 `urllib.parse.urlparse` + 白名单匹配 hostname，拒绝路径拼接攻击（如 `https://evil.com/mp.weixin.qq.com/...`）
- **依赖版本锁定**: `requirements.txt` `>=` → `==` 精确版本，降低供应链风险

### 📝 文档

- **安全说明**: SKILL.md 新增「安全与隐私」章节，披露 LLM 数据外发、Cookie 隔离、权限最小化等安全边界
- **扩展指南**: 更新平台扩展步骤（`ALLOWED_HOSTS` 替换旧正则描述）

---

## v1.0.0 (2026-05-07)

### 🎯 正式发布

- **文档精简**: SKILL.md 重写为精简扼要格式，层次清晰，面向用户与 Agent
- **版本标注**: 统一版本号为 v1.0.0（SKILL.md metadata、README、CHANGELOG）
- **清理冗余**: 移除 `tests/` 目录、`__init__.py`、`__pycache__/` 缓存文件
- **安全加固**: 消除 `config.py` 中 `DEBUG` 变量暴露到全局模块命名空间
- **SKILL.md**: 新增 Notion 数据库字段说明、扩展平台指南、模块调用示例

---

## v0.2.0 (2026-05-06)

### ✨ 关键词提取优化

- **LLM 优先策略**: 关键词提取优先调用 DashScope LLM 理解文章核心内容
- **智能降级**: LLM 失败或未配置 `DASHSCOPE_API_KEY` 时自动降级为本地词频分析
- **标题上下文**: 传递文章标题给 LLM，提升关键词提取准确度
- **超时重试**: 3 次重试机制（60s → 90s → 120s），兼容 429/5xx 错误
- **新增配置**: `.env.example` 添加 `DASHSCOPE_API_KEY`/`DASHSCOPE_BASE_URL`/`DASHSCOPE_MODEL` 说明

### 📝 文档更新

- SKILL.md 更新关键词提取描述（纯本地 → LLM 优先 + 降级方案）

---

## v0.1.1 (2026-05-01)

### 🐛 Bug 修复

- **关键词提取**: 移除 LLM API 依赖，改为纯本地词频方案，解决 Coding Plan Key 不能用于后端脚本的合规问题
- **知乎抓取**: 修复 `#HttpOnly` 前缀导致 Cookies 解析失败（base_fetcher.py）
- **知乎清理**: 移除知乎 HTML 中 64K+ CSS 噪音（内嵌 `<style>` 标签、动态 class、JS 属性）
- **知乎图片提取**: 修复图片选择器不匹配问题，提取 `_r.jpg` + `_720w.jpg` 双变体 URL
- **Notion 存档**: 修复单段文本超过 2000 字符导致 400 错误，段落/引用/代码块自动拆分
- **Notion 图片**: 修复知乎图片 SVG 占位符未被跳过的问题，增加 `data-original` 优先级

### 🔧 优化

- **Cookies 路径**: 默认路径改为 `~/.cookies/<platform>_cookies.txt`，可通过环境变量覆盖
- **安全文档**: SKILL.md 新增完整的「安全与隐私说明」章节
- **SKILL.md**: 更新关键词提取描述（LLM → 纯本地词频）

---

## v0.1.0 (2026-04-29)

### ✨ 初始版本

- 多平台支持：微信公众号、小红书、豆瓣、知乎
- 图片上传阿里云 OSS
- 关键词提取（LLM + 词频降级方案）
- 一键存档到 Notion
