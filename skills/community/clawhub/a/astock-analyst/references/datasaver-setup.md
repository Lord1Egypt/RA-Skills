# Datasaver 安装与配置指南

Datasaver 是本 Skill 的可选增强组件，用于从东方财富网页提取资金流向、千股千评等
curl 无法直接获取的数据（需要登录态或 JS 渲染）。

**不安装 Datasaver 时，核心分析功能（行情/K线/指标/五关论证/复盘）完全正常。**
仅在需要资金流向超大单、千股千评控盘度时才需要此组件。

---

## 一、安装步骤

### 1. 安装 Datasaver Chrome 插件
参照官方帮助文档完成插件安装与账号注册：
https://docs.qq.com/doc/DT3FZT09Zd254c1Bv

安装完成后，浏览器右上角会出现 Datasaver 插件图标，确认显示为**已连接**状态。

### 2. 获取 dev_id 和 api-key
登录 Datasaver 平台后，在个人设置页面获取：
- `dev_id`：你的开发者 ID
- `api-key`：你的 API 密钥

**安全提示：这两个凭证是你的个人身份，不要分享给他人，不要提交到代码仓库。**

### 3. 配置 MCP 连接
在工作区根目录（`~/.openclaw/workspace/`）的 `.mcp.json` 文件中添加：

```json
{
  "mcpServers": {
    "browser": {
      "type": "http",
      "url": "https://datasaver.deepminingai.com/api/v2/{dev_id}/mcp",
      "headers": {
        "Authorization": "Bearer {api-key}"
      }
    }
  }
}
```

将 `{dev_id}` 和 `{api-key}` 替换为你的真实值。

### 4. 验证连接
配置完成后，可以用以下方式验证（把 URL 中的占位符替换成你的真实 dev_id 和 api-key）：

```bash
curl -s --ipv4 -H "Authorization: Bearer {你的api-key}" \
  "https://datasaver.deepminingai.com/api/v2/{你的dev_id}/mcp" 2>&1 | head -5
```

---

## 二、在股票分析中的使用方式

配置完成后，通过 datasaver 的 `chrome_navigate` + `chrome_get_web_content` 工具抓取东方财富数据页面。

### 资金流向（超大单/大单/中单/小单净额）

```
目标页面：https://data.eastmoney.com/zjlx/{股票代码}.html
示例：https://data.eastmoney.com/zjlx/603893.html（瑞芯微）
```

提取后关注字段：
- 超大单净额（单笔>200万）
- 大单净额（单笔50~200万）
- 中单净额（单笔10~50万）
- 小单净额（散户）

判断逻辑：
- 超大单净买 → 机构/主力进场
- 超大单净卖 + 中小单净买 → 主力出货，散户接盘，危险
- 连续多日超大单净流出 → 机构撤退，不入场

### 千股千评（控盘度/主力成本/次日概率）

```
目标页面：https://data.eastmoney.com/stockcomment/stock/{股票代码}.html
示例：https://data.eastmoney.com/stockcomment/stock/603893.html
```

提取后关注字段：
- **综合评分**（满分100）：60分以上才考虑
- **控盘度**：越高说明主力越集中，不容易大起大落
- **主力成本**：低于当前价说明主力盈利，高于则套牢
- **次日上涨概率**：参考，不是绝对依据

### 融资融券（判断杠杆情绪）

```
目标页面：https://data.eastmoney.com/rzrq/detail/{股票代码}.html
```

提取后关注：
- 融资余额持续上升 → 市场情绪乐观，但也意味着高位风险
- 融券余额大幅增加 → 有机构做空

---

## 三、常见报错处理

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| 设备不存在 / device not found | 插件未安装或未连接 | 检查插件是否安装并启用 |
| 设备离线 / device offline | 浏览器未打开或插件未激活 | 打开浏览器，确认插件图标已连接 |
| 401 Unauthorized | api-key 错误或过期 | 检查 .mcp.json 中的 api-key |
| 开发者不存在 | dev_id 配置错误 | 检查 .mcp.json 中的 dev_id |
| 连接超时 | 网络问题 | 检查网络，稍后重试 |
| 页面内容为空 | JS 渲染未完成 | 导航后等待 2~3 秒再提取 |

**通用排查步骤：**
1. 确认 Chrome 已打开，Datasaver 插件图标显示为已连接
2. 检查 `.mcp.json` 中 dev_id 和 api-key 是否正确（无多余空格/换行）
3. 重启浏览器或重新启用插件
4. 仍无法解决，参照：https://docs.qq.com/doc/DT3FZT09Zd254c1Bv

---

## 四、不用 Datasaver 的替代方案

如果暂时无法配置 Datasaver，以下数据可用替代方式获取（功能有限）：

| 数据 | 替代方案 |
|------|----------|
| 资金流向大概 | 通过成交量+OBV间接判断，精度较低 |
| 千股千评评分 | 用涨跌量不对称比+OBV综合替代 |
| 融资融券 | 暂无替代，跳过此项分析 |

核心的五关论证、技术指标、期望值计算均不依赖 Datasaver，不影响主要分析流程。
