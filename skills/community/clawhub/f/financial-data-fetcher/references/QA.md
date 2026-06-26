# # Q：运行的python文件可不可以随便放，不一定在PYPlugins\user目录下？

A： 可以。在import tqcenter前添加通达信安装目录\PYPlugins\user这个绝对路径。

```python
import sys
sys.path.append('C:/new_tdx64/PYPlugins/user')
from tqcenter import tq
tq.initialize(__file__)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

# # Q：无法内部执行策略之如何把python路径添加到PATH中

A： 内部执行python策略时，会寻找用户设定的默认python解释器执行python策略，所以必须在操作系统<高级系统设置>---&gt;环境变量设置里，配置python路径。
![](https://help.tdx.com.cn/quant/uploads/mindoc/images/m_f25c88b591329593ed4e0808ace92059_r.png)
 如图所示，环境变量中分为用户变量和系统变量，都有PATH，在这两个中添加python路径都可生效，但是用户变量的优先级高于系统变量，所以图中仅在用户变量中的PATH中添加python路径。
![](https://help.tdx.com.cn/quant/uploads/mindoc/images/m_c51b67fae608d8af460f59310b0af99e_r.png)
 图中可见，PATH中可以配置多个版本的python，但是最后生效为最上面的，每个版本的python需要配置两个路径。

# # Q：出现类似以下的报错怎么办？

```python
FileNotFoundError: Could not find module 'F:\tdx\new_tdx_600\PYPlugins\TPythClient.dll' (or one of its dependencies). Try using the full path with constructor syntax.
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

A： 这通常是TPythClient.dll缺少依赖库导致的，请检查TPythClient.dll同目录下（../PYPlugins/）是否有tdxrpcx64.dll，通常是杀毒软件误杀此dll导致，需要重装或给予白名单确保tdxrpcx64.dll不会被杀毒软件误杀。

# # Q：外部运行的py文件报已经存在运行的，怎么处理？

A： 请在TQ策略管理器找到这个正在运行的已经运行出错的OutSide策略，点删除策略删除它。

# # Q：菜单一直显示“正在开启TQ策略..”

A： 是否有以下这个提示？如果有，请允许访问。

![](https://help.tdx.com.cn/quant/uploads/mindoc/images/m_455b7bd3b841ab135979a77f0700ab9a_r.png)

# # Q：获取的数据count=5，返回的指标值怎么前面的是none？

![](https://help.tdx.com.cn/quant/uploads/mindoc/images/m_07755b2e850d812e54e273ed63993d19_r.png)
 A： formula_set_res = tq.formula_set_data_info(stock_code=stock,stock_period='1d', count=4,dividend_type=1)这里的count=4 是获取最近4根k线的数据用于计算指标，所以最近4根k的数据
 ZF:(C-REF(C,1))/REF(C,1)*100;这个式子的只能计算出 最后4根k的涨幅值。
 所以在获取指标值时注意获取k线数目要覆盖到最大参数值，否则计算结果会为空。

# # Q：为什么同一个选股公式，用formula_process_mul_xg选股的结果比客户端条件选股中得到的结果少？

A： 请确认formula_process_mul_xg中的count参数是否合理？数据个数要满足公式计算中的数据要求。客户端的条件选股中使用了所有的本地数据。
