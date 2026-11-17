#!/usr/bin/env python3
"""
嵌入式C代码静态审查工具 - 核心引擎
27条规则，按高危/中危/低危分级。

更新（1.1.0 · 2026-09-28 · R25~R27 新增 + R3 off-by-one 修复）：
  - 规则3（高危）off-by-one 漏报修复：循环/同行/窗口豁免中 `i <= N` 与
    `i < N` 此前同等放行——`for(i=0;i<=10;i++) buf[i]=0;`（buf[10]）访问
    buf[10] 越界一字节却被豁免。现收紧：上界为纯数字或 sizeof(本数组)
    且恰等于数组大小时不再豁免，特化为「循环边界 off-by-one」报告；
    `<`、`<= size-1`、宏名/变量上界（无法判定）维持豁免，宁漏勿误
  - 新增规则26（高危）：memcpy/memmove/memset/strncpy 长度实参超过目标
    数组大小——`uint8_t buf[16]; memcpy(buf, src, 32);` 直接踩内存。
    长度为 sizeof(另一个更大的已知数组) 时同样命中；sizeof(目标自身)
    与 sizeof(目标[0]) 惯用法豁免；目标为指针/带下标引用/长度为宏或
    变量、sizeof 表达式带除法时无法判定不报（宁漏勿误）。MISRA 映射 R1.3
  - 新增规则27（中危）：数组形参上 sizeof——C99 6.7.5.3 规定形参数组
    类型被调整为指针，`void f(uint8_t buf[16])` 里 sizeof(buf) 得到的是
    指针大小（4/8）而非 16，`memset(buf,0,sizeof(buf))` 只清 4 字节。
    建议：把长度作为独立参数传入。sizeof(形参[0]) 取元素大小合法不报；
    裸指针形参（uint8_t *p）不属本规则
  - 测试：120 → 135 项断言（F 组 15 条正反例）

更新（9/16 MISRA 缩量扩展，原计划 9/16 待办落地）：
  - 新增规则20（中危）：裸 int 位域——`int x : 3;` 的符号性在 C99 中是
    实现定义（C99 6.7.2.5），MISRA C:2012 R6.1 要求位域只以明确类型声明
    （unsigned int / signed int / _Bool）。unsigned/signed 前缀豁免；
    uint8_t/uint32_t 等 stdint 类型按缩量口径不报（多数工具链明确支持，
    报了无行动价值——STM32 LL 寄存器映射满屏此形态）；.h 头文件不豁免
    （位域重灾区恰在头文件寄存器映射）。MISRA 映射 R6.1（Required，
    IAR C-STAT / Klocwork / Parasoft 多源核实）
  - 新增规则21（中危）：函数式宏副作用——宏定义体内出现自增/自减
    （`#define NEXT(n) ((n)++)`）或简单赋值（`#define SET(x,v) ((x)=(v))`），
    表达式语境下调用者的变量被暗中修改，Dir4.9 要求此类场景改用函数。
    语料校准后的豁免口径（防止厂商库惯例刷屏）：
      a) do-while(0) 语句封装豁免（多语句宏标准写法，调用者明确知道是语句）
      b) 复合赋值 |= &= ^= <<= >>= 豁免——真实语料 6073 条（CMSIS
         SET_BIT 风格既成惯例，用户不会改厂商库，报了无行动价值）
      c) enum/struct/union 声明块内的 = 是初始化不是赋值（TU_VERIFY_STATIC
         编译期断言惯用法同款），块内屏蔽
      d) 函数调用不检测——`#define LED_ON() HAL_GPIO_WritePin(...)` 是
         合法封装惯例，词法无法区分有无副作用，报了误报主导
      e) 字符串内容先行剥离（内联汇编约束 "=l" (r) 不误报）
    已知局限：#define 续行符（反斜杠）只扫首行；designated initializer 宏
    （`#define DECL .name = x`）与结构体成员赋值词法同形，接受个位数误报
    换取不漏真赋值宏。MISRA 映射 Dir4.9（Advisory，函数式宏应可被函数
    替换——副作用宏正是不可替换的场景）
  - 新增规则19（高危）：硬编码寄存器指针解引用——整型常量（尤其0x十六进制）
    强转为指针后直接解引用（读/写均报），如 *(volatile uint32_t*)0x40000000 = x;
    建议改用CMSIS式外设寄存器宏定义；#define 行豁免（CMSIS/TivaWare头文件
    自身即此写法，检测目标是业务代码里的裸写）；MISRA 映射 R11.4
  - 规则3（高危）两项修复：
    a) 写操作正则补 (?!=)——此前 arr[i] == x 的"=="比较被当成赋值误报
       （规则2 同款问题的规则3版）
    b) 边界豁免补循环头识别——沿访问行向上查找所属最内层 for/while 循环头，
       循环条件含索引变量比较即豁免（原设计只回看5行，循环头与循环体中后段
       访问距离超窗即误报）
  - 规则4（高危）修复：跳过 #define 行——do-while 宏体内的寄存器写是
    合法常用封装（CMSIS 同款），不再误报"硬编码寄存器值"
  - 规则12（低危）修复：.h 文件整体豁免 + struct/union 定义体屏蔽——
    此前头文件里的结构体字段（如 ring_buffer.h 的 head/tail/count）被
    误报为"定义后未使用"
  - 规则14（低危）增强：--dir 批量模式收集 .h 中带注释的函数声明表，
    .c 中同名函数定义即使定义行前无注释也豁免（"注释在 .h 声明处"是
    标准做法）；单文件模式维持原逻辑
  - 规则2（高危）类型表扩展：全局变量识别与定义行回查补
    bool/_Bool/u8/u16/u32/u64/s8/s16/s32/s64——此前 u32 g_cnt; 这类
    嵌入式常用别名定义的全局变量在 ISR 中自增不会命中

更新：
  - exit code 语义修正：发现问题退出码 1、无问题 0、用法/内部错误 2
    （此前发现问题时也返回 0，与文档约定不符）
  - 规则6（中危）覆盖 return 表达式溢出：return a*b*1000; 等乘法/加法
    直接作为返回值的写法此前漏报；豁免纯常量运算、浮点表达式、
    已显式加宽强转、sizeof/assert 上下文

更新：
  - 新增 MISRA C:2012 规则映射：18条规则逐条映射到 MISRA 规则编号
    （MISRA_MAPPING 常量字典，编号经公开权威来源核实，无杜撰）；
    问题清单每条新增 misra 字段（如 "MISRA C:2012 R18.1, R1.3"）与
    misra_refs 数组；无直接对应条目两字段为空
  - JSON 报告头部新增 misra_note 免责声明：映射供合规参考，不替代
    正式 MISRA 检查工具
  - 检测逻辑零改动（映射仅在结果汇总层注入）

更新：
  - 规则2（高危）修复：ISR共享变量写法匹配从"仅 var = 赋值"扩展为
    赋值 / ++/--（前缀+后缀）/ += -= ^= |= &= 等复合赋值，
    修复 g_ticks++、++g_flag、g_reg |= MASK 等自增自减写法漏报
    （ISR共享计数器最常见写法）；比较运算 ==/!= 仍不报；局部变量、
    已带volatile声明变量的豁免逻辑保持不变
  - 规则5（中危）文案修正：「临界区未关中断配对」→「临界区未开中断配对」
    （原文表述与检测逻辑相反：检测的是关中断后未找到对应的开中断）

更新：
  - 规则16（高危）：RTOS上下文检查——ISR中调用FreeRTOS任务级阻塞API（FromISR变体除外）
  - 规则17（中危）：栈溢出风险——函数内大局部数组（累计>=512字节）
  - 规则18（中危）：递归函数——直接/间接自调用检测
  - 新增 --dir <目录> 批量扫描模式（与单文件模式互斥）
"""

import re
import os
import json
from typing import Optional


# 阻塞函数列表（不应在ISR中调用）
BLOCKING_FUNCS = [
    "HAL_Delay", "printf", "sprintf", "fprintf", "puts",
    "malloc", "calloc", "realloc", "free",
    "fopen", "fclose", "fread", "fwrite",
    "sleep", "usleep", "delay_ms", "delay_us",
]

# 危险函数（应该用安全版本）
DANGEROUS_FUNCS = {
    "sprintf": "建议使用snprintf替代，防止缓冲区溢出",
    "strcpy": "建议使用strncpy替代",
    "strcat": "建议使用strncat替代",
    "gets": "绝对不要使用gets",
}

# 常见寄存器写模式
REGISTER_WRITE_RE = re.compile(
    r"->(?:[A-Z0-9_]+)\s*=\s*(?:0x[0-9A-Fa-f]+|\d+)\s*;"
    r"|(?:REG|REG32|REG16|REG8|ADDR)\s*\([^)]+\)\s*=\s*(?:0x[0-9A-Fa-f]+|\d+)\s*;"
    r"|(?:GPIOA|GPIOB|GPIOC|GPIOD|GPIOE|GPIOF|GPIOG|TIM\d|ADC\d|USART\d|SPI\d|I2C\d|RCC|PWR|FLASH|DMA\d|SCB|NVIC)->[A-Z0-9_]+\s*=\s*(?:0x[0-9A-Fa-f]+|\d+)\s*;"
)

# 魔术数字（排除0, 1, -1, 以及常见宏值）
MAGIC_NUMBER_RE = re.compile(r"(?<![A-Za-z0-9_])(?!0x)(?!0b)(-?\d{2,})(?![A-Za-z0-9_])")

# ---- 规则16：FreeRTOS 任务级（可能阻塞）API ----
# 这些API只能在任务上下文调用；ISR中必须使用 FromISR 变体（中断安全版本）
RTOS_BLOCKING_APIS = [
    "vTaskDelay", "vTaskDelayUntil",
    "xQueueSend", "xQueueSendToBack", "xQueueSendToFront",
    "xQueueReceive", "xQueuePeek",
    "xSemaphoreTake", "xSemaphoreGive",
    "xEventGroupWaitBits", "xEventGroupSync",
    "xTaskNotifyWait", "ulTaskNotifyTake",
    "pvPortMalloc", "vPortFree",
]

# ---- 规则22：RT-Thread 中断上下文违规 API ----
# 判据来源（双源核实 2026-09-15）：
#   官方编程手册《中断管理》："在这个运行环境中不能使用挂起当前线程的操作"
#   （违规时内核报 "Function [xxx] shall not used in ISR"）；
#   官方内核 master 源码：rt_sem_create/delete 等对象创建/删除类有
#   RT_DEBUG_NOT_IN_INTERRUPT 断言；rt_sem_take 无中断断言且 timeout=0
#   （RT_WAITING_NO）不挂起——试探型降为 low。
# RT-Thread 没有 FromISR 后缀惯例（区别于 FreeRTOS）：ISR 内直接调用
# release/send 类 API 是官方推荐用法（中断底半处理范例），不报。
RTTHREAD_THREAD_APIS = [
    "rt_thread_mdelay", "rt_thread_delay", "rt_thread_sleep",
    "rt_thread_create", "rt_thread_suspend", "rt_thread_delete",
    "rt_thread_yield",
]
RTTHREAD_MEM_APIS = ["rt_malloc", "rt_free", "rt_realloc", "rt_calloc"]
RTTHREAD_OBJ_CREATE_APIS = [
    "rt_sem_create", "rt_sem_delete",
    "rt_mutex_create", "rt_mutex_delete",
    "rt_event_create", "rt_event_delete",
    "rt_mb_create", "rt_mb_delete",
    "rt_mq_create", "rt_mq_delete",
]
# 带 timeout 实参的等待类 API -> timeout 实参序号（1-based）
# 官方文档+源码：非零 timeout 为挂起语义，ISR 内禁止；timeout=0 试探型 low
RTTHREAD_WAIT_APIS = {
    "rt_sem_take": 2,
    "rt_mb_recv": 2,
    "rt_mq_recv": 4,
    "rt_event_recv": 4,
    "rt_mb_send_wait": 3,
}
# rt_mutex_take 任何 timeout 都禁：互斥量带所有者/优先级继承语义，
# 必须在线程上下文（官方文档明确，timeout=0 也不可）
RTTHREAD_MUTEX_APIS = ["rt_mutex_take"]

# ---- 规则17：类型大小表（字节），用于局部数组栈占用估算 ----
TYPE_SIZES = {
    "char": 1, "int8_t": 1, "uint8_t": 1, "int8": 1, "uint8": 1,
    "u8": 1, "s8": 1, "bool": 1, "_Bool": 1,
    "short": 2, "int16_t": 2, "uint16_t": 2, "int16": 2, "uint16": 2,
    "u16": 2, "s16": 2,
    "int": 4, "unsigned": 4, "int32_t": 4, "uint32_t": 4, "int32": 4,
    "uint32": 4, "u32": 4, "s32": 4, "float": 4, "long": 4, "size_t": 4,
    "double": 8, "int64_t": 8, "uint64_t": 8, "int64": 8, "uint64": 8,
    "u64": 8, "s64": 8,
}

# 局部数组声明：uint8_t frame_buf[1024]; / char buf[10] = {0};
LOCAL_ARRAY_RE = re.compile(
    r"\b(?P<type>char|short|int|long|float|double|"
    r"uint8_t|int8_t|uint16_t|int16_t|uint32_t|int32_t|uint64_t|int64_t|"
    r"uint8|uint16|uint32|uint64|int8|int16|int32|int64|"
    r"u8|u16|u32|u64|s8|s16|s32|s64|size_t|_Bool|bool)\s+"
    r"(?P<name>[A-Za-z_]\w*)\s*\[\s*(?P<size>\d+)\s*\]"
)

# 局部数组栈占用阈值（字节）
LOCAL_ARRAY_STACK_THRESHOLD = 512

# ---- MISRA C:2012 映射 ----
# 18条审查规则 → MISRA C:2012 规则编号。依据：MISRA C:2012 Third Edition
# （含 TC1/TC2 与 AMD1/AMD2 修订）；编号均经公开权威来源交叉核实
# （IAR C-STAT / Klocwork / IBM Test RealTime / CodeSonar / Parasoft /
#  MISRA C:2012 TC2 官方 Permits 文档），无杜撰编号。
# 无直接对应者置空列表：MISRA 是C语言子集标准，实时性/并发屏蔽/文档类
# 工程规则不在其语言条款覆盖范围内——宁标"无直接对应"，不硬凑编号。
MISRA_MAPPING = {
    1: [],                    # ISR阻塞调用：无直接对应——MISRA不约束中断实时性
    2: [],                    # 共享变量缺volatile：无直接对应——MISRA无volatile条款（AMD4 Dir5.1仅覆盖C11线程数据竞争，ISR场景无条款）
    3: ["R18.1", "R1.3"],     # R18.1: 指针运算结果须寻址同一数组元素；越界访问属未定义行为(R1.3)
    4: [],                    # 硬编码寄存器值：无直接对应——可读性/维护性规则，MISRA无字面量数值禁令
    5: [],                    # 临界区未配对：无直接对应——中断屏蔽配对属并发/架构问题
    6: ["R1.3", "R10.3"],     # 有符号整数溢出属未定义行为(R1.3)；乘积赋给更窄本质类型违反R10.3
    7: [],                    # ISR浮点：无直接对应——实时性/平台开销问题
    8: ["R21.3", "R1.3"],     # R21.3: 禁用malloc/calloc/realloc/free；分配失败未判空致空指针解引用属UB(R1.3)
    9: [],                    # 硬编码延时：无直接对应——时序实现方式
    10: ["R10.1"],            # 浮点操作数用于==/!=属不恰当基本类型（R10.1运算符表，IAR/Parasoft均实现为10.1子项）
    11: ["R21.6", "R21.17"],  # sprintf/gets属被禁用的<stdio.h>(R21.6)；strcpy/strcat受R21.17越界访问禁令约束
    12: [],                   # 未使用变量：MISRA仅有R2.7(参数)/R2.5(宏)/R2.6(标签)，无未使用变量条款
    13: [],                   # 魔术数字：无直接对应——MISRA无数值字面量禁令
    14: [],                   # 函数缺注释：无直接对应——文档性要求不在语言条款内
    15: ["R16.4"],            # R16.4: 每个switch语句必须有default标签(Required)
    16: [],                   # RTOS API in ISR：无直接对应——RTOS调度约束超出MISRA语言规则范围
    17: ["Dir4.1"],           # 栈耗尽属运行时失败，Dir4.1要求最小化运行时失败(Required，方向性参考)
    18: ["R17.2"],            # R17.2: 函数不得直接或间接递归(Required)
    19: ["R11.4"],            # R11.4: 对象指针与整型之间不得转换（规则19：硬编码寄存器指针解引用）
    20: ["R6.1"],             # R6.1: 位域只得以适当类型声明(Required)；裸int符号性为实现定义
    21: ["Dir4.9"],           # Dir4.9: 可与函数互换时优先用函数(Advisory)；副作用宏不可互换
    22: [],                   # RT-Thread API in ISR：无直接对应——RTOS调度约束超出MISRA语言规则范围
    23: ["C++ 18-4-1"],       # MISRA C++:2008 18-4-1(Required): 禁用动态堆分配(new/delete/malloc)；规则23仅检非放置new
    24: ["R7.2"],             # R7.2(Required): 8/16进制整型常量应加u/U后缀；轻量口径仅覆盖大值+表达式语境
    25: ["R1.3"],             # R1.3(Required): 不得出现未定义行为——整数除零属C11 6.5.5定义的UB
    26: ["R1.3"],             # R1.3(Required): 不得出现未定义行为——越界写踩坏相邻内存属UB
}

MISRA_NOTICE = ("映射基于 MISRA C:2012，供合规参考，不替代正式 MISRA 检查工具"
                "（如 PC-lint Plus / Polyspace / Coverity）")

# ---- C++ 轻量支持：文件扩展名分类 ----
# C++ 支持定位：面向嵌入式常见的"C 风格 C++"（.cpp 里写 C 子集 + 少量类封装），
# 不做模板/重载/namespace 语义分析——那些形态下函数识别与作用域近似会失准，
# 文档已注明局限。
SOURCE_EXTS = (".c", ".cpp", ".cc", ".cxx")
HEADER_EXTS = (".h", ".hpp", ".hh")
CPP_SOURCE_EXTS = (".cpp", ".cc", ".cxx")


def _attach_misra(issues: list) -> list:
    """为问题清单附加 MISRA C:2012 引用（检测逻辑零改动，仅汇总层注入）。

    有映射:     misra="MISRA C:2012 R18.1, R1.3", misra_refs=["R18.1", "R1.3"]
    无直接对应: misra="", misra_refs=[]
    """
    for issue in issues:
        refs = MISRA_MAPPING.get(issue.get("rule_id"), [])
        # 支持 MISRA C++ 映射——refs 全部以 "C++" 开头时前缀换用 MISRA C++:2008
        if refs and all(r.startswith("C++") for r in refs):
            issue["misra"] = "MISRA C++:2008 " + ", ".join(
                r.split(" ", 1)[1] if r.startswith("C++ ") else r for r in refs)
            issue["misra_refs"] = list(refs)
            continue
        issue["misra"] = ("MISRA C:2012 " + ", ".join(refs)) if refs else ""
        issue["misra_refs"] = list(refs)
    return issues



def review_code(
    file_path: Optional[str] = None,
    code: Optional[str] = None,
    rules: str = "all",
    commented_decls: Optional[set] = None,
) -> dict:
    """
    审查嵌入式C代码。

    Args:
        file_path: C源文件路径
        code: 直接传入的C代码
        rules: "all"/"high"/"medium"/"low"
        commented_decls: 批量模式下 .h 中带注释的函数声明名集合，
                         供规则14豁免"注释在.h声明处"的函数（单文件调用可不传）

    Returns:
        {"success": bool, "score": int, "summary": {...}, "issues": [...]}
    """
    if file_path:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"文件不存在: {file_path}"}
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
    elif code is not None:
        source = code
    else:
        return {"success": False, "error": "必须提供file_path或code参数"}

    if not source.strip():
        return {"success": False, "error": "代码为空"}

    # 预处理：去掉注释和字符串（用于模式匹配）
    cleaned = _strip_comments_strings(source)
    lines = source.split("\n")
    cleaned_lines = cleaned.split("\n")

    # 识别ISR函数
    isr_ranges = _find_isr_functions(cleaned, cleaned_lines)

    # 识别全局变量
    global_vars = _find_global_vars(cleaned_lines)

    # .h 头文件判定（规则12整体豁免用）；支持 .hpp/.hh
    is_header = bool(file_path) and file_path.lower().endswith(HEADER_EXTS)
    # C++ 源文件判定（规则23动态内存检测仅对 .cpp/.cc/.cxx 生效）
    is_cpp = bool(file_path) and file_path.lower().endswith(CPP_SOURCE_EXTS)

    issues = []

    # 规则1: ISR阻塞调用
    if rules in ("all", "high"):
        issues.extend(_check_isr_blocking(lines, cleaned_lines, isr_ranges))

    # 规则2: 共享变量未加volatile（标量）+ 共享数组扩展
    if rules in ("all", "high"):
        issues.extend(_check_volatile(source, cleaned, global_vars, isr_ranges))
        issues.extend(_check_shared_arrays_volatile(source, cleaned, global_vars, isr_ranges))

    # 规则3: 数组越界
    if rules in ("all", "high"):
        issues.extend(_check_array_bounds(cleaned_lines))

    # 规则25: 常量除零/模零（整数除零=UB，Cortex-M 上 UsageFault/HardFault）
    if rules in ("all", "high"):
        issues.extend(_check_div_by_zero(cleaned_lines))

    # 规则26: memcpy/memset 等长度实参超过目标数组大小（踩内存，高危）
    if rules in ("all", "high"):
        issues.extend(_check_memcpy_overflow(cleaned_lines))

    # 规则4: 硬编码寄存器值
    if rules in ("all", "high"):
        issues.extend(_check_register_magic(cleaned_lines))

    # 规则19: 硬编码寄存器指针解引用（新增，高危）
    if rules in ("all", "high"):
        issues.extend(_check_register_ptr_deref(cleaned_lines))

    # 规则5: 临界区未配对
    if rules in ("all", "medium"):
        issues.extend(_check_critical_section(cleaned_lines))

    # 规则6: 整数溢出风险
    if rules in ("all", "medium"):
        issues.extend(_check_integer_overflow(cleaned_lines))

    # 规则7: ISR浮点
    if rules in ("all", "medium"):
        issues.extend(_check_isr_float(lines, cleaned_lines, isr_ranges))

    # 规则8: malloc未检查NULL（C++ 文件附加裸 new 检测）
    if rules in ("all", "medium"):
        issues.extend(_check_malloc_null(cleaned_lines, is_cpp))

    # 规则9 已移至 low 组：ISR 内由规则1高危覆盖，主流程降级 low

    # 规则10: 浮点==比较
    if rules in ("all", "medium"):
        issues.extend(_check_float_equality(cleaned_lines))

    # 规则11: 危险函数(sprintf等)
    if rules in ("all", "medium"):
        issues.extend(_check_dangerous_funcs(cleaned_lines))

    # 规则12: 未使用变量（.h 文件整体豁免 + struct/union 屏蔽）
    if rules in ("all", "low"):
        issues.extend(_check_unused_vars(source, cleaned, is_header))

    # 规则13: 魔术数字
    if rules in ("all", "low"):
        issues.extend(_check_magic_numbers(cleaned_lines))

    # 规则9: 硬编码延时（降级 low：ISR 内已由规则1高危覆盖不重复报，
    # 主流程延时时序误差属低危可维护性问题；真实语料实测 medium 档 87% 为
    # 主流程 LED 闪烁类延时，刷屏无行动价值）
    if rules in ("all", "low"):
        issues.extend(_check_hardcoded_delay(cleaned_lines, isr_ranges))

    # 规则14: 函数缺少注释（批量模式支持 .h 注释声明豁免）
    if rules in ("all", "low"):
        issues.extend(_check_missing_comments(source, cleaned_lines, commented_decls))

    # 规则15: switch缺default
    if rules in ("all", "low"):
        issues.extend(_check_switch_default(cleaned_lines))

    # 规则24: 十六进制字面量缺u/U后缀（R7.2 轻量口径，限流3条）
    if rules in ("all", "low"):
        issues.extend(_check_hex_suffix(cleaned_lines))

    # 规则16: RTOS上下文检查（ISR中调用任务级阻塞API）
    if rules in ("all", "high"):
        issues.extend(_check_rtos_in_isr(cleaned_lines, isr_ranges))

    # 规则22: RT-Thread 中断上下文违规API
    if rules in ("all", "high"):
        issues.extend(_check_rtthread_in_isr(cleaned_lines, isr_ranges))

    # 规则17: 大局部数组栈溢出风险
    if rules in ("all", "medium"):
        issues.extend(_check_large_local_arrays(cleaned, cleaned_lines))

    # 规则18: 递归函数
    if rules in ("all", "medium"):
        issues.extend(_check_recursion(cleaned, cleaned_lines))

    # 规则20: 裸 int 位域（新增，MISRA R6.1）
    if rules in ("all", "medium"):
        issues.extend(_check_bitfield(cleaned_lines))

    # 规则21: 宏副作用（新增，MISRA Dir4.9）
    if rules in ("all", "medium"):
        issues.extend(_check_macro_side_effects(cleaned_lines))

    # 规则27: 数组形参上 sizeof（C99 形参调整为指针，中危）
    if rules in ("all", "medium"):
        issues.extend(_check_array_param_sizeof(cleaned, cleaned_lines))

    # 按严重级别和行号排序
    sev_order = {"high": 0, "medium": 1, "low": 2}
    issues.sort(key=lambda x: (sev_order.get(x["severity"], 9), x["line"]))

    # 注入 MISRA C:2012 映射引用（检测逻辑零改动，仅汇总层附加字段）
    issues = _attach_misra(issues)

    # 计算评分
    score = 100
    for issue in issues:
        if issue["severity"] == "high":
            score -= 8
        elif issue["severity"] == "medium":
            score -= 4
        else:
            score -= 1
    score = max(0, score)

    summary = {
        "high": sum(1 for i in issues if i["severity"] == "high"),
        "medium": sum(1 for i in issues if i["severity"] == "medium"),
        "low": sum(1 for i in issues if i["severity"] == "low"),
        "total": len(issues),
    }

    return {
        "success": True,
        "misra_note": MISRA_NOTICE,
        "score": score,
        "summary": summary,
        "issues": issues,
    }


def _strip_comments_strings(source: str) -> str:
    """去掉C代码中的注释和字符串内容，保留行结构。"""
    result = []
    i = 0
    n = len(source)
    while i < n:
        # 单行注释
        if i < n - 1 and source[i] == '/' and source[i + 1] == '/':
            while i < n and source[i] != '\n':
                result.append(' ')
                i += 1
            continue
        # 多行注释
        if i < n - 1 and source[i] == '/' and source[i + 1] == '*':
            while i < n - 1 and not (source[i] == '*' and source[i + 1] == '/'):
                result.append('\n' if source[i] == '\n' else ' ')
                i += 1
            if i < n - 1:
                result.append('  ')
                i += 2
            continue
        # 字符串
        if source[i] == '"':
            result.append('"')
            i += 1
            while i < n and source[i] != '"':
                if source[i] == '\\':
                    result.append('  ')
                    i += 2
                    continue
                result.append(' ' if source[i] != '\n' else '\n')
                i += 1
            if i < n:
                result.append('"')
                i += 1
            continue
        # 字符
        if source[i] == "'":
            result.append("'")
            i += 1
            while i < n and source[i] != "'":
                if source[i] == '\\':
                    result.append('  ')
                    i += 2
                    continue
                result.append(' ')
                i += 1
            if i < n:
                result.append("'")
                i += 1
            continue
        result.append(source[i])
        i += 1
    return "".join(result)


# ---- 函数识别"签名"正则（_find_isr_functions 与 _find_all_function_ranges 共用）----
# 两处必须共用同一正则，否则 ISR 判定与其他规则对函数边界的判定会互相打架。
#
# 修正（地基级缺陷）：
#   旧正则 r"(?:^|\n)\s*(?:[A-Za-z_][\w\s\*]*?)\s+([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{"
#   中前置的 \s* 与返回类型里的 [\w\s\*]*? 都能匹配换行，使匹配从上一行甚至更早处开始：
#     1) start_line 用 m.start() 换算时整体偏移一行 —— 实测 400 个真实工程文件上，
#        92% 的"递归"报告（34/37）指向的是上一个函数的 "}" 行；
#     2) 会把 "if (...) {" 识别成名为 if 的函数，在调用图里造出伪节点。
#   修正：[ \t] 取代 \s（返回类型与函数名必须同行）+ 函数名关键字黑名单。
# 注意：只有"返回类型→函数名"这一段禁止跨行；参数表与 ") 到 {" 之间仍允许换行，
# 否则 K&R 风格（左花括号另起一行，HAL/CubeMX 代码的常见写法）会被整片漏识别。
FUNC_DEF_RE = re.compile(
    r"(?:^|\n)[ \t]*(?:[A-Za-z_][\w \t\*]*?)[ \t]+([A-Za-z_]\w*)[ \t]*"
    r"\([^;{}]*\)\s*(?:__attribute__\s*\(\s*\([^)]*\)\s*\)\s*)?\{",
    re.MULTILINE,
)

# 不能作为函数名的关键字（旧正则会把 if/while/for/switch 等误识别成函数）
_FUNC_NAME_BLOCKLIST = frozenset({
    "if", "else", "for", "while", "do", "switch", "return", "sizeof",
    "case", "default", "goto", "break", "continue", "typedef", "struct",
    "union", "enum",
})


def _find_isr_functions(cleaned: str, cleaned_lines: list) -> list:
    """识别ISR/中断回调函数，返回[(start_line, end_line, name)]。

    覆盖常见写法（v5 扩展，旧版只认名字含 IRQHandler 的函数，导致
    ISR_TIM1 / HAL_xxx_Callback / __irq 等全部漏识别，ISR内问题全漏报）：
      - void TIM1_IRQHandler(void) / void XXX_IRQHandler(...)
      - void ISR_TIM1(void) / void ISR_TIMx(...)
      - void HAL_GPIO_EXTI_Callback(...) / HAL_xxx_Callback
      - 函数定义带 __irq / __interrupt / __attribute__((interrupt)) 修饰

    中断修饰符只看签名行及紧邻上一行。旧版抓签名前200字符并匹配
    IRQn，上一函数尾部的 HAL_NVIC_SetPriority(SysTick_IRQn,..) 会把
    main / MX_xxx_Init 等普通函数误判成 ISR（真实语料400文件实测，37个
    "ISR"中15个为假，R1/R2/R7/R16 四条规则全部被污染）。
    """
    isrs = []
    # 与 _find_all_function_ranges 共用 FUNC_DEF_RE，保证函数边界判定一致
    func_def = FUNC_DEF_RE

    def _is_isr_name(name: str) -> bool:
        n = name.lower()
        if "irqhandler" in n or n.startswith("isr") or "_isr" in n or n.endswith("_isr"):
            return True
        # HAL/标准外设中断回调。endswith("_callback") 改为
        # endswith("callback")——HAL 驼峰命名（HAL_UART_RxCpltCallback /
        # HAL_ADC_ConvCpltCallback / HAL_TIM_PeriodElapsedCallback）小写化后
        # Callback 前没有下划线，旧判据整队漏识别（HAL_GPIO_EXTI_Callback
        # 能命中纯属 EXTI 全大写天然带下划线）
        if n.endswith("callback") and any(
            k in n for k in ("exti", "irq", "it", "tim", "uart", "adc", "dma", "spi", "can", "i2c")
        ):
            return True
        if n in ("hard_fault_handler", "nmi_handler", "mem_manage_handler",
                 "bus_fault_handler", "usage_fault_handler", "svcall_handler",
                 "pendsv_handler", "systick_handler"):
            return True
        return False

    matches = list(func_def.finditer(cleaned))
    for idx, m in enumerate(matches):
        name = m.group(1)
        # if/while/for/switch 等关键字不是函数名
        if name in _FUNC_NAME_BLOCKLIST:
            continue
        # 中断修饰符只看签名行+紧邻上一行（不再抓前200字符）。
        # __irq/__interrupt 双下划线开头，参数名几乎不可能撞名；Keil C51
        # 的 `void f(void) interrupt 1` 用 interrupt+数字 匹配；__attribute__
        # ((interrupt)) 属 GNU ARM。刻意不匹配裸 IRQn——它出现在
        # HAL_NVIC_SetPriority/IRQn_Type 等普通代码里，是本轮误判根源。
        sig_start = cleaned.rfind("\n", 0, m.start(1)) + 1
        sig_text = cleaned[sig_start:m.end()]
        prev_nl = cleaned.rfind("\n", 0, sig_start)
        prev_line = cleaned[prev_nl + 1:sig_start] if prev_nl >= 0 else ""
        isr_ctx = sig_text + "\n" + prev_line
        is_isr = _is_isr_name(name) or bool(
            re.search(
                r"\b__irq\b|\b__interrupt\b"
                r"|__attribute__\s*\(\s*\(\s*interrupt"
                r"|\binterrupt\s+\d",
                isr_ctx,
            )
        )
        if not is_isr:
            # RT-Thread 挂接式 ISR（rt_hw_interrupt_install 注册的
            # xxx_handler）无法从命名/修饰符区分——本函数签名至下一个函数
            # 签名之间出现 rt_interrupt_enter() 调用（官方文档 ISR 标准写法，
            # 零误判强判据）即判 ISR。只切片两次不做全文逐字符扫描。
            next_start = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned)
            if not re.search(r"\brt_interrupt_enter\s*\(", cleaned[m.start():next_start]):
                continue
        # 用函数名所在行换算起始行。旧版用 m.start()，而匹配起点是前置的
        # 换行符本身，count("\n") 少算一个，导致起始行整体上移一行。
        start_line = cleaned[:m.start(1)].count("\n")
        # 找匹配的右括号
        brace_count = 0
        found_start = False
        for i in range(m.start(), len(cleaned)):
            if cleaned[i] == "{":
                brace_count += 1
                found_start = True
            elif cleaned[i] == "}":
                brace_count -= 1
                if found_start and brace_count == 0:
                    end_line = cleaned[:i].count("\n")
                    isrs.append((start_line, end_line, name))
                    break
    return isrs


# ---- 全局变量识别类型组（含嵌入式常用缩写别名），规则2依赖 ----
GLOBAL_TYPE_GROUP = (
    r"(?:int|char|short|long|float|double|size_t|bool|_Bool|"
    r"uint\d+_t|int\d+_t|u8|u16|u32|u64|s8|s16|s32|s64)"
)


def _find_global_vars(cleaned_lines: list) -> dict:
    """找全局变量定义，返回{var_name: line_number}。"""
    globals_found = {}
    # 简单检测：在函数外定义的变量
    in_function = 0
    for i, line in enumerate(cleaned_lines):
        stripped = line.strip()
        if "{" in stripped and not stripped.startswith("if") and not stripped.startswith("for") and not stripped.startswith("while") and not stripped.startswith("switch"):
            in_function += 1
        if "}" in stripped:
            in_function = max(0, in_function - 1)
        if in_function == 0:
            # 全局变量定义
            m = re.match(
                r"(?:static\s+)?(?:volatile\s+)?(?:const\s+)?(?:unsigned\s+)?"
                + GLOBAL_TYPE_GROUP
                + r"\s+\**(\w+)\s*(?:=|;|\[)",
                stripped,
            )
            if m:
                globals_found[m.group(1)] = i + 1
    return globals_found


def _line_in_isr(line_num: int, isr_ranges: list) -> bool:
    for start, end, _ in isr_ranges:
        if start <= line_num - 1 <= end:
            return True
    return False


def _check_isr_blocking(lines, cleaned_lines, isr_ranges) -> list:
    issues = []
    for start, end, name in isr_ranges:
        for i in range(start, min(end + 1, len(cleaned_lines))):
            for func in BLOCKING_FUNCS:
                if re.search(r"\b" + re.escape(func) + r"\s*\(", cleaned_lines[i]):
                    issues.append({
                        "rule_id": 1,
                        "severity": "high",
                        "line": i + 1,
                        "title": f"ISR中使用阻塞函数 {func}",
                        "description": f"中断服务函数 {name} 第{i+1}行调用了 {func}()，这会导致中断执行时间过长，影响系统实时性。",
                        "suggestion": f"在ISR中只设置标志位（volatile flag）或往队列发送数据，在主循环中调用 {func}。",
                    })
    return issues


# ---- 规则2：ISR内共享变量"写操作"匹配 ----
# 覆盖五类写法（ISR共享变量最常被漏检的自增/自减/复合赋值）：
#   1) 直接赋值   var = x      （(?!=) 排除 == 比较）
#   2) 后缀自增减 var++ / var--
#   3) 前缀自增减 ++var / --var （(?<![+\-\w]) 排除 a-(-b)、a+++b 等非修改场景）
#   4) 复合赋值   += -= *= /= %= &= |= ^= <<= >>=
# 比较运算（== != <= >=）属于读操作，不匹配，避免误报。
def _var_write_pattern(var: str):
    v = re.escape(var)
    return re.compile(
        r"\b" + v + r"\s*(?:\+\+|--)"                                # 后缀
        r"|(?<![+\-\w])(?:\+\+|--)\s*\b" + v + r"\b"                 # 前缀
        r"|\b" + v + r"\s*(?:\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=)"   # 复合赋值
        r"|\b" + v + r"\s*=(?!=)"                                    # 直接赋值
    )


def _check_volatile(source, cleaned, global_vars, isr_ranges) -> list:
    issues = []
    # 找在ISR中被写过的全局变量（覆盖赋值/自增自减/复合赋值）
    write_res = {var: _var_write_pattern(var) for var in global_vars}
    isr_modified = set()
    cleaned_lines = cleaned.split('\n')
    for start, end, name in isr_ranges:
        for i in range(start, min(end + 1, len(cleaned_lines))):
            line = cleaned_lines[i]
            for var in global_vars:
                if write_res[var].search(line):
                    isr_modified.add(var)

    # 检查这些变量是否有volatile
    for var in isr_modified:
        # 在源代码中找变量定义
        def_line = global_vars.get(var, 0)
        if def_line > 0:
            # 找定义行附近的原始文本（类型表与 _find_global_vars 对齐）
            pattern = re.compile(
                r"(?:static\s+)?((?:volatile\s+)?)(?:const\s+)?(?:unsigned\s+)?"
                + GLOBAL_TYPE_GROUP
                + r"\s+\**" + re.escape(var) + r"\b",
            )
            m = pattern.search(cleaned)
            if m and "volatile" not in m.group(0):
                issues.append({
                    "rule_id": 2,
                    "severity": "high",
                    "line": def_line,
                    "title": f"中断共享变量 {var} 未加volatile",
                    "description": f"全局变量 {var} 在中断服务函数中被修改，但定义时未加volatile修饰。编译器优化可能导致主循环读到缓存的旧值。",
                    "suggestion": f"将变量定义改为：volatile uint8_t {var};",
                })
    return issues


# ---- 规则2扩展：中断/主循环共享的全局数组 ----
# 现有 R2 只覆盖标量变量的五类写法（var= / var++ / ++var / var op= x），
# 对数组元素写（buf[i] = x）不匹配——而共享数组与标量共享是同一种玄学 bug：
# ISR 写元素、主循环读元素，无 volatile 时优化后的主循环可能永远读到旧值。
# 判定口径（防误报）：
#   - 必须 ISR 中对数组"元素级写"（赋值/自增减/复合赋值），仅传指针不算
#   - 必须 ISR 之外的代码也访问过该数组（读或写），纯 ISR 私有不报
#   - 定义带 volatile 则豁免（与标量 R2 口径一致）
def _array_write_pattern(name: str):
    n = re.escape(name)
    return re.compile(
        r"\b" + n + r"\s*\[[^\]]*\]\s*=(?!=)"                                       # 元素赋值
        r"|\b" + n + r"\s*\[[^\]]*\]\s*(?:\+\+|--)"                                 # 后缀自增减
        r"|\b" + n + r"\s*\[[^\]]*\]\s*(?:\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=)"     # 复合赋值
        r"|(?<![+\-\w])(?:\+\+|--)\s*\b" + n + r"\s*\["                             # 前缀自增减
    )


def _check_shared_arrays_volatile(source, cleaned, global_vars, isr_ranges) -> list:
    issues = []
    if not isr_ranges:
        return issues
    cleaned_lines = cleaned.split("\n")
    # 候选：被以数组形式访问（arr[...]）的全局变量
    array_names = [v for v in global_vars
                   if re.search(r"\b" + re.escape(v) + r"\s*\[", cleaned)]
    if not array_names:
        return issues
    write_res = {v: _array_write_pattern(v) for v in array_names}
    access_res = {v: re.compile(r"\b" + re.escape(v) + r"\s*\[") for v in array_names}

    # 1) ISR 中写过元素
    isr_written = set()
    for v in array_names:
        for start, end, _ in isr_ranges:
            for i in range(start, min(end + 1, len(cleaned_lines))):
                if write_res[v].search(cleaned_lines[i]):
                    isr_written.add(v)
                    break

    # 2) ISR 之外也访问过（读或写都算——碰了就有共享风险）
    shared = set()
    for v in isr_written:
        covered = set()
        for start, end, _ in isr_ranges:
            covered.update(range(start, end + 1))
        for i, line in enumerate(cleaned_lines):
            if i in covered:
                continue
            if access_res[v].search(line):
                shared.add(v)
                break

    # 3) 检查定义是否带 volatile（与标量 R2 口径一致）
    for v in shared:
        def_line = global_vars.get(v, 0)
        if def_line <= 0:
            continue
        pattern = re.compile(
            r"(?:static\s+)?((?:volatile\s+)?)(?:const\s+)?(?:unsigned\s+)?"
            + GLOBAL_TYPE_GROUP
            + r"\s+\**" + re.escape(v) + r"\s*\[",
        )
        m = pattern.search(cleaned)
        if m and "volatile" not in m.group(0):
            issues.append({
                "rule_id": 2,
                "severity": "high",
                "line": def_line,
                "title": f"中断共享数组 {v} 未加volatile",
                "description": f"全局数组 {v} 在中断服务函数中被写入，同时主循环也在访问，且定义时未加volatile修饰。编译器优化下主循环可能永远读到缓存的旧元素，产生偶发数据错误。",
                "suggestion": f"将定义改为 volatile 修饰（如 volatile uint8_t {v}[N];）；若数组较大担心性能，可改用双缓冲或临界区保护主循环的读取段。",
            })
    return issues


# ---- 规则25：常量除零/模零 ----
# 整数除零是 C 标准未定义行为（C11 6.5.5）：x86 上直接崩溃，
# Cortex-M 上触发 UsageFault（除零陷阱使能时）或得到垃圾结果，均为真雷。
# 口径：只报字面量除数 0（含 /= 0、%= 0）；变量除数静态分析无法判断不报；
# 0x10 / 0b101 / 0.5 / 01 / 0f 等非零字面量形态已排除，避免 a/0x1F 误报。
DIV_ZERO_RE = re.compile(r"(?<![/*])[/%]=?\s*0(?![.xXbB0-9fFlL])")


def _check_div_by_zero(cleaned_lines) -> list:
    issues = []
    for i, line in enumerate(cleaned_lines):
        m = DIV_ZERO_RE.search(line)
        if m:
            issues.append({
                "rule_id": 25,
                "severity": "high",
                "line": i + 1,
                "title": "除数/模数为常量0",
                "description": "整数除以常量0是C标准未定义行为：Cortex-M 上触发 UsageFault/HardFault（除零陷阱使能时）或静默得到垃圾结果，编译器多数只给警告、照常生成会故障的代码。",
                "suggestion": "除法前检查除数：if (divisor != 0) { q = a / divisor; } else { /* 走故障保护/缺省值分支 */ }",
            })
    return issues


def _check_array_bounds(cleaned_lines) -> list:
    issues = []

    # --- 先收集数组声明：type name[SIZE] / type name[SIZE] = {...}，建立大小表 ---
    # 支持  char buf[10];  uint8_t rx[64];  static int table[8]; 指针数组不处理
    decl_re = re.compile(
        r"\b(?:static\s+|volatile\s+|const\s+)*"
        r"(?:unsigned\s+|signed\s+)?"
        r"(?:int|char|short|long|float|double|uint\d+_t|int\d+_t|size_t|u?int\w*_t)\b"
        r"[\s\*]+(\w+)\s*\[\s*(\d+)\s*\]"
    )
    # 同名数组按 (行号, 大小) 列表记录，引用判定取"引用行之前最近的定义"。
    # 此前是单值字典后定义覆盖前定义——同函数不同块（甚至不同函数）里的
    # 同名不同尺寸数组会互相污染，如 uint8_t tx[4] 在前、tx[2] 在后，
    # 前面块的 tx[3] 合法访问被按 tx[2] 误报越界（生成器闭环实测命中）。
    # 同行引用（int a[4]; x=a[5];）取 <= 当前行，C 先声明后使用，安全。
    array_sizes = {}  # name -> [(line_no_0based, size), ...] 行序
    for ln, line in enumerate(cleaned_lines):
        for dm in decl_re.finditer(line):
            array_sizes.setdefault(dm.group(1), []).append((ln, int(dm.group(2))))

    # --- 常量索引越界检测：name[CONST] 且 CONST >= 声明SIZE ---
    # 注意：声明本身 `type name[10];` 中的 [10] 是大小不是下标，必须排除
    const_access = re.compile(r"(\w+)\s*\[\s*(\d+)\s*\]")
    for i, line in enumerate(cleaned_lines):
        for cm in const_access.finditer(line):
            arr_name, idx = cm.group(1), int(cm.group(2))
            # 跳过数组声明位置（同名、数字跨度重合即判定为声明）
            is_declaration = any(
                dm.group(1) == arr_name and dm.span(2) == cm.span(2)
                for dm in decl_re.finditer(line)
            )
            if is_declaration:
                continue
            # 取引用行之前（<=，同行先声明后使用）最近的定义行
            size = None
            for def_ln, sz in reversed(array_sizes.get(arr_name, [])):
                if def_ln <= i:
                    size = sz
                    break
            if size is not None and idx >= size:
                issues.append({
                    "rule_id": 3,
                    "severity": "high",
                    "line": i + 1,
                    "title": f"数组 {arr_name} 常量索引越界",
                    "description": (f"第{i+1}行 {arr_name}[{idx}] 越界："
                                    f"{arr_name} 声明大小为 {size}，合法下标 0~{size-1}，"
                                    f"访问 [{idx}] 会踩坏相邻内存（栈溢出/全局区踩踏）。"),
                    "suggestion": (f"把下标改为 0~{size-1}，或确认数组声明是否应改为 "
                                   f"{arr_name}[{idx+1}]。"),
                })

    # 匹配数组写入：array[index] = ...（index为非常量）
    # R3-a：补 (?!=) 排除 == 比较——此前 arr[i] == x 的第一个等号
    # 会被当作赋值匹配，导致"比较"被误报为"越界写"（与规则2 同款修复）
    array_access = re.compile(r"(\w+)\s*\[\s*(\w+)\s*\]\s*=(?!=)")
    for i, line in enumerate(cleaned_lines):
        m = array_access.search(line)
        if m:
            index_var = m.group(2)
            # 检查是否是常量索引（安全）
            if index_var.isdigit():
                continue
            # R3-c：数组"定义/初始化"行不是访问，必须跳过。
            # 形如 `uint32_t wConfig[NBR_OF_MOTORS] = {...}` / `static uint8_t t[SIZE] = {...}`，
            # 当长度写成宏名或枚举名（非数字）时，旧版把它当成"变量索引写访问"误报。
            # 真实工程实测 52 条命中里 22 条（42%）属于此类。
            # 判据：数组名之前紧邻另一个标识符（类型名），即"类型 + 名字 + ["；
            # 而真实访问 buf[i]= 的 '[' 前只有数组名本身（或 ->/. 结尾）。
            if re.search(r"[A-Za-z_]\w*[ \t]+$", line[:m.start(1)]):
                continue
            # R3-d：全大写标识符是宏/枚举常量（C 命名惯例），下标在编译期
            # 即确定，不存在运行期越界风险。实测 `configLUTs[0].input_source
            # [HAL_PLAY_LUT_INPUT3] = ...` 这类写法会被当成变量索引误报。
            if re.fullmatch(r"[A-Z][A-Z0-9_]*", index_var):
                continue
            arr_name = m.group(1)
            # 检查同一行是否有边界检查（如 if (i < SIZE) arr[i] = x;）
            same_line_check = re.search(
                r"if\s*\([^)]*(?:<|>|<=|>=|==|!=)\s*" + re.escape(index_var) + r"\b",
                line,
            )
            # 检查前面最多5行是否有对该变量的边界检查
            # 支持的模式：if (var < LIMIT), if (var >= SIZE), if (LIMIT > var) 等
            context_start = max(0, i - 5)
            context = "\n".join(cleaned_lines[context_start:i + 1])
            bound_patterns = [
                # var < LIMIT 或 var <= LIMIT 或 var > 0 等
                r"\b" + re.escape(index_var) + r"\s*(?:<|<=|>|>=|==|!=)\s*\w+",
                # LIMIT > var 或 LIMIT >= var 等
                r"\w+\s*(?:<|<=|>|>=|==|!=)\s*" + re.escape(index_var) + r"\b",
                # 函数式边界检查：check_bounds(var) / is_valid(var) / in_range(var)
                r"\b(?:check|valid|range|bound|within|assert)[\w]*\s*\([^)]*\b" + re.escape(index_var) + r"\b",
            ]
            # R3-e：收集豁免命中来源的上下文文本，供 off-by-one 泄漏判定
            exempt_texts = []
            if same_line_check:
                exempt_texts.append(line)
            has_check = any(re.search(p, context, re.IGNORECASE) for p in bound_patterns)
            if has_check:
                exempt_texts.append(context)
            # R3-b：循环头豁免——沿访问行向上查找所属最内层
            # for/while 循环头，循环条件含索引变量比较即视为有边界检查。
            # 原设计只回看5行，但循环头与循环体中后段访问的距离可以任意远
            # （如 for 头后第8行才写 arr[i]），超过窗口即误报。
            # 遇到独立右括号行（闭块）停止向上，防止把循环外/前序块误判为宿主。
            for j in range(i - 1, max(-1, i - 60), -1):
                lj = cleaned_lines[j]
                if re.search(r"^\s*\}\s*;?\s*$", lj):
                    break
                if re.search(r"\b(?:for|while)\s*\(", lj):
                    if any(re.search(p, lj, re.IGNORECASE) for p in bound_patterns):
                        has_check = True
                        exempt_texts.append(lj)
                    break
            if has_check:
                # R3-e：`<=` 型边界恰等于数组大小时，循环最后一轮访问
                # arr[size] 仍越界一字节——豁免收紧为改报 off-by-one。
                # `<`、`<= size-1`、宏名/变量上界（无法判定）维持豁免。
                leak = False
                size_known = None
                for def_ln, sz in reversed(array_sizes.get(arr_name, [])):
                    if def_ln <= i:
                        size_known = sz
                        break
                if size_known is not None:
                    for txt in exempt_texts:
                        lv = _le_boundary_val(txt, index_var, arr_name)
                        if lv == "SELF" or (isinstance(lv, int) and lv == size_known):
                            leak = True
                            break
                if not leak:
                    continue
                issues.append({
                    "rule_id": 3,
                    "severity": "high",
                    "line": i + 1,
                    "title": f"数组 {arr_name} 循环边界 off-by-one",
                    "description": (
                        f"第{i+1}行边界检查使用 <=（上界恰为数组大小 {size_known}），"
                        f"循环最后一轮会访问 {arr_name}[{size_known}]，越界写 1 个元素"
                        "踩坏相邻内存（栈/全局区相邻变量）。C 循环惯用法为左闭右开。"
                    ),
                    "suggestion": (
                        f"把 {index_var} <= 上界 改为 {index_var} < 上界"
                        f"（{arr_name} 合法下标 0~{size_known - 1}）。"
                    ),
                })
                continue
            issues.append({
                "rule_id": 3,
                "severity": "high",
                "line": i + 1,
                "title": "数组访问可能越界",
                "description": f"第{i+1}行使用变量 {index_var} 索引数组，但附近未发现边界检查。",
                "suggestion": f"在访问前检查：if ({index_var} < ARRAY_SIZE && {index_var} >= 0) {{ ... }}",
            })
    return issues


def _le_boundary_val(text: str, index_var: str, arr_name: str):
    """R3-e：从边界检查文本提取 `var <= 上界` 的可判定上界。

    只识别两种形态（其余返回 None → 维持豁免，宁漏勿误）：
      - 纯数字：i <= 10  -> int
      - sizeof(本数组)（含 sizeof(arr) / sizeof arr）-> "SELF"（恒等于数组大小）
    反向写法（10 >= i）同样识别。sizeof(arr[0]) 为元素大小，不属 SELF，
    词法不匹配返回 None 维持豁免（保守正确）。
    """
    num = r"[0-9]+(?:[uU][lL]{0,2}|[lL]{1,2}[uU]?)?"
    sz_self = r"sizeof\s*(?:\(\s*)?" + re.escape(arr_name) + r"\s*\)?"
    m = (re.search(r"\b" + re.escape(index_var) + r"\s*<=\s*(" + num + "|" + sz_self + ")", text)
         or re.search(r"(" + num + "|" + sz_self + r")\s*>=\s*\b" + re.escape(index_var) + r"\b", text))
    if not m:
        return None
    bound = m.group(1).strip()
    if bound.lower().startswith("sizeof"):
        return "SELF"
    try:
        return int(bound.rstrip("uUlL"))
    except ValueError:
        return None


_MEMCPY_FUNCS = ("memcpy", "memmove", "memset", "strncpy")


def _check_memcpy_overflow(cleaned_lines) -> list:
    """规则26（高危）：memcpy/memmove/memset/strncpy 长度实参超过目标数组大小。

    目标为已知大小的定长数组而长度实参为纯数字且超出、或为 sizeof(另一个
    更大的已知数组) 时，必然越界写踩内存。
    豁免（宁漏勿误）：长度为 sizeof(目标自身)/sizeof(目标[0]) 惯用法；
    目标名带下标引用（多维数组行元素，词法不可知）；目标不在数组大小表
    （指针/malloc/强转表达式）；长度为宏名/变量/含除法的 sizeof 表达式。
    """
    issues = []
    decl_re = re.compile(
        r"\b(?:static\s+|volatile\s+|const\s+)*"
        r"(?:unsigned\s+|signed\s+)?"
        r"(?:int|char|short|long|float|double|uint\d+_t|int\d+_t|size_t|u?int\w*_t)\b"
        r"[\s\*]+(\w+)\s*\[\s*(\d+)\s*\]"
    )
    array_sizes = {}
    for ln, line in enumerate(cleaned_lines):
        for dm in decl_re.finditer(line):
            array_sizes.setdefault(dm.group(1), []).append((ln, int(dm.group(2))))

    num = r"[0-9]+(?:[uU][lL]{0,2}|[lL]{1,2}[uU]?)?"
    # 实参可含一层嵌套括号（sizeof(x) 惯用法），[^()] 单层不够
    call_re = re.compile(r"\b(" + "|".join(_MEMCPY_FUNCS) + r")\s*\(((?:[^()]|\([^()]*\))*)\)")
    for i, line in enumerate(cleaned_lines):
        for cm in call_re.finditer(line):
            args = [a.strip() for a in cm.group(2).split(",")]
            if len(args) < 3:
                continue
            dst, n_expr = args[0], args[-1]
            if "/" in n_expr:      # sizeof(x)/sizeof(x[0]) 等除法形态保守放行
                continue
            dst_m = re.search(r"(?:\(\s*[\w\s\*]+?\s*\)\s*)*(\w+)\s*$", dst)
            if not dst_m or "[" in dst:
                continue
            dst_name = dst_m.group(1)
            size = None
            for def_ln, sz in reversed(array_sizes.get(dst_name, [])):
                if def_ln <= i:
                    size = sz
                    break
            if size is None:
                continue
            overflow = None
            if re.fullmatch(num, n_expr):
                val = int(n_expr.rstrip("uUlL"))
                if val > size:
                    overflow = f"长度实参 {val}"
            else:
                sz_m = re.fullmatch(
                    r"sizeof\s*(?:\(\s*)?(\w+)\s*(?:\[\s*\d+\s*\]\s*)?\)?\s*[uUlL]*",
                    n_expr,
                )
                if sz_m:
                    src_name = sz_m.group(1)
                    if src_name != dst_name:
                        src_size = None
                        for def_ln, sz in reversed(array_sizes.get(src_name, [])):
                            if def_ln <= i:
                                src_size = sz
                                break
                        if src_size is not None and src_size > size:
                            overflow = (f"长度实参 sizeof({src_name})（{src_name} 声明 "
                                        f"{src_size} 字节）")
            if overflow:
                issues.append({
                    "rule_id": 26,
                    "severity": "high",
                    "line": i + 1,
                    "title": f"{cm.group(1)} 写入长度超过目标数组大小",
                    "description": (
                        f"第{i+1}行 {cm.group(1)}() 目标 {dst_name} 声明大小为 {size} 字节，"
                        f"{overflow} 超出上限，必然越界写踩坏相邻内存"
                        "（栈溢出/全局区踩踏，且烧写现场难复现）。"
                    ),
                    "suggestion": (
                        f"核对目标 {dst_name} 大小（{size} 字节）与拷贝长度："
                        f"把长度压到 {size} 以内，或把 {dst_name} 声明加大到足够容纳。"
                    ),
                })
    return issues


def _check_array_param_sizeof(cleaned, cleaned_lines) -> list:
    """规则27（中危）：数组形参上做 sizeof。

    C99 6.7.5.3：形参声明的「数组类型」被调整为指针类型，
    `void f(uint8_t buf[16])` 里 sizeof(buf) == 指针大小（4/8），
    不是 16——memset(buf,0,sizeof(buf)) 只清 4 字节，属真 bug。
    sizeof(形参[0]) 取元素大小，合法，不报；裸指针形参不属本规则。
    """
    issues = []
    funcs = _find_all_function_ranges(cleaned)
    param_re = re.compile(
        r"\b(?:unsigned\s+|signed\s+|const\s+|volatile\s+)*"
        r"(?:int|char|short|long|float|double|uint\d+_t|int\d+_t|u?int\w*_t)\b"
        r"[\s\*]+(\w+)\s*\[\s*\d*\s*\]"
    )
    for f in funcs:
        sig = "\n".join(cleaned_lines[f["start"]:min(f["start"] + 8, len(cleaned_lines))])
        brace = sig.find("{")
        if brace >= 0:
            sig = sig[:brace]
        for pm in param_re.finditer(sig):
            pname = pm.group(1)
            sz_re = re.compile(r"sizeof\s*(?:\(\s*)?" + re.escape(pname) + r"\s*\)?(?!\s*\[)")
            for i in range(f["start"], min(f["end"] + 1, len(cleaned_lines))):
                line = cleaned_lines[i]
                if not sz_re.search(line):
                    continue
                issues.append({
                    "rule_id": 27,
                    "severity": "medium",
                    "line": i + 1,
                    "title": f"对数组形参 {pname} 使用 sizeof",
                    "description": (
                        f"第{i+1}行对形参 {pname} 求 sizeof。{pname} 虽声明为数组形参，"
                        "但 C99 6.7.5.3 规定形参数组类型被调整为指针——sizeof 得到的是"
                        "指针大小（4/8 字节）而非声明时的数组长度。常见后果：memset 只"
                        "清零前几个字节、memcpy 拷贝长度不足、缓冲区长度计算错误。"
                    ),
                    "suggestion": (
                        f"把数组长度作为独立参数传入（如 void f(uint8_t *{pname}, size_t len)），"
                        f"函数体内用 len，不用 sizeof({pname})。"
                    ),
                })
    return issues


def _check_register_magic(cleaned_lines) -> list:
    issues = []
    for i, line in enumerate(cleaned_lines):
        # 豁免 #define 行——do-while 宏体内的寄存器写是合法常用封装
        # （CMSIS/TivaWare 同款写法），检测目标是业务代码里的裸寄存器写
        if line.strip().startswith("#define"):
            continue
        if REGISTER_WRITE_RE.search(line):
            issues.append({
                "rule_id": 4,
                "severity": "high",
                "line": i + 1,
                "title": "寄存器写入使用硬编码数值",
                "description": f"第{i+1}行直接向寄存器写入数字，建议用宏定义描述位域含义，提高可读性和可维护性。",
                "suggestion": "使用 #define MODULE_BIT_POSITION (1U << 3) 等宏，或使用CMSIS位域定义。",
            })
    return issues


# ---- 规则19：硬编码寄存器指针解引用（高危） ----
# 匹配"整型常量强转为指针"（读/写解引用前必现），如：
#   *(volatile uint32_t*)0x40000000 = x;   （写）
#   x = *(uint32_t*)0x40000000UL;          （读）
# 类型名后带 * 且括号外紧跟 0x/十进制常量即命中；GPIO_TypeDef 等外设结构体
# 强转不在整型组内，不误报。
REG_PTR_DEREF_RE = re.compile(
    r"\*\s*\(\s*(?:volatile\s+|const\s+)*"
    r"(?:unsigned\s+|signed\s+)?"
    r"(?:int|long|short|char|uint\d+_t|int\d+_t|u8|u16|u32|u64|s8|s16|s32|s64)"
    r"\s*\*+\s*\)\s*(?:0x[0-9A-Fa-f]+|\d+)\s*[UuLl]*"
)


def _check_register_ptr_deref(cleaned_lines) -> list:
    """规则19（高危）：硬编码寄存器指针解引用。

    整型常量强转指针后直接解引用访问外设寄存器，绕过CMSIS外设定义，
    可读性/可移植性差且地址写错无任何编译期防护。#define 行豁免
    （外设库头文件自身即此写法）。
    """
    issues = []
    for i, line in enumerate(cleaned_lines):
        if line.strip().startswith("#define"):
            continue  # CMSIS/TivaWare 头文件自身即此写法，豁免
        if REG_PTR_DEREF_RE.search(line):
            issues.append({
                "rule_id": 19,
                "severity": "high",
                "line": i + 1,
                "title": "硬编码寄存器指针解引用",
                "description": (
                    f"第{i+1}行将整型常量强转为指针后直接解引用访问寄存器，"
                    "地址写错无编译期防护，且无法表达寄存器位域语义。"
                ),
                "suggestion": (
                    "改用CMSIS式外设寄存器宏：#define GPIOA ((GPIO_TypeDef *)GPIOA_BASE)，"
                    "再以 GPIOA->ODR 访问；或使用厂商头文件提供的外设符号定义。"
                ),
            })
    return issues


# ---- 规则20：裸 int 位域（MISRA R6.1 系，中危） ----
# `int x : 3;` 的符号性在 C99 中是实现定义（C99 6.7.2.5），跨工具链/编译器
# 可移植性差。MISRA C:2012 R6.1 要求位域只以明确类型声明（unsigned int /
# signed int / _Bool，AMD1 补充 _Bool）。
# 豁免：unsigned/signed 前缀；stdint 类型（uint8_t x:1 等）按缩量口径不报
# （工具链明确支持，STM32 LL 寄存器映射满屏此形态，报了无行动价值）。
# .h 头文件不豁免——位域重灾区恰在头文件寄存器映射。
BITFIELD_BARE_INT_RE = re.compile(r"(?<![A-Za-z0-9_])int\s+([A-Za-z_]\w*)\s*:\s*(\d+)")


def _check_bitfield(cleaned_lines) -> list:
    """规则20（中危）：裸 int 位域。

    实现定义符号性 + MISRA R6.1 合规双目标。多成员声明行
    （`int a:1, b:2;`）的逗号续位域按词法局限不逐个展开，报首个。
    """
    issues = []
    for i, line in enumerate(cleaned_lines):
        for m in BITFIELD_BARE_INT_RE.finditer(line):
            before = line[: m.start()].rstrip()
            # unsigned int / signed int 前缀豁免（int 前紧邻符号修饰符）
            if re.search(r"(?:unsigned|signed)$", before):
                continue
            issues.append({
                "rule_id": 20,
                "severity": "medium",
                "line": i + 1,
                "title": f"位域 {m.group(1)} 使用裸 int 类型",
                "description": (
                    f"第{i+1}行位域 {m.group(1)}:{m.group(2)} 声明为裸 int。"
                    "C99 中 int 位域的符号性是实现定义（C99 6.7.2.5），"
                    "同一代码在不同编译器下高位截断/符号扩展行为可能不同。"
                ),
                "suggestion": (
                    "显式声明符号性：unsigned int x:3（或 signed int x:3）；"
                    "MISRA C:2012 R6.1 要求位域只使用明确类型。"
                ),
            })
            break  # 每行只报一个
    return issues


# ---- 规则21：函数式宏副作用（MISRA Dir4.9 系，中危） ----
# 宏定义体内出现自增/自减或简单赋值：表达式语境下调用者的变量被暗中修改
# （`#define NEXT(n) ((n)++)` → `if (NEXT(i))` 里 i 被偷偷加一），
# Dir4.9 要求此类与函数不可安全互换的宏改用函数。
# 语料校准豁免口径（防止厂商库惯例刷屏）见 docstring。
DEFINE_RE = re.compile(r"^\s*#define\s+([A-Za-z_]\w*)(\([^)]*\))?\s?(.*)$")
MACRO_INCDEC_RE = re.compile(
    r"(?<![+\-\w])(?:\+\+|--)\s*[A-Za-z_]\w*"
    r"|[A-Za-z_]\w*(?:\s*\))*\s*(?:\+\+|--)(?![+\-\w])"
)
MACRO_ASSIGN_RE = re.compile(r"(?<![=!<>+\-*/&|^])=(?!=)")


def _mask_decl_blocks(body: str) -> str:
    """将 enum/struct/union 声明块内的内容置为空白（等长保列号）。

    块内的 `X = value` 是成员初始化不是赋值（TU_VERIFY_STATIC 编译期
    断言 `enum { CNT = 1/(expr) }` 惯用法同款），不得当作副作用。
    """
    out = list(body)
    for kw in ("enum", "struct", "union"):
        for m in re.finditer(r"\b" + kw + r"\b[^;{]*\{", body):
            depth = 0
            for k in range(m.end() - 1, len(body)):
                if body[k] == "{":
                    depth += 1
                elif body[k] == "}":
                    depth -= 1
                    if depth == 0:
                        for c in range(m.end(), k):
                            if out[c] != "\n":
                                out[c] = " "
                        break
    return "".join(out)


def _check_macro_side_effects(cleaned_lines) -> list:
    """规则21（中危）：函数式宏副作用。

    只扫单行 #define（续行符只作用首行，词法局限，文档已注明）。
    豁免：do-while(0) 语句封装；复合赋值（CMSIS SET_BIT 惯例，
    语料 6073 条无行动价值）；enum/struct/union 声明块（初始化语境）；
    函数调用（合法封装惯例，词法不可靠）。
    """
    issues = []
    for i, line in enumerate(cleaned_lines):
        m = DEFINE_RE.match(line)
        if not m:
            continue
        # 双下划线开头宏名豁免：C 标准保留命名空间（7.1.3），业务代码不应
        # 使用、厂商库（__HAL_* / __UNALIGNED_* 寄存器操作宏）用户不会改
        if m.group(1).startswith("__"):
            continue
        body = m.group(3)
        if re.search(r"\bdo\s*\{", body):
            continue  # do-while(0) 语句宏封装：调用者明确知道是语句，豁免
        masked = _mask_decl_blocks(body)
        # a) 自增/自减——副作用宏最毒形态（STATS_INC(i++) 双重自增陷阱）
        inc_m = MACRO_INCDEC_RE.search(masked)
        if inc_m:
            issues.append({
                "rule_id": 21,
                "severity": "medium",
                "line": i + 1,
                "title": f"宏 {m.group(1)} 定义体内含自增/自减（副作用）",
                "description": (
                    f"第{i+1}行宏 {m.group(1)} 的定义体中包含 ++/-- 操作。"
                    "该宏在表达式语境调用时调用者的变量被暗中修改，"
                    "参数或目标若带副作用会产生双重求值陷阱。"
                ),
                "suggestion": (
                    "改用 static inline 函数实现；或保证宏只在语句语境单独调用"
                    "并加 do { ... } while(0) 封装。"
                ),
            })
            continue
        # b) 简单赋值（复合赋值豁免，见 MACRO_ASSIGN_RE 前置字符排除）
        if MACRO_ASSIGN_RE.search(masked):
            issues.append({
                "rule_id": 21,
                "severity": "medium",
                "line": i + 1,
                "title": f"宏 {m.group(1)} 定义体内含赋值（副作用）",
                "description": (
                    f"第{i+1}行宏 {m.group(1)} 的定义体中包含赋值操作。"
                    "宏调用外观像函数调用（传值语义）却会修改调用者的变量/内存，"
                    "不可与函数安全互换。"
                ),
                "suggestion": (
                    "改用 static inline 函数实现同等功能（MISRA Dir4.9）；"
                    "确需保留时用 do { ... } while(0) 封装为显式语句宏。"
                ),
            })
    return issues


def _check_critical_section(cleaned_lines) -> list:
    issues = []
    disable_count = 0
    # 记录每一个尚未配对的关中断行号（1-based）。旧版只记最后一个，
    # 导致"一处死循环豁免"会连带掩盖同文件里另一处真正的漏配。
    pending_disable = []
    for i, line in enumerate(cleaned_lines):
        if re.search(r"__disable_irq\s*\(\)|disable_irq\s*\(|__set_PRIMASK\s*\(\s*1", line):
            disable_count += 1
            pending_disable.append(i + 1)
        if re.search(r"__enable_irq\s*\(\)|enable_irq\s*\(|__set_PRIMASK\s*\(\s*0", line):
            if disable_count > 0:
                disable_count -= 1
                pending_disable.pop()
            else:
                issues.append({
                    "rule_id": 5,
                    "severity": "medium",
                    "line": i + 1,
                    "title": "临界区开中断未匹配",
                    "description": f"第{i+1}行开中断，但之前没有对应的关中断。",
                    "suggestion": "检查临界区配对逻辑，确保关中断和开中断成对出现。",
                })
    # R5-a：关中断后紧跟死循环，是错误处理/断言失败的标准设计意图
    # （HAL 的 Error_Handler 就是 __disable_irq(); while(1); —— 关中断停机等复位，
    # 本来就不打算再开中断）。真实工程实测 27 条命中里 26 条（96%）属此类噪音。
    for disable_line in pending_disable:
        tail = "\n".join(cleaned_lines[disable_line: disable_line + 8])
        if re.search(r"while\s*\(\s*(?:1|true)\s*\)|for\s*\(\s*;\s*;\s*\)", tail):
            continue
        issues.append({
            "rule_id": 5,
            "severity": "medium",
            "line": disable_line,
            "title": "临界区未开中断配对",
            "description": f"第{disable_line}行关中断后未找到对应的开中断，可能导致系统关中断过久。",
            "suggestion": "确保临界区结束后立即开中断，或使用RAII风格的临界区守卫。",
        })
    return issues


# C类型/关键字：出现在return表达式里通常是强转，不算变量操作数
_C_EXPR_KEYWORDS = {
    "uint8_t", "int8_t", "uint16_t", "int16_t", "uint32_t", "int32_t",
    "uint64_t", "int64_t", "uint8", "int8", "uint16", "int16",
    "uint32", "int32", "uint64", "int64", "u8", "s8", "u16", "s16",
    "u32", "s32", "u64", "s64", "char", "short", "int", "long",
    "unsigned", "signed", "float", "double", "size_t", "bool", "_Bool",
    "sizeof", "NULL", "true", "false", "return", "const", "volatile",
    "static", "struct", "enum", "union", "ASSERT", "assert",
}

# 显式加宽强转：return (uint32_t)a*b 等写法已是推荐修复，不报
_WIDE_CAST_RE = re.compile(
    r"\(\s*(?:u?int(?:32|64)_t?|u?int(?:32|64)|unsigned\s+long(?:\s+long)?|"
    r"signed\s+long(?:\s+long)?|long\s+long|u32|u64|s32|s64|long)\s*\)")


def _return_expr_overflow_risk(expr) -> bool:
    """判断return表达式是否存在整数溢出风险。

    覆盖乘法/加法直接作为返回值的场景：溢出发生在表达式求值本身，
    无宽类型中间变量承接（如 return a*b*1000;）。
    豁免：纯常量运算、浮点表达式（规则7/10负责）、已显式加宽强转。
    """
    if not expr:
        return False
    # 剥离字符串/字符字面量，避免 "a*b" 之类内容误判
    expr_scan = re.sub(r'"(?:\\.|[^"\\])*"', '""', expr)
    expr_scan = re.sub(r"'(?:\\.|[^'\\])*'", "''", expr_scan)
    # 浮点表达式不归规则6管
    if re.search(r"\d+\.\d+|\bfloat\b|\bdouble\b|\d+f\b", expr_scan):
        return False
    # 已显式加宽到32/64位强转的不报
    if _WIDE_CAST_RE.search(expr_scan):
        return False
    idents = [w for w in re.findall(r"[A-Za-z_]\w*", expr_scan)
              if w not in _C_EXPR_KEYWORDS and not re.fullmatch(r"[uUlL]+", w)]
    if not idents:
        return False  # 纯常量运算（如 return 2*3;）无变量溢出风险
    has_mul = re.search(r"[A-Za-z_0-9)\]]\s*\*\s*[A-Za-z_0-9(]", expr_scan) is not None
    has_add = re.search(r"[A-Za-z_0-9)\]]\s*\+\s*[A-Za-z_0-9(]", expr_scan) is not None
    if has_mul:
        return True   # 乘法：任一变量操作数即风险
    if has_add and len(idents) >= 2:
        return True   # 加法：变量+变量组合才报，x+1/指针偏移等常见写法不报
    return False


def _check_integer_overflow(cleaned_lines) -> list:
    issues = []
    for i, line in enumerate(cleaned_lines):
        reported = False
        # 变量乘法后赋值给可能更小的类型
        if re.search(r"=\s*\w+\s*\*\s*\w+", line) and "uint" in line:
            if not re.search(r"sizeof|static_assert|ASSERT|assert", "\n".join(cleaned_lines[max(0,i-2):i+2])):
                issues.append({
                    "rule_id": 6,
                    "severity": "medium",
                    "line": i + 1,
                    "title": "整数乘法可能溢出",
                    "description": f"第{i+1}行整数乘法运算，建议检查操作数范围或使用更大类型。",
                    "suggestion": "使用uint32_t/uint64_t中间变量，或添加范围断言。",
                })
                reported = True
        # return表达式扫描——乘法/加法直接作为返回值（如 return a*b*1000;）
        # 支持同行函数体内的return（前缀允许 { 或 ;），如 { return a*b; }
        if not reported:
            m_ret = re.search(r"(?:^|[;{])\s*return\b\s*(.+?)\s*;\s*\}?\s*$", line)
            if m_ret and _return_expr_overflow_risk(m_ret.group(1)):
                if not re.search(r"sizeof|static_assert|ASSERT|assert", "\n".join(cleaned_lines[max(0,i-2):i+2])):
                    expr = m_ret.group(1)
                    op = "乘法" if re.search(r"[A-Za-z_0-9)\]]\s*\*\s*[A-Za-z_0-9(]", expr) else "加法"
                    issues.append({
                        "rule_id": 6,
                        "severity": "medium",
                        "line": i + 1,
                        "title": f"整数{op}可能溢出",
                        "description": (
                            f"第{i+1}行return表达式直接返回{op}结果，"
                            "无宽类型中间变量承接，窄整型下溢出发生在表达式求值本身。"
                        ),
                        "suggestion": (
                            "先赋值给uint32_t/uint64_t宽类型中间变量并检查范围后再返回，"
                            "如 uint32_t tmp = (uint32_t)a * b; return tmp;"
                        ),
                    })
    return issues


def _check_isr_float(lines, cleaned_lines, isr_ranges) -> list:
    issues = []
    float_pattern = re.compile(r"\b(?:float|double)\b|\d+\.\d+|->[fe]\d+")
    for start, end, name in isr_ranges:
        for i in range(start, min(end + 1, len(cleaned_lines))):
            if float_pattern.search(cleaned_lines[i]):
                issues.append({
                    "rule_id": 7,
                    "severity": "medium",
                    "line": i + 1,
                    "title": "ISR中使用浮点运算",
                    "description": f"中断服务函数 {name} 第{i+1}行包含浮点运算。Cortex-M4F的惰性压栈在中断中触发会导致额外的栈保存开销。",
                    "suggestion": "在ISR中避免浮点，将浮点计算移到主循环；如必须使用，在任务初始化时设置FPCCR控制惰性压栈。",
                })
    return issues


def _check_malloc_null(cleaned_lines, is_cpp: bool = False) -> list:
    """规则8（扩展）：malloc未判空 + C++ 文件裸 new 检测。

    C++ 分支（规则23，medium，MISRA C++:2008 18-4-1）：检测非放置形态的
    `new`。placement new（`new (buf) T()`）与 nothrow new（`new (std::nothrow)
    T()`）因 `new` 后紧跟 `(` 被排除——前者不占堆、后者失败返回 NULL 不抛异常，
    均为嵌入式 C++ 的合规形态。delete 不单独报：只释放不分配，无配对判定
    能力时报了是噪音（new 被报处已标记该文件需人工复核动态内存策略）。
    """
    issues = []
    for i, line in enumerate(cleaned_lines):
        if re.search(r"\b(?:malloc|calloc|realloc)\s*\(", line):
            # 检查后续3行是否有NULL检查
            context = "\n".join(cleaned_lines[i:min(i + 4, len(cleaned_lines))])
            if not re.search(r"!=\s*NULL|==\s*NULL|if\s*\(\s*!\s*\w+", context):
                issues.append({
                    "rule_id": 8,
                    "severity": "medium",
                    "line": i + 1,
                    "title": "malloc后未检查NULL",
                    "description": f"第{i+1}行动态内存分配后未检查返回值，内存分配失败时会导致空指针解引用。",
                    "suggestion": "ptr = malloc(size); if (ptr == NULL) { /* 错误处理 */ }",
                })
        if is_cpp and re.search(r"\bnew\b(?!\s*\()", line):
            issues.append({
                "rule_id": 23,
                "severity": "medium",
                "line": i + 1,
                "title": "C++动态内存分配（裸new）",
                "description": (f"第{i+1}行使用了非放置形态的 new。嵌入式C++惯例禁用"
                                "动态内存与异常：裸new失败将抛异常（禁异常环境=致命），"
                                "且堆碎片化在长期运行系统中不可控。"),
                "suggestion": ("静态分配/内存池替代；确需堆时用 nothrow new 并判空："
                               "ptr = new (std::nothrow) T(); if (!ptr) { /* 错误处理 */ }"),
            })
    return issues


def _check_hex_suffix(cleaned_lines) -> list:
    """规则24（low）：十六进制字面量缺 u/U 后缀（MISRA C:2012 R7.2 轻量口径）。

    R7.2 条文要求所有用于表达式的 8/16 进制整型常量加 u/U 后缀。完整检查
    需要类型分析，轻量口径按语料校准收窄（400 文件实测：全口径 13.7 万条
    命中不可用），只报同时满足以下条件的字面量：
      a) 非 #define 等预处理行（厂商库寄存器宏重灾区豁免）；
      b) 值 >= 0x80000000（落入 unsigned 域、int 混算越界的高危区间）；
      c) 同行参与位运算/算术运算（表达式语境近似）；
      d) 每文件限流 3 条（CMSIS-DSP 等三方库内部代码个位数命中不刷屏）。
    八进制不在轻量覆盖内（0 前缀误报源多，文档已注明）。
    """
    issues = []
    hex_re = re.compile(r"(?<![\w.])0[xX][0-9a-fA-F]+")
    op_re = re.compile(r"[|&^+\-*/]|<<|>>")
    reported = 0
    for i, line in enumerate(cleaned_lines):
        if reported >= 3:
            break
        if line.lstrip().startswith("#"):
            continue
        for m in hex_re.finditer(line):
            if re.match(r"[uUlL]", line[m.end():m.end() + 1]):
                continue
            if int(m.group(0), 16) < 0x80000000:
                continue
            if not op_re.search(line):
                continue
            issues.append({
                "rule_id": 24,
                "severity": "low",
                "line": i + 1,
                "title": "十六进制字面量缺u/U后缀",
                "description": (f"第{i+1}行 0x 十六进制常量 {m.group(0)} 未加 u/U 后缀且参与运算。"
                                "该值已落入 unsigned 域，与有符号量混算时类型提升语义易踩坑"
                                "（MISRA C:2012 R7.2 轻量口径）."),
                "suggestion": f"为常量加后缀：{m.group(0)}U（无符号运算语境）或改用带后缀的 stdint 宏。",
            })
            reported += 1
            break  # 每行最多一条
    return issues


def _check_hardcoded_delay(cleaned_lines, isr_ranges=None) -> list:
    """规则9（降级 low）：硬编码延时。

    - ISR 上下文内豁免：ISR 中的 HAL_Delay 已由规则1以高危报告，重复
      报告只增加噪音；
    - 主流程延时降为 low 并限流：LED 闪烁等待等场景属故意延时，报了
      用户通常不会改，保留提醒价值但不刷屏。
    """
    issues = []
    isr_lines = set()
    for start, end, _ in (isr_ranges or []):
        isr_lines.update(range(start, end + 1))
    for i, line in enumerate(cleaned_lines):
        if i in isr_lines:
            continue
        if re.search(r"\b(?:HAL_Delay|delay_ms|delay_us|sleep|usleep)\s*\(\s*\d+\s*\)", line):
            issues.append({
                "rule_id": 9,
                "severity": "low",
                "line": i + 1,
                "title": "硬编码延时用于时序",
                "description": f"第{i+1}行使用硬编码延时，实际时序受编译器优化和中断影响，不精确。",
                "suggestion": "使用硬件定时器(TIM)或DWT周期计数器做精确延时。",
            })
    return issues[:5]


def _check_float_equality(cleaned_lines) -> list:
    issues = []
    for i, line in enumerate(cleaned_lines):
        # 跳过变量声明行（收紧：声明必须带 = 赋值；此前
        # "float a) { if (a == 1.5f)" 这类带浮点参数的函数体行被误豁免漏报）
        if re.search(r"(?:const\s+)?(?:float|double)\s+\w+\s*=", line):
            continue
        # 匹配 variable == number 或 number == variable
        m = re.search(
            r"([a-zA-Z_]\w*)\s*==\s*([\d.]+[fFlL]?[uUlL]*)|([\d.]+[fFlL]?[uUlL]*)\s*==\s*([a-zA-Z_]\w*)",
            line,
        )
        if not m:
            continue
        # 判断是否真的是浮点比较：
        # 1. 数字字面量含小数点（如 3.14）
        # 2. 数字字面量有 f/F 后缀且无 u/U 后缀（如 1.0f, 2f）
        # 排除：0u, 1U, 0L, 10UL 等整数后缀
        num_str = m.group(2) or m.group(3) or ""
        is_float_literal = (
            "." in num_str
            or (re.search(r"[fF]$", num_str) and not re.search(r"[uU]", num_str))
        )
        if not is_float_literal:
            continue
        issues.append({
            "rule_id": 10,
            "severity": "medium",
            "line": i + 1,
            "title": "浮点数使用==比较",
            "description": f"第{i+1}行浮点数直接用==比较，由于浮点精度误差，应该比较绝对值差。",
            "suggestion": "if (fabsf(a - b) < 1e-6f) { ... }",
        })
    return issues


def _check_dangerous_funcs(cleaned_lines) -> list:
    issues = []
    for i, line in enumerate(cleaned_lines):
        for func, suggestion in DANGEROUS_FUNCS.items():
            if re.search(r"\b" + func + r"\s*\(", line):
                issues.append({
                    "rule_id": 11,
                    "severity": "medium",
                    "line": i + 1,
                    "title": f"使用不安全函数 {func}",
                    "description": f"第{i+1}行使用了 {func}()，存在缓冲区溢出风险。{suggestion}",
                    "suggestion": suggestion,
                })
    return issues


def _mask_struct_blocks(cleaned: str) -> str:
    """R12：将 struct/union 定义体替换为等长空白（保留换行与行号）。

    防止把结构体字段声明（如 ring_buffer.h 的 head/tail/count）当成
    "定义后未使用"的普通变量。等长替换保证后续行号计算不变。
    """
    out = list(cleaned)
    for kw in ("struct", "union"):
        for m in re.finditer(r"\b" + kw + r"\s*\w*\s*\{", cleaned):
            open_pos = m.end() - 1  # 指向 '{'
            depth = 0
            for k in range(open_pos, len(cleaned)):
                if cleaned[k] == "{":
                    depth += 1
                elif cleaned[k] == "}":
                    depth -= 1
                    if depth == 0:
                        for c in range(m.end(), k):
                            if out[c] != "\n":
                                out[c] = " "
                        break
    return "".join(out)


def _check_unused_vars(source, cleaned, is_header: bool = False) -> list:
    issues = []
    # R12：.h 文件整体豁免——头文件以类型/宏/函数声明为主，
    # "未使用变量"检测在声明语境下噪音远大于信号（结构体字段、
    # 前向声明关联符号均会被误报）
    if is_header:
        return issues
    # 屏蔽 struct/union 体内的字段声明后再统计
    masked = _mask_struct_blocks(cleaned)
    # 简化检测：找定义了但只出现一次的局部变量
    # R12-a：改用 finditer 拿匹配位置，修两处问题——
    #   1) extern 声明不是定义（其定义在别的编译单元），旧版会误报为"未使用"。
    #      真实工程实测 44 条命中里 13 条（30%）是 extern 声明；
    #   2) 行号改用匹配位置换算。旧版用 re.search(var) 找的是全文第一次出现，
    #      同名符号先出现在别处时会算错行。
    var_defs = re.compile(
        r"(?:uint\d+_t|int\d+_t|int|char|short|long|float|double|size_t)\s+(\w+)\s*(?:=|;)"
    )
    for m in var_defs.finditer(masked):
        var = m.group(1)
        if len(var) <= 2:
            continue
        # extern 声明不是定义，跳过
        _ls = masked.rfind("\n", 0, m.start()) + 1
        _le = masked.find("\n", m.start())
        if re.search(r"\bextern\b", masked[_ls: _le if _le != -1 else len(masked)]):
            continue
        count = len(re.findall(r"\b" + re.escape(var) + r"\b", masked))
        if count == 1:
            line_num = masked[:m.start(1)].count("\n") + 1
            issues.append({
                "rule_id": 12,
                "severity": "low",
                "line": line_num,
                "title": f"变量 {var} 定义后未使用",
                "description": f"变量 {var} 定义后未在代码中使用，可能是遗留代码。",
                "suggestion": "删除未使用的变量，保持代码整洁。",
            })
    return issues[:10]  # 限制数量避免噪音


def _check_magic_numbers(cleaned_lines) -> list:
    issues = []
    allowed = {"0", "1", "-1", "2", "10", "100", "1000", "0xFF", "0xFFF", "0xFFFF",
               "0xFFFFF", "0xFFFFFF", "0xFFFFFFFF", "16", "32", "64", "128", "256",
               "512", "4096", "8", "4", "3", "5", "6", "7", "9", "12", "24", "48"}
    for i, line in enumerate(cleaned_lines):
        if "#define" in line or "case " in line or "return" in line:
            continue
        if "." in line:  # 跳过含小数的行（浮点常量）
            continue
        # 与规则4同行去重——寄存器写入行的裸数字由规则4以高危报告，
        # 低危的魔术数字再报一次纯属重复
        if REGISTER_WRITE_RE.search(line):
            continue
        for m in MAGIC_NUMBER_RE.finditer(line):
            val = m.group(1)
            if val.lstrip("-") in allowed or val in allowed:
                continue
            if int(val) > 10000:
                continue
            before = line[:m.start(1)]
            # 数组下标豁免——arr[3000] 的下标语义由数组定义约束，
            # 访问处报魔术数字无行动价值
            if re.search(r"\[[^\]]*$", before):
                continue
            # 函数调用实参豁免——foo(3000) 的配置值语义由 API 名提供
            # （HAL_DAC_SetValue(...,3000)），真正需要命名的魔术数字出现在
            # 赋值右侧/比较/数组定义处，这些仍报。真实语料实测实参形态占
            # 命中的 61%，豁免后噪音大幅下降且不漏主要场景。
            # 注意排除 if/while/for/switch——"if (x > 3000)" 的 ( 是条件
            # 括号不是调用括号（负向断言会被关键字尾字符绕过，如 if 的 f，
            # 故抓出函数名整体判断）。
            m_call = re.search(r"(\w+)\s*\([^()]*$", before)
            if m_call and m_call.group(1).lower() not in ("if", "while", "for", "switch"):
                continue
            issues.append({
                "rule_id": 13,
                "severity": "low",
                "line": i + 1,
                "title": "魔术数字",
                "description": f"第{i+1}行出现裸数字 {val}，建议用#define定义为有意义的名称。",
                "suggestion": f"#define {val} 改为有意义的宏名，如 MAX_BUFFER_SIZE {val}",
            })
            break  # 每行只报一个
    return issues[:10]


def _check_missing_comments(source, cleaned_lines, commented_decls=None) -> list:
    """规则14（低危）：非static函数定义缺注释检测。

    --dir 批量模式下由 review_directory 预先收集各 .h 中带注释的
    函数声明名集合 commented_decls——"注释在 .h 声明处、.c 只留定义"
    是标准做法，此类函数不再报缺注释。单文件模式无跨文件信息，维持
    原逻辑（文档已标注局限）。
    """
    issues = []
    if commented_decls is None:
        commented_decls = set()
    # 找非static函数定义
    func_def = re.compile(r"^(?!static\b)(?:void|int|char|float|double|uint\d+_t|int\d+_t|size_t|bool|HAL_StatusTypeDef)\s+\**(\w+)\s*\([^)]*\)\s*\{?\s*$")
    # 工具生成函数豁免——MX_xxx_Init / HAL_xxx_MspInit 等由 CubeMX
    # 生成，用户改了注释也会在重新生成代码时被覆盖，报了无行动价值。
    # 真实语料实测此类命中占规则14的 15%。
    generated_fn = re.compile(
        r"^(?:MX_\w+_(?:Init|DeInit)|HAL_\w+_Msp(?:De)?Init|"
        r"HAL_\w+_ClockConfig|PeriphCommonClock_Config|SystemClock_Config|"
        r"SystemInit|Error_Handler|assert_failed)$"
    )
    for i, line in enumerate(cleaned_lines):
        m = func_def.match(line.strip())
        if m and "IRQHandler" not in m.group(1) and not generated_fn.match(m.group(1)):
            # R14：.h 中已有带注释的同名声明则豁免
            if m.group(1) in commented_decls:
                continue
            # 检查前3行是否有注释
            context = "\n".join(source.split("\n")[max(0, i - 3):i])
            if not re.search(r"(?:/\*|\*|//)", context):
                issues.append({
                    "rule_id": 14,
                    "severity": "low",
                    "line": i + 1,
                    "title": f"函数 {m.group(1)} 缺少注释",
                    "description": f"公有函数 {m.group(1)} 定义前没有注释说明。",
                    "suggestion": "添加Doxygen注释：/** @brief 功能描述 @param 参数 @return 返回值 */",
                })
    return issues[:5]


def _check_switch_default(cleaned_lines) -> list:
    issues = []
    in_switch = False
    switch_line = 0
    brace_depth = 0
    has_default = False

    for i, line in enumerate(cleaned_lines):
        if re.search(r"\bswitch\s*\(", line):
            in_switch = True
            switch_line = i + 1
            brace_depth = 0
            has_default = False
        if in_switch:
            brace_depth += line.count("{") - line.count("}")
            if re.search(r"\bdefault\s*:", line):
                has_default = True
            if brace_depth <= 0 and "{" in "".join(cleaned_lines[switch_line - 1:i + 1]):
                if not has_default:
                    issues.append({
                        "rule_id": 15,
                        "severity": "low",
                        "line": switch_line,
                        "title": "switch缺少default分支",
                        "description": f"第{switch_line}行的switch语句没有default分支，未处理的枚举值可能导致未定义行为。",
                        "suggestion": "添加 default: break; 或 default: ASSERT(0); 处理意外情况。",
                    })
                in_switch = False
    return issues


def _find_all_function_ranges(cleaned: str) -> list:
    """识别所有函数定义，返回[{"name", "start", "end", "name_pos"}]。

    start/end 为函数体起止行号（0-based，含定义行），name_pos 为函数名
    在 cleaned 中的绝对偏移（用于区分"定义头"与"调用"）。
    与 _find_isr_functions 使用相同的函数定义正则，保证行为一致。
    """
    funcs = []
    # 与 _find_isr_functions 共用 FUNC_DEF_RE，保证函数边界判定一致
    func_def = FUNC_DEF_RE
    for m in func_def.finditer(cleaned):
        name = m.group(1)
        # if/while/for/switch 等关键字不是函数名（旧版会造出名为 if 的伪函数）
        if name in _FUNC_NAME_BLOCKLIST:
            continue
        start_pos = m.start()
        # 用函数名所在行换算起始行（旧版用 m.start() 会整体上移一行）
        start_line = cleaned[:m.start(1)].count("\n")
        brace_count = 0
        found_start = False
        for i in range(start_pos, len(cleaned)):
            if cleaned[i] == "{":
                brace_count += 1
                found_start = True
            elif cleaned[i] == "}":
                brace_count -= 1
                if found_start and brace_count == 0:
                    end_line = cleaned[:i].count("\n")
                    funcs.append({
                        "name": name,
                        "start": start_line,
                        "end": end_line,
                        "name_pos": m.start(1),
                    })
                    break
    return funcs


def _check_rtos_in_isr(cleaned_lines, isr_ranges) -> list:
    """规则16（高危）：中断上下文调用可能阻塞的RTOS API。

    FreeRTOS任务级API（vTaskDelay/xQueueSend/xSemaphoreTake等）只允许在
    任务上下文调用；ISR内调用会破坏调度器状态、触发configASSERT或硬错误。
    以 FromISR 结尾的变体是中断安全版本，不报。
    """
    issues = []
    api_names = "|".join(re.escape(a) for a in RTOS_BLOCKING_APIS)
    call_re = re.compile(r"\b(" + api_names + r"[A-Za-z0-9_]*)\s*\(")
    for start, end, name in isr_ranges:
        for i in range(start, min(end + 1, len(cleaned_lines))):
            for m in call_re.finditer(cleaned_lines[i]):
                func_name = m.group(1)
                if func_name.endswith("FromISR"):
                    continue  # FromISR变体中断安全，合法用法
                issues.append({
                    "rule_id": 16,
                    "severity": "high",
                    "line": i + 1,
                    "title": f"中断上下文调用可能阻塞的RTOS API {func_name}",
                    "description": (
                        f"中断服务函数 {name} 第{i+1}行调用了FreeRTOS任务级API {func_name}()。"
                        "该API仅允许在任务上下文调用，ISR中调用会导致调度器状态被破坏、"
                        "触发configASSERT断言或直接HardFault。"
                    ),
                    "suggestion": (
                        f"改用中断安全版本 {func_name}FromISR()（若存在），"
                        "或仅在ISR中置volatile标志，把耗时处理移到任务中。"
                    ),
                })
    return issues


def _check_rtthread_in_isr(cleaned_lines, isr_ranges) -> list:
    """规则22：中断上下文调用 RT-Thread 违规 API。

    双源判据（2026-09-15 核实）：
    - 官方编程手册《中断管理》：ISR 内不能使用挂起当前线程的操作，
      违规内核报 "Function [xxx] shall not used in ISR"
    - 官方内核 master 源码：对象创建/删除类（rt_sem_create 等）带
      RT_DEBUG_NOT_IN_INTERRUPT 断言；rt_sem_take 无中断断言，
      timeout=0（RT_WAITING_NO）不挂起

    分级：
      high：睡眠/线程管理类、动态内存类、对象创建/删除类（源码断言实锤）、
            rt_mutex_take（互斥量所有者语义，任何 timeout）、等待类 API
            非零 timeout（含 RT_WAITING_FOREVER）
      low： 等待类 API timeout=0 试探型（master 内核可运行、不挂起，
            但依赖内核实现细节，非官方推荐写法）
    不报：rt_sem_release/rt_event_send/rt_mb_send/rt_mq_send 等
          ISR 安全 API（官方底半处理范例用法）
    MISRA：RTOS 工程规则，无直接对应条款，如实标注
    """
    issues = []

    def _timeout_is_zero(args_text: str, pos: int) -> bool:
        # 实参按顶层逗号切分（不含嵌套括号的简单调用）；抓不到指定位置
        # 实参（多行调用/嵌套括号截断）返回 False 按阻塞型保守处理
        parts = args_text.split(",")
        if len(parts) < pos:
            return False
        arg = parts[pos - 1].strip()
        return bool(re.fullmatch(r"0[uUlL]*|RT_WAITING_NO", arg))

    fixed_re = re.compile(
        r"\b(" + "|".join(re.escape(a) for a in
                          RTTHREAD_THREAD_APIS + RTTHREAD_MEM_APIS
                          + RTTHREAD_OBJ_CREATE_APIS + RTTHREAD_MUTEX_APIS)
        + r")\s*\(([^()]*)"
    )
    wait_re = re.compile(
        r"\b(" + "|".join(re.escape(a) for a in RTTHREAD_WAIT_APIS)
        + r")\s*\(([^()]*)"
    )
    for start, end, name in isr_ranges:
        for i in range(start, min(end + 1, len(cleaned_lines))):
            line = cleaned_lines[i]
            for m in fixed_re.finditer(line):
                api = m.group(1)
                issues.append({
                    "rule_id": 22,
                    "severity": "high",
                    "line": i + 1,
                    "title": f"中断上下文调用 RT-Thread 违规 API {api}",
                    "description": (
                        f"中断服务函数 {name} 第{i+1}行调用了 {api}()。"
                        "官方规定 ISR 内不能执行挂起当前线程的操作"
                        "（内核报 Function [xxx] shall not used in ISR），"
                        "对象创建/删除类在内核源码中带中断上下文断言。"
                    ),
                    "suggestion": (
                        "ISR 内只做硬件操作与置标志/发信号"
                        "（rt_sem_release/rt_event_send/rt_mb_send），"
                        "把该调用移到唤醒的任务线程中执行。"
                    ),
                })
            for m in wait_re.finditer(line):
                api = m.group(1)
                if _timeout_is_zero(m.group(2), RTTHREAD_WAIT_APIS[api]):
                    issues.append({
                        "rule_id": 22,
                        "severity": "low",
                        "line": i + 1,
                        "title": f"ISR 内试探型等待 {api}(…, 0)",
                        "description": (
                            f"中断服务函数 {name} 第{i+1}行以 timeout=0 调用 "
                            f"{api}()。master 内核无中断断言且不挂起，"
                            "当前可运行，但依赖内核实现细节而非官方推荐写法，"
                            "换内核版本/移植有风险。"
                        ),
                        "suggestion": (
                            "改为在 ISR 内置 volatile 标志，"
                            "由任务线程做带等待的 take/recv。"
                        ),
                    })
                else:
                    issues.append({
                        "rule_id": 22,
                        "severity": "high",
                        "line": i + 1,
                        "title": f"中断上下文调用阻塞型 API {api}",
                        "description": (
                            f"中断服务函数 {name} 第{i+1}行以非零 timeout 调用 "
                            f"{api}()，该调用会挂起当前线程。ISR 没有线程控制块，"
                            "官方明确禁止（Function [xxx] shall not used in ISR）。"
                        ),
                        "suggestion": (
                            "ISR 内改用 rt_sem_release/rt_mb_send 等发送类 API "
                            "通知任务，由任务线程做等待接收。"
                        ),
                    })
    return issues


def _check_large_local_arrays(cleaned, cleaned_lines) -> list:
    """规则17（中危）：大局部数组可能耗尽任务栈。

    按类型大小估算函数内局部数组累计字节数，>=512字节即命中。
    static局部数组存放在静态存储区、不占栈，排除不报。
    """
    issues = []
    funcs = _find_all_function_ranges(cleaned)
    threshold = LOCAL_ARRAY_STACK_THRESHOLD
    for f in funcs:
        start, end, fname = f["start"], f["end"], f["name"]
        total = 0
        details = []
        for i in range(start, min(end + 1, len(cleaned_lines))):
            line = cleaned_lines[i]
            if "static" in line:
                continue  # static数组不占栈
            if not line.rstrip().endswith(";"):
                continue  # 排除函数参数列表等非声明行
            for m in LOCAL_ARRAY_RE.finditer(line):
                ctype = m.group("type")
                elem = TYPE_SIZES.get(ctype)
                if elem is None:
                    continue
                arr_len = int(m.group("size"))
                size = arr_len * elem
                total += size
                details.append((i + 1, m.group("name"), arr_len, elem, size))
        if total >= threshold and details:
            first_line = details[0][0]
            det_str = "、".join(f"{n}[{l}×{e}B={s}B]" for _, n, l, e, s in details)
            issues.append({
                "rule_id": 17,
                "severity": "medium",
                "line": first_line,
                "title": "大局部数组可能耗尽任务栈",
                "description": (
                    f"函数 {fname} 内局部数组累计约 {total} 字节（{det_str}），"
                    f"达到{threshold}字节阈值。FreeRTOS默认任务栈常为128~512字"
                    "（512~2048字节），大数组极易栈溢出并踩坏相邻任务/TCB内存。"
                ),
                "suggestion": (
                    "改为static局部变量/全局缓冲区/消息队列传递（注意重入与并发），"
                    "或增大任务栈并用uxTaskGetStackHighWaterMark()验证余量。"
                ),
            })
    return issues


def _check_recursion(cleaned, cleaned_lines) -> list:
    """规则18（中危）：递归函数检测。

    直接自调用：函数体内调用自身（精确定位，排除定义头本身）。
    间接递归：基于函数调用图做深度限制的DFS找环，同一环只报一次。
    """
    issues = []
    funcs = _find_all_function_ranges(cleaned)
    if not funcs:
        return issues

    # 行首偏移表：把绝对偏移转为(行号, 列号)
    line_starts = [0]
    for idx, ch in enumerate(cleaned):
        if ch == "\n":
            line_starts.append(idx + 1)

    def _pos_to_line_col(pos: int):
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo, pos - line_starts[lo]

    # 定义头位置集合：(0-based行号, 函数名列号) -> 函数名
    def_locations = {}
    for f in funcs:
        line_no, col = _pos_to_line_col(f["name_pos"])
        def_locations[(line_no, col)] = f["name"]

    # 建调用图（只统计本文件有定义的函数；自调用记为自环）
    call_graph = {f["name"]: set() for f in funcs}
    call_re = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
    for f in funcs:
        fname = f["name"]
        for i in range(f["start"], min(f["end"] + 1, len(cleaned_lines))):
            line_abs_base = line_starts[i] if i < len(line_starts) else 0
            for m in call_re.finditer(cleaned_lines[i]):
                if (i, m.start(1)) in def_locations:
                    continue  # 函数定义头本身，不是调用
                callee = m.group(1)
                if callee in call_graph:
                    call_graph[fname].add(callee)

    # 找环：直接自环 + 间接环（DFS，深度限制防爆炸）
    raw_cycles = []
    MAX_DEPTH = 12

    def _dfs(node, path, on_path):
        for nxt in sorted(call_graph.get(node, ())):
            if nxt == path[0]:
                raw_cycles.append(path[:])
            elif nxt not in on_path and len(path) < MAX_DEPTH:
                _dfs(nxt, path + [nxt], on_path | {nxt})

    for node in sorted(call_graph):
        _dfs(node, [node], {node})

    # 环规范化去重：环 [A,B,C] 与 [B,C,A] 视为同一个
    def _canon(cyc):
        rots = [tuple(cyc[i:] + cyc[:i]) for i in range(len(cyc))]
        return min(rots)

    seen = set()
    func_by_name = {f["name"]: f for f in funcs}
    for cyc in raw_cycles:
        key = _canon(cyc)
        if key in seen:
            continue
        seen.add(key)
        starter = cyc[0]
        f = func_by_name[starter]
        if len(cyc) == 1:
            chain = f"函数 {starter} 在函数体内直接调用自身"
        else:
            chain = "调用链 " + " -> ".join(cyc + [cyc[0]]) + " 形成间接递归环"
        issues.append({
            "rule_id": 18,
            "severity": "medium",
            "line": f["start"] + 1,
            "title": "递归在无MMU的MCU上有栈溢出风险，建议改写为迭代",
            "description": (
                f"{chain}。递归在无MMU的MCU上无法按需扩展栈，"
                "每次递归都消耗栈帧，深层递归会溢出任务栈/主栈并踩坏相邻内存。"
            ),
            "suggestion": (
                "改写为迭代实现（循环+显式栈/表驱动）；"
                "如必须保留，严格限制递归深度并核算最坏情况栈占用。"
            ),
        })
    return issues


def review_directory(dir_path: str, rules: str = "all") -> dict:
    """批量扫描目录下所有 .c/.h 文件，输出汇总报告。

    Args:
        dir_path: 目录路径（递归遍历）
        rules: "all"/"high"/"medium"/"low"

    Returns:
        {"success", "mode": "directory", "dir", "summary", "top5_files", "files"}
    """
    if not os.path.isdir(dir_path):
        return {"success": False, "error": f"目录不存在: {dir_path}"}
    if rules not in ("all", "high", "medium", "low"):
        return {"success": False, "error": f"无效的rules参数: {rules}（可选all/high/medium/low）"}

    c_files = []
    for root, dirs, files in os.walk(dir_path):
        dirs.sort()
        for fn in sorted(files):
            # 纳入 C++ 扩展名（.cpp/.cc/.cxx 源文件 + .hpp/.hh 头文件）
            if fn.lower().endswith(SOURCE_EXTS + HEADER_EXTS):
                c_files.append(os.path.join(root, fn))

    # R14：第一遍收集各 .h 中"带注释的函数声明名"集合，
    # 供第二遍审查 .c 时豁免"注释在 .h 声明处"的函数
    commented_decls = set()
    for fp in c_files:
        if not fp.lower().endswith(".h"):
            continue
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                h_source = f.read()
        except OSError:
            continue
        h_clean = _strip_comments_strings(h_source)
        h_lines = h_source.split("\n")
        h_clean_lines = h_clean.split("\n")
        proto_re = re.compile(
            r"^\s*(?!static\b)(?:[A-Za-z_][\w\s\*]*?)\s+([A-Za-z_]\w*)\s*\([^;{}]*\)\s*;\s*$"
        )
        for i, cl in enumerate(h_clean_lines):
            pm = proto_re.match(cl)
            if not pm:
                continue
            ctx = "\n".join(h_lines[max(0, i - 3):i + 1])
            if re.search(r"(?:/\*|\*|//)", ctx):
                commented_decls.add(pm.group(1))

    results = []
    for fp in c_files:
        try:
            r = review_code(file_path=fp, rules=rules, commented_decls=commented_decls)
        except Exception as e:
            r = {"success": False, "error": f"审查失败: {e}"}
        entry = {"file": fp}
        entry.update(r)
        results.append(entry)

    scanned = [r for r in results if r.get("success")]
    skipped = [r for r in results if not r.get("success")]
    high = sum(r["summary"]["high"] for r in scanned)
    medium = sum(r["summary"]["medium"] for r in scanned)
    low = sum(r["summary"]["low"] for r in scanned)
    total_issues = high + medium + low

    top5 = sorted(scanned, key=lambda r: (-r["summary"]["total"], r["file"]))[:5]
    top5_files = [
        {"file": r["file"], "issues": r["summary"]["total"]}
        for r in top5 if r["summary"]["total"] > 0
    ]

    return {
        "success": True,
        "misra_note": MISRA_NOTICE,
        "mode": "directory",
        "dir": dir_path,
        "summary": {
            "total_files": len(c_files),
            "scanned": len(scanned),
            "skipped": len(skipped),
            "high": high,
            "medium": medium,
            "low": low,
            "total_issues": total_issues,
        },
        "top5_files": top5_files,
        "files": results,
    }


def generate_html_report(result: dict) -> str:
    """把审查结果渲染为单文件 HTML 报告（内联样式，无外部依赖）。

    兼容单文件模式与 --dir 批量模式两种 result 结构。
    中文界面、浅色配色（打印/截图分享友好），按严重度分色 + 规则分布条形图。
    """
    import html as _html
    from datetime import datetime

    def esc(s) -> str:
        return _html.escape(str(s), quote=True)

    issues_by_file = []
    if result.get("success") and result.get("mode") == "directory":
        for f in result.get("files", []):
            if f.get("success") and f.get("issues"):
                issues_by_file.append({"file": f["file"], "issues": f["issues"]})
        scan_desc = f"扫描目录 {result.get('dir', '')}"
    elif result.get("success"):
        issues_by_file.append({"file": result.get("file", ""), "issues": result.get("issues", [])})
        scan_desc = f"审查文件 {result.get('file', '')}"

    summary = result.get("summary", {})
    sev_cnt = {"high": summary.get("high", 0),
               "medium": summary.get("medium", 0),
               "low": summary.get("low", 0)}
    total = summary.get("total_issues", summary.get("total", sum(sev_cnt.values())))
    n_files = summary.get("scanned", 1)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 规则分布（降序）
    rule_counts = {}
    for fb in issues_by_file:
        for it in fb["issues"]:
            rule_counts[it.get("rule_id", 0)] = rule_counts.get(it.get("rule_id", 0), 0) + 1
    max_cnt = max(rule_counts.values()) if rule_counts else 1
    bars = "".join(
        f'<div class="bar-row"><div class="bar-label" title="R{esc(rid)}">{esc(rid)}号规则</div>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{c / max_cnt * 100:.0f}%"></div></div>'
        f'<div class="bar-count">{c}</div></div>'
        for rid, c in sorted(rule_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    )

    sev_label = {"high": "高危", "medium": "中危", "low": "低危"}
    blocks = []
    for fb in issues_by_file:
        rows = []
        for it in fb["issues"]:
            sev = it.get("severity", "low")
            misra = it.get("misra", "")
            misra_html = f'<span class="misra">{esc(misra)}</span>' if misra else ""
            rows.append(
                f'<div class="issue {esc(sev)}">'
                f'<div class="issue-head"><span class="sev {esc(sev)}">{sev_label.get(sev, sev)}</span>'
                f'R{esc(it.get("rule_id", "?"))} {esc(it.get("title", ""))}{misra_html}</div>'
                f'<div class="issue-meta">第 {esc(it.get("line", "?"))} 行</div>'
                f'<div class="issue-desc">{esc(it.get("description", ""))}</div>'
                f'<div class="issue-fix">✔ {esc(it.get("suggestion", ""))}</div>'
                f'</div>'
            )
        if rows:
            blocks.append(
                f'<div class="file-block"><div class="file-name">{esc(fb["file"])}</div>{"".join(rows)}</div>'
            )
    detail = "".join(blocks) if blocks else '<div class="ok">✔ 未发现问题（按当前规则集）</div>'

    # MISRA 覆盖声明（动态统计映射表，诚实口径）
    c12_refs = sum(1 for refs in MISRA_MAPPING.values()
                   if refs and not all(r.startswith("C++") for r in refs))
    cpp_refs = sum(1 for refs in MISRA_MAPPING.values()
                   if refs and all(r.startswith("C++") for r in refs))
    misra_note = (
        f'<div class="misra-note"><b>MISRA 覆盖声明：</b>'
        f'本工具将 {c12_refs} 条审查规则映射到 MISRA C:2012 规则编号'
        f'（含 {cpp_refs} 条 MISRA C++:2008 映射），'
        f'其中部分规则为轻量口径（如 R7.2 仅覆盖大值+表达式语境的十六进制常量）。'
        f'本工具<b>不构成完整 MISRA 合规检查</b>，正式合规认证请使用 '
        f'PC-lint Plus / Polyspace / Coverity 等工业工具。'
        f'完整映射表见包内 <code>references/misra-mapping.md</code>。</div>'
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>嵌入式代码审查报告 - {esc(now)}</title>
<style>
:root{{--red:#d93026;--orange:#e8710a;--yellow:#b8860b;--ink:#1f2328;--muted:#656d76;--line:#d8dee4;--bg:#f6f8fa}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Microsoft YaHei","PingFang SC",sans-serif;color:var(--ink);background:#fff;padding:32px 40px;max-width:1100px;margin:0 auto}}
h1{{font-size:22px}} .meta{{color:var(--muted);font-size:13px;margin:6px 0 20px}}
.cards{{display:flex;gap:14px;margin-bottom:24px}}
.card{{flex:1;border:1px solid var(--line);border-radius:8px;padding:14px 18px;background:var(--bg)}}
.card .num{{font-size:28px;font-weight:700}}
.card.h .num{{color:var(--red)}}.card.m .num{{color:var(--orange)}}.card.l .num{{color:var(--yellow)}}.card.f .num{{color:#0969da}}
.card .lbl{{font-size:13px;color:var(--muted);margin-top:2px}}
.bar-row{{display:flex;align-items:center;gap:10px;margin:6px 0;font-size:13px}}
.bar-label{{width:210px;color:var(--muted);text-align:right}}
.bar-track{{flex:1;background:var(--bg);border-radius:4px;height:16px;overflow:hidden}}
.bar-fill{{height:100%;background:#0969da}}
.bar-count{{width:36px;font-weight:600}}
h2{{font-size:16px;margin:26px 0 12px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.file-block{{margin-bottom:20px}}
.file-name{{font-family:Consolas,monospace;font-size:13px;color:#0969da;margin-bottom:8px;word-break:break-all}}
.issue{{border:1px solid var(--line);border-left-width:4px;border-radius:6px;padding:10px 14px;margin-bottom:8px}}
.issue.high{{border-left-color:var(--red)}}.issue.medium{{border-left-color:var(--orange)}}.issue.low{{border-left-color:var(--yellow)}}
.issue-head{{font-size:14px;font-weight:600}}
.sev{{display:inline-block;font-size:11px;font-weight:600;border-radius:4px;padding:1px 6px;margin-right:8px;color:#fff}}
.sev.high{{background:var(--red)}}.sev.medium{{background:var(--orange)}}.sev.low{{background:var(--yellow)}}
.issue-meta{{font-size:12px;color:var(--muted);margin:3px 0 6px;font-family:Consolas,monospace}}
.issue-desc{{font-size:13px;margin:4px 0}}
.issue-fix{{font-size:13px;color:#116329;background:#f0fff4;border-radius:4px;padding:5px 8px;margin-top:5px}}
.misra{{display:inline-block;font-size:11px;font-weight:normal;color:#8250df;background:#faf5ff;border:1px solid #e5d9f2;border-radius:4px;padding:1px 6px;margin-left:6px}}
.ok{{color:#116329;background:#f0fff4;border:1px solid #cef0d4;border-radius:8px;padding:16px;font-size:14px}}
footer{{margin-top:30px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:12px}}
.misra-note{{margin-top:22px;font-size:12px;color:var(--muted);background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:10px 14px;line-height:1.7}}
.misra-note code{{font-family:Consolas,monospace;background:#fff;padding:1px 4px;border-radius:3px;border:1px solid var(--line)}}
</style>
</head>
<body>
<h1>嵌入式代码审查报告</h1>
<div class="meta">{esc(scan_desc)} · 生成时间 {esc(now)} · 共 {n_files} 个文件 · {total} 个问题</div>
<div class="cards">
<div class="card h"><div class="num">{sev_cnt['high']}</div><div class="lbl">高危</div></div>
<div class="card m"><div class="num">{sev_cnt['medium']}</div><div class="lbl">中危</div></div>
<div class="card l"><div class="num">{sev_cnt['low']}</div><div class="lbl">低危</div></div>
<div class="card f"><div class="num">{n_files}</div><div class="lbl">扫描文件</div></div>
</div>
<h2>规则分布</h2>
{bars if bars else '<div class="meta">无问题记录</div>'}
<h2>问题明细</h2>
{detail}
{misra_note}
<footer>{esc(MISRA_NOTICE)}<br>embedded-code-reviewer 1.1.0 · 单文件 HTML 报告，可直接分享/存档</footer>
</body>
</html>"""


if __name__ == "__main__":
    # exit code 约定（CI集成友好）：
    #   0 = 扫描成功且未发现问题
    #   1 = 扫描成功但发现问题（供CI/脚本判断）
    #   2 = 内部错误或用法错误（参数缺失/互斥冲突/异常，扫描未正常完成）
    import sys
    argv = sys.argv[1:]
    if not argv or argv[0] in ("--help", "-h"):
        print("""用法: python reviewer.py <file.c> [rules] [--html 报告.html]
      python reviewer.py --dir <目录路径> [rules] [--html 报告.html]

参数:
  file.c      C源代码文件路径（单文件模式）
  --dir 目录  递归扫描目录下所有 .c/.h 文件（批量模式，与单文件模式互斥）
  rules       all|high|medium|low，默认all
  --html 路径  额外生成单文件HTML报告（中文界面，可截图分享/存档）

文件类型: C (.c/.h) 全规则；C++ (.cpp/.cc/.cxx/.hpp/.hh) 轻量支持——
  C 风格 C++ 直接复用全部规则，另检裸 new（规则23），不做模板/重载语义分析

exit code: 0=无问题；1=发现问题；2=用法/内部错误

示例:
  python reviewer.py main.c
  python reviewer.py main.cpp
  python reviewer.py main.c high
  python reviewer.py --dir ./src
  python reviewer.py --dir ./src high --html report.html""")
        sys.exit(0 if argv else 2)

    # 可选 --html <输出路径>，从 argv 摘除后不影响原有解析
    html_path = None
    if "--html" in argv:
        hi = argv.index("--html")
        if hi + 1 >= len(argv):
            print(json.dumps({"success": False, "error": "--html 需要输出文件路径参数"}, ensure_ascii=False))
            sys.exit(2)
        html_path = argv[hi + 1]
        argv = argv[:hi] + argv[hi + 2:]

    # 互斥校验：--dir 与单文件模式不能混用（用法错误）
    if "--dir" in argv and argv[0] != "--dir":
        print(json.dumps({"success": False,
                          "error": "--dir 批量模式与单文件模式互斥，不能同时使用"}, ensure_ascii=False))
        sys.exit(2)

    if argv[0] == "--dir":
        if len(argv) < 2:
            print(json.dumps({"success": False, "error": "--dir 需要目录路径参数"}, ensure_ascii=False))
            sys.exit(2)
        dir_arg = argv[1]
        r = argv[2] if len(argv) > 2 else "all"
        if len(argv) > 3 or (len(argv) == 3 and r not in ("all", "high", "medium", "low")):
            print(json.dumps({"success": False,
                              "error": "--dir 批量模式与单文件模式互斥，只接受 [rules] 一个附加参数"}, ensure_ascii=False))
            sys.exit(2)
        try:
            result = review_directory(dir_arg, r)
        except Exception as e:
            result = {"success": False, "error": f"批量扫描失败: {e}"}
    else:
        fp = argv[0]
        r = argv[1] if len(argv) > 1 else "all"
        try:
            result = review_code(file_path=fp, rules=r)
        except Exception as e:
            result = {"success": False, "error": f"审查失败: {e}"}
    # 生成 HTML 报告（JSON 输出中带 html_report 字段指向报告文件）
    if html_path:
        try:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(generate_html_report(result))
            if result.get("success"):
                result["html_report"] = html_path
        except OSError as e:
            result["html_report_error"] = f"HTML报告写入失败: {e}"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result.get("success"):
        sys.exit(2)  # 内部错误：扫描未正常完成
    summary = result.get("summary", {})
    total_issues = summary.get("total_issues", summary.get("total", 0))
    sys.exit(1 if total_issues > 0 else 0)
