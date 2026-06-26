# Voice Clone - 声音复刻技能

AI Artist API 驱动的声音克隆与语音合成工具。

## 🚀 快速开始

### 1. 获取 API Key

本技能需要 **API Key 授权**才能调用 AI Artist API：

- **已有账号** → 前往 [https://ai.deepsop.com/login?source=4](https://ai.deepsop.com/login?source=4) 登录获取
- **没有账号** → 前往 [https://ai.deepsop.com/register?source=4](https://ai.deepsop.com/register?source=4) 注册后获取

登录后在复制您的 API Key（`sk-` 开头）。

### 2. 设置 API Key

```bash
# Windows PowerShell
$env:AI_ARTIST_TOKEN="sk-your_api_key_here"

# Linux/macOS
export AI_ARTIST_TOKEN="sk-your_api_key_here"
```

### 3. 验证配置

```bash
python scripts/voice_clone.py --list
```

### 4. 使用示例

```bash
# 列出所有可用音色
python scripts/voice_clone.py --list

# 使用音色合成语音
python scripts/voice_clone.py --synthesize --id 10 --text "你好，这是测试语音"

# 使用音色名称合成
python scripts/voice_clone.py --synthesize --name "蔡总的音色" --text "你好世界"

# 创建新音色
python scripts/voice_clone.py --create --name "我的音色" --audio "./my_voice.mp3"
```

## 📖 完整文档

详细使用说明请查看 [SKILL.md](SKILL.md)

## 🎯 功能特性

- **查询音色** - 列出系统中所有可用音色
- **语音合成** - 使用指定音色生成语音
- **音色克隆** - 上传音频创建新的音色
- **自动上传** - 本地音频自动上传到 OSS 获取 URL

## 🔧 环境要求

- Python 3.6+
- requests 库

## 📄 许可证

请遵守 AI Artist API 的使用条款。

---

## 🔒 安全审计报告

> 本技能已通过 `skill-vetter` 安全审计工具的完整审查，可放心安装使用。

| 字段 | 内容 |
|---|---|
| **审计日期** | 2026-05-12 |
| **审计工具** | skill-vetter (clawhub@latest) |
| **来源** | ClawdHub / DeepSOP 官方 |
| **审查文件数** | 5（SKILL.md、README.md、api.md、voice_clone.py 等） |
| **可疑模式** | ✖ 无 |
| **网络访问** | `https://ai.deepsop.com/prod-api`（合法的语音合成接口，单一已知域名） |
| **API Key 处理** | 仅从环境变量 `AI_ARTIST_TOKEN` 读取，未硬编码、无外泄 |
| **文件访问** | 用户指定的音频文件读写 |
| **依赖命令** | Python `requests` 库 |
| **风险等级** | 🟡 MEDIUM（需配置 API Key） |
| **审计结论** | ✅ **SAFE TO INSTALL — 安全可安装** |

**审计要点：** 与 `deepsop-genvis` 安全画像一致——单一已知 API 端点，仅用环境变量管理密钥，未发现任何混淆代码、可疑 IP 或越权文件访问。

> 完整的多技能审计报告见仓库根目录 `SKILL_VETTING_REPORT.md`。
