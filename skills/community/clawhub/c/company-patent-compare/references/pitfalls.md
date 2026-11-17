# 实测坑

> 真实运行中撞出来的，开跑前扫一眼，每条都能省时间和钱。

这几条是真实运行中撞出来的，每撞一次都在烧时间和钱。

**`--sort rank` 在组配式检索上会脱靶。** 实测查「BMS 充电策略」返回三元正极材料制备、LED 驱动器。**用 `--sort relation` 或不传 `--sort`**，`rank` 只在单一宽词检索时才可靠。

**宽泛关键词必须叠 IPC 收窄。** 实测「热管理」命中从千级膨胀到 **35,298 件**，前排全是电池包结构件、液冷板、整车热泵。这种命中量的结果不可用，加 `ipc:H01M10/613` 这类限定再检——**别用翻页去啃 3 万条**。

**Windows 上用 PowerShell，别用 Bash。** 实测 WorkBuddy 等桌面客户端里 `ls` / `mkdir` / `dirname` 都报 command not found。

**Windows 上一律加 `--json-out`，不要去捕获 stdout。**

```powershell
python scripts/patentmax_client.py search --q "锂电池 AND 热管理" --size 30 --json-out .\search1.json
```

完整 JSON 由 Python 自己以 UTF-8 写进文件，stdout 只回一行纯 ASCII 的确认
（含 `saved_to` 和 `_spent`）。然后读那个文件即可。

> **这条之前写错过，别再照老方子走。** 旧版本建议
> `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` 然后正常捕获输出——
> 实测盖不住，原因有两个：
>
> 1. **每条命令往往是一个全新的 PowerShell 进程**，上一条里设的编码带不到下一条，
>    除非每条命令都带上这个前缀；
> 2. **`Out-String` 默认按固定宽度折行**（通常 80 列），会往 JSON 里插换行——
>    这跟编码无关，是另一个破坏源。
>
> 而且一旦按 GBK 解码过一次，非法字节就被替换成了 `?` / `�`，**不可逆**，
> 事后再怎么转码都救不回来。`--json-out` 把整条链路绕开了：不经过控制台，
> 就没有代码页的事。
>
> 非要捕获 stdout 的话，用 Python 子进程读**原始字节**再自己 `decode("utf-8")`，
> 不要用 PowerShell 的管道。
