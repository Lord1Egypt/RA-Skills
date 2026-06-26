# MCP工具清单

> 调用原则：先用 `*_get_info` 查询接口参数定义，再用 `*_get_data` 获取实际数据

## 股票基础信息

### datayes-stock-info-mcp

- **工具名：**stock_info_get_info
- **功能：**股票基础信息数据接口查询，获取上市公司证券信息、公司概况、员工构成、管理层、实控人等参数定义
- **调用示例：**`stock_finoper_get_info(api_name="getEquOperData")`



- **工具名：**stock_info_get_data
- **功能：**  获取股票基础信息实际数据（证券信息、公司概况、员工构成、管理层、实控人等）
- **调用示例：**`stock_finoper_get_data(api_name="getEquOperData", api_parameters={"ticker": "600519"})`

## 股票财务与经营

### datayes-stock-finoper-mcp

- **工具名：**stock_finoper_get_info
- **功能：**财务与经营数据接口查询，获取利润表、资产负债表、现金流量表、杜邦分析等参数定义
- **调用示例：**`stock_finoper_get_info(api_name="getFdmtISLT2018")`



- **工具名：**stock_finoper_get_data
- **功能：**  获取财务报表及经营数据实际值（合并利润表/资产负债表/现金流/业绩预告等）
- **调用示例：** `stock_finoper_get_data(api_name="getFdmtISLT2018", api_parameters={"ticker": "600519", "reportDate": "2024-12-31"})`

## 股票行情与交易

### datayes-stock-mkt-mcp

- **工具名：**stock_mkt_get_info
- **功能：**行情与交易数据接口查询，获取日/周/月行情、资金流向、融资融券、龙虎榜等参数定义
- **调用示例：**`stock_mkt_get_info(api_name="getMktEqud")`



- **工具名：**stock_mkt_get_data
- **功能：**  获取行情与交易数据实际值（股票行情、估值指标、技术指标、大宗交易等）
- **调用示例：**  `stock_mkt_get_data(api_name="getMktEqud", api_parameters={"ticker": "600519", "beginDate": "2026-05-01", "endDate": "2026-05-09"})`

## 股票股本股东

### datayes-stock-eqhld-mcp

- **工具名：**stock_eqhld_get_info
- **功能：**股本股东数据接口查询，获取十大股东、股权质押、限售解禁、机构持股等参数定义
- **调用示例：**`stock_eqhld_get_info(api_name="getEquShTen")`



- **工具名：**stock_eqhld_get_data
- **功能：**获取股本股东数据实际值（股东结构、持股变动、股本变化、质押解禁等）
- **调用示例：**`stock_eqhld_get_data(api_name="getEquShTen", api_parameters={"ticker": "600519"})`

## 股票重大事项

### datayes-stock-event-mcp

- **工具名：**stock_event_get_info
- **功能：**重大事项数据接口查询，获取分红、增发、股权激励、股份回购、IPO等参数定义
- **调用示例：**`stock_event_get_info(api_name="getEquDivPIT")`



- **工具名：**stock_event_get_data
- **功能：**  获取重大事项数据实际值（分红送配、再融资、诉讼违规、员工持股计划等）
- **调用示例：**`stock_event_get_data(api_name="getEquDivPIT", api_parameters={"ticker": "600519", "beginDate": "2024-01-01"})`