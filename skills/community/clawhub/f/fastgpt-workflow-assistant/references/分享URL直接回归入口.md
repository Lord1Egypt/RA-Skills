# 分享URL直接回归入口

## 新对话不依赖聊天历史
通用执行器 scripts/run_share_api_regression.py 已提供POST请求体、share-only、会话隔离、SSE解析、限速与结果断言。新入口 scripts/run_share_url_regression.py 负责从用户分享URL提取origin/shareId，读取本机有证据的实例协议，构造调用命令；不需要用户每次再提供接口URL、appId或F12抓包。

查询顺序：显式 --registry > 环境变量 FASTGPT_SHARE_REGISTRY > 用户主目录 .config/fastgpt-workflow-assistant/share-instances.json。配置不放在专家/技能缓存内，所以重新导入、开新对话或换项目仍可复用；换电脑/用户账户需迁移本机配置。实例配置含接口来源证据，属于本地项目资料，不进入公开技能包。

先核对现有实例协议和历史成功调用，再做一次新的低影响冒烟。历史HTTP200只证明当时接口可用，不证明当前应用正确；成功后继续已授权用例。协议变化、鉴权异常、非SSE或版本不匹配时保存首次失败，再查本地其他证据/HTTP公开资料；浏览器最后降级，不反复要求抓包。

## 调用方法
```text
python scripts/run_share_url_regression.py "https://host/chat/share?shareId=USER_SHARE_ID" smoke-cases.json restricted/smoke-results.json
python scripts/run_share_url_regression.py "https://host/chat/share?shareId=USER_SHARE_ID" smoke-cases.json restricted/smoke-results.json --execute
```
第一条只检查实例配置与用例、显示实际计划，不联网。第二条在用户已经要求测试的范围内执行；--execute是命令运行模式，不是要求用户再次口头确认。先生成一个“你好”等低影响用例的smoke-cases.json；运行成功再生成其他业务边界用例，使用新的结果路径，保留首次失败。不要直接复跑旧应用的业务用例。
已有用例需符合现有run_share_api_regression.py的case_id/turns与期望契约；按实际JSON生成，不把接口响应状态当业务通过。该入口使用同源已登记路径，不做路径扫描，不读取浏览器Cookie、密码或本地存储，不伪造appId。

## 注册表格式与适用边界
参照 assets/share-instances.example.json。每条记录精确匹配origin（包含协议/端口），以 endpoint_path/mode/protocol 指定证据支持的调用方式，evidence记录核验日期、来源文件与哈希。没有实例证据的主机不可套用另一公司的接口；未知实例应先自行寻找本地配置/历史调用和公开协议资料。
--share-only代表“不发送appId”，不等于所有实例或分享链接都无需额外鉴权。需要额外鉴权/访问码时按实例实际契约扩展适配，不能绕过权限；当前简化入口仅支持本机已登记的fastgpt-share-sse/share-only配置。

## 分享URL、接口和产物不能混用
分享URL用于确定目标；聊天API用于发送测试；本地workflow JSON用于核对预期；结果报告/调用计划不能导入平台。注册表不是工作流JSON也不是业务接口配置。
调用分享聊天API与启用资产/ping业务接口分开。当前测试保持contractReady关闭；即使收到普通未就绪回复，也不能凭答案证明隐藏HTTP节点没执行，缺运行详情时引导后台日志。工作流线上导入/发布状态、分享渠道版本、当前协议冒烟与功能回归分别报告。
