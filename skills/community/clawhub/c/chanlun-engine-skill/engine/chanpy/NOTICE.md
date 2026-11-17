本目录为 [Vespa314/chan.py](https://github.com/Vespa314/chan.py) 的精简打包版（commit 429d6ed，MIT License，版权归原作者 Memos）。
仅保留缠论结构计算所需模块（移除了绘图/示例/回测演示），代码本体做过安全化补丁（2026-08-24）：移除 ChanConfig.py/BSPointConfig.py 的 exec 配置装载（改直接调用，行为等价，回归输出逐字节一致）、Chan.py 的任意模块动态 import（改白名单）与 pickle 序列化辅助（移除）。其余未动。LICENSE 原文见本目录。
打包进本技能的原因：国内网络环境下运行时 git clone 不可达，且技能市场安全扫描不允许运行时远程拉取代码。
