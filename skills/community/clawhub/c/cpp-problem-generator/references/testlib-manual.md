# Testlib.h 本地版本 API 快速参考手册 (v0.9.41)

> **【系统最高指令】**：在编写 `gen.cpp` (生成器) 和 `valid.cpp` (校验器) 时，必须**严格**遵守本手册提供的 API。**绝对禁止臆造任何本手册未列出的函数（例如严禁使用 `print()`）**。

## 1. 全局初始化 (Initialization)
在 `main()` 函数的第一行，必须根据程序类型进行初始化：
* **生成器 (gen.cpp)**: `registerGen(argc, argv, 1);`
* **校验器 (valid.cpp)**: `registerValidation(argc, argv);`

## 2. 命令行参数解析 (Options - 专用于 Generator)
本地版本原生支持强大的命令行参数提取：
* `has_opt("key")`：判断是否传入了名为 `key` 的参数。
* `opt<int>("n")` / `opt<long long>("m")`：获取名为 `n` 或 `m` 的整型参数。
* `opt<std::string>("type")`：获取字符串参数。
* `opt<int>(1)`：按位置索引获取参数（索引从 1 开始）。

## 3. 输出语法 (Output - 专用于 Generator)
本地 `testlib.h` 提供了现代化的输出函数：
* **`println(...)` [核心推荐]**：打印所有参数，参数间自动加空格，**并在末尾自动换行**。
    * ✅ 支持多参数：`println(n, m);` （输出：`10 20\n`）
    * ✅ 支持容器/迭代器：`println(a.begin(), a.end());` 会自动用空格分隔输出整个数组并换行。
* **🚫 绝对禁忌**：**本库不存在 `print()` 函数！** 任何情况下都严禁调用 `print()`。
* **同行连续输出**：若需在同行内循环输出且不换行，请使用标准 C++ 的 `std::cout << x << " ";`，循环结束后再 `std::cout << std::endl;`。

## 4. 随机数生成 (Random - `rnd` 对象)
在 Generator 中必须使用全局对象 `rnd` 生成随机数，严禁使用 `rand()` 或 `srand()`：
* **整数随机**：
    * `rnd.next(n)`：返回 $[0, n-1]$ 范围内的随机整数。
    * `rnd.next(L, R)`：返回 $[L, R]$ 范围内的随机整数（支持 `int` 和 `long long`）。
    * **⚠️【类型匹配铁律】**：调用 `rnd.next(L, R)` 时，传入的左右边界参数类型**必须绝对一致**！要么全是 `int`（如 `rnd.next(1, n)`），要么全是 `long long`（如 `rnd.next(1LL, (long long)n)`）。严禁 `1LL` 与 `int` 混用，否则将导致 `ambiguous` 编译致命错误！
* **浮点随机**：
    * `rnd.next()`：返回 $[0.0, 1.0)$ 范围内的随机浮点数。
* **权重随机**：
    * `rnd.wnext(L, R, w)`：带权重的随机数。$w>0$ 时偏向大数（取 $w$ 次随机数中的最大值），$w<0$ 时偏向小数。
* **高级数据结构生成**：
    * `rnd.any(container)`：从 STL 容器中随机返回一个元素。
    * `rnd.perm(size, first)`：返回一个长度为 `size` 的随机排列，元素从 `first` 开始（通常 `first=1`）。
    * `rnd.distinct(size, L, R)`：返回 `size` 个在 $[L, R]$ 范围内互不相同的随机数（返回 `std::vector`）。
    * `rnd.partition(size, sum, min_part)`：将整数 `sum` 随机拆分为 `size` 个部分，每部分至少为 `min_part`（返回 `std::vector`）。
* **正则字符串随机**：
    * `rnd.next("[a-z]{1,10}")`：生成符合正则表达式的随机字符串。
    * **⚠️【打乱数组铁律】**：在 Windows (MinGW) 环境下，`testlib` 的 `rnd` 与标准库的 `std::shuffle` 存在底层兼容性 Bug。**绝对禁止使用 `std::shuffle(..., rnd)`！** 如果需要打乱数组或生成随机排列，必须严格使用 `rnd.perm(size, first)`，或者手动写 `for` 循环配合 `swap(a[i], a[rnd.next(0, i)])` 来实现洗牌！

## 5. 格式与范围校验 (Validation - 专用于 Validator)
在 Validator 中必须使用全局对象 `inf` 进行极度严格的校验，空白字符也必须显式读取：
* **读取并校验变量**：
    * `inf.readInt(L, R, "name")`：读取整数，断言其在 $[L, R]$ 内，并在报错时提示变量名 `name`。
    * `inf.readLong(L, R, "name")`：读取 64 位整数并断言范围。
    * `inf.readDouble(L, R, "name")`：读取浮点数并断言范围。
    * `inf.readToken(regex, "name")`：读取一个符合正则表达式的字符串。
* **批量读取**：
    * `inf.readInts(size, L, R, "name")`：连续读取 `size` 个整数，每个都在 $[L, R]$ 内，自动处理元素间的空格（返回 `std::vector<int>`）。
* **严格空白符校验**：
    * `inf.readSpace()`：断言并读取一个空格字符。
    * `inf.readEoln()`：断言并读取一个换行符 (`\n`)。
    * `inf.readEof()`：断言并读取文件结束符（校验器末尾**必须**调用此方法，确保文件末尾没有多余的垃圾字符）。

### 标准 Validator 模板示例
```cpp
#include "testlib.h"

int main(int argc, char* argv[]) {
    registerValidation(argc, argv);
    int n = inf.readInt(1, 100000, "n");
    inf.readSpace();
    int m = inf.readInt(1, 100000, "m");
    inf.readEoln();
    
    inf.readInts(n, -1000, 1000, "a");
    inf.readEoln();
    
    inf.readEof(); // 必须以 EOF 断言收尾
    return 0;
}
```