# CTF REVERSE 子技能

## 总体流程

```
静态分析（strings/反汇编/反编译） → 理解算法逻辑 → 动态调试验证 → 逆向算法求解 → 输出 flag
```

---

## Phase 1：初步分析

```bash
file ./binary
strings ./binary | grep -E "(flag|FLAG|password|key|secret|input|correct|wrong)"
strings ./binary | grep -E "[A-Za-z0-9+/]{20,}={0,2}"  # Base64 常量

# 导入表（依赖哪些函数）
readelf -d ./binary | grep NEEDED
nm ./binary 2>/dev/null | grep -E "(check|verify|encrypt|decode)"
objdump -d ./binary | head -100

# 运行观察
strace ./binary 2>&1 | head -30   # 系统调用
ltrace ./binary 2>&1 | head -30   # 库函数调用（常直接打印比较）
./binary <<< "AAAAAAAAAAAAAAAA"   # 输入测试
```

---

## Phase 2：反汇编 / 反编译工具

### 2.1 Ghidra（免费，强烈推荐）

```bash
# 安装
apt-get install -y ghidra 2>/dev/null ||
wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.1.2_build/ghidra_11.1.2_PUBLIC_20240709.zip

# 主要功能
# 1. 打开 binary → Analysis → Auto Analyze
# 2. Window → Decompiler 查看 C 伪代码
# 3. 搜索字符串：Search → For Strings
# 4. 找 main：Window → Symbol Tree → Functions
```

### 2.2 radare2（命令行）

```bash
pip install r2pipe --break-system-packages
apt-get install -y radare2 2>/dev/null

r2 ./binary
[0x00000000]> aaa          # 全自动分析
[0x00000000]> afl           # 列出所有函数
[0x00000000]> s main        # 跳转到 main
[0x00000000]> pdf           # 反汇编当前函数
[0x00000000]> pdg           # 反编译（需 r2ghidra）
[0x00000000]> iz            # 列出字符串
[0x00000000]> /flag         # 搜索字符串
```

**通过 r2pipe 自动化**：

```python
import r2pipe
r2 = r2pipe.open('./binary')
r2.cmd('aaa')
funcs = r2.cmdj('aflj')           # JSON 格式函数列表
for f in funcs:
    print(f['name'], hex(f['offset']))
# 反编译 main
r2.cmd('s main')
print(r2.cmd('pdg'))              # Ghidra 反编译器
```

### 2.3 objdump + 手工分析

```bash
objdump -d ./binary -M intel | grep -A 30 "<main>"
objdump -d ./binary -M intel | grep -A 20 "<check>"
```

---

## Phase 3：常见逆向模式

### 3.1 字符串比较（最简单）

```python
# ltrace 直接看到
# strcmp(input, "flag{hello_world}")

# 或在反编译中找类似：
# if (strcmp(input, target) == 0) puts("Correct")
# → flag 就是 target 字符串

# strncmp 逐字节比较
# → 直接读取比较目标
```

### 3.2 逐字节检查（常见）

```python
# 常见模式（伪代码）：
# for i in range(len(input)):
#     if input[i] ^ key[i] != target[i]: wrong()
# → 逆向：flag[i] = target[i] ^ key[i]

# 用 angr 符号执行自动解
pip install angr --break-system-packages
python3 << 'EOF'
import angr
proj = angr.Project('./binary', auto_load_libs=False)
state = proj.factory.entry_state(stdin=angr.SimFile)
simgr = proj.factory.simgr(state)
simgr.explore(find=lambda s: b"Correct" in s.posix.dumps(1),
              avoid=lambda s: b"Wrong" in s.posix.dumps(1))
if simgr.found:
    print(simgr.found[0].posix.dumps(0))
EOF
```

### 3.3 哈希验证

```python
# 程序做：md5(input) == "abc123..."
# → 反向爆破

import hashlib
target = "5f4dcc3b5aa765d61d8327deb882cf99"  # 示例
# 先尝试常见弱口令
wordlist = ["password", "flag", "admin", "1234", "secret"]
for w in wordlist:
    if hashlib.md5(w.encode()).hexdigest() == target:
        print(f"Found: {w}")

# 在线彩虹表：https://crackstation.net/
```

### 3.4 自定义加密逆向

```python
# 程序加密流程：flag → encrypt → check with hardcoded ciphertext
# 逆向步骤：
# 1. 理解 encrypt 函数的每一步
# 2. 写出 decrypt 函数（逆操作，逆顺序）
# 3. 对 hardcoded ciphertext 执行 decrypt

# 示例：XOR + 移位
def decrypt(ct, key):
    result = []
    for i, c in enumerate(ct):
        result.append(c ^ key[i % len(key)] - i & 0xFF)  # 逆 +i 操作
    return bytes(result)

ct = [0x41, 0x52, 0x63, ...]  # 从程序中读取
key = b"secret"
print(decrypt(ct, key))
```

### 3.5 SMT Solver（z3）

```python
# 当逻辑复杂但约束明确时
pip install z3-solver --break-system-packages
from z3 import *

flag = [BitVec(f'flag_{i}', 8) for i in range(20)]
s = Solver()

# 添加 flag 格式约束
for i, c in enumerate(b'flag{'):
    s.add(flag[i] == c)
s.add(flag[-1] == ord('}'))

# 添加程序逻辑约束（从反编译结果翻译）
# s.add(flag[5] + flag[6] == 0x99)
# s.add(flag[5] ^ flag[7] == 0x42)
# ...

if s.check() == sat:
    m = s.model()
    result = bytes([m[flag[i]].as_long() for i in range(20)])
    print(result)
```

---

## Phase 4：动态调试

```bash
# GDB 基础
gdb ./binary
(gdb) break main          # 断点
(gdb) run <<< "AAAAAAAA"  # 带输入运行
(gdb) ni                  # 单步（不进入函数）
(gdb) si                  # 单步（进入函数）
(gdb) x/s $rdi            # 查看寄存器指向字符串
(gdb) x/20x $rsp          # 查看栈
(gdb) info registers      # 所有寄存器
(gdb) set $rax = 1        # 修改寄存器（强制跳过检查）

# 在比较前断点，查看要比较的值
(gdb) break strcmp
(gdb) run <<< "test"
(gdb) x/s $rdi            # 第一个参数
(gdb) x/s $rsi            # 第二个参数
```

**gdb-peda / pwndbg**（增强 gdb）：
```bash
git clone https://github.com/pwndbg/pwndbg && cd pwndbg && ./setup.sh
# 之后 gdb 自动加载 pwndbg
```

---

## Phase 5：特殊类型逆向

### 5.1 Python 字节码（.pyc）

```bash
pip install uncompyle6 pycdc --break-system-packages
uncompyle6 challenge.pyc > source.py
# 或
python3 -m dis challenge.pyc
```

### 5.2 Java / Android APK

```bash
# 反编译 jar
jar xf challenge.jar
javap -c *.class

# APK
pip install jadx --break-system-packages
# jadx-gui challenge.apk  （GUI）
jadx -d output/ challenge.apk  （命令行）
grep -r "flag" output/
```

### 5.3 .NET / C# 

```bash
# 使用 dnSpy（Windows）或 ilspy
dotnet-dump / ILSpy

# Mono + monodis
monodis challenge.exe | grep -A 20 "method.*check\|verify"
```

### 5.4 Rust / Go 二进制

```bash
# 函数名被 mangle
# Ghidra / IDA 能识别大多数标准库函数
# 找入口点 main.main（Go）或 main（Rust）
strings ./binary | grep -E "panicked|goroutine|runtime"
```

---

## Phase 6：angr 符号执行（通用解法）

```python
#!/usr/bin/env python3
import angr, claripy

proj = angr.Project('./binary', auto_load_libs=False)

# 假设 flag 作为命令行参数或 stdin
flag_len = 32  # 估计 flag 长度
flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(flag_len)]
flag_sym = claripy.Concat(*flag_chars)

# 约束 flag 字符范围（可打印字符）
state = proj.factory.full_init_state(
    args=['./binary', flag_sym],
    add_options=angr.options.unicorn
)
for c in flag_chars:
    state.solver.add(c >= 0x20, c <= 0x7e)

# 符号执行
simgr = proj.factory.simgr(state)
simgr.explore(
    find=0x401234,    # 成功分支地址（从反汇编中找）
    avoid=0x401256    # 失败分支地址
)

if simgr.found:
    sol = simgr.found[0]
    result = sol.solver.eval(flag_sym, cast_to=bytes)
    print(f"[+] FLAG: {result}")
```

---

## 快速提取 flag 技巧

```bash
# 1. 直接运行
./binary                    # 也许直接打印 flag

# 2. patch 绕过检查（改跳转指令）
# 找 jne/je 比较后的跳转，改为 nop 或反向跳转
python3 -c "
with open('./binary', 'rb') as f: data = bytearray(f.read())
data[0x1234] = 0x90  # NOP（偏移从 objdump 找）
data[0x1235] = 0x90
with open('./binary_patched', 'wb') as f: f.write(data)
"
chmod +x ./binary_patched && ./binary_patched

# 3. 环境变量 / 文件
echo "flag_placeholder" > flag.txt
./binary flag.txt
FLAG=test ./binary
```
