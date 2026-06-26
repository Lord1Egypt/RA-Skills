#!/usr/bin/env node
/**
 * 简化版对抗性验证
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 借口列表
const EXCUSES = [
    "代码看起来正确",
    "这是个简单变更，应该能工作",
    "我以前见过类似模式",
    "测试会发现问题",
    "我时间不够了",
    "用户在等待",
    "linter通过了",
    "Agent说成功了",
    "我累了"
];

class SimpleAdversarialVerifier {
    constructor(target, targetPath) {
        this.target = target;
        this.path = targetPath;
        this.excusesDetected = [];
        this.results = [];
    }

    // 检测借口
    detectExcuses() {
        console.log('🚨 借口检测...');
        const testThoughts = "代码看起来正确，应该能工作";
        
        for (const excuse of EXCUSES) {
            if (testThoughts.includes(excuse)) {
                this.excusesDetected.push(excuse);
                console.log(`  检测到: "${excuse}" → 做相反的事！`);
            }
        }
    }

    // 执行命令
    execute(command, description) {
        console.log(`🔧 ${description}: ${command}`);
        
        try {
            const result = execSync(command, {
                cwd: this.path,
                shell: true,
                windowsHide: true,
                encoding: 'utf8',
                timeout: 10000
            });
            
            console.log(`  ✅ 成功`);
            return { success: true, output: result };
        } catch (error) {
            console.log(`  ❌ 失败: ${error.message}`);
            return { success: false, error: error.message };
        }
    }

    // 验证前端
    verifyFrontend() {
        console.log('\n🎯 前端对抗性验证...');
        
        const packageJson = path.join(this.path, 'package.json');
        if (!fs.existsSync(packageJson)) {
            console.log('❌ 没有package.json');
            return false;
        }

        // 1. 检查package.json
        const result1 = this.execute(
            'node -e "try { const pkg = require(\'./package.json\'); console.log(\'项目:\', pkg.name) } catch(e) { console.log(\'错误:\', e.message) }"',
            '检查package.json'
        );
        this.results.push({ step: '检查package.json', ...result1 });

        // 2. 安装依赖
        const result2 = this.execute(
            'npm install --silent --no-audit --no-fund',
            '安装依赖'
        );
        this.results.push({ step: '安装依赖', ...result2 });

        // 3. 构建
        const result3 = this.execute(
            'npm run build --if-present',
            '构建项目'
        );
        this.results.push({ step: '构建项目', ...result3 });

        return this.evaluate();
    }

    // 验证CLI
    verifyCli() {
        console.log('\n🎯 CLI对抗性验证...');
        
        if (!fs.existsSync(this.path)) {
            console.log(`❌ 文件不存在: ${this.path}`);
            return false;
        }

        const fileDir = path.dirname(this.path);
        const fileName = path.basename(this.path);
        const originalCwd = this.path;
        this.path = fileDir;

        // 测试帮助
        const result1 = this.execute(
            `node "${fileName}" --help`,
            '测试帮助选项'
        );
        this.results.push({ step: '测试帮助选项', ...result1 });

        // 测试空输入
        const result2 = this.execute(
            `node "${fileName}"`,
            '测试空输入'
        );
        this.results.push({ step: '测试空输入', ...result2 });

        this.path = originalCwd;
        return this.evaluate();
    }

    // 评估结果
    evaluate() {
        const passed = this.results.filter(r => r.success).length;
        const failed = this.results.filter(r => !r.success).length;
        
        console.log(`\n📊 结果: ${passed}通过 / ${failed}失败`);
        
        if (failed > 0) {
            console.log('❌ VERIFICATION FAILED');
            return false;
        } else {
            console.log('✅ VERIFICATION PASSED');
            return true;
        }
    }

    // 运行
    run() {
        console.log('='.repeat(50));
        console.log('🔍 对抗性验证启动');
        console.log('='.repeat(50));
        
        this.detectExcuses();
        
        let result;
        if (this.target === 'frontend') {
            result = this.verifyFrontend();
        } else if (this.target === 'cli') {
            result = this.verifyCli();
        } else {
            console.log(`❌ 未知目标: ${this.target}`);
            return false;
        }
        
        console.log('='.repeat(50));
        console.log(`🎯 最终判决: ${result ? '✅ PASS' : '❌ FAIL'}`);
        console.log('='.repeat(50));
        
        return result;
    }
}

// 命令行接口
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.log('用法: node simple-verify.js <target> <path>');
        console.log('target: frontend, cli');
        process.exit(1);
    }
    
    const verifier = new SimpleAdversarialVerifier(args[0], args[1]);
    const success = verifier.run();
    
    process.exit(success ? 0 : 1);
}

module.exports = SimpleAdversarialVerifier;