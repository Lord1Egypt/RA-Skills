# MISRA C:2012 映射表

> 本表随规则演进持续增补：规则19、规则20/21、规则22、规则23/24（含 MISRA C++:2008 映射）、规则25/26 均已纳入。
> 编号经公开权威来源交叉核实（IAR C-STAT、Klocwork、CodeSonar、Parasoft、MathWorks Polyspace、MISRA C:2012 TC2 官方文档），无杜撰编号；实时性/并发屏蔽/文档类工程规则不在 MISRA 语言条款覆盖范围内，如实标注"无直接对应"，不硬凑编号。

**映射基于 MISRA C:2012（规则23为 MISRA C++:2008），供合规参考，不替代正式 MISRA 检查工具（PC-lint Plus / Polyspace / Coverity）。**

| 规则号 | 规则名 | MISRA 引用 |
|--------|--------|-------------------|
| 1 | ISR阻塞调用 | 无直接对应 |
| 2 | 共享变量未加volatile | 无直接对应 |
| 3 | 数组访问可能越界 | R18.1, R1.3 |
| 4 | 硬编码寄存器值 | 无直接对应 |
| 5 | 临界区未配对 | 无直接对应 |
| 6 | 整数溢出风险 | R1.3, R10.3 |
| 7 | ISR中使用浮点 | 无直接对应 |
| 8 | malloc后未检查NULL | R21.3, R1.3 |
| 9 | 硬编码延时 | 无直接对应 |
| 10 | 浮点数用==比较 | R10.1 |
| 11 | sprintf可能溢出 | R21.6, R21.17 |
| 12 | 未使用的变量/函数 | 无直接对应 |
| 13 | 魔术数字 | 无直接对应 |
| 14 | 函数缺少注释 | 无直接对应 |
| 15 | switch缺少default | R16.4 |
| 16 | 中断上下文调用阻塞RTOS API（FreeRTOS） | 无直接对应 |
| 17 | 大局部数组可能耗尽任务栈 | Dir4.1（参考） |
| 18 | 递归函数 | R17.2 |
| 19 | 硬编码寄存器指针解引用 | R11.4 |
| 20 | 裸int位域 | R6.1 |
| 21 | 宏副作用 | Dir4.9（Advisory） |
| 22 | RT-Thread违规API（中断上下文） | 无直接对应 |
| 23 | C++动态内存分配（裸new） | **MISRA C++:2008** 18-4-1（Required） |
| 24 | 十六进制字面量缺u/U后缀 | R7.2（Required，轻量口径） |
| 25 | 除数为零/模数为零 | R1.3（Required，C11 6.5.5 未定义行为） |
| 26 | memcpy/memset长度超限 | R1.3（Required，越界写属未定义行为） |

## 引用编号说明

- **R1.3**（Mandatory）：不得出现未定义或关键未指定行为（越界访问、有符号整数溢出、空指针解引用均属此类）
- **R6.1**（Required）：位域只得以适当类型声明（unsigned int / signed int / _Bool；裸 int 位域的符号性为实现定义）
- **R10.1**（Required）：操作数不得为不恰当的基本类型（浮点操作数用于 ==/!= 属违反）
- **R10.3**（Required）：表达式值不得赋给更窄基本类型的对象
- **R11.4**（Advisory，AMD1 起为 Required）：对象指针与整型之间不得转换（整型常量强转指针后解引用属此类）
- **R16.4**（Required）：每个 switch 语句必须有 default 标签
- **R17.2**（Required）：函数不得直接或间接递归
- **R18.1**（Required）：指针运算结果必须寻址同一数组内的元素
- **R21.3**（Required）：不得使用 malloc/calloc/realloc/free
- **R21.6**（Required）：不得使用 <stdio.h> 标准库输入输出函数
- **R21.17**（Mandatory）：<string.h> 字符串函数不得越界访问其指针参数引用的对象
- **Dir4.1**（Required）：运行时失败应最小化（栈耗尽属运行时失败，为方向性参考）
- **Dir4.9**（Advisory）：函数式宏与函数可互换时应优先使用函数（副作用宏——体内含自增/自减/赋值——正是不可与函数安全互换的场景）

## RT-Thread 规则22 判据来源（双源核实 2026-09-15）

- 官方编程手册《中断管理》：ISR 内不能执行挂起当前线程的操作，违规时内核报 `Function [xxx] shall not used in ISR`；官方中断底半处理范例中 ISR 直接调用 `rt_sem_release`/`rt_mb_send` 属推荐用法
- 官方内核 master 源码：`rt_sem_create/delete` 等对象创建/删除类带 `RT_DEBUG_NOT_IN_INTERRUPT` 断言；`rt_sem_take` 无中断断言且 `timeout=0`（RT_WAITING_NO）不挂起——试探型降为 low
