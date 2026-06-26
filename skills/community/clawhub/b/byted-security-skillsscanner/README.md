# Volcengine 技能安全扫描器

## 简介

通过将技能目录打包并上传火山引擎安全扫描服务进行扫描，审计工作区中的其他技能是否存在潜在的安全风险。

## 何时使用

- **审计**：定期扫描所有技能以确保符合安全策略。
- **开发**：在开发过程中检查自己的技能。
- **要求**：必须确保目标技能包含 `SKILL.md` 文件，因为它是扫描的主要输入。

## 配置方式

### 方式一：OpenClaw 全局配置文件（推荐）

推荐在 OpenClaw 的全局配置文件 `openclaw.json` 中进行配置，这样无需每次手动设置环境变量，且能更安全地管理凭证。

**配置文件路径：**
```
~/.openclaw/openclaw.json
```

**配置内容：**
在 `skills.entries` 字段下添加以下内容：

```json
{
  "skills": {
    "entries": {
      "volcengine_skills_scanner": {
        "enabled": true,
        "env": {
          "VOLC_ACCESSKEY": "",
          "VOLC_SECRETKEY": ""
        }
      }
    }
  }
}
```

### 方式二：OpenClaw UI 配置

在 OpenClaw UI 中添加配置：
1. 进入【配置】 - 【Skills】
2. 添加对应的 Entries 以及 env 变量

### 方式三：环境变量配置

如果需要临时使用，可以直接设置环境变量：

```bash
export VOLC_ACCESSKEY="your-access-key"
export VOLC_SECRETKEY="your-secret-key"
export VOLC_REGION="cn-north-1"  # 可选，默认 cn-north-1
```

## 使用方式

使用 `scripts/scan.py` 脚本执行扫描：

```bash
python3 scripts/scan.py --name "skill-name" --path "/path/to/skill"
```

**参数说明：**
- `--name`: 技能名称（用于标识扫描任务）
- `--path`: 技能目录或压缩包路径（支持 ~ 展开用户主目录）

**示例：**
```bash
python3 scripts/scan.py --name feishu --path ~/.openclaw/workspace/skills/feishu-docs
```

## 输出格式

脚本会自动打包目录（如果提供的是目录）并上传，输出包含扫描结果的 JSON 数组。

## 环境变量说明

| 变量名 | 说明 | 是否必须 | 默认值 |
|--------|------|----------|--------|
| `VOLC_ACCESSKEY` | 火山引擎 Access Key | 是 | - |
| `VOLC_SECRETKEY` | 火山引擎 Secret Key | 是 | - |
| `VOLC_REGION` | 火山引擎区域 | 否 | cn-north-1 |
| `SCAN_BASE_URL` | 自定义扫描服务地址 | 否 | - |

## 获取访问凭证

参考火山引擎官方文档获取 AK/SK：
[用户指南 - 获取访问密钥](https://www.volcengine.com/docs/6291/65568?lang=zh)
