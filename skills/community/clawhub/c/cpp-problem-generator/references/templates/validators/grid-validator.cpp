#include "testlib.h"
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    // 必须初始化校验器
    registerValidation(argc, argv);
    
    // 【警告】这里填写题目规定的最大行数和列数
    int max_n = 1000; 
    int max_m = 1000;
    
    // 读取行数和列数
    int n = inf.readInt(1, max_n, "n");
    inf.readSpace();
    int m = inf.readInt(1, max_m, "m");
    inf.readEoln(); // 行末必须读取换行符
    
    // 【核心防错技巧：网格图/矩阵严格校验法】
    // 千万不要手动用 readToken() 配合 readEoln()，极容易出现 Expected EOF 报错！
    // 强烈建议直接使用 testlib 的正则模式匹配功能：inf.readString("[字符集]{长度}", "变量名");
    // 例如下面读取 n 行只包含 0 和 1，且长度严格等于 m 的字符串：
    for (int i = 1; i <= n; i++) {
        // 这行代码会自动处理换行符，并严格校验内容格式，是最安全的做法！
        inf.readString("[01]{" + to_string(m) + "}", "grid_row_" + to_string(i));
        
        /* 如果是读取由空格隔开的数字矩阵，请改用如下写法：
        for(int j=1; j<=m; j++) {
            inf.readInt(-1e9, 1e9, "val");
            if (j < m) inf.readSpace();
        }
        inf.readEoln();
        */
    }
    
    // 必须确保文件末尾没有多余数据
    inf.readEof();
    
    return 0;
}