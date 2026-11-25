# 浏览器方法

安装并启动 Easy WebBridge：[GitHub](https://github.com/xxjrq/easy-webbridge)，[Gitee 备用](https://gitee.com/xxjrq/easy-webbridge)。它只连接本机已授权浏览器，不是内容数据 API。

通过 `GET /v1/browsers` 获取在线环境。请求已提供 `browserId` 时精确匹配；未提供且只有一个在线浏览器时自动选择；未提供且多个在线时停止，让用户运行 `list` 后明确选择。绝不广播，也不按浏览器名称猜测。

每次运行创建唯一任务 session，只放在命令的 `args.session` 中。同一标签组依次访问 `/hot` 和关键词搜索页；每页先核验域名、路径、页面类型和可见卡片，再执行最多三次短等待和受限滚动。采集成功或失败后，只关闭本次 session 建立的标签组；用户显式设置 `keepTab=true` 时保留。

发现登录、验证码、安全验证、风控、权限、关键词不一致、URL 不符、元素不可见或证据为空时停止并写脱敏诊断。禁止使用临时浏览器、第三方内容 API、互动操作或验证码规避。
