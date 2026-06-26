#include "testlib.h"
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    registerGen(argc, argv, 1);
    
    int min_n = opt<int>("min_n");
    int max_n = opt<int>("max_n");
    string type = opt<string>("type");
    
    // 网格图的长宽生成
    int n = rnd.next(min_n, max_n);
    int m = rnd.next(min_n, max_n); // 若题目要求 m 与 n 不同比例，可自行调整
    
    cout << n << " " << m << endl;
    
    if (type == "random") {
        for (int i = 0; i < n; i++) {
            string row = "";
            for (int j = 0; j < m; j++) {
                // 生成只包含 0 和 1 的字符矩阵
                row += rnd.next(0, 1) ? '1' : '0';
            }
            cout << row << endl;
        }
    } 
    else if (type == "extreme") {
        // 【防退化技巧】网格图极易出现的错解，可以生成全0/全1矩阵、棋盘格矩阵等
        for (int i = 0; i < n; i++) {
            cout << string(m, '1') << endl; // 示例：生成全 1
        }
    }
    
    return 0;
}