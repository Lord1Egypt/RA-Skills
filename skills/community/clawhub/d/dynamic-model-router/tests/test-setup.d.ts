/**
 * Jest测试全局设置
 * 在所有测试运行前执行
 */
declare global {
    namespace NodeJS {
        interface Global {
            TEST_MODE: boolean;
        }
    }
    const console: Console;
}
export {};
//# sourceMappingURL=test-setup.d.ts.map