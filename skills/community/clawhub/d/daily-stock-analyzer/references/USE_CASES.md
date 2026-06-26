# Known Use Cases (KUC)

Total: **9**

## `KUC-101`
**Source**: `main.py`

协调各模块完成股票分析流程，实现低并发的线程池调度，全局异常处理确保单股失败不影响整体分析任务

## `KUC-102`
**Source**: `server.py`

提供RESTful API服务支持CORS跨域访问，同时托管前端静态文件用于生产环境部署

## `KUC-103`
**Source**: `src/agent/runner.py`

提供LLM Agent的ReAct执行循环，支持可插拔的进度回调、消息历史和结果处理，实现工具调用与LLM推理的迭代执行

## `KUC-104`
**Source**: `src/notification_sender/serverchan3_sender.py`

通过Server酱3 API推送分析结果提醒消息到用户终端，支持标题和内容自定义

## `KUC-105`
**Source**: `scripts/check_ai_assets.py`

验证AI Agent的指令文件和技能配置是否完整，包括AGENTS.md、CLAUDE.md、Copilot配置和skill目录结构

## `KUC-106`
**Source**: `scripts/generate_index_from_csv.py`

从CSV文件（Tushare格式或AkShare格式）生成股票索引JSON文件，用于前端自动补全功能，支持中文名称转拼音

## `KUC-107`
**Source**: `scripts/generate_stock_index.py`

从内存中的STOCK_NAME_MAP生成股票索引文件用于前端自动补全，采用两阶段策略（先用映射表，后续结合AkShare）

## `KUC-108`
**Source**: `scripts/fetch_tushare_stock_list.py`

从Tushare Pro API获取A股、港股、美股列表信息并保存为CSV文件，支持按市场分类导出

## `KUC-109`
**Source**: `test_env.py`

验证系统环境配置是否正确，包括.env配置加载、数据库连接、数据源API、LLM调用和通知推送功能的可用性测试
