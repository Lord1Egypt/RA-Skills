# TOOLS.md - 家语（Jiayu）工具配置

> 版本: v2.0.0 | 创建日期: 2026-06-07

---

## 企微群配置

### Webhook URL（如果需要直接调用企微API）
- **配置方式**：在 `openclaw.json` 或环境变量 `WECOM_WEBHOOK_URL` 中配置
- **状态**：待用户在首次使用时配置

### 群ID
- **配置方式**：在 `family/members.json` 中配置家庭群ID
- **状态**：待用户在首次使用时配置

---

## 腾讯文档配置（可选）

### 用途
- 长期保存家庭记录
- 家庭成员协同编辑时间轴

### 配置方式
- 依赖 `tencent-docs` skill
- 用户需要在首次使用时完成腾讯文档授权

---

## 日历接入（后续迭代）

### 用途
- 检测家庭活动时间冲突
- 自动建议无冲突时间

### 支持的平台
- 腾讯日历（待接入）
- 飞书日历（待接入）

---

## 本地文件路径

### 数据存储路径
- **根目录**：`family/`（相对于workspace根目录）
- **成员信息**：`family/members.json`
- **家庭时间轴**：`family/timeline/`
- **家语时刻记录**：`family/memory/`
- **成员成长档案**：`family/growth/`
- **家庭传承资料**：`family/legacy/`
- **决策库**：`family/decisions/`
- **记录模板**：`family/templates/`

---

## 环境变量（可选）

| 变量名 | 用途 | 默认值 |
|--------|------|--------|
| `WECOM_WEBHOOK_URL` | 企微Webhook URL | 无 |
| `TENCENT_DOCS_TOKEN` | 腾讯文档Token | 无 |
| `JIAYU_DEBUG` | 调试模式 | false |

---

*本文件版本：v2.0.0 | 最后更新：2026-06-07*
