---
name: amber_energy_manager
description: "Access real-time electricity prices, forecasts, and site details from Amber Electric. Supports fetching current price data, 24-hour forecasts, and account site lists. 获取 Amber Electric 的实时电价、预测电价及站点信息。"
parameters:
  action:
    type: string
    description: "The action to perform. Options: 'get_sites' (list sites), 'get_current_price' (get current price), 'get_forecast' (get price forecasts). 执行的操作：获取站点、实时电价或预测。"
  site_id:
    type: string
    description: "The unique ID of the site. Required for price/forecast actions. 站点的唯一 ID (执行实时价格或预测时必填)。"
handler: |
  const baseUrl = 'https://api.amber.com.au/v1';
  const headers = {
    'Authorization': `Bearer ${process.env.AMBER_API_KEY}`,
    'Accept': 'application/json'
  };

  if (params.action === 'get_sites') {
    const res = await fetch(`${baseUrl}/sites`, { headers });
    return await res.json();
  }

  if (params.action === 'get_current_price') {
    if (!params.site_id) return { error: "site_id is required" };
    const res = await fetch(`${baseUrl}/sites/${params.site_id}/prices/current`, { headers });
    return await res.json();
  }

  if (params.action === 'get_forecast') {
    if (!params.site_id) return { error: "site_id is required" };
    const res = await fetch(`${baseUrl}/sites/${params.site_id}/prices/forecasts`, { headers });
    return await res.json();
  }

  return { error: "Invalid action" };
---

# Amber Electric Energy Assistant | 能源助手

This skill enables OpenClaw to access wholesale electricity price data from Amber Electric (Australia).
此技能允许 OpenClaw 接入澳洲 Amber Electric 的批发电价数据。

### Key Features / 主要功能
- **View Sites / 查看站点**: Retrieve the NMI and Site ID(s). 获取你名下的 NMI 和站点 ID。
- **Real-time Pricing / 实时价格**: Get current price levels (e.g., `extremelyLow`, `spike`). 获取当前电价等级和具体数值。
- **Price Forecasting / 电价预测**: View 24-hour price trends. 获取未来 24 小时的价格趋势。

### Configuration / 配置要求
需要在环境变量或 `openclaw.json` 中配置：
`AMBER_API_KEY`: Your personal Amber API token. 你的 Amber API 令牌。
