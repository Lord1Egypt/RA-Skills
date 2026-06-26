#include "testlib.h"

using namespace std;

// 这里必须根据题目描述，手动硬编码最大可能的全局范围边界
const int MAX_N = 200000;

int main(int argc, char* argv[]) {
    // 铁律：必须初始化校验器
    registerValidation(argc, argv);

    // 读取第一个变量并在范围内校验
    // 参数含义：下界, 上界, 变量名 (报错时显示)
    int n = inf.readInt(1, MAX_N, "n");
    inf.readEoln(); // 铁律：该行最后一个元素读取完，必须调用换行校验！

    /* 示例：读取数组
    for (int i = 0; i < n; i++) {
        inf.readInt(1, 1000000000, "a_i");
        if (i < n - 1) inf.readSpace(); // 元素间需要空格
    }
    inf.readEoln();
    */

    // 铁律：文件末尾必须调用 readEof() 确保没有多余脏数据
    inf.readEof(); 
    return 0;
}