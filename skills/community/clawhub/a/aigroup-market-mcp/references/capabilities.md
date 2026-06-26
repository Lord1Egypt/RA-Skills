# Market MCP Capabilities

## Exposed operations in this workspace

- `current_timestamp`
- `finance_news`
- `stock_data`
- `stock_data_minutes`
- `index_data`
- `macro_econ`
- `company_performance`
- `fund_data`
- `fund_manager_by_name`
- `convertible_bond`
- `block_trade`
- `money_flow`
- `margin_trade`
- `company_performance_hk`
- `company_performance_us`
- `csi_index_constituents`
- `dragon_tiger_inst`
- `hot_news_7x24`
- `basic_info`

## Task mapping

- Single-name China equity check:
  - `stock_data`, `stock_data_minutes`, `basic_info`, `company_performance`
- Index or benchmark context:
  - `index_data`, `csi_index_constituents`
- Flow and positioning:
  - `money_flow`, `margin_trade`, `block_trade`, `dragon_tiger_inst`
- Funds and convertibles:
  - `fund_data`, `fund_manager_by_name`, `convertible_bond`
- Macro and news:
  - `macro_econ`, `finance_news`, `hot_news_7x24`

## Dependency

- MCP server name: `aigroup-market-mcp`
- Local launch pattern in this workspace: `npx -y aigroup-market-mcp`
- Required environment variable in this workspace: `TUSHARE_TOKEN`
