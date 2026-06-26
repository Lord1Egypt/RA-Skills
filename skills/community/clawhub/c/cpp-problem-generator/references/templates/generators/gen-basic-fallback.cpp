#include "testlib.h"
#include <iostream>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    // 铁律：必须在第一行调用 registerGen 初始化生成器
    registerGen(argc, argv, 1);

    // 铁律：必须从命令行参数读取规模，严禁写死！
    int min_n = opt<int>("min_n");
    int max_n = opt<int>("max_n");
    
    // 动态生成规模
    int n = rnd.next(min_n, max_n);
    println(n); // 使用 println 自动处理换行

    /* 示例：生成数组
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        a[i] = rnd.next(1, 1000000000); // 使用 rnd.next()
    }
    println(a); // testlib 支持直接输出 vector，自动用空格分隔
    */

    return 0;
}