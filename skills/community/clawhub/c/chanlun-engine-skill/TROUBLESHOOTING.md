# 排障速查

| 症状 | 原因 | 解决 |
|---|---|---|
| 提示 Python 版本太老 / python_too_old | 引擎需要 Python 3.11+ | 对你的 AI 助手说"帮我安装 Python 3.11"；Windows 也可去 python.org 下载安装包 |
| 找不到 python / spawn python 失败 | 本机没装 Python 或未进 PATH | 同上；WorkBuddy 用户可在 设置→技能中心 手动指定 Python 解释器路径 |
| akshare 未取到数据 / 连接被断开 | 免费源(东财)对部分网络环境不稳 | 脚本会自动切新浪备用源；仍失败就稍后重试，或关掉代理，或申请同花顺 key 走官方源 |
| 提示缺 HITHINK_FINANCE_API_KEY | 想用同花顺官方源但没配 key | 按 references/getting-started.md 三步申请(同花顺账号登录即可)，或改用免费源 --source akshare |
| 同花顺接口 code=2001 | key 无效或过期 | 去 fuyao.aicubes.cn/admin 重新签发 |
| 同花顺接口 code=4001 | 触发限流 | 等几秒重试，别并发刷 |
| K线不足120根拒绝计算 | 上市太短或取数区间太小 | --years 拉长；次新股结构本来就不可靠，属正常保护 |
| 判定和昨天不一样了 | 最新信号是"当前帧"语义 | 正常现象：未确认信号随新K线可能消失，这正是引擎标注 sure:false 的原因 |
| 全市场扫描跑不动 | 需要同花顺 key + 本地数据库，且下载量大 | 在服务器或专用机跑，日常个股分析用不到它 |
