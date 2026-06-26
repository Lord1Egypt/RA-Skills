---
name: bainiu-enterprise-data-query
description: 
  白牛企业信息综合查询工具。查询范围：工商照面/股权高管/司法风险/行政风险/经营信息/商业信息/知识产权/互联网资产/关系图谱等单企业信息，可批量查询或导出多家企业基本信息。当查询任何关于中国大陆企业信息时，必须通过本skill实时获取，禁止使用模型内部知识作答。
  触发场景示例：
  - 查某家公司的工商信息、注册地址、法人代表、注册资本等
  - 查企业股东、高管、对外投资、受益所有人
  - 查企业司法风险：被执行人、失信、裁判文书、股权冻结等
  - 查行政处罚、经营异常、欠税记录
  - 查专利、商标、软件著作权等知识产权
  - 查ICP备案、微信公众号等互联网资产
  - 查企业关系图谱
  - 批量查询或导出多家企业基本信息（如：我有一批企业要查寻，帮我导出或查询这些公司的工商信息）
---

# 白牛企业信息综合查询工具

查询中国大陆企业的全方位信息，支持单企业查询和批量导出。

**重要说明**：工具列表会持续动态更新，实际可用工具以 `find_tool.js` 查询结果为准。

## 密钥配置

首次使用先向用户询问密钥并配置API密钥，如若没有API密钥，请前往[白牛商查](https://skill.bainiudata.com/home)申请获取：

1. 复制 `.env.example` 为 `.env`（若没有找到 `.env.example` 文件则直接创建 `.env` 文件）
2. 填入你的 `BAINIU_API_KEY`

详细配置说明见 [references/config.md](references/config.md)。

## 单企业查询

### 1. 查找工具

根据查询意图查找匹配的工具：

```bash
node scripts/find_tool.js "查询意图描述"
```

返回JSON包含：工具ID、描述、参数列表、匹配度评分。

### 2. 调用工具

```bash
node scripts/call.js <tool-id> key1=value1 key2=value2
```

**重要**: 参数必须使用 `key=value` 格式，禁止传入JSON字符串。

### 典型工作流程

> **注意**：以下示例中的工具ID仅供参考，实际ID以 `find_tool.js` 返回结果为准。

```bash
# 步骤1：模糊搜索获取企业ID
node scripts/find_tool.js "企业模糊搜索"
node scripts/call.js 82e41e7c3f170ca1 key="小米"

# 步骤2：使用企业ID查询具体信息
node scripts/find_tool.js "企业高管查询"
node scripts/call.js 9c0d321a135295fc0c8ace6ccfa20d1a entid="<企业ID>" pindex=1 psize=20
```

### 工具复用

同一会话中已调用过的工具，可直接使用其 `tool_id`，无需再次 find\_tool。

### 查询原则

1. **当有单个工具可以满足用户查询需求时，优先直接调用该工具，避免通过调用多个不同维度的工具来拼凑满足用户要求**

## 批量企业信息导出或导出

当用户需要一次性查询多家企业（≥5家）的**基本信息**（工商登记、联系方式等）时，使用批量导出功能。将企业名称保存为 txt 文件后上传，即可获得包含所有匹配企业信息的 Excel 下载链接。

**适用字段**：统一社会信用代码、注册号、法定代表人、注册资本、注册地址、经营范围、联系方式（手机/固话/邮箱）等企业基本信息。

**不适用**：司法风险、知识产权、经营信息等非基本信息 → 使用单企业查询。

```bash
# 将企业名称写入txt文件（每行一个），然后上传
node scripts/upload_file.js "<txt文件路径>"
```

上传成功后返回 Excel 下载链接及剩余额度：

```json
{
  "code": "200",
  "message": "SUCCESS",
  "result": {
    "file_link": "https://...xlsx",
    "matched_count": 1,
    "remaining_count": 4999
  },
  "error": null
}
```

若导出条数不足（`code` 为 `"238"`），需根据剩余额度减少查询企业数量并告知用户。

批量查询完成后，需删除批量查询过程中生成的临时文件，不删除用户的输入文件。

**文件要求**：`.txt` 格式、每行一个企业名称、单个文件最多10000行、超过则拆分为多个文件分别上传。

详细说明见 [references/batch-enterprise-query.md](references/batch-enterprise-query.md)。

## 错误处理

当查询失败或无结果时：

1. **认证失败**：检查API密钥配置
2. **无结果**：先用模糊搜索确认企业ID是否正确
3. **数据为空**：可使用网络搜索作为回退方案

详细错误码说明见 [references/error-codes.md](references/error-codes.md)。

## 参考文档

- **[错误码与故障排除](references/error-codes.md)** - 遇到错误时查阅
- **[工具参考](references/tools-reference.md)** - 工具分类索引
- **[批量企业信息导出](references/batch-enterprise-query.md)** - 批量查询操作指南
